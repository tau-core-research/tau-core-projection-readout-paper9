#!/usr/bin/env python3
"""Build the UGC12506 beta-closure transfer formula freeze gate.

The formula-freeze gate is the non-scoring bridge between accepted spin-route
prefreeze values and the separate scoring runner.  It writes the manifest file
that a future scoring script will consume.  In the current state the spin route
prefreeze is blocked, so the manifest is emitted with headers and zero rows.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint"


PREFREEZE_SUMMARY = DATA / "ugc12506_beta_closure_spin_route_prefreeze_summary.csv"
PREFREEZE_VALUES = DATA / "ugc12506_beta_closure_spin_route_prefreeze_values.csv"
HALO_FIELDS = DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv"
PRIORITY_GATE = DATA / "ugc12506_beta_closure_transfer_priority_gate.csv"
CARRIER_SUMMARY = DATA / "ugc12506_beta_closure_transfer_carrier_freeze_summary.csv"
CARRIER_MANIFEST = DATA / "ugc12506_beta_closure_transfer_carrier_manifest.csv"
SOURCE_PROXY_FIELDS = DATA / "ugc12506_beta_closure_source_declared_spin_proxy_fields.csv"

MANIFEST_COLUMNS = [
    "galaxy",
    "formula_id",
    "carrier_id",
    "carrier_expression",
    "selected_spin_normalization_route",
    "lambda_spin_value",
    "nfw_preference_load",
    "edgeon_load",
    "beta_cl_formula",
    "beta_cl_value",
    "source_value_artifacts",
    "formula_freeze_status",
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

    prefreeze_summary = pd.read_csv(PREFREEZE_SUMMARY).iloc[0]
    prefreeze_values = pd.read_csv(PREFREEZE_VALUES)
    halo = pd.read_csv(HALO_FIELDS)
    priority = pd.read_csv(PRIORITY_GATE)
    source_fields = pd.read_csv(SOURCE_PROXY_FIELDS)
    source_loads = source_fields[["galaxy", "edgeon_load"]].drop_duplicates("galaxy")
    carrier_summary = pd.read_csv(CARRIER_SUMMARY).iloc[0]
    carrier_manifest = pd.read_csv(CARRIER_MANIFEST)

    prefreeze_allowed = bool_value(
        prefreeze_summary["beta_cl_transfer_prefreeze_allowed"]
    )
    selected_route = str(prefreeze_summary["selected_spin_normalization_route"])
    route_values_exist = len(prefreeze_values) > 0

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BETA_FORMULA_1_SPIN_ROUTE_PREFREEZE_READY",
                "gate_status": "PASS" if prefreeze_allowed else "BLOCKED",
                "reason": str(prefreeze_summary["spin_route_prefreeze_status"]),
                "formula_manifest_rows_allowed": prefreeze_allowed,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_FORMULA_2_PREFREEZE_VALUES_EXIST",
                "gate_status": "PASS" if route_values_exist else "BLOCKED",
                "reason": f"n_prefreeze_values={len(prefreeze_values)}",
                "formula_manifest_rows_allowed": route_values_exist,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_FORMULA_3_HALO_FIELDS_READY",
                "gate_status": "PASS" if len(halo) > 0 else "BLOCKED",
                "reason": f"n_halo_field_rows={len(halo)}",
                "formula_manifest_rows_allowed": len(halo) > 0,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_FORMULA_4_PRIORITY_FIELDS_READY",
                "gate_status": "PASS" if len(priority) > 0 else "BLOCKED",
                "reason": f"n_priority_rows={len(priority)}",
                "formula_manifest_rows_allowed": len(priority) > 0,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_FORMULA_5_CARRIER_MANIFEST_READY",
                "gate_status": "PASS"
                if bool_value(carrier_summary["carrier_manifest_ready_for_scoring"])
                and len(carrier_manifest) > 0
                else "BLOCKED",
                "reason": f"carrier_status={carrier_summary['carrier_freeze_status']}; n_carriers={len(carrier_manifest)}",
                "formula_manifest_rows_allowed": bool_value(
                    carrier_summary["carrier_manifest_ready_for_scoring"]
                )
                and len(carrier_manifest) > 0,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    formula_ready = gates["gate_status"].eq("PASS").all()
    if formula_ready:
        joined = (
            prefreeze_values.merge(
                priority[["galaxy", "nfw_preference_load"]],
                on="galaxy",
                how="left",
            )
            .merge(source_loads, on="galaxy", how="left")
            .copy()
            .sort_values("galaxy")
        )
        joined["edgeon_load"] = joined["edgeon_load"].fillna(0.0)
        carrier_row = carrier_manifest.iloc[0]
        manifest = pd.DataFrame(
            {
                "galaxy": joined["galaxy"],
                "formula_id": "BETA_CL_TRANSFER_SOURCE_FROZEN",
                "carrier_id": carrier_row["carrier_id"],
                "carrier_expression": carrier_row["carrier_expression"],
                "selected_spin_normalization_route": joined[
                    "selected_spin_normalization_route"
                ],
                "lambda_spin_value": joined["lambda_spin_prefreeze_value"],
                "nfw_preference_load": joined["nfw_preference_load"],
                "edgeon_load": joined["edgeon_load"],
                "beta_cl_formula": (
                    "1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10"
                ),
                "beta_cl_value": (
                    1.0
                    + (joined["lambda_spin_prefreeze_value"] / 0.10)
                    * joined["nfw_preference_load"]
                    + joined["edgeon_load"]
                ),
                "source_value_artifacts": joined["source_artifact"],
                "formula_freeze_status": "SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING",
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    else:
        manifest = pd.DataFrame(columns=MANIFEST_COLUMNS)

    summary = pd.DataFrame(
        [
            {
                "formula_freeze_status": (
                    "U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_READY_FOR_SCORING_RUNNER"
                    if formula_ready
                    else "U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_BLOCKED_PREFREEZE_PENDING"
                ),
                "selected_spin_normalization_route": selected_route,
                "n_formula_manifest_rows": len(manifest),
                "n_pass_gates": int(gates["gate_status"].eq("PASS").sum()),
                "n_blocked_gates": int(gates["gate_status"].eq("BLOCKED").sum()),
                "formula_manifest_written": True,
                "formula_manifest_ready_for_scoring": formula_ready,
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "run_ugc12506_beta_closure_transfer_scoring"
                    if formula_ready
                    else "obtain_review_response_then_prefreeze_spin_route_values"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ugc12506_beta_closure_transfer_formula_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_beta_closure_transfer_formula_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_beta_closure_transfer_formula_freeze_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Transfer Formula Freeze Gate",
        "",
        "This gate creates the frozen transfer formula manifest consumed by the",
        "separate scoring runner. In the current state it writes only an empty",
        "manifest with headers because the spin-route prefreeze is still blocked.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Formula Manifest",
        "",
        markdown_table(manifest) if not manifest.empty else "No manifest rows are frozen.",
        "",
        "## Claim Boundary",
        "",
        "This gate does not read observed rotation curves and does not score. It",
        "only freezes the formula inputs that a later scoring runner may consume.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_formula_freeze_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
