#!/usr/bin/env python3
"""Build rotation-comparison figures for the strengthened NGC4088/NGC4013 audit.

The figures are visualization artifacts only.  They read frozen endpoint,
protocol, and control point products already produced by the scoring scripts.
They do not choose labels, fit amplitudes, or promote endpoint status.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"
CLAIM_BOUNDARY = "ngc4088_ngc4013_strengthened_rotation_comparison_visualization_not_new_fit"


def setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.dpi": 160,
            "savefig.dpi": 300,
            "font.size": 9,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 7.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#E5E7EB",
            "grid.linewidth": 0.65,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def rmse(y: pd.Series | np.ndarray, obs: pd.Series | np.ndarray) -> float:
    return float(np.sqrt(np.mean((np.asarray(y, dtype=float) - np.asarray(obs, dtype=float)) ** 2)))


def finite_err(df: pd.DataFrame, column: str) -> pd.Series | None:
    if column not in df.columns:
        return None
    err = pd.to_numeric(df[column], errors="coerce")
    if err.notna().any():
        return err
    return None


def plot_family(
    ax_curve: plt.Axes,
    ax_resid: plt.Axes,
    *,
    df: pd.DataFrame,
    r_col: str,
    vobs_col: str,
    err_col: str,
    title: str,
    models: list[dict[str, str]],
) -> list[dict[str, object]]:
    r = df[r_col]
    vobs = df[vobs_col]
    err = finite_err(df, err_col)
    ax_curve.errorbar(
        r,
        vobs,
        yerr=err,
        fmt="o",
        ms=4.2,
        lw=0.9,
        color="#111827",
        ecolor="#9CA3AF",
        capsize=2,
        label="observed",
        zorder=6,
    )
    ax_resid.axhline(0, color="#111827", lw=0.8)

    rows: list[dict[str, object]] = []
    for model in models:
        y = df[model["column"]]
        score = rmse(y, vobs)
        label = f"{model['label']} ({score:.2f})"
        ax_curve.plot(
            r,
            y,
            color=model["color"],
            lw=float(model.get("lw", "1.8")),
            ls=model.get("ls", "-"),
            alpha=float(model.get("alpha", "1.0")),
            label=label,
            zorder=int(model.get("zorder", "3")),
        )
        ax_resid.plot(
            r,
            y - vobs,
            color=model["color"],
            lw=float(model.get("resid_lw", model.get("lw", "1.4"))),
            ls=model.get("ls", "-"),
            alpha=float(model.get("alpha", "1.0")),
            label=model["label"],
        )
        rows.append(
            {
                "model": model["label"],
                "rmse_km_s": score,
                "score_role": model["role"],
                "endpoint_scores_allowed": model["endpoint_scores_allowed"],
                "endpoint_validation_claim": False,
            }
        )

    ax_curve.set_title(title, loc="left")
    ax_curve.set_ylabel("velocity (km s$^{-1}$)")
    ax_resid.set_ylabel("model - observed")
    ax_resid.set_xlabel("radius (kpc)")
    ax_curve.legend(frameon=False, loc="upper left", bbox_to_anchor=(1.005, 1.0), ncols=1)
    return rows


def build_ngc4013() -> pd.DataFrame:
    endpoint = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_endpoint_points.csv")
    protocol = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_points.csv")[
        ["r", "v_K_exponential_disk", "v_expdisk_wvo_frozen"]
    ]
    df = endpoint.merge(protocol, on="r", how="left", suffixes=("", "_protocol"))
    if "v_K_exponential_disk_protocol" in df.columns:
        df["v_K_exponential_disk"] = df["v_K_exponential_disk_protocol"].fillna(
            df["v_K_exponential_disk"]
        )
    models = [
        {
            "column": "vn",
            "label": "Newtonian",
            "role": "baseline",
            "endpoint_scores_allowed": False,
            "color": "#64748B",
            "ls": ":",
            "lw": "1.5",
        },
        {
            "column": "v_v6",
            "label": "TPG/v6 carrier",
            "role": "internal_predecessor_comparator",
            "endpoint_scores_allowed": False,
            "color": "#F97316",
            "ls": "-.",
            "lw": "1.5",
        },
        {
            "column": "v_mond",
            "label": "MOND proxy",
            "role": "baseline_proxy",
            "endpoint_scores_allowed": False,
            "color": "#A855F7",
            "ls": "--",
            "lw": "1.5",
        },
        {
            "column": "v_K_compact_finite",
            "label": "compact proxy",
            "role": "source_rejected_starting_proxy",
            "endpoint_scores_allowed": False,
            "color": "#94A3B8",
            "ls": "--",
            "lw": "1.6",
        },
        {
            "column": "v_wvo_endpoint",
            "label": "WVO caveated endpoint",
            "role": "caveated_preliminary_endpoint_control",
            "endpoint_scores_allowed": True,
            "color": "#2563EB",
            "lw": "2.4",
            "zorder": "5",
        },
        {
            "column": "v_expdisk_wvo_frozen",
            "label": "expdisk+WVO prospective",
            "role": "prospective_protocol_not_retroactive_endpoint",
            "endpoint_scores_allowed": False,
            "color": "#059669",
            "lw": "2.4",
            "zorder": "4",
        },
    ]
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10.2, 6.2),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1]},
    )
    rows = plot_family(
        axes[0],
        axes[1],
        df=df,
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        title="NGC4013: source-supported morphology refinement",
        models=models,
    )
    fig.text(
        0.07,
        0.012,
        "Note: green is the strongest score here, but prospective/protocol-only; blue is the caveated endpoint route.",
        fontsize=8,
        color="#374151",
    )
    fig.tight_layout(rect=(0, 0.025, 0.82, 1))
    out_png = FIGURES / "fig_ngc4013_strengthened_rotation_comparison.png"
    out_pdf = FIGURES / "fig_ngc4013_strengthened_rotation_comparison.pdf"
    fig.savefig(out_png, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    out = pd.DataFrame(rows)
    out.insert(0, "galaxy", "NGC4013")
    out["figure_png"] = str(out_png.relative_to(ROOT))
    out["claim_boundary"] = CLAIM_BOUNDARY
    return out


def build_ngc4088() -> pd.DataFrame:
    endpoint = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_points.csv")
    ablation = pd.read_csv(DATA / "ngc4088_time_projection_ablation_control_points.csv")[
        [
            "r_kpc",
            "v_base_projection_km_s",
            "v_additive_warp_history_km_s",
            "v_clock_only_on_base_km_s",
            "v_additive_plus_clock_stress_km_s",
        ]
    ]
    df = endpoint.merge(ablation, left_on="r", right_on="r_kpc", how="left")
    models = [
        {
            "column": "vn",
            "label": "Newtonian",
            "role": "best_local_baseline",
            "endpoint_scores_allowed": False,
            "color": "#64748B",
            "ls": ":",
            "lw": "1.5",
        },
        {
            "column": "v_v6",
            "label": "TPG/v6 carrier",
            "role": "internal_predecessor_comparator",
            "endpoint_scores_allowed": False,
            "color": "#F97316",
            "ls": "-.",
            "lw": "1.4",
        },
        {
            "column": "v_mond",
            "label": "MOND proxy",
            "role": "baseline_proxy",
            "endpoint_scores_allowed": False,
            "color": "#A855F7",
            "ls": "--",
            "lw": "1.4",
        },
        {
            "column": "v_K_thick_flared",
            "label": "wrong-family thick/flared",
            "role": "wrong_family_control",
            "endpoint_scores_allowed": False,
            "color": "#94A3B8",
            "ls": "--",
            "lw": "1.4",
        },
        {
            "column": "v_warp_history_formula_freeze_km_s",
            "label": "accepted warp/history",
            "role": "caveated_accepted_endpoint_preliminary_control",
            "endpoint_scores_allowed": True,
            "color": "#2563EB",
            "lw": "2.5",
            "zorder": "5",
        },
        {
            "column": "v_additive_warp_history_km_s",
            "label": "additive control",
            "role": "control_replay_not_new_endpoint",
            "endpoint_scores_allowed": False,
            "color": "#059669",
            "lw": "2.0",
            "alpha": "0.85",
        },
        {
            "column": "v_clock_only_on_base_km_s",
            "label": "clock-only control",
            "role": "diagnostic_control_not_endpoint",
            "endpoint_scores_allowed": False,
            "color": "#DC2626",
            "ls": "-",
            "lw": "1.7",
            "alpha": "0.8",
        },
        {
            "column": "v_additive_plus_clock_stress_km_s",
            "label": "additive+clock stress",
            "role": "stress_control_double_count_blocked",
            "endpoint_scores_allowed": False,
            "color": "#111827",
            "lw": "2.0",
            "alpha": "0.75",
        },
    ]
    fig, axes = plt.subplots(
        2,
        1,
        figsize=(10.2, 6.2),
        sharex=True,
        gridspec_kw={"height_ratios": [2.2, 1]},
    )
    rows = plot_family(
        axes[0],
        axes[1],
        df=df,
        r_col="r",
        vobs_col="vobs",
        err_col="errv",
        title="NGC4088: accepted warp/history route and controls",
        models=models,
    )
    fig.text(
        0.07,
        0.012,
        "Note: blue is endpoint-readable as caveated control; black is lower RMSE but double-count blocked.",
        fontsize=8,
        color="#374151",
    )
    fig.tight_layout(rect=(0, 0.025, 0.82, 1))
    out_png = FIGURES / "fig_ngc4088_strengthened_rotation_comparison.png"
    out_pdf = FIGURES / "fig_ngc4088_strengthened_rotation_comparison.pdf"
    fig.savefig(out_png, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)
    out = pd.DataFrame(rows)
    out.insert(0, "galaxy", "NGC4088")
    out["figure_png"] = str(out_png.relative_to(ROOT))
    out["claim_boundary"] = CLAIM_BOUNDARY
    return out


def write_report(scores: pd.DataFrame) -> None:
    display = scores.copy()
    display["rmse_km_s"] = display["rmse_km_s"].map(lambda value: f"{value:.3f}")
    lines = [
        "# NGC4088/NGC4013 Strengthened Rotation Comparison Figures",
        "",
        "These figures visualize already-frozen endpoint/protocol/control products. They do not fit new amplitudes or select labels from residuals.",
        "",
        "| galaxy | model | RMSE km/s | role | endpoint allowed |",
        "| --- | --- | --- | --- | --- |",
    ]
    for _, row in display.iterrows():
        lines.append(
            f"| {row['galaxy']} | {row['model']} | {row['rmse_km_s']} | "
            f"{row['score_role']} | {row['endpoint_scores_allowed']} |"
        )
    lines.extend(
        [
            "",
            "Outputs:",
            "- `papers/paper2_projection_enriched/source/figures/fig_ngc4013_strengthened_rotation_comparison.png`",
            "- `papers/paper2_projection_enriched/source/figures/fig_ngc4088_strengthened_rotation_comparison.png`",
        ]
    )
    (REPORTS / "ngc4088_ngc4013_strengthened_rotation_comparison_figures.md").write_text(
        "\n".join(lines) + "\n"
    )


def main() -> None:
    setup_style()
    FIGURES.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    scores = pd.concat([build_ngc4013(), build_ngc4088()], ignore_index=True)
    scores.to_csv(
        DATA / "ngc4088_ngc4013_strengthened_rotation_comparison_figure_scores.csv",
        index=False,
    )
    write_report(scores)
    print("NGC4088_NGC4013_STRENGTHENED_ROTATION_COMPARISON_FIGURES_COMPLETE")
    print(scores[["galaxy", "model", "rmse_km_s", "score_role"]].to_string(index=False))


if __name__ == "__main__":
    main()
