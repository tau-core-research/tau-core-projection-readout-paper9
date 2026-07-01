#!/usr/bin/env python3
"""Consolidate NGC7331 exact-transfer readiness after q_warp review.

This is not an endpoint scorer. It reads source-side THINGS/q_warp/sign
summaries and determines whether Paper9 can advance from "exact transfer
blocked" to "formula-freeze preparation allowed with carried intervals".
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ngc7331_exact_transfer_readiness_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals: list[str] = []
        for col in cols:
            value = row[col]
            if pd.isna(value):
                vals.append("")
            elif isinstance(value, float):
                vals.append(f"{value:.6g}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    first = pd.read_csv(DATA / "ngc7331_things_qwarp_first_pass_summary.csv").iloc[0]
    sensitivity = pd.read_csv(
        DATA / "ngc7331_things_qwarp_measurement_sensitivity_summary.csv"
    ).iloc[0]
    sign_cross = pd.read_csv(DATA / "ngc7331_things_mom1_sign_cross_summary.csv").iloc[0]
    review = pd.read_csv(DATA / "ngc7331_qwarp_source_only_review_response_summary.csv").iloc[0]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "status": "EXACT_TRANSFER_FORMULA_FREEZE_PREP_READY_INTERVAL_CARRIED_ENDPOINT_BLOCKED",
                "q_warp_interval": str(review["q_warp_interval"]),
                "q_centroid_range": (
                    f"{float(sensitivity['q_centroid_mean_min']):.6f}.."
                    f"{float(sensitivity['q_centroid_mean_max']):.6f}"
                ),
                "q_envelope_range": (
                    f"{float(sensitivity['q_envelope_p80_mean_min']):.6f}.."
                    f"{float(sensitivity['q_envelope_p80_mean_max']):.6f}"
                ),
                "epsilon_cross_candidate_bound": float(
                    review["epsilon_cross_candidate_bound"]
                ),
                "mom1_sign_context_status": str(sign_cross["mom1_sign_cross_status"]),
                "qwarp_first_pass": float(first["q_warp_first_pass"]),
                "formula_freeze_prep_allowed": bool(
                    review["formula_freeze_allowed_after_review"]
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    fields = pd.DataFrame(
        [
            {
                "field": "q_warp",
                "field_status": "CARRIED_INTERVAL_ACCEPTED_FOR_FREEZE_PREP",
                "accepted_form": str(review["q_warp_interval"]),
                "source_basis": (
                    "THINGS MOM0 centroid and envelope observables; interval carried "
                    "because the source-native observables disagree by design choice."
                ),
                "remaining_obligation": "formula freeze must propagate interval, not collapse it to one fitted value",
            },
            {
                "field": "sigma_warp_sign",
                "field_status": "CONTEXT_AVAILABLE_SIGN_RULE_STILL_FORMULA_LEVEL",
                "accepted_form": "MOM1 consistent receding-side orientation carried to formula freeze",
                "source_basis": "THINGS MOM1 sign/cross review",
                "remaining_obligation": "freeze added-readout vs attenuation convention explicitly",
            },
            {
                "field": "epsilon_cross",
                "field_status": "CONSERVATIVE_BOUND_CARRIED",
                "accepted_form": str(review["epsilon_cross_candidate_bound"]),
                "source_basis": "MOM1 PA/velocity/q-observable/context terms",
                "remaining_obligation": "treat as caveated bound, not validation",
            },
        ]
    )
    fields["claim_boundary"] = CLAIM

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_ETR1_Q_INTERVAL",
                "gate_status": "PASS_INTERVAL_CARRIED",
                "evidence": f"q_warp_interval={review['q_warp_interval']}",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "N7331_ETR2_SIGN_CONTEXT",
                "gate_status": "PASS_CONTEXT_FORMULA_RULE_REQUIRED",
                "evidence": "MOM1 receding-side orientation is consistent; formula sign convention still must be explicit",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "N7331_ETR3_EPSILON_BOUND",
                "gate_status": "PASS_CAVEATED_BOUND_CARRIED",
                "evidence": f"epsilon_cross_candidate_bound={review['epsilon_cross_candidate_bound']}",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "N7331_ETR4_FREEZE_PREP",
                "gate_status": "PASS_FORMULA_FREEZE_PREP_ALLOWED",
                "evidence": "source-only review allows formula-freeze preparation after carrying interval",
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "N7331_ETR5_ENDPOINT_SCORING",
                "gate_status": "BLOCKED_UNTIL_FORMULA_FREEZE_MANIFEST_EXISTS",
                "evidence": "no exact-transfer formula-freeze manifest has been built in Paper9",
                "endpoint_scores_allowed": False,
            },
        ]
    )
    gates["claim_boundary"] = CLAIM

    summary_path = DATA / "ngc7331_exact_transfer_readiness_summary_v1.csv"
    fields_path = DATA / "ngc7331_exact_transfer_readiness_fields_v1.csv"
    gates_path = DATA / "ngc7331_exact_transfer_readiness_gates_v1.csv"
    report_path = REPORTS / "ngc7331_exact_transfer_readiness_audit.md"

    summary.to_csv(summary_path, index=False)
    fields.to_csv(fields_path, index=False)
    gates.to_csv(gates_path, index=False)

    report = [
        "# NGC7331 Exact-Transfer Readiness Audit",
        "",
        "**Doc class:** source-side formula-freeze readiness audit",
        "",
        "**Reader role:** Paper 9 exact-transfer maintainer",
        "",
        "**Status:** `EXACT_TRANSFER_FORMULA_FREEZE_PREP_READY_INTERVAL_CARRIED_ENDPOINT_BLOCKED`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "This audit checks whether the NGC7331 exact-transfer blocker has moved",
        "after the source-only q_warp review response. It does not run endpoint",
        "scores and does not choose a curve-saving value.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Field Ledger",
        "",
        markdown_table(fields),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "The old blocker was too coarse: exact transfer was not simply blocked by",
        "absence of q_warp. A source-native interval now exists and may be carried",
        "into formula-freeze preparation. The MOM1 route also provides consistent",
        "orientation context and a conservative epsilon_cross candidate bound.",
        "",
        "However, this is still not endpoint-ready. The next object must be a frozen",
        "exact-transfer formula manifest that propagates the q_warp interval and",
        "states the sign convention explicitly. Endpoint scoring remains blocked",
        "until that manifest exists.",
        "",
        "## Allowed Claim",
        "",
        "`NGC7331 exact-transfer has advanced from measurement-missing to",
        "formula-freeze-preparation ready with carried source intervals, while",
        "endpoint scoring remains blocked.`",
        "",
        "## Disallowed Claims",
        "",
        "- no unique q_warp value is selected",
        "- no endpoint score is run",
        "- no population validation is claimed",
        "- no residual or observed rotation data are used in this audit",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
