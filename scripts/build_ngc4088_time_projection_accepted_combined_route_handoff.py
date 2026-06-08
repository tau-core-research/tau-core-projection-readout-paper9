#!/usr/bin/env python3
"""Build the NGC4088 accepted combined-route handoff after double-count review.

This artifact does not introduce a new endpoint score.  It records that the
double-count-resolved combined route is the already accepted additive
warp/history endpoint with Xi_eff set to one.  The clock-only replay is
preserved as a control, and the additive-plus-clock curve remains a rejected
stress test.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_time_projection_accepted_combined_route_handoff"


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


def bool_value(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    endpoint = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_summary.csv").iloc[0]
    scores = pd.read_csv(DATA / "ngc4088_warp_history_accepted_endpoint_scores.csv")
    double_count = pd.read_csv(
        DATA / "ngc4088_time_projection_double_count_resolution_summary.csv"
    ).iloc[0]
    ablation = pd.read_csv(DATA / "ngc4088_time_projection_ablation_control_summary.csv").iloc[0]

    matched = scores[scores["model_id"].eq("TAU_NGC4088_WARP_HISTORY_ACCEPTED")].iloc[0]
    accepted_rmse = float(matched["rmse_km_s"])
    clock_only_rmse = float(ablation["clock_only_rmse_km_s"])
    stress_rmse = float(ablation["additive_plus_clock_rmse_km_s"])
    double_count_resolved = (
        str(double_count["double_count_resolution_status"])
        == "NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE"
    )
    endpoint_allowed = bool_value(endpoint["endpoint_scores_allowed"])
    accepted_route_allowed = double_count_resolved and endpoint_allowed

    routes = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "route_id": "ACCEPTED_COMBINED_ADDITIVE_WARP_HISTORY_XI_ONE",
                "route_status": (
                    "ACCEPTED_ENDPOINT_ROUTE"
                    if accepted_route_allowed
                    else "BLOCKED"
                ),
                "xi_eff_policy": "Xi_eff=1",
                "rmse_km_s": accepted_rmse,
                "control_replay_allowed": False,
                "endpoint_scores_allowed": accepted_route_allowed,
                "endpoint_validation_claim": False,
                "interpretation": (
                    "same numerical curve as the caveated accepted additive "
                    "warp/history endpoint after double-count resolution"
                ),
            },
            {
                "galaxy": GALAXY,
                "route_id": "CLOCK_ONLY_XIEFF_ON_BASE_PROJECTION",
                "route_status": "CONTROL_ROUTE_ALLOWED_NOT_ENDPOINT",
                "xi_eff_policy": "active only on the base projection control",
                "rmse_km_s": clock_only_rmse,
                "control_replay_allowed": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "interpretation": "useful clock/readout control signal, not an accepted endpoint",
            },
            {
                "galaxy": GALAXY,
                "route_id": "ADDITIVE_WARP_HISTORY_PLUS_XIEFF",
                "route_status": "STRESS_TEST_REJECTED_FOR_ENDPOINT",
                "xi_eff_policy": "forbidden with the additive kernel until non-overlap clock evidence exists",
                "rmse_km_s": stress_rmse,
                "control_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "interpretation": "improves numerically but double-counts source evidence",
            },
        ]
    )
    routes["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "handoff_status": (
                    "NGC4088_ACCEPTED_COMBINED_ROUTE_HANDOFF_READY"
                    if accepted_route_allowed
                    else "NGC4088_ACCEPTED_COMBINED_ROUTE_HANDOFF_BLOCKED"
                ),
                "galaxy": GALAXY,
                "accepted_combined_route": "additive_warp_history_endpoint_with_Xi_eff_equal_one",
                "accepted_combined_rmse_km_s": accepted_rmse,
                "clock_only_control_rmse_km_s": clock_only_rmse,
                "additive_plus_clock_stress_rmse_km_s": stress_rmse,
                "stress_test_improves_over_accepted_route": stress_rmse < accepted_rmse,
                "stress_test_endpoint_allowed": False,
                "clock_only_control_preserved": bool_value(
                    double_count["clock_only_control_preserved"]
                ),
                "time_endpoint_reopened": False,
                "requires_new_nonoverlap_clock_evidence": True,
                "construction_used_vobs": False,
                "reads_endpoint_scores_for_handoff": True,
                "endpoint_scores_allowed_for_accepted_combined_route": accepted_route_allowed,
                "endpoint_validation_claim": False,
                "claim_status": (
                    "single-galaxy caveated accepted route plus time-projection control; "
                    "not population validation"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4088_TPH_G1_ADDITIVE_ENDPOINT_EXISTS",
                "gate_status": "PASS" if endpoint_allowed else "BLOCKED",
                "evidence": str(endpoint["endpoint_status"]),
                "remaining_obligation": "retain single-galaxy caveated status",
            },
            {
                "gate_id": "N4088_TPH_G2_DOUBLE_COUNT_RESOLVED",
                "gate_status": "PASS" if double_count_resolved else "BLOCKED",
                "evidence": str(double_count["double_count_resolution_status"]),
                "remaining_obligation": "keep Xi_eff=1 for the combined route",
            },
            {
                "gate_id": "N4088_TPH_G3_CLOCK_CONTROL_PRESERVED",
                "gate_status": "PASS_CONTROL_ONLY",
                "evidence": str(ablation["interpretation"]),
                "remaining_obligation": "do not present clock-only replay as endpoint validation",
            },
            {
                "gate_id": "N4088_TPH_G4_STRESS_TEST_NOT_ENDPOINT",
                "gate_status": "PASS_GUARDRAIL",
                "evidence": "additive-plus-clock stress RMSE is lower but endpoint permission is false",
                "remaining_obligation": "new endpoint requires independent non-overlap clock evidence",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["claim_boundary"] = CLAIM_BOUNDARY

    routes.to_csv(
        DATA / "ngc4088_time_projection_accepted_combined_route_handoff_routes.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ngc4088_time_projection_accepted_combined_route_handoff_gates.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ngc4088_time_projection_accepted_combined_route_handoff_summary.csv",
        index=False,
    )

    report = "\n".join(
        [
            "# NGC4088 Time-Projection Accepted Combined-Route Handoff",
            "",
            "This artifact records the route policy after the double-count audit. It",
            "does not compute a new endpoint score. The accepted combined route is",
            "the caveated accepted additive warp/history endpoint with `Xi_eff=1`.",
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Routes",
            "",
            markdown_table(routes),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Claim Boundary",
            "",
            "The clock-only route remains a useful control signal. The additive-plus-",
            "clock stress curve is not endpoint-permitted, even though it improves",
            "the RMSE, because every current `Xi_eff` source term overlaps the active",
            "additive warp/history morphology route.",
            "",
        ]
    )
    (REPORTS / "ngc4088_time_projection_accepted_combined_route_handoff.md").write_text(
        report, encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
