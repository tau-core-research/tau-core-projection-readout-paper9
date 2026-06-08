#!/usr/bin/env python3
"""Build a human/external review handoff for the UGC12506 Xi_t source route.

The handoff packages the current source-review packet into a prompt and a
fillable response CSV.  It is not a review response, not an accepted manifest,
and not an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_external_review_handoff_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    packet = pd.read_csv(DATA / "ugc12506_xi_t_source_review_packet.csv").iloc[0]
    obligations = pd.read_csv(DATA / "ugc12506_xi_t_source_review_obligations.csv")
    allowed = pd.read_csv(DATA / "ugc12506_xi_t_source_review_response_template.csv")
    forbidden = pd.read_csv(DATA / "ugc12506_xi_t_source_review_forbidden_inputs.csv")
    hashes = pd.read_csv(DATA / "ugc12506_xi_t_source_review_input_hashes.csv")
    intake = pd.read_csv(DATA / "ugc12506_xi_t_source_review_response_intake_summary.csv").iloc[0]

    response_form = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "reviewer_id": "FILL_ME",
                "review_timestamp_utc": "FILL_ME",
                "allowed_response": "PENDING_INDEPENDENT_REVIEW",
                "source_inputs_used": "PENDING",
                "forbidden_inputs_used": "none",
                "endpoint_scores_allowed_after_response": False,
                "accepted_manifest_allowed_after_response": False,
                "claims_universal_tau_constant": False,
                "highspin_clock_status_decision": "PENDING",
                "edgeon_pv_clock_slice_decision": "PENDING",
                "envelope_mapping_decision": "PENDING",
                "asymmetry_phase_decision": "PENDING",
                "path_zero_policy_decision": "PENDING",
                "cap_policy_decision": "PENDING",
                "review_notes": "FILL_ME",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    tasks = obligations[
        [
            "obligation_id",
            "obligation_status",
            "question",
            "accepted_evidence",
            "forbidden_evidence",
        ]
    ].copy()
    tasks["response_fields"] = [
        "highspin_clock_status_decision",
        "edgeon_pv_clock_slice_decision",
        "envelope_mapping_decision",
        "asymmetry_phase_decision",
        "path_zero_policy_decision",
        "cap_policy_decision",
    ]
    tasks["allowed_field_values"] = (
        "ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING"
    )
    tasks["endpoint_scores_allowed"] = False
    tasks["claim_boundary"] = CLAIM_BOUNDARY

    handoff_summary = pd.DataFrame(
        [
            {
                "handoff_status": "U12506_XI_T_EXTERNAL_REVIEW_HANDOFF_READY",
                "galaxy": GALAXY,
                "response_form_path": "data/derived/ugc12506_xi_t_source_review_response_blank.csv",
                "response_intake_script": "scripts/run_ugc12506_xi_t_source_review_response_intake.py",
                "current_intake_status": intake["review_response_intake_status"],
                "n_review_tasks": int(len(tasks)),
                "n_allowed_route_responses": int(len(allowed)),
                "n_forbidden_inputs": int(len(forbidden)),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    prompt = f"""# External Review Prompt: UGC12506 Xi_t Time-Readout Source Route

You are asked to perform a residual-blind source review of the UGC12506
time-readout candidate route.  Do not inspect or use rotation-curve residuals,
endpoint RMSE, baseline ranks, wrong-family Tau scores, or any post-hoc fit
quality.  Your task is only to decide whether the source evidence supports the
candidate source-side readout route.

## Candidate route

- Galaxy: `{GALAXY}`
- Candidate formula: `{packet['candidate_formula']}`
- Candidate kernel: `{packet['candidate_kernel']}`
- Epsilon rule: `{packet['epsilon_rule']}`
- Current epsilon_t: `{float(packet['epsilon_t']):.6g}`
- Path policy: `{packet['path_policy']}`

## What to review

1. Is the high-spin, low-density H I envelope context admissible as a
   clock/readout settling proxy?
2. Is the high-inclination PV/envelope-method context admissible as a
   time-slice/readout proxy, rather than only an ordinary projection proxy?
3. Is the radial K_t envelope ramp from disk scale / optical radius toward
   H I support radius acceptable as a source-side mapping?
4. Should the approaching/receding side asymmetry remain as a caveated
   clock-phase component, be demoted, or be excluded?
5. Is the zero path/environment term correct unless a cone/path review
   establishes a foreground/path object?
6. May `epsilon_cap=0.035` be carried only as a predeclared small-mismatch
   protocol cap, not as a universal Tau Core constant?

## Allowed route-level responses

Choose exactly one value for `allowed_response` in the response CSV:

{markdown_table(allowed)}

## Forbidden inputs

The following inputs must not be used:

{markdown_table(forbidden)}

## Required response file

Fill:

`data/derived/ugc12506_xi_t_source_review_response_blank.csv`

Then save a copy as:

`data/derived/ugc12506_xi_t_source_review_response.csv`

After that, run:

`python scripts/run_ugc12506_xi_t_source_review_response_intake.py`

The response may feed a later accepted-manifest gate.  It cannot by itself
authorize endpoint scoring or promote `epsilon_cap` to a universal constant.
"""

    response_form.to_csv(DATA / "ugc12506_xi_t_source_review_response_blank.csv", index=False)
    tasks.to_csv(DATA / "ugc12506_xi_t_external_review_handoff_tasks.csv", index=False)
    handoff_summary.to_csv(DATA / "ugc12506_xi_t_external_review_handoff_summary.csv", index=False)
    (REPORTS / "ugc12506_xi_t_external_review_prompt.md").write_text(prompt, encoding="utf-8")

    report = "\n".join(
        [
            "# UGC12506 Xi_t External Review Handoff",
            "",
            "This handoff converts the UGC12506 Xi_t source-review packet into a fillable response form and reviewer prompt. It is not an accepted manifest and not an endpoint.",
            "",
            "## Handoff Summary",
            "",
            markdown_table(handoff_summary),
            "",
            "## Review Tasks",
            "",
            markdown_table(tasks),
            "",
            "## Response Form",
            "",
            markdown_table(response_form),
            "",
            "## Allowed Route Responses",
            "",
            markdown_table(allowed),
            "",
            "## Forbidden Inputs",
            "",
            markdown_table(forbidden),
            "",
            "## Input Hashes",
            "",
            markdown_table(hashes),
            "",
            "## Claim Boundary",
            "",
            "The handoff is ready for residual-blind external review. A filled response must be passed through the response-intake validator before any accepted-manifest gate can be rerun.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_external_review_handoff.md").write_text(report, encoding="utf-8")
    print(handoff_summary.to_string(index=False))


if __name__ == "__main__":
    main()
