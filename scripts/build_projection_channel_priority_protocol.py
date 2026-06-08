#!/usr/bin/env python3
"""Build the source-token priority protocol for projection-channel assignment.

The protocol answers: if the same residual-blind source datum could support a
morphology/projection kernel and a time/clock projection kernel, which channel
gets to use it in an endpoint?

No rotation residuals or endpoint scores are read.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_channel_priority_protocol_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in df.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rules = pd.DataFrame(
        [
            {
                "priority": 1,
                "rule_id": "DIRECT_READOUT_FIRST",
                "condition": "source token directly describes geometry, morphology, warp, asymmetry, bar/ring, vertical overlay, or observer/path appearance",
                "endpoint_assignment": "morphology_or_observer_projection_kernel",
                "time_projection_allowed": "no, unless an independent clock/readout aspect is separately frozen",
                "reason": "the most direct readout consumes the token first",
            },
            {
                "priority": 2,
                "rule_id": "TIME_REQUIRES_CLOCK_CONTENT",
                "condition": "source token describes component settling, relaxation state, multi-waveband phase offset, lag/clock mismatch, or path-clock evidence not already used by morphology",
                "endpoint_assignment": "time_or_clock_projection_channel",
                "time_projection_allowed": "yes, if non-overlap ledger passes",
                "reason": "time projection needs clock/readout meaning beyond shape alone",
            },
            {
                "priority": 3,
                "rule_id": "ONE_TOKEN_ONE_ENDPOINT_CHANNEL",
                "condition": "same token could be read by multiple projection channels",
                "endpoint_assignment": "single predeclared channel only",
                "time_projection_allowed": "only for quotient-surviving remainder T/A",
                "reason": "prevents counting the same source evidence twice",
            },
            {
                "priority": 4,
                "rule_id": "LOWER_ONTOLOGICAL_LEVEL_WINS_TIES",
                "condition": "source token supports both ordinary morphology/projection and deeper time/clock interpretation with no independent separator",
                "endpoint_assignment": "morphology_or_projection_kernel",
                "time_projection_allowed": "control only",
                "reason": "deeper time/clock claims require stronger independent evidence",
            },
            {
                "priority": 5,
                "rule_id": "RESIDUAL_CANNOT_BREAK_TIES",
                "condition": "two channel assignments remain ambiguous",
                "endpoint_assignment": "block endpoint or keep weaker/direct channel",
                "time_projection_allowed": "diagnostic/control only",
                "reason": "rotation residuals and RMSE cannot decide the source assignment",
            },
        ]
    )
    rules["uses_vobs_or_residual"] = False
    rules["endpoint_scores_allowed"] = False
    rules["claim_boundary"] = CLAIM_BOUNDARY

    examples = pd.DataFrame(
        [
            {
                "example_token": "warp onset / x_w",
                "direct_assignment": "warp/history morphology kernel",
                "time_assignment": "blocked unless separate settling-clock evidence exists",
                "ngc4088_status": "assigned to additive warp/history; Xi_t overlap",
            },
            {
                "example_token": "q_warp / warp strength",
                "direct_assignment": "warp/history source-strength factor",
                "time_assignment": "blocked as direct source-strength overlap",
                "ngc4088_status": "assigned to additive warp/history; Xi_t overlap",
            },
            {
                "example_token": "position-angle/orientation mismatch",
                "direct_assignment": "observer/path or warp geometry projection",
                "time_assignment": "control unless source proves clock-slice mismatch",
                "ngc4088_status": "shared warp geometry; no orthogonal clock load",
            },
            {
                "example_token": "component lag or settling state independent of warp",
                "direct_assignment": "not consumed by shape alone if separately measured",
                "time_assignment": "candidate clock/readout channel",
                "ngc4088_status": "not currently available as non-overlapping source token",
            },
            {
                "example_token": "line-of-sight foreground/path environment",
                "direct_assignment": "path projection only if source-native causal-path evidence exists",
                "time_assignment": "candidate observer/path clock channel",
                "ngc4088_status": "not primary for current route",
            },
        ]
    )
    examples["uses_vobs_or_residual"] = False
    examples["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "protocol_id": "PROJECTION_CHANNEL_SOURCE_TOKEN_PRIORITY_V1",
                "main_rule": "assign each source token to the most direct predeclared readout channel; time projection receives only independent clock/readout content or quotient-surviving remainder",
                "formal_test": "time endpoint load is carried by T/A, where A is the active morphology/projection source subspace and T is the time-projection source ledger",
                "reviewer_guardrail": "endpoint RMSE cannot decide channel priority",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rules.to_csv(DATA / "projection_channel_priority_protocol_rules.csv", index=False)
    examples.to_csv(DATA / "projection_channel_priority_protocol_examples.csv", index=False)
    summary.to_csv(DATA / "projection_channel_priority_protocol_summary.csv", index=False)

    report = "\n\n".join(
        [
            "# Projection Channel Source-Token Priority Protocol",
            (
                "This protocol decides how residual-blind source tokens are assigned when "
                "the same datum could support morphology/projection and time/clock projection."
            ),
            "## Summary",
            markdown_table(summary),
            "## Rules",
            markdown_table(rules),
            "## Examples",
            markdown_table(examples),
            (
                "Operationally, the time-projection endpoint load is measured in the "
                "quotient T/A. A is the active morphology/projection source subspace; "
                "T is the candidate time-projection source ledger. If a time token is "
                "already in A, it may remain a control but not an endpoint contribution."
            ),
        ]
    )
    (REPORTS / "projection_channel_priority_protocol.md").write_text(report + "\n")
    print("PROJECTION_CHANNEL_PRIORITY_PROTOCOL_COMPLETE")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
