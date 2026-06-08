#!/usr/bin/env python3
"""Run a diagnostic full-time morphology phase layer on trial galaxies.

This script asks a narrow question: if the already frozen morphology/projection
readout is treated as a present-slice approximation, does a small trajectory /
phase component improve the rotation curve on the existing trial galaxies?

The construction is deliberately residual-blind.  The observed velocity is used
only for scoring.  The phase loads are fixed per source status, not fitted per
galaxy, and this is diagnostic/preflight only.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "figures" / "endpoint_diagnostics"
CLAIM_BOUNDARY = "full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation"


@dataclass(frozen=True)
class TrialSpec:
    galaxy: str
    points_path: str
    r_col: str
    vobs_col: str
    err_col: str | None
    carrier_col: str
    base_col: str
    kernel_col: str
    phase_load: float
    source_status: str
    source_note: str


TRIALS = [
    TrialSpec(
        galaxy="NGC4013",
        points_path="ngc4013_warp_vertical_overlay_endpoint_points.csv",
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        carrier_col="v_v6",
        base_col="v_wvo_endpoint",
        kernel_col="K_wvo",
        phase_load=0.18,
        source_status="warp_vertical_overlay",
        source_note="edge-on warp plus vertical-overlay source context",
    ),
    TrialSpec(
        galaxy="NGC5907",
        points_path="ngc5907_projection_accepted_endpoint_points.csv",
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        carrier_col="v_v6",
        base_col="v_projection_accepted",
        kernel_col="projection_kernel",
        phase_load=0.12,
        source_status="edgeon_projection_vertical_warp",
        source_note="edge-on projection and warp/truncation context",
    ),
    TrialSpec(
        galaxy="NGC7331",
        points_path="ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv",
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        carrier_col="v_K_exponential_disk",
        base_col="v_mixed_population",
        kernel_col="mixed_kernel",
        phase_load=0.10,
        source_status="vertical_outer_warp_overlay",
        source_note="outer warp / vertical-scale mixed readout context",
    ),
    TrialSpec(
        galaxy="NGC4088",
        points_path="ngc4088_warp_history_accepted_endpoint_points.csv",
        r_col="r",
        vobs_col="vobs",
        err_col=None,
        carrier_col="vn",
        base_col="v_warp_history_formula_freeze_km_s",
        kernel_col="kernel_warp_history",
        phase_load=0.35,
        source_status="warp_history_asymmetric_projection",
        source_note="strong warp/history/asymmetry plus companion context",
    ),
    TrialSpec(
        galaxy="NGC4183",
        points_path="ngc4183_weak_projection_null_control_accepted_endpoint_points.csv",
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        carrier_col="v_K_exponential_disk",
        base_col="v_null_control_interval_midpoint_km_s",
        kernel_col="x_R_over_RHI",
        phase_load=0.03,
        source_status="weak_projection_null_control",
        source_note="weak projection/null-control case; phase effect expected to be small",
    ),
]


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def normalize(x: np.ndarray) -> np.ndarray:
    m = float(np.max(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray | None) -> float:
    if err is None:
        return float("nan")
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


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


def score_row(galaxy: str, model_id: str, role: str, obs: np.ndarray, pred: np.ndarray, err: np.ndarray | None) -> dict:
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


def build_phase_curve(spec: TrialSpec) -> tuple[pd.DataFrame, list[dict], dict]:
    df = pd.read_csv(DATA / spec.points_path).sort_values(spec.r_col).reset_index(drop=True)
    r = df[spec.r_col].to_numpy(dtype=float)
    obs = df[spec.vobs_col].to_numpy(dtype=float)
    err = df[spec.err_col].to_numpy(dtype=float) if spec.err_col and spec.err_col in df.columns else None
    carrier = df[spec.carrier_col].to_numpy(dtype=float)
    base = df[spec.base_col].to_numpy(dtype=float)
    raw_kernel = df[spec.kernel_col].to_numpy(dtype=float)

    x = (r - float(np.min(r))) / max(float(np.max(r) - np.min(r)), 1.0e-6)
    late_window = 0.65 + 0.35 * smoothstep((x - 0.35) / 0.65)
    k_phase = normalize(np.clip(raw_kernel, 0.0, None) * late_window * np.sqrt(np.clip(x, 0.0, 1.0)))

    positive_base_increment = np.maximum(np.square(base) - np.square(carrier), 0.0)
    outer = x >= 0.5
    if np.any(outer):
        source_scale = float(np.median(positive_base_increment[outer]))
    else:
        source_scale = float(np.median(positive_base_increment))
    if source_scale <= 1.0e-9:
        source_scale = 0.02 * float(np.median(np.square(base)))
    amplitude = spec.phase_load * source_scale

    v2_full = np.square(base) + amplitude * k_phase
    full = np.sqrt(np.maximum(v2_full, 0.0))

    out = df.copy()
    out["K_full_time_morph_phase"] = k_phase
    out["phase_load_source_frozen"] = spec.phase_load
    out["A_full_time_morph_phase_km2_s2"] = amplitude
    out["v2_full_time_morphology_km2_s2"] = v2_full
    out["v_full_time_morphology_km_s"] = full
    out["construction_used_vobs"] = False
    out["endpoint_validation_claim"] = False
    out["full_time_claim_boundary"] = CLAIM_BOUNDARY

    model_scores = [
        score_row(spec.galaxy, "carrier_reference", spec.carrier_col, obs, carrier, err),
        score_row(spec.galaxy, "base_projection_morphology_kernel", spec.base_col, obs, base, err),
        score_row(spec.galaxy, "full_time_morphology_phase_kernel", "diagnostic_phase_enriched", obs, full, err),
    ]
    if "v_v6" in df.columns and spec.carrier_col != "v_v6":
        model_scores.append(score_row(spec.galaxy, "TPG_V6_v_v6", "baseline", obs, df["v_v6"].to_numpy(dtype=float), err))
    if "v_mond" in df.columns:
        model_scores.append(score_row(spec.galaxy, "MOND_v_mond", "baseline", obs, df["v_mond"].to_numpy(dtype=float), err))
    if "vn" in df.columns and spec.carrier_col != "vn":
        model_scores.append(score_row(spec.galaxy, "NEWTONIAN_vn", "baseline", obs, df["vn"].to_numpy(dtype=float), err))

    base_rmse = rmse(obs, base)
    full_rmse = rmse(obs, full)
    summary = {
        "galaxy": spec.galaxy,
        "source_status": spec.source_status,
        "source_note": spec.source_note,
        "n_points": int(len(df)),
        "phase_load_source_frozen": spec.phase_load,
        "amplitude_full_time_km2_s2": amplitude,
        "rmse_base_projection_morphology_km_s": base_rmse,
        "rmse_full_time_morphology_km_s": full_rmse,
        "full_time_minus_base_rmse_km_s": full_rmse - base_rmse,
        "improves_base": bool(full_rmse < base_rmse),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    return out, model_scores, summary


def plot(points: pd.DataFrame) -> Path:
    galaxies = list(points["galaxy"].drop_duplicates())
    fig, axes = plt.subplots(len(galaxies), 1, figsize=(10, 2.75 * len(galaxies)), sharex=False)
    if len(galaxies) == 1:
        axes = [axes]
    for ax, galaxy in zip(axes, galaxies):
        sub = points.loc[points["galaxy"].eq(galaxy)].sort_values("r_plot_kpc")
        err = sub["err_plot_km_s"].to_numpy(dtype=float)
        yerr = err if np.all(np.isfinite(err)) else None
        ax.errorbar(
            sub["r_plot_kpc"],
            sub["vobs_plot_km_s"],
            yerr=yerr,
            fmt="o",
            ms=3.4,
            color="black",
            ecolor="black",
            alpha=0.8,
            lw=0.8,
            label="observed",
        )
        ax.plot(sub["r_plot_kpc"], sub["v_carrier_plot_km_s"], color="#8a8a8a", lw=1.5, label="carrier")
        ax.plot(sub["r_plot_kpc"], sub["v_base_plot_km_s"], color="#5e3c99", lw=2.0, label="base morphology/projection")
        ax.plot(sub["r_plot_kpc"], sub["v_full_time_morphology_km_s"], color="#009392", lw=2.5, label="full-time morphology diagnostic")
        ax.set_title(galaxy)
        ax.set_ylabel("v [km/s]")
        ax.grid(alpha=0.25)
        ax.legend(loc="best", fontsize=8, ncols=2)
    axes[-1].set_xlabel("Radius [kpc]")
    fig.suptitle("Full-time morphology phase diagnostic on trial galaxies", y=0.995, fontsize=14)
    fig.tight_layout()
    path = FIGURES / "full_time_morphology_trial_galaxy_rotation_curves.png"
    fig.savefig(path, dpi=180)
    plt.close(fig)
    return path


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    all_points: list[pd.DataFrame] = []
    all_scores: list[dict] = []
    summaries: list[dict] = []
    gates: list[dict] = []

    for spec in TRIALS:
        out, scores, summary = build_phase_curve(spec)
        out["r_plot_kpc"] = out[spec.r_col]
        out["vobs_plot_km_s"] = out[spec.vobs_col]
        out["err_plot_km_s"] = out[spec.err_col] if spec.err_col and spec.err_col in out.columns else np.nan
        out["v_carrier_plot_km_s"] = out[spec.carrier_col]
        out["v_base_plot_km_s"] = out[spec.base_col]
        out["base_column"] = spec.base_col
        out["carrier_column"] = spec.carrier_col
        out["kernel_column"] = spec.kernel_col
        out["source_status"] = spec.source_status
        all_points.append(out)
        all_scores.extend(scores)
        summaries.append(summary)
        gates.append(
            {
                "galaxy": spec.galaxy,
                "gate_id": f"{spec.galaxy}_FULL_TIME_G1_SOURCE_STATUS",
                "gate_status": "PASS_DIAGNOSTIC_SOURCE_STATUS",
                "evidence": spec.source_note,
                "endpoint_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
        gates.append(
            {
                "galaxy": spec.galaxy,
                "gate_id": f"{spec.galaxy}_FULL_TIME_G2_NO_BACKWARD_CAUSAL_CLAIM",
                "gate_status": "PASS_CLAIM_BOUNDARY",
                "evidence": "trajectory/phase component, not backward 4D causality",
                "endpoint_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    points = pd.concat(all_points, ignore_index=True)
    scores = pd.DataFrame(all_scores).sort_values(["galaxy", "rmse_km_s"]).reset_index(drop=True)
    summary = pd.DataFrame(summaries).sort_values("galaxy").reset_index(drop=True)
    gates_df = pd.DataFrame(gates)

    points.to_csv(DATA / "full_time_morphology_trial_galaxy_points.csv", index=False)
    scores.to_csv(DATA / "full_time_morphology_trial_galaxy_scores.csv", index=False)
    summary.to_csv(DATA / "full_time_morphology_trial_galaxy_summary.csv", index=False)
    gates_df.to_csv(DATA / "full_time_morphology_trial_galaxy_gates.csv", index=False)
    fig_path = plot(points)

    report = "\n".join(
        [
            "# Full-Time Morphology Phase Diagnostic",
            "",
            "Status: diagnostic/preflight only, not endpoint validation.",
            "",
            "The added layer is source-frozen from morphology/projection status and existing carrier scale. "
            "Observed velocities are used only for scoring.",
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
    (REPORTS / "full_time_morphology_trial_galaxy_diagnostic.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))
    print(f"wrote {fig_path}")


if __name__ == "__main__":
    main()
