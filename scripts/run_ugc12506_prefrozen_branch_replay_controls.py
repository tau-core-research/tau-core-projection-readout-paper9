#!/usr/bin/env python3
"""Score UGC12506 prefrozen high-spin/projection branch controls.

This script is the first step that reads vobs for this UGC12506 lane.  It reads
the replay gate manifest unchanged and reports the result as a caveated
single-galaxy control replay, not population validation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_prefrozen_branch_replay_controls_not_validation"


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


def rmse(obs: pd.Series | np.ndarray, pred: pd.Series | np.ndarray) -> float:
    obs_arr = np.asarray(obs, dtype=float)
    pred_arr = np.asarray(pred, dtype=float)
    return float(np.sqrt(np.mean(np.square(pred_arr - obs_arr))))


def mae(obs: pd.Series | np.ndarray, pred: pd.Series | np.ndarray) -> float:
    obs_arr = np.asarray(obs, dtype=float)
    pred_arr = np.asarray(pred, dtype=float)
    return float(np.mean(np.abs(pred_arr - obs_arr)))


def wrmse(obs: pd.Series, pred: pd.Series | np.ndarray, err: pd.Series) -> float:
    obs_arr = np.asarray(obs, dtype=float)
    pred_arr = np.asarray(pred, dtype=float)
    err_arr = np.maximum(np.asarray(err, dtype=float), 1.0e-6)
    weights = 1.0 / np.square(err_arr)
    return float(np.sqrt(np.sum(weights * np.square(pred_arr - obs_arr)) / np.sum(weights)))


def safe_velocity(v2: pd.Series | np.ndarray) -> np.ndarray:
    return np.sqrt(np.maximum(np.asarray(v2, dtype=float), 0.0))


def score_row(
    model_id: str,
    model_role: str,
    obs: pd.Series,
    pred: pd.Series | np.ndarray,
    err: pd.Series,
) -> dict[str, object]:
    pred_arr = np.asarray(pred, dtype=float)
    obs_arr = np.asarray(obs, dtype=float)
    return {
        "galaxy": GALAXY,
        "model_id": model_id,
        "model_role": model_role,
        "n_points": int(len(obs_arr)),
        "rmse_km_s": rmse(obs_arr, pred_arr),
        "weighted_rmse_km_s": wrmse(obs, pred_arr, err),
        "mae_km_s": mae(obs_arr, pred_arr),
        "bias_km_s": float(np.mean(pred_arr - obs_arr)),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ugc12506_prefrozen_branch_control_replay_gate_manifest.csv").iloc[0]
    if not bool(manifest["control_replay_scores_allowed"]):
        raise RuntimeError("UGC12506 prefrozen branch control replay gate is blocked")
    if bool(manifest["endpoint_validation_claim_allowed"]):
        raise RuntimeError("This script must not run as endpoint validation")
    if bool(manifest["uses_vobs_or_residual_in_gate"]):
        raise RuntimeError("Gate was not residual-blind")

    points = pd.read_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_grid.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if points.empty:
        raise ValueError(f"No prefrozen UGC12506 points found")
    if bool(points["prefreeze_used_vobs_or_residual"].any()):
        raise RuntimeError("Prefreeze grid unexpectedly used vobs/residual")

    v2 = points["v2_carrier_km2_s2"].astype(float)
    ahs = float(manifest["highspin_amplitude_km2_s2"])
    apa = float(manifest["asymmetry_amplitude_km2_s2"])
    khs = points[str(manifest["highspin_kernel_column"])].astype(float)
    kpa = points[str(manifest["asymmetry_kernel_column"])].astype(float)

    points["v_highspin_positive_replay_kms"] = safe_velocity(v2 + ahs * khs)
    points["v_highspin_negative_control_kms"] = safe_velocity(v2 - ahs * khs)
    points["v_asymmetry_positive_replay_kms"] = safe_velocity(v2 + apa * kpa)
    points["v_asymmetry_negative_control_kms"] = safe_velocity(v2 - apa * kpa)
    points["v_combined_positive_replay_kms"] = safe_velocity(v2 + ahs * khs + apa * kpa)
    points["v_combined_negative_control_kms"] = safe_velocity(v2 - ahs * khs - apa * kpa)
    points["v_split_highspin_plus_asymmetry_minus_control_kms"] = safe_velocity(v2 + ahs * khs - apa * kpa)
    points["v_split_highspin_minus_asymmetry_plus_control_kms"] = safe_velocity(v2 - ahs * khs + apa * kpa)
    points["construction_used_vobs"] = False
    points["scoring_used_vobs"] = True
    points["endpoint_validation_claim"] = False
    points["claim_boundary"] = CLAIM_BOUNDARY

    obs = points["vobs_kms"]
    err = points["errv_kms"]
    scores = [
        score_row("BARYONIC_CARRIER_V050", "carrier_reference", obs, points["v_baryon_050_kms"], err),
        score_row(
            "UGC12506_HIGHS_PIN_POSITIVE_PREFROZEN",
            "source_prefrozen_positive_branch",
            obs,
            points["v_highspin_positive_replay_kms"],
            err,
        ),
        score_row(
            "UGC12506_HIGHS_PIN_NEGATIVE_ATTENUATION_CONTROL",
            "negative_sign_control",
            obs,
            points["v_highspin_negative_control_kms"],
            err,
        ),
        score_row(
            "UGC12506_PROJECTION_ASYMMETRY_POSITIVE_PREFROZEN",
            "source_prefrozen_positive_branch",
            obs,
            points["v_asymmetry_positive_replay_kms"],
            err,
        ),
        score_row(
            "UGC12506_PROJECTION_ASYMMETRY_NEGATIVE_CONTROL",
            "negative_sign_control",
            obs,
            points["v_asymmetry_negative_control_kms"],
            err,
        ),
        score_row(
            "UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN",
            "combined_positive_branch",
            obs,
            points["v_combined_positive_replay_kms"],
            err,
        ),
        score_row(
            "UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_NEGATIVE_CONTROL",
            "combined_negative_control",
            obs,
            points["v_combined_negative_control_kms"],
            err,
        ),
        score_row(
            "UGC12506_SPLIT_HS_PLUS_PA_MINUS_CONTROL",
            "split_sign_control",
            obs,
            points["v_split_highspin_plus_asymmetry_minus_control_kms"],
            err,
        ),
        score_row(
            "UGC12506_SPLIT_HS_MINUS_PA_PLUS_CONTROL",
            "split_sign_control",
            obs,
            points["v_split_highspin_minus_asymmetry_plus_control_kms"],
            err,
        ),
    ]

    prior_baselines = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    prior_baselines = prior_baselines.loc[prior_baselines["galaxy"].eq(GALAXY)].copy()
    for _, row in prior_baselines.iterrows():
        scores.append(
            {
                "galaxy": GALAXY,
                "model_id": f"PRIOR_DIAGNOSTIC_{row['model_id']}",
                "model_role": "prior_diagnostic_reference_not_same_carrier",
                "n_points": int(row["n_points"]),
                "rmse_km_s": float(row["rmse_kms"]),
                "weighted_rmse_km_s": np.nan,
                "mae_km_s": float(row["mae_kms"]),
                "bias_km_s": float(row["bias_kms"]),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "claim_boundary": "prior_multigalaxy_fit_inspection_reference_not_endpoint_validation",
            }
        )

    scores_df = pd.DataFrame(scores).sort_values("rmse_km_s").reset_index(drop=True)

    carrier_rmse = float(
        scores_df.loc[scores_df["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0]
    )
    branch_scores = scores_df.loc[
        scores_df["model_role"].isin(
            [
                "source_prefrozen_positive_branch",
                "combined_positive_branch",
                "negative_sign_control",
                "combined_negative_control",
                "split_sign_control",
            ]
        )
    ].copy()
    best_branch = branch_scores.sort_values("rmse_km_s").iloc[0]
    positive_branch_scores = scores_df.loc[
        scores_df["model_role"].isin(["source_prefrozen_positive_branch", "combined_positive_branch"])
    ].copy()
    best_positive = positive_branch_scores.sort_values("rmse_km_s").iloc[0]
    best_prior = prior_baselines.sort_values("rmse_kms").iloc[0] if not prior_baselines.empty else None

    max_outer_gap = float((points["vobs_kms"] - points["v_baryon_050_kms"]).tail(8).mean())
    max_positive_delta = float(
        (points["v_combined_positive_replay_kms"] - points["v_baryon_050_kms"]).tail(8).mean()
    )

    summary = pd.DataFrame(
        [
            {
                "replay_status": "UGC12506_PREFROZEN_BRANCH_REPLAY_COMPLETE_NOT_VALIDATION",
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "carrier_rmse_km_s": carrier_rmse,
                "best_prefrozen_branch_model": str(best_branch["model_id"]),
                "best_prefrozen_branch_role": str(best_branch["model_role"]),
                "best_prefrozen_branch_rmse_km_s": float(best_branch["rmse_km_s"]),
                "best_positive_prefrozen_model": str(best_positive["model_id"]),
                "best_positive_prefrozen_rmse_km_s": float(best_positive["rmse_km_s"]),
                "best_positive_minus_carrier_rmse_km_s": float(best_positive["rmse_km_s"]) - carrier_rmse,
                "best_branch_minus_carrier_rmse_km_s": float(best_branch["rmse_km_s"]) - carrier_rmse,
                "prior_best_diagnostic_model": "" if best_prior is None else str(best_prior["model_id"]),
                "prior_best_diagnostic_rmse_km_s": np.nan if best_prior is None else float(best_prior["rmse_kms"]),
                "best_positive_minus_prior_best_diagnostic_rmse_km_s": (
                    np.nan
                    if best_prior is None
                    else float(best_positive["rmse_km_s"]) - float(best_prior["rmse_kms"])
                ),
                "outer_mean_observed_minus_baryonic_km_s_last8": max_outer_gap,
                "outer_mean_combined_positive_lift_km_s_last8": max_positive_delta,
                "lift_fraction_of_outer_gap_last8": (
                    np.nan if abs(max_outer_gap) < 1.0e-9 else max_positive_delta / max_outer_gap
                ),
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "population_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "interpretation": (
                    "prefrozen control replay; if weak, diagnose source-normalized amplitude/kernel "
                    "strength rather than retuning from residuals"
                ),
            }
        ]
    )

    diagnostics = pd.DataFrame(
        [
            {
                "diagnostic_id": "D1_AMPLITUDE_STRENGTH",
                "status": (
                    "AMPLITUDE_TOO_WEAK_FOR_OUTER_GAP"
                    if summary["lift_fraction_of_outer_gap_last8"].iloc[0] < 0.25
                    else "AMPLITUDE_HAS_VISIBLE_OUTER_LIFT"
                ),
                "value": float(summary["lift_fraction_of_outer_gap_last8"].iloc[0]),
                "interpretation": (
                    "Compares the source-frozen combined positive branch lift to the outer observed-baryonic gap. "
                    "Low values mean the replay is source-clean but underpowered."
                ),
            },
            {
                "diagnostic_id": "D2_SIGN_BRANCH",
                "status": (
                    "POSITIVE_BRANCH_IS_BEST_PREFROZEN_BRANCH"
                    if str(best_branch["model_role"]) in ["source_prefrozen_positive_branch", "combined_positive_branch"]
                    else "CONTROL_BRANCH_BEATS_POSITIVE_BRANCH"
                ),
                "value": str(best_branch["model_id"]),
                "interpretation": "Sign is not promoted from this replay; this only diagnoses branch behavior.",
            },
            {
                "diagnostic_id": "D3_PRIOR_BASELINE_COMPARISON",
                "status": (
                    "POSITIVE_REPLAY_BEATS_PRIOR_BEST_DIAGNOSTIC"
                    if best_prior is not None and float(best_positive["rmse_km_s"]) < float(best_prior["rmse_kms"])
                    else "POSITIVE_REPLAY_DOES_NOT_BEAT_PRIOR_BEST_DIAGNOSTIC"
                ),
                "value": (
                    "nan"
                    if best_prior is None
                    else f"{float(best_positive['rmse_km_s']) - float(best_prior['rmse_kms']):.6g}"
                ),
                "interpretation": (
                    "Prior diagnostics are not identical baselines for this replay, but they expose whether the "
                    "new frozen branch is numerically competitive."
                ),
            },
        ]
    )

    points.to_csv(DATA / "ugc12506_prefrozen_branch_replay_control_points.csv", index=False)
    scores_df.to_csv(DATA / "ugc12506_prefrozen_branch_replay_control_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_prefrozen_branch_replay_control_summary.csv", index=False)
    diagnostics.to_csv(DATA / "ugc12506_prefrozen_branch_replay_control_diagnostics.csv", index=False)

    report = [
        "# UGC12506 Prefrozen Branch Replay Controls",
        "",
        "This is a caveated single-galaxy control replay. It reads `vobs` only",
        "after the source-normalized formula inputs have been frozen. It is not",
        "a population-validation endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores_df),
        "",
        "## Diagnostics",
        "",
        markdown_table(diagnostics),
        "",
        "## Claim Boundary",
        "",
        "Negative or weak results are preserved. Any change to the kernel, sign,",
        "or amplitude after this score demotes the next run to diagnostic unless",
        "it is justified by new residual-blind source evidence and replayed as a",
        "new frozen protocol.",
        "",
    ]
    (REPORTS / "ugc12506_prefrozen_branch_replay_controls.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores_df.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
