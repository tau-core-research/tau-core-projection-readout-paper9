#!/usr/bin/env python3
"""Run control replay for the distributed vertical/halo beta formula."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures" / "endpoint_diagnostics" / "beta_transfer_distributed_vertical_halo"
PAPER_FIGURES = ROOT / "papers" / "paper2_projection_enriched" / "source" / "figures"
MANIFEST = DATA / "beta_transfer_distributed_vertical_halo_formula_freeze_manifest.csv"
SOURCE_POINTS = DATA / "ugc12506_beta_closure_transfer_scoring_points.csv"
EVH_POINTS = DATA / "beta_transfer_edgeon_vertical_halo_control_replay_points.csv"
CLAIM_BOUNDARY = "beta_transfer_distributed_vertical_halo_control_replay_not_endpoint"


def smoothstep(x: np.ndarray) -> np.ndarray:
    t = np.clip(x, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def rmse(residual: np.ndarray) -> float:
    return float(np.sqrt(np.mean(residual * residual)))


def weighted_rmse(residual: np.ndarray, err: np.ndarray) -> float:
    safe_err = np.maximum(err, 1.0)
    weights = 1.0 / safe_err**2
    return float(np.sqrt(np.sum(weights * residual**2) / np.sum(weights)))


def score(galaxy: str, model_id: str, values: np.ndarray, g: pd.DataFrame) -> dict[str, object]:
    residual = g["vobs_kms"].to_numpy(float) - values
    err = g["errv_kms"].to_numpy(float)
    return {
        "galaxy": galaxy,
        "model_id": model_id,
        "n_points": len(g),
        "rmse_km_s": rmse(residual),
        "weighted_rmse_km_s": weighted_rmse(residual, err),
        "mae_km_s": float(np.mean(np.abs(residual))),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def plot_galaxy(galaxy: str, g: pd.DataFrame, formula_row: pd.Series, score_rows: list[dict[str, object]]) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    r = g["radius_kpc"].to_numpy(float)
    obs = g["vobs_kms"].to_numpy(float)
    err = g["errv_kms"].to_numpy(float)
    score_map = {s["model_id"]: s for s in score_rows if s["galaxy"] == galaxy}

    fig, (ax, ax_resid) = plt.subplots(
        2,
        1,
        figsize=(9.0, 6.8),
        sharex=True,
        gridspec_kw={"height_ratios": [2.25, 1.0], "hspace": 0.05},
    )
    ax.errorbar(
        r,
        obs,
        yerr=err,
        fmt="o",
        ms=4.2,
        lw=0.8,
        color="black",
        ecolor="#555555",
        capsize=2,
        label="observed",
        zorder=10,
    )
    curves = [
        ("baryonic carrier", "v_carrier_kms", "#8c8c8c", "--", 1.7),
        ("pure beta transfer", "v_beta_cl_transfer_kms", "#c51b7d", ":", 1.9),
        ("V1 far-outer EVH lock", "v_edgeon_vertical_halo_gated_beta_kms", "#d95f02", "-.", 1.9),
        ("current V2 distributed vertical/halo lock", "v_distributed_vertical_halo_beta_kms", "#e66101", "-", 3.4),
    ]
    for label, col, color, style, width in curves:
        ax.plot(r, g[col], color=color, ls=style, lw=width, label=label)
    ax.axvline(float(formula_row["r_on_kpc"]), color="#4d9221", lw=1.1, alpha=0.65)
    ax.axvline(float(formula_row["r_full_kpc"]), color="#4d9221", lw=1.1, alpha=0.65, ls="--")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.set_title(f"{galaxy}: distributed vertical/halo morphology refinement")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=7.7, loc="best")

    ax_resid.axhline(0.0, color="#999999", lw=1.0)
    for label, col, color, style, width in [
        ("obs - carrier", "v_carrier_kms", "#8c8c8c", "--", 1.5),
        ("obs - V1", "v_edgeon_vertical_halo_gated_beta_kms", "#d95f02", "-.", 1.7),
        ("obs - current V2", "v_distributed_vertical_halo_beta_kms", "#e66101", "-", 2.5),
    ]:
        ax_resid.plot(r, obs - g[col], color=color, ls=style, lw=width, label=label)
    ax_resid.set_xlabel("Radius [kpc]")
    ax_resid.set_ylabel("Residual [km/s]")
    ax_resid.grid(alpha=0.25)
    ax_resid.legend(frameon=False, fontsize=7.8, loc="best")

    note = (
        "Control replay only; not endpoint validation. "
        f"Carrier RMSE={score_map['BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE']['rmse_km_s']:.2f}; "
        f"V1 RMSE={score_map['EDGEON_VERTICAL_HALO_GATED_BETA_V1']['rmse_km_s']:.2f}; "
        f"current V2 RMSE={score_map['DISTRIBUTED_VERTICAL_HALO_BETA_V2']['rmse_km_s']:.2f} km/s."
    )
    fig.text(0.015, 0.012, note, fontsize=8.0, color="#333333")
    fig.subplots_adjust(left=0.09, right=0.985, top=0.91, bottom=0.15)

    safe = galaxy.lower().replace("-", "_")
    fig.savefig(FIGURES / f"{safe}_distributed_vertical_halo_control_replay.png", dpi=220)
    fig.savefig(FIGURES / f"{safe}_distributed_vertical_halo_control_replay.pdf")
    fig.savefig(PAPER_FIGURES / f"fig_beta_transfer_distributed_vertical_halo_{safe}.png", dpi=220)
    plt.close(fig)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    PAPER_FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(MANIFEST)
    points = pd.read_csv(SOURCE_POINTS)
    evh = pd.read_csv(EVH_POINTS)[
        ["galaxy", "radius_kpc", "v_edgeon_vertical_halo_gated_beta_kms"]
    ]
    points = points[points["galaxy"].isin(manifest["galaxy"])].copy()
    points = points.merge(evh, on=["galaxy", "radius_kpc"], how="left")

    point_frames = []
    score_rows = []
    for _, row in manifest.iterrows():
        galaxy = str(row["galaxy"])
        g = points[points["galaxy"].eq(galaxy)].sort_values("radius_kpc").copy()
        r = g["radius_kpc"].to_numpy(float)
        beta_cl = float(row["beta_cl_value"])
        r_on = float(row["r_on_kpc"])
        r_full = float(row["r_full_kpc"])
        k = smoothstep((r - r_on) / max(r_full - r_on, 1e-9))
        carrier = g["v_carrier_kms"].to_numpy(float)
        v2 = carrier**2 * (1.0 + (beta_cl - 1.0) * k)
        g["k_distributed_vertical_halo"] = k
        g["v_distributed_vertical_halo_beta_kms"] = np.sqrt(np.maximum(v2, 0.0))
        g["formula_id"] = str(row["formula_id"])
        g["r_on_kpc"] = r_on
        g["r_full_kpc"] = r_full
        g["construction_used_vobs"] = False
        g["scoring_used_vobs"] = True
        g["endpoint_validation_claim"] = False
        g["claim_boundary"] = CLAIM_BOUNDARY

        score_rows.extend(
            [
                score(galaxy, "BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE", carrier, g),
                score(galaxy, "BETA_CL_TRANSFER_SOURCE_FROZEN", g["v_beta_cl_transfer_kms"].to_numpy(float), g),
                score(galaxy, "EDGEON_VERTICAL_HALO_GATED_BETA_V1", g["v_edgeon_vertical_halo_gated_beta_kms"].to_numpy(float), g),
                score(galaxy, "DISTRIBUTED_VERTICAL_HALO_BETA_V2", g["v_distributed_vertical_halo_beta_kms"].to_numpy(float), g),
            ]
        )
        point_frames.append(g)

    points_out = pd.concat(point_frames, ignore_index=True)
    scores = pd.DataFrame(score_rows)
    comparison = scores.pivot(index="galaxy", columns="model_id", values="rmse_km_s").reset_index()
    comparison["v2_minus_v1_km_s"] = (
        comparison["DISTRIBUTED_VERTICAL_HALO_BETA_V2"]
        - comparison["EDGEON_VERTICAL_HALO_GATED_BETA_V1"]
    )
    comparison["v2_minus_carrier_km_s"] = (
        comparison["DISTRIBUTED_VERTICAL_HALO_BETA_V2"]
        - comparison["BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE"]
    )
    comparison["v2_beats_v1"] = comparison["v2_minus_v1_km_s"] < 0
    comparison["v2_beats_carrier"] = comparison["v2_minus_carrier_km_s"] < 0
    comparison["claim_boundary"] = CLAIM_BOUNDARY

    for _, row in manifest.iterrows():
        galaxy = str(row["galaxy"])
        plot_galaxy(galaxy, points_out[points_out["galaxy"].eq(galaxy)], row, score_rows)

    points_out.to_csv(DATA / "beta_transfer_distributed_vertical_halo_control_replay_points.csv", index=False)
    scores.to_csv(DATA / "beta_transfer_distributed_vertical_halo_control_replay_scores.csv", index=False)
    comparison.to_csv(DATA / "beta_transfer_distributed_vertical_halo_control_replay_comparison.csv", index=False)
    summary = pd.DataFrame(
        [
            {
                "control_replay_status": "DISTRIBUTED_VERTICAL_HALO_BETA_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT",
                "n_galaxies": comparison["galaxy"].nunique(),
                "n_points": len(points_out),
                "v2_beats_v1_count": int(comparison["v2_beats_v1"].sum()),
                "v2_beats_carrier_count": int(comparison["v2_beats_carrier"].sum()),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_action": "review_control_replay_before_formula_promotion",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(DATA / "beta_transfer_distributed_vertical_halo_control_replay_summary.csv", index=False)

    print(summary.to_string(index=False))
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()
