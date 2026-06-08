#!/usr/bin/env python3
"""Build a source-side morphology adequacy review for NGC4088 and NGC4013.

This is a residual-blind review artifact.  It reads existing source-review
ledgers and summarizes whether the currently used morphology/readout family is
well supported, too coarse, or still blocked by missing independent morphology
fields.  It must not read observed rotation velocities or endpoint residuals.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "ngc4088_ngc4013_morphology_adequacy_review_not_endpoint"


def _read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return pd.read_csv(path)


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals = [str(row[c]).replace("\n", " ") for c in cols]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def build() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    ngc4088_lit = _read_csv(DATA / "ngc4088_source_review_literature_fields.csv")
    ngc4088_gates = _read_csv(DATA / "ngc4088_source_review_gate_decisions.csv")
    ngc4013_fields = _read_csv(
        DATA / "ngc4013_mixed_overlay_fresh_source_freeze_fields.csv"
    )
    ngc4013_replacement = _read_csv(
        DATA / "ngc4013_warp_vertical_overlay_replacement_label_source_fields.csv"
    )

    evidence_rows: list[dict[str, object]] = []

    for _, row in ngc4088_lit.iterrows():
        evidence_rows.append(
            {
                "galaxy": "NGC4088",
                "evidence_id": row["field_id"],
                "evidence_lane": "source_literature",
                "source_field": row["observable"],
                "source_value": row["value"],
                "status": row["support_status"],
                "source": row["source"],
                "source_ref": row["source_file"],
                "interpretation": row["promotion_use"],
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for _, row in ngc4088_gates.iterrows():
        evidence_rows.append(
            {
                "galaxy": "NGC4088",
                "evidence_id": row["gate_id"],
                "evidence_lane": "morphology_precision_gate",
                "source_field": row["needed_observable"],
                "source_value": row["current_value"],
                "status": row["decision"],
                "source": "existing_ngc4088_source_review_packet",
                "source_ref": "data/derived/ngc4088_source_review_gate_decisions.csv",
                "interpretation": row["reason"],
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for _, row in ngc4013_fields.iterrows():
        evidence_rows.append(
            {
                "galaxy": "NGC4013",
                "evidence_id": row["evidence_id"],
                "evidence_lane": row["evidence_lane"],
                "source_field": row["source_field"],
                "source_value": row["source_value"],
                "status": row["pass_status"],
                "source": "mixed_overlay_fresh_source_freeze_review",
                "source_ref": (
                    "data/derived/"
                    "ngc4013_mixed_overlay_fresh_source_freeze_fields.csv"
                ),
                "interpretation": row["interpretation"],
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    for _, row in ngc4013_replacement.iterrows():
        evidence_rows.append(
            {
                "galaxy": "NGC4013",
                "evidence_id": row["field_id"],
                "evidence_lane": "replacement_label_gate",
                "source_field": row["field_name"],
                "source_value": row["field_value"],
                "status": row["field_status"],
                "source": row["source"],
                "source_ref": (
                    "data/derived/"
                    "ngc4013_warp_vertical_overlay_replacement_label_source_fields.csv"
                ),
                "interpretation": "supports caveated replacement label review",
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    evidence = pd.DataFrame(evidence_rows)

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "current_or_proposed_readout": "K_warp_history_coupled",
                "broad_morphology_direction": "ACCEPTED_STRONG",
                "precision_status": "INSUFFICIENT_FOR_ACCEPTED_ENDPOINT_PRECISION",
                "adequacy_verdict": "GOOD_DIRECTION_BUT_NUMERIC_MORPHOLOGY_REVIEW_STILL_OPEN",
                "why": (
                    "Literature strongly supports distorted/asymmetric warped H I "
                    "disk plus companion/history context, so the warp/history "
                    "classification is not merely residual-driven.  However "
                    "x_warp, q_warp, memory/history, and epsilon_cross still need "
                    "independent acceptance before this becomes a source-complete "
                    "endpoint-grade morphology label."
                ),
                "main_support": (
                    "PA/inclination/H I size; strongly distorted disk; PV "
                    "asymmetry; asymmetric warp with side-dependent PA change; "
                    "near companion NGC4085"
                ),
                "main_blockers": (
                    "independent x_warp review; independent q_warp review; "
                    "accepted memory/history decomposition; epsilon_cross bound"
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "recommended_next_gate": (
                    "independent warp-onset/q-warp/memory review or source-native "
                    "H I product extraction; do not use score improvement as "
                    "classification evidence"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "current_or_proposed_readout": (
                    "K_warp_vertical_overlay_candidate / "
                    "mixed exponential-disk plus WVO"
                ),
                "broad_morphology_direction": "ACCEPTED_CAVEATED",
                "precision_status": "PROSPECTIVE_PROTOCOL_READY_NOT_RETROACTIVE_VALIDATION",
                "adequacy_verdict": "SUFFICIENT_FOR_CAVEATED_PROSPECTIVE_MIXED_OVERLAY_REPLAY",
                "why": (
                    "Source evidence supports a smooth/edge-on disk carrier plus "
                    "warp/flare/disk-halo vertical overlay and rejects the pure "
                    "compact lane.  Numeric and contextual source fields exist for "
                    "the overlay window, vertical kernel, extended component, and "
                    "lag context.  The earlier diagnostic score remains forbidden "
                    "as label evidence."
                ),
                "main_support": (
                    "S4G edge-disk component; disk scale; compact-lane rejection; "
                    "warp/flare/disk-halo pressure; line-of-sight warp onset; "
                    "h/R and extended component; radial lag context"
                ),
                "main_blockers": (
                    "not retroactive endpoint validation; lag-map digitization "
                    "would strengthen the kernel; future prospective scoring must "
                    "use the frozen protocol unchanged"
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "recommended_next_gate": (
                    "prospective replay/holdout lane or future source-selected "
                    "analogue; keep Xi_t overlay as a double-counting control unless "
                    "non-overlap evidence is added"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "gate_id": "MORPH_REVIEW_4088_1_BROAD_CLASS",
                "gate_status": "PASS",
                "evidence": "distorted asymmetric warped H I disk and companion/history context",
                "remaining_obligation": "none at broad class level",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "gate_id": "MORPH_REVIEW_4088_2_NUMERIC_PRECISION",
                "gate_status": "BLOCKED",
                "evidence": "x_warp, q_warp, and memory/history are not all independently accepted",
                "remaining_obligation": "independent morphology reviewer or source-native H I extraction",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4088",
                "gate_id": "MORPH_REVIEW_4088_3_NO_LEAKAGE",
                "gate_status": "PASS",
                "evidence": "review uses source ledgers and gates only; no vobs/residual fields",
                "remaining_obligation": "keep endpoint scores excluded from label promotion",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "MORPH_REVIEW_4013_1_COMPACT_REJECTION",
                "gate_status": "PASS",
                "evidence": "source review rejects pure compact lane",
                "remaining_obligation": "none at compact-rejection level",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "MORPH_REVIEW_4013_2_MIXED_OVERLAY_SUPPORT",
                "gate_status": "PASS_CAVEATED",
                "evidence": "smooth edge disk, warp/flare/disk-halo overlay, vertical component, lag context",
                "remaining_obligation": "lag-map digitization can strengthen but is not required for protocol",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "MORPH_REVIEW_4013_3_RETROACTIVE_VALIDATION",
                "gate_status": "BLOCKED",
                "evidence": "mixed lane developed after earlier diagnostic/control inspection",
                "remaining_obligation": "use only prospectively or on uninspected analogue/holdout",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "MORPH_REVIEW_4013_4_NO_LEAKAGE",
                "gate_status": "PASS",
                "evidence": "diagnostic RMSE is explicitly forbidden as label evidence",
                "remaining_obligation": "future scoring script must read frozen manifest unchanged",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary.to_csv(
        DATA / "ngc4088_ngc4013_morphology_adequacy_review_summary.csv",
        index=False,
    )
    evidence.to_csv(
        DATA / "ngc4088_ngc4013_morphology_adequacy_review_evidence.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ngc4088_ngc4013_morphology_adequacy_review_gates.csv",
        index=False,
    )

    report = "\n".join(
        [
            "# NGC4088 / NGC4013 Morphology Adequacy Review",
            "",
            f"Claim boundary: `{CLAIM_BOUNDARY}`",
            "",
            "This review asks whether the morphology/readout classifications used for",
            "NGC4088 and NGC4013 are source-side adequate.  It does not score rotation",
            "curves and it does not use observed-velocity residuals to choose labels.",
            "",
            "## Summary",
            "",
            _markdown_table(summary),
            "",
            "## Gates",
            "",
            _markdown_table(gates),
            "",
            "## Evidence Ledger",
            "",
            _markdown_table(evidence),
            "",
            "## Verdict",
            "",
            "- **NGC4088:** the broad warp/history-coupled classification is well",
            "  supported by source literature, but the numeric morphology precision is",
            "  still not endpoint-grade.  It should remain a strong but caveated",
            "  source-review case until independent warp-onset, q-warp, and",
            "  memory/history fields are accepted.",
            "- **NGC4013:** the pure compact classification is source-rejected, and the",
            "  mixed smooth-disk plus warp/vertical-overlay classification is source",
            "  supported enough for a caveated prospective protocol.  It should not be",
            "  counted as retroactive validation, and the extra Xi_t overlay should",
            "  remain a double-counting control unless new non-overlap evidence is",
            "  supplied.",
            "",
            "## Leakage Check",
            "",
            "All rows set `uses_vobs_or_residual=False`.  Existing diagnostic RMSE",
            "values are not read here and cannot promote a morphology label.",
            "",
        ]
    )
    (REPORTS / "ngc4088_ngc4013_morphology_adequacy_review.md").write_text(
        report, encoding="utf-8"
    )

    print("MORPHOLOGY_ADEQUACY_REVIEW_COMPLETE")
    print(summary[["galaxy", "adequacy_verdict", "precision_status"]].to_string(index=False))


if __name__ == "__main__":
    build()
