#!/usr/bin/env python3
"""Score the UGC12506 edge-on/envelope/asymmetry frozen replay."""

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
CLAIM_BOUNDARY = "ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation"


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
    weights = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(weights * np.square(pred - obs)) / np.sum(weights)))


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

    freeze = pd.read_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_summary.csv").iloc[0]
    manifest = pd.read_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_manifest.csv").iloc[0]
    if bool(freeze["construction_used_vobs_or_residual"]) or bool(manifest["construction_used_vobs_or_residual"]):
        raise RuntimeError("EEA formula shell is not residual-blind")
    if not bool(freeze["control_replay_scores_allowed"]):
        raise RuntimeError("EEA replay is not score-allowed")

    points = pd.read_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_grid.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    obs = points["vobs_kms"].to_numpy(dtype=float)
    err = points["errv_kms"].to_numpy(dtype=float)
    carrier = points["v_baryon_050_kms"].to_numpy(dtype=float)
    eea_pos = points["v_eea_positive_prefrozen_kms"].to_numpy(dtype=float)
    eea_neg = points["v_eea_negative_control_kms"].to_numpy(dtype=float)

    envelope = pd.read_csv(DATA / "ugc12506_source_envelope_support_replay_points.csv")
    envelope = envelope.loc[envelope["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    env_pos = envelope["v_envelope_positive_prefrozen_kms"].to_numpy(dtype=float)

    old = pd.read_csv(DATA / "ugc12506_prefrozen_branch_replay_control_points.csv")
    old = old.loc[old["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    old_pos = old["v_combined_positive_replay_kms"].to_numpy(dtype=float)

    scores = pd.DataFrame(
        [
            score_row("BARYONIC_CARRIER_V050", "carrier_reference", obs, carrier, err),
            score_row(
                "UGC12506_EEA_POSITIVE_PREFROZEN",
                "edgeon_envelope_asymmetry_positive_replay",
                obs,
                eea_pos,
                err,
            ),
            score_row(
                "UGC12506_EEA_NEGATIVE_CONTROL",
                "negative_sign_control",
                obs,
                eea_neg,
                err,
            ),
            score_row(
                "UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN",
                "source_envelope_reference",
                obs,
                env_pos,
                err,
            ),
            score_row(
                "UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE",
                "old_prefrozen_reference",
                obs,
                old_pos,
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

    eea_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_EEA_POSITIVE_PREFROZEN"), "rmse_km_s"].iloc[0])
    env_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN"),
            "rmse_km_s",
        ].iloc[0]
    )
    old_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE"),
            "rmse_km_s",
        ].iloc[0]
    )
    carrier_rmse = float(scores.loc[scores["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0])
    best_prior = prior.sort_values("rmse_kms").iloc[0]

    outer = points["radius_kpc"].to_numpy(dtype=float) >= np.quantile(points["radius_kpc"], 0.70)
    outer_gap = float(np.mean(obs[outer] - carrier[outer]))
    outer_eea_lift = float(np.mean(eea_pos[outer] - carrier[outer]))
    outer_env_lift = float(np.mean(env_pos[outer] - carrier[outer]))

    status = (
        "UGC12506_EEA_REPLAY_IMPROVES_SOURCE_FROZEN_KERNELS_NOT_PRIOR_DIAGNOSTICS"
        if eea_rmse < env_rmse and eea_rmse > float(best_prior["rmse_kms"])
        else "UGC12506_EEA_REPLAY_STATUS_REVIEW_REQUIRED"
    )
    summary = pd.DataFrame(
        [
            {
                "replay_status": status,
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "carrier_rmse_km_s": carrier_rmse,
                "old_prefrozen_combined_rmse_km_s": old_rmse,
                "source_envelope_rmse_km_s": env_rmse,
                "eea_positive_rmse_km_s": eea_rmse,
                "eea_minus_source_envelope_rmse_km_s": eea_rmse - env_rmse,
                "eea_minus_old_prefrozen_rmse_km_s": eea_rmse - old_rmse,
                "eea_minus_carrier_rmse_km_s": eea_rmse - carrier_rmse,
                "prior_best_diagnostic_model": str(best_prior["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(best_prior["rmse_kms"]),
                "eea_minus_prior_best_diagnostic_rmse_km_s": eea_rmse - float(best_prior["rmse_kms"]),
                "outer_mean_observed_minus_baryonic_km_s_last30pct": outer_gap,
                "outer_mean_source_envelope_lift_km_s_last30pct": outer_env_lift,
                "outer_mean_eea_lift_km_s_last30pct": outer_eea_lift,
                "eea_lift_fraction_of_outer_gap": outer_eea_lift / outer_gap,
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
                "diagnostic_id": "D1_SOURCE_FROZEN_IMPROVEMENT",
                "status": "EEA_IMPROVES_ENVELOPE_SUPPORT" if eea_rmse < env_rmse else "EEA_DOES_NOT_IMPROVE_ENVELOPE_SUPPORT",
                "value": eea_rmse - env_rmse,
                "claim_type": "replay_numerical_evidence_not_validation",
            },
            {
                "diagnostic_id": "D2_PRIOR_DIAGNOSTIC_GAP",
                "status": "EEA_DOES_NOT_REACH_PRIOR_TAU_BEST_DIAGNOSTIC"
                if eea_rmse > float(best_prior["rmse_kms"])
                else "EEA_REACHES_OR_BEATS_PRIOR_DIAGNOSTIC",
                "value": eea_rmse - float(best_prior["rmse_kms"]),
                "claim_type": "diagnostic_reference_comparison",
            },
            {
                "diagnostic_id": "D3_OUTER_GAP_COVERAGE",
                "status": "EEA_PARTIALLY_COVERS_OUTER_GAP"
                if outer_eea_lift / outer_gap > 0.25
                else "EEA_WEAK_OUTER_GAP_COVERAGE",
                "value": outer_eea_lift / outer_gap,
                "claim_type": "radial_zone_diagnostic",
            },
        ]
    )

    fig, ax = plt.subplots(figsize=(8.4, 5.2))
    ax.errorbar(points["radius_kpc"], obs, yerr=err, fmt="o", ms=4, lw=0.8, color="black", label="observed")
    ax.plot(points["radius_kpc"], carrier, color="#777777", lw=2.0, label="baryonic carrier")
    ax.plot(points["radius_kpc"], old_pos, color="#d95f02", lw=1.8, label="old high-spin/projection")
    ax.plot(points["radius_kpc"], env_pos, color="#1b9e77", lw=2.0, label="source envelope")
    ax.plot(points["radius_kpc"], eea_pos, color="#4c78a8", lw=2.5, label="edge-on + envelope + asymmetry")
    ax.set_title("UGC12506 edge-on/envelope/asymmetry replay")
    ax.set_xlabel("Radius [kpc]")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_edgeon_envelope_asymmetry_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    points.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_replay_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_replay_summary.csv", index=False)
    diagnostics.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_replay_diagnostics.csv", index=False)

    report = [
        "# UGC12506 Edge-on + Envelope + Asymmetry Replay",
        "",
        "This replay scores the frozen EEA formula shell. It is not accepted",
        "endpoint validation and it does not include the image-plane interloper",
        "as a gravity/path kernel.",
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
        f"![UGC12506 EEA replay]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_edgeon_envelope_asymmetry_replay_controls.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
