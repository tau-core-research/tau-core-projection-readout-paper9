#!/usr/bin/env python3
"""Build the UGC12506 projection/history-enriched readout candidate gate.

This gate checks whether the current source record justifies treating UGC12506
as a projection/history-enriched readout candidate after the source-native
NFW-HSE replay leaves a large gap. It does not score an endpoint and does not
promote a foreground/path kernel without source-native path evidence.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_projection_history_readout_candidate_gate_not_endpoint"


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
    REPORTS.mkdir(parents=True, exist_ok=True)

    context = pd.read_csv(DATA / "ugc12506_highmass_fast_source_context_summary.csv").iloc[0]
    opi = pd.read_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv").iloc[0]
    decision = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_decision_gate_summary.csv").iloc[0]
    snfw = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_replay_summary.csv").iloc[0]

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "U12506_PH_E1_EDGEON_PROJECTION",
                "source_basis": "Hallenbeck2014 high-inclination PV/envelope method context",
                "source_status": str(opi["internal_projection_status"]),
                "bridge_interpretation": (
                    "strong observer/projection layer from edge-on disk integration"
                ),
                "supports_projection_history_candidate": True,
                "allowed_kernel_role": "internal_edgeon_projection_component",
                "forbidden_role": "none",
            },
            {
                "evidence_id": "U12506_PH_E2_EXTENDED_HI_HIGHSPIN",
                "source_basis": "R_HI about 58 kpc, diffuse stable H I, lambda_spin=0.15",
                "source_status": str(opi["envelope_support_status"]),
                "bridge_interpretation": (
                    "morphology-carried persistence/high-spin envelope support"
                ),
                "supports_projection_history_candidate": True,
                "allowed_kernel_role": "extended_hi_envelope_persistence_component",
                "forbidden_role": "endpoint-residual amplitude multiplier",
            },
            {
                "evidence_id": "U12506_PH_E3_ARM_ASYMMETRY",
                "source_basis": "approaching/receding sides differ in shape and detectable extent",
                "source_status": str(opi["arm_asymmetry_status"]),
                "bridge_interpretation": (
                    "caveated lopsided/projection-asymmetry history proxy"
                ),
                "supports_projection_history_candidate": True,
                "allowed_kernel_role": "secondary_asymmetry_component_after_source_weight_rule",
                "forbidden_role": "residual-selected radial sign or hand-tuned weight",
            },
            {
                "evidence_id": "U12506_PH_E4_IMAGE_INTERLOPER_OVERLAY",
                "source_basis": "star and higher-redshift galaxy overlap the optical image",
                "source_status": str(opi["image_interloper_status"]),
                "bridge_interpretation": (
                    "K_obs-to-K_readout mask/caveat, not a path-gravity term"
                ),
                "supports_projection_history_candidate": True,
                "allowed_kernel_role": "photometric_overlay_mask_or_caveat",
                "forbidden_role": "foreground/path gravity kernel",
            },
            {
                "evidence_id": "U12506_PH_E5_FOREGROUND_PATH_OBJECT",
                "source_basis": "no foreground massive object along the path is established",
                "source_status": str(opi["foreground_path_status"]),
                "bridge_interpretation": (
                    "full observer/path gravity component remains blocked"
                ),
                "supports_projection_history_candidate": False,
                "allowed_kernel_role": "none until catalogue cone/path search",
                "forbidden_role": "line-of-sight gravity kernel from current evidence",
            },
            {
                "evidence_id": "U12506_PH_E6_SOURCE_NATIVE_REPLAY_GAP",
                "source_basis": "source-native NFW-HSE improves branches but leaves large gap",
                "source_status": str(decision["decision_status"]),
                "bridge_interpretation": (
                    "gap motivates source acquisition for projection-history/carrier layers; "
                    "it does not itself define the component"
                ),
                "supports_projection_history_candidate": False,
                "allowed_kernel_role": "worklist_priority_signal_only",
                "forbidden_role": "using endpoint residual to choose label or amplitude",
            },
        ]
    )
    evidence["galaxy"] = GALAXY
    evidence["uses_vobs_or_residual"] = False
    evidence.loc[
        evidence["evidence_id"].eq("U12506_PH_E6_SOURCE_NATIVE_REPLAY_GAP"),
        "uses_vobs_or_residual",
    ] = True
    evidence["endpoint_scores_allowed"] = False
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence = evidence[
        [
            "galaxy",
            "evidence_id",
            "source_basis",
            "source_status",
            "bridge_interpretation",
            "supports_projection_history_candidate",
            "allowed_kernel_role",
            "forbidden_role",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_PH_G1_INTERNAL_PROJECTION",
                "gate_status": "PASS_STRONG",
                "evidence": "high inclination and PV/envelope method requirement",
                "decision": "include as projection-history candidate ingredient",
            },
            {
                "gate_id": "U12506_PH_G2_MORPHOLOGY_HISTORY_ENVELOPE",
                "gate_status": "PASS_STRONG",
                "evidence": "extended diffuse stable H I and high spin",
                "decision": "include as morphology-carried persistence candidate ingredient",
            },
            {
                "gate_id": "U12506_PH_G3_ASYMMETRY_HISTORY",
                "gate_status": "PASS_CAVEATED",
                "evidence": "approaching/receding asymmetry; radial rule not frozen",
                "decision": "allow only after source-side sign/weight rule",
            },
            {
                "gate_id": "U12506_PH_G4_FOREGROUND_PATH",
                "gate_status": "BLOCKED_NOT_ESTABLISHED",
                "evidence": "known galaxy interloper is higher-redshift; no foreground/path object established",
                "decision": "do not include full foreground/path gravity term",
            },
            {
                "gate_id": "U12506_PH_G5_ENDPOINT_BLINDNESS",
                "gate_status": "PASS_WITH_CAUTION",
                "evidence": "candidate support comes from source context; replay gap is worklist priority only",
                "decision": "no endpoint score allowed from this gate",
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
            "decision",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    status = (
        "UGC12506_PROJECTION_HISTORY_ENRICHED_READOUT_CANDIDATE_SOURCE_SUPPORTED_CAVEATED"
    )
    summary = pd.DataFrame(
        [
            {
                "candidate_status": status,
                "galaxy": GALAXY,
                "highmass_context_status": str(context["context_status"]),
                "source_native_nfw_hse_rmse_km_s": float(snfw["source_native_nfw_hse_rmse_km_s"]),
                "gap_to_prior_best_after_uncertainty_km_s": float(
                    decision["gap_to_prior_best_after_uncertainty_km_s"]
                ),
                "projection_history_formula_allowed": False,
                "why_not_allowed_yet": (
                    "asymmetry/history radial sign and weight are not source-frozen; "
                    "foreground/path gravity term is not established"
                ),
                "next_gate": (
                    "derive source-side projection-history component with no residual-selected "
                    "sign, weight, or amplitude"
                ),
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    formula_skeleton = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "skeleton_id": "UGC12506_PROJECTION_HISTORY_ENRICHED_SKELETON",
                "not_yet_frozen_formula": (
                    "v_readout^2 = v_carrier^2 + A_NFW_HSE K_NFW_HSE "
                    "+ A_PH K_projection_history"
                ),
                "candidate_component": (
                    "K_projection_history = combine(K_edgeon_disk_integration, "
                    "K_HI_envelope_persistence, K_arm_asymmetry_history)"
                ),
                "allowed_source_inputs": (
                    "inclination/PV envelope method, H I extent, high-spin context, "
                    "approaching/receding extent asymmetry, resolved H I/velocity-field morphology"
                ),
                "blocked_inputs": (
                    "foreground/path gravity without cone/path source; residual-selected sign; "
                    "endpoint-selected amplitude"
                ),
                "formula_freeze_status": "BLOCKED_SOURCE_SIDE_RULE_REQUIRED",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence.to_csv(DATA / "ugc12506_projection_history_readout_candidate_evidence.csv", index=False)
    gates.to_csv(DATA / "ugc12506_projection_history_readout_candidate_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_projection_history_readout_candidate_summary.csv", index=False)
    formula_skeleton.to_csv(DATA / "ugc12506_projection_history_readout_candidate_formula_skeleton.csv", index=False)

    report = [
        "# UGC12506 Projection/History-Enriched Readout Candidate Gate",
        "",
        "This gate tests whether the source record justifies treating UGC12506 as",
        "a projection/history-enriched readout candidate after the source-native",
        "NFW-HSE replay leaves a large gap. It does not score an endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Formula Skeleton",
        "",
        markdown_table(formula_skeleton),
        "",
        "## Claim Boundary",
        "",
        "The source record supports internal edge-on projection, extended H I",
        "envelope persistence, high spin, and caveated asymmetry/history context.",
        "It does not yet support a full foreground/path gravity kernel. The next",
        "honest step is a residual-blind source-side sign/weight rule for the",
        "projection-history component.",
        "",
    ]
    (REPORTS / "ugc12506_projection_history_readout_candidate_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(gates.to_string(index=False))


if __name__ == "__main__":
    main()
