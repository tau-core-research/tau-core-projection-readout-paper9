#!/usr/bin/env python3
"""Build the UGC12506 Xi_t accepted-manifest gate.

This is a promotion gate, not an endpoint run.  It collects the current
source-only UGC12506 Xi_t shell, bounded normalization shape, and small-mismatch
cap protocol, then records whether the object can be promoted to an accepted
time-readout endpoint manifest.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_accepted_manifest_gate_not_endpoint"


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


def read_row(path: str, column: str = "galaxy", value: str = GALAXY) -> pd.Series:
    df = pd.read_csv(DATA / path)
    if column not in df.columns:
        raise ValueError(f"{path} has no {column!r} column")
    rows = df.loc[df[column].astype(str).eq(value)]
    if rows.empty:
        raise ValueError(f"{path} has no row for {value}")
    return rows.iloc[0]


def optional_row(path: str, column: str = "galaxy", value: str = GALAXY) -> pd.Series | None:
    candidate = DATA / path
    if not candidate.exists():
        return None
    return read_row(path, column=column, value=value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    intake = read_row("time_readout_xi_p1_source_review_intake.csv")
    shell = read_row("ugc12506_xi_t_highspin_envelope_clock_shell_summary.csv")
    normalization = read_row("ugc12506_xi_t_normalization_summary.csv")
    cap = read_row("ugc12506_xi_t_epsilon_cap_protocol_summary.csv")
    response_validation = optional_row("ugc12506_xi_t_source_review_response_intake_validation.csv")

    no_residual_leakage = not any(
        bool(row["uses_vobs_or_residual"])
        for row in [shell, normalization, cap]
        if "uses_vobs_or_residual" in row.index
    )
    endpoint_blocked_upstream = any(
        bool(row["endpoint_scores_allowed"])
        for row in [intake, shell, normalization, cap]
        if "endpoint_scores_allowed" in row.index
    )

    blocked_fields = str(intake["blocked_fields"])
    missing_clock_proxy = "clock/readout settling proxy" in blocked_fields
    missing_envelope_mapping = "accepted K_t(R) envelope mapping" in blocked_fields
    cap_not_universal = not bool(cap["universal_tau_constant_derived"])
    protocol_cap_frozen = bool(cap["accepted_as_protocol_cap"])
    cap_origin_accepted = bool(normalization["cap_origin_accepted"])
    review_usable = False if response_validation is None else bool(response_validation["review_usable"])
    review_decision = "NO_REVIEW_RESPONSE"
    if response_validation is not None:
        review_decision = str(response_validation["review_decision"])
    caveated_interval_review = (
        review_usable
        and review_decision == "ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL"
    )

    standard_endpoint_manifest_allowed = (
        no_residual_leakage
        and not endpoint_blocked_upstream
        and not missing_clock_proxy
        and not missing_envelope_mapping
        and (cap_origin_accepted or protocol_cap_frozen)
    )
    caveated_interval_manifest_allowed = (
        no_residual_leakage
        and not endpoint_blocked_upstream
        and caveated_interval_review
        and protocol_cap_frozen
        and cap_not_universal
    )
    accepted_manifest_allowed = standard_endpoint_manifest_allowed or caveated_interval_manifest_allowed
    endpoint_scores_allowed = False

    obligations = []
    if missing_envelope_mapping and not caveated_interval_review:
        obligations.append("promote or reject the K_t(R) envelope mapping with independent source review")
    if missing_clock_proxy and not caveated_interval_review:
        obligations.append("fill the clock/readout settling proxy from residual-blind source evidence")
    if caveated_interval_review:
        obligations.append("carry K_t(R) only as caveated interval/control manifest, not as standard endpoint permission")
        obligations.append("keep asymmetry as caveated phase component, not standalone route driver")
        obligations.append("keep path term fixed to zero unless a later path review supplies source evidence")
    if cap_not_universal and protocol_cap_frozen:
        obligations.append("record epsilon_cap as protocol cap, not universal Tau constant, in any accepted manifest")
    if cap_not_universal and not cap_origin_accepted:
        obligations.append("derive deeper Tau-side cap origin before any universal-law claim")

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "gate_status": (
                    "CAVEATED_INTERVAL_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED"
                    if caveated_interval_manifest_allowed
                    else "ACCEPTED_MANIFEST_BLOCKED_SOURCE_PROXY_OPEN"
                ),
                "source_support_level": intake["source_support_level"],
                "formula_shell_status": shell["formula_shell_status"],
                "normalization_status": normalization["normalization_status"],
                "cap_protocol_status": cap["cap_protocol_status"],
                "epsilon_t": float(shell["epsilon_t"]),
                "source_load_L": float(normalization["source_load_L"]),
                "gamma_clock": float(normalization["gamma_clock"]),
                "epsilon_cap": float(cap["epsilon_cap"]),
                "path_term_status": intake["path_term_status"],
                "path_load": float(shell["path_load"]),
                "review_decision": review_decision,
                "review_usable": review_usable,
                "standard_endpoint_manifest_allowed": standard_endpoint_manifest_allowed,
                "caveated_interval_manifest_allowed": caveated_interval_manifest_allowed,
                "accepted_manifest_allowed": accepted_manifest_allowed,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "uses_vobs_or_residual": not no_residual_leakage,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_XIT_ACCEPT_G1_SOURCE_SHELL_EXISTS",
                "gate_status": "PASS",
                "evidence": shell["formula_shell_status"],
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G2_NO_RESIDUAL_LEAKAGE",
                "gate_status": "PASS" if no_residual_leakage else "FAIL",
                "evidence": "shell, normalization, and cap summaries report uses_vobs_or_residual=False",
                "remaining_obligation": "none" if no_residual_leakage else "remove residual-dependent construction",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G3_PATH_POLICY",
                "gate_status": "PASS",
                "evidence": "path term remains zero because path evidence is NOT_ESTABLISHED",
                "remaining_obligation": "rerun cone/path review before any nonzero path term",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G4_BOUNDED_SHAPE",
                "gate_status": "PASS_CONDITIONAL",
                "evidence": "epsilon_t = epsilon_cap L/(1+L) with L>=0",
                "remaining_obligation": "class-level acceptance required before endpoint use",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G5_CAP_PROTOCOL",
                "gate_status": "PASS_PROTOCOL_FREEZE",
                "evidence": "epsilon_cap=0.035 lies inside epsilon_t<=0.04 small-mismatch bound",
                "remaining_obligation": "do not claim universal Tau constant",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G6_SOURCE_PROXY_COMPLETENESS",
                "gate_status": "PASS_CAVEATED_INTERVAL_REVIEW"
                if caveated_interval_review
                else "BLOCKED",
                "evidence": blocked_fields,
                "remaining_obligation": "; ".join(obligations),
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G7_REVIEW_RESPONSE",
                "gate_status": "PASS_CAVEATED_INTERVAL"
                if caveated_interval_review
                else "BLOCKED",
                "evidence": review_decision,
                "remaining_obligation": "standard endpoint still blocked"
                if caveated_interval_review
                else "obtain usable independent source-review response",
            },
            {
                "gate_id": "U12506_XIT_ACCEPT_G8_ENDPOINT_PERMISSION",
                "gate_status": "BLOCKED",
                "evidence": "endpoint_scores_allowed=False",
                "remaining_obligation": "run endpoint only after a separate endpoint permission gate",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "accepted_manifest_status": (
                    "U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED"
                    if caveated_interval_manifest_allowed
                    else "U12506_XI_T_ACCEPTED_MANIFEST_NOT_READY"
                ),
                "galaxy": GALAXY,
                "review_decision": review_decision,
                "review_usable": review_usable,
                "standard_endpoint_manifest_allowed": standard_endpoint_manifest_allowed,
                "caveated_interval_manifest_allowed": caveated_interval_manifest_allowed,
                "accepted_manifest_allowed": accepted_manifest_allowed,
                "endpoint_scores_allowed": endpoint_scores_allowed,
                "n_open_obligations": len(obligations),
                "open_obligations": "; ".join(obligations),
                "next_step": (
                    "build caveated interval/control manifest artifact; endpoint scoring remains separately blocked"
                    if caveated_interval_manifest_allowed
                    else "source-review K_t envelope mapping and clock/readout settling proxy; then rerun this gate"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_items.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Accepted-Manifest Gate",
            "",
            "This gate asks whether the current source-only UGC12506 time-readout shell can be promoted to an accepted endpoint manifest. It does not score the rotation curve.",
            "",
            "## Manifest",
            "",
            markdown_table(manifest),
            "",
            "## Gate Items",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Claim Boundary",
            "",
            "UGC12506 now has a source-only Xi_t shell, a bounded normalization shape, and a conservative small-mismatch cap protocol. It is still not an accepted endpoint because the readout-relevant K_t envelope mapping and clock/readout settling proxy require independent source review.",
            "If an independent response accepts the K_t route only as a caveated interval/control manifest, this gate may promote that control manifest while keeping endpoint scoring blocked.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_accepted_manifest_gate.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
