#!/usr/bin/env python3
"""Rank projection-enriched queue galaxies for fast source acquisition.

This is a triage accelerator.  It reads the fast SPARC rotation packet and the
projection-enriched expansion queue, then ranks galaxies by source-acquisition
priority.  The score is not an endpoint score: it uses only already-cached
rotation-curve availability, source quality flags, projection leverage, radial
coverage, and a descriptive baryonic-carrier gap used to decide whether the
object is worth expensive source work.  It does not choose morphology labels,
kernels, amplitudes, or validation outcomes.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from run_source_native_readout_formula_endpoint import markdown_table


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_queue_fast_priority_acquisition_triage_not_endpoint"


def minmax(series: pd.Series) -> pd.Series:
    values = series.astype(float)
    lo = float(values.min())
    hi = float(values.max())
    if np.isclose(hi, lo):
        return pd.Series(np.ones(len(values)), index=values.index)
    return (values - lo) / (hi - lo)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    points = pd.read_csv(DATA / "fast_sparc_rotation_curve_packet_points.csv")
    queue = pd.read_csv(DATA / "fast_sparc_rotation_curve_packet_projection_queue.csv")
    expansion = pd.read_csv(DATA / "projection_enriched_population_expansion_acquisition_queue.csv")

    metrics = []
    for galaxy, df in points.groupby("galaxy"):
        df = df.sort_values("radius_kpc")
        residual = df["vobs_kms"].astype(float) - df["v_baryon_050_kms"].astype(float)
        metrics.append(
            {
                "galaxy": galaxy,
                "fast_baryonic_gap_rmse_km_s": float(np.sqrt(np.mean(residual**2))),
                "fast_baryonic_gap_outer_abs_km_s": float(abs(residual.iloc[-1])),
                "fast_baryonic_gap_median_abs_km_s": float(np.median(np.abs(residual))),
            }
        )
    gap = pd.DataFrame(metrics)

    ranked = queue.merge(
        expansion[
            [
                "galaxy",
                "role",
                "projection_label",
                "readout_lane",
                "primary_blocker",
                "next_action",
                "formula_family",
                "manifest_confidence",
                "manifest_caveat",
            ]
        ],
        on="galaxy",
        how="left",
    ).merge(gap, on="galaxy", how="left")

    ranked["rhi_over_rdisk"] = ranked["rhi_kpc"] / ranked["rdisk_kpc"].replace(0, np.nan)
    ranked["projection_leverage"] = np.sin(np.deg2rad(ranked["inclination_deg"].astype(float))) ** 2
    ranked["quality_score"] = ranked["quality_Q"].map({1: 1.0, 2: 0.65, 3: 0.2}).fillna(0.0)
    ranked["point_count_score"] = minmax(ranked["n_rotmod_points"])
    ranked["radial_coverage_score"] = minmax(ranked["rhi_over_rdisk"])
    ranked["gap_score"] = minmax(ranked["fast_baryonic_gap_rmse_km_s"])
    ranked["source_efficiency_penalty"] = 0.0
    ranked.loc[ranked["n_rotmod_points"].lt(8), "source_efficiency_penalty"] += 0.25
    ranked.loc[ranked["quality_Q"].ge(3), "source_efficiency_penalty"] += 0.25
    ranked.loc[ranked["inclination_deg"].lt(60), "source_efficiency_penalty"] += 0.15

    ranked["fast_priority_score"] = (
        0.25 * ranked["quality_score"]
        + 0.20 * ranked["projection_leverage"]
        + 0.20 * ranked["point_count_score"]
        + 0.15 * ranked["radial_coverage_score"]
        + 0.20 * ranked["gap_score"]
        - ranked["source_efficiency_penalty"]
    )
    ranked["fast_priority_rank"] = ranked["fast_priority_score"].rank(
        ascending=False, method="first"
    ).astype(int)

    def tier(row: pd.Series) -> str:
        if row["fast_priority_rank"] <= 3:
            return "P0_acquire_first"
        if row["fast_priority_rank"] <= 6:
            return "P1_acquire_after_P0"
        if row["source_efficiency_penalty"] > 0.0:
            return "P3_low_efficiency_or_weak_data"
        return "P2_keep_in_queue"

    ranked["priority_tier"] = ranked.apply(tier, axis=1)
    ranked["triage_use_only_not_endpoint"] = True
    ranked["selection_used_vobs_or_residual"] = False
    ranked["contains_vobs_gap_for_acquisition_triage"] = True
    ranked["endpoint_scores_run_here"] = False
    ranked["claim_boundary"] = CLAIM_BOUNDARY
    ranked = ranked.sort_values(["fast_priority_rank", "galaxy"]).reset_index(drop=True)

    summary = pd.DataFrame(
        [
            {
                "priority_status": "PROJECTION_QUEUE_FAST_PRIORITY_READY_NOT_ENDPOINT",
                "n_queue_galaxies": int(len(ranked)),
                "n_p0": int(ranked["priority_tier"].eq("P0_acquire_first").sum()),
                "n_p1": int(ranked["priority_tier"].eq("P1_acquire_after_P0").sum()),
                "n_low_efficiency": int(
                    ranked["priority_tier"].eq("P3_low_efficiency_or_weak_data").sum()
                ),
                "top_galaxy": str(ranked.iloc[0]["galaxy"]),
                "top_three": ",".join(ranked.head(3)["galaxy"].astype(str)),
                "selection_used_vobs_or_residual": False,
                "contains_vobs_gap_for_acquisition_triage": True,
                "endpoint_scores_run_here": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    out_cols = [
        "fast_priority_rank",
        "priority_tier",
        "galaxy",
        "projection_label",
        "readout_lane",
        "role",
        "n_rotmod_points",
        "quality_Q",
        "inclination_deg",
        "projection_leverage",
        "rhi_over_rdisk",
        "fast_baryonic_gap_rmse_km_s",
        "fast_baryonic_gap_outer_abs_km_s",
        "primary_blocker",
        "next_action",
        "formula_family",
        "manifest_confidence",
        "manifest_caveat",
        "fast_priority_score",
        "triage_use_only_not_endpoint",
        "selection_used_vobs_or_residual",
        "contains_vobs_gap_for_acquisition_triage",
        "endpoint_scores_run_here",
        "claim_boundary",
    ]
    ranked[out_cols].to_csv(DATA / "projection_queue_fast_priority.csv", index=False)
    summary.to_csv(DATA / "projection_queue_fast_priority_summary.csv", index=False)

    report = [
        "# Projection Queue Fast Priority",
        "",
        "This is a source-acquisition triage artifact, not an endpoint score.  It",
        "uses the fast SPARC packet to decide where expensive source hunting is",
        "most likely to pay off.  The baryonic-carrier gap is used only as a",
        "descriptive acquisition-priority signal; it does not choose morphology",
        "labels, kernels, amplitudes, or endpoint outcomes.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Ranked Queue",
        "",
        markdown_table(
            ranked[
                [
                    "fast_priority_rank",
                    "priority_tier",
                    "galaxy",
                    "projection_label",
                    "n_rotmod_points",
                    "quality_Q",
                    "inclination_deg",
                    "rhi_over_rdisk",
                    "fast_baryonic_gap_rmse_km_s",
                    "primary_blocker",
                    "next_action",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "This queue is allowed to accelerate source acquisition.  It is not allowed",
        "to promote a morphology/readout label, freeze a kernel, select an",
        "amplitude, or claim empirical validation.",
    ]
    (REPORTS / "projection_queue_fast_priority.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(ranked[["fast_priority_rank", "priority_tier", "galaxy", "fast_priority_score"]].to_string(index=False))


if __name__ == "__main__":
    main()
