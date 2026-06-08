#!/usr/bin/env python3
"""Build a residual-blind worklist for strengthening NGC4088/NGC4013 labels."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_ngc4013_classification_strengthening_worklist_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]).replace("\n", " ") for c in cols) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "galaxy": "NGC4088",
            "priority": "P1",
            "target": "x_warp_onset",
            "current_status": "protocol numeric ready, independent review required",
            "strengthening_action": "source-native H I channel/PV map measurement or independent reviewer remeasure",
            "accepted_evidence": "published H I map/PV figure, WHISP/source-native product, or reviewer digitization packet",
            "forbidden_evidence": "rotation-curve residual shape or endpoint RMSE",
            "expected_effect": "promotes warp-window precision from caveated to accepted if consistent",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4088",
            "priority": "P1",
            "target": "q_warp / asymmetry amplitude",
            "current_status": "first-pass source fill, not independently accepted",
            "strengthening_action": "measure side-dependent PA/warp asymmetry from H I channel maps",
            "accepted_evidence": "north/south PA or warp-asymmetry measurements with source image provenance",
            "forbidden_evidence": "choosing amplitude because it improves the rotation curve",
            "expected_effect": "locks the warp/history kernel amplitude without curve tuning",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4088",
            "priority": "P2",
            "target": "memory/history decomposition",
            "current_status": "partly filled; companion context accepted, decomposition incomplete",
            "strengthening_action": "separate interaction context, asymmetry, and persistence/history flags",
            "accepted_evidence": "companion geometry, disturbed H I morphology, optical/kinematic distortion literature",
            "forbidden_evidence": "post-score interpretation of residual zones",
            "expected_effect": "decides whether history is a real morphology channel or only context",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4088",
            "priority": "P2",
            "target": "epsilon_cross bound",
            "current_status": "blocked until q_warp and memory/history are accepted",
            "strengthening_action": "rerun epsilon_cross bound after P1/P2 fields are frozen",
            "accepted_evidence": "derived only from accepted source fields",
            "forbidden_evidence": "numeric bound chosen to rescue endpoint score",
            "expected_effect": "turns broad warp/history label into endpoint-grade precision candidate",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4013",
            "priority": "P1",
            "target": "lag-profile digitization",
            "current_status": "accepted context, caveated kernel support",
            "strengthening_action": "digitize or source-extract lag profile from H I kinematics figure/table",
            "accepted_evidence": "radial lag measurements independent of rotation residual scoring",
            "forbidden_evidence": "using Tau-vs-observed residuals to choose lag window",
            "expected_effect": "strengthens warp/vertical-overlay kernel shape",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4013",
            "priority": "P1",
            "target": "vertical overlay normalization",
            "current_status": "h/R and extended component available",
            "strengthening_action": "cross-check S4G edge-disk h/R and Comeron extended-component fraction",
            "accepted_evidence": "independent vertical decomposition, dust lane, or thick-disk measurements",
            "forbidden_evidence": "amplitude adjustment from curve fit",
            "expected_effect": "reduces caveat on vertical-overlay amplitude",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4013",
            "priority": "P2",
            "target": "prospective replay status",
            "current_status": "protocol ready, not retroactive validation",
            "strengthening_action": "apply frozen mixed-overlay rule to uninspected analogue or future holdout",
            "accepted_evidence": "same rule, same frozen fields, no post-score relabeling",
            "forbidden_evidence": "counting existing diagnostic score as validation",
            "expected_effect": "turns NGC4013 from strong case study into reusable protocol evidence",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4013",
            "priority": "P2",
            "target": "Xi_t non-overlap",
            "current_status": "overlay worsens; double-counting control",
            "strengthening_action": "only reopen if an independent clock/readout source field is non-overlapping",
            "accepted_evidence": "source field not already used by warp/vertical-overlay morphology",
            "forbidden_evidence": "adding Xi_t because it improves or worsens a plot",
            "expected_effect": "keeps projection/time channel honest and non-universal",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]

    worklist = pd.DataFrame(rows)
    worklist.to_csv(DATA / "ngc4088_ngc4013_classification_strengthening_worklist.csv", index=False)

    summary = (
        worklist.groupby(["galaxy", "priority"], as_index=False)
        .size()
        .rename(columns={"size": "n_items"})
    )
    summary.to_csv(
        DATA / "ngc4088_ngc4013_classification_strengthening_worklist_summary.csv",
        index=False,
    )

    report = "\n".join(
        [
            "# NGC4088 / NGC4013 Classification Strengthening Worklist",
            "",
            f"Claim boundary: `{CLAIM_BOUNDARY}`",
            "",
            "This worklist records how to strengthen the two morphology labels without",
            "using rotation residuals or endpoint scores as classification evidence.",
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Worklist",
            "",
            markdown_table(worklist),
            "",
            "## Practical Verdict",
            "",
            "- NGC4088 can be strengthened most by independent H I warp-onset and",
            "  asymmetry/amplitude review.  This is the shortest route from a strong",
            "  broad label to an endpoint-grade morphology label.",
            "- NGC4013 can be strengthened most by digitizing the lag profile and",
            "  cross-checking the vertical-overlay normalization.  Its broad mixed",
            "  label is already good enough for caveated prospective protocol use.",
            "",
        ]
    )
    (REPORTS / "ngc4088_ngc4013_classification_strengthening_worklist.md").write_text(
        report, encoding="utf-8"
    )
    print("CLASSIFICATION_STRENGTHENING_WORKLIST_COMPLETE")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
