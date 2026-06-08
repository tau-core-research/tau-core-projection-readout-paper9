#!/usr/bin/env python3
"""Build comparison rotation-curve figures for the UGC12506 beta-closure transfer.

The figures are control-score diagnostics only. They compare the source-frozen
beta-closure transfer kernel against the frozen baryonic carrier used in this
stress test, with the current kernel visually highlighted.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures" / "endpoint_diagnostics" / "ugc12506_beta_closure_transfer"
PAPER_FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"

POINTS = DATA / "ugc12506_beta_closure_transfer_scoring_points.csv"
SCORES = DATA / "ugc12506_beta_closure_transfer_scoring_scores.csv"

CURRENT_MODEL_ID = "BETA_CL_TRANSFER_SOURCE_FROZEN"
CARRIER_MODEL_ID = "BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_figures_control_only_not_endpoint"


def score_lookup(scores: pd.DataFrame) -> pd.DataFrame:
    wide = scores.pivot(index="galaxy", columns="model_id", values="rmse_km_s")
    wide = wide.rename(
        columns={
            CURRENT_MODEL_ID: "beta_rmse_km_s",
            CARRIER_MODEL_ID: "carrier_rmse_km_s",
        }
    )
    wide["delta_carrier_minus_beta_km_s"] = (
        wide["carrier_rmse_km_s"] - wide["beta_rmse_km_s"]
    )
    return wide.reset_index()


def plot_single_galaxy(galaxy: str, points: pd.DataFrame, score_row: pd.Series) -> list[Path]:
    g = points[points["galaxy"].eq(galaxy)].sort_values("radius_kpc")
    r = g["radius_kpc"].to_numpy(float)
    vobs = g["vobs_kms"].to_numpy(float)
    err = g["errv_kms"].to_numpy(float)
    carrier = g["v_carrier_kms"].to_numpy(float)
    beta = g["v_beta_cl_transfer_kms"].to_numpy(float)

    delta = float(score_row["delta_carrier_minus_beta_km_s"])
    improved = delta > 0
    title_suffix = "improves carrier" if improved else "does not improve carrier"

    fig, (ax, ax_resid) = plt.subplots(
        2,
        1,
        figsize=(8.9, 6.7),
        sharex=True,
        gridspec_kw={"height_ratios": [2.25, 1.0], "hspace": 0.05},
    )

    ax.errorbar(
        r,
        vobs,
        yerr=err,
        fmt="o",
        ms=4.2,
        lw=0.8,
        color="black",
        ecolor="#555555",
        capsize=2,
        label="observed rotation curve",
        zorder=10,
    )
    ax.plot(
        r,
        carrier,
        color="#7f7f7f",
        ls="--",
        lw=1.8,
        label="frozen baryonic carrier",
        zorder=4,
    )
    ax.plot(
        r,
        beta,
        color="#e66101",
        ls="-",
        lw=3.2,
        label="current kernel: beta-closure transfer",
        zorder=7,
    )
    ax.fill_between(
        r,
        beta - np.maximum(err, 3.0),
        beta + np.maximum(err, 3.0),
        color="#e66101",
        alpha=0.09,
        linewidth=0,
        zorder=1,
    )
    ax.set_ylabel("Rotation speed [km/s]")
    ax.set_title(f"{galaxy}: beta-closure transfer control comparison ({title_suffix})")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8.4, loc="best")

    ax_resid.axhline(0.0, color="#999999", lw=1.0)
    ax_resid.plot(
        r,
        vobs - carrier,
        color="#7f7f7f",
        ls="--",
        lw=1.7,
        label="obs - carrier",
    )
    ax_resid.plot(
        r,
        vobs - beta,
        color="#e66101",
        ls="-",
        lw=2.7,
        label="obs - current kernel",
    )
    ax_resid.set_xlabel("Radius [kpc]")
    ax_resid.set_ylabel("Residual [km/s]")
    ax_resid.grid(alpha=0.25)
    ax_resid.legend(frameon=False, fontsize=8.0, loc="best")

    note = (
        "Control-score diagnostic only; not endpoint validation. "
        f"Carrier RMSE={score_row['carrier_rmse_km_s']:.2f} km/s; "
        f"current-kernel RMSE={score_row['beta_rmse_km_s']:.2f} km/s; "
        f"carrier-current delta={delta:+.2f} km/s."
    )
    fig.text(0.015, 0.012, note, fontsize=8.0, color="#333333")
    fig.subplots_adjust(left=0.09, right=0.985, top=0.91, bottom=0.15)

    safe = galaxy.lower().replace("-", "_")
    png = FIGURES / f"{safe}_beta_closure_transfer_comparison.png"
    pdf = FIGURES / f"{safe}_beta_closure_transfer_comparison.pdf"
    paper_png = PAPER_FIGURES / f"fig_ugc12506_beta_closure_transfer_{safe}.png"
    fig.savefig(png, dpi=220)
    fig.savefig(pdf)
    fig.savefig(paper_png, dpi=220)
    plt.close(fig)
    return [png, pdf, paper_png]


def plot_panel(points: pd.DataFrame, score_table: pd.DataFrame) -> list[Path]:
    ordered = score_table.sort_values("delta_carrier_minus_beta_km_s", ascending=False)
    galaxies = ordered["galaxy"].tolist()

    ncols = 3
    nrows = int(np.ceil(len(galaxies) / ncols))
    fig, axes = plt.subplots(nrows, ncols, figsize=(14.2, 12.0), sharex=False, sharey=False)
    axes = np.asarray(axes).reshape(-1)

    for ax, galaxy in zip(axes, galaxies):
        g = points[points["galaxy"].eq(galaxy)].sort_values("radius_kpc")
        row = ordered[ordered["galaxy"].eq(galaxy)].iloc[0]
        r = g["radius_kpc"].to_numpy(float)
        delta = float(row["delta_carrier_minus_beta_km_s"])
        ax.errorbar(
            r,
            g["vobs_kms"],
            yerr=g["errv_kms"],
            fmt="o",
            ms=2.8,
            lw=0.55,
            color="black",
            ecolor="#777777",
            capsize=1.5,
            zorder=10,
        )
        ax.plot(r, g["v_carrier_kms"], color="#8c8c8c", ls="--", lw=1.2, label="carrier")
        ax.plot(
            r,
            g["v_beta_cl_transfer_kms"],
            color="#e66101",
            ls="-",
            lw=2.5,
            label="current kernel",
        )
        edge_color = "#1b7837" if delta > 0 else ("#b2182b" if delta < 0 else "#777777")
        ax.text(
            0.03,
            0.95,
            f"{galaxy}\nΔRMSE={delta:+.1f}",
            transform=ax.transAxes,
            va="top",
            ha="left",
            fontsize=8.2,
            bbox={
                "boxstyle": "round,pad=0.22",
                "facecolor": "white",
                "edgecolor": edge_color,
                "alpha": 0.88,
            },
        )
        ax.grid(alpha=0.2)
        ax.tick_params(labelsize=7.5)

    for ax in axes[len(galaxies) :]:
        ax.axis("off")

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, frameon=False, ncol=3, loc="upper center", bbox_to_anchor=(0.5, 0.985))
    fig.suptitle(
        "UGC12506 beta-closure transfer: source-frozen current kernel vs frozen baryonic carrier",
        y=0.998,
        fontsize=13.0,
    )
    fig.text(0.5, 0.04, "Radius [kpc]", ha="center", fontsize=10.5)
    fig.text(0.012, 0.5, "Rotation speed [km/s]", va="center", rotation="vertical", fontsize=10.5)
    fig.text(
        0.5,
        0.014,
        "Control-score diagnostic only. Orange curve is the current highlighted kernel; panels are ordered by carrier-current RMSE improvement.",
        ha="center",
        fontsize=8.4,
        color="#333333",
    )
    fig.subplots_adjust(left=0.06, right=0.985, top=0.945, bottom=0.075, hspace=0.30, wspace=0.20)

    png = FIGURES / "ugc12506_beta_closure_transfer_all_galaxies_panel.png"
    pdf = FIGURES / "ugc12506_beta_closure_transfer_all_galaxies_panel.pdf"
    paper_png = PAPER_FIGURES / "fig_ugc12506_beta_closure_transfer_all_galaxies_panel.png"
    fig.savefig(png, dpi=220)
    fig.savefig(pdf)
    fig.savefig(paper_png, dpi=220)
    plt.close(fig)
    return [png, pdf, paper_png]


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(POINTS)
    scores = pd.read_csv(SCORES)
    table = score_lookup(scores)
    table["improved_over_carrier"] = table["delta_carrier_minus_beta_km_s"] > 0
    table["claim_boundary"] = CLAIM_BOUNDARY
    summary_path = DATA / "ugc12506_beta_closure_transfer_comparison_figure_summary.csv"
    table.sort_values("delta_carrier_minus_beta_km_s", ascending=False).to_csv(summary_path, index=False)

    written: list[Path] = []
    written.extend(plot_panel(points, table))
    for _, row in table.iterrows():
        written.extend(plot_single_galaxy(str(row["galaxy"]), points, row))

    print(f"wrote summary {summary_path}")
    for path in written:
        print(f"wrote {path}")
    improved = int(table["improved_over_carrier"].sum())
    print(
        f"current kernel improves over carrier for {improved}/{len(table)} galaxies; "
        f"mean delta={table['delta_carrier_minus_beta_km_s'].mean():.3f} km/s; "
        f"median delta={table['delta_carrier_minus_beta_km_s'].median():.3f} km/s"
    )


if __name__ == "__main__":
    main()
