#!/usr/bin/env python3
"""Build a residual-blind beta-closure spin-proxy review bundle.

The UGC12506 beta-closure transfer route has no accepted direct
halo/envelope lambda_spin source for the primary transfer targets.  A
source-only proxy rule has therefore been declared, but it is not promoted
here.  This script packages the declared proxy, direct-source audit, definition
conversion rejection, review obligations, and a blank response form for an
independent reviewer.  It is not a review response, not a replay manifest, and
not an endpoint.
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
BUNDLE_ROOT = ROOT / "review_bundles" / "ugc12506_beta_closure_spin_proxy"
ZIP_PATH = ROOT / "review_bundles" / "ugc12506_beta_closure_spin_proxy_review_bundle.zip"
CLAIM_BOUNDARY = "ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint"
PACKET_ID = "U12506_BETA_SPIN_PROXY_REVIEW_PACKET_V1"


BUNDLE_FILES = [
    (
        "reports/ugc12506_beta_closure_source_declared_spin_proxy_gate.md",
        REPORTS / "ugc12506_beta_closure_source_declared_spin_proxy_gate.md",
    ),
    (
        "reports/ugc12506_beta_closure_direct_lambda_spin_source_gate.md",
        REPORTS / "ugc12506_beta_closure_direct_lambda_spin_source_gate.md",
    ),
    (
        "reports/ugc12506_beta_closure_lambda_definition_conversion_gate.md",
        REPORTS / "ugc12506_beta_closure_lambda_definition_conversion_gate.md",
    ),
    (
        "reports/ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md",
        REPORTS / "ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md",
    ),
    (
        "data/ugc12506_beta_closure_source_declared_spin_proxy_fields.csv",
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_fields.csv",
    ),
    (
        "data/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv",
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv",
    ),
    (
        "data/ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv",
        DATA / "ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv",
    ),
    (
        "data/ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv",
        DATA / "ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv",
    ),
    (
        "data/ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv",
        DATA / "ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv",
    ),
    (
        "data/ugc12506_beta_closure_lambda_definition_conversion_checks.csv",
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_checks.csv",
    ),
    (
        "data/ugc12506_beta_closure_lambda_definition_conversion_comparison.csv",
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_comparison.csv",
    ),
    (
        "data/ugc12506_beta_closure_lambda_definition_conversion_worklist.csv",
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_worklist.csv",
    ),
    (
        "data/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv",
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv",
    ),
    (
        "data/ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv",
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv",
    ),
    (
        "data/ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv",
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv",
    ),
    (
        "data/ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv",
        DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_candidates.csv",
        DATA / "ugc12506_beta_closure_transfer_candidates.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_halo_fit_fields.csv",
        DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv",
    ),
    (
        "data/ugc12506_beta_closure_transfer_priority_gate.csv",
        DATA / "ugc12506_beta_closure_transfer_priority_gate.csv",
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


def build_review_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "BSP_REV_1_SOURCE_FIELDS",
                "review_question": (
                    "Are RHI/Rdisk, Vflat, H I mass, and inclination acceptable "
                    "source-side observables for a spin/envelope exposure proxy?"
                ),
                "required_decision": "ACCEPT_FIELDS_OR_REJECT_PROXY",
                "allowed_evidence": (
                    "SPARC source fields; source-native H I/kinematic context; "
                    "literature spin/envelope context"
                ),
                "forbidden_inputs": "rotation residuals; endpoint RMSE; baseline ranks",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "obligation_id": "BSP_REV_2_WEIGHT_RULE",
                "review_question": (
                    "Is the predeclared exposure load-weight rule defensible as a "
                    "protocol candidate, should the Bullock-like disk-conversion "
                    "proxy be preferred, or must both be replaced before replay?"
                ),
                "required_decision": "ACCEPT_EXPOSURE_RULE_OR_BULLOCK_RULE_OR_REQUIRE_NEW_RULE",
                "allowed_evidence": (
                    "source-side dimensional and monotonicity audit; Bullock-like "
                    "disk-inferred conversion report"
                ),
                "forbidden_inputs": "best-fit beta; endpoint score; wrong-family rank",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "obligation_id": "BSP_REV_3_DEFINITION_BOUNDARY",
                "review_question": (
                    "Does the reviewer agree that Marr (2015) NGC7331 disc lambda "
                    "is context only and cannot directly fill beta_cl lambda_spin?"
                ),
                "required_decision": "ACCEPT_CONTEXT_ONLY_OR_SUPPLY_CONVERSION",
                "allowed_evidence": "definition comparison; source-side conversion theorem",
                "forbidden_inputs": "choosing the larger lambda because it improves a curve",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "obligation_id": "BSP_REV_4_TRANSFER_SCOPE",
                "review_question": (
                    "Which targets, if any, may carry the proxy as a caveated "
                    "transfer-review input?"
                ),
                "required_decision": "ACCEPT_TARGET_SET_OR_RESTRICT_TARGET_SET",
                "allowed_evidence": "proxy transfer queue and source evidence only",
                "forbidden_inputs": "post-score target promotion",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    forbidden = pd.DataFrame(
        [
            {
                "forbidden_input_id": "BSP_FORBID_1_ROTATION_RESIDUALS",
                "forbidden_input": "v_obs residuals or residual-zone plots",
                "reason": "would turn the proxy into residual rescue",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "forbidden_input_id": "BSP_FORBID_2_ENDPOINT_SCORES",
                "forbidden_input": "endpoint RMSE, beat fractions, or rank after scoring",
                "reason": "proxy promotion must precede any replay",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "forbidden_input_id": "BSP_FORBID_3_BASELINE_RANKS",
                "forbidden_input": "Newton/MOND/RAR/RMOND/TPG baseline comparison ranks",
                "reason": "baseline weakness can motivate audit but not define the proxy",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "forbidden_input_id": "BSP_FORBID_4_DISC_DIRECT_INSERTION",
                "forbidden_input": "direct insertion of disc lambda into halo/envelope slot",
                "reason": "definition conversion gate rejected direct substitution",
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
                "source_fields_decision": "PENDING_INDEPENDENT_REVIEW",
                "weight_rule_decision": "PENDING_INDEPENDENT_REVIEW",
                "selected_spin_normalization_route": "PENDING_INDEPENDENT_REVIEW",
                "definition_boundary_decision": "PENDING_INDEPENDENT_REVIEW",
                "transfer_scope_decision": "PENDING_INDEPENDENT_REVIEW",
                "accepted_targets": "PENDING_INDEPENDENT_REVIEW",
                "rejected_targets": "PENDING_INDEPENDENT_REVIEW",
                "required_changes": "PENDING_INDEPENDENT_REVIEW",
                "review_rationale": "PENDING_INDEPENDENT_REVIEW",
                "source_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "forbidden_inputs_used": "PENDING_INDEPENDENT_REVIEW",
                "proxy_promotion_allowed_after_review": False,
                "beta_cl_replay_allowed_after_review": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return obligations, forbidden, response_template


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    BUNDLE_ROOT.parent.mkdir(parents=True, exist_ok=True)
    if BUNDLE_ROOT.exists():
        shutil.rmtree(BUNDLE_ROOT)
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)

    obligations, forbidden, response_template = build_review_tables()
    obligations.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_obligations.csv",
        index=False,
    )
    forbidden.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv",
        index=False,
    )
    response_template.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_response_template.csv",
        index=False,
    )

    review_packet = pd.DataFrame(
        [
            {
                "review_packet_id": PACKET_ID,
                "packet_status": "READY_FOR_INDEPENDENT_REVIEW_RESPONSE",
                "review_subject": "source-only beta_cl spin/envelope normalization route",
                "proxy_formula": (
                    "lambda_spin_proxy=lambda_ref*(1 + 0.35*extent_load + "
                    "0.25*velocity_load + 0.25*gas_load + 0.15*edgeon_load)"
                ),
                "bullock_like_conversion_formula": (
                    "lambda'_disk=(2*Rdisk*Vflat)/(sqrt(2)*R200*V200); "
                    "R200=V200/(10*H0)"
                ),
                "lambda_ref": 0.10,
                "primary_review_target": "NGC0891",
                "secondary_review_targets": "NGC7331;NGC2841;NGC0801;NGC4013",
                "direct_lambda_status": "no_beta_cl_direct_lambda_accepted",
                "definition_conversion_status": "ngc7331_disc_lambda_context_only",
                "endpoint_scores_allowed": False,
                "beta_cl_replay_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    review_packet.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_packet.csv",
        index=False,
    )

    prompt = "\n".join(
        [
            "# UGC12506 Beta-Closure Spin Proxy Review Prompt",
            "",
            "You are reviewing a residual-blind source-proxy gate, not an endpoint result.",
            "",
            "Please decide whether any residual-blind spin/envelope normalization route can be carried as a caveated transfer-review input for beta_cl preflight. Do not use rotation-curve residuals, endpoint RMSE, baseline ranks, wrong-family Tau scores, or post-hoc amplitude changes.",
            "",
            "Review objects:",
            "",
            "`lambda_spin_proxy = lambda_ref * (1 + 0.35 extent_load + 0.25 velocity_load + 0.25 gas_load + 0.15 edgeon_load)`",
            "",
            "with `lambda_ref = 0.10`. The loads use source-side `RHI/Rdisk`, `Vflat`, H I mass, and inclination only.",
            "",
            "and the conservative Bullock-like disk-inferred conversion control:",
            "",
            "`lambda'_disk = (2 Rdisk Vflat) / (sqrt(2) R200 V200)`, with `R200 = V200/(10 H0)`.",
            "",
            "Key decisions:",
            "",
            "1. Are the source fields acceptable for a spin/envelope exposure proxy?",
            "2. Should the exposure proxy, Bullock-like conversion proxy, direct-source route, or a new residual-blind rule be used?",
            "3. Do you agree that the Marr (2015) NGC7331 disc-spin lambda is source context only and cannot directly fill the beta_cl halo/envelope lambda_spin slot without a conversion rule?",
            "4. Which transfer targets, if any, may carry the proxy as caveated inputs?",
            "",
            "Fill `response/ugc12506_beta_closure_spin_proxy_review_response_blank.csv` and leave `endpoint_scores_allowed=false` unless a separate future endpoint manifest is built after this review.",
            "",
        ]
    )
    prompt_path = REPORTS / "ugc12506_beta_closure_spin_proxy_review_prompt.md"
    prompt_path.write_text(prompt, encoding="utf-8")

    response_blank_path = DATA / "ugc12506_beta_closure_spin_proxy_review_response_blank.csv"
    response_template.to_csv(response_blank_path, index=False)

    extra_files = [
        ("README.md", prompt_path),
        (
            "response/ugc12506_beta_closure_spin_proxy_review_response_blank.csv",
            response_blank_path,
        ),
        (
            "data/ugc12506_beta_closure_spin_proxy_review_packet.csv",
            DATA / "ugc12506_beta_closure_spin_proxy_review_packet.csv",
        ),
        (
            "data/ugc12506_beta_closure_spin_proxy_review_obligations.csv",
            DATA / "ugc12506_beta_closure_spin_proxy_review_obligations.csv",
        ),
        (
            "data/ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv",
            DATA / "ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv",
        ),
        (
            "data/ugc12506_beta_closure_spin_proxy_review_response_template.csv",
            DATA / "ugc12506_beta_closure_spin_proxy_review_response_template.csv",
        ),
    ]

    manifest_rows = []
    missing = []
    for relative_name, source in [*BUNDLE_FILES, *extra_files]:
        exists = source.exists()
        if not exists:
            sha = ""
            missing.append(str(source.relative_to(ROOT)))
        else:
            target = BUNDLE_ROOT / relative_name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            sha = file_sha256(target)
        manifest_rows.append(
            {
                "bundle_relative_path": relative_name,
                "source_repo_path": str(source.relative_to(ROOT)),
                "exists": exists,
                "sha256": sha,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    usage = "\n".join(
        [
            "# UGC12506 Beta-Closure Spin Proxy Review Bundle Usage",
            "",
            "This bundle is for residual-blind source review only. It is not an endpoint package.",
            "",
            "1. Read `README.md` first.",
            "2. Inspect the `data/` and `reports/` files.",
            "3. Fill `response/ugc12506_beta_closure_spin_proxy_review_response_blank.csv`.",
            "4. Return the completed CSV for intake before any beta_cl transfer replay is considered.",
            "",
            "Forbidden inputs: rotation residuals, endpoint scores, baseline ranks, wrong-family ranks, and direct disc-lambda insertion without a conversion rule.",
            "",
        ]
    )
    usage_path = BUNDLE_ROOT / "USAGE.md"
    usage_path.write_text(usage, encoding="utf-8")
    manifest_rows.append(
        {
            "bundle_relative_path": "USAGE.md",
            "source_repo_path": "generated_by_bundle_builder",
            "exists": True,
            "sha256": file_sha256(usage_path),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    )

    manifest = pd.DataFrame(manifest_rows)
    manifest.to_csv(BUNDLE_ROOT / "bundle_manifest.csv", index=False)
    manifest.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_bundle_manifest.csv",
        index=False,
    )

    input_hashes = manifest[
        manifest["exists"].eq(True)
        & manifest["bundle_relative_path"].str.startswith(("data/", "reports/"))
    ][["bundle_relative_path", "source_repo_path", "sha256", "claim_boundary"]]
    input_hashes.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_input_hashes.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "review_bundle_status": (
                    "U12506_BETA_SPIN_PROXY_REVIEW_BUNDLE_READY_RESPONSE_PENDING"
                    if not missing
                    else "U12506_BETA_SPIN_PROXY_REVIEW_BUNDLE_MISSING_INPUTS"
                ),
                "review_packet_id": PACKET_ID,
                "bundle_dir": str(BUNDLE_ROOT.relative_to(ROOT)),
                "bundle_zip": str(ZIP_PATH.relative_to(ROOT)),
                "n_files_listed": int(len(manifest)),
                "n_missing_inputs": int(len(missing)),
                "missing_inputs": ";".join(missing) if missing else "none",
                "review_response_received": False,
                "proxy_promotion_allowed": False,
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": "intake_independent_spin_proxy_review_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_spin_proxy_review_bundle_summary.csv",
        index=False,
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(BUNDLE_ROOT.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(BUNDLE_ROOT.parent))

    report = [
        "# UGC12506 Beta-Closure Spin Proxy Review Bundle",
        "",
        "This bundle prepares an independent, residual-blind review of the",
        "source-declared beta_cl spin/envelope exposure proxy. It is not a",
        "review response, not a replay manifest, and not an endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Review Packet",
        "",
        markdown_table(review_packet),
        "",
        "## Review Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Forbidden Inputs",
        "",
        markdown_table(forbidden),
        "",
        "## Bundle Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Claim Boundary",
        "",
        "The proxy can only move forward after a completed independent response",
        "passes an intake validator. This script does not authorize beta_cl replay",
        "or endpoint scoring.",
    ]
    (REPORTS / "ugc12506_beta_closure_spin_proxy_review_bundle.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
