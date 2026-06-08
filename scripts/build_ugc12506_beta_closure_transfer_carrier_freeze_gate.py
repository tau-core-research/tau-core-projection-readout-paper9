#!/usr/bin/env python3
"""Build the UGC12506 beta-closure transfer carrier-freeze gate.

The beta_cl transfer factor is not a complete scoring formula until the
velocity-squared carrier is source-frozen.  This gate records the admissible
carrier choices without selecting one from rotation residuals.  In the current
state no carrier route is independently accepted, so it writes an empty carrier
manifest and blocks downstream scoring.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint"
INTAKE_SUMMARY = DATA / "ugc12506_beta_closure_carrier_review_response_intake_summary.csv"


MANIFEST_COLUMNS = [
    "carrier_id",
    "carrier_status",
    "carrier_expression",
    "source_artifacts",
    "construction_used_vobs",
    "scoring_used_vobs",
    "endpoint_scores_allowed",
    "endpoint_validation_claim",
    "claim_boundary",
]


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


def bool_value(value: object) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    routes = pd.DataFrame(
        [
            {
                "carrier_id": "BARYONIC_050_FAST_PACKET",
                "route_status": "REVIEWABLE_NOT_ACCEPTED",
                "carrier_expression": "v_carrier^2 = v_baryon_050^2 from fast SPARC packet",
                "source_artifacts": "data/derived/fast_sparc_rotation_curve_packet_points.csv",
                "scientific_role": "endpoint-safe minimal stress carrier if independently accepted",
                "limitation": "not the same as the UGC12506 source-native NFW/HSE carrier",
                "review_obligation": "ACCEPT_AS_MINIMAL_TRANSFER_STRESS_CARRIER_OR_REJECT",
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "carrier_id": "LI2020_NFW_FIT_CARRIER",
                "route_status": "DIAGNOSTIC_OR_CONTROL_ONLY_NOT_ENDPOINT_SAFE",
                "carrier_expression": "NFW halo-fit curve reconstructed from Li et al. parameters",
                "source_artifacts": "data/external/literature/li2020_sparc_halo_catalog/table1_vizier.tsv",
                "scientific_role": "useful diagnostic control for NFW-preference transfer context",
                "limitation": "published halo parameters are rotation-curve fit products",
                "review_obligation": "KEEP_CONTROL_ONLY_UNLESS_ENDPOINT_LEAKAGE_POLICY_ACCEPTS",
                "construction_used_vobs": True,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "carrier_id": "SOURCE_NATIVE_NFW_HSE_TRANSFER_CARRIER",
                "route_status": "PREFERRED_BUT_CURRENTLY_MISSING",
                "carrier_expression": "source-native envelope/closure carrier analogous to UGC12506 NFW/HSE",
                "source_artifacts": "missing independent source-native transfer carrier manifests",
                "scientific_role": "closest scientific continuation of the UGC12506 beta_cl derivation",
                "limitation": "requires per-galaxy residual-blind source-native carrier construction",
                "review_obligation": "ACQUIRE_OR_DERIVE_SOURCE_NATIVE_TRANSFER_CARRIER",
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    selected_carrier = "PENDING_INDEPENDENT_REVIEW"
    carrier_allowed = False
    intake_status = "missing"
    if INTAKE_SUMMARY.exists():
        intake = pd.read_csv(INTAKE_SUMMARY).iloc[0]
        selected_carrier = str(intake.get("selected_carrier_id", selected_carrier))
        carrier_allowed = bool_value(intake.get("carrier_prefreeze_allowed", False))
        intake_status = str(intake.get("carrier_review_intake_status", "missing"))

    route = routes.loc[routes["carrier_id"].eq(selected_carrier)]
    route_supported = carrier_allowed and not route.empty and selected_carrier == "BARYONIC_050_FAST_PACKET"
    if route_supported:
        carrier_row = route.iloc[0]
        manifest = pd.DataFrame(
            [
                {
                    "carrier_id": selected_carrier,
                    "carrier_status": "SOURCE_FROZEN_CARRIER_READY_FOR_FORMULA_MANIFEST",
                    "carrier_expression": carrier_row["carrier_expression"],
                    "source_artifacts": carrier_row["source_artifacts"],
                    "construction_used_vobs": False,
                    "scoring_used_vobs": False,
                    "endpoint_scores_allowed": False,
                    "endpoint_validation_claim": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            ]
        )
    else:
        manifest = pd.DataFrame(columns=MANIFEST_COLUMNS)
    gates = pd.DataFrame(
        [
            {
                "gate_id": "BETA_CARRIER_1_ROUTE_ACCEPTED",
                "gate_status": "PASS" if carrier_allowed else "BLOCKED",
                "reason": intake_status
                if carrier_allowed
                else "no carrier route has been independently accepted",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_CARRIER_2_NO_ENDPOINT_LEAKAGE",
                "gate_status": "PASS" if route_supported else "BLOCKED",
                "reason": (
                    "accepted carrier is endpoint-blind BARYONIC_050_FAST_PACKET"
                    if route_supported
                    else "Li2020 NFW route is diagnostic/control-only unless leakage policy accepts it; baryonic route needs review"
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    summary = pd.DataFrame(
        [
            {
                "carrier_freeze_status": (
                    "U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST"
                    if route_supported
                    else "U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_BLOCKED_CARRIER_REVIEW_PENDING"
                ),
                "selected_carrier_id": selected_carrier,
                "n_carrier_routes": len(routes),
                "n_reviewable_not_accepted": int(
                    routes["route_status"].eq("REVIEWABLE_NOT_ACCEPTED").sum()
                ),
                "n_control_only_routes": int(
                    routes["route_status"].str.contains("CONTROL_ONLY", regex=False).sum()
                ),
                "n_preferred_missing_routes": int(
                    routes["route_status"].eq("PREFERRED_BUT_CURRENTLY_MISSING").sum()
                ),
                "n_frozen_carrier_rows": len(manifest),
                "carrier_manifest_ready_for_scoring": route_supported,
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "build_beta_cl_transfer_formula_manifest"
                    if route_supported
                    else "independent_review_accept_carrier_or_derive_source_native_transfer_carrier"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    routes.to_csv(
        DATA / "ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv",
        index=False,
    )
    manifest.to_csv(
        DATA / "ugc12506_beta_closure_transfer_carrier_manifest.csv",
        index=False,
    )
    gates.to_csv(
        DATA / "ugc12506_beta_closure_transfer_carrier_freeze_gates.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_carrier_freeze_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Transfer Carrier Freeze Gate",
        "",
        "This gate records that beta_cl is only an amplitude/closure factor until",
        "a velocity-squared carrier is source-frozen. It does not score and does",
        "not read observed rotation curves.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Carrier Routes",
        "",
        markdown_table(routes),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Frozen Carrier Manifest",
        "",
        "No carrier rows are frozen.",
        "",
        "## Claim Boundary",
        "",
        "A future scoring runner must read a carrier from the frozen manifest.",
        "It may not choose the carrier from endpoint residuals.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_carrier_freeze_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
