#!/usr/bin/env python3
"""Build a no-repository reviewer packet for UGC12506 beta-closure scoring.

The packet is meant for reviewers who cannot access the repository.  It
contains human-readable instructions, the exact two fillable CSV files expected
by the active-response installer, and compact supporting ledgers.  It does not
create active responses and does not authorize endpoint scoring.
"""

from __future__ import annotations

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
REVIEW_BUNDLES = ROOT / "review_bundles"
PACKET_DIR = REVIEW_BUNDLES / "ugc12506_beta_closure_no_repo_reviewer_packet"
RESPONSE_DIR = PACKET_DIR / "response"
SUPPORT_DIR = PACKET_DIR / "supporting_ledgers"
ZIP_PATH = REVIEW_BUNDLES / "ugc12506_beta_closure_no_repo_reviewer_packet.zip"
CLAIM_BOUNDARY = "ugc12506_beta_closure_no_repo_reviewer_packet_not_endpoint"


SPIN_ACTIVE_NAME = "ugc12506_beta_closure_spin_proxy_review_response.csv"
CARRIER_ACTIVE_NAME = "ugc12506_beta_closure_carrier_review_response.csv"


SUPPORT_FILES = [
    DATA / "ugc12506_beta_closure_transfer_scoring_unlock_requirements.csv",
    DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv",
    DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv",
    DATA / "ugc12506_beta_closure_scoring_readiness_summary.csv",
    DATA / "ugc12506_beta_closure_scoring_readiness_dashboard.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_packet.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_obligations.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_bundle_manifest.csv",
    DATA / "ugc12506_beta_closure_carrier_review_obligations.csv",
    DATA / "ugc12506_beta_closure_carrier_review_forbidden_inputs.csv",
    DATA / "ugc12506_beta_closure_carrier_review_bundle_manifest.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_response_example_only_exposure_proxy.csv",
    DATA / "ugc12506_beta_closure_spin_proxy_review_response_example_only_bullock_conversion.csv",
    DATA / "ugc12506_beta_closure_carrier_review_response_example_only_baryonic_stress.csv",
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


def clean_dir(path: Path) -> None:
    if path.exists():
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file() or child.is_symlink():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
    path.mkdir(parents=True, exist_ok=True)


def write_fillable_csvs() -> None:
    spin = pd.read_csv(DATA / "ugc12506_beta_closure_spin_proxy_review_response_template.csv")
    carrier = pd.read_csv(DATA / "ugc12506_beta_closure_carrier_review_response_template.csv")
    spin.to_csv(RESPONSE_DIR / SPIN_ACTIVE_NAME, index=False)
    carrier.to_csv(RESPONSE_DIR / CARRIER_ACTIVE_NAME, index=False)


def copy_support_files() -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for source in SUPPORT_FILES:
        exists = source.exists()
        target = SUPPORT_DIR / source.name
        if exists:
            target.write_bytes(source.read_bytes())
        rows.append(
            {
                "source_file": str(source.relative_to(ROOT)),
                "packet_file": str(target.relative_to(PACKET_DIR)),
                "included": exists,
                "active_response_file": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def write_text_files() -> None:
    message = """Subject: Independent UGC12506 beta-closure source-review request

Dear Reviewer,

Thank you for reviewing this UGC12506 beta-closure transfer packet. You do not
need access to the repository. The ZIP contains all fields needed for this
review and two fillable CSV files in the `response/` directory.

What we need
------------
Please fill exactly these two files:

1. response/ugc12506_beta_closure_spin_proxy_review_response.csv
2. response/ugc12506_beta_closure_carrier_review_response.csv

The review is residual-blind. Please use only the supplied source/protocol
materials and any independent source-side astrophysical judgement you are
comfortable documenting. Do not use rotation-curve residuals, endpoint scores,
RMSE comparisons, or a post-hoc desire to improve UGC12506.

Decision 1: spin normalization route
------------------------------------
Choose whether the source-side evidence supports one of the reviewable routes:

- EXPOSURE_PROXY with weight_rule_decision=ACCEPT_EXPOSURE_RULE
- BULLOCK_DISK_CONVERSION with weight_rule_decision=ACCEPT_BULLOCK_CONVERSION

If neither is acceptable, reject or request changes in the CSV. Do not invent a
new route inside the response unless you clearly mark it as required_changes.

Decision 2: velocity-squared carrier
------------------------------------
Choose whether the minimal baryonic stress carrier is acceptable:

- selected_carrier_id=BARYONIC_050_FAST_PACKET
- carrier_route_decision=ACCEPT_BARYONIC_STRESS_CARRIER
- li2020_policy_decision=KEEP_LI2020_CONTROL_ONLY

If it is not acceptable, reject it or require a source-native carrier.

Hard safety requirements
------------------------
For both responses:

- forbidden_inputs_used must be False
- endpoint_scores_allowed must be False
- uses_vobs_or_residual must be False
- reviewer_or_method_id must identify you or your review method
- review_timestamp_utc must be filled
- review_rationale and source_inputs_used must be non-placeholder text

The examples in `supporting_ledgers/` are examples only. Please do not return
the example-only rows as active decisions.

Claim boundary
--------------
Your response does not validate Tau Core and does not authorize a paper claim by
itself. It only decides whether the predeclared UGC12506 beta-closure transfer
route may pass into the already-built post-review scoring launcher.
"""

    readme = """# UGC12506 Beta-Closure No-Repository Reviewer Packet

This packet is for reviewers without repository access.

## Fill These Files

Return the two CSV files in `response/` after replacing the pending values:

- `ugc12506_beta_closure_spin_proxy_review_response.csv`
- `ugc12506_beta_closure_carrier_review_response.csv`

Keep the filenames unchanged.

## Supporting Files

The `supporting_ledgers/` directory contains requirements, obligations,
forbidden inputs, dry-run summaries, readiness status, and example-only rows.

## Current Pre-Review Status

The computational path is mechanically prepared, but scoring is blocked because
the two active reviewer responses are absent. No observed rotation curve is read
by the pre-scoring artifacts.

## Returning The Review

Send back the two filled CSV files only. They will be placed into:

`review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/`

Then the installer will validate that the rows are non-placeholder,
schema-valid, one-row, and free of endpoint/residual flags.
"""

    (PACKET_DIR / "MESSAGE_TO_REVIEWER.txt").write_text(message, encoding="utf-8")
    (PACKET_DIR / "README.md").write_text(readme, encoding="utf-8")


def write_manifest(support_manifest: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "packet_file": "README.md",
            "file_role": "human_readme",
            "fillable": False,
            "active_response_file": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_file": "MESSAGE_TO_REVIEWER.txt",
            "file_role": "copyable_reviewer_message",
            "fillable": False,
            "active_response_file": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_file": f"response/{SPIN_ACTIVE_NAME}",
            "file_role": "fillable_active_spin_response",
            "fillable": True,
            "active_response_file": True,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "packet_file": f"response/{CARRIER_ACTIVE_NAME}",
            "file_role": "fillable_active_carrier_response",
            "fillable": True,
            "active_response_file": True,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    for _, row in support_manifest.iterrows():
        rows.append(
            {
                "packet_file": row["packet_file"],
                "file_role": "supporting_ledger",
                "fillable": False,
                "active_response_file": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows)
    manifest.to_csv(PACKET_DIR / "packet_manifest.csv", index=False)
    return manifest


def build_zip(manifest: pd.DataFrame) -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as archive:
        for packet_file in manifest["packet_file"]:
            path = PACKET_DIR / packet_file
            archive.write(path, arcname=packet_file)


def main() -> None:
    REVIEW_BUNDLES.mkdir(parents=True, exist_ok=True)
    clean_dir(PACKET_DIR)
    RESPONSE_DIR.mkdir(parents=True, exist_ok=True)
    SUPPORT_DIR.mkdir(parents=True, exist_ok=True)

    write_fillable_csvs()
    support_manifest = copy_support_files()
    write_text_files()
    manifest = write_manifest(support_manifest)
    build_zip(manifest)

    summary = pd.DataFrame(
        [
            {
                "packet_status": "U12506_BETA_CLOSURE_NO_REPO_REVIEWER_PACKET_READY",
                "zip_path": str(ZIP_PATH.relative_to(ROOT)),
                "packet_dir": str(PACKET_DIR.relative_to(ROOT)),
                "n_fillable_response_files": 2,
                "n_supporting_ledgers": int(support_manifest["included"].sum()),
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(DATA / "ugc12506_beta_closure_no_repo_reviewer_packet_summary.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_beta_closure_no_repo_reviewer_packet_manifest.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure No-Repository Reviewer Packet",
        "",
        f"ZIP: `{ZIP_PATH.relative_to(ROOT)}`",
        "",
        "The packet contains two fillable active-response CSV files and compact",
        "supporting ledgers for reviewers without repository access. It does not",
        "create active decisions and does not authorize endpoint scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
    ]
    (REPORTS / "ugc12506_beta_closure_no_repo_reviewer_packet.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
