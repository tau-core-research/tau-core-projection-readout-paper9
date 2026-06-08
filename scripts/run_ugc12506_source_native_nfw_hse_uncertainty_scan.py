#!/usr/bin/env python3
"""Scan UGC12506 source-native NFW-HSE uncertainty variants.

This is a sensitivity diagnostic, not a retuning step.  It varies only the
published Table 5 NFW c and R200 values within their quoted one-sigma source
uncertainties while keeping the source-frozen amplitude rule unchanged.
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
CLAIM_BOUNDARY = "ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint"


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


def normalized(x: np.ndarray) -> np.ndarray:
    m = float(np.max(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def nfw_velocity2_shape(r_kpc: np.ndarray, concentration: float, r200_kpc: float) -> np.ndarray:
    y = np.maximum(r_kpc / max(r200_kpc, 1.0e-9), 1.0e-9)
    cy = concentration * y
    denom = np.log1p(concentration) - concentration / (1.0 + concentration)
    profile = (np.log1p(cy) - cy / (1.0 + cy)) / np.maximum(y * denom, 1.0e-12)
    return normalized(profile)


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def delta_label(delta: int) -> str:
    if delta < 0:
        return f"m{abs(delta)}"
    if delta > 0:
        return f"p{delta}"
    return "0"


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_manifest.csv").iloc[0]
    if bool(freeze["construction_used_vobs_or_residual"]):
        raise RuntimeError("Source-native NFW-HSE shell is not residual-blind")

    grid = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    r = grid["radius_kpc"].to_numpy(dtype=float)
    obs = grid["vobs_kms"].to_numpy(dtype=float)
    carrier_v2 = grid["v2_carrier_km2_s2"].to_numpy(dtype=float)
    k_env = grid["K_highspin_envelope"].to_numpy(dtype=float)
    outer_window = grid["W_outer_Rd_to_RHI_source"].to_numpy(dtype=float)
    amplitude = float(manifest["amplitude_total_km2_s2"])

    c0 = float(manifest["nfw_c"])
    dc = float(manifest["nfw_c_err"])
    r200_0 = float(manifest["nfw_r200_kpc"])
    dr200 = float(manifest["nfw_r200_err_kpc"])
    variants = []
    variant_points = []
    for c_delta in [-1, 0, 1]:
        for r_delta in [-1, 0, 1]:
            c = c0 + c_delta * dc
            r200 = r200_0 + r_delta * dr200
            k_nfw = nfw_velocity2_shape(r, c, r200)
            k = normalized((1.0 - outer_window) * k_nfw + outer_window * np.maximum(k_nfw, k_env))
            v = np.sqrt(np.maximum(carrier_v2 + amplitude * k, 0.0))
            model_id = f"c{delta_label(c_delta)}_r200{delta_label(r_delta)}"
            variants.append(
                {
                    "galaxy": GALAXY,
                    "variant_id": model_id,
                    "nfw_c": c,
                    "nfw_r200_kpc": r200,
                    "rs_nfw_kpc": r200 / c,
                    "rmse_km_s": rmse(obs, v),
                    "mean_kernel": float(np.mean(k)),
                    "inner_kernel_mean_first8": float(np.mean(k[:8])),
                    "outer_kernel_mean_last8": float(np.mean(k[-8:])),
                    "uses_only_source_uncertainty_box": True,
                    "construction_used_vobs_or_residual": False,
                    "scoring_used_vobs": True,
                    "endpoint_validation_claim": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
            for radius, kval, pred in zip(r, k, v):
                variant_points.append(
                    {
                        "galaxy": GALAXY,
                        "variant_id": model_id,
                        "radius_kpc": radius,
                        "K_variant": kval,
                        "v_variant_kms": pred,
                        "nfw_c": c,
                        "nfw_r200_kpc": r200,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

    variants_df = pd.DataFrame(variants).sort_values("rmse_km_s").reset_index(drop=True)
    points_df = pd.DataFrame(variant_points)
    best = variants_df.iloc[0]
    nominal = variants_df.loc[variants_df["variant_id"].eq("c0_r2000")].iloc[0]
    prior = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    prior_best = prior.loc[prior["galaxy"].eq(GALAXY)].sort_values("rmse_kms").iloc[0]
    summary = pd.DataFrame(
        [
            {
                "scan_status": "UGC12506_SOURCE_NATIVE_NFW_HSE_UNCERTAINTY_SCAN_COMPLETE_GAP_REMAINS",
                "galaxy": GALAXY,
                "n_variants": int(len(variants_df)),
                "nominal_rmse_km_s": float(nominal["rmse_km_s"]),
                "best_uncertainty_variant": str(best["variant_id"]),
                "best_uncertainty_rmse_km_s": float(best["rmse_km_s"]),
                "best_minus_nominal_rmse_km_s": float(best["rmse_km_s"] - nominal["rmse_km_s"]),
                "prior_best_diagnostic_model": str(prior_best["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(prior_best["rmse_kms"]),
                "best_uncertainty_minus_prior_best_diagnostic_rmse_km_s": float(
                    best["rmse_km_s"] - prior_best["rmse_kms"]
                ),
                "interpretation": (
                    "quoted c/R200 uncertainty cannot close the gap to prior diagnostic references"
                ),
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fig, ax = plt.subplots(figsize=(7.2, 4.8))
    ax.scatter(variants_df["rs_nfw_kpc"], variants_df["rmse_km_s"], color="#b2182b", s=42)
    for _, row in variants_df.iterrows():
        ax.text(row["rs_nfw_kpc"], row["rmse_km_s"] + 0.08, row["variant_id"], fontsize=7, ha="center")
    ax.axhline(float(prior_best["rmse_kms"]), color="#555555", lw=1.2, ls="--", label="prior best diagnostic")
    ax.set_xlabel("Source-native NFW scale radius R200/c [kpc]")
    ax.set_ylabel("RMSE [km/s]")
    ax.set_title("UGC12506 source-native NFW-HSE uncertainty scan")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_source_native_nfw_hse_uncertainty_scan.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    variants_df.to_csv(DATA / "ugc12506_source_native_nfw_hse_uncertainty_scan_variants.csv", index=False)
    points_df.to_csv(DATA / "ugc12506_source_native_nfw_hse_uncertainty_scan_points.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_native_nfw_hse_uncertainty_scan_summary.csv", index=False)

    report = [
        "# UGC12506 Source-Native NFW-HSE Uncertainty Scan",
        "",
        "This diagnostic varies only the published Table 5 NFW concentration and",
        "R200 within their quoted one-sigma source uncertainties. It does not",
        "retune labels, signs, kernels, or amplitudes from endpoint residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Variants",
        "",
        markdown_table(variants_df),
        "",
        f"![UGC12506 source-native NFW-HSE uncertainty scan]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_source_native_nfw_hse_uncertainty_scan.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(variants_df.to_string(index=False))


if __name__ == "__main__":
    main()
