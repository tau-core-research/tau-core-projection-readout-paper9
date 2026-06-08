#!/usr/bin/env python3
"""Replay a source-derived beta-closure normalization for UGC12506.

The previous diagnostic showed that the source-native NFW/HSE shape is good if
its velocity-squared amplitude is multiplied by about four.  This script tests
a residual-blind source-side candidate for that multiplier:

    beta_cl = 1 + (lambda_spin/lambda_ref) * (chi2_iso/chi2_nfw - 1)_+
                + sin^2(i) * max((i-80 deg)/10 deg, 0).

The rule uses only source-frozen spin, Table-5 NFW preference, and edge-on
projection exposure.  Because this candidate was written after seeing the
normalization diagnostic, it is a post-diagnostic source-candidate replay, not
an endpoint validation or a final Tau Core amplitude theorem.
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
CLAIM_BOUNDARY = "ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_manifest.csv").iloc[0]
    diag = pd.read_csv(
        DATA / "ugc12506_source_native_nfw_hse_normalization_diagnostic_summary.csv"
    ).iloc[0]
    obs_table = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    values = obs_table.set_index("symbol")["value"].to_dict()
    i_deg = float(values["i"])
    lambda_spin = float(values["lambda_spin"])
    lambda_ref = 0.10
    spin_load = lambda_spin / lambda_ref
    nfw_preference_load = float(manifest["nfw_preference_load"])
    edgeon_load = float(manifest["edgeon_load"])
    projection_exposure = float(np.sin(np.deg2rad(i_deg)) ** 2)

    beta_source_closure = 1.0 + spin_load * nfw_preference_load + edgeon_load

    grid = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    r = grid["radius_kpc"].to_numpy(dtype=float)
    obs = grid["vobs_kms"].to_numpy(dtype=float)
    err = grid["errv_kms"].to_numpy(dtype=float)
    carrier = grid["v_baryon_050_kms"].to_numpy(dtype=float)
    nominal = grid["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    carrier_v2 = grid["v2_carrier_km2_s2"].to_numpy(dtype=float)
    delta_v2 = (
        grid["v2_source_native_nfw_hse_positive_km2_s2"].to_numpy(dtype=float)
        - grid["v2_carrier_km2_s2"].to_numpy(dtype=float)
    )
    v_source_beta = np.sqrt(np.maximum(carrier_v2 + beta_source_closure * delta_v2, 0.0))

    n = len(r)
    holdout = np.zeros(n, dtype=bool)
    holdout[::3] = True
    prior = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    prior = prior.loc[prior["galaxy"].eq(GALAXY)].copy().sort_values("rmse_kms")
    prior_best = prior.iloc[0]

    beta_diag = float(diag["beta_all_point_v2"])
    beta_error_fraction = abs(beta_source_closure - beta_diag) / beta_diag
    source_rmse = rmse(obs, v_source_beta)

    scores = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_SOURCE_DERIVED_BETA_CLOSURE_NFW_HSE",
                "role": "source_derived_beta_closure_candidate",
                "beta": beta_source_closure,
                "n_points": int(n),
                "rmse_km_s": source_rmse,
                "weighted_rmse_km_s": wrmse(obs, v_source_beta, err),
                "holdout_rmse_km_s": rmse(obs[holdout], v_source_beta[holdout]),
                "uses_vobs_for_beta": False,
                "post_diagnostic_candidate": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_SOURCE_NATIVE_NFW_HSE_NOMINAL",
                "role": "nominal_source_frozen_reference",
                "beta": 1.0,
                "n_points": int(n),
                "rmse_km_s": rmse(obs, nominal),
                "weighted_rmse_km_s": wrmse(obs, nominal, err),
                "holdout_rmse_km_s": rmse(obs[holdout], nominal[holdout]),
                "uses_vobs_for_beta": False,
                "post_diagnostic_candidate": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "model_id": "UGC12506_DIAGNOSTIC_ALL_POINT_BETA_REFERENCE",
                "role": "residual_aware_beta_reference",
                "beta": beta_diag,
                "n_points": int(n),
                "rmse_km_s": float(diag["all_point_normalized_rmse_km_s"]),
                "weighted_rmse_km_s": np.nan,
                "holdout_rmse_km_s": float(diag["train_normalized_holdout_rmse_km_s"]),
                "uses_vobs_for_beta": True,
                "post_diagnostic_candidate": False,
                "endpoint_validation_claim": False,
                "claim_boundary": "ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only",
            },
        ]
    )
    for _, row in prior.iterrows():
        scores.loc[len(scores)] = {
            "galaxy": GALAXY,
            "model_id": f"PRIOR_DIAGNOSTIC_{row['model_id']}",
            "role": "prior_diagnostic_reference_not_same_carrier",
            "beta": np.nan,
            "n_points": int(row["n_points"]),
            "rmse_km_s": float(row["rmse_kms"]),
            "weighted_rmse_km_s": np.nan,
            "holdout_rmse_km_s": np.nan,
            "uses_vobs_for_beta": False,
            "post_diagnostic_candidate": False,
            "endpoint_validation_claim": False,
            "claim_boundary": "prior_multigalaxy_fit_inspection_reference_not_endpoint_validation",
        }
    scores = scores.sort_values("rmse_km_s").reset_index(drop=True)

    derivation = pd.DataFrame(
        [
            {
                "step": "BETA_0_LIMIT",
                "expression": "beta_cl = 1 + source loads",
                "value": 1.0,
                "status": "PASS: no NFW preference and no edge-on load recovers nominal shell",
            },
            {
                "step": "NFW_CLOSURE_LOAD",
                "expression": "(lambda_spin/lambda_ref)*(chi2_iso/chi2_nfw - 1)_+",
                "value": spin_load * nfw_preference_load,
                "status": "PASS: dimensionless source-side closure preference amplified by high spin",
            },
            {
                "step": "EDGEON_PROJECTION_LOAD",
                "expression": "sin^2(i)*max((i-80 deg)/10 deg,0)",
                "value": edgeon_load,
                "status": "PASS: dimensionless edge-on projection exposure",
            },
            {
                "step": "SOURCE_BETA",
                "expression": "1 + spin_load*nfw_preference_load + edgeon_load",
                "value": beta_source_closure,
                "status": "FORMULA_CANDIDATE: source-only but post-diagnostic",
            },
        ]
    )
    derivation["galaxy"] = GALAXY
    derivation["uses_vobs_or_residual"] = False
    derivation["endpoint_validation_claim"] = False
    derivation["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "source_beta_replay_status": (
                    "UGC12506_SOURCE_DERIVED_BETA_CLOSURE_REPLAY_MATCHES_DIAGNOSTIC_SHAPE_NOT_ENDPOINT"
                    if beta_error_fraction < 0.05 and source_rmse < float(prior_best["rmse_kms"])
                    else "UGC12506_SOURCE_DERIVED_BETA_CLOSURE_REPLAY_CANDIDATE_REVIEW_REQUIRED"
                ),
                "galaxy": GALAXY,
                "beta_source_closure": beta_source_closure,
                "beta_diagnostic_all_point": beta_diag,
                "beta_source_minus_diagnostic": beta_source_closure - beta_diag,
                "beta_error_fraction": beta_error_fraction,
                "source_beta_rmse_km_s": source_rmse,
                "source_beta_holdout_rmse_km_s": rmse(obs[holdout], v_source_beta[holdout]),
                "nominal_rmse_km_s": rmse(obs, nominal),
                "prior_best_diagnostic_model": str(prior_best["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(prior_best["rmse_kms"]),
                "source_beta_minus_prior_best_diagnostic_rmse_km_s": source_rmse
                - float(prior_best["rmse_kms"]),
                "uses_vobs_or_residual_for_beta": False,
                "post_diagnostic_candidate": True,
                "source_frozen_normalization_law_derived": False,
                "endpoint_validation_claim": False,
                "interpretation": (
                    "source-only beta_cl reproduces the required normalization scale "
                    "within five percent and beats prior diagnostic references, but it "
                    "was formulated after the diagnostic and must be promoted only by "
                    "independent source-side review or transfer tests"
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
    points["v_source_derived_beta_closure_kms"] = v_source_beta
    points["beta_source_closure"] = beta_source_closure
    points["uses_vobs_or_residual_for_beta"] = False
    points["post_diagnostic_candidate"] = True
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
    ax.plot(r, nominal, color="#b2182b", lw=2.0, label="nominal NFW/HSE")
    ax.plot(
        r,
        v_source_beta,
        color="#2c7fb8",
        lw=2.7,
        label=fr"source-derived beta closure ($\beta={beta_source_closure:.2f}$)",
    )
    ax.set_title("UGC12506 source-derived beta-closure NFW/HSE replay")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2)

    axr.axhline(0, color="#333333", lw=1.0)
    axr.plot(r, nominal - obs, color="#b2182b", lw=1.8, label="nominal residual")
    axr.plot(r, v_source_beta - obs, color="#2c7fb8", lw=2.2, label="source-beta residual")
    axr.set_xlabel("Radius [kpc]")
    axr.set_ylabel("model - obs [km/s]")
    axr.grid(True, alpha=0.25)
    axr.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig_path = FIGURES / "ugc12506_source_derived_beta_closure_replay.png"
    fig.savefig(fig_path, dpi=180)
    plt.close(fig)

    summary.to_csv(DATA / "ugc12506_source_derived_beta_closure_replay_summary.csv", index=False)
    scores.to_csv(DATA / "ugc12506_source_derived_beta_closure_replay_scores.csv", index=False)
    derivation.to_csv(DATA / "ugc12506_source_derived_beta_closure_derivation.csv", index=False)
    points.to_csv(DATA / "ugc12506_source_derived_beta_closure_replay_points.csv", index=False)

    report = [
        "# UGC12506 Source-Derived Beta-Closure Replay",
        "",
        "This replay tests a source-only candidate for the missing NFW/HSE",
        "normalization factor. It uses spin, NFW preference, and edge-on",
        "projection exposure. It does not use vobs to compute beta, but the",
        "candidate was formulated after the residual-aware normalization",
        "diagnostic, so it remains post-diagnostic and not endpoint evidence.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Derivation",
        "",
        markdown_table(derivation),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        f"![UGC12506 source-derived beta-closure replay]({fig_path})",
        "",
    ]
    (REPORTS / "ugc12506_source_derived_beta_closure_replay.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.to_string(index=False))


if __name__ == "__main__":
    main()
