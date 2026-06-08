#!/usr/bin/env python3
"""Build the UGC12506 beta-closure carrier-review bundle.

The beta_cl transfer path needs a source-frozen velocity-squared carrier before
any scoring runner may read observed rotation curves.  This bundle packages
the carrier decision matrix and a blank independent-review response.  It does
not accept a carrier, freeze a formula, or score.
"""

from __future__ import annotations

import hashlib
import shutil
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
BUNDLE_ROOT = ROOT / "review_bundles" / "ugc12506_beta_closure_carrier"
ZIP_PATH = ROOT / "review_bundles" / "ugc12506_beta_closure_carrier_review_bundle.zip"
CLAIM_BOUNDARY = "ugc12506_beta_closure_carrier_review_bundle_not_endpoint"
PACKET_ID = "U12506_BETA_CARRIER_REVIEW_PACKET_V1"


BUNDLE_FILES = [
    (
        "reports/ugc12506_beta_closure_transfer_carrier_freeze_gate.md",
        REPORTS / "ugc12506_beta_closure_transfer_carrier_freeze_gate.md",
    ),
    (
        "data/ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv",
        DATA / "ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv",
        DATA / "ugc12506_beta_closure_transfer_carrier_freeze_summary.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_carrier_freeze_gates.csv",
        DATA / "ugc12506_beta_closure_transfer_carrier_freeze_gates.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_candidates.csv",
        DATA / "ugc12506_beta_closure_transfer_candidates.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_priority_gate.csv",
        DATA / "ugc12506_beta_closure_transfer_priority_gate.csv",
    ),
    (
        "data/fast_sparc_rotation_curve_packet_galaxy_summary.csv",
        DATA / "fast_sparc_rotation_curve_packet_galaxy_summary.csv",
    ),
]


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)
    (BUNDLE_ROOT / "data").mkdir(parents=True, exist_ok=True)
    (BUNDLE_ROOT / "reports").mkdir(parents=True, exist_ok=True)
    (BUNDLE_ROOT / "response").mkdir(parents=True, exist_ok=True)

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "BCR_REV_1_CARRIER_ROUTE",
                "review_question": (
                    "Which carrier route, if any, may be frozen before beta_cl "
                    "transfer scoring?"
                ),
                "required_decision": (
                    "ACCEPT_BARYONIC_STRESS_CARRIER_OR_REQUIRE_SOURCE_NATIVE_CARRIER_OR_REJECT"
                ),
                "allowed_evidence": (
                    "carrier route decision matrix; SPARC fast-packet provenance; "
                    "source-native carrier derivation artifacts if supplied"
                ),
                "forbidden_inputs": "endpoint residuals; score ranks; curve-saving amplitude choices",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "obligation_id": "BCR_REV_2_LEAKAGE_POLICY",
                "review_question": (
                    "Should Li et al. NFW-fit products remain control-only, or has "
                    "a separate leakage policy justified their use?"
                ),
                "required_decision": "KEEP_LI2020_CONTROL_ONLY_OR_SUPPLY_POLICY",
                "allowed_evidence": "provenance and leakage-policy arguments",
                "forbidden_inputs": "selecting NFW carrier because it improves endpoint score",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    forbidden = pd.DataFrame(
        [
            {
                "forbidden_input_id": "BCR_FORBID_1_ENDPOINT_RESIDUALS",
                "forbidden_input": "rotation residuals or endpoint RMSE",
                "reason": "carrier selection must precede scoring",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "forbidden_input_id": "BCR_FORBID_2_BASELINE_RANKS",
                "forbidden_input": "Newton/MOND/RAR/RMOND/TPG rank comparisons",
                "reason": "baseline weakness may motivate stress testing but cannot choose carrier",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "forbidden_input_id": "BCR_FORBID_3_NFW_SCORE_SELECTION",
                "forbidden_input": "choosing Li2020 NFW carrier from fit quality or endpoint advantage",
                "reason": "Li2020 halo-fit products are control-only without explicit leakage policy",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    response_template = pd.DataFrame(
        [
            {
                "packet_id": PACKET_ID,
                "reviewer_or_method_id": "PENDING_INDEPENDENT_REVIEW",
                "review_timestamp_utc": "PENDING_INDEPENDENT_REVIEW",
                "carrier_route_decision": "PENDING_INDEPENDENT_REVIEW",
                "selected_carrier_id": "PENDING_INDEPENDENT_REVIEW",
                "li2020_policy_decision": "PENDING_INDEPENDENT_REVIEW",
                "accepted_targets": "PENDING_INDEPENDENT_REVIEW",
                "rejected_targets": "PENDING_INDEPENDENT_REVIEW",
                "required_changes": "PENDING_INDEPENDENT_REVIEW",
                "review_rationale": "PENDING_INDEPENDENT_REVIEW",
                "source_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "forbidden_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "carrier_prefreeze_allowed_after_review": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    obligations.to_csv(
        DATA / "ugc12506_beta_closure_carrier_review_obligations.csv",
        index=False,
    )
    forbidden.to_csv(
        DATA / "ugc12506_beta_closure_carrier_review_forbidden_inputs.csv",
        index=False,
    )
    response_template.to_csv(
        DATA / "ugc12506_beta_closure_carrier_review_response_template.csv",
        index=False,
    )
    response_template.to_csv(
        DATA / "ugc12506_beta_closure_carrier_review_response_blank.csv",
        index=False,
    )

    manifest_rows = []
    for rel, src in BUNDLE_FILES:
        exists = src.exists()
        dest = BUNDLE_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if exists:
            shutil.copy2(src, dest)
        manifest_rows.append(
            {
                "bundle_relative_path": rel,
                "source_path": str(src.relative_to(ROOT)),
                "exists": exists,
                "sha256": file_sha256(src) if exists else "",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    extra_files = [
        (
            "data/ugc12506_beta_closure_carrier_review_obligations.csv",
            DATA / "ugc12506_beta_closure_carrier_review_obligations.csv",
        ),
        (
            "data/ugc12506_beta_closure_carrier_review_forbidden_inputs.csv",
            DATA / "ugc12506_beta_closure_carrier_review_forbidden_inputs.csv",
        ),
        (
            "response/ugc12506_beta_closure_carrier_review_response_blank.csv",
            DATA / "ugc12506_beta_closure_carrier_review_response_blank.csv",
        ),
    ]
    for rel, src in extra_files:
        dest = BUNDLE_ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        manifest_rows.append(
            {
                "bundle_relative_path": rel,
                "source_path": str(src.relative_to(ROOT)),
                "exists": True,
                "sha256": file_sha256(src),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    bundle_manifest = pd.DataFrame(manifest_rows)
    bundle_manifest.to_csv(DATA / "ugc12506_beta_closure_carrier_review_bundle_manifest.csv", index=False)
    bundle_manifest.to_csv(BUNDLE_ROOT / "bundle_manifest.csv", index=False)

    readme = "\n".join(
        [
            "# UGC12506 Beta-Closure Carrier Review Bundle",
            "",
            "This bundle is for independent carrier-route review. It is not a score.",
            "",
            "Fill `response/ugc12506_beta_closure_carrier_review_response_blank.csv`.",
            "Keep `endpoint_scores_allowed=false` and `uses_vobs_or_residual=false`.",
            "",
            "Currently implemented endpoint-safe carrier prefreeze support exists only",
            "for `BARYONIC_050_FAST_PACKET`. The Li2020 NFW route remains control-only",
            "unless a separate leakage policy is supplied.",
            "",
        ]
    )
    (BUNDLE_ROOT / "README.md").write_text(readme, encoding="utf-8")

    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in BUNDLE_ROOT.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(BUNDLE_ROOT.parent))

    summary = pd.DataFrame(
        [
            {
                "carrier_review_bundle_status": (
                    "U12506_BETA_CARRIER_REVIEW_BUNDLE_READY_RESPONSE_PENDING"
                ),
                "review_packet_id": PACKET_ID,
                "bundle_root": str(BUNDLE_ROOT.relative_to(ROOT)),
                "zip_path": str(ZIP_PATH.relative_to(ROOT)),
                "n_bundle_files": len(bundle_manifest),
                "n_missing_inputs": int((~bundle_manifest["exists"]).sum()),
                "review_response_received": False,
                "carrier_prefreeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": "intake_independent_carrier_review_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(DATA / "ugc12506_beta_closure_carrier_review_bundle_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Carrier Review Bundle",
        "",
        "This bundle packages the carrier decision matrix and review obligations.",
        "It does not accept a carrier and does not score.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Forbidden Inputs",
        "",
        markdown_table(forbidden),
        "",
        "## Bundle Manifest",
        "",
        markdown_table(bundle_manifest),
    ]
    (REPORTS / "ugc12506_beta_closure_carrier_review_bundle.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
