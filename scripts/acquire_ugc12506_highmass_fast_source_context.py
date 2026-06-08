#!/usr/bin/env python3
"""Record fast UGC12506 source context from Hallenbeck et al. 2014.

This acquisition cache supports rapid projection-enriched triage.  It records
residual-blind H I/projection statements for UGC12506 from the HIghMass VLA
paper without freezing a Tau Core formula or scoring an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from run_source_native_readout_formula_endpoint import markdown_table


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
PDF = ROOT / "data" / "external" / "literature" / "ugc12506_highmass_hi_context" / (
    "hallenbeck_2014_highmass_ugc12506.pdf"
)
TXT = PDF.with_suffix(".txt")
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_highmass_fast_source_context_not_kernel_freeze"
ARXIV_URL = "https://arxiv.org/abs/1407.1744"
PDF_URL = "https://arxiv.org/pdf/1407.1744"
DOI = "10.1088/0004-6256/148/4/69"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    if not PDF.exists():
        raise FileNotFoundError(f"Missing cached PDF: {PDF}")
    if not TXT.exists():
        raise FileNotFoundError(f"Missing extracted text: {TXT}")

    source = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "source_name": "Hallenbeck et al. 2014 HIghMass VLA imaging",
                "source_url": ARXIV_URL,
                "pdf_url": PDF_URL,
                "doi": DOI,
                "local_pdf": str(PDF.relative_to(ROOT)),
                "local_text": str(TXT.relative_to(ROOT)),
                "source_status": "CACHED_AND_TEXT_EXTRACTED",
                "machine_readable_text": True,
                "machine_readable_radial_profile": False,
                "residual_blind": True,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    evidence = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "evidence_id": "UGC12506_HM_E1_HIGH_INCLINATION_PV_REQUIRED",
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "evidence_type": "projection_context",
                "text_line_range": "206-225,681-690",
                "paraphrased_evidence": (
                    "The galaxy is highly inclined, so velocity-field curves underestimate "
                    "rotation and the authors use a position-velocity/envelope method."
                ),
                "supports_field": "projection_enriched_kernel_candidate",
                "freezes_kernel_value": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "UGC12506_HM_E2_EXTENDED_HI_SUPPORT",
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "evidence_type": "hi_extent_context",
                "text_line_range": "666-673",
                "paraphrased_evidence": (
                    "The H I disk is traced beyond 60 kpc and the observed H I radius "
                    "is reported as 58 +/- 2 kpc, consistent with the expected radius."
                ),
                "supports_field": "outer_support_window",
                "freezes_kernel_value": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "UGC12506_HM_E3_ORDERED_BUT_ASYMMETRIC_PV",
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "evidence_type": "projection_asymmetry_context",
                "text_line_range": "680-696",
                "paraphrased_evidence": (
                    "The galaxy shows ordered rotation to the detectable edge, but the "
                    "approaching and receding sides differ in shape and length."
                ),
                "supports_field": "projection_or_lopsided_support_context",
                "freezes_kernel_value": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "UGC12506_HM_E4_LOW_DENSITY_STABLE_HI",
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "evidence_type": "closure_stability_context",
                "text_line_range": "719-735",
                "paraphrased_evidence": (
                    "UGC12506 has low H I surface densities, typically 1-5 Msun/pc^2 "
                    "out to 60 kpc, and is described as stable over most of the disk."
                ),
                "supports_field": "closure_load_context",
                "freezes_kernel_value": False,
            },
            {
                "galaxy": GALAXY,
                "evidence_id": "UGC12506_HM_E5_HIGH_SPIN_CONTEXT",
                "source_id": "UGC12506_HI_SRC1_HIGHMASS_VLA",
                "evidence_type": "history_memory_context",
                "text_line_range": "768-774",
                "paraphrased_evidence": (
                    "The paper reports a very high spin parameter for UGC12506, "
                    "interpreted as an unusual gas-rich high-spin state."
                ),
                "supports_field": "memory_history_or_high_spin_context",
                "freezes_kernel_value": False,
            },
        ]
    )
    evidence["residual_blind"] = True
    evidence["claim_boundary"] = CLAIM_BOUNDARY

    candidate_fields = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "candidate_field": "projection_load_from_high_inclination_pv",
                "field_status": "CONTEXT_SUPPORTED_VALUES_OPEN",
                "source_basis": "high-inclination PV/envelope-tracing method",
                "why_open": "no predeclared normalized e_proj value has been extracted",
            },
            {
                "galaxy": GALAXY,
                "candidate_field": "outer_hi_support_window",
                "field_status": "NUMERIC_CONTEXT_AVAILABLE_NOT_FORMULA_FREEZE",
                "source_basis": "H I traced beyond 60 kpc; observed H I radius 58 +/- 2 kpc in source",
                "why_open": "needs mapping into a kernel window and amplitude rule",
            },
            {
                "galaxy": GALAXY,
                "candidate_field": "closure_stability_load",
                "field_status": "CONTEXT_SUPPORTED_VALUES_OPEN",
                "source_basis": "low density stable H I disk, stability thresholds discussed",
                "why_open": "no normalized z_cl(R) field is frozen",
            },
            {
                "galaxy": GALAXY,
                "candidate_field": "history_memory_high_spin_load",
                "field_status": "CONTEXT_SUPPORTED_VALUES_OPEN",
                "source_basis": "reported high spin parameter lambda=0.15",
                "why_open": "needs residual-blind Tau-side mapping before use in a kernel",
            },
        ]
    )
    candidate_fields["uses_vobs_or_residual"] = False
    candidate_fields["formula_freeze_allowed"] = False
    candidate_fields["endpoint_scores_allowed"] = False
    candidate_fields["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "context_status": "UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN",
                "galaxy": GALAXY,
                "source_cached": True,
                "text_extracted": True,
                "n_evidence_rows": len(evidence),
                "supports_projection_context": True,
                "supports_outer_hi_context": True,
                "supports_closure_stability_context": True,
                "supports_history_memory_context": True,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_acquisition": False,
                "recommended_next_gate": (
                    "build_ugc12506_projection_highspin_formula_preflight_from_source_context"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    source.to_csv(DATA / "ugc12506_highmass_fast_source_context_source.csv", index=False)
    evidence.to_csv(DATA / "ugc12506_highmass_fast_source_context_evidence.csv", index=False)
    candidate_fields.to_csv(
        DATA / "ugc12506_highmass_fast_source_context_candidate_fields.csv", index=False
    )
    summary.to_csv(DATA / "ugc12506_highmass_fast_source_context_summary.csv", index=False)

    report = [
        "# UGC12506 HIghMass Fast Source Context",
        "",
        "This acquisition cache records residual-blind source context for UGC12506",
        "from Hallenbeck et al. 2014.  It supports a projection-enriched/high-spin",
        "candidate route, but does not freeze a Tau Core formula and does not score",
        "an endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source",
        "",
        markdown_table(source),
        "",
        "## Evidence",
        "",
        markdown_table(evidence),
        "",
        "## Candidate Fields",
        "",
        markdown_table(candidate_fields),
        "",
        "## Claim Boundary",
        "",
        "The source provides strong context for high-inclination projection, extended",
        "H I support, low-density stable gas, and high-spin/history interpretation.",
        "It does not by itself freeze `e_proj`, `z_cl(R)`, a kernel amplitude, or an",
        "endpoint-ready formula.",
    ]
    (REPORTS / "ugc12506_highmass_fast_source_context.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
