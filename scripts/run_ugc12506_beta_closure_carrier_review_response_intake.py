#!/usr/bin/env python3
"""Validate an independent UGC12506 beta-closure carrier review response."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_carrier_review_response_intake_not_endpoint"
RESPONSE_PATH = DATA / "ugc12506_beta_closure_carrier_review_response.csv"
TEMPLATE_PATH = DATA / "ugc12506_beta_closure_carrier_review_response_template.csv"

ACCEPT_CARRIER_DECISIONS = {
    "ACCEPT_CARRIER_ROUTE",
    "ACCEPT_BARYONIC_STRESS_CARRIER",
}
SUPPORTED_CARRIERS = {"BARYONIC_050_FAST_PACKET"}
ACCEPT_LI2020_POLICIES = {
    "KEEP_LI2020_CONTROL_ONLY",
    "SUPPLY_ENDPOINT_LEAKAGE_POLICY",
}
FALSE_VALUES = {"", "none", "false", "no", "n", "0"}


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


def norm(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def upper(value: object) -> str:
    return norm(value).upper()


def false_clean(value: object) -> bool:
    return norm(value).lower() in FALSE_VALUES


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    response_received = RESPONSE_PATH.exists()
    response_source = RESPONSE_PATH if response_received else TEMPLATE_PATH
    response = pd.read_csv(response_source).iloc[0]

    if not response_received:
        checks = pd.DataFrame(
            [
                {
                    "check_id": "BCR_INTAKE_1_RESPONSE_PRESENT",
                    "result": "BLOCKED_PENDING_RESPONSE",
                    "reason": "No completed independent carrier review response CSV is present.",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
        carrier_prefreeze_allowed = False
        status = "U12506_BETA_CARRIER_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED"
    else:
        carrier_decision = upper(response["carrier_route_decision"])
        selected_carrier = upper(response["selected_carrier_id"])
        li2020_policy = upper(response["li2020_policy_decision"])
        checks = pd.DataFrame(
            [
                {
                    "check_id": "BCR_INTAKE_1_CARRIER_DECISION",
                    "result": "PASS"
                    if carrier_decision in ACCEPT_CARRIER_DECISIONS
                    else "FAIL",
                    "reason": f"carrier_route_decision={carrier_decision}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BCR_INTAKE_2_SUPPORTED_CARRIER",
                    "result": "PASS" if selected_carrier in SUPPORTED_CARRIERS else "FAIL",
                    "reason": f"selected_carrier_id={selected_carrier}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BCR_INTAKE_3_LI2020_POLICY",
                    "result": "PASS" if li2020_policy in ACCEPT_LI2020_POLICIES else "FAIL",
                    "reason": f"li2020_policy_decision={li2020_policy}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BCR_INTAKE_4_FORBIDDEN_INPUTS",
                    "result": "PASS" if false_clean(response["forbidden_inputs_used"]) else "FAIL",
                    "reason": f"forbidden_inputs_used={norm(response['forbidden_inputs_used'])}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BCR_INTAKE_5_NO_ENDPOINT_FLAGS",
                    "result": "PASS"
                    if false_clean(response["endpoint_scores_allowed"])
                    and false_clean(response["uses_vobs_or_residual"])
                    else "FAIL",
                    "reason": (
                        f"endpoint_scores_allowed={norm(response['endpoint_scores_allowed'])}; "
                        f"uses_vobs_or_residual={norm(response['uses_vobs_or_residual'])}"
                    ),
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ]
        )
        carrier_prefreeze_allowed = checks["result"].eq("PASS").all()
        status = (
            "U12506_BETA_CARRIER_REVIEW_ACCEPTED_PREFREEZE_ALLOWED"
            if carrier_prefreeze_allowed
            else "U12506_BETA_CARRIER_REVIEW_REJECTED_OR_INCOMPLETE_ENDPOINT_BLOCKED"
        )

    summary = pd.DataFrame(
        [
            {
                "carrier_review_intake_status": status,
                "response_received": response_received,
                "response_source": str(response_source.relative_to(ROOT)),
                "selected_carrier_id": (
                    norm(response.get("selected_carrier_id", ""))
                    if response_received
                    else "PENDING_INDEPENDENT_REVIEW"
                ),
                "carrier_prefreeze_allowed": carrier_prefreeze_allowed,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": (
                    "build_beta_cl_transfer_carrier_prefreeze_manifest"
                    if carrier_prefreeze_allowed
                    else "obtain_independent_carrier_review_response_or_source_native_carrier"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    checks.to_csv(DATA / "ugc12506_beta_closure_carrier_review_response_intake_checks.csv", index=False)
    summary.to_csv(DATA / "ugc12506_beta_closure_carrier_review_response_intake_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Carrier Review Response Intake",
        "",
        "This intake validates a completed independent carrier review response if",
        "one is present. It does not score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Checks",
        "",
        markdown_table(checks),
        "",
        "## Claim Boundary",
        "",
        "Only a passed independent carrier response can move the carrier toward a",
        "prefreeze manifest. Endpoint scoring remains false here.",
    ]
    (REPORTS / "ugc12506_beta_closure_carrier_review_response_intake.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
