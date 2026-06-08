#!/usr/bin/env python3
"""Diagnostic amplitude normalization for UGC12506 source-native NFW/HSE.

This script answers a narrow shape question: if the source-native NFW/HSE
kernel shape is kept fixed, how much scalar amplitude would be required to
follow the observed rotation curve?  The normalization uses v_obs and is
therefore diagnostic only.  It must not be promoted as an endpoint or as a
source-frozen Tau Core normalization law.
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
CLAIM_BOUNDARY = "ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only"


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


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    weights = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(weights * np.square(pred - obs)) / np.sum(weights)))


def best_beta_v2(target_v2: np.ndarray, carrier_v2: np.ndarray, delta_v2: np.ndarray) -> float:
    y = target_v2 - carrier_v2
    denom = float(np.dot(delta_v2, delta_v2))
    if denom <= 1.0e-12:
        return 0.0
    return max(float(np.dot(delta_v2, y) / denom), 0.0)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    shell_summary = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_summary.csv").iloc[0]
    if bool(shell_summary["construction_used_vobs_or_residual"]):
        raise RuntimeError("Input shell must be residual-blind before diagnostic normalization")

    grid = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    r = grid["radius_kpc"].to_numpy(dtype=float)
    obs = grid["vobs_kms"].to_numpy(dtype=float)
    err = grid["errv_kms"].to_numpy(dtype=float)
    carrier = grid["v_baryon_050_kms"].to_numpy(dtype=float)
    carrier_v2 = np.square(carrier)
    nominal = grid["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    delta_v2 = (
        grid["v2_source_native_nfw_hse_positive_km2_s2"].to_numpy(dtype=float)
        - grid["v2_carrier_km2_s2"].to_numpy(dtype=float)
    )

    beta_all = best_beta_v2(np.square(obs), carrier_v2, delta_v2)
    normalized_v2 = carrier_v2 + beta_all * delta_v2
    normalized = np.sqrt(np.maximum(normalized_v2, 0.0))

    n = len(r)
    holdout_mask = np.zeros(n, dtype=bool)
    holdout_mask[::3] = True
    train_mask = ~holdout_mask
    beta_train = best_beta_v2(np.square(obs[train_mask]), carrier_v2[train_mask], delta_v2[train_mask])
    train_norm = np.sqrt(np.maximum(carrier_v2 + beta_train * delta_v2, 0.0))

    prior = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    prior = prior.loc[prior["galaxy"].eq(GALAXY)].copy().sort_values("rmse_kms")
    prior_best = prior.iloc[0]

    scores = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": "BARYONIC_CARRIER_V050",
                "normalization_role": "carrier_reference",
                "beta": 0.0,
                "n_points": int(n),
                "rmse_km_s": rmse(obs, carrier),
                "weighted_rmse_km_s": wrmse(obs, carrier, err),
                "holdout_rmse_km_s": rmse(obs[holdout_mask], carrier[holdout_mask]),
                "uses_vobs_for_normalization": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_SOURCE_NATIVE_NFW_HSE_NOMINAL",
                "normalization_role": "source_frozen_nominal_reference",
                "beta": 1.0,
                "n_points": int(n),
                "rmse_km_s": rmse(obs, nominal),
                "weighted_rmse_km_s": wrmse(obs, nominal, err),
                "holdout_rmse_km_s": rmse(obs[holdout_mask], nominal[holdout_mask]),
                "uses_vobs_for_normalization": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_SOURCE_NATIVE_NFW_HSE_ALL_POINT_NORMALIZED",
                "normalization_role": "residual_aware_shape_diagnostic",
                "beta": beta_all,
                "n_points": int(n),
                "rmse_km_s": rmse(obs, normalized),
                "weighted_rmse_km_s": wrmse(obs, normalized, err),
                "holdout_rmse_km_s": rmse(obs[holdout_mask], normalized[holdout_mask]),
                "uses_vobs_for_normalization": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_SOURCE_NATIVE_NFW_HSE_TRAIN_NORMALIZED",
                "normalization_role": "train_split_residual_aware_shape_diagnostic",
                "beta": beta_train,
                "n_points": int(n),
                "rmse_km_s": rmse(obs, train_norm),
                "weighted_rmse_km_s": wrmse(obs, train_norm, err),
                "holdout_rmse_km_s": rmse(obs[holdout_mask], train_norm[holdout_mask]),
                "uses_vobs_for_normalization": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    for _, row in prior.iterrows():
        scores.loc[len(scores)] = {
            "galaxy": GALAXY,
            "model_id": f"PRIOR_DIAGNOSTIC_{row['model_id']}",
            "normalization_role": "prior_diagnostic_reference_not_same_carrier",
            "beta": np.nan,
            "n_points": int(row["n_points"]),
            "rmse_km_s": float(row["rmse_kms"]),
            "weighted_rmse_km_s": np.nan,
            "holdout_rmse_km_s": np.nan,
            "uses_vobs_for_normalization": False,
            "endpoint_validation_claim": False,
            "claim_boundary": "prior_multigalaxy_fit_inspection_reference_not_endpoint_validation",
        }
    scores = scores.sort_values("rmse_km_s").reset_index(drop=True)

    all_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_ALL_POINT_NORMALIZED"),
            "rmse_km_s",
        ].iloc[0]
    )
    train_holdout_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_TRAIN_NORMALIZED"),
            "holdout_rmse_km_s",
        ].iloc[0]
    )
    nominal_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_NOMINAL"),
            "rmse_km_s",
        ].iloc[0]
    )

    summary = pd.DataFrame(
        [
            {
                "normalization_diagnostic_status": (
                    "UGC12506_SOURCE_NATIVE_NFW_HSE_SHAPE_NORMALIZES_WELL_DIAGNOSTIC_ONLY"
                    if all_rmse < nominal_rmse and all_rmse < float(prior_best["rmse_kms"])
                    else "UGC12506_SOURCE_NATIVE_NFW_HSE_NORMALIZATION_DIAGNOSTIC_GAP_REMAINS"
                ),
                "galaxy": GALAXY,
                "n_points": int(n),
                "beta_all_point_v2": beta_all,
                "beta_train_split_v2": beta_train,
                "nominal_rmse_km_s": nominal_rmse,
                "all_point_normalized_rmse_km_s": all_rmse,
                "train_normalized_holdout_rmse_km_s": train_holdout_rmse,
                "prior_best_diagnostic_model": str(prior_best["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(prior_best["rmse_kms"]),
                "all_point_minus_prior_best_diagnostic_rmse_km_s": all_rmse
                - float(prior_best["rmse_kms"]),
                "diagnostic_used_vobs_or_residual": True,
                "source_frozen_normalization_law_derived": False,
                "endpoint_validation_claim": False,
                "interpretation": (
                    "fixed source-native NFW/HSE shape can be made competitive only by "
                    "a residual-aware scalar normalization; this identifies the missing "
                    "source-side amplitude law and is not endpoint evidence"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    points = grid[
        [
            "galaxy",
            "radius_kpc",
            "vobs_kms",
            "errv_kms",
            "v_baryon_050_kms",
            "v_source_native_nfw_hse_positive_kms",
        ]
    ].copy()
    points["v_nfw_hse_all_point_normalized_kms"] = normalized
    points["v_nfw_hse_train_normalized_kms"] = train_norm
    points["beta_all_point_v2"] = beta_all
    points["beta_train_split_v2"] = beta_train
    points["is_holdout_point"] = holdout_mask
    points["diagnostic_used_vobs_or_residual"] = True
    points["endpoint_validation_claim"] = False
    points["claim_boundary"] = CLAIM_BOUNDARY

    fig, (ax, axr) = plt.subplots(
        2,
        1,
        figsize=(8.8, 7.2),
        sharex=True,
        gridspec_kw={"height_ratios": [2.4, 1.0]},
    )
    ax.errorbar(r, obs, yerr=err, fmt="o", ms=4, lw=0.8, color="black", label="observed")
    ax.plot(r, carrier, color="#777777", lw=1.8, label="baryonic carrier")
    ax.plot(r, nominal, color="#b2182b", lw=2.0, label="source-native NFW/HSE nominal")
    ax.plot(
        r,
        normalized,
        color="#f28e2b",
        lw=2.6,
        label=f"all-point normalized diagnostic (beta={beta_all:.2f})",
    )
    ax.plot(
        r,
        train_norm,
        color="#4c78a8",
        lw=2.0,
        ls="--",
        label=f"train-normalized diagnostic (beta={beta_train:.2f})",
    )
    ax.scatter(r[holdout_mask], obs[holdout_mask], facecolors="none", edgecolors="#4c78a8", s=68, lw=1.1, label="holdout markers")
    ax.set_title("UGC12506 source-native NFW/HSE amplitude-normalization diagnostic")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2)

    axr.axhline(0, color="#333333", lw=1.0)
    axr.plot(r, nominal - obs, color="#b2182b", lw=1.8, label="nominal residual")
    axr.plot(r, normalized - obs, color="#f28e2b", lw=2.2, label="all-point normalized residual")
    axr.plot(r, train_norm - obs, color="#4c78a8", lw=1.8, ls="--", label="train-normalized residual")
    axr.set_xlabel("Radius [kpc]")
    axr.set_ylabel("model - obs [km/s]")
    axr.grid(True, alpha=0.25)
    axr.legend(frameon=False, fontsize=8, ncol=2)
    fig.tight_layout()
    fig_path = FIGURES / "ugc12506_source_native_nfw_hse_normalization_diagnostic.png"
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)

    summary.to_csv(DATA / "ugc12506_source_native_nfw_hse_normalization_diagnostic_summary.csv", index=False)
    scores.to_csv(DATA / "ugc12506_source_native_nfw_hse_normalization_diagnostic_scores.csv", index=False)
    points.to_csv(DATA / "ugc12506_source_native_nfw_hse_normalization_diagnostic_points.csv", index=False)

    report = [
        "# UGC12506 Source-Native NFW/HSE Normalization Diagnostic",
        "",
        "This is a residual-aware shape diagnostic. It keeps the source-native",
        "NFW/HSE kernel fixed and fits only one scalar velocity-squared amplitude",
        "multiplier. Because the multiplier uses v_obs, it is not endpoint",
        "evidence and not a source-frozen Tau Core normalization law.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        f"![UGC12506 source-native NFW/HSE normalization diagnostic]({fig_path})",
        "",
    ]
    (REPORTS / "ugc12506_source_native_nfw_hse_normalization_diagnostic.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
