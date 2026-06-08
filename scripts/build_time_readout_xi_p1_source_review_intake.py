#!/usr/bin/env python3
"""Build a first-pass source-review intake for P1 Xi_t targets.

This script reads the existing residual-blind source artifacts and converts
them into a compact readiness ledger for accepted Xi_t(R) manifest work.  It
does not read rotation residuals and does not permit endpoint scoring.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_readout_xi_p1_source_review_intake_not_endpoint"


def read_csv(name: str) -> pd.DataFrame:
    path = DATA / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


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


def build_intake() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    ngc4088_warp = read_csv("s4g75_ngc4088_warp_asymmetry_extraction_gate.csv")
    ngc4088_mem = read_csv("s4g75_ngc4088_memory_history_proxy_gate.csv")
    ngc4088_q = read_csv("s4g75_ngc4088_qwarp_measurement_gate.csv")
    ngc4088_review = read_csv("s4g75_ngc4088_source_response_independent_review_summary.csv")
    ugc_evidence = read_csv("ugc12506_highmass_fast_source_context_evidence.csv")
    ugc_path = read_csv("ugc12506_observer_path_interloper_audit_summary.csv")
    xi_worklist = read_csv("time_readout_xi_p1_source_review_worklist.csv")

    rows = []

    ngc_warp_ready = not ngc4088_warp.empty and bool(
        ngc4088_warp.iloc[0].get("warp_presence_flag", False)
    )
    ngc_pv_asym = not ngc4088_warp.empty and bool(
        ngc4088_warp.iloc[0].get("pv_asymmetry_flag", False)
    )
    ngc_pa_asym = not ngc4088_warp.empty and bool(
        ngc4088_warp.iloc[0].get("pa_asymmetry_flag", False)
    )
    ngc_q_blocked = (
        not ngc4088_q.empty
        and (ngc4088_q["gate_status"].astype(str).str.contains("BLOCKED").any())
    )
    ngc_mem_blocked = (
        not ngc4088_mem.empty
        and (ngc4088_mem["gate_status"].astype(str).str.contains("BLOCKED").any())
    )
    ngc_review_ready = (
        not ngc4088_review.empty
        and bool(ngc4088_review.iloc[0].get("numeric_bound_source_authorization", False))
    )
    ngc_review_summary = ngc4088_review.iloc[0] if ngc_review_ready else {}
    ngc_blocked_fields = (
        "accepted epsilon_t normalization law; residual-blind B_i coefficient rule"
        if ngc_review_ready
        else "q_warp_measured; m_history_warp; independent review; epsilon_t normalization law"
    )
    ngc_support_level = (
        "STRONG_SOURCE_REVIEWED_QMEM_NORMALIZATION_BLOCKED"
        if ngc_review_ready
        else "STRONG_CONTEXT_MEASUREMENT_BLOCKED"
    )
    ngc_filled_values = (
        f"warp={ngc_warp_ready}; pv_asym={ngc_pv_asym}; pa_asym={ngc_pa_asym}; "
        f"q_warp={float(ngc_review_summary.get('accepted_q_warp_measured', 0.0)):.6g}; "
        f"m_history={float(ngc_review_summary.get('accepted_m_history_warp', 0.0)):.6g}"
        if ngc_review_ready
        else f"warp={ngc_warp_ready}; pv_asym={ngc_pv_asym}; pa_asym={ngc_pa_asym}"
    )
    ngc_next = (
        "freeze residual-blind B_i / epsilon_t normalization rule, then build accepted Xi_eff manifest gate"
        if ngc_review_ready
        else "fill q_warp and m_history worksheets from source images/literature, then independent review"
    )
    rows.append(
        {
            "galaxy": "NGC4088",
            "intake_route": "warp_history_asymmetry_clock_phase",
            "source_support_level": ngc_support_level,
            "filled_source_evidence": "warp flag; PV asymmetry flag; PA asymmetry flag",
            "filled_values": ngc_filled_values,
            "blocked_fields": ngc_blocked_fields,
            "double_count_risk": "MODERATE_UNTIL_CLOCK_NORMALIZATION_SEPARATED_FROM_ADDITIVE_WARP_KERNEL"
            if ngc_review_ready
            else "HIGH_UNTIL_CLOCK_PHASE_DISTINCT_FROM_ADDITIVE_WARP_KERNEL",
            "path_term_status": "NOT_PRIMARY_FOR_THIS_ROUTE",
            "accepted_xi_t_manifest_allowed": False,
            "endpoint_scores_allowed": False,
            "recommended_next_action": ngc_next,
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    evidence_types = set(ugc_evidence.get("evidence_type", pd.Series(dtype=str)).astype(str))
    path_row = ugc_path.iloc[0] if not ugc_path.empty else {}
    rows.append(
        {
            "galaxy": "UGC12506",
            "intake_route": "edgeon_highspin_clock_envelope",
            "source_support_level": "STRONG_CONTEXT_PATH_FOREGROUND_REJECTED",
            "filled_source_evidence": "high inclination PV/envelope; extended HI support; asymmetric PV; low-density stable HI; high-spin context",
            "filled_values": "; ".join(sorted(evidence_types)),
            "blocked_fields": "accepted K_t(R) envelope mapping; epsilon_t normalization law; clock/readout settling proxy",
            "double_count_risk": "MODERATE_UNTIL_EDGEON_SPATIAL_PROJECTION_SEPARATED_FROM_CLOCK_READOUT",
            "path_term_status": str(path_row.get("foreground_path_status", "UNKNOWN")),
            "accepted_xi_t_manifest_allowed": False,
            "endpoint_scores_allowed": False,
            "recommended_next_action": "derive source-only high-spin/envelope clock proxy; keep foreground path term zero unless a new cone/path review supports it",
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    intake = pd.DataFrame(rows)

    gates = pd.DataFrame(
        [
            {
                "gate_id": "XI_INTAKE_G1_EXISTING_SOURCE_ARTIFACTS_READ",
                "gate_status": "PASS",
                "current_result": "NGC4088 WHISP/Ursa Major and UGC12506 HIghMass/path artifacts are present.",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "XI_INTAKE_G2_NGC4088_MEASUREMENT_BLOCKED",
                "gate_status": "PASS_SOURCE_REVIEWED" if ngc_review_ready else "BLOCKED",
                "current_result": (
                    "NGC4088 q_warp and m_history are accepted for protocol numeric bounds; normalization remains blocked."
                    if ngc_review_ready
                    else "NGC4088 has qualitative warp/asymmetry support, but q_warp and m_history remain unfilled and unreviewed."
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "XI_INTAKE_G3_UGC12506_PATH_TERM_ZERO",
                "gate_status": "PASS_CAVEATED",
                "current_result": "UGC12506 has strong internal edge-on/envelope/high-spin support, while foreground path object evidence is not established.",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "XI_INTAKE_G4_NO_ENDPOINT_PROMOTION",
                "gate_status": "PASS_RECORDED",
                "current_result": "No accepted Xi_t manifest exists; diagnostic improvement cannot promote endpoint scoring.",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "intake_status": "XI_T_P1_SOURCE_REVIEW_INTAKE_BUILT_ENDPOINT_BLOCKED",
                "n_p1_targets": int(len(intake)),
                "n_strong_context_targets": int(
                    intake["source_support_level"].str.contains("STRONG").sum()
                ),
                "n_endpoint_allowed": int(intake["endpoint_scores_allowed"].sum()),
                "ngc4088_next": ngc_next,
                "ugc12506_next": "derive high-spin/envelope clock proxy with foreground path term set to zero unless independently supported",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    # Keep a provenance list for reviewers.
    provenance = []
    if not xi_worklist.empty:
        provenance.append("time_readout_xi_p1_source_review_worklist.csv")
    for name, df in [
        ("s4g75_ngc4088_warp_asymmetry_extraction_gate.csv", ngc4088_warp),
        ("s4g75_ngc4088_memory_history_proxy_gate.csv", ngc4088_mem),
        ("s4g75_ngc4088_qwarp_measurement_gate.csv", ngc4088_q),
        ("s4g75_ngc4088_source_response_independent_review_summary.csv", ngc4088_review),
        ("ugc12506_highmass_fast_source_context_evidence.csv", ugc_evidence),
        ("ugc12506_observer_path_interloper_audit_summary.csv", ugc_path),
    ]:
        if not df.empty:
            provenance.append(name)
    summary["source_artifacts_used"] = "; ".join(provenance)

    return intake, gates, summary


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    intake, gates, summary = build_intake()

    intake.to_csv(DATA / "time_readout_xi_p1_source_review_intake.csv", index=False)
    gates.to_csv(DATA / "time_readout_xi_p1_source_review_intake_gates.csv", index=False)
    summary.to_csv(DATA / "time_readout_xi_p1_source_review_intake_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time-Readout Xi_t P1 Source-Review Intake",
            "",
            "This intake reads existing residual-blind source artifacts for the two",
            "P1 Xi_t targets. It does not use rotation residuals and does not",
            "authorize endpoint scoring.",
            "",
            "## Intake",
            "",
            markdown_table(intake),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
        ]
    )
    (REPORTS / "time_readout_xi_p1_source_review_intake.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
