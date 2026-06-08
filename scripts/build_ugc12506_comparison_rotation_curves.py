#!/usr/bin/env python3
"""Build comparison rotation-curve figures for UGC12506 controls.

The figures compare source-frozen/control curves only.  They are visual
diagnostics for the UGC12506 combined-control replay, not endpoint validation.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures" / "endpoint_diagnostics"
PAPER_FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(DATA / "ugc12506_theta_xit_combined_control_replay_points.csv")
    points = points.sort_values("radius_kpc").reset_index(drop=True)
    scores = pd.read_csv(DATA / "ugc12506_theta_xit_combined_control_replay_scores.csv")
    summary = pd.read_csv(DATA / "ugc12506_theta_xit_combined_control_replay_summary.csv").iloc[0]

    r = points["radius_kpc"].to_numpy(float)
    obs = points["vobs_kms"].to_numpy(float)
    err = points["errv_kms"].to_numpy(float)

    curves = [
        ("Newtonian baryonic", "v_baryon_050_kms", "#8c8c8c", "--", 1.5),
        ("source-native NFW-HSE", "v_source_native_nfw_hse_positive_kms", "#b2182b", "-.", 1.6),
        ("projection-history base", "v_projection_history_incremental_positive_kms", "#5e3c99", "-", 1.8),
        (r"$\Theta_{\rm morph}$ only", "v_theta_morph_phase_positive_kms", "#008b8b", "-", 2.4),
        (
            r"$\Theta_{\rm morph}$ + $\Xi_t$ cap-only control",
            "v_theta_xit_cap_only_control_kms",
            "#e66101",
            "-",
            2.5,
        ),
        (
            r"shared-context $K_t$ stress control",
            "v_theta_xit_shared_high_control_kms",
            "#b2182b",
            ":",
            2.0,
        ),
    ]

    fig, (ax, ax_resid) = plt.subplots(
        2,
        1,
        figsize=(10.4, 8.4),
        sharex=True,
        gridspec_kw={"height_ratios": [2.35, 1.0], "hspace": 0.05},
    )
    ax.errorbar(
        r,
        obs,
        yerr=err,
        fmt="o",
        ms=4.5,
        lw=0.8,
        color="black",
        ecolor="#555555",
        capsize=2,
        label="observed SPARC",
        zorder=10,
    )

    for label, col, color, style, width in curves:
        ax.plot(r, points[col], color=color, ls=style, lw=width, label=label)

    ax.set_ylabel("Rotation speed [km/s]")
    ax.set_title("UGC12506 control comparison: morphology phase vs clock/readout cap")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2, loc="lower right")

    residual_curves = [
        (r"$\Theta_{\rm morph}$ only", "v_theta_morph_phase_positive_kms", "#008b8b", "-", 2.0),
        (
            r"$\Theta_{\rm morph}$ + $\Xi_t$ cap-only",
            "v_theta_xit_cap_only_control_kms",
            "#e66101",
            "-",
            2.2,
        ),
        (
            r"shared-context $K_t$ stress",
            "v_theta_xit_shared_high_control_kms",
            "#b2182b",
            ":",
            1.8,
        ),
        ("projection-history base", "v_projection_history_incremental_positive_kms", "#5e3c99", "--", 1.5),
    ]
    ax_resid.axhline(0.0, color="#999999", lw=1.0)
    for label, col, color, style, width in residual_curves:
        ax_resid.plot(r, obs - points[col], color=color, ls=style, lw=width, label=label)
    ax_resid.set_xlabel("Radius [kpc]")
    ax_resid.set_ylabel("obs - model [km/s]")
    ax_resid.grid(alpha=0.25)
    ax_resid.legend(
        frameon=False,
        fontsize=7.6,
        ncol=2,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.28),
    )

    note = (
        "Control replay only: combined endpoint remains blocked. "
        f"Theta RMSE={summary['theta_rmse_km_s']:.2f}, "
        f"cap-only RMSE={summary['combined_cap_only_rmse_km_s']:.2f}, "
        f"shared-Kt RMSE={summary['combined_shared_kt_high_rmse_km_s']:.2f} km/s."
    )
    fig.text(0.01, 0.006, note, fontsize=8.2, color="#333333")
    fig.subplots_adjust(left=0.08, right=0.985, top=0.92, bottom=0.19, hspace=0.05)

    png_path = FIGURES / "ugc12506_comparison_rotation_curves.png"
    pdf_path = FIGURES / "ugc12506_comparison_rotation_curves.pdf"
    paper_png = PAPER_FIGURES / "fig26_ugc12506_comparison_rotation_curves.png"
    fig.savefig(png_path, dpi=220)
    fig.savefig(pdf_path)
    fig.savefig(paper_png, dpi=220)
    plt.close(fig)

    compact_scores = scores[
        [
            "model_id",
            "model_role",
            "channel_policy",
            "rmse_km_s",
            "weighted_rmse_km_s",
            "mae_km_s",
            "endpoint_validation_claim",
        ]
    ].copy()
    compact_scores.to_csv(DATA / "ugc12506_comparison_rotation_curve_scores.csv", index=False)

    print(f"wrote {png_path}")
    print(f"wrote {pdf_path}")
    print(f"wrote {paper_png}")
    print(compact_scores.to_string(index=False))


if __name__ == "__main__":
    main()
