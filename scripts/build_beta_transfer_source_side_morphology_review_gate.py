#!/usr/bin/env python3
"""Build a source-side morphology review gate for beta-transfer control results.

The beta-closure transfer score can trigger a review, but it cannot choose a
new readout family.  This gate records that separation explicitly: score
outcomes are diagnostic triggers only, while the review targets are inferred
from residual-blind morphology/source proxies already present in the manifests.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

SCORE_SUMMARY = DATA / "ugc12506_beta_closure_transfer_comparison_figure_summary.csv"
POINTS = DATA / "ugc12506_beta_closure_transfer_scoring_points.csv"
MORPH = DATA / "morphology_parameter_manifest.csv"

CLAIM_BOUNDARY = "beta_transfer_source_side_morphology_review_gate_not_endpoint"


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


def boolish(value: object) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def source_review_target(row: pd.Series) -> tuple[str, str, str, str]:
    """Return source-only review target, rationale, needed sources, and status."""
    inc = float(row.get("inclination_deg", 0.0) or 0.0)
    max_bulge = float(row.get("max_bulge", 0.0) or 0.0)
    mean_bulge = float(row.get("mean_bulge", 0.0) or 0.0)
    mean_gas = float(row.get("mean_gas", 0.0) or 0.0)
    caveat = str(row.get("manifest_caveat", ""))
    family = str(row.get("formula_family", ""))

    edge_on = inc >= 80.0
    bulge_dominated = max_bulge >= 0.7 or mean_bulge >= 0.25
    gas_rich = mean_gas >= 0.10
    vertical_caveat = "vertical" in caveat.lower()
    distance_caveat = "distance" in caveat.lower()

    if edge_on and bulge_dominated:
        return (
            "K_edgeon_compact_vertical_overlay_or_bulge_split",
            (
                f"source proxies show edge-on geometry (i={inc:.0f} deg) plus a strong compact/bulge "
                f"component (max_bulge={max_bulge:.2f}, mean_bulge={mean_bulge:.2f}); beta-transfer "
                "should not be promoted unless the compact carrier and vertical/projection layer are "
                "separately frozen"
            ),
            "S4G/NED bulge-disk decomposition; vertical/dust-lane evidence; H I extent/asymmetry if available",
            "REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY",
        )
    if edge_on and vertical_caveat:
        return (
            "K_thick_flared_or_projection_dominated",
            (
                f"source proxies show edge-on/high-inclination geometry (i={inc:.0f} deg) with vertical "
                "geometry caveat; review should decide whether projection/vertical overlay, not beta-transfer, "
                "is the matched readout"
            ),
            "S4G/NED vertical morphology notes; DustPedia/HI support; optional path/projection caveat",
            "REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY",
        )
    if gas_rich and family in {"K_thick_flared", "K_scale_tail_spiral"}:
        return (
            "K_outer_hi_support_or_scale_tail_mixed",
            (
                f"source proxies show non-negligible gas support (mean_gas={mean_gas:.2f}) in a "
                f"{family} lane; review should test outer H I support/history before beta-transfer replay"
            ),
            "H I extent/asymmetry; tail/warp onset; outer support radius; source-native active window",
            "REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY",
        )
    if distance_caveat:
        return (
            "K_distance_caveated_control_only",
            "large distance caveat prevents strong formula-family promotion without distance/provenance review",
            "NED distance provenance; SPARC distance uncertainty review; do not endpoint-score as clean case",
            "BLOCKED_DISTANCE_OR_PROVENANCE_REVIEW",
        )
    return (
        "K_beta_transfer_compatibility_review",
        (
            "available source proxies do not reject beta-transfer, but the branch remains a transfer-control "
            "candidate until morphology/source review confirms a matched lane"
        ),
        "spin route provenance; carrier provenance; external morphology source cross-check",
        "REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY",
    )


def trigger_status(delta: float) -> tuple[str, str]:
    if delta < -5.0:
        return (
            "NEGATIVE_SCORE_TRIGGER_REVIEW_ONLY",
            "beta-transfer worsens carrier; open source-side morphology/reprojection review, not retuning",
        )
    if delta <= 5.0:
        return (
            "WEAK_OR_NEUTRAL_SCORE_TRIGGER_REVIEW_ONLY",
            "beta-transfer is weak/neutral; review whether this is the correct readout family",
        )
    return (
        "POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION",
        "beta-transfer improves carrier; still requires matched source-family review before endpoint claims",
    )


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    scores = pd.read_csv(SCORE_SUMMARY)
    morph = pd.read_csv(MORPH)
    points = pd.read_csv(POINTS)

    morph = morph.drop_duplicates("galaxy")
    merged = scores.merge(morph, on="galaxy", how="left", suffixes=("", "_morph"))
    point_counts = (
        points.groupby("galaxy", as_index=False)
        .agg(
            n_scored_points=("radius_kpc", "size"),
            r_min_kpc=("radius_kpc", "min"),
            r_max_kpc=("radius_kpc", "max"),
            beta_cl_value=("beta_cl_value", "first"),
        )
    )
    merged = merged.merge(point_counts, on="galaxy", how="left")

    rows = []
    for _, row in merged.iterrows():
        delta = float(row["delta_carrier_minus_beta_km_s"])
        trigger, trigger_note = trigger_status(delta)
        target, rationale, needed_sources, review_status = source_review_target(row)
        rows.append(
            {
                "galaxy": row["galaxy"],
                "score_trigger_status": trigger,
                "score_trigger_note": trigger_note,
                "carrier_rmse_km_s": row["carrier_rmse_km_s"],
                "beta_rmse_km_s": row["beta_rmse_km_s"],
                "delta_carrier_minus_beta_km_s": delta,
                "score_may_choose_family": False,
                "current_proxy_family": row.get("formula_family", ""),
                "source_side_review_target": target,
                "source_side_rationale_no_vobs": rationale,
                "needed_residual_blind_sources": needed_sources,
                "source_review_status": review_status,
                "inclination_deg": row.get("inclination_deg", pd.NA),
                "max_bulge": row.get("max_bulge", pd.NA),
                "mean_bulge": row.get("mean_bulge", pd.NA),
                "mean_gas": row.get("mean_gas", pd.NA),
                "manifest_caveat": row.get("manifest_caveat", ""),
                "beta_cl_value": row.get("beta_cl_value", pd.NA),
                "n_scored_points": row.get("n_scored_points", pd.NA),
                "r_min_kpc": row.get("r_min_kpc", pd.NA),
                "r_max_kpc": row.get("r_max_kpc", pd.NA),
                "forbidden_inputs_for_review": (
                    "rotation residuals; endpoint RMSE; wrong-family rank; required_S_tau; "
                    "posthoc amplitude/sign/radial-window tuning"
                ),
                "allowed_next_action": (
                    "collect_or_review_source_evidence_then_freeze_replacement_label_before_any_replay"
                ),
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    review = pd.DataFrame(rows).sort_values(
        ["score_trigger_status", "delta_carrier_minus_beta_km_s"],
        ascending=[True, True],
    )
    review_path = DATA / "beta_transfer_source_side_morphology_review_gate.csv"
    review.to_csv(review_path, index=False)

    summary = pd.DataFrame(
        [
            {
                "review_gate_status": "BETA_TRANSFER_SOURCE_SIDE_MORPHOLOGY_REVIEW_GATE_BUILT_NO_REPLAY",
                "n_galaxies": len(review),
                "n_negative_score_triggers": int(
                    review["score_trigger_status"].eq("NEGATIVE_SCORE_TRIGGER_REVIEW_ONLY").sum()
                ),
                "n_weak_or_neutral_triggers": int(
                    review["score_trigger_status"].eq("WEAK_OR_NEUTRAL_SCORE_TRIGGER_REVIEW_ONLY").sum()
                ),
                "n_positive_control_signals": int(
                    review["score_trigger_status"].eq(
                        "POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION"
                    ).sum()
                ),
                "n_review_targets": int(review["source_side_review_target"].nunique()),
                "uses_vobs_or_residual_for_family_choice": False,
                "scores_used_only_as_audit_trigger": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_action": (
                    "run independent residual-blind morphology/source review for negative and weak triggers; "
                    "only then freeze replacement labels and replay"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary_path = DATA / "beta_transfer_source_side_morphology_review_gate_summary.csv"
    summary.to_csv(summary_path, index=False)

    excerpt_cols = [
        "galaxy",
        "score_trigger_status",
        "delta_carrier_minus_beta_km_s",
        "current_proxy_family",
        "source_side_review_target",
        "source_review_status",
        "needed_residual_blind_sources",
    ]
    report = [
        "# Beta-transfer Source-Side Morphology Review Gate",
        "",
        "This gate prevents the beta-transfer control score from becoming a curve-fitting selector.",
        "Scores can trigger review, but they cannot choose the morphology/readout family.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Review Queue",
        "",
        markdown_table(review[excerpt_cols]),
        "",
        "## Claim Boundary",
        "",
        "- This is not endpoint validation.",
        "- Negative beta-transfer cases are preserved as diagnostic triggers.",
        "- Any replacement label must be source-frozen from residual-blind evidence before replay.",
        "- Forbidden for review: rotation residuals, endpoint RMSE, wrong-family ranks, required-S diagnostics, and posthoc amplitude/sign/radial-window tuning.",
        "",
    ]
    report_path = REPORTS / "beta_transfer_source_side_morphology_review_gate.md"
    report_path.write_text("\n".join(report), encoding="utf-8")

    print(summary.to_string(index=False))
    print(f"wrote {review_path}")
    print(f"wrote {summary_path}")
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
