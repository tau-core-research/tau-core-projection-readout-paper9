#!/usr/bin/env python3
"""Diagnose the weak UGC12506 prefrozen branch replay.

This diagnostic may read vobs.  It is explicitly not a formula-freeze step and
must not be used to retune the accepted kernel without new residual-blind source
evidence.
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
CLAIM_BOUNDARY = "ugc12506_prefrozen_replay_failure_modes_diagnostic_only"


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


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(DATA / "ugc12506_prefrozen_branch_replay_control_points.csv")
    scores = pd.read_csv(DATA / "ugc12506_prefrozen_branch_replay_control_scores.csv")
    summary = pd.read_csv(DATA / "ugc12506_prefrozen_branch_replay_control_summary.csv").iloc[0]

    r = points["radius_kpc"].to_numpy(dtype=float)
    obs = points["vobs_kms"].to_numpy(dtype=float)
    err = points["errv_kms"].to_numpy(dtype=float)
    carrier = points["v_baryon_050_kms"].to_numpy(dtype=float)
    v2_carrier = np.square(carrier)
    v2_obs = np.square(obs)
    delta_v2_required = v2_obs - v2_carrier
    delta_v2_prefrozen = (
        np.square(points["v_combined_positive_replay_kms"].to_numpy(dtype=float)) - v2_carrier
    )

    active = delta_v2_prefrozen > 0
    scale = float(
        np.dot(delta_v2_prefrozen[active], delta_v2_required[active])
        / np.dot(delta_v2_prefrozen[active], delta_v2_prefrozen[active])
    )
    scale_nonnegative = max(scale, 0.0)
    v_scaled = np.sqrt(np.maximum(v2_carrier + scale_nonnegative * delta_v2_prefrozen, 0.0))

    corr = float(np.corrcoef(delta_v2_required[active], delta_v2_prefrozen[active])[0, 1])
    outer = r >= np.quantile(r, 0.70)
    outer_gap = float(np.mean(obs[outer] - carrier[outer]))
    outer_lift = float(
        np.mean(points.loc[outer, "v_combined_positive_replay_kms"].to_numpy(dtype=float) - carrier[outer])
    )
    outer_required_v2 = float(np.mean(delta_v2_required[outer]))
    outer_prefrozen_v2 = float(np.mean(delta_v2_prefrozen[outer]))

    best_prior = scores.loc[
        scores["model_role"].eq("prior_diagnostic_reference_not_same_carrier")
    ].sort_values("rmse_km_s").iloc[0]
    best_prefrozen = scores.loc[
        scores["model_role"].isin(
            [
                "combined_positive_branch",
                "source_prefrozen_positive_branch",
                "negative_sign_control",
                "combined_negative_control",
                "split_sign_control",
            ]
        )
    ].sort_values("rmse_km_s").iloc[0]

    diagnostics = pd.DataFrame(
        [
            {
                "diagnostic": "direction",
                "status": "CORRECT_SIGN_WEAK_MAGNITUDE"
                if str(best_prefrozen["model_role"]) == "combined_positive_branch"
                else "SIGN_OR_BRANCH_NOT_CONFIRMED",
                "value": str(best_prefrozen["model_id"]),
                "claim_type": "diagnostic_only",
            },
            {
                "diagnostic": "shape_correlation_v2",
                "status": "KERNEL_SHAPE_HAS_POSITIVE_ALIGNMENT" if corr > 0 else "KERNEL_SHAPE_MISALIGNED",
                "value": corr,
                "claim_type": "diagnostic_only",
            },
            {
                "diagnostic": "required_multiplier_on_prefrozen_delta_v2",
                "status": "PREFROZEN_AMPLITUDE_UNDERPOWERED" if scale_nonnegative > 3 else "PREFROZEN_AMPLITUDE_CLOSE",
                "value": scale_nonnegative,
                "claim_type": "diagnostic_only",
            },
            {
                "diagnostic": "outer_lift_fraction",
                "status": "OUTER_LIFT_TOO_SMALL" if abs(outer_lift / outer_gap) < 0.25 else "OUTER_LIFT_VISIBLE",
                "value": outer_lift / outer_gap,
                "claim_type": "diagnostic_only",
            },
            {
                "diagnostic": "prior_best_gap",
                "status": "PREFROZEN_REPLAY_NOT_BASELINE_COMPETITIVE",
                "value": float(best_prefrozen["rmse_km_s"]) - float(best_prior["rmse_km_s"]),
                "claim_type": "diagnostic_only",
            },
        ]
    )

    scaled_row = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "model_id": "DIAGNOSTIC_ONLY_SCALED_PREFROZEN_SHAPE",
                "rmse_km_s": rmse(obs, v_scaled),
                "scale_multiplier": scale_nonnegative,
                "uses_vobs_for_scale": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
                "interpretation": (
                    "If this is much better than the frozen replay, the kernel shape has information "
                    "but the source-normalized amplitude rule is too weak. This is not an endpoint result."
                ),
            }
        ]
    )

    zone_summary = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "outer_radius_threshold_kpc": float(np.min(r[outer])),
                "outer_mean_observed_minus_baryonic_km_s": outer_gap,
                "outer_mean_prefrozen_lift_km_s": outer_lift,
                "outer_mean_required_delta_v2_km2_s2": outer_required_v2,
                "outer_mean_prefrozen_delta_v2_km2_s2": outer_prefrozen_v2,
                "outer_delta_v2_fraction": outer_prefrozen_v2 / outer_required_v2,
                "best_prefrozen_rmse_km_s": float(best_prefrozen["rmse_km_s"]),
                "best_prior_diagnostic_model": str(best_prior["model_id"]),
                "best_prior_diagnostic_rmse_km_s": float(best_prior["rmse_km_s"]),
                "diagnostic_scaled_shape_rmse_km_s": float(scaled_row["rmse_km_s"].iloc[0]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    ax.errorbar(r, obs, yerr=err, fmt="o", color="black", ms=4, lw=0.8, label="observed")
    ax.plot(r, carrier, color="#777777", lw=2.0, label="baryonic carrier")
    ax.plot(
        r,
        points["v_combined_positive_replay_kms"],
        color="#d95f02",
        lw=2.2,
        label="prefrozen combined positive",
    )
    ax.plot(
        r,
        v_scaled,
        color="#1b9e77",
        lw=2.0,
        ls="--",
        label="diagnostic scaled shape",
    )
    ax.set_title("UGC12506 prefrozen branch replay diagnostic")
    ax.set_xlabel("Radius [kpc]")
    ax.set_ylabel("Rotation speed [km/s]")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    figure_path = FIGURES / "ugc12506_prefrozen_branch_replay_failure_modes.png"
    fig.savefig(figure_path, dpi=180)
    plt.close(fig)

    diagnostics.to_csv(DATA / "ugc12506_prefrozen_replay_failure_mode_diagnostics.csv", index=False)
    scaled_row.to_csv(DATA / "ugc12506_prefrozen_replay_failure_mode_scaled_shape.csv", index=False)
    zone_summary.to_csv(DATA / "ugc12506_prefrozen_replay_failure_mode_zone_summary.csv", index=False)

    report = [
        "# UGC12506 Prefrozen Replay Failure-Mode Audit",
        "",
        "This diagnostic reads `vobs` and therefore cannot freeze a new formula.",
        "It is used only to decide what residual-blind source evidence would be",
        "needed before a new endpoint attempt.",
        "",
        "## Zone Summary",
        "",
        markdown_table(zone_summary),
        "",
        "## Diagnostics",
        "",
        markdown_table(diagnostics),
        "",
        "## Diagnostic Scaled Shape",
        "",
        markdown_table(scaled_row),
        "",
        "## Interpretation",
        "",
        "The positive prefrozen branch has the expected direction but the",
        "source-normalized amplitude is too small for the observed outer gap.",
        "The scaled-shape row is not an endpoint result; it only shows whether",
        "the current kernel shape could become competitive if a stronger",
        "residual-blind amplitude theorem or source-native normalization were",
        "derived.",
        "",
        f"![UGC12506 diagnostic]({figure_path})",
        "",
    ]
    (REPORTS / "ugc12506_prefrozen_replay_failure_modes.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(zone_summary.to_string(index=False))
    print(diagnostics.to_string(index=False))
    print(scaled_row.to_string(index=False))


if __name__ == "__main__":
    main()
