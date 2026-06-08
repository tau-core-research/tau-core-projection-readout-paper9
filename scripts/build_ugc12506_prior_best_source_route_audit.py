#!/usr/bin/env python3
"""Audit why the prior diagnostic Tau-best branch is strong for UGC12506.

The previous atlas diagnostic reports `best_family=K_compact_finite` for
UGC12506.  This script does not promote that family.  Instead it asks whether
source evidence supports a compact/cored route, or whether the diagnostic is
better interpreted as pressure toward a different source-side readout, such as
NFW-like rapid-rise / halo-concentration / high-spin support.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_prior_best_source_route_audit_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.6g}")
        else:
            display[column] = display[column].astype(str)
    lines = [
        "| " + " | ".join(display.columns) + " |",
        "| " + " | ".join(["---"] * len(display.columns) + [""])[:-2] + " |",
    ]
    # fix above line if column formatting would be malformed
    lines[1] = "| " + " | ".join(["---"] * len(display.columns)) + " |"
    for _, row in display.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(DATA / "multigalaxy_fit_inspection_scores.csv")
    u = scores.loc[scores["galaxy"].eq(GALAXY)].copy()
    if u.empty:
        raise ValueError("Missing UGC12506 prior diagnostic scores")
    best = u.loc[u["model_id"].eq("TAU_BEST_FAMILY")].iloc[0]
    if bool(best["validation_claim_allowed"]):
        raise RuntimeError("Prior diagnostic unexpectedly claims validation")

    evidence = pd.DataFrame(
        [
            {
                "evidence_id": "U12506_PB_E1_PRIOR_DIAGNOSTIC",
                "evidence_class": "diagnostic_score_reference",
                "source": "multigalaxy_fit_inspection_scores.csv",
                "statement": (
                    "Prior diagnostic TAU_BEST_FAMILY has RMSE 37.36 km/s and reports "
                    "best_family=K_compact_finite, but validation_claim_allowed=False."
                ),
                "route_interpretation": (
                    "Useful signal about missing readout shape, not a source-accepted "
                    "morphology label."
                ),
                "status": "DIAGNOSTIC_ONLY_NOT_SOURCE_LABEL",
                "uses_vobs_or_residual": True,
            },
            {
                "evidence_id": "U12506_PB_E2_NFW_PREFERENCE",
                "evidence_class": "source_halo_fit_context",
                "source": "Hallenbeck2014 lines 730-738",
                "statement": (
                    "UGC12506 has a very significant preference for the NFW halo model "
                    "over the pseudo-isothermal model in the source discussion."
                ),
                "route_interpretation": (
                    "Source pressure points toward rapid-rise / NFW-like halo-concentration "
                    "readout, not toward a cored compact-support interpretation."
                ),
                "status": "SOURCE_SUPPORTED_NFW_LIKE_ROUTE",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_PB_E3_FAST_RISE",
                "evidence_class": "source_rotation_shape_context",
                "source": "Hallenbeck2014 lines 679-681, 736-738",
                "statement": (
                    "The rotation curve rises quickly to about 250 km/s, and the source "
                    "notes this is unlike the slowly rising curves expected for many LSBs."
                ),
                "route_interpretation": (
                    "Supports a steep inner/halo-concentration shell rather than simply "
                    "amplifying the outer envelope."
                ),
                "status": "SOURCE_SUPPORTED_RAPID_RISE_ROUTE",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_PB_E4_HIGH_SPIN",
                "evidence_class": "source_spin_context",
                "source": "Hallenbeck2014 lines 800-811, 834-839",
                "statement": (
                    "UGC12506 has high spin lambda=0.15 and a diffuse stable H I reservoir."
                ),
                "route_interpretation": (
                    "Supports coupling the rapid-rise shell to high-spin envelope support "
                    "rather than using a generic compact family."
                ),
                "status": "SOURCE_SUPPORTED_HIGH_SPIN_ROUTE",
                "uses_vobs_or_residual": False,
            },
            {
                "evidence_id": "U12506_PB_E5_COMPACT_CORED_ROUTE",
                "evidence_class": "negative_source_route",
                "source": "Hallenbeck2014 lines 326-344, 730-738",
                "statement": (
                    "The source defines a pseudo-isothermal cored halo option, but UGC12506 "
                    "is reported to prefer NFW significantly."
                ),
                "route_interpretation": (
                    "Do not promote K_compact_finite as source-native for UGC12506 from "
                    "the current evidence."
                ),
                "status": "COMPACT_CORED_ROUTE_NOT_SOURCE_PROMOTED",
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
            "source",
            "statement",
            "route_interpretation",
            "status",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_PB_G1_PRIOR_DIAGNOSTIC_NOT_LABEL",
                "gate_status": "PASS",
                "decision": "preserve prior K_compact_finite as diagnostic only",
                "evidence": "validation_claim_allowed=False",
            },
            {
                "gate_id": "U12506_PB_G2_COMPACT_SOURCE_PROMOTION",
                "gate_status": "BLOCKED",
                "decision": "do not promote compact/cored source label",
                "evidence": "source reports significant NFW preference for UGC12506",
            },
            {
                "gate_id": "U12506_PB_G3_NFW_RAPID_RISE_ROUTE",
                "gate_status": "PASS_CANDIDATE",
                "decision": "open source-side NFW-like rapid-rise / concentration shell",
                "evidence": "NFW preference plus rapid rotation-curve rise",
            },
            {
                "gate_id": "U12506_PB_G4_HIGH_SPIN_COUPLING",
                "gate_status": "PASS_CANDIDATE",
                "decision": "couple rapid-rise shell to high-spin extended-envelope route",
                "evidence": "lambda=0.15 and stable diffuse H I reservoir",
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
            "decision",
            "evidence",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    route_plan = pd.DataFrame(
        [
            {
                "route_id": "UGC12506_ROUTE_A_SOURCE_NATIVE_NFW_RAPID_RISE",
                "route_status": "NEXT_FORMULA_SHELL_CANDIDATE",
                "formula_family_hint": "K_nfw_like_rapid_rise_highspin_envelope",
                "source_basis": "NFW preference, rapid rise, high spin, extended H I envelope",
                "not_allowed": "using prior K_compact_finite score as source label",
            },
            {
                "route_id": "UGC12506_ROUTE_B_COMPACT_FINITE",
                "route_status": "BLOCKED_AS_SOURCE_LABEL_DIAGNOSTIC_ONLY",
                "formula_family_hint": "K_compact_finite",
                "source_basis": "diagnostic score only; source prefers NFW over pseudo-isothermal",
                "not_allowed": "promotion without independent compact/cored source evidence",
            },
        ]
    )
    route_plan["galaxy"] = GALAXY
    route_plan["claim_boundary"] = CLAIM_BOUNDARY
    route_plan = route_plan[
        [
            "galaxy",
            "route_id",
            "route_status",
            "formula_family_hint",
            "source_basis",
            "not_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "audit_status": "UGC12506_PRIOR_BEST_AUDIT_COMPLETE_NFW_RAPID_RISE_ROUTE_OPENED",
                "galaxy": GALAXY,
                "prior_best_family": str(best["best_family"]),
                "prior_best_rmse_km_s": float(best["rmse_kms"]),
                "compact_source_promotion": "BLOCKED_DIAGNOSTIC_ONLY",
                "nfw_rapid_rise_route": "SOURCE_SUPPORTED_CANDIDATE",
                "highspin_envelope_coupling": "SOURCE_SUPPORTED_CANDIDATE",
                "endpoint_scores_allowed": False,
                "next_gate": "derive_ugc12506_nfw_like_rapid_rise_highspin_envelope_shell",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence.to_csv(DATA / "ugc12506_prior_best_source_route_audit_evidence.csv", index=False)
    gates.to_csv(DATA / "ugc12506_prior_best_source_route_audit_gates.csv", index=False)
    route_plan.to_csv(DATA / "ugc12506_prior_best_source_route_plan.csv", index=False)
    summary.to_csv(DATA / "ugc12506_prior_best_source_route_audit_summary.csv", index=False)

    report = [
        "# UGC12506 Prior-Best Source Route Audit",
        "",
        "The previous diagnostic Tau-best row is useful, but it cannot promote",
        "a source label. This audit checks whether its K_compact_finite hint is",
        "source-supported for UGC12506.",
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
        "## Route Plan",
        "",
        markdown_table(route_plan),
        "",
        "## Interpretation",
        "",
        "The current source evidence does not support promoting the prior",
        "K_compact_finite diagnostic as an accepted UGC12506 morphology/readout",
        "label.  Instead, Hallenbeck et al. report a significant NFW preference,",
        "rapid rotation-curve rise, high spin, and an extended H I envelope.  The",
        "claim-safe next route is therefore an NFW-like rapid-rise/high-spin",
        "envelope shell.",
        "",
    ]
    (REPORTS / "ugc12506_prior_best_source_route_audit.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
