#!/usr/bin/env python3
"""Diagnostic Xi_t time-readout replay on trial galaxies.

The run is intentionally conservative.  It does not fit Xi_t from the rotation
residual.  Each galaxy receives a small source-status epsilon scale, and the
radial shape is inherited from the already source-frozen phase/projection
kernel.  This tests directionality only; it is not endpoint validation.
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
CLAIM_BOUNDARY = "time_readout_xi_trial_diagnostic_not_endpoint_validation"


EPSILON_CAP = 0.035


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray | None) -> float:
    if err is None:
        return float("nan")
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for col in display.columns:
        if pd.api.types.is_float_dtype(display[col]):
            display[col] = display[col].map(lambda v: f"{v:.6g}")
        else:
            display[col] = display[col].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in display.columns) + " |")
    return "\n".join(lines)


def score(galaxy: str, model_id: str, role: str, obs: np.ndarray, pred: np.ndarray, err: np.ndarray | None) -> dict:
    return {
        "galaxy": galaxy,
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


def load_trial_points() -> pd.DataFrame:
    trial = pd.read_csv(DATA / "full_time_morphology_trial_galaxy_points.csv")
    rows = []
    for _, row in trial.iterrows():
        rows.append(
            {
                "galaxy": row["galaxy"],
                "r_kpc": float(row["r_plot_kpc"]),
                "vobs_km_s": float(row["vobs_plot_km_s"]),
                "err_km_s": float(row["err_plot_km_s"]) if pd.notna(row["err_plot_km_s"]) else np.nan,
                "v_base_km_s": float(row["v_base_plot_km_s"]),
                "v_full_time_km_s": float(row["v_full_time_morphology_km_s"]),
                "K_time_shape": float(row["K_full_time_morph_phase"]),
                "source_load": float(row["phase_load_source_frozen"]),
                "source_status": row["source_status"],
                "source_note": "existing trial galaxy full-time/projection source status",
                "construction_used_vobs": False,
            }
        )

    u = pd.read_csv(DATA / "ugc12506_theta_morph_phase_replay_points.csv")
    for _, row in u.iterrows():
        rows.append(
            {
                "galaxy": "UGC12506",
                "r_kpc": float(row["radius_kpc"]),
                "vobs_km_s": float(row["vobs_kms"]),
                "err_km_s": float(row["errv_kms"]),
                "v_base_km_s": float(row["v_projection_history_incremental_positive_kms"]),
                "v_full_time_km_s": float(row["v_theta_morph_phase_positive_kms"]),
                "K_time_shape": float(row["K_theta_morph_phase_late_settling"]),
                "source_load": float(row["theta_morph_phase_load"]),
                "source_status": "edgeon_highspin_projection_history_theta",
                "source_note": "UGC12506 high-spin, edge-on, extended H I trajectory/phase diagnostic",
                "construction_used_vobs": False,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    points = load_trial_points()
    out_parts = []
    score_rows = []
    summary_rows = []
    gate_rows = []

    for galaxy, g in points.groupby("galaxy", sort=True):
        g = g.sort_values("r_kpc").copy()
        obs = g["vobs_km_s"].to_numpy(dtype=float)
        err_vals = g["err_km_s"].to_numpy(dtype=float)
        err = err_vals if np.all(np.isfinite(err_vals)) else None
        base = g["v_base_km_s"].to_numpy(dtype=float)
        full_time = g["v_full_time_km_s"].to_numpy(dtype=float)
        k = np.clip(g["K_time_shape"].to_numpy(dtype=float), 0.0, None)
        load = float(g["source_load"].iloc[0])

        epsilon_0 = min(EPSILON_CAP, 0.06 * load)
        xi_t = 1.0 + epsilon_0 * k
        v_xi_base = xi_t * base
        v_xi_full = xi_t * full_time

        g["epsilon_time_readout_source_frozen"] = epsilon_0
        g["Xi_t_time_readout"] = xi_t
        g["v_xi_base_time_readout_km_s"] = v_xi_base
        g["v_xi_full_time_readout_km_s"] = v_xi_full
        g["time_readout_construction_used_vobs"] = False
        g["time_readout_endpoint_validation_claim"] = False
        g["time_readout_claim_boundary"] = CLAIM_BOUNDARY
        out_parts.append(g)

        score_rows.extend(
            [
                score(galaxy, "base_projection_morphology", "reference", obs, base, err),
                score(galaxy, "full_time_morphology_additive_proxy", "reference", obs, full_time, err),
                score(galaxy, "xi_t_on_base_projection_morphology", "time_readout_diagnostic", obs, v_xi_base, err),
                score(galaxy, "xi_t_on_full_time_morphology", "time_readout_diagnostic", obs, v_xi_full, err),
            ]
        )
        base_rmse = rmse(obs, base)
        full_rmse = rmse(obs, full_time)
        xi_base_rmse = rmse(obs, v_xi_base)
        xi_full_rmse = rmse(obs, v_xi_full)
        best_id, best_rmse = min(
            [
                ("base_projection_morphology", base_rmse),
                ("full_time_morphology_additive_proxy", full_rmse),
                ("xi_t_on_base_projection_morphology", xi_base_rmse),
                ("xi_t_on_full_time_morphology", xi_full_rmse),
            ],
            key=lambda item: item[1],
        )
        summary_rows.append(
            {
                "galaxy": galaxy,
                "n_points": int(len(g)),
                "source_status": g["source_status"].iloc[0],
                "epsilon_0_source_frozen": epsilon_0,
                "rmse_base_km_s": base_rmse,
                "rmse_full_time_additive_km_s": full_rmse,
                "rmse_xi_on_base_km_s": xi_base_rmse,
                "rmse_xi_on_full_time_km_s": xi_full_rmse,
                "best_trial_model": best_id,
                "best_trial_rmse_km_s": best_rmse,
                "xi_improves_base": bool(xi_base_rmse < base_rmse),
                "xi_improves_full_time": bool(xi_full_rmse < full_rmse),
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        gate_rows.append(
            {
                "galaxy": galaxy,
                "gate_id": f"{galaxy}_XI_G1_SOURCE_FROZEN_DIAGNOSTIC",
                "gate_status": "PASS_DIAGNOSTIC_NOT_ACCEPTED_ENDPOINT",
                "evidence": "epsilon_0 = min(0.035, 0.06 * source_load); source_load inherited from residual-blind projection/phase status",
                "endpoint_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    out = pd.concat(out_parts, ignore_index=True)
    scores = pd.DataFrame(score_rows).sort_values(["galaxy", "rmse_km_s"])
    summary = pd.DataFrame(summary_rows).sort_values("galaxy")
    gates = pd.DataFrame(gate_rows)

    out.to_csv(DATA / "time_readout_xi_trial_galaxy_points.csv", index=False)
    scores.to_csv(DATA / "time_readout_xi_trial_galaxy_scores.csv", index=False)
    summary.to_csv(DATA / "time_readout_xi_trial_galaxy_summary.csv", index=False)
    gates.to_csv(DATA / "time_readout_xi_trial_galaxy_gates.csv", index=False)

    galaxies = list(summary["galaxy"])
    fig, axes = plt.subplots(len(galaxies), 1, figsize=(10, 2.7 * len(galaxies)), sharex=False)
    if len(galaxies) == 1:
        axes = [axes]
    for ax, galaxy in zip(axes, galaxies):
        g = out[out["galaxy"] == galaxy].sort_values("r_kpc")
        err = g["err_km_s"].to_numpy(dtype=float)
        yerr = err if np.all(np.isfinite(err)) else None
        ax.errorbar(g["r_kpc"], g["vobs_km_s"], yerr=yerr, fmt="o", color="black", ms=3, lw=0.8, label="observed")
        ax.plot(g["r_kpc"], g["v_base_km_s"], color="#6a3d9a", lw=1.8, label="base")
        ax.plot(g["r_kpc"], g["v_full_time_km_s"], color="#009392", lw=1.9, label="full-time additive")
        ax.plot(g["r_kpc"], g["v_xi_full_time_readout_km_s"], color="#e66101", lw=2.1, label="Xi_t on full-time")
        ax.set_title(galaxy)
        ax.set_ylabel("v [km/s]")
        ax.grid(alpha=0.25)
        ax.legend(fontsize=8, ncols=2)
    axes[-1].set_xlabel("Radius [kpc]")
    fig.suptitle("Diagnostic time-readout Xi_t replay on trial galaxies", y=0.995, fontsize=14)
    fig.tight_layout()
    fig_path = FIGURES / "time_readout_xi_trial_galaxy_rotation_curves.png"
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)

    report = "\n".join(
        [
            "# Time-Readout Xi_t Trial Diagnostic",
            "",
            "Status: diagnostic only, not endpoint validation.",
            "",
            "The run applies a small residual-blind clock/readout factor to the existing base and full-time morphology curves.",
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Scores",
            "",
            markdown_table(scores),
            "",
            f"Figure: `{fig_path.relative_to(ROOT)}`",
            "",
        ]
    )
    (REPORTS / "time_readout_xi_trial_galaxy_diagnostic.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))
    print(f"wrote {fig_path}")


if __name__ == "__main__":
    main()
