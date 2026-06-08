#!/usr/bin/env python3
"""Run the UGC12506 Xi_t caveated interval/control replay.

This script is deliberately not a standard endpoint.  It reads the frozen
caveated interval/control manifest and then scores only the predeclared control
band:

    v_low(R)  = v_base(R)
    v_high(R) = Xi_t,max(R) v_base(R)

The scoring stage reads observed rotation data only after the source-side
manifest has been frozen.  The interval-clipped curve is reported as a coverage
diagnostic, not as a fitted model.
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
CLAIM_BOUNDARY = "ugc12506_xi_t_caveated_interval_control_replay_not_endpoint"


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


def score_row(
    model_id: str,
    role: str,
    obs: np.ndarray,
    pred: np.ndarray,
    err: np.ndarray,
    *,
    diagnostic_clipped_to_obs: bool = False,
) -> dict[str, object]:
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
        "diagnostic_clipped_to_obs": diagnostic_clipped_to_obs,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_manifest.csv").iloc[0]
    if manifest["manifest_kind"] != "caveated_interval_control":
        raise RuntimeError("UGC12506 Xi_t control replay requires a caveated interval/control manifest")
    if bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("Control replay must not run as standard endpoint scoring")
    if bool(manifest["uses_vobs_or_residual"]):
        raise RuntimeError("Control manifest used forbidden vobs/residual inputs")

    grid = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 Xi_t shell grid")
    if bool(grid["construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Frozen Xi_t grid used forbidden vobs/residual inputs")

    r = grid["radius_kpc"].to_numpy(dtype=float)
    obs = grid["vobs_kms"].to_numpy(dtype=float)
    err = grid["errv_kms"].to_numpy(dtype=float)
    baryon = grid["v_baryon_050_kms"].to_numpy(dtype=float)
    base = grid["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    k_t = np.clip(grid["K_t_highspin_envelope_clock"].to_numpy(dtype=float), 0.0, None)
    epsilon_max = float(manifest["epsilon_t_interval_max"])
    epsilon_mid = 0.5 * epsilon_max
    xi_mid = 1.0 + epsilon_mid * k_t
    xi_max = 1.0 + epsilon_max * k_t

    v_low = base
    v_mid = xi_mid * base
    v_high = xi_max * base
    v_interval_clipped = np.clip(obs, np.minimum(v_low, v_high), np.maximum(v_low, v_high))
    inside_interval = (obs >= np.minimum(v_low, v_high)) & (obs <= np.maximum(v_low, v_high))
    inside_interval_with_err = (
        (obs + err >= np.minimum(v_low, v_high))
        & (obs - err <= np.maximum(v_low, v_high))
    )

    points = grid.copy()
    points["Xi_t_control_mid"] = xi_mid
    points["Xi_t_control_max"] = xi_max
    points["v_xi_t_control_low_kms"] = v_low
    points["v_xi_t_control_mid_kms"] = v_mid
    points["v_xi_t_control_high_kms"] = v_high
    points["v_xi_t_interval_clipped_diagnostic_kms"] = v_interval_clipped
    points["obs_inside_xi_t_interval"] = inside_interval
    points["obs_inside_xi_t_interval_with_err"] = inside_interval_with_err
    points["control_replay_used_vobs_for_scoring_only"] = True
    points["endpoint_validation_claim"] = False
    points["claim_boundary"] = CLAIM_BOUNDARY

    scores = pd.DataFrame(
        [
            score_row("NEWTONIAN_BARYONIC_V050", "baseline_reference", obs, baryon, err),
            score_row("UGC12506_XIT_CONTROL_LOW_EPS0", "control_interval_lower_edge", obs, v_low, err),
            score_row("UGC12506_XIT_CONTROL_MID", "control_interval_midpoint", obs, v_mid, err),
            score_row("UGC12506_XIT_CONTROL_HIGH", "control_interval_upper_edge", obs, v_high, err),
            score_row(
                "UGC12506_XIT_INTERVAL_CLIPPED_DIAGNOSTIC",
                "best_possible_within_frozen_interval_not_model",
                obs,
                v_interval_clipped,
                err,
                diagnostic_clipped_to_obs=True,
            ),
        ]
    ).sort_values("rmse_km_s")

    low_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_XIT_CONTROL_LOW_EPS0"), "rmse_km_s"].iloc[0])
    high_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_XIT_CONTROL_HIGH"), "rmse_km_s"].iloc[0])
    mid_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_XIT_CONTROL_MID"), "rmse_km_s"].iloc[0])
    clipped_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_XIT_INTERVAL_CLIPPED_DIAGNOSTIC"),
            "rmse_km_s",
        ].iloc[0]
    )
    best_edge = min(low_rmse, mid_rmse, high_rmse)
    improvement = low_rmse - min(mid_rmse, high_rmse)

    summary = pd.DataFrame(
        [
            {
                "control_replay_status": "U12506_XI_T_CAVEATED_INTERVAL_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "epsilon_t_max": epsilon_max,
                "xi_t_max_max": float(np.max(xi_max)),
                "control_low_rmse_km_s": low_rmse,
                "control_mid_rmse_km_s": mid_rmse,
                "control_high_rmse_km_s": high_rmse,
                "best_control_edge_rmse_km_s": best_edge,
                "rmse_improvement_vs_low_km_s": improvement,
                "interval_clipped_diagnostic_rmse_km_s": clipped_rmse,
                "obs_inside_interval_fraction": float(np.mean(inside_interval)),
                "obs_inside_interval_with_err_fraction": float(np.mean(inside_interval_with_err)),
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
                "gate_id": "U12506_XIT_REPLAY_G1_MANIFEST_KIND",
                "gate_status": "PASS",
                "evidence": str(manifest["manifest_kind"]),
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_REPLAY_G2_ENDPOINT_BLOCK",
                "gate_status": "PASS_RECORDED",
                "evidence": "endpoint_scores_allowed=False",
                "remaining_obligation": "do not report as endpoint validation",
            },
            {
                "gate_id": "U12506_XIT_REPLAY_G3_SCORING_SEPARATION",
                "gate_status": "PASS",
                "evidence": "manifest/grid construction forbids vobs; this script reads vobs only for control scoring",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_REPLAY_G4_INTERVAL_CLAIM_BOUNDARY",
                "gate_status": "PASS_RECORDED",
                "evidence": "interval-clipped curve is diagnostic only and marked as such",
                "remaining_obligation": "separate endpoint-permission gate before endpoint claim",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    points.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_scores.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9.5, 5.3))
    ax.errorbar(r, obs, yerr=err, fmt="o", color="black", ms=4, lw=0.8, label="observed")
    ax.plot(r, baryon, color="#777777", lw=1.5, ls="--", label="Newtonian baryonic")
    ax.plot(r, v_low, color="#6a3d9a", lw=2.0, label=r"$\Xi_t$ interval low ($\epsilon_t=0$)")
    ax.plot(r, v_high, color="#e66101", lw=2.2, label=r"$\Xi_t$ interval high")
    ax.fill_between(r, v_low, v_high, color="#e66101", alpha=0.16, label=r"caveated $\Xi_t$ control interval")
    ax.plot(
        r,
        v_interval_clipped,
        color="#1b9e77",
        lw=1.5,
        ls=":",
        label="interval-clipped diagnostic bound",
    )
    ax.set_title("UGC12506 caveated Xi_t interval/control replay")
    ax.set_xlabel("Radius [kpc]")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(alpha=0.25)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig_path = FIGURES / "ugc12506_xi_t_caveated_interval_control_replay.png"
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Caveated Interval/Control Replay",
            "",
            "This is a control replay, not a standard endpoint validation.",
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
            "The lower, midpoint, and upper curves are fixed by the source-reviewed caveated interval/control manifest. The interval-clipped diagnostic reports the best possible within-band residual and is not a fitted model.",
            "",
            f"![UGC12506 Xi_t control replay]({fig_path})",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_caveated_interval_control_replay.md").write_text(
        report,
        encoding="utf-8",
    )
    print(summary.to_string(index=False))
    print(f"wrote {fig_path}")


if __name__ == "__main__":
    main()
