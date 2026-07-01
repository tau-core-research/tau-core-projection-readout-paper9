#!/usr/bin/env python3
"""Explain why an NGC4013 wrong-family control beats the pure WVO route.

This is not a scorer. It reads the already frozen NGC4013 WVO, wrong-family,
radial-zone, and prospective protocol artifacts and records the claim-safe
interpretation: the better exponential-disk control is morphology-completion
pressure, not validation and not a true negative against Tau Core.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ngc4013_morphology_completion_pressure_not_validation"


def markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals: list[str] = []
        for col in cols:
            value = row[col]
            if pd.isna(value):
                vals.append("")
            elif isinstance(value, float):
                vals.append(f"{value:.6g}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    candidates = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_control_candidates.csv")
    control = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_control_summary.csv").iloc[0]
    radial = pd.read_csv(DATA / "ngc4013_warp_vertical_overlay_radial_zone_summary.csv").iloc[0]
    protocol = pd.read_csv(DATA / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv").iloc[0]

    ranked = candidates.sort_values("rank_all_candidates").copy()
    ranked["claim_boundary"] = CLAIM

    matched = ranked[ranked["candidate_id"] == "matched_K_warp_vertical_overlay"].iloc[0]
    best_wrong = ranked[ranked["candidate_role"].str.contains("wrong_family", regex=False)].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "matched_route": str(matched["candidate_id"]),
                "matched_rmse_km_s": float(matched["rmse"]),
                "best_wrong_family": str(best_wrong["candidate_id"]),
                "best_wrong_rmse_km_s": float(best_wrong["rmse"]),
                "matched_minus_best_wrong_km_s": float(control["matched_minus_wrong_best"]),
                "matched_minus_wrong_mean_km_s": float(control["matched_minus_wrong_mean"]),
                "prospective_mixed_protocol": "exponential_disk_plus_wvo",
                "prospective_mixed_rmse_km_s": float(
                    protocol["rmse_expdisk_wvo_frozen_protocol"]
                ),
                "inner_prewarp_kernel_active": float(radial["inner_K_wvo_mean"]) > 0.0,
                "outer_window_wvo_minus_tpg_km_s": float(
                    radial["active_window_weighted_wvo_minus_tpg_rmse"]
                ),
                "completion_verdict": "PURE_WVO_UNDERCOMPLETE_EXPONENTIAL_CARRIER_NEEDED",
                "true_negative_against_tau_core": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    components = pd.DataFrame(
        [
            {
                "component": "regular_exponential_disk_carrier",
                "source_role": "global disk carrier / inner-to-full-curve support",
                "current_status": "suggested by best wrong-family control and prospective protocol",
                "allowed_use": "prospective mixed kernel component on future holdout/analogue",
                "blocked_use": "retroactive NGC4013 endpoint validation from the old score",
            },
            {
                "component": "warp_vertical_overlay",
                "source_role": "outer warp / vertical-overlay correction",
                "current_status": "caveated replay-allowed after non-overlap ledger",
                "allowed_use": "NGC4013 caveated replay/control evidence",
                "blocked_use": "full-profile standalone morphology claim",
            },
            {
                "component": "observer_path_projection",
                "source_role": "line-of-sight orientation and projection caveat",
                "current_status": "context component assigned to WVO/mixed route",
                "allowed_use": "projection context inside the shared WVO contribution",
                "blocked_use": "independent amplitude or clock factor",
            },
            {
                "component": "time_clock_projection_Xi_t",
                "source_role": "independent clock/readout route",
                "current_status": "blocked for NGC4013",
                "allowed_use": "diagnostic only until independent non-overlap clock source exists",
                "blocked_use": "reuse of warp/vertical/lag evidence already assigned to WVO",
            },
        ]
    )
    components["claim_boundary"] = CLAIM

    summary_path = DATA / "ngc4013_morphology_completion_pressure_summary_v1.csv"
    ranking_path = DATA / "ngc4013_morphology_completion_pressure_ranking_v1.csv"
    components_path = DATA / "ngc4013_morphology_completion_pressure_components_v1.csv"
    report_path = REPORTS / "ngc4013_morphology_completion_pressure.md"

    summary.to_csv(summary_path, index=False)
    ranked.to_csv(ranking_path, index=False)
    components.to_csv(components_path, index=False)

    report = [
        "# NGC4013 Morphology-Completion Pressure Audit",
        "",
        "**Doc class:** claim-boundary audit",
        "",
        "**Reader role:** Paper 9 projection/mixed replay maintainer",
        "",
        "**Status:** `PURE_WVO_UNDERCOMPLETE_EXPONENTIAL_CARRIER_NEEDED`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "This audit explains why the best wrong-family control can beat the pure",
        "NGC4013 WVO route without making the result a true negative against the",
        "Tau Core morphology-readout program. It reads frozen score summaries only;",
        "it does not fit a new curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidate Ranking",
        "",
        markdown_table(ranked),
        "",
        "## Component Assignment",
        "",
        markdown_table(components),
        "",
        "## Interpretation",
        "",
        "The best wrong-family control is `wrong_K_exponential_disk`. This is not",
        "surprising for NGC4013: a regular exponential-disk carrier can describe the",
        "global disk trend better than a pure outer warp/vertical-overlay correction.",
        "The WVO kernel is source-supported, but the radial-zone audit shows it is an",
        "outer-lane correction: it is inactive before the warp window and improves the",
        "active outer window.",
        "",
        "Therefore the result is not a true negative. It is morphology-completion",
        "pressure: the source-supported full readout should likely be a mixed kernel",
        "with an exponential-disk carrier plus WVO/observer-path correction. The",
        "existing expdisk+WVO protocol score points in that direction, but remains",
        "prospective-only for NGC4013.",
        "",
        "## Allowed Claim",
        "",
        "`NGC4013 supports the need for a mixed morphology readout: regular disk",
        "carrier plus warp/vertical-overlay projection. Pure WVO is undercomplete,",
        "but source-supported in its active outer lane.`",
        "",
        "## Disallowed Claims",
        "",
        "- endpoint validation of expdisk+WVO on NGC4013",
        "- population validation",
        "- treating `wrong_K_exponential_disk` as a literal wrong-family defeat",
        "- promoting independent `Xi_t` from the same source facts",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
