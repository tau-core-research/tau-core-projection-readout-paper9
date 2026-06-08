#!/usr/bin/env python3
"""Build rotation-curve comparison figures for projection-enriched candidates.

The figure compares, for the four path/projection-enriched candidate galaxies,
the measured rotation curve, a simpler pre-enrichment morphology proxy, the
projection-enriched readout, and the best conventional/comparator baseline
reported by the frozen endpoint outputs.

This is a plotting/ledger script.  It does not choose labels, fit amplitudes, or
derive formulas; it reads already frozen endpoint/control point products.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
FIGURES = ROOT / "paper8_submission_source" / "figures"


@dataclass(frozen=True)
class Case:
    galaxy: str
    path: str
    original_col: str
    original_label: str
    improved_col: str
    improved_label: str
    baseline_col: str
    baseline_label: str
    caveat: str


CASES = [
    Case(
        galaxy="NGC4013",
        path="ngc4013_warp_vertical_overlay_endpoint_points.csv",
        original_col="v_K_compact_finite",
        original_label="original proxy: compact",
        improved_col="v_wvo_endpoint",
        improved_label="projection-enriched: warp/vertical overlay",
        baseline_col="v_v6",
        baseline_label="best baseline: TPG/v6",
        caveat="retrospective/caveated mixed-reference case",
    ),
    Case(
        galaxy="NGC5907",
        path="ngc5907_expdisk_projection_mixed_accepted_endpoint_points.csv",
        original_col="v_K_exponential_disk",
        original_label="original proxy: exponential disk",
        improved_col="v_mixed_population",
        improved_label="projection-enriched: edge-on mixed",
        baseline_col="v_v6",
        baseline_label="best baseline: TPG/v6",
        caveat="fresh single-galaxy preliminary control",
    ),
    Case(
        galaxy="NGC7331",
        path="ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_points.csv",
        original_col="v_K_exponential_disk",
        original_label="original proxy: exponential disk",
        improved_col="v_mixed_population",
        improved_label="projection-enriched: vertical/outer warp",
        baseline_col="v_K_exponential_disk",
        baseline_label="best baseline: expdisk carrier",
        caveat="broad outer-warp window caveat",
    ),
    Case(
        galaxy="NGC4088",
        path="ngc4088_warp_history_accepted_endpoint_points.csv",
        original_col="v_K_thick_flared",
        original_label="original proxy: thick/flared",
        improved_col="v_warp_history_formula_freeze_km_s",
        improved_label="projection-enriched: warp/history",
        baseline_col="vn",
        baseline_label="best baseline: Newtonian",
        caveat="source-review and normalization-law caveats",
    ),
]


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "font.size": 8,
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#E5E7EB",
            "grid.linewidth": 0.65,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def rmse(model: pd.Series, observed: pd.Series) -> float:
    return float(np.sqrt(np.mean((model.to_numpy(float) - observed.to_numpy(float)) ** 2)))


def load_case(case: Case) -> pd.DataFrame:
    df = pd.read_csv(DERIVED / case.path).sort_values("r").copy()
    required = ["r", "vobs", case.original_col, case.improved_col, case.baseline_col]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"{case.galaxy} missing columns {missing} in {case.path}")
    return df


def build_summary() -> pd.DataFrame:
    rows = []
    for case in CASES:
        df = load_case(case)
        rows.append(
            {
                "galaxy": case.galaxy,
                "n_points": len(df),
                "original_proxy": case.original_label,
                "improved_kernel": case.improved_label,
                "best_baseline": case.baseline_label,
                "rmse_original_km_s": rmse(df[case.original_col], df["vobs"]),
                "rmse_improved_km_s": rmse(df[case.improved_col], df["vobs"]),
                "rmse_best_baseline_km_s": rmse(df[case.baseline_col], df["vobs"]),
                "improved_minus_original_km_s": rmse(df[case.improved_col], df["vobs"])
                - rmse(df[case.original_col], df["vobs"]),
                "improved_minus_best_baseline_km_s": rmse(df[case.improved_col], df["vobs"])
                - rmse(df[case.baseline_col], df["vobs"]),
                "caveat": case.caveat,
                "claim_boundary": "projection_enriched_rotation_comparison_visualization_not_new_fit",
            }
        )
    return pd.DataFrame(rows)


def plot_case(ax_curve: plt.Axes, ax_resid: plt.Axes, case: Case) -> None:
    df = load_case(case)
    r = df["r"]
    vobs = df["vobs"]

    err = df["errv"] if "errv" in df.columns else None
    ax_curve.errorbar(
        r,
        vobs,
        yerr=err,
        fmt="o",
        ms=3.5,
        lw=0.8,
        color="#111827",
        ecolor="#9CA3AF",
        capsize=1.8,
        label="observed",
        zorder=4,
    )
    ax_curve.plot(r, df[case.original_col], color="#94A3B8", lw=1.6, ls="--", label=case.original_label)
    ax_curve.plot(r, df[case.baseline_col], color="#F97316", lw=1.35, ls=":", label=case.baseline_label)
    ax_curve.plot(r, df[case.improved_col], color="#2563EB", lw=2.0, label=case.improved_label)

    original_rmse = rmse(df[case.original_col], vobs)
    improved_rmse = rmse(df[case.improved_col], vobs)
    baseline_rmse = rmse(df[case.baseline_col], vobs)
    ax_curve.set_title(
        f"{case.galaxy}: improved {improved_rmse:.2f}, original {original_rmse:.2f}, baseline {baseline_rmse:.2f} km/s",
        loc="left",
    )
    ax_curve.set_ylabel("velocity (km s$^{-1}$)")

    ax_resid.axhline(0, color="#111827", lw=0.8)
    ax_resid.plot(r, df[case.original_col] - vobs, color="#94A3B8", lw=1.4, ls="--", label="original - obs")
    ax_resid.plot(r, df[case.baseline_col] - vobs, color="#F97316", lw=1.15, ls=":", label="baseline - obs")
    ax_resid.plot(r, df[case.improved_col] - vobs, color="#2563EB", lw=1.7, label="improved - obs")
    ax_resid.set_ylabel("residual")
    ax_resid.set_xlabel("radius (kpc)")

def build_figure() -> None:
    setup_style()
    FIGURES.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(
        nrows=4,
        ncols=2,
        figsize=(7.6, 10.5),
        gridspec_kw={"height_ratios": [1, 1, 1, 1], "width_ratios": [1.55, 1.0]},
    )

    for row, case in enumerate(CASES):
        plot_case(axes[row, 0], axes[row, 1], case)

    axes[0, 0].legend(frameon=False, loc="best", ncols=1)
    axes[0, 1].legend(frameon=False, loc="best", ncols=1)
    fig.suptitle(
        "Projection-enriched candidate kernels: original proxy versus improved readout",
        y=0.995,
        fontsize=11,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    fig.savefig(FIGURES / "fig20_projection_enriched_kernel_rotation_comparison.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / "fig20_projection_enriched_kernel_rotation_comparison.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    summary = build_summary()
    summary_path = DERIVED / "projection_enriched_rotation_comparison_summary.csv"
    summary.to_csv(summary_path, index=False)
    build_figure()
    print(summary.to_string(index=False))
    print(f"\nwrote {summary_path}")
    print(f"wrote {FIGURES / 'fig20_projection_enriched_kernel_rotation_comparison.pdf'}")
    print(f"wrote {FIGURES / 'fig20_projection_enriched_kernel_rotation_comparison.png'}")


if __name__ == "__main__":
    main()
