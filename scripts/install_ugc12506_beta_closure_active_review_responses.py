#!/usr/bin/env python3
"""Install active UGC12506 beta-closure review responses after validation.

This script is intentionally narrow.  It does not generate review decisions
and it never promotes example-only rows.  It looks for two completed reviewer
CSV files in an incoming directory, validates their schema and safety flags,
and only then copies them into the active response paths consumed by the
standard intake scripts.

Default incoming directory:
    review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/

Expected filenames:
    ugc12506_beta_closure_spin_proxy_review_response.csv
    ugc12506_beta_closure_carrier_review_response.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
DEFAULT_INCOMING = (
    ROOT / "review_bundles" / "incoming" / "ugc12506_beta_closure_transfer_scoring"
)
CLAIM_BOUNDARY = "ugc12506_beta_closure_active_review_response_installer_not_endpoint"

ACTIVE_SPIN = DATA / "ugc12506_beta_closure_spin_proxy_review_response.csv"
ACTIVE_CARRIER = DATA / "ugc12506_beta_closure_carrier_review_response.csv"

SPIN_COLUMNS = [
    "packet_id",
    "reviewer_or_method_id",
    "review_timestamp_utc",
    "source_fields_decision",
    "weight_rule_decision",
    "selected_spin_normalization_route",
    "definition_boundary_decision",
    "transfer_scope_decision",
    "accepted_targets",
    "rejected_targets",
    "required_changes",
    "review_rationale",
    "source_inputs_used",
    "forbidden_inputs_used",
    "proxy_promotion_allowed_after_review",
    "beta_cl_replay_allowed_after_review",
    "endpoint_scores_allowed",
    "uses_vobs_or_residual",
    "claim_boundary",
]

CARRIER_COLUMNS = [
    "packet_id",
    "reviewer_or_method_id",
    "review_timestamp_utc",
    "carrier_route_decision",
    "selected_carrier_id",
    "li2020_policy_decision",
    "accepted_targets",
    "rejected_targets",
    "required_changes",
    "review_rationale",
    "source_inputs_used",
    "forbidden_inputs_used",
    "carrier_prefreeze_allowed_after_review",
    "endpoint_scores_allowed",
    "uses_vobs_or_residual",
    "claim_boundary",
]

FALSE_VALUES = {"", "none", "false", "no", "n", "0"}
PLACEHOLDER_MARKERS = {"PENDING_INDEPENDENT_REVIEW", "EXAMPLE_ONLY", "EXAMPLE_ONLY_NOT_A_REVIEW_DECISION"}


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


def norm(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def norm_upper(value: object) -> str:
    return norm(value).upper()


def false_clean(value: object) -> bool:
    return norm(value).lower() in FALSE_VALUES


def validate_response(
    input_path: Path,
    expected_columns: list[str],
    response_type: str,
) -> tuple[dict[str, object], pd.DataFrame | None]:
    row = {
        "response_type": response_type,
        "incoming_path": str(input_path.relative_to(ROOT)) if input_path.exists() else str(input_path),
        "exists": input_path.exists(),
        "schema_pass": False,
        "single_row_pass": False,
        "not_placeholder_pass": False,
        "forbidden_flags_pass": False,
        "install_allowed": False,
        "reason": "",
        "endpoint_scores_allowed": False,
        "uses_vobs_or_residual": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }
    if not input_path.exists():
        row["reason"] = "incoming response file missing"
        return row, None
    try:
        df = pd.read_csv(input_path)
    except Exception as exc:  # pragma: no cover - defensive report path
        row["reason"] = f"could not read csv: {exc}"
        return row, None
    missing_columns = [column for column in expected_columns if column not in df.columns]
    row["schema_pass"] = not missing_columns
    row["single_row_pass"] = len(df) == 1
    if missing_columns:
        row["reason"] = f"missing columns: {missing_columns}"
        return row, df
    if len(df) != 1:
        row["reason"] = f"expected exactly one row; got {len(df)}"
        return row, df
    first = df.iloc[0]
    placeholder_values = {
        norm_upper(first.get("reviewer_or_method_id", "")),
        norm_upper(first.get("review_timestamp_utc", "")),
    }
    row["not_placeholder_pass"] = not bool(placeholder_values & PLACEHOLDER_MARKERS)
    row["forbidden_flags_pass"] = (
        false_clean(first.get("forbidden_inputs_used", ""))
        and false_clean(first.get("endpoint_scores_allowed", ""))
        and false_clean(first.get("uses_vobs_or_residual", ""))
    )
    row["install_allowed"] = (
        row["schema_pass"]
        and row["single_row_pass"]
        and row["not_placeholder_pass"]
        and row["forbidden_flags_pass"]
    )
    row["reason"] = (
        "validated active response"
        if row["install_allowed"]
        else "placeholder or forbidden endpoint/residual flag detected"
    )
    return row, df


def maybe_install(source: Path, destination: Path, allowed: bool) -> bool:
    if not allowed:
        return False
    if destination.exists():
        backup = destination.with_suffix(destination.suffix + ".bak")
        shutil.copy2(destination, backup)
    shutil.copy2(source, destination)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--incoming-dir",
        type=Path,
        default=DEFAULT_INCOMING,
        help="Directory containing completed active reviewer response CSVs.",
    )
    args = parser.parse_args()

    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    incoming = args.incoming_dir

    spin_incoming = incoming / ACTIVE_SPIN.name
    carrier_incoming = incoming / ACTIVE_CARRIER.name

    spin_check, _ = validate_response(spin_incoming, SPIN_COLUMNS, "spin_route_review")
    carrier_check, _ = validate_response(carrier_incoming, CARRIER_COLUMNS, "carrier_review")
    checks = pd.DataFrame([spin_check, carrier_check])

    install_all = checks["install_allowed"].all()
    spin_installed = maybe_install(spin_incoming, ACTIVE_SPIN, install_all)
    carrier_installed = maybe_install(carrier_incoming, ACTIVE_CARRIER, install_all)

    status = (
        "U12506_BETA_ACTIVE_REVIEW_RESPONSES_INSTALLED_RUN_POST_REVIEW_LAUNCHER"
        if install_all and spin_installed and carrier_installed
        else "U12506_BETA_ACTIVE_REVIEW_RESPONSE_INSTALL_BLOCKED_INCOMING_PENDING_OR_INVALID"
    )
    summary = pd.DataFrame(
        [
            {
                "active_response_install_status": status,
                "incoming_dir": str(incoming.relative_to(ROOT)) if incoming.is_relative_to(ROOT) else str(incoming),
                "n_required_responses": len(checks),
                "n_existing_incoming_responses": int(checks["exists"].sum()),
                "n_install_allowed_responses": int(checks["install_allowed"].sum()),
                "spin_response_installed": spin_installed,
                "carrier_response_installed": carrier_installed,
                "active_spin_response_exists": ACTIVE_SPIN.exists(),
                "active_carrier_response_exists": ACTIVE_CARRIER.exists(),
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "run_ugc12506_beta_closure_post_review_scoring_launcher"
                    if install_all and spin_installed and carrier_installed
                    else "place_completed_independent_responses_in_incoming_dir"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    checks.to_csv(
        DATA / "ugc12506_beta_closure_active_review_response_install_checks.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_active_review_response_install_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Active Review Response Installer",
        "",
        "This installer validates completed reviewer response CSVs from the",
        "incoming directory and copies them into active response paths only when",
        "both files are present, non-placeholder, one-row, schema-valid, and",
        "free of endpoint/residual flags.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Checks",
        "",
        markdown_table(checks),
        "",
        "## Claim Boundary",
        "",
        "This script does not create review decisions. Missing or placeholder",
        "responses keep scoring blocked.",
    ]
    (REPORTS / "ugc12506_beta_closure_active_review_response_installer.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
