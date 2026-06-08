#!/usr/bin/env python3
"""Score the UGC12506 source-envelope support replay.

This is the first step that reads vobs for the stronger source-envelope shell.
The formula inputs are read from the freeze manifest and are not retuned here.
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
CLAIM_BOUNDARY = "ugc12506_source_envelope_support_replay_controls_not_validation"


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


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    w = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(w * np.square(pred - obs)) / np.sum(w)))


def score_row(model_id: str, role: str, obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> dict[str, object]:
    return {
        "galaxy": GALAXY,
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


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    manifest = pd.read_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_manifest.csv").iloc[0]
    summary_in = pd.read_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_summary.csv").iloc[0]
    if bool(manifest["construction_used_vobs_or_residual"]):
        raise RuntimeError("Envelope formula freeze is not residual-blind")
    if not bool(summary_in["control_replay_scores_allowed"]):
        raise RuntimeError("Envelope replay is not allowed by the freeze gate")

    points = pd.read_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_grid.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    obs = points["vobs_kms"].to_numpy(dtype=float)
    err = points["errv_kms"].to_numpy(dtype=float)
    carrier = points["v_baryon_050_kms"].to_numpy(dtype=float)
    env_pos = points["v_envelope_positive_prefrozen_kms"].to_numpy(dtype=float)
    env_neg = points["v_envelope_negative_control_kms"].to_numpy(dtype=float)

    old = pd.read_csv(DATA / "ugc12506_prefrozen_branch_replay_control_points.csv")
    old = old.loc[old["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    old_combined = old["v_combined_positive_replay_kms"].to_numpy(dtype=float)

    scores = pd.DataFrame(
        [
            score_row("BARYONIC_CARRIER_V050", "carrier_reference", obs, carrier, err),
            score_row(
                "UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN",
                "source_envelope_positive_replay",
                obs,
                env_pos,
                err,
            ),
            score_row(
                "UGC12506_SOURCE_ENVELOPE_SUPPORT_NEGATIVE_CONTROL",
                "negative_sign_control",
                obs,
                env_neg,
                err,
            ),
            score_row(
                "UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE",
                "old_prefrozen_reference",
                obs,
                old_combined,
                err,
            ),
        ]
    )

    prior = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    prior = prior.loc[prior["galaxy"].eq(GALAXY)].copy()
    for _, row in prior.iterrows():
        scores.loc[len(scores)] = {
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
    scores = scores.sort_values("rmse_km_s").reset_index(drop=True)

    env_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN"),
            "rmse_km_s",
        ].iloc[0]
    )
    carrier_rmse = float(scores.loc[scores["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0])
    old_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE"),
            "rmse_km_s",
        ].iloc[0]
    )
    best_prior = prior.sort_values("rmse_kms").iloc[0]

    outer = points["radius_kpc"].to_numpy(dtype=float) >= np.quantile(points["radius_kpc"], 0.70)
    outer_gap = float(np.mean(obs[outer] - carrier[outer]))
    outer_env_lift = float(np.mean(env_pos[outer] - carrier[outer]))
    outer_old_lift = float(np.mean(old_combined[outer] - carrier[outer]))

    result_status = (
        "SOURCE_ENVELOPE_REPLAY_IMPROVES_OLD_PREFROZEN_BUT_NOT_PRIOR_DIAGNOSTICS"
        if env_rmse < old_rmse and env_rmse > float(best_prior["rmse_kms"])
        else "SOURCE_ENVELOPE_REPLAY_STATUS_REVIEW_REQUIRED"
    )
    summary = pd.DataFrame(
        [
            {
                "replay_status": result_status,
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "carrier_rmse_km_s": carrier_rmse,
                "old_prefrozen_combined_rmse_km_s": old_rmse,
                "source_envelope_rmse_km_s": env_rmse,
                "source_envelope_minus_old_prefrozen_rmse_km_s": env_rmse - old_rmse,
                "source_envelope_minus_carrier_rmse_km_s": env_rmse - carrier_rmse,
                "prior_best_diagnostic_model": str(best_prior["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(best_prior["rmse_kms"]),
                "source_envelope_minus_prior_best_diagnostic_rmse_km_s": env_rmse
                - float(best_prior["rmse_kms"]),
                "outer_mean_observed_minus_baryonic_km_s_last30pct": outer_gap,
                "outer_mean_old_prefrozen_lift_km_s_last30pct": outer_old_lift,
                "outer_mean_source_envelope_lift_km_s_last30pct": outer_env_lift,
                "source_envelope_lift_fraction_of_outer_gap": outer_env_lift / outer_gap,
                "formula_frozen_before_scoring": True,
                "construction_used_vobs": False,
                "scoring_used_vobs": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    diagnostics = pd.DataFrame(
        [
            {
                "diagnostic_id": "D1_STRENGTHENING",
                "status": "ENVELOPE_SUPPORT_STRONGER_THAN_OLD_PREFROZEN"
                if env_rmse < old_rmse
                else "ENVELOPE_SUPPORT_NOT_STRONGER_THAN_OLD_PREFROZEN",
                "value": env_rmse - old_rmse,
                "claim_type": "replay_numerical_evidence_not_validation",
            },
            {
                "diagnostic_id": "D2_BASELINE_COMPETITION",
                "status": "DOES_NOT_BEAT_PRIOR_BEST_DIAGNOSTIC"
                if env_rmse > float(best_prior["rmse_kms"])
                else "BEATS_PRIOR_BEST_DIAGNOSTIC",
                "value": env_rmse - float(best_prior["rmse_kms"]),
                "claim_type": "diagnostic_reference_comparison",
            },
            {
                "diagnostic_id": "D3_OUTER_GAP_COVERAGE",
                "status": "OUTER_GAP_PARTIALLY_COVERED"
                if outer_env_lift / outer_gap > 0.25
                else "OUTER_GAP_STILL_WEAKLY_COVERED",
                "value": outer_env_lift / outer_gap,
                "claim_type": "radial_zone_diagnostic",
            },
        ]
    )

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.errorbar(points["radius_kpc"], obs, yerr=err, fmt="o", ms=4, lw=0.8, color="black", label="observed")
    ax.plot(points["radius_kpc"], carrier, color="#777777", lw=2.0, label="baryonic carrier")
    ax.plot(points["radius_kpc"], old_combined, color="#d95f02", lw=2.0, label="old prefrozen combined")
    ax.plot(points["radius_kpc"], env_pos, color="#1b9e77", lw=2.4, label="source-envelope support")
    ax.set_title("UGC12506 source-envelope support replay")
    ax.set_xlabel("Radius [kpc]")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_source_envelope_support_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    points.to_csv(DATA / "ugc12506_source_envelope_support_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_source_envelope_support_replay_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_envelope_support_replay_summary.csv", index=False)
    diagnostics.to_csv(DATA / "ugc12506_source_envelope_support_replay_diagnostics.csv", index=False)

    report = [
        "# UGC12506 Source-Envelope Support Replay",
        "",
        "This replay scores the residual-blind source-envelope support freeze.",
        "It is not accepted endpoint validation.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scores",
        "",
        markdown_table(scores),
        "",
        "## Diagnostics",
        "",
        markdown_table(diagnostics),
        "",
        f"![UGC12506 source-envelope replay]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_source_envelope_support_replay_controls.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
