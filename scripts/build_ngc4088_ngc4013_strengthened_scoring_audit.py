#!/usr/bin/env python3
"""Summarize scoring consequences of the strengthened NGC4088/NGC4013 review.

The source review itself is residual-blind.  This script reads already-frozen
endpoint/control score artifacts and records what the strengthened morphology
review does, and does not, license numerically.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_ngc4013_strengthened_scoring_audit"


def read_first(name: str) -> dict[str, Any]:
    path = DATA / name
    if not path.exists():
        raise FileNotFoundError(path)
    frame = pd.read_csv(path)
    if frame.empty:
        raise ValueError(f"{path} is empty")
    return frame.iloc[0].to_dict()


def f(row: dict[str, Any], key: str) -> float:
    value = float(row[key])
    if pd.isna(value):
        raise ValueError(f"{key} is NaN")
    return value


def b(row: dict[str, Any], key: str) -> bool:
    return str(row.get(key, "")).strip().lower() in {"true", "1", "yes", "pass"}


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
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    n4013_wvo = read_first("ngc4013_warp_vertical_overlay_endpoint_scores.csv")
    n4013_mixed = read_first("ngc4013_expdisk_wvo_frozen_protocol_scores.csv")
    n4088_endpoint = read_first("ngc4088_warp_history_accepted_endpoint_summary.csv")
    n4088_ablation = read_first("ngc4088_time_projection_ablation_control_summary.csv")

    rows = [
        {
            "galaxy": "NGC4013",
            "route": "original_compact_proxy",
            "rmse_km_s": f(n4013_wvo, "rmse_original_compact_family"),
            "reference_rmse_km_s": "",
            "delta_vs_reference_km_s": "",
            "reference": "starting compact proxy",
            "score_role": "baseline_for_morphology_refinement",
            "endpoint_scores_allowed": False,
            "endpoint_validation_claim": False,
            "interpretation": "Original simple morphology proxy; retained as source-rejected starting point.",
        },
        {
            "galaxy": "NGC4013",
            "route": "warp_vertical_overlay",
            "rmse_km_s": f(n4013_wvo, "rmse_warp_vertical_overlay"),
            "reference_rmse_km_s": f(n4013_wvo, "rmse_original_compact_family"),
            "delta_vs_reference_km_s": f(n4013_wvo, "wvo_minus_original_compact"),
            "reference": "original compact proxy",
            "score_role": "caveated_preliminary_endpoint_control",
            "endpoint_scores_allowed": b(n4013_wvo, "endpoint_scores_allowed"),
            "endpoint_validation_claim": False,
            "interpretation": (
                "Source-supported WVO refinement improves strongly over compact proxy "
                "and also beats the local TPG/v6 and MOND comparators in this artifact."
            ),
        },
        {
            "galaxy": "NGC4013",
            "route": "exponential_disk_plus_wvo_frozen_protocol",
            "rmse_km_s": f(n4013_mixed, "rmse_expdisk_wvo_frozen_protocol"),
            "reference_rmse_km_s": f(n4013_mixed, "rmse_warp_vertical_overlay"),
            "delta_vs_reference_km_s": f(n4013_mixed, "frozen_minus_wvo"),
            "reference": "WVO endpoint route",
            "score_role": "prospective_protocol_score_not_retroactive_endpoint",
            "endpoint_scores_allowed": False,
            "endpoint_validation_claim": False,
            "interpretation": (
                "Strongest NGC4013 score in this packet, but it is a prospective "
                "source-frozen protocol reference, not retroactive validation."
            ),
        },
        {
            "galaxy": "NGC4088",
            "route": "accepted_warp_history",
            "rmse_km_s": f(n4088_endpoint, "rmse_warp_history_accepted"),
            "reference_rmse_km_s": f(n4088_endpoint, "best_baseline_rmse_km_s"),
            "delta_vs_reference_km_s": f(n4088_endpoint, "matched_minus_best_baseline_rmse_km_s"),
            "reference": str(n4088_endpoint["best_baseline_model"]),
            "score_role": "caveated_accepted_endpoint_preliminary_control",
            "endpoint_scores_allowed": b(n4088_endpoint, "endpoint_scores_allowed"),
            "endpoint_validation_claim": False,
            "interpretation": (
                "Accepted warp/history route remains strong and beats all local baselines "
                "and wrong-family controls; this is still a single-galaxy caveated control result."
            ),
        },
        {
            "galaxy": "NGC4088",
            "route": "additive_warp_history_control",
            "rmse_km_s": f(n4088_ablation, "additive_rmse_km_s"),
            "reference_rmse_km_s": f(n4088_ablation, "base_rmse_km_s"),
            "delta_vs_reference_km_s": f(n4088_ablation, "additive_rmse_km_s") - f(n4088_ablation, "base_rmse_km_s"),
            "reference": "base projection",
            "score_role": "control_replay_not_new_endpoint",
            "endpoint_scores_allowed": False,
            "endpoint_validation_claim": False,
            "interpretation": (
                "Improves over the base projection, but the strengthened review did not "
                "supply new endpoint-grade numeric x_warp/q_warp fields."
            ),
        },
        {
            "galaxy": "NGC4088",
            "route": "clock_only_control",
            "rmse_km_s": f(n4088_ablation, "clock_only_rmse_km_s"),
            "reference_rmse_km_s": f(n4088_ablation, "base_rmse_km_s"),
            "delta_vs_reference_km_s": f(n4088_ablation, "clock_only_rmse_km_s") - f(n4088_ablation, "base_rmse_km_s"),
            "reference": "base projection",
            "score_role": "diagnostic_control_not_endpoint",
            "endpoint_scores_allowed": False,
            "endpoint_validation_claim": False,
            "interpretation": (
                "Clock-only replay improves modestly, but remains diagnostic because "
                "independent non-overlap clock evidence is not frozen."
            ),
        },
        {
            "galaxy": "NGC4088",
            "route": "additive_plus_clock_stress",
            "rmse_km_s": f(n4088_ablation, "additive_plus_clock_rmse_km_s"),
            "reference_rmse_km_s": f(n4088_ablation, "base_rmse_km_s"),
            "delta_vs_reference_km_s": f(n4088_ablation, "additive_plus_clock_rmse_km_s") - f(n4088_ablation, "base_rmse_km_s"),
            "reference": "base projection",
            "score_role": "stress_control_double_count_blocked",
            "endpoint_scores_allowed": False,
            "endpoint_validation_claim": False,
            "interpretation": (
                "Best numerical stress score, but explicitly blocked from endpoint "
                "interpretation because additive and clock channels overlap."
            ),
        },
    ]
    scores = pd.DataFrame(rows)
    scores["construction_used_vobs"] = False
    scores["scoring_used_vobs"] = True
    scores["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "score_verdict": "SOURCE_REFINEMENT_IMPROVES_BUT_STRONGEST_ROUTE_PROSPECTIVE",
                "headline": (
                    "Compact proxy 16.99 -> WVO 11.45 -> expdisk+WVO 10.61 km/s."
                ),
                "endpoint_reading": (
                    "WVO is caveated preliminary; expdisk+WVO is prospective protocol, "
                    "not retroactive endpoint validation."
                ),
                "source_review_effect": (
                    "Strengthened numeric lag/warp/vertical-component source evidence "
                    "supports the mixed-overlay direction."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "score_verdict": "BASE_ENDPOINT_STRONG_CONTROLS_IMPROVE_BUT_NUMERIC_KERNEL_STILL_BLOCKED",
                "headline": (
                    "Accepted warp/history 11.62 km/s beats best baseline 25.40 km/s; "
                    "controls can reach 9.39/10.50/8.38 km/s."
                ),
                "endpoint_reading": (
                    "Accepted warp/history remains endpoint-readable as a caveated "
                    "single-galaxy control; additive/clock refinements are controls."
                ),
                "source_review_effect": (
                    "Strengthened qualitative H I/PV evidence supports the broad class, "
                    "but not new endpoint-grade numeric x_warp/q_warp fields."
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "gate": "WVO_SOURCE_REFINEMENT_SCORE",
                "status": "PASS_CAVEATED_SCORE",
                "evidence": "WVO improves over source-rejected compact proxy by 5.54 km/s RMSE.",
                "endpoint_scores_allowed": True,
            },
            {
                "galaxy": "NGC4013",
                "gate": "EXPDISK_WVO_STRONGEST_SCORE",
                "status": "PROSPECTIVE_ONLY",
                "evidence": "10.61 km/s RMSE is best in this packet, but retrospective endpoint scores remain disallowed.",
                "endpoint_scores_allowed": False,
            },
            {
                "galaxy": "NGC4088",
                "gate": "BROAD_CLASS_ACCEPTED_ENDPOINT",
                "status": "PASS_CAVEATED_SCORE",
                "evidence": "Accepted route beats all baselines and all wrong-family controls.",
                "endpoint_scores_allowed": True,
            },
            {
                "galaxy": "NGC4088",
                "gate": "NUMERIC_KERNEL_PROMOTION",
                "status": "BLOCKED",
                "evidence": "New source review is qualitative; x_warp/q_warp/memory/epsilon_cross are not newly accepted numeric fields.",
                "endpoint_scores_allowed": False,
            },
            {
                "galaxy": "NGC4088",
                "gate": "ADDITIVE_PLUS_CLOCK_STRESS",
                "status": "CONTROL_ONLY_DOUBLE_COUNT_BLOCKED",
                "evidence": "RMSE improves to 8.38 km/s, but source-channel overlap blocks endpoint interpretation.",
                "endpoint_scores_allowed": False,
            },
        ]
    )
    gates["claim_boundary"] = CLAIM_BOUNDARY

    scores.to_csv(DATA / "ngc4088_ngc4013_strengthened_scoring_audit_scores.csv", index=False)
    summary.to_csv(DATA / "ngc4088_ngc4013_strengthened_scoring_audit_summary.csv", index=False)
    gates.to_csv(DATA / "ngc4088_ngc4013_strengthened_scoring_audit_gates.csv", index=False)

    report = "\n\n".join(
        [
            "# NGC4088/NGC4013 Strengthened Scoring Audit",
            (
                "This audit records the numerical consequence of the strengthened "
                "source review.  It does not use scores to choose morphology labels. "
                "It only summarizes frozen endpoint/control score artifacts after "
                "the source-side review has been recorded."
            ),
            "## Summary",
            markdown_table(summary),
            "## Scores",
            markdown_table(scores),
            "## Gates",
            markdown_table(gates),
            "## Interpretation",
            (
                "NGC4013 shows a clear source-refinement ladder: the source-supported "
                "warp/vertical-overlay route improves over the compact proxy, and the "
                "exponential-disk plus WVO frozen protocol improves further.  The latter "
                "is still prospective/protocol-only, not retroactive validation."
            ),
            (
                "NGC4088 remains strong on the accepted warp/history endpoint route. "
                "The source-strengthening packet supports the broad class but does not "
                "yet promote new numeric kernel fields, so the additive and clock "
                "improvements remain controls or stress tests."
            ),
        ]
    )
    (REPORTS / "ngc4088_ngc4013_strengthened_scoring_audit.md").write_text(report + "\n")

    print("NGC4088_NGC4013_STRENGTHENED_SCORING_AUDIT_COMPLETE")
    print(summary[["galaxy", "score_verdict"]].to_string(index=False))


if __name__ == "__main__":
    main()
