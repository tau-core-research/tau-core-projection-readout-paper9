#!/usr/bin/env python3
"""Build the UGC12506 Xi_t source-review packet.

This packet prepares the readout-relevant K_t(R) envelope mapping and
clock/readout settling proxy for independent source review.  It does not accept
the route, does not promote an accepted manifest, and does not score an
endpoint.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_source_review_packet_not_endpoint"

INPUT_FILES = [
    "ugc12506_highmass_fast_source_context_evidence.csv",
    "ugc12506_observer_path_interloper_audit_summary.csv",
    "ugc12506_projection_highspin_preflight_observables.csv",
    "time_readout_xi_p1_source_review_intake.csv",
    "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv",
    "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv",
    "ugc12506_xi_t_highspin_envelope_clock_shell_gates.csv",
    "ugc12506_xi_t_normalization_theorem.csv",
    "ugc12506_xi_t_epsilon_cap_protocol_theorem.csv",
    "ugc12506_xi_t_accepted_manifest_gate_items.csv",
]


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    evidence = pd.read_csv(DATA / "ugc12506_highmass_fast_source_context_evidence.csv")
    observables = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    intake = pd.read_csv(DATA / "time_readout_xi_p1_source_review_intake.csv")
    intake = intake.loc[intake["galaxy"].eq(GALAXY)].iloc[0]
    components = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv")
    manifest = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv").iloc[0]
    cap = pd.read_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_theorem.csv").iloc[0]
    accepted_gate = pd.read_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_items.csv")

    source_packet = pd.DataFrame(
        [
            {
                "packet_id": "U12506_XIT_REVIEW_PACKET_1_INPUTS",
                "packet_status": "READY_FOR_INDEPENDENT_REVIEW_RESPONSE",
                "review_target": "UGC12506 source-only Xi_t K_t(R) mapping and clock/readout settling proxy",
                "candidate_formula": str(manifest["formula_text"]),
                "candidate_kernel": str(manifest["kernel_text"]),
                "epsilon_rule": str(manifest["epsilon_rule"]),
                "epsilon_t": float(manifest["epsilon_t"]),
                "source_load_total": float(manifest["source_load_total"]),
                "path_policy": str(manifest["path_policy"]),
                "n_source_evidence_rows": int(len(evidence)),
                "n_source_observables": int(len(observables)),
                "n_clock_components": int(len(components)),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
            }
        ]
    )
    source_packet["galaxy"] = GALAXY
    source_packet["claim_boundary"] = CLAIM_BOUNDARY

    review_obligations = pd.DataFrame(
        [
            {
                "obligation_id": "U12506_XIT_REV_1_HIGHSPIN_CLOCK_STATUS",
                "obligation_status": "REVIEW_REQUIRED",
                "question": "Is the reported high-spin, low-density H I envelope source context admissible as a clock/readout settling proxy?",
                "accepted_evidence": "HIghMass or source-native H I context: high spin, low-density extended H I, stable/settling interpretation",
                "forbidden_evidence": "rotation-curve residual size or best-fitting readout family",
            },
            {
                "obligation_id": "U12506_XIT_REV_2_EDGEON_PV_CLOCK_SLICE",
                "obligation_status": "REVIEW_REQUIRED",
                "question": "Is the high-inclination PV/envelope-method context admissible as a time-slice/readout proxy rather than only an ordinary projection proxy?",
                "accepted_evidence": "source statements that velocity-field curves underestimate rotation and PV/envelope method is required",
                "forbidden_evidence": "choosing the clock channel because it improves the endpoint curve",
            },
            {
                "obligation_id": "U12506_XIT_REV_3_ENVELOPE_MAPPING",
                "obligation_status": "REVIEW_REQUIRED",
                "question": "Is the radial K_t envelope ramp from disk scale to H I support radius acceptable as source-side mapping?",
                "accepted_evidence": "source-frozen R_d, R_opt, R_HI, H I extent, and low-density envelope support",
                "forbidden_evidence": "moving the active radius or ramp shape after inspecting residual zones",
            },
            {
                "obligation_id": "U12506_XIT_REV_4_ASYMMETRY_PHASE",
                "obligation_status": "REVIEW_REQUIRED_CAVEATED",
                "question": "Should the approaching/receding side asymmetry remain as a caveated clock-phase component, be demoted, or be excluded?",
                "accepted_evidence": "source-native PV/envelope asymmetry statements and source-side extent asymmetry",
                "forbidden_evidence": "including asymmetry only where the curve underpredicts",
            },
            {
                "obligation_id": "U12506_XIT_REV_5_PATH_ZERO_POLICY",
                "obligation_status": "REVIEW_REQUIRED_FOR_NONZERO_PATH_ONLY",
                "question": "Is the current zero path/environment term correct until a cone/path review establishes a foreground/path object?",
                "accepted_evidence": "observer-path interloper audit and catalogue cone/path review",
                "forbidden_evidence": "activating path load from image-plane coincidence or residual rescue",
            },
            {
                "obligation_id": "U12506_XIT_REV_6_CAP_POLICY",
                "obligation_status": "PROTOCOL_REVIEW_REQUIRED",
                "question": "May epsilon_cap=0.035 be carried as a predeclared small-mismatch protocol cap for this source shell?",
                "accepted_evidence": str(cap["statement"]),
                "forbidden_evidence": "claiming epsilon_cap is a universal Tau Core constant",
            },
        ]
    )
    review_obligations["galaxy"] = GALAXY
    review_obligations["endpoint_scores_allowed"] = False
    review_obligations["uses_vobs_or_residual"] = False
    review_obligations["claim_boundary"] = CLAIM_BOUNDARY

    response_template = pd.DataFrame(
        [
            {
                "allowed_response": "ACCEPT_SOURCE_ONLY_XIT_MANIFEST_WITH_PROTOCOL_CAP",
                "response_meaning": "accept K_t(R), clock proxy, zero-path policy, and epsilon_cap as protocol cap",
                "effect_on_endpoint_path": "allows a future accepted-manifest gate, but not endpoint scoring by response alone",
                "requires_extra_source_work": False,
                "endpoint_scores_allowed_by_response_alone": False,
            },
            {
                "allowed_response": "ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL",
                "response_meaning": "accept K_t(R) shape but carry cap or asymmetry as interval/control uncertainty",
                "effect_on_endpoint_path": "requires interval manifest and controls before scoring",
                "requires_extra_source_work": False,
                "endpoint_scores_allowed_by_response_alone": False,
            },
            {
                "allowed_response": "ACCEPT_CORE_COMPONENTS_DROP_ASYMMETRY",
                "response_meaning": "accept high-spin, edge-on PV, and envelope terms, but exclude asymmetry phase component",
                "effect_on_endpoint_path": "rebuild source shell without asymmetry before accepted-manifest gate",
                "requires_extra_source_work": False,
                "endpoint_scores_allowed_by_response_alone": False,
            },
            {
                "allowed_response": "REQUEST_SOURCE_NATIVE_REMEASUREMENT",
                "response_meaning": "request new source-native measurement of envelope window, asymmetry, or clock proxy",
                "effect_on_endpoint_path": "keeps endpoint blocked and creates a source acquisition/reduction task",
                "requires_extra_source_work": True,
                "endpoint_scores_allowed_by_response_alone": False,
            },
            {
                "allowed_response": "REJECT_XIT_CLOCK_ROUTE",
                "response_meaning": "reject UGC12506 Xi_t time-readout route as insufficiently source-grounded",
                "effect_on_endpoint_path": "preserve as negative route result; do not run Xi_t endpoint",
                "requires_extra_source_work": False,
                "endpoint_scores_allowed_by_response_alone": False,
            },
        ]
    )
    response_template["galaxy"] = GALAXY
    response_template["uses_vobs_or_residual"] = False
    response_template["claim_boundary"] = CLAIM_BOUNDARY

    forbidden_inputs = pd.DataFrame(
        [
            {
                "forbidden_input_id": "U12506_XIT_FORBID_1_ROTATION_RESIDUALS",
                "forbidden_input": "v_obs residuals, endpoint RMSE, or radial residual zones",
                "reason": "would turn source review into residual-selected clock tuning",
            },
            {
                "forbidden_input_id": "U12506_XIT_FORBID_2_BASELINE_RANKS",
                "forbidden_input": "Newton/MOND/RAR/RMOND/TPG baseline ranks",
                "reason": "baseline comparison can only be post-score diagnostic context",
            },
            {
                "forbidden_input_id": "U12506_XIT_FORBID_3_TAU_WRONG_FAMILY_SCORES",
                "forbidden_input": "wrong-family Tau score ranks or best Tau family",
                "reason": "readout route must be selected from source morphology/projection evidence",
            },
            {
                "forbidden_input_id": "U12506_XIT_FORBID_4_POSTHOC_CAP_CHANGE",
                "forbidden_input": "changing epsilon_cap after endpoint scoring",
                "reason": "would convert the protocol cap into amplitude rescue",
            },
            {
                "forbidden_input_id": "U12506_XIT_FORBID_5_FOREGROUND_RESCUE",
                "forbidden_input": "activating path term from a residual deficit without cone/path evidence",
                "reason": "path/environment term must remain zero unless source review supports it",
            },
        ]
    )
    forbidden_inputs["galaxy"] = GALAXY
    forbidden_inputs["claim_boundary"] = CLAIM_BOUNDARY

    blocker_update = pd.DataFrame(
        [
            {
                "blocker_symbol": "K_t(R) envelope mapping",
                "updated_status": "INDEPENDENT_REVIEW_PACKET_READY_RESPONSE_PENDING",
                "remaining_blocker": "review response required before K_t(R) can be accepted",
                "blocks_endpoint_manifest": True,
            },
            {
                "blocker_symbol": "clock/readout settling proxy",
                "updated_status": "INDEPENDENT_REVIEW_PACKET_READY_RESPONSE_PENDING",
                "remaining_blocker": "review response required before clock proxy can be accepted",
                "blocks_endpoint_manifest": True,
            },
            {
                "blocker_symbol": "epsilon_cap",
                "updated_status": "PROTOCOL_CAP_FROZEN_REVIEW_RESPONSE_PENDING_FOR_MANIFEST_USE",
                "remaining_blocker": "response must record cap as protocol cap, not universal law",
                "blocks_endpoint_manifest": True,
            },
            {
                "blocker_symbol": "path/environment term",
                "updated_status": "ZERO_PATH_POLICY_READY_FOR_REVIEW",
                "remaining_blocker": "nonzero path term requires new cone/path review",
                "blocks_endpoint_manifest": False,
            },
        ]
    )
    blocker_update["galaxy"] = GALAXY
    blocker_update["endpoint_scores_allowed"] = False
    blocker_update["uses_vobs_or_residual"] = False
    blocker_update["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_XIT_REVIEW_G1_PACKET_READY",
                "gate_status": "PASS_PACKET_READY_RESPONSE_PENDING",
                "evidence": "source packet, obligations, response template, forbidden inputs, and hashes written",
                "remaining_obligation": "obtain independent review response",
            },
            {
                "gate_id": "U12506_XIT_REVIEW_G2_FORBIDDEN_INPUTS",
                "gate_status": "PASS_GUARDRAILS_RECORDED",
                "evidence": "rotation residuals, baseline ranks, wrong-family scores, cap changes, and foreground rescue are forbidden",
                "remaining_obligation": "enforce in response intake validator",
            },
            {
                "gate_id": "U12506_XIT_REVIEW_G3_ENDPOINT",
                "gate_status": "BLOCKED",
                "evidence": "review response pending and accepted-manifest gate not ready",
                "remaining_obligation": "do not score endpoint",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    input_hashes = []
    for filename in INPUT_FILES:
        path = DATA / filename
        input_hashes.append(
            {
                "input_file": filename,
                "exists": path.exists(),
                "sha256": file_sha256(path) if path.exists() else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    input_hashes = pd.DataFrame(input_hashes)

    summary = pd.DataFrame(
        [
            {
                "review_packet_status": "U12506_XI_T_SOURCE_REVIEW_PACKET_READY_RESPONSE_PENDING",
                "galaxy": GALAXY,
                "review_packet_ready": True,
                "review_response_received": False,
                "accepted_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "n_obligations": int(len(review_obligations)),
                "n_allowed_responses": int(len(response_template)),
                "next_gate": "intake_independent_ugc12506_xi_t_source_review_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    source_packet.to_csv(DATA / "ugc12506_xi_t_source_review_packet.csv", index=False)
    review_obligations.to_csv(DATA / "ugc12506_xi_t_source_review_obligations.csv", index=False)
    response_template.to_csv(DATA / "ugc12506_xi_t_source_review_response_template.csv", index=False)
    forbidden_inputs.to_csv(DATA / "ugc12506_xi_t_source_review_forbidden_inputs.csv", index=False)
    blocker_update.to_csv(DATA / "ugc12506_xi_t_source_review_blocker_update.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_source_review_gates.csv", index=False)
    input_hashes.to_csv(DATA / "ugc12506_xi_t_source_review_input_hashes.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_source_review_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Source-Review Packet",
            "",
            "This packet prepares the UGC12506 time-readout source shell for independent review. It does not promote an accepted manifest and does not score an endpoint.",
            "",
            "## Source Packet",
            "",
            markdown_table(source_packet),
            "",
            "## Review Obligations",
            "",
            markdown_table(review_obligations),
            "",
            "## Allowed Responses",
            "",
            markdown_table(response_template),
            "",
            "## Forbidden Inputs",
            "",
            markdown_table(forbidden_inputs),
            "",
            "## Blocker Update",
            "",
            markdown_table(blocker_update),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Input Hashes",
            "",
            markdown_table(input_hashes),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Claim Boundary",
            "",
            "The packet is ready for an independent source response. It preserves the zero-path policy and forbids residual-based promotion of the clock/readout route.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_source_review_packet.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
