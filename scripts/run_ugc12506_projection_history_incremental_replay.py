#!/usr/bin/env python3
"""Score UGC12506 incremental projection-history replay."""

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
CLAIM_BOUNDARY = "ugc12506_projection_history_incremental_replay_not_validation"


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


def load_series(path: str, column: str) -> np.ndarray:
    df = pd.read_csv(DATA / path)
    df = df.loc[df["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    return df[column].to_numpy(dtype=float)


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    freeze = pd.read_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_summary.csv").iloc[0]
    if bool(freeze["construction_used_vobs_or_residual"]):
        raise RuntimeError("Projection-history shell is not residual-blind")
    if not bool(freeze["control_replay_scores_allowed"]):
        raise RuntimeError("Projection-history replay is not score-allowed")

    points = pd.read_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_grid.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    r = points["radius_kpc"].to_numpy(dtype=float)
    obs = points["vobs_kms"].to_numpy(dtype=float)
    err = points["errv_kms"].to_numpy(dtype=float)
    carrier = points["v_baryon_050_kms"].to_numpy(dtype=float)
    source_native = points["v_source_native_nfw_hse_positive_kms"].to_numpy(dtype=float)
    phi = points["v_projection_history_incremental_positive_kms"].to_numpy(dtype=float)
    phi_neg = points["v_projection_history_incremental_negative_kms"].to_numpy(dtype=float)

    old_nfw = load_series(
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
            score_row("UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE", "source_native_base_reference", obs, source_native, err),
            score_row(
                "UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE",
                "incremental_projection_history_positive_replay",
                obs,
                phi,
                err,
            ),
            score_row(
                "UGC12506_INCREMENTAL_PROJECTION_HISTORY_NEGATIVE",
                "negative_sign_control",
                obs,
                phi_neg,
                err,
            ),
            score_row("UGC12506_OLD_RD_PROXY_NFW_HSE_POSITIVE", "old_rd_proxy_reference", obs, old_nfw, err),
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

    phi_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE"), "rmse_km_s"].iloc[0])
    snfw_rmse = float(scores.loc[scores["model_id"].eq("UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE"), "rmse_km_s"].iloc[0])
    carrier_rmse = float(scores.loc[scores["model_id"].eq("BARYONIC_CARRIER_V050"), "rmse_km_s"].iloc[0])
    best_prior = prior.sort_values("rmse_kms").iloc[0]

    inner = r <= np.quantile(r, 0.30)
    middle = (r > np.quantile(r, 0.30)) & (r < np.quantile(r, 0.70))
    outer = r >= np.quantile(r, 0.70)
    phi_increment = phi - source_native
    outer_gap_after_snfw = float(np.mean(obs[outer] - source_native[outer]))
    outer_increment = float(np.mean(phi_increment[outer]))

    if phi_rmse < snfw_rmse and phi_rmse > float(best_prior["rmse_kms"]):
        status = "UGC12506_INCREMENTAL_PROJECTION_HISTORY_IMPROVES_SOURCE_NATIVE_BASE_NOT_PRIOR_DIAGNOSTICS"
    elif phi_rmse <= float(best_prior["rmse_kms"]):
        status = "UGC12506_INCREMENTAL_PROJECTION_HISTORY_REACHES_PRIOR_DIAGNOSTIC_REVIEW_REQUIRED"
    else:
        status = "UGC12506_INCREMENTAL_PROJECTION_HISTORY_DOES_NOT_IMPROVE_SOURCE_NATIVE_BASE"

    summary = pd.DataFrame(
        [
            {
                "replay_status": status,
                "galaxy": GALAXY,
                "n_points": int(len(points)),
                "carrier_rmse_km_s": carrier_rmse,
                "source_native_nfw_hse_rmse_km_s": snfw_rmse,
                "projection_history_incremental_rmse_km_s": phi_rmse,
                "projection_history_minus_source_native_rmse_km_s": phi_rmse - snfw_rmse,
                "projection_history_minus_carrier_rmse_km_s": phi_rmse - carrier_rmse,
                "prior_best_diagnostic_model": str(best_prior["model_id"]),
                "prior_best_diagnostic_rmse_km_s": float(best_prior["rmse_kms"]),
                "projection_history_minus_prior_best_diagnostic_rmse_km_s": phi_rmse - float(best_prior["rmse_kms"]),
                "inner_mean_increment_km_s_first30pct": float(np.mean(phi_increment[inner])),
                "middle_mean_increment_km_s": float(np.mean(phi_increment[middle])),
                "outer_mean_increment_km_s_last30pct": outer_increment,
                "outer_gap_after_source_native_coverage_fraction": outer_increment / outer_gap_after_snfw,
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
                "diagnostic_id": "D1_INCREMENTAL_IMPROVEMENT",
                "status": "IMPROVES_SOURCE_NATIVE_BASE" if phi_rmse < snfw_rmse else "DOES_NOT_IMPROVE_SOURCE_NATIVE_BASE",
                "value": phi_rmse - snfw_rmse,
                "claim_type": "caveated_control_replay_not_validation",
            },
            {
                "diagnostic_id": "D2_PRIOR_DIAGNOSTIC_GAP",
                "status": "GAP_REMAINS_TO_PRIOR_DIAGNOSTIC"
                if phi_rmse > float(best_prior["rmse_kms"])
                else "REACHES_OR_BEATS_PRIOR_DIAGNOSTIC",
                "value": phi_rmse - float(best_prior["rmse_kms"]),
                "claim_type": "diagnostic_reference_comparison",
            },
            {
                "diagnostic_id": "D3_OUTER_GAP_AFTER_SOURCE_NATIVE_COVERAGE",
                "status": "OUTER_GAP_PARTIALLY_COVERED"
                if outer_increment / outer_gap_after_snfw > 0.25
                else "OUTER_GAP_WEAKLY_COVERED",
                "value": outer_increment / outer_gap_after_snfw,
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
    ax.plot(r, carrier, color="#777777", lw=1.8, label="baryonic carrier")
    ax.plot(r, source_native, color="#b2182b", lw=2.0, label="source-native NFW-HSE")
    ax.plot(r, phi, color="#5e3c99", lw=2.5, label="NFW-HSE + incremental projection-history")
    ax.plot(r, old_nfw, color="#f28e2b", lw=1.4, alpha=0.8, label="old R_d-proxy NFW-HSE")
    ax.set_title("UGC12506 incremental projection-history replay")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8, ncol=2)

    ax2.axhline(0.0, color="#999999", lw=1.0)
    ax2.plot(r, phi_increment, color="#5e3c99", lw=2.0, label="PH increment over source-native base")
    ax2.plot(r, obs - source_native, color="#333333", lw=1.2, alpha=0.8, label="observed minus source-native base")
    ax2.set_xlabel("Radius [kpc]")
    ax2.set_ylabel("Delta v [km/s]")
    ax2.grid(True, alpha=0.25)
    ax2.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_projection_history_incremental_replay.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    points.to_csv(DATA / "ugc12506_projection_history_incremental_replay_points.csv", index=False)
    scores.to_csv(DATA / "ugc12506_projection_history_incremental_replay_scores.csv", index=False)
    summary.to_csv(DATA / "ugc12506_projection_history_incremental_replay_summary.csv", index=False)
    diagnostics.to_csv(DATA / "ugc12506_projection_history_incremental_replay_diagnostics.csv", index=False)

    report = [
        "# UGC12506 Incremental Projection-History Replay",
        "",
        "This replay scores the caveated incremental projection-history shell on",
        "top of the source-native NFW-HSE base. It is not endpoint validation.",
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
        f"![UGC12506 incremental projection-history replay]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_projection_history_incremental_replay.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(scores.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
