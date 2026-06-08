#!/usr/bin/env python3
"""Run the NGC4088 Xi_eff ablation control replay.

This is not an accepted endpoint.  It reads the frozen NGC4088 Xi_eff manifest
and compares three ablations against the existing projection/morphology curves:

1. base projection morphology,
2. additive warp/history morphology,
3. clock-only Xi_eff on the base curve,
4. Xi_eff on top of the additive curve as a double-count stress test.

The construction is frozen before scoring.  Observed velocities are read only
inside this replay script for control scoring.
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
PAPER_FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_time_projection_ablation_control_replay_not_endpoint"


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


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


def score(model_id: str, role: str, obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> dict:
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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ngc4088_time_projection_xi_eff_manifest_gate.csv").iloc[0]
    if not bool(manifest["control_manifest_allowed"]):
        raise RuntimeError("NGC4088 Xi_eff control manifest is not allowed")
    if bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("This script is a control replay, not an endpoint scorer")
    if bool(manifest["uses_vobs_or_residual"]):
        raise RuntimeError("Manifest construction used forbidden residual inputs")

    trial = pd.read_csv(DATA / "full_time_morphology_trial_galaxy_points.csv")
    g = trial.loc[trial["galaxy"].eq(GALAXY)].sort_values("r_plot_kpc").copy()
    if g.empty:
        raise RuntimeError("No NGC4088 rows in full_time_morphology_trial_galaxy_points.csv")

    epsilon_clock = float(manifest["epsilon_clock_candidate"])
    k_time = np.clip(g["K_full_time_morph_phase"].to_numpy(dtype=float), 0.0, None)
    xi_eff = 1.0 + epsilon_clock * k_time

    obs = g["vobs_plot_km_s"].to_numpy(dtype=float)
    err = g["err_plot_km_s"].to_numpy(dtype=float)
    base = g["v_base_plot_km_s"].to_numpy(dtype=float)
    additive = g["v_full_time_morphology_km_s"].to_numpy(dtype=float)
    clock_only = xi_eff * base
    additive_plus_clock = xi_eff * additive

    points = pd.DataFrame(
        {
            "galaxy": GALAXY,
            "r_kpc": g["r_plot_kpc"].to_numpy(dtype=float),
            "vobs_km_s": obs,
            "err_km_s": err,
            "v_base_projection_km_s": base,
            "v_additive_warp_history_km_s": additive,
            "K_time_shape_source_frozen": k_time,
            "epsilon_clock_candidate": epsilon_clock,
            "Xi_eff_clock": xi_eff,
            "v_clock_only_on_base_km_s": clock_only,
            "v_additive_plus_clock_stress_km_s": additive_plus_clock,
            "construction_used_vobs": False,
            "scoring_used_vobs": True,
            "endpoint_validation_claim": False,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    scores = pd.DataFrame(
        [
            score("N4088_BASE_PROJECTION", "reference", obs, base, err),
            score("N4088_ADDITIVE_WARP_HISTORY", "additive_reference", obs, additive, err),
            score("N4088_XIEFF_CLOCK_ONLY_ON_BASE", "clock_ablation_control", obs, clock_only, err),
            score(
                "N4088_ADDITIVE_PLUS_XIEFF_STRESS",
                "double_count_stress_control",
                obs,
                additive_plus_clock,
                err,
            ),
        ]
    ).sort_values("rmse_km_s")

    additive_rmse = float(scores.loc[scores["model_id"].eq("N4088_ADDITIVE_WARP_HISTORY"), "rmse_km_s"].iloc[0])
    clock_rmse = float(scores.loc[scores["model_id"].eq("N4088_XIEFF_CLOCK_ONLY_ON_BASE"), "rmse_km_s"].iloc[0])
    stress_rmse = float(scores.loc[scores["model_id"].eq("N4088_ADDITIVE_PLUS_XIEFF_STRESS"), "rmse_km_s"].iloc[0])
    base_rmse = float(scores.loc[scores["model_id"].eq("N4088_BASE_PROJECTION"), "rmse_km_s"].iloc[0])

    if clock_rmse < additive_rmse:
        interpretation = "CLOCK_ONLY_BEATS_ADDITIVE_CONTROL"
    elif stress_rmse < additive_rmse:
        interpretation = "ADDITIVE_PLUS_CLOCK_IMPROVES_BUT_DOUBLE_COUNT_BLOCKED"
    elif clock_rmse < base_rmse:
        interpretation = "CLOCK_ONLY_IMPROVES_BASE_BUT_NOT_ADDITIVE"
    else:
        interpretation = "CLOCK_LAYER_NOT_COMPETITIVE_IN_CONTROL_REPLAY"

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4088_ABL_G1_MANIFEST_FROZEN",
                "gate_status": "PASS",
                "evidence": str(manifest["manifest_status"]),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "N4088_ABL_G2_ENDPOINT_BLIND_CONSTRUCTION",
                "gate_status": "PASS",
                "evidence": "scoring script reads vobs only after manifest construction",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "N4088_ABL_G3_DOUBLE_COUNT_NOT_RESOLVED",
                "gate_status": "BLOCKED",
                "evidence": "additive_plus_clock remains stress test, not accepted endpoint model",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "ablation_replay_status": "NGC4088_XIEFF_ABLATION_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "epsilon_clock_candidate": epsilon_clock,
                "best_control_model": str(scores.iloc[0]["model_id"]),
                "best_control_rmse_km_s": float(scores.iloc[0]["rmse_km_s"]),
                "base_rmse_km_s": base_rmse,
                "additive_rmse_km_s": additive_rmse,
                "clock_only_rmse_km_s": clock_rmse,
                "additive_plus_clock_rmse_km_s": stress_rmse,
                "interpretation": interpretation,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_step": "if clock-only is useful, build a separate accepted clock-only endpoint route; otherwise keep Xi_eff as diagnostic/control",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points.to_csv(DATA / "ngc4088_time_projection_ablation_control_points.csv", index=False)
    scores.to_csv(DATA / "ngc4088_time_projection_ablation_control_scores.csv", index=False)
    gates.to_csv(DATA / "ngc4088_time_projection_ablation_control_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4088_time_projection_ablation_control_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9.0, 5.2))
    ax.errorbar(points["r_kpc"], points["vobs_km_s"], yerr=points["err_km_s"], fmt="o", color="black", ms=4, lw=0.8, label="observed")
    ax.plot(points["r_kpc"], points["v_base_projection_km_s"], color="#64748b", lw=1.8, label="base projection")
    ax.plot(points["r_kpc"], points["v_additive_warp_history_km_s"], color="#2563eb", lw=2.2, label="additive warp/history")
    ax.plot(points["r_kpc"], points["v_clock_only_on_base_km_s"], color="#f97316", lw=2.0, label="Xi_eff clock only")
    ax.plot(points["r_kpc"], points["v_additive_plus_clock_stress_km_s"], color="#dc2626", lw=1.8, ls="--", label="additive + Xi_eff stress")
    ax.set_title("NGC4088 time-projection ablation control replay")
    ax.set_xlabel("Radius [kpc]")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig_path = FIGURES / "ngc4088_time_projection_ablation_control_replay.png"
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)
    paper_path = PAPER_FIGURES / "fig24_ngc4088_time_projection_ablation_control_replay.png"
    paper_path.write_bytes(fig_path.read_bytes())

    report = "\n".join(
        [
            "# NGC4088 Time-Projection Ablation Control Replay",
            "",
            "This is a control replay, not an accepted endpoint.  The manifest was",
            "frozen before scoring; observed velocities are used only inside this",
            "script to compute control RMSEs.",
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
            "## Claim Boundary",
            "",
            "The additive-plus-clock curve is explicitly a double-count stress test.",
            "It cannot be promoted until the clock/readout channel is separated from",
            "the additive warp-history morphology kernel by a predeclared endpoint",
            "route.",
            "",
            f"Figure: `{fig_path}`",
            "",
        ]
    )
    (REPORTS / "ngc4088_time_projection_ablation_control_replay.md").write_text(
        report, encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
