#!/usr/bin/env python3
"""Build residual-blind lock-type review for beta-transfer negative triggers.

This records whether the negative beta-transfer control cases are really
beta/compact locks, or whether source morphology supports a different readout
lock type.  The review uses literature/source morphology evidence only; score
outcomes are not used to choose the replacement lock.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "beta_transfer_lock_type_source_review_residual_blind_not_replay"


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

    evidence = pd.DataFrame(
        [
            {
                "galaxy": "NGC0891",
                "source_id": "NASA_HUBBLE_NGC891_EDGE_ON_DUST_GAS",
                "source_url": "https://science.nasa.gov/missions/hubble/hubble-spies-edge-on-beauty/",
                "source_type": "public_hubble_source",
                "residual_blind_field": "edge_on_dust_gas_halo_filaments",
                "source_statement_summary": (
                    "NGC 891 is seen exactly edge-on and shows a thick plane of dust and "
                    "interstellar gas with filaments escaping into the halo."
                ),
                "supports_lock_component": "observer_projection;vertical_dust_gas_overlay;halo_fountain",
                "source_strength": "HIGH",
                "uses_vobs_or_residual": False,
            },
            {
                "galaxy": "NGC0891",
                "source_id": "HOWK_SAVAGE_1997_EXTRAPLANAR_DUST",
                "source_url": "https://arxiv.org/abs/astro-ph/9709197",
                "source_type": "journal_arxiv_abstract",
                "residual_blind_field": "extraplanar_dust_massive_high_z_structures",
                "source_statement_summary": (
                    "High-resolution imaging reveals hundreds of extraplanar dust-absorbing "
                    "structures visible to |z| < 1.5 kpc; associated high-z gas mass likely "
                    "exceeds 2e8 solar masses."
                ),
                "supports_lock_component": "vertical_dust_overlay;thick_disk_halo_source",
                "source_strength": "HIGH",
                "uses_vobs_or_residual": False,
            },
            {
                "galaxy": "NGC0891",
                "source_id": "MOUHCINE_REJKUBA_IBATA_2009_NGC891_STRUCTURE",
                "source_url": "https://academic.oup.com/mnras/article/395/1/126/1079019",
                "source_type": "peer_reviewed_structure_paper",
                "residual_blind_field": "edge_on_disc_halo_hi_halo_structural_complexity",
                "source_statement_summary": (
                    "NGC 891 is almost perfectly edge-on, has substantial H I halo, H-alpha "
                    "envelope, thick-disc/halo structure, and small-scale halo substructure."
                ),
                "supports_lock_component": "hi_halo;thick_disc_halo;history_or_accretion_context",
                "source_strength": "HIGH",
                "uses_vobs_or_residual": False,
            },
            {
                "galaxy": "NGC4217",
                "source_id": "ESA_HUBBLE_NGC4217_DUST_FILAMENTS",
                "source_url": "https://esahubble.org/images/potw1503a/",
                "source_type": "public_hubble_source",
                "residual_blind_field": "edge_on_extraplanar_dust_filaments",
                "source_statement_summary": (
                    "NGC 4217 is seen almost perfectly edge-on and is a candidate for studying "
                    "extraplanar gas/dust structures above and below the plane."
                ),
                "supports_lock_component": "observer_projection;vertical_dust_gas_overlay",
                "source_strength": "HIGH",
                "uses_vobs_or_residual": False,
            },
            {
                "galaxy": "NGC4217",
                "source_id": "ESA_HUBBLE_NGC4217_FILAMENT_GEOMETRY",
                "source_url": "https://esahubble.org/images/potw1503a/",
                "source_type": "public_hubble_source",
                "residual_blind_field": "dust_filament_heights_and_shapes",
                "source_statement_summary": (
                    "The image shows dozens of dust structures, some reaching about 7000 "
                    "light-years from the central plane, including columns, loops, and cones."
                ),
                "supports_lock_component": "vertical_overlay;outflow_or_fountain_geometry",
                "source_strength": "HIGH",
                "uses_vobs_or_residual": False,
            },
            {
                "galaxy": "NGC4217",
                "source_id": "CHANGES_2024_NGC4217_RADIO_BUBBLE",
                "source_url": "https://arxiv.org/abs/2409.15449",
                "source_type": "journal_arxiv_abstract",
                "residual_blind_field": "extra_planar_radio_halo_bubble",
                "source_statement_summary": (
                    "Radio continuum study of edge-on NGC 4217 targets extra-planar cosmic "
                    "rays and magnetic fields; reports a large halo radio-bubble context."
                ),
                "supports_lock_component": "halo_bubble;magnetic_or_cosmic_ray_projection_context",
                "source_strength": "MEDIUM_HIGH",
                "uses_vobs_or_residual": False,
            },
        ]
    )

    lock_rows = [
        {
            "galaxy": "NGC0891",
            "previous_proxy_family": "K_compact_finite",
            "lock_type_verdict": "SOURCE_REJECTS_PURE_BETA_COMPACT_AS_PRIMARY_LOCK",
            "source_supported_lock_type": "K_edgeon_vertical_dust_hi_halo_mixed",
            "readout_lane_pressure": (
                "projection/vertical overlay plus H I halo/history component before any beta-transfer replay"
            ),
            "why_not_curve_fitting": (
                "classification follows edge-on/dust/H I halo literature, not endpoint residual shape"
            ),
            "required_next_sources": (
                "source-native vertical dust/halo support window; H I halo/load profile; bulge/disk split if compact lane is retained as subcomponent"
            ),
            "replay_allowed_now": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4217",
            "previous_proxy_family": "K_compact_finite",
            "lock_type_verdict": "SOURCE_REJECTS_PURE_BETA_COMPACT_AS_PRIMARY_LOCK",
            "source_supported_lock_type": "K_edgeon_vertical_dust_radio_halo_mixed",
            "readout_lane_pressure": (
                "projection/vertical dust overlay with halo/radio-bubble context; compact lane may only be a component"
            ),
            "why_not_curve_fitting": (
                "classification follows edge-on/extraplanar dust/radio halo source evidence, not endpoint score"
            ),
            "required_next_sources": (
                "vertical dust extent/window; S4G/NED bulge-disk decomposition; H I or radio-halo support context"
            ),
            "replay_allowed_now": False,
            "endpoint_scores_allowed": False,
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    lock = pd.DataFrame(lock_rows)

    evidence_path = DATA / "beta_transfer_lock_type_source_review_evidence.csv"
    lock_path = DATA / "beta_transfer_lock_type_source_review.csv"
    summary_path = DATA / "beta_transfer_lock_type_source_review_summary.csv"
    evidence.to_csv(evidence_path, index=False)
    lock.to_csv(lock_path, index=False)

    summary = pd.DataFrame(
        [
            {
                "lock_type_review_status": "LOCK_TYPE_REVIEW_BUILT_SOURCE_REJECTS_PURE_BETA_FOR_NEGATIVE_TRIGGERS",
                "n_galaxies_reviewed": lock["galaxy"].nunique(),
                "n_source_evidence_rows": len(evidence),
                "n_pure_beta_rejections": int(
                    lock["lock_type_verdict"].eq(
                        "SOURCE_REJECTS_PURE_BETA_COMPACT_AS_PRIMARY_LOCK"
                    ).sum()
                ),
                "uses_vobs_or_residual_for_lock_type": False,
                "replay_allowed_now": False,
                "endpoint_scores_allowed": False,
                "next_action": (
                    "derive source-frozen mixed vertical/projection formulas for NGC0891 and NGC4217, "
                    "then run replay only after formula freeze"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(summary_path, index=False)

    report = [
        "# Beta-Transfer Negative Trigger Lock-Type Source Review",
        "",
        "This review asks what kind of lock the negative beta-transfer galaxies appear to be from source morphology alone.",
        "It does not use rotation residuals to choose a replacement readout.",
        "",
        "## Verdict",
        "",
        markdown_table(lock),
        "",
        "## Evidence Ledger",
        "",
        markdown_table(
            evidence[
                [
                    "galaxy",
                    "source_id",
                    "source_url",
                    "residual_blind_field",
                    "supports_lock_component",
                    "source_strength",
                ]
            ]
        ),
        "",
        "## Claim Boundary",
        "",
        "- Pure beta/compact transfer is rejected as the primary lock type for these negative-trigger cases.",
        "- This is a source-side morphology/readout review, not a replay and not endpoint validation.",
        "- Any new scoring run must first freeze a replacement formula from source-native fields.",
        "- Forbidden inputs remain rotation residuals, endpoint RMSE, wrong-family ranks, required-S diagnostics, and posthoc kernel tuning.",
        "",
    ]
    report_path = REPORTS / "beta_transfer_lock_type_source_review.md"
    report_path.write_text("\n".join(report), encoding="utf-8")

    print(summary.to_string(index=False))
    print(f"wrote {evidence_path}")
    print(f"wrote {lock_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
