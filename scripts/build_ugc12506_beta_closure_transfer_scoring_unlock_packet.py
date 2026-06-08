#!/usr/bin/env python3
"""Build the UGC12506 beta-closure transfer scoring unlock packet.

This packet is the final pre-scoring handoff.  It does not accept a review
decision and does not create active response files.  It writes example-only
CSV rows and a requirements ledger so an independent reviewer can provide the
two active response files needed by the existing intake scripts:

* ugc12506_beta_closure_spin_proxy_review_response.csv
* ugc12506_beta_closure_carrier_review_response.csv

The packet is deliberately non-scoring and does not read observed rotation
curves or residuals.
"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
REVIEW_BUNDLES = ROOT / "review_bundles"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_scoring_unlock_packet_not_endpoint"

DRY_RUN_SCENARIOS = DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv"
SPIN_ACTIVE_RESPONSE = DATA / "ugc12506_beta_closure_spin_proxy_review_response.csv"
CARRIER_ACTIVE_RESPONSE = DATA / "ugc12506_beta_closure_carrier_review_response.csv"

SPIN_EXPOSURE_EXAMPLE = DATA / "ugc12506_beta_closure_spin_proxy_review_response_example_only_exposure_proxy.csv"
SPIN_BULLOCK_EXAMPLE = DATA / "ugc12506_beta_closure_spin_proxy_review_response_example_only_bullock_conversion.csv"
CARRIER_EXAMPLE = DATA / "ugc12506_beta_closure_carrier_review_response_example_only_baryonic_stress.csv"
ZIP_PATH = REVIEW_BUNDLES / "ugc12506_beta_closure_transfer_scoring_unlock_packet.zip"


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


def spin_example(route: str, scenario_id: str) -> pd.DataFrame:
    weight_decision = (
        "ACCEPT_EXPOSURE_RULE"
        if route == "EXPOSURE_PROXY"
        else "ACCEPT_BULLOCK_CONVERSION"
    )
    return pd.DataFrame(
        [
            {
                "packet_id": "U12506_BETA_SPIN_PROXY_REVIEW_PACKET_V1",
                "reviewer_or_method_id": "EXAMPLE_ONLY_NOT_A_REVIEW_DECISION",
                "review_timestamp_utc": "EXAMPLE_ONLY",
                "source_fields_decision": "ACCEPT_SOURCE_FIELDS",
                "weight_rule_decision": weight_decision,
                "selected_spin_normalization_route": route,
                "definition_boundary_decision": "ACCEPT_CONTEXT_ONLY",
                "transfer_scope_decision": "ACCEPT_TARGET_SET",
                "accepted_targets": "all dry-run scenario targets",
                "rejected_targets": "none",
                "required_changes": "independent reviewer must replace this example row",
                "review_rationale": (
                    f"example-only row for {scenario_id}; not active unless an independent reviewer writes the active response path"
                ),
                "source_inputs_used": (
                    "review packet source fields only; no observed rotation residuals"
                ),
                "forbidden_inputs_used": "False",
                "proxy_promotion_allowed_after_review": False,
                "beta_cl_replay_allowed_after_review": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def carrier_example() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "packet_id": "U12506_BETA_CARRIER_REVIEW_PACKET_V1",
                "reviewer_or_method_id": "EXAMPLE_ONLY_NOT_A_REVIEW_DECISION",
                "review_timestamp_utc": "EXAMPLE_ONLY",
                "carrier_route_decision": "ACCEPT_BARYONIC_STRESS_CARRIER",
                "selected_carrier_id": "BARYONIC_050_FAST_PACKET",
                "li2020_policy_decision": "KEEP_LI2020_CONTROL_ONLY",
                "accepted_targets": "all dry-run scenario targets",
                "rejected_targets": "none",
                "required_changes": "independent reviewer must replace this example row",
                "review_rationale": (
                    "example-only row for minimal baryonic stress carrier; not active unless an independent reviewer writes the active response path"
                ),
                "source_inputs_used": (
                    "fast SPARC baryonic carrier columns only; no observed rotation residuals for carrier selection"
                ),
                "forbidden_inputs_used": "False",
                "carrier_prefreeze_allowed_after_review": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    REVIEW_BUNDLES.mkdir(parents=True, exist_ok=True)

    scenarios = pd.read_csv(DRY_RUN_SCENARIOS)
    ready_scenarios = scenarios.loc[
        scenarios["contract_ready_if_reviews_accept"].astype(bool)
    ].copy()

    exposure = ready_scenarios.loc[
        ready_scenarios["selected_spin_normalization_route"].eq("EXPOSURE_PROXY")
    ].iloc[0]
    bullock = ready_scenarios.loc[
        ready_scenarios["selected_spin_normalization_route"].eq("BULLOCK_DISK_CONVERSION")
    ].iloc[0]

    spin_exposure = spin_example(
        "EXPOSURE_PROXY",
        str(exposure["dry_run_scenario_id"]),
    )
    spin_bullock = spin_example(
        "BULLOCK_DISK_CONVERSION",
        str(bullock["dry_run_scenario_id"]),
    )
    carrier = carrier_example()

    spin_exposure.to_csv(SPIN_EXPOSURE_EXAMPLE, index=False)
    spin_bullock.to_csv(SPIN_BULLOCK_EXAMPLE, index=False)
    carrier.to_csv(CARRIER_EXAMPLE, index=False)

    requirements = pd.DataFrame(
        [
            {
                "required_active_response": str(SPIN_ACTIVE_RESPONSE.relative_to(ROOT)),
                "response_type": "spin_route_review",
                "accepted_values": (
                    "source_fields_decision=ACCEPT_SOURCE_FIELDS; "
                    "weight_rule_decision in {ACCEPT_EXPOSURE_RULE,ACCEPT_BULLOCK_CONVERSION}; "
                    "selected_spin_normalization_route in {EXPOSURE_PROXY,BULLOCK_DISK_CONVERSION}; "
                    "definition_boundary_decision=ACCEPT_CONTEXT_ONLY; "
                    "transfer_scope_decision=ACCEPT_TARGET_SET; "
                    "forbidden_inputs_used=False"
                ),
                "example_only_files": (
                    f"{SPIN_EXPOSURE_EXAMPLE.relative_to(ROOT)};"
                    f"{SPIN_BULLOCK_EXAMPLE.relative_to(ROOT)}"
                ),
                "active_file_exists_now": SPIN_ACTIVE_RESPONSE.exists(),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "required_active_response": str(CARRIER_ACTIVE_RESPONSE.relative_to(ROOT)),
                "response_type": "carrier_review",
                "accepted_values": (
                    "carrier_route_decision=ACCEPT_BARYONIC_STRESS_CARRIER; "
                    "selected_carrier_id=BARYONIC_050_FAST_PACKET; "
                    "li2020_policy_decision=KEEP_LI2020_CONTROL_ONLY; "
                    "forbidden_inputs_used=False; endpoint_scores_allowed=False; "
                    "uses_vobs_or_residual=False"
                ),
                "example_only_files": str(CARRIER_EXAMPLE.relative_to(ROOT)),
                "active_file_exists_now": CARRIER_ACTIVE_RESPONSE.exists(),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "unlock_packet_status": (
                    "U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING"
                ),
                "n_contract_ready_scenarios": len(ready_scenarios),
                "n_required_active_response_files": len(requirements),
                "n_active_response_files_present": int(
                    requirements["active_file_exists_now"].sum()
                ),
                "n_example_only_response_files": 3,
                "zip_path": str(ZIP_PATH.relative_to(ROOT)),
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "external_reviewer_writes_active_response_files_then_run_intakes"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    requirements.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_unlock_requirements.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv",
        index=False,
    )

    manifest = pd.DataFrame(
        [
            {
                "bundle_file": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "active_response_file": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for path in [
                DATA / "ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv",
                DATA / "ugc12506_beta_closure_transfer_scoring_unlock_requirements.csv",
                SPIN_EXPOSURE_EXAMPLE,
                SPIN_BULLOCK_EXAMPLE,
                CARRIER_EXAMPLE,
                DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv",
                DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv",
            ]
        ]
    )
    manifest.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_unlock_packet_manifest.csv",
        index=False,
    )

    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as archive:
        for path in manifest["bundle_file"]:
            archive.write(ROOT / path, arcname=path)

    report = [
        "# UGC12506 Beta-Closure Transfer Scoring Unlock Packet",
        "",
        "This is the final pre-scoring handoff packet. It does not accept review",
        "decisions and does not create active response files. It gives the",
        "external reviewer exact response schemas and example-only rows.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Required Active Responses",
        "",
        markdown_table(requirements),
        "",
        "## Contract-Ready Dry-Run Scenarios",
        "",
        markdown_table(ready_scenarios),
        "",
        "## Claim Boundary",
        "",
        "The example-only rows are not active review responses. Scoring remains",
        "blocked until an independent reviewer writes the active response files",
        "and the standard intake, prefreeze, formula-freeze, and scoring-launch",
        "gates pass.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_scoring_unlock_packet.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
