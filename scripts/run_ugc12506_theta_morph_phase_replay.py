#!/usr/bin/env python3
"""Compute a UGC12506 trajectory/phase-enriched diagnostic replay.

This is a K^(2)-style source-side test:

    K(R; K_present, O_obs/path, Theta_morph)

The added Theta_morph term is not inferred from the rotation residual.  It uses
the residual-blind UGC12506 source context already cached from SPARC and
Hallenbeck et al. 2014: high inclination, high spin, extended low-density H I,
and mild H I extent asymmetry.  The output is diagnostic/preflight only, not
endpoint validation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "figures" / "endpoint_diagnostics"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_theta_morph_phase_replay_diagnostic_not_validation"


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def normalized(x: np.ndarray) -> np.ndarray:
    m = float(np.max(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def score(model_id: str, role: str, obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> dict[str, object]:
    return {
        "galaxy": GALAXY,
        "model_id": model_id,
        "model_role": role,
        "n_points": int(len(obs)),
        "rmse_km_s": rmse(obs, pred),
        "weighted_rmse_km_s": wrmse(obs, pred, err),
        "mae_km_s": mae(obs, pred),
        "bias_km_s": float(np.mean(pred - obs)),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    obs_df = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    values = obs_df.set_index("symbol")["value"].to_dict()
    if bool(obs_df["uses_vobs_or_residual"].any()):
        raise RuntimeError("Source observable table is not residual-blind")

    base_summary = pd.read_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_summary.csv").iloc[0]
    if bool(base_summary["construction_used_vobs_or_residual"]):
        raise RuntimeError("Input projection-history shell is not residual-blind")

    grid = pd.read_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc").reset_index(drop=True)
    if bool(grid["construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Input grid is not residual-blind")

    r = grid["radius_kpc"].to_numpy(dtype=float)
    obs = grid["vobs_kms"].to_numpy(dtype=float)
    err = grid["errv_kms"].to_numpy(dtype=float)
    baryon = grid["v_baryon_050_kms"].to_numpy(dtype=float)
    source_native = grid["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    projection_history = grid["v_projection_history_incremental_positive_kms"].to_numpy(dtype=float)

    i_deg = float(values["i"])
    rd_kpc = float(values["R_d"])
    rhi_kpc = float(values["R_HI_source"])
    ropt_kpc = float(values["R_opt"])
    lambda_spin = float(values["lambda_spin"])
    extent_asymmetry = float(values["A_extent"])

    sin2_i = float(np.sin(np.deg2rad(i_deg)) ** 2)
    q_spin = float(np.clip(lambda_spin / 0.15, 0.0, 1.0))
    q_low_density_stability = 0.4
    q_asymmetry_phase = float(np.clip(extent_asymmetry / 0.25, 0.0, 1.0))
    theta_load = sin2_i * q_spin * (0.65 * q_low_density_stability + 0.35 * q_asymmetry_phase)
    gamma_theta = theta_load / (1.0 + theta_load)

    outer_window = smoothstep((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6))
    post_optical_window = smoothstep((r - ropt_kpc) / max(rhi_kpc - ropt_kpc, 1.0e-6))
    late_settling_shape = outer_window * (0.7 + 0.3 * post_optical_window) * np.sqrt(
        np.clip(r / max(rhi_kpc, 1.0e-6), 0.0, 1.0)
    )
    k_theta = normalized(late_settling_shape)

    base_v2 = grid["v2_projection_history_incremental_positive_km2_s2"].to_numpy(dtype=float)
    scale_col = "v2_source_native_nfw_hse_positive_km2_s2"
    outer_scale = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), scale_col].median())
    amplitude_theta = gamma_theta * outer_scale
    v2_theta = base_v2 + amplitude_theta * k_theta
    v_theta = np.sqrt(np.maximum(v2_theta, 0.0))

    out = grid.copy()
    out["K_theta_morph_phase_late_settling"] = k_theta
    out["theta_morph_phase_load"] = theta_load
    out["gamma_theta_morph_phase"] = gamma_theta
    out["A_theta_morph_phase_km2_s2"] = amplitude_theta
    out["v2_theta_morph_phase_positive_km2_s2"] = v2_theta
    out["v_theta_morph_phase_positive_kms"] = v_theta
    out["theta_construction_used_vobs_or_residual"] = False
    out["theta_endpoint_validation_claim"] = False
    out["theta_claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            score("BARYONIC_CARRIER_V050", "carrier_reference", obs, baryon, err),
            score("UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE", "source_native_base_reference", obs, source_native, err),
            score(
                "UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE",
                "projection_history_reference",
                obs,
                projection_history,
                err,
            ),
            score(
                "UGC12506_THETA_MORPH_PHASE_POSITIVE",
                "trajectory_phase_enriched_diagnostic",
                obs,
                v_theta,
                err,
            ),
        ]
    )
    prior_path = DATA / "multigalaxy_fit_inspection_scores.csv"
    if prior_path.exists():
        prior = pd.read_csv(prior_path)
        prior = prior.loc[prior["galaxy"].eq(GALAXY)].copy()
        for _, row in prior.iterrows():
            scores.loc[len(scores)] = {
                "galaxy": GALAXY,
                "model_id": f"PRIOR_DIAGNOSTIC_{row['model_id']}",
                "model_role": "prior_diagnostic_reference_not_same_carrier",
                "n_points": int(row["n_points"]),
                "rmse_km_s": float(row["rmse_kms"]),
                "weighted_rmse_km_s": np.nan,
                "mae_km_s": float(row["mae_kms"]),
                "bias_km_s": float(row["bias_kms"]),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "claim_boundary": "prior_multigalaxy_fit_inspection_reference_not_endpoint_validation",
            }
    scores = scores.sort_values("rmse_km_s").reset_index(drop=True)

    theta_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_THETA_MORPH_PHASE_POSITIVE"), "rmse_km_s"].iloc[0])
    ph_rmse = float(
        scores.loc[scores["model_id"].eq("UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE"), "rmse_km_s"].iloc[0]
    )
    sn_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE"), "rmse_km_s"].iloc[0])
    carrier_rmse = float(scores.loc[scores["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0])
    best = scores.iloc[0]
    status = (
        "UGC12506_THETA_MORPH_PHASE_IMPROVES_PROJECTION_HISTORY_DIAGNOSTIC"
        if theta_rmse < ph_rmse
        else "UGC12506_THETA_MORPH_PHASE_DOES_NOT_IMPROVE_PROJECTION_HISTORY"
    )

    summary = pd.DataFrame(
        [
            {
                "diagnostic_status": status,
                "galaxy": GALAXY,
                "n_points": int(len(out)),
                "carrier_rmse_km_s": carrier_rmse,
                "source_native_nfw_hse_rmse_km_s": sn_rmse,
                "projection_history_rmse_km_s": ph_rmse,
                "theta_morph_phase_rmse_km_s": theta_rmse,
                "theta_minus_projection_history_rmse_km_s": theta_rmse - ph_rmse,
                "theta_minus_source_native_rmse_km_s": theta_rmse - sn_rmse,
                "best_scored_model": str(best["model_id"]),
                "best_scored_rmse_km_s": float(best["rmse_km_s"]),
                "theta_load": theta_load,
                "gamma_theta": gamma_theta,
                "q_spin": q_spin,
                "q_low_density_stability": q_low_density_stability,
                "q_asymmetry_phase": q_asymmetry_phase,
                "amplitude_theta_km2_s2": amplitude_theta,
                "formula_text": (
                    "v_theta^2(R)=v_projection_history^2(R)+A_theta K_theta(R); "
                    "K_theta is source-frozen late-settling morphology phase"
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_THETA_G1_SOURCE_PROXY",
                "gate_status": "PASS_DIAGNOSTIC_SOURCE_SUPPORTED",
                "evidence": "lambda_spin=0.15, extended low-density H I, high inclination, and mild H I asymmetry",
                "endpoint_claim_allowed": False,
            },
            {
                "gate_id": "U12506_THETA_G2_NO_BACKWARD_CAUSAL_CLAIM",
                "gate_status": "PASS_CLAIM_BOUNDARY",
                "evidence": "Theta_morph is treated as trajectory/phase, not future-to-present 4D causality",
                "endpoint_claim_allowed": False,
            },
            {
                "gate_id": "U12506_THETA_G3_RESIDUAL_BLIND_CONSTRUCTION",
                "gate_status": "PASS",
                "evidence": "kernel, load, sign, and amplitude use source observables and source-native carrier scale",
                "endpoint_claim_allowed": False,
            },
            {
                "gate_id": "U12506_THETA_G4_STATUS",
                "gate_status": "DIAGNOSTIC_ONLY",
                "evidence": "theta phase proxy is not yet accepted population observable",
                "endpoint_claim_allowed": False,
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["claim_boundary"] = CLAIM_BOUNDARY

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8.8, 7.2), sharex=True, gridspec_kw={"height_ratios": [2.4, 1.0]})
    ax.errorbar(r, obs, yerr=err, fmt="o", ms=4, lw=0.8, color="black", label="observed")
    ax.plot(r, baryon, color="#888888", lw=1.6, label="Newtonian/baryonic")
    ax.plot(r, source_native, color="#b2182b", lw=1.9, label="source-native NFW-HSE")
    ax.plot(r, projection_history, color="#5e3c99", lw=2.2, label="projection-history K^(1)/partial K^(2)")
    ax.plot(r, v_theta, color="#008b8b", lw=2.5, label="theta_morph phase diagnostic")
    ax.set_title("UGC12506 trajectory/phase-enriched diagnostic rotation curve")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2)

    ax2.axhline(0.0, color="#999999", lw=1.0)
    ax2.plot(r, v_theta - projection_history, color="#008b8b", lw=2.0, label="theta increment over projection-history")
    ax2.plot(r, obs - projection_history, color="#333333", lw=1.2, alpha=0.8, label="observed minus projection-history")
    ax2.set_xlabel("Radius [kpc]")
    ax2.set_ylabel("Delta v [km/s]")
    ax2.grid(True, alpha=0.25)
    ax2.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_theta_morph_phase_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    out.to_csv(DATA / "ugc12506_theta_morph_phase_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_theta_morph_phase_replay_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_theta_morph_phase_replay_summary.csv", index=False)
    gates.to_csv(DATA / "ugc12506_theta_morph_phase_replay_gates.csv", index=False)

    report = [
        "# UGC12506 Theta Morphology Phase Replay",
        "",
        "This diagnostic computes a trajectory/phase-enriched UGC12506 rotation curve.",
        "The construction does not treat future-directed morphology as backward",
        "causality. It treats `Theta_morph` as a source-frozen trajectory/phase",
        "proxy supported by high spin, extended low-density H I, high inclination,",
        "and mild H I extent asymmetry.",
        "",
        "Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT_VALIDATION`.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Figure",
        "",
        f"![UGC12506 theta morphology phase replay]({figure_path})",
        "",
        "## Claim boundary",
        "",
        "A positive or negative score here is kernel-development evidence only.",
        "The trajectory/phase proxy must still be promoted to an accepted",
        "source-side observable before endpoint-style claims.",
    ]
    (REPORTS / "ugc12506_theta_morph_phase_replay.md").write_text("\n".join(report) + "\n")

    print(summary.to_string(index=False))
    print(f"wrote {figure_path}")


if __name__ == "__main__":
    main()
