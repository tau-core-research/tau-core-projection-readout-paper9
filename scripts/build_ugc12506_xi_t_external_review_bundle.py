#!/usr/bin/env python3
"""Build a portable UGC12506 Xi_t external-review bundle.

The bundle collects the prompt, blank response form, source-review packet, and
source evidence needed by a residual-blind reviewer.  It uses relative paths in
the manifest and writes a zip archive for handoff.  This is not a review
response, not an accepted manifest, and not an endpoint.
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
BUNDLE_ROOT = ROOT / "review_bundles" / "ugc12506_xi_t"
ZIP_PATH = ROOT / "review_bundles" / "ugc12506_xi_t_external_review_bundle.zip"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_external_review_bundle_not_endpoint"


BUNDLE_FILES = [
    ("README.md", REPORTS / "ugc12506_xi_t_external_review_prompt.md"),
    ("response/ugc12506_xi_t_source_review_response_blank.csv", DATA / "ugc12506_xi_t_source_review_response_blank.csv"),
    ("reports/ugc12506_xi_t_external_review_handoff.md", REPORTS / "ugc12506_xi_t_external_review_handoff.md"),
    ("reports/ugc12506_xi_t_source_review_packet.md", REPORTS / "ugc12506_xi_t_source_review_packet.md"),
    ("reports/ugc12506_xi_t_source_review_response_intake.md", REPORTS / "ugc12506_xi_t_source_review_response_intake.md"),
    ("data/ugc12506_xi_t_source_review_packet.csv", DATA / "ugc12506_xi_t_source_review_packet.csv"),
    ("data/ugc12506_xi_t_source_review_obligations.csv", DATA / "ugc12506_xi_t_source_review_obligations.csv"),
    ("data/ugc12506_xi_t_source_review_response_template.csv", DATA / "ugc12506_xi_t_source_review_response_template.csv"),
    ("data/ugc12506_xi_t_source_review_forbidden_inputs.csv", DATA / "ugc12506_xi_t_source_review_forbidden_inputs.csv"),
    ("data/ugc12506_xi_t_source_review_input_hashes.csv", DATA / "ugc12506_xi_t_source_review_input_hashes.csv"),
    ("data/ugc12506_highmass_fast_source_context_evidence.csv", DATA / "ugc12506_highmass_fast_source_context_evidence.csv"),
    ("data/ugc12506_observer_path_interloper_audit_summary.csv", DATA / "ugc12506_observer_path_interloper_audit_summary.csv"),
    ("data/ugc12506_projection_highspin_preflight_observables.csv", DATA / "ugc12506_projection_highspin_preflight_observables.csv"),
    ("data/ugc12506_xi_t_highspin_envelope_clock_shell_components.csv", DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv"),
    ("data/ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv", DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv"),
    ("data/ugc12506_xi_t_normalization_theorem.csv", DATA / "ugc12506_xi_t_normalization_theorem.csv"),
    ("data/ugc12506_xi_t_epsilon_cap_protocol_theorem.csv", DATA / "ugc12506_xi_t_epsilon_cap_protocol_theorem.csv"),
    ("data/ugc12506_xi_t_accepted_manifest_gate_items.csv", DATA / "ugc12506_xi_t_accepted_manifest_gate_items.csv"),
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
    DATA.mkdir(parents=True, exist_ok=True)
    BUNDLE_ROOT.parent.mkdir(parents=True, exist_ok=True)
    if BUNDLE_ROOT.exists():
        shutil.rmtree(BUNDLE_ROOT)
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)

    manifest_rows = []
    missing = []
    for relative_name, source in BUNDLE_FILES:
        exists = source.exists()
        if not exists:
            missing.append(str(source.relative_to(ROOT)))
            sha = ""
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
            "# UGC12506 Xi_t External Review Bundle Usage",
            "",
            "This bundle is for residual-blind source review only. It is not an endpoint package.",
            "",
            "1. Read `README.md` first.",
            "2. Fill `response/ugc12506_xi_t_source_review_response_blank.csv`.",
            "3. Save the completed file in the repository as `data/derived/ugc12506_xi_t_source_review_response.csv`.",
            "4. Run `python scripts/run_ugc12506_xi_t_source_review_response_intake.py` from the repository root.",
            "",
            "Do not use rotation residuals, endpoint RMSE, baseline ranks, wrong-family Tau scores, post-hoc cap changes, or foreground/path rescue without source evidence.",
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
    manifest.to_csv(DATA / "ugc12506_xi_t_external_review_bundle_manifest.csv", index=False)

    summary = pd.DataFrame(
        [
            {
                "bundle_status": "U12506_XI_T_EXTERNAL_REVIEW_BUNDLE_READY"
                if not missing
                else "U12506_XI_T_EXTERNAL_REVIEW_BUNDLE_MISSING_INPUTS",
                "galaxy": GALAXY,
                "bundle_dir": str(BUNDLE_ROOT.relative_to(ROOT)),
                "bundle_zip": str(ZIP_PATH.relative_to(ROOT)),
                "n_files_listed": len(manifest),
                "n_missing_inputs": len(missing),
                "missing_inputs": ";".join(missing) if missing else "none",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(DATA / "ugc12506_xi_t_external_review_bundle_summary.csv", index=False)

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(BUNDLE_ROOT.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(BUNDLE_ROOT.parent))

    report = "\n".join(
        [
            "# UGC12506 Xi_t External Review Bundle",
            "",
            "This report records the portable review bundle for the UGC12506 Xi_t source route. It is not an accepted manifest and not an endpoint.",
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Manifest",
            "",
            markdown_table(manifest),
            "",
            "## Claim Boundary",
            "",
            "The bundle is a handoff artifact. It may be sent to a residual-blind reviewer, whose completed response must still pass the response-intake validator.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_external_review_bundle.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
