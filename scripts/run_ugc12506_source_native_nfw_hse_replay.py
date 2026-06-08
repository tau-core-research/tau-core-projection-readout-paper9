#!/usr/bin/env python3
"""Score the UGC12506 source-native NFW/high-spin-envelope replay shell."""

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
CLAIM_BOUNDARY = "ugc12506_source_native_nfw_hse_replay_not_validation"


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


def load_series(path: str, value_column: str) -> np.ndarray:
    df = pd.read_csv(DATA / path)
    df = df.loc[df["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    return df[value_column].to_numpy(dtype=float)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_summary.csv").iloc[0]
    if bool(freeze["construction_used_vobs_or_residual"]):
        raise RuntimeError("Source-native NFW-HSE shell is not residual-blind")
    if not bool(freeze["control_replay_scores_allowed"]):
        raise RuntimeError("Source-native NFW-HSE replay is not score-allowed")

    points = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    obs = points["vobs_kms"].to_numpy(dtype=float)
    err = points["errv_kms"].to_numpy(dtype=float)
    carrier = points["v_baryon_050_kms"].to_numpy(dtype=float)
    snfw_hse = points["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    snfw_hse_neg = points["v_source_native_nfw_hse_negative_kms"].to_numpy(dtype=float)

    old_nfw_hse = load_series(
        "ugc12506_nfw_like_rapid_rise_highspin_envelope_replay_points.csv",
        "v_nfw_hse_positive_prefrozen_kms",
    )
    eea = load_series(
        "ugc12506_edgeon_envelope_asymmetry_replay_points.csv",
        "v_eea_positive_prefrozen_kms",
    )
    env = load_series(
        "ugc12506_source_envelope_support_replay_points.csv",
        "v_envelope_positive_prefrozen_kms",
    )

    scores = pd.DataFrame(
        [
            score_row("BARYONIC_CARRIER_V050", "carrier_reference", obs, carrier, err),
            score_row(
                "UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE",
                "source_native_nfw_highspin_envelope_positive_replay",
                obs,
                snfw_hse,
                err,
            ),
            score_row(
                "UGC12506_SOURCE_NATIVE_NFW_HSE_NEGATIVE",
                "negative_sign_control",
                obs,
                snfw_hse_neg,
                err,
            ),
            score_row(
                "UGC12506_OLD_RD_PROXY_NFW_HSE_POSITIVE",
                "old_rd_proxy_nfw_hse_reference",
                obs,
                old_nfw_hse,
                err,
            ),
            score_row("UGC12506_EEA_POSITIVE_PREFROZEN", "eea_reference", obs, eea, err),
            score_row("UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN", "envelope_reference", obs, env, err),
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

    snfw_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE"), "rmse_km_s"].iloc[0])
    old_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_OLD_RD_PROXY_NFW_HSE_POSITIVE"), "rmse_km_s"].iloc[0])
    eea_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_EEA_POSITIVE_PREFROZEN"), "rmse_km_s"].iloc[0])
    env_rmse = float(
        scores.loc[
            scores["model_id"].eq("UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN"),
            "rmse_km_s",
        ].iloc[0]
    )
    carrier_rmse = float(scores.loc[scores["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0])
    best_prior = prior.sort_values("rmse_kms").iloc[0]

    r = points["radius_kpc"].to_numpy(dtype=float)
    inner = r <= np.quantile(r, 0.30)
    middle = (r > np.quantile(r, 0.30)) & (r < np.quantile(r, 0.70))
    outer = r >= np.quantile(r, 0.70)
    inner_lift = float(np.mean(snfw_hse[inner] - carrier[inner]))
    middle_lift = float(np.mean(snfw_hse[middle] - carrier[middle]))
    outer_lift = float(np.mean(snfw_hse[outer] - carrier[outer]))
    outer_gap = float(np.mean(obs[outer] - carrier[outer]))

    if snfw_rmse < old_rmse and snfw_rmse > float(best_prior["rmse_kms"]):
        status = "UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_IMPROVES_RD_PROXY_NOT_PRIOR_DIAGNOSTICS"
    elif snfw_rmse < eea_rmse and snfw_rmse > float(best_prior["rmse_kms"]):
        status = "UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_IMPROVES_SOURCE_BRANCHES_NOT_PRIOR_DIAGNOSTICS"
    elif snfw_rmse <= float(best_prior["rmse_kms"]):
        status = "UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_REACHES_PRIOR_DIAGNOSTIC_REVIEW_REQUIRED"
    else:
        status = "UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_STATUS_REVIEW_REQUIRED"

    summary = pd.DataFrame(
        [
            {
                "replay_status": status,
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "carrier_rmse_km_s": carrier_rmse,
                "source_envelope_rmse_km_s": env_rmse,
                "eea_rmse_km_s": eea_rmse,
                "old_rd_proxy_nfw_hse_rmse_km_s": old_rmse,
                "source_native_nfw_hse_rmse_km_s": snfw_rmse,
                "source_native_minus_old_rd_proxy_rmse_km_s": snfw_rmse - old_rmse,
                "source_native_minus_eea_rmse_km_s": snfw_rmse - eea_rmse,
                "source_native_minus_envelope_rmse_km_s": snfw_rmse - env_rmse,
                "source_native_minus_carrier_rmse_km_s": snfw_rmse - carrier_rmse,
                "prior_best_diagnostic_model": str(best_prior["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(best_prior["rmse_kms"]),
                "source_native_minus_prior_best_diagnostic_rmse_km_s": snfw_rmse - float(best_prior["rmse_kms"]),
                "inner_mean_lift_km_s_first30pct": inner_lift,
                "middle_mean_lift_km_s": middle_lift,
                "outer_mean_lift_km_s_last30pct": outer_lift,
                "outer_gap_coverage_fraction": outer_lift / outer_gap,
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
                "diagnostic_id": "D1_SOURCE_NATIVE_VS_RD_PROXY",
                "status": "SOURCE_NATIVE_IMPROVES_RD_PROXY" if snfw_rmse < old_rmse else "SOURCE_NATIVE_DOES_NOT_IMPROVE_RD_PROXY",
                "value": snfw_rmse - old_rmse,
                "claim_type": "source_native_replay_comparison_not_validation",
            },
            {
                "diagnostic_id": "D2_SOURCE_FROZEN_BRANCH_IMPROVEMENT",
                "status": "SOURCE_NATIVE_IMPROVES_EEA" if snfw_rmse < eea_rmse else "SOURCE_NATIVE_DOES_NOT_IMPROVE_EEA",
                "value": snfw_rmse - eea_rmse,
                "claim_type": "replay_numerical_evidence_not_validation",
            },
            {
                "diagnostic_id": "D3_PRIOR_DIAGNOSTIC_GAP",
                "status": "SOURCE_NATIVE_DOES_NOT_REACH_PRIOR_TAU_BEST_DIAGNOSTIC"
                if snfw_rmse > float(best_prior["rmse_kms"])
                else "SOURCE_NATIVE_REACHES_OR_BEATS_PRIOR_DIAGNOSTIC",
                "value": snfw_rmse - float(best_prior["rmse_kms"]),
                "claim_type": "diagnostic_reference_comparison",
            },
            {
                "diagnostic_id": "D4_OUTER_GAP_COVERAGE",
                "status": "OUTER_GAP_PARTIALLY_COVERED" if outer_lift / outer_gap > 0.25 else "OUTER_GAP_WEAKLY_COVERED",
                "value": outer_lift / outer_gap,
                "claim_type": "radial_zone_diagnostic",
            },
        ]
    )

    fig, (ax, ax2) = plt.subplots(
        2,
        1,
        figsize=(8.8, 7.4),
        sharex=True,
        gridspec_kw={"height_ratios": [2.5, 1.0]},
    )
    ax.errorbar(r, obs, yerr=err, fmt="o", ms=4, lw=0.8, color="black", label="observed")
    ax.plot(r, carrier, color="#777777", lw=2.0, label="baryonic carrier")
    ax.plot(r, env, color="#1b9e77", lw=1.6, label="source envelope")
    ax.plot(r, eea, color="#4c78a8", lw=1.6, label="edge-on/envelope/asym")
    ax.plot(r, old_nfw_hse, color="#f28e2b", lw=1.9, label="old R_d-proxy NFW-HSE")
    ax.plot(r, snfw_hse, color="#b2182b", lw=2.5, label="source-native NFW-HSE")
    ax.set_title("UGC12506 source-native NFW/high-spin envelope replay")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2)

    ax2.axhline(0.0, color="#999999", lw=1.0)
    ax2.plot(r, snfw_hse - old_nfw_hse, color="#b2182b", lw=2.0, label="source-native minus old proxy")
    ax2.plot(r, snfw_hse - carrier, color="#444444", lw=1.4, alpha=0.8, label="source-native lift over carrier")
    ax2.set_xlabel("Radius [kpc]")
    ax2.set_ylabel("Delta v [km/s]")
    ax2.grid(True, alpha=0.25)
    ax2.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_source_native_nfw_hse_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    points.to_csv(DATA / "ugc12506_source_native_nfw_hse_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_source_native_nfw_hse_replay_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_native_nfw_hse_replay_summary.csv", index=False)
    diagnostics.to_csv(DATA / "ugc12506_source_native_nfw_hse_replay_diagnostics.csv", index=False)

    report = [
        "# UGC12506 Source-Native NFW + High-Spin Envelope Replay",
        "",
        "This replay scores the source-native NFW/HSE shell frozen from published",
        "Table 5 halo parameters. It is a replay/control result, not endpoint",
        "validation.",
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
        f"![UGC12506 source-native NFW-HSE replay]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_source_native_nfw_hse_replay.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
