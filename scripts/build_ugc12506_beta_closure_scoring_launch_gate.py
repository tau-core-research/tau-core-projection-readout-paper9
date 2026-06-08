#!/usr/bin/env python3
"""Build the UGC12506 beta-closure transfer scoring launch gate.

This is the last non-scoring gate before any beta_cl transfer endpoint or
control replay.  It verifies that a spin-normalization route was independently
accepted, that source-frozen prefreeze values exist, and that no endpoint score
can be launched from a pending review state.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_scoring_launch_gate_not_endpoint"


REQUIRED_INPUTS = {
    "decision_matrix_summary": DATA / "ugc12506_beta_closure_spin_route_decision_matrix_summary.csv",
    "review_intake_summary": DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv",
    "spin_route_prefreeze_summary": DATA / "ugc12506_beta_closure_spin_route_prefreeze_summary.csv",
    "spin_route_prefreeze_values": DATA / "ugc12506_beta_closure_spin_route_prefreeze_values.csv",
    "transfer_carrier_freeze_summary": DATA / "ugc12506_beta_closure_transfer_carrier_freeze_summary.csv",
    "transfer_carrier_manifest": DATA / "ugc12506_beta_closure_transfer_carrier_manifest.csv",
    "transfer_candidates": DATA / "ugc12506_beta_closure_transfer_candidates.csv",
    "halo_fit_fields": DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv",
    "priority_gate": DATA / "ugc12506_beta_closure_transfer_priority_gate.csv",
}


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


def read_row(path: Path) -> pd.Series:
    if not path.exists():
        return pd.Series(dtype=object)
    df = pd.read_csv(path)
    if df.empty:
        return pd.Series(dtype=object)
    return df.iloc[0]


def bool_value(row: pd.Series, key: str) -> bool:
    if row.empty or key not in row:
        return False
    value = row[key]
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    input_rows = []
    for input_id, path in REQUIRED_INPUTS.items():
        exists = path.exists()
        n_rows = 0
        n_columns = 0
        if exists:
            try:
                df = pd.read_csv(path)
                n_rows = len(df)
                n_columns = len(df.columns)
            except pd.errors.EmptyDataError:
                n_rows = 0
                n_columns = 0
        input_rows.append(
            {
                "input_id": input_id,
                "path": str(path.relative_to(ROOT)),
                "exists": exists,
                "n_rows": n_rows,
                "n_columns": n_columns,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    inputs = pd.DataFrame(input_rows)

    intake = read_row(REQUIRED_INPUTS["review_intake_summary"])
    prefreeze = read_row(REQUIRED_INPUTS["spin_route_prefreeze_summary"])
    decision = read_row(REQUIRED_INPUTS["decision_matrix_summary"])
    carrier = read_row(REQUIRED_INPUTS["transfer_carrier_freeze_summary"])
    prefreeze_values = pd.read_csv(REQUIRED_INPUTS["spin_route_prefreeze_values"])
    carrier_manifest = pd.read_csv(REQUIRED_INPUTS["transfer_carrier_manifest"])

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BSP_SCORE_1_INPUTS_PRESENT",
                "gate_status": "PASS" if inputs["exists"].all() else "BLOCKED",
                "reason": "all required scoring-launch inputs exist"
                if inputs["exists"].all()
                else "one or more required scoring-launch inputs are missing",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BSP_SCORE_2_REVIEW_ROUTE_ACCEPTED",
                "gate_status": "PASS"
                if bool_value(intake, "beta_cl_replay_preflight_allowed")
                else "BLOCKED",
                "reason": f"review_intake_status={intake.get('review_intake_status', 'missing')}",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BSP_SCORE_3_PREFREEZE_VALUES_EXIST",
                "gate_status": "PASS"
                if bool_value(prefreeze, "beta_cl_transfer_prefreeze_allowed")
                and len(prefreeze_values) > 0
                else "BLOCKED",
                "reason": f"prefreeze_status={prefreeze.get('spin_route_prefreeze_status', 'missing')}; n_values={len(prefreeze_values)}",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BSP_SCORE_4_DECISION_MATRIX_READY",
                "gate_status": "PASS"
                if str(decision.get("spin_route_decision_matrix_status", "")).endswith(
                    "REVIEW_REQUIRED"
                )
                else "BLOCKED",
                "reason": f"decision_matrix_status={decision.get('spin_route_decision_matrix_status', 'missing')}",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BSP_SCORE_5_CARRIER_MANIFEST_READY",
                "gate_status": "PASS"
                if bool_value(carrier, "carrier_manifest_ready_for_scoring")
                and len(carrier_manifest) > 0
                else "BLOCKED",
                "reason": f"carrier_freeze_status={carrier.get('carrier_freeze_status', 'missing')}; n_carriers={len(carrier_manifest)}",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    launch_allowed = gates["gate_status"].eq("PASS").all()
    summary = pd.DataFrame(
        [
            {
                "scoring_launch_status": (
                    "U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY"
                    if launch_allowed
                    else "U12506_BETA_CLOSURE_SCORING_LAUNCH_BLOCKED_REVIEW_PREFREEZE_PENDING"
                ),
                "selected_spin_normalization_route": intake.get(
                    "selected_spin_normalization_route", "PENDING_INDEPENDENT_REVIEW"
                ),
                "n_required_inputs": len(inputs),
                "n_missing_inputs": int((~inputs["exists"]).sum()),
                "n_pass_gates": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked_gates": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_prefrozen_transfer_rows": len(prefreeze_values),
                "n_frozen_carrier_rows": len(carrier_manifest),
                "beta_cl_transfer_scoring_allowed": launch_allowed,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": (
                    "run_beta_cl_transfer_control_replay_scoring"
                    if launch_allowed
                    else "obtain_review_response_then_prefreeze_spin_route_values"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    scoring_protocol = pd.DataFrame(
        [
            {
                "protocol_step": "SCORING_1_READ_FROZEN_VALUES",
                "required_artifact": "ugc12506_beta_closure_spin_route_prefreeze_values.csv",
                "allowed_to_read_vobs": False,
                "status_now": "READY" if len(prefreeze_values) > 0 else "BLOCKED_NO_PREFREEZE_VALUES",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "protocol_step": "SCORING_2_BUILD_TRANSFER_FORMULA_MANIFEST",
                "required_artifact": "future_beta_cl_transfer_formula_manifest.csv",
                "allowed_to_read_vobs": False,
                "status_now": "BLOCKED_UNTIL_PREFREEZE_AND_CARRIER_READY",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "protocol_step": "SCORING_3_RUN_SEPARATE_SCORING_SCRIPT",
                "required_artifact": "future_beta_cl_transfer_scores.csv",
                "allowed_to_read_vobs": True,
                "status_now": "BLOCKED_UNTIL_FORMULA_MANIFEST_FROZEN",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    inputs.to_csv(DATA / "ugc12506_beta_closure_scoring_launch_inputs.csv", index=False)
    gates.to_csv(DATA / "ugc12506_beta_closure_scoring_launch_gates.csv", index=False)
    scoring_protocol.to_csv(
        DATA / "ugc12506_beta_closure_scoring_protocol_skeleton.csv",
        index=False,
    )
    summary.to_csv(DATA / "ugc12506_beta_closure_scoring_launch_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Scoring Launch Gate",
        "",
        "This gate moves the beta_cl route toward scoring without scoring it.",
        "It verifies whether the independent spin-route review and prefreeze",
        "contracts are complete. In the current state the launch is blocked.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Required Inputs",
        "",
        markdown_table(inputs),
        "",
        "## Scoring Protocol Skeleton",
        "",
        markdown_table(scoring_protocol),
        "",
        "## Claim Boundary",
        "",
        "This artifact does not read rotation curves and does not compute endpoint",
        "scores. It only defines the final non-scoring launch gate before a future",
        "separate scoring script.",
    ]
    (REPORTS / "ugc12506_beta_closure_scoring_launch_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
