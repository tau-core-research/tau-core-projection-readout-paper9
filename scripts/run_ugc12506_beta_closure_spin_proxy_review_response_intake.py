#!/usr/bin/env python3
"""Validate an independent beta-closure spin-proxy review response.

This intake script is deliberately conservative.  If no completed response is
present, it records a pending status.  If a response is present, it can only
promote the source-only proxy to a caveated transfer-review input when the
review explicitly accepts source fields, accepts or caveats the weight rule,
keeps the NGC7331 disc-lambda definition boundary clean, selects at least one
target, and declares that no forbidden residual/endpoint inputs were used.

It does not run replay scores and does not create an endpoint manifest.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_spin_proxy_review_response_intake_not_endpoint"
RESPONSE_PATH = DATA / "ugc12506_beta_closure_spin_proxy_review_response.csv"
TEMPLATE_PATH = DATA / "ugc12506_beta_closure_spin_proxy_review_response_template.csv"


ACCEPT_FIELD_DECISIONS = {"ACCEPT_SOURCE_FIELDS", "ACCEPT_FIELDS"}
ACCEPT_WEIGHT_DECISIONS = {
    "ACCEPT_WEIGHT_RULE",
    "CARRY_CAVEATED_WEIGHT_RULE",
    "ACCEPT_EXPOSURE_RULE",
    "ACCEPT_BULLOCK_RULE",
    "ACCEPT_BULLOCK_CONVERSION",
    "SUPPLY_NEW_RESIDUAL_BLIND_RULE",
}
ACCEPT_SPIN_ROUTES = {
    "EXPOSURE_PROXY",
    "BULLOCK_DISK_CONVERSION",
    "BULLOCK_LIKE_CONVERSION",
    "DIRECT_SOURCE_NATIVE_SPIN",
    "NEW_RESIDUAL_BLIND_RULE",
}
ACCEPT_BOUNDARY_DECISIONS = {
    "ACCEPT_CONTEXT_ONLY",
    "SUPPLY_RESIDUAL_BLIND_CONVERSION_RULE",
}
ACCEPT_SCOPE_DECISIONS = {
    "ACCEPT_TARGET_SET",
    "RESTRICT_TARGET_SET",
}
FORBIDDEN_FALSE_VALUES = {"", "none", "false", "no", "n", "0"}


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


def norm_upper(value: object) -> str:
    return norm(value).upper()


def forbidden_clean(value: object) -> bool:
    return norm(value).lower() in FORBIDDEN_FALSE_VALUES


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
                    "check_id": "BSP_INTAKE_1_RESPONSE_PRESENT",
                    "result": "BLOCKED_PENDING_RESPONSE",
                    "reason": "No completed independent review response CSV is present.",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
        summary_status = "U12506_BETA_SPIN_PROXY_REVIEW_RESPONSE_PENDING_ENDPOINT_BLOCKED"
        proxy_promotion_allowed = False
        beta_cl_replay_preflight_allowed = False
    else:
        decisions = {
            "source_fields": norm_upper(response["source_fields_decision"]),
            "weight_rule": norm_upper(response["weight_rule_decision"]),
            "selected_spin_normalization_route": norm_upper(
                response.get("selected_spin_normalization_route", "")
            ),
            "definition_boundary": norm_upper(response["definition_boundary_decision"]),
            "transfer_scope": norm_upper(response["transfer_scope_decision"]),
        }
        checks = pd.DataFrame(
            [
                {
                    "check_id": "BSP_INTAKE_1_SOURCE_FIELDS",
                    "result": "PASS"
                    if decisions["source_fields"] in ACCEPT_FIELD_DECISIONS
                    else "FAIL",
                    "reason": f"source_fields_decision={decisions['source_fields']}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BSP_INTAKE_2_WEIGHT_RULE",
                    "result": "PASS"
                    if decisions["weight_rule"] in ACCEPT_WEIGHT_DECISIONS
                    else "FAIL",
                    "reason": f"weight_rule_decision={decisions['weight_rule']}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BSP_INTAKE_2B_SELECTED_SPIN_ROUTE",
                    "result": "PASS"
                    if decisions["selected_spin_normalization_route"] in ACCEPT_SPIN_ROUTES
                    else "FAIL",
                    "reason": (
                        "selected_spin_normalization_route="
                        f"{decisions['selected_spin_normalization_route']}"
                    ),
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BSP_INTAKE_3_DEFINITION_BOUNDARY",
                    "result": "PASS"
                    if decisions["definition_boundary"] in ACCEPT_BOUNDARY_DECISIONS
                    else "FAIL",
                    "reason": (
                        "definition_boundary_decision="
                        f"{decisions['definition_boundary']}"
                    ),
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BSP_INTAKE_4_TRANSFER_SCOPE",
                    "result": "PASS"
                    if decisions["transfer_scope"] in ACCEPT_SCOPE_DECISIONS
                    else "FAIL",
                    "reason": f"transfer_scope_decision={decisions['transfer_scope']}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
                {
                    "check_id": "BSP_INTAKE_5_FORBIDDEN_INPUTS",
                    "result": "PASS"
                    if forbidden_clean(response["forbidden_inputs_used"])
                    else "FAIL",
                    "reason": f"forbidden_inputs_used={norm(response['forbidden_inputs_used'])}",
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                },
            ]
        )
        proxy_promotion_allowed = checks["result"].eq("PASS").all()
        beta_cl_replay_preflight_allowed = proxy_promotion_allowed
        summary_status = (
            "U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED"
            if proxy_promotion_allowed
            else "U12506_BETA_SPIN_PROXY_REVIEW_REJECTED_OR_INCOMPLETE_ENDPOINT_BLOCKED"
        )

    summary = pd.DataFrame(
        [
            {
                "review_intake_status": summary_status,
                "response_received": response_received,
                "response_source": str(response_source.relative_to(ROOT)),
                "selected_spin_normalization_route": (
                    norm(response.get("selected_spin_normalization_route", ""))
                    if response_received
                    else "PENDING_INDEPENDENT_REVIEW"
                ),
                "proxy_promotion_allowed": proxy_promotion_allowed,
                "beta_cl_replay_preflight_allowed": beta_cl_replay_preflight_allowed,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": (
                    "build_beta_cl_transfer_prefreeze_manifest"
                    if beta_cl_replay_preflight_allowed
                    else "obtain_independent_spin_proxy_review_response_or_direct_spin_source"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    checks.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_checks.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Spin Proxy Review Response Intake",
        "",
        "This intake validates a completed independent review response if one is",
        "present. In the current state it records whether the response is still",
        "pending. It does not authorize endpoint scoring.",
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
        "Only a passed independent response can move the proxy toward a beta_cl",
        "transfer prefreeze manifest. Endpoint scoring remains false here.",
    ]
    (REPORTS / "ugc12506_beta_closure_spin_proxy_review_response_intake.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
