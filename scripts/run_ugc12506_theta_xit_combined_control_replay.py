#!/usr/bin/env python3
"""Run the UGC12506 Theta_morph + Xi_t combined-control replay.

This is not an endpoint.  It is allowed only because the source-nonoverlap
ledger freezes which ingredients can count in each channel:

* Theta_morph supplies the additive late-settling morphology phase curve.
* Xi_t supplies a small clock/readout interval cap.
* The shaped Xi_t kernel remains a caveated shared-context stress control.

Observed velocities are read only in the scoring section after the source-side
ledger and manifests are frozen.
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
CLAIM_BOUNDARY = "ugc12506_theta_xit_combined_control_replay_not_endpoint"


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


def score_row(
    model_id: str,
    role: str,
    obs: np.ndarray,
    pred: np.ndarray,
    err: np.ndarray,
    *,
    channel_policy: str,
) -> dict[str, object]:
    return {
        "galaxy": GALAXY,
        "model_id": model_id,
        "model_role": role,
        "channel_policy": channel_policy,
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
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    nonoverlap = pd.read_csv(DATA / "ugc12506_theta_xit_source_nonoverlap_summary.csv").iloc[0]
    ledger = pd.read_csv(DATA / "ugc12506_theta_xit_source_nonoverlap_ledger.csv")
    theta = pd.read_csv(DATA / "ugc12506_theta_morph_phase_replay_points.csv")
    xi = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_points.csv")
    xi_manifest = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_manifest.csv").iloc[0]

    if not bool(nonoverlap["combined_control_replay_allowed"]):
        raise RuntimeError("Combined-control replay is not allowed by the nonoverlap gate")
    if bool(nonoverlap["combined_endpoint_allowed"]):
        raise RuntimeError("This script must not run as a combined endpoint")
    if bool(nonoverlap["endpoint_validation_claim"]):
        raise RuntimeError("Nonoverlap gate unexpectedly claims endpoint validation")
    if bool(theta["theta_construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Theta_morph construction used forbidden observed residual inputs")
    if bool(xi_manifest["uses_vobs_or_residual"]):
        raise RuntimeError("Xi_t manifest used forbidden observed residual inputs")
    if not ledger["assignment"].eq("THETA_ONLY").any():
        raise RuntimeError("Missing Theta-only ledger assignment")
    if not ledger["assignment"].eq("XIT_ONLY_PROTOCOL_CAP").any():
        raise RuntimeError("Missing Xi_t-only protocol-cap assignment")

    t = theta.sort_values("radius_kpc").reset_index(drop=True)
    x = xi.sort_values("radius_kpc").reset_index(drop=True)
    if not np.allclose(t["radius_kpc"].to_numpy(float), x["radius_kpc"].to_numpy(float)):
        raise RuntimeError("Theta and Xi_t grids do not share the same radial grid")

    r = t["radius_kpc"].to_numpy(dtype=float)
    obs = t["vobs_kms"].to_numpy(dtype=float)
    err = t["errv_kms"].to_numpy(dtype=float)
    baryon = t["v_baryon_050_kms"].to_numpy(dtype=float)
    source_native = t["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    projection_history = t["v_projection_history_incremental_positive_kms"].to_numpy(dtype=float)
    theta_v = t["v_theta_morph_phase_positive_kms"].to_numpy(dtype=float)
    theta_v2 = t["v2_theta_morph_phase_positive_km2_s2"].to_numpy(dtype=float)

    epsilon_max = float(xi_manifest["epsilon_t_interval_max"])
    xi_cap_only = 1.0 + epsilon_max
    k_t_shared = np.clip(x["K_t_highspin_envelope_clock"].to_numpy(dtype=float), 0.0, None)
    xi_shared_max = 1.0 + epsilon_max * k_t_shared
    xi_shared_mid = 1.0 + 0.5 * epsilon_max * k_t_shared

    # Ledger-strict path: Xi_t contributes only its own small-mismatch cap.
    v_combined_cap_only = xi_cap_only * theta_v
    # Caveated stress paths: reuse the shaped K_t(R), explicitly flagged as
    # shared-context control rather than endpoint permission.
    v_combined_shared_mid = xi_shared_mid * theta_v
    v_combined_shared_high = xi_shared_max * theta_v

    points = t.copy()
    points["Xi_t_cap_only_uniform"] = xi_cap_only
    points["Xi_t_shared_context_mid"] = xi_shared_mid
    points["Xi_t_shared_context_high"] = xi_shared_max
    points["v2_theta_xit_cap_only_control_km2_s2"] = np.square(v_combined_cap_only)
    points["v_theta_xit_cap_only_control_kms"] = v_combined_cap_only
    points["v2_theta_xit_shared_mid_control_km2_s2"] = np.square(v_combined_shared_mid)
    points["v_theta_xit_shared_mid_control_kms"] = v_combined_shared_mid
    points["v2_theta_xit_shared_high_control_km2_s2"] = np.square(v_combined_shared_high)
    points["v_theta_xit_shared_high_control_kms"] = v_combined_shared_high
    points["theta_xit_combined_control_used_vobs_for_scoring_only"] = True
    points["endpoint_validation_claim"] = False
    points["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            score_row(
                "NEWTONIAN_BARYONIC_V050",
                "baseline_reference",
                obs,
                baryon,
                err,
                channel_policy="reference_only",
            ),
            score_row(
                "UGC12506_SOURCE_NATIVE_NFW_HSE",
                "source_native_reference",
                obs,
                source_native,
                err,
                channel_policy="reference_only",
            ),
            score_row(
                "UGC12506_PROJECTION_HISTORY",
                "projection_history_reference",
                obs,
                projection_history,
                err,
                channel_policy="reference_only",
            ),
            score_row(
                "UGC12506_THETA_MORPH_PHASE",
                "theta_additive_diagnostic_base",
                obs,
                theta_v,
                err,
                channel_policy="theta_only_late_settling_shape",
            ),
            score_row(
                "UGC12506_THETA_XIT_CAP_ONLY_COMBINED_CONTROL",
                "ledger_strict_combined_control",
                obs,
                v_combined_cap_only,
                err,
                channel_policy="theta_only_shape_plus_xit_only_cap",
            ),
            score_row(
                "UGC12506_THETA_XIT_SHARED_KT_MID_STRESS_CONTROL",
                "shared_context_stress_control_mid",
                obs,
                v_combined_shared_mid,
                err,
                channel_policy="theta_shape_plus_caveated_shared_context_xit_shape",
            ),
            score_row(
                "UGC12506_THETA_XIT_SHARED_KT_HIGH_STRESS_CONTROL",
                "shared_context_stress_control_high",
                obs,
                v_combined_shared_high,
                err,
                channel_policy="theta_shape_plus_caveated_shared_context_xit_shape",
            ),
        ]
    ).sort_values("rmse_km_s")

    theta_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_THETA_MORPH_PHASE"), "rmse_km_s"].iloc[0])
    cap_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_THETA_XIT_CAP_ONLY_COMBINED_CONTROL"),
            "rmse_km_s",
        ].iloc[0]
    )
    shared_high_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_THETA_XIT_SHARED_KT_HIGH_STRESS_CONTROL"),
            "rmse_km_s",
        ].iloc[0]
    )
    best = scores.iloc[0]
    control_status = (
        "U12506_THETA_XIT_COMBINED_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT"
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_COMBINED_G1_NONOVERLAP_LEDGER",
                "gate_status": "PASS_CONTROL_ONLY",
                "evidence": str(nonoverlap["nonoverlap_status"]),
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U12506_COMBINED_G2_LEDGER_STRICT_ROUTE",
                "gate_status": "PASS_CONTROL_ONLY",
                "evidence": "Theta-only late-settling shape plus Xi_t-only epsilon cap",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U12506_COMBINED_G3_SHARED_KT_ROUTE",
                "gate_status": "CAVEATED_STRESS_CONTROL_ONLY",
                "evidence": "shaped K_t(R) still uses shared source context",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U12506_COMBINED_G4_ENDPOINT_BOUNDARY",
                "gate_status": "BLOCK_ENDPOINT",
                "evidence": "combined_endpoint_allowed=False in nonoverlap summary",
                "endpoint_scores_allowed": False,
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "combined_control_status": control_status,
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "epsilon_t_cap": epsilon_max,
                "theta_rmse_km_s": theta_rmse,
                "combined_cap_only_rmse_km_s": cap_rmse,
                "combined_shared_kt_high_rmse_km_s": shared_high_rmse,
                "cap_only_minus_theta_rmse_km_s": cap_rmse - theta_rmse,
                "shared_kt_high_minus_theta_rmse_km_s": shared_high_rmse - theta_rmse,
                "best_scored_model": str(best["model_id"]),
                "best_scored_rmse_km_s": float(best["rmse_km_s"]),
                "combined_control_replay_allowed": True,
                "combined_endpoint_allowed": False,
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(DATA / "ugc12506_theta_xit_combined_control_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_theta_xit_combined_control_replay_scores.csv", index=False)
    gates.to_csv(DATA / "ugc12506_theta_xit_combined_control_replay_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_theta_xit_combined_control_replay_summary.csv", index=False)

    fig, (ax, ax2) = plt.subplots(
        2,
        1,
        figsize=(9.6, 7.2),
        sharex=True,
        gridspec_kw={"height_ratios": [2.4, 1.0]},
    )
    ax.errorbar(r, obs, yerr=err, fmt="o", color="black", ms=4, lw=0.8, label="observed")
    ax.plot(r, baryon, color="#777777", lw=1.3, ls="--", label="Newtonian baryonic")
    ax.plot(r, projection_history, color="#5e3c99", lw=1.9, label="projection-history base")
    ax.plot(r, theta_v, color="#008b8b", lw=2.3, label=r"$\Theta_{\rm morph}$")
    ax.plot(
        r,
        v_combined_cap_only,
        color="#e66101",
        lw=2.2,
        label=r"$\Theta_{\rm morph}$ + ledger-strict $\Xi_t$ cap",
    )
    ax.plot(
        r,
        v_combined_shared_high,
        color="#b2182b",
        lw=1.7,
        ls=":",
        label=r"shared-context $K_t$ stress control",
    )
    ax.set_title("UGC12506 Theta_morph + Xi_t combined-control replay")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8, ncol=2)

    ax2.axhline(0.0, color="#999999", lw=1.0)
    ax2.plot(r, obs - theta_v, color="#008b8b", lw=1.7, label="obs - Theta_morph")
    ax2.plot(
        r,
        obs - v_combined_cap_only,
        color="#e66101",
        lw=1.7,
        label="obs - combined cap-only",
    )
    ax2.plot(
        r,
        obs - v_combined_shared_high,
        color="#b2182b",
        lw=1.3,
        ls=":",
        label="obs - shared-context stress",
    )
    ax2.set_xlabel("Radius [kpc]")
    ax2.set_ylabel("Residual [km/s]")
    ax2.grid(alpha=0.25)
    ax2.legend(fontsize=8, ncol=2)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_theta_xit_combined_control_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    report = [
        "# UGC12506 Theta_morph + Xi_t Combined-Control Replay",
        "",
        "This replay is controlled by the source-nonoverlap ledger. It is not an endpoint.",
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
        "## Ledger interpretation",
        "",
        "The primary combined-control curve uses the Theta_morph late-settling shape",
        "and only the Xi_t protocol cap.  The shaped K_t curve is retained as a",
        "caveated stress control because the current K_t shape still uses shared",
        "high-spin/envelope/asymmetry source context.",
        "",
        "## Figure",
        "",
        f"![UGC12506 combined control replay]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_theta_xit_combined_control_replay.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(summary.to_string(index=False))
    print(f"wrote {figure_path}")


if __name__ == "__main__":
    main()
