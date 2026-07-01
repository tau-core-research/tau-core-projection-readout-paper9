#!/usr/bin/env python3
"""Build a source-side preflight for UGC07151 as an expdisk+WVO analogue.

The purpose is to decide whether UGC07151 is the fastest clean prospective
analogue for the NGC4013 expdisk+WVO completion route. This script does not
score a rotation curve. It uses source-side catalogue/literature fields only.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ugc07151_expdisk_wvo_source_preflight_not_endpoint"


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
    queue = pd.read_csv(DATA / "fast_sparc_rotation_curve_packet_projection_queue.csv")
    priority = pd.read_csv(DATA / "projection_queue_fast_priority.csv")
    row = queue[queue["galaxy"] == "UGC07151"].iloc[0]
    prow = priority[priority["galaxy"] == "UGC07151"].iloc[0]

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "E1_SPARC_PACKET",
                "source": "SPARC fast packet / SPARC public database",
                "source_url": str(row["source_url"]),
                "secondary_source_url": str(row["secondary_source_url"]),
                "observable": "regular disk carrier and edge-on orientation",
                "value": (
                    f"T={row['hubble_type_T']}; Q={row['quality_Q']}; "
                    f"inclination={row['inclination_deg']} deg; "
                    f"RHI/Rdisk={row['rhi_kpc'] / row['rdisk_kpc']:.3f}; "
                    f"rotation_ref={row['rotation_curve_ref']}"
                ),
                "source_side_status": "ACCEPTED_CONTEXT",
                "interpretation": (
                    "Supports UGC07151 as a high-inclination regular disk "
                    "candidate with extended H I context. This does not by "
                    "itself prove WVO/warp support."
                ),
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "E2_EDGEON_TRUNCATION_WARP_CONTEXT",
                "source": "Truncations of stellar disks and warps of HI-layers in edge-on spiral galaxies",
                "source_url": "https://www.astro.rug.nl/~vdkruit/jea3/homepage/warppaper.pdf",
                "secondary_source_url": "https://arxiv.org/pdf/astro-ph/0702486",
                "observable": "UGC 7151 H I extent / truncation-warps context",
                "value": (
                    "Paper notes UGC 7151 among systems whose H I distributions "
                    "do not extend significantly farther than the optical image."
                ),
                "source_side_status": "NEGATIVE_OR_CAVEATED_WVO_SUPPORT",
                "interpretation": (
                    "This weakens the case for using UGC07151 as the first clean "
                    "expdisk+WVO analogue. It is better treated as an orientation/"
                    "truncation control unless independent WVO/onset evidence is found."
                ),
                "uses_vobs_or_residual": False,
            },
        ]
    )
    evidence["claim_boundary"] = CLAIM

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U7151_G1_REGULAR_EXPDISK_CARRIER",
                "gate_status": "PASS_SOURCE_CONTEXT",
                "reason": (
                    "SPARC/manifest context supports K_exponential_disk and no "
                    "bulge-dominated caveat is active in the queue."
                ),
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U7151_G2_EDGEON_ORIENTATION",
                "gate_status": "PASS_CAVEATED_SOURCE_CONTEXT",
                "reason": (
                    "Inclination is 90 deg in the SPARC packet. This promotes "
                    "observer/projection relevance, but not WVO by itself."
                ),
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U7151_G3_WVO_VERTICAL_WARP_ONSET",
                "gate_status": "BLOCKED_NEGATIVE_OR_INSUFFICIENT_SOURCE_SUPPORT",
                "reason": (
                    "The fastest located external source gives truncation/H I "
                    "extent context rather than clean vertical/warp/onset support."
                ),
                "endpoint_scores_allowed": False,
            },
            {
                "gate_id": "U7151_G4_EXPDISK_WVO_PROSPECTIVE_REPLAY",
                "gate_status": "BLOCKED_DO_NOT_SCORE_AS_WVO_ANALOGUE_YET",
                "reason": (
                    "A source-native WVO/onset observable is missing. The galaxy "
                    "can be retained as edge-on/truncation control or revisited "
                    "if independent WVO evidence is acquired."
                ),
                "endpoint_scores_allowed": False,
            },
        ]
    )
    gates["claim_boundary"] = CLAIM

    summary = pd.DataFrame(
        [
            {
                "galaxy": "UGC07151",
                "status": "EXPDISK_ORIENTATION_CONTEXT_PASS_WVO_BLOCKED",
                "formula_family": "K_exponential_disk",
                "candidate_route": "exponential_disk_plus_wvo",
                "fast_priority_rank": int(prow["fast_priority_rank"]),
                "priority_tier": str(prow["priority_tier"]),
                "inclination_deg": float(row["inclination_deg"]),
                "quality_Q": int(row["quality_Q"]),
                "rhi_over_rdisk": float(row["rhi_kpc"] / row["rdisk_kpc"]),
                "wvo_source_support": "blocked_or_negative",
                "recommended_role": "edge_on_truncation_control_or_source_reacquisition",
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "uses_vobs_or_residual_for_selection": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    evidence_path = DATA / "ugc07151_expdisk_wvo_source_preflight_evidence_v1.csv"
    gates_path = DATA / "ugc07151_expdisk_wvo_source_preflight_gates_v1.csv"
    summary_path = DATA / "ugc07151_expdisk_wvo_source_preflight_summary_v1.csv"
    report_path = REPORTS / "ugc07151_expdisk_wvo_source_preflight.md"

    evidence.to_csv(evidence_path, index=False)
    gates.to_csv(gates_path, index=False)
    summary.to_csv(summary_path, index=False)

    report = [
        "# UGC07151 Expdisk+WVO Source Preflight",
        "",
        "**Doc class:** source-side preflight audit",
        "",
        "**Reader role:** Paper 9 projection/mixed replay maintainer",
        "",
        "**Status:** `EXPDISK_ORIENTATION_CONTEXT_PASS_WVO_BLOCKED`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "This preflight tests the fastest proposed fresh analogue from the NGC4013",
        "expdisk+WVO selection audit. It does not run endpoint scoring. It asks only",
        "whether UGC07151 has enough residual-blind source support to freeze an",
        "exponential-disk carrier plus WVO route.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "UGC07151 passes the fast regular-disk/orientation context: it is a high",
        "inclination, quality-1 SPARC object with an exponential-disk family in the",
        "projection queue. That is enough to keep it as an observer/projection",
        "candidate.",
        "",
        "It does not yet pass the WVO-specific gate. The quickest source-side check",
        "found truncation/H I extent context rather than independent vertical-warp",
        "or onset support. Therefore the honest fast route is not to score it as",
        "an expdisk+WVO analogue now.",
        "",
        "## Verdict",
        "",
        "`UGC07151 is a useful edge-on/truncation control or source-reacquisition",
        "target, but it is not yet the clean fresh expdisk+WVO holdout.`",
        "",
        "## Next Finite Action",
        "",
        "Either locate an independent source-native WVO/onset/vertical-overlay",
        "observable for UGC07151, or move to the next candidate. If no such source",
        "exists, preserve UGC07151 as a negative/quiet control rather than forcing",
        "a WVO kernel.",
        "",
        "## Disallowed Claims",
        "",
        "- no endpoint score is run here",
        "- no validation claim is made here",
        "- edge-on orientation is not treated as WVO evidence by itself",
        "- the NGC4013 residual shape is not used to promote UGC07151",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
