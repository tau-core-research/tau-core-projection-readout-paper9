#!/usr/bin/env python3
"""Audit UGC12506 observer/path/interloper evidence before kernel revision.

This source gate separates four logically different objects:

1. internal edge-on disk projection,
2. source-native extended H I envelope and arm asymmetry,
3. image-plane interlopers/overlays,
4. foreground/path objects along the light path.

It does not score the rotation curve and does not freeze a new endpoint kernel.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_observer_path_interloper_audit_source_gate_not_endpoint"


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

    source = pd.read_csv(DATA / "ugc12506_highmass_fast_source_context_source.csv").iloc[0]
    summary = pd.read_csv(DATA / "ugc12506_highmass_fast_source_context_summary.csv").iloc[0]
    preflight = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_summary.csv").iloc[0]

    if not bool(source["residual_blind"]):
        raise RuntimeError("UGC12506 source context is not residual-blind")
    if bool(summary["uses_vobs_or_residual_in_acquisition"]):
        raise RuntimeError("UGC12506 source acquisition used vobs/residual")
    if bool(preflight["uses_vobs_or_residual_in_preflight"]):
        raise RuntimeError("UGC12506 preflight used vobs/residual")

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "U12506_OPI_E1_EDGEON_INTERNAL_PROJECTION",
                "evidence_class": "internal_disk_projection",
                "source_id": str(source["source_id"]),
                "line_range": "206-225, 666-675",
                "source_statement": (
                    "UGC12506 has high inclination near 86 deg; the velocity field is a poor "
                    "rotation-velocity indicator and the PV/envelope method is required."
                ),
                "tau_core_readout_interpretation": (
                    "Strong observer/projection layer from line-of-sight integration through "
                    "the galaxy's own disk."
                ),
                "evidence_status": "SOURCE_SUPPORTED_STRONG",
                "kernel_role": "eligible_internal_projection_kernel_component",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_OPI_E2_HI_ENVELOPE_SUPPORT",
                "evidence_class": "source_native_morphology",
                "source_id": str(source["source_id"]),
                "line_range": "652-658, 800-811, 834-839",
                "source_statement": (
                    "The H I disk is traced beyond 60 kpc; UGC12506 is gas-rich, diffuse, "
                    "stable over most of the disk, and has high spin lambda=0.15."
                ),
                "tau_core_readout_interpretation": (
                    "Strong source-native extended-envelope support component; should not be "
                    "treated as a small context multiplier only."
                ),
                "evidence_status": "SOURCE_SUPPORTED_STRONG",
                "kernel_role": "eligible_envelope_support_kernel_component",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_OPI_E3_ARM_ASYMMETRY",
                "evidence_class": "source_native_asymmetry",
                "source_id": str(source["source_id"]),
                "line_range": "676-681",
                "source_statement": (
                    "The approaching and receding sides differ in shape and length; one side "
                    "is detectable to about 70 kpc and the other to about 50 kpc."
                ),
                "tau_core_readout_interpretation": (
                    "Source-supported lopsided/projection-asymmetry component; radial sign "
                    "and weighting still need a source-side rule."
                ),
                "evidence_status": "SOURCE_SUPPORTED_CAVEATED",
                "kernel_role": "eligible_asymmetry_kernel_component_with_caveat",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_OPI_E4_IMAGE_INTERLOPERS",
                "evidence_class": "image_plane_interloper",
                "source_id": str(source["source_id"]),
                "line_range": "659-661",
                "source_statement": (
                    "The optical image contains two interlopers not connected with UGC12506: "
                    "an eastern star and a southern higher-redshift galaxy intersecting the image."
                ),
                "tau_core_readout_interpretation": (
                    "Photometric/morphology-overlay caveat for K_obs -> K_readout; not by "
                    "itself a foreground path-gravity component."
                ),
                "evidence_status": "SOURCE_SUPPORTED_OVERLAY_CAVEAT",
                "kernel_role": "mask_or_caveat_component_not_gravity_kernel",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_OPI_E5_FOREGROUND_PATH_OBJECT",
                "evidence_class": "foreground_path",
                "source_id": str(source["source_id"]),
                "line_range": "659-661 plus source context",
                "source_statement": (
                    "The identified galaxy interloper is reported as higher redshift; no "
                    "foreground massive object along the UGC12506 light path is established."
                ),
                "tau_core_readout_interpretation": (
                    "Do not add a foreground/path lens-like kernel from this evidence. "
                    "A wider catalogue cone search would be required."
                ),
                "evidence_status": "NOT_ESTABLISHED",
                "kernel_role": "blocked_foreground_path_kernel_component",
                "uses_vobs_or_residual": False,
            },
        ]
    )
    evidence["galaxy"] = GALAXY
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence = evidence[
        [
            "galaxy",
            "evidence_id",
            "evidence_class",
            "source_id",
            "line_range",
            "source_statement",
            "tau_core_readout_interpretation",
            "evidence_status",
            "kernel_role",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_OPI_G1_INTERNAL_PROJECTION",
                "gate_status": "PASS_STRONG",
                "evidence": "i=86 deg and PV/envelope method required",
                "kernel_decision": "include_internal_edgeon_projection_component",
            },
            {
                "gate_id": "U12506_OPI_G2_ENVELOPE_SUPPORT",
                "gate_status": "PASS_STRONG",
                "evidence": "R_HI about 58 kpc, low-density stable H I, high spin lambda=0.15",
                "kernel_decision": "include_extended_hi_envelope_support_component",
            },
            {
                "gate_id": "U12506_OPI_G3_ARM_ASYMMETRY",
                "gate_status": "PASS_CAVEATED",
                "evidence": "approaching/receding arms differ in shape and detectable extent",
                "kernel_decision": "include_asymmetry_component_only_with_source_side_weight_caveat",
            },
            {
                "gate_id": "U12506_OPI_G4_IMAGE_INTERLOPER",
                "gate_status": "PASS_CAVEATED",
                "evidence": "star and higher-redshift galaxy interlopers in optical image",
                "kernel_decision": "treat_as_photometric_overlay_mask_or_label_caveat",
            },
            {
                "gate_id": "U12506_OPI_G5_FOREGROUND_PATH",
                "gate_status": "BLOCKED_NOT_ESTABLISHED",
                "evidence": "known galaxy interloper is higher redshift, not established foreground",
                "kernel_decision": "do_not_include_foreground_path_kernel_without_new_catalogue_search",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "kernel_decision",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    component_plan = pd.DataFrame(
        [
            {
                "component_id": "K_edgeon_disk_integration",
                "component_status": "SOURCE_SUPPORTED_NEXT_FORMULA_REQUIRED",
                "source_basis": "high inclination and PV/envelope tracing requirement",
                "allowed_role": "principal projection kernel",
                "blocked_role": "none",
            },
            {
                "component_id": "K_extended_hi_envelope",
                "component_status": "SOURCE_SUPPORTED_NEXT_FORMULA_REQUIRED",
                "source_basis": "large H I extent, diffuse stable gas, high spin",
                "allowed_role": "principal envelope support kernel",
                "blocked_role": "none",
            },
            {
                "component_id": "K_arm_asymmetry_extent",
                "component_status": "SOURCE_SUPPORTED_CAVEATED_NEXT_FORMULA_REQUIRED",
                "source_basis": "approaching/receding extent difference",
                "allowed_role": "secondary asymmetry kernel",
                "blocked_role": "residual-selected sign or radial weight",
            },
            {
                "component_id": "M_photometric_interloper_mask",
                "component_status": "SOURCE_SUPPORTED_CAVEAT_NOT_GRAVITY_KERNEL",
                "source_basis": "star and higher-redshift galaxy image-plane interlopers",
                "allowed_role": "K_obs -> K_readout mask/caveat",
                "blocked_role": "foreground/path gravity kernel",
            },
            {
                "component_id": "K_foreground_path_object",
                "component_status": "BLOCKED_NOT_ESTABLISHED",
                "source_basis": "no source-supported foreground object along path",
                "allowed_role": "none yet",
                "blocked_role": "full observer/path kernel contribution",
            },
        ]
    )
    component_plan["galaxy"] = GALAXY
    component_plan["claim_boundary"] = CLAIM_BOUNDARY
    component_plan = component_plan[
        [
            "galaxy",
            "component_id",
            "component_status",
            "source_basis",
            "allowed_role",
            "blocked_role",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "audit_status": "UGC12506_OBSERVER_PATH_INTERLOPER_AUDIT_COMPLETE_KERNEL_REVISION_REQUIRED",
                "galaxy": GALAXY,
                "internal_projection_status": "SOURCE_SUPPORTED_STRONG",
                "envelope_support_status": "SOURCE_SUPPORTED_STRONG",
                "arm_asymmetry_status": "SOURCE_SUPPORTED_CAVEATED",
                "image_interloper_status": "SOURCE_SUPPORTED_OVERLAY_CAVEAT",
                "foreground_path_status": "NOT_ESTABLISHED",
                "recommended_kernel_revision": (
                    "K_edgeon_disk_integration + K_extended_hi_envelope + "
                    "caveated K_arm_asymmetry_extent; photometric interloper as mask/caveat"
                ),
                "do_not_include": "foreground/path-object gravity kernel without new catalogue cone search",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": "derive_ugc12506_edgeon_envelope_asymmetry_formula_shell",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence.to_csv(DATA / "ugc12506_observer_path_interloper_audit_evidence.csv", index=False)
    gates.to_csv(DATA / "ugc12506_observer_path_interloper_audit_gates.csv", index=False)
    component_plan.to_csv(DATA / "ugc12506_observer_path_interloper_component_plan.csv", index=False)
    summary.to_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv", index=False)

    report = [
        "# UGC12506 Observer/Path/Interloper Audit Gate",
        "",
        "This source gate separates internal edge-on projection, source-native",
        "H I envelope support, arm asymmetry, image-plane interlopers, and",
        "foreground/path-object evidence. It does not score the rotation curve.",
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
        "## Component Plan",
        "",
        markdown_table(component_plan),
        "",
        "## Interpretation",
        "",
        "UGC12506 has strong source evidence for internal observer/projection",
        "effects from edge-on disk integration and for a large high-spin H I",
        "envelope. It also has image-plane interlopers, but the source states",
        "that they are not connected with UGC12506, and the identified galaxy is",
        "at higher redshift. Therefore the interloper evidence should be used as",
        "a photometric/morphology mask or caveat, not as a foreground/path gravity",
        "kernel unless a new catalogue cone search establishes a foreground/path",
        "object.",
        "",
    ]
    (REPORTS / "ugc12506_observer_path_interloper_audit_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
