#!/usr/bin/env python3
"""Record direct lambda/spin-source acquisition for beta-closure transfer.

This source-acquisition gate checks whether the primary beta-closure transfer
targets have direct literature lambda/spin values that can replace the
predeclared source-only proxy.  It records candidate sources and definition
mismatches, but authorizes no beta replay.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_direct_lambda_spin_source_gate_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(
                lambda value: "" if pd.isna(value) else f"{value:.6g}"
            )
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns)) + " |",
    ]
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    evidence_rows = [
        {
            "galaxy": "NGC7331",
            "source_field": "disc_spin_lambda",
            "source_status": "CANDIDATE_DIRECT_DISC_LAMBDA_DEFINITION_MISMATCH",
            "source_value": 0.423,
            "source_uncertainty": "",
            "definition": (
                "disc spin parameter from lognormal self-gravitating disc model; "
                "not the same object as the beta_cl halo/envelope lambda_spin slot"
            ),
            "source_reference": (
                "Marr 2015, MNRAS 453, 2214, Table 1; NGC 7331 row"
            ),
            "source_url": "https://academic.oup.com/mnras/article/453/2/2214/1146982",
            "accepted_as_beta_cl_lambda_spin": False,
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "notes": (
                "Useful as a direct angular-momentum reference. Requires a "
                "definition-conversion review before it can replace lambda_spin_proxy."
            ),
        },
        {
            "galaxy": "NGC0891",
            "source_field": "halo_spin_lambda",
            "source_status": "BLOCKED_NO_DIRECT_SOURCE_NATIVE_VALUE_FOUND",
            "source_value": "",
            "source_uncertainty": "",
            "definition": "direct source-native halo/envelope spin value",
            "source_reference": (
                "No accepted direct NGC0891 lambda_spin value cached by this gate"
            ),
            "source_url": "",
            "accepted_as_beta_cl_lambda_spin": False,
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "notes": (
                "PV/envelope context is accepted from earlier source-freeze preflight, "
                "but the spin slot remains blocked or proxy-review dependent."
            ),
        },
        {
            "galaxy": "NGC0891",
            "source_field": "model_analogue_lambda",
            "source_status": "MODEL_ANALOGUE_CONTEXT_NOT_SOURCE_NATIVE_FREEZE",
            "source_value": 0.038,
            "source_uncertainty": "",
            "definition": (
                "Milky-Way-like simulation/model analogue spin parameter discussed "
                "for NGC891-like extraplanar H I context; not a direct observed NGC0891 value"
            ),
            "source_reference": (
                "Kaufmann/Mayer-style NGC891 analogue context as summarized in lecture/source material"
            ),
            "source_url": "https://www.mpifr-bonn.mpg.de/1180177/tue_Lucio.pdf",
            "accepted_as_beta_cl_lambda_spin": False,
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
            "notes": (
                "May inform source review, but cannot be inserted into beta_cl replay."
            ),
        },
    ]
    evidence = pd.DataFrame(evidence_rows)
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence.to_csv(
        DATA / "ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "direct_lambda_spin_gate_status": (
                    "UGC12506_BETA_CLOSURE_DIRECT_LAMBDA_SOURCE_GATE_PARTIAL_ENDPOINT_BLOCKED"
                ),
                "n_primary_targets_checked": 2,
                "n_direct_values_accepted_for_beta_cl": int(
                    evidence["accepted_as_beta_cl_lambda_spin"].sum()
                ),
                "n_candidate_definition_mismatch_values": int(
                    evidence["source_status"]
                    .eq("CANDIDATE_DIRECT_DISC_LAMBDA_DEFINITION_MISMATCH")
                    .sum()
                ),
                "n_model_analogue_context_values": int(
                    evidence["source_status"]
                    .eq("MODEL_ANALOGUE_CONTEXT_NOT_SOURCE_NATIVE_FREEZE")
                    .sum()
                ),
                "ngc7331_status": "disc_lambda_candidate_definition_conversion_required",
                "ngc0891_status": "direct_lambda_blocked_proxy_or_new_source_required",
                "endpoint_scores_allowed": False,
                "beta_cl_replay_allowed": False,
                "next_gate": (
                    "definition_conversion_review_for_ngc7331_or_direct_spin_source_for_ngc0891"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Direct Lambda/Spin Source Gate",
        "",
        "This gate records a direct-source search for the two primary",
        "beta-closure transfer targets. It does not authorize a replay.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Interpretation",
        "",
        "NGC7331 has a published disc-spin-like value in Marr (2015), but its",
        "definition is not the same as the beta_cl halo/envelope lambda_spin",
        "slot. NGC0891 remains blocked for a direct lambda_spin value; the",
        "available NGC891-like lambda context is model-analogue material only.",
        "Therefore the admissible next step is either a definition-conversion",
        "review for NGC7331, direct source-native spin acquisition for NGC0891,",
        "or independent review of the already declared source-only proxy rule.",
    ]
    (REPORTS / "ugc12506_beta_closure_direct_lambda_spin_source_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(evidence.to_string(index=False))


if __name__ == "__main__":
    main()
