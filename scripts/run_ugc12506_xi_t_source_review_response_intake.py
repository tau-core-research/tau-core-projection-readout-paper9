#!/usr/bin/env python3
"""Validate the UGC12506 Xi_t source-review response.

This intake follows the UGC12506 Xi_t source-review packet.  It is not a
reviewer, does not promote an accepted manifest, and does not score an
endpoint.  If the response file is absent, it records a clean pending state.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_source_review_response_intake_not_endpoint"
RESPONSE_FILE = DATA / "ugc12506_xi_t_source_review_response.csv"


ACCEPT_LIKE = {
    "ACCEPT_SOURCE_ONLY_XIT_MANIFEST_WITH_PROTOCOL_CAP",
    "ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL",
    "ACCEPT_CORE_COMPONENTS_DROP_ASYMMETRY",
}
REJECT_OR_REMEASURE = {
    "REQUEST_SOURCE_NATIVE_REMEASUREMENT",
    "REJECT_XIT_CLOCK_ROUTE",
}


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


def split_tokens(value: object) -> set[str]:
    if pd.isna(value):
        return set()
    text = str(value).strip()
    if not text or text.upper() in {"NONE", "PENDING", "PENDING_INDEPENDENT_REVIEW"}:
        return set()
    return {item.strip() for item in text.replace(",", ";").split(";") if item.strip()}


def normalized(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def bool_from_row(row: pd.Series, field: str, default: bool = False) -> bool:
    if field not in row.index or pd.isna(row[field]):
        return default
    value = row[field]
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    packet_summary = pd.read_csv(DATA / "ugc12506_xi_t_source_review_summary.csv").iloc[0]
    packet = pd.read_csv(DATA / "ugc12506_xi_t_source_review_packet.csv").iloc[0]
    template = pd.read_csv(DATA / "ugc12506_xi_t_source_review_response_template.csv")
    forbidden = pd.read_csv(DATA / "ugc12506_xi_t_source_review_forbidden_inputs.csv")
    accepted_gate = pd.read_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_summary.csv").iloc[0]

    allowed_responses = set(template["allowed_response"])
    response_received = RESPONSE_FILE.exists()
    response_row = pd.Series(dtype=object)
    if response_received:
        response = pd.read_csv(RESPONSE_FILE)
        response_row = response.iloc[0]
        review_decision = normalized(response_row.get("allowed_response", ""))
        source_inputs_used = split_tokens(response_row.get("source_inputs_used", ""))
        forbidden_used = split_tokens(response_row.get("forbidden_inputs_used", ""))
        response_claims_endpoint = bool_from_row(
            response_row, "endpoint_scores_allowed_after_response", default=False
        )
        response_claims_manifest = bool_from_row(
            response_row, "accepted_manifest_allowed_after_response", default=False
        )
        response_claims_universal_cap = bool_from_row(
            response_row, "claims_universal_tau_constant", default=False
        )
    else:
        review_decision = "PENDING_INDEPENDENT_REVIEW"
        source_inputs_used = set()
        forbidden_used = set()
        response_claims_endpoint = False
        response_claims_manifest = False
        response_claims_universal_cap = False

    allowed_response_valid = review_decision in allowed_responses
    source_inputs_present = bool(source_inputs_used)
    forbidden_clean = not forbidden_used
    endpoint_clean = not response_claims_endpoint
    manifest_clean = not response_claims_manifest
    universal_cap_clean = not response_claims_universal_cap
    accept_like = review_decision in ACCEPT_LIKE
    reject_like = review_decision in REJECT_OR_REMEASURE

    review_usable = (
        response_received
        and allowed_response_valid
        and source_inputs_present
        and forbidden_clean
        and endpoint_clean
        and manifest_clean
        and universal_cap_clean
    )

    selected_route_status = "NONE"
    next_gate = "obtain_independent_ugc12506_xi_t_source_review_response"
    if review_usable and accept_like:
        selected_route_status = f"{review_decision}_SOURCE_REVIEW_USABLE_MANIFEST_GATE_REQUIRED"
        next_gate = "rerun_ugc12506_xi_t_accepted_manifest_gate_with_review_response"
    elif review_usable and reject_like:
        selected_route_status = f"{review_decision}_SOURCE_REVIEW_ROUTE_NOT_USABLE"
        next_gate = "preserve_negative_route_or_request_source_remeasurement"
    elif response_received:
        selected_route_status = "REVIEW_RESPONSE_INVALID_OR_INCOMPLETE"
        next_gate = "repair_independent_ugc12506_xi_t_source_review_response"

    validation = pd.DataFrame(
        [
            {
                "validation_id": "U12506_XIT_SOURCE_REVIEW_RESPONSE_INTAKE_V1",
                "galaxy": GALAXY,
                "response_received": response_received,
                "review_decision": review_decision,
                "allowed_response_valid": allowed_response_valid,
                "source_inputs_present": source_inputs_present,
                "source_inputs_used": ";".join(sorted(source_inputs_used)) if source_inputs_used else "none",
                "forbidden_clean": forbidden_clean,
                "forbidden_inputs_used": ";".join(sorted(forbidden_used)) if forbidden_used else "none",
                "response_claims_endpoint_scores": response_claims_endpoint,
                "response_claims_accepted_manifest": response_claims_manifest,
                "response_claims_universal_tau_constant": response_claims_universal_cap,
                "review_usable": review_usable,
                "selected_route_status": selected_route_status,
                "accepted_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_XIT_RESP_G1_PACKET_READY",
                "gate_status": "PASS" if bool(packet_summary["review_packet_ready"]) else "BLOCKED",
                "evidence": str(packet["packet_status"]),
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_RESP_G2_RESPONSE_PRESENT",
                "gate_status": "PASS" if response_received else "PENDING",
                "evidence": RESPONSE_FILE.name if response_received else "no response file present",
                "remaining_obligation": "obtain independent source-review response"
                if not response_received
                else "none",
            },
            {
                "gate_id": "U12506_XIT_RESP_G3_ALLOWED_RESPONSE",
                "gate_status": "PASS" if allowed_response_valid else "BLOCKED",
                "evidence": review_decision,
                "remaining_obligation": "choose one allowed response from template"
                if response_received and not allowed_response_valid
                else "pending response" if not response_received else "none",
            },
            {
                "gate_id": "U12506_XIT_RESP_G4_SOURCE_INPUTS",
                "gate_status": "PASS" if source_inputs_present else "BLOCKED",
                "evidence": validation.iloc[0]["source_inputs_used"],
                "remaining_obligation": "cite source-side review inputs"
                if response_received and not source_inputs_present
                else "pending response" if not response_received else "none",
            },
            {
                "gate_id": "U12506_XIT_RESP_G5_FORBIDDEN_INPUTS",
                "gate_status": "PASS" if forbidden_clean else "BLOCKED",
                "evidence": validation.iloc[0]["forbidden_inputs_used"],
                "remaining_obligation": "remove residual/rank/post-hoc inputs"
                if not forbidden_clean
                else "none",
            },
            {
                "gate_id": "U12506_XIT_RESP_G6_NO_RESPONSE_ALONE_ENDPOINT",
                "gate_status": "PASS" if endpoint_clean else "BLOCKED",
                "evidence": f"endpoint_scores_allowed_after_response={response_claims_endpoint}",
                "remaining_obligation": "response may not authorize endpoint scoring by itself",
            },
            {
                "gate_id": "U12506_XIT_RESP_G7_NO_RESPONSE_ALONE_MANIFEST",
                "gate_status": "PASS" if manifest_clean else "BLOCKED",
                "evidence": f"accepted_manifest_allowed_after_response={response_claims_manifest}",
                "remaining_obligation": "response may only feed the accepted-manifest gate",
            },
            {
                "gate_id": "U12506_XIT_RESP_G8_CAP_BOUNDARY",
                "gate_status": "PASS" if universal_cap_clean else "BLOCKED",
                "evidence": f"claims_universal_tau_constant={response_claims_universal_cap}",
                "remaining_obligation": "cap cannot be promoted to universal constant by review response",
            },
            {
                "gate_id": "U12506_XIT_RESP_G9_ENDPOINT_BLOCK",
                "gate_status": "BLOCKED",
                "evidence": "endpoint requires a separate accepted-manifest gate after response intake",
                "remaining_obligation": "endpoint scoring forbidden at response intake",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    blockers = pd.DataFrame(
        [
            {
                "blocker_symbol": "independent source-review response",
                "blocker_status": "OPEN" if not response_received else "INTAKED",
                "blocks_accepted_manifest": not review_usable or reject_like,
                "resolution_path": next_gate,
            },
            {
                "blocker_symbol": "accepted Xi_t manifest",
                "blocker_status": str(accepted_gate["accepted_manifest_status"]),
                "blocks_accepted_manifest": True,
                "resolution_path": "rerun accepted-manifest gate only after usable review response",
            },
            {
                "blocker_symbol": "endpoint scoring",
                "blocker_status": "FORBIDDEN_AT_RESPONSE_INTAKE",
                "blocks_accepted_manifest": False,
                "resolution_path": "separate endpoint script only after accepted manifest",
            },
        ]
    )
    blockers["galaxy"] = GALAXY
    blockers["endpoint_scores_allowed"] = False
    blockers["uses_vobs_or_residual"] = False
    blockers["claim_boundary"] = CLAIM_BOUNDARY

    status = (
        "U12506_XI_T_SOURCE_REVIEW_RESPONSE_INTAKE_PENDING_ENDPOINT_BLOCKED"
        if not response_received
        else "U12506_XI_T_SOURCE_REVIEW_RESPONSE_USABLE_MANIFEST_GATE_REQUIRED"
        if review_usable and accept_like
        else "U12506_XI_T_SOURCE_REVIEW_RESPONSE_REJECTS_ROUTE_ENDPOINT_BLOCKED"
        if review_usable and reject_like
        else "U12506_XI_T_SOURCE_REVIEW_RESPONSE_INVALID_ENDPOINT_BLOCKED"
    )
    summary = pd.DataFrame(
        [
            {
                "review_response_intake_status": status,
                "galaxy": GALAXY,
                "response_received": response_received,
                "review_usable": review_usable,
                "selected_route_status": selected_route_status,
                "accepted_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": next_gate,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    validation.to_csv(DATA / "ugc12506_xi_t_source_review_response_intake_validation.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_source_review_response_intake_gates.csv", index=False)
    blockers.to_csv(DATA / "ugc12506_xi_t_source_review_response_intake_blockers.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_source_review_response_intake_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Source-Review Response Intake",
            "",
            "This intake validates an independent source-review response for the UGC12506 time-readout shell. It is not a reviewer, not an accepted manifest, and not an endpoint.",
            "",
            "## Validation",
            "",
            markdown_table(validation),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Blockers",
            "",
            markdown_table(blockers),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Claim Boundary",
            "",
            "A usable response may feed the accepted-manifest gate. It cannot by itself authorize endpoint scoring or promote epsilon_cap to a universal Tau Core constant.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_source_review_response_intake.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
