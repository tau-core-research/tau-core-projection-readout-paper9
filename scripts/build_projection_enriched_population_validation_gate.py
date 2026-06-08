#!/usr/bin/env python3
"""Build the projection-enriched population validation gate.

This is a protocol/readiness gate, not a rotation-curve scoring run.  It turns
the four-object projection-enriched audit into a predeclared population
validation target: source-frozen observer/projection labels must choose the
enriched family before endpoint scoring, and the matched enriched family must
be tested against simpler proxies, wrong enriched families, shuffled projection
labels, and conventional baselines.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_enriched_population_validation_gate_not_endpoint"


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


def source_status_for(galaxy: str) -> tuple[str, str, str]:
    """Return source-field summary, projection label, and caveat for a candidate."""
    mapping = {
        "NGC4013": (
            "H I lag/warp context plus vertical-structure source support",
            "warp_vertical_overlay",
            "retrospective mixed-reference case; needs prospective replay",
        ),
        "NGC5907": (
            "edge-on geometry, warp/truncation, projection/ISM source context",
            "edge_on_projection_vertical_warp",
            "fresh single-galaxy preliminary control; wrong-label replay remains tight",
        ),
        "NGC7331": (
            "H I warp/history plus vertical-scale source context",
            "vertical_outer_warp_overlay",
            "broad outer-warp window and wrong-label replay caveats",
        ),
        "NGC4088": (
            "H I geometry, strong distortion, P-V asymmetry, asymmetric warp, companion context",
            "warp_history_asymmetric_projection",
            "source-review, memory/asymmetry, epsilon_cross, and normalization-law caveats",
        ),
    }
    return mapping[galaxy]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    audit = pd.read_csv(DATA / "projection_enriched_candidate_kernel_audit.csv")
    rotation = pd.read_csv(DATA / "projection_enriched_rotation_comparison_summary.csv")

    protocol = pd.DataFrame(
        [
            {
                "gate_id": "PEV1_SOURCE_FROZEN_PROJECTION_LABEL",
                "required_condition": "observer/projection labels are assigned from external source fields before scoring",
                "pass_measure": "projection_label_source_status is accepted_or_caveated_source_frozen and construction_used_vobs=False",
                "failure_mode": "projection label inferred from residual shape, RMSE, or endpoint score",
            },
            {
                "gate_id": "PEV2_ENRICHED_KERNEL_FREEZE",
                "required_condition": "component kernels, observer weights, signs, windows, carrier, and amplitude policy are frozen before scoring",
                "pass_measure": "formula_freeze_manifest exists and forbidden endpoint fields are absent",
                "failure_mode": "component weight or activation window changed after seeing residuals",
            },
            {
                "gate_id": "PEV3_MATCHED_VS_SIMPLER_PROXY",
                "required_condition": "matched projection-enriched kernel beats the simpler pre-enrichment morphology proxy",
                "pass_measure": "RMSE_original_proxy - RMSE_projection_enriched > 0",
                "failure_mode": "projection layer adds flexibility without improving the source-matched simpler proxy",
            },
            {
                "gate_id": "PEV4_MATCHED_VS_WRONG_ENRICHED",
                "required_condition": "correct enriched label beats wrong enriched families under the same scoring rules",
                "pass_measure": "RMSE_wrong_enriched_mean - RMSE_matched_enriched > 0 and correct rank is high",
                "failure_mode": "wrong enriched labels perform as well as the source-matched label",
            },
            {
                "gate_id": "PEV5_SHUFFLED_PROJECTION_NULL",
                "required_condition": "source-frozen projection labels beat shuffled observer/projection labels",
                "pass_measure": "matched-vs-shuffled p-value and effect size pass predeclared threshold",
                "failure_mode": "signal survives random projection-label assignment",
            },
            {
                "gate_id": "PEV6_BASELINE_COMPARISON",
                "required_condition": "matched enriched readout is compared with Newtonian, MOND/RAR, TPG/v6, and RMOND-facing comparators",
                "pass_measure": "baseline competitiveness reported without claiming universal superiority unless population endpoint passes",
                "failure_mode": "baseline comparison omitted or overclaimed",
            },
            {
                "gate_id": "PEV7_PATH_AWARE_CLAIM_BOUNDARY",
                "required_condition": "approximate source-plus-observer kernels are separated from the full path-aware Tau Core kernel",
                "pass_measure": "path-environment term is marked not modeled unless a path catalogue exists",
                "failure_mode": "four-object source/projection audit is overread as full path-aware validation",
            },
        ]
    )
    protocol["claim_boundary"] = CLAIM_BOUNDARY

    cases = []
    for _, row in audit.iterrows():
        galaxy = str(row["galaxy"])
        source_fields, projection_label, source_caveat = source_status_for(galaxy)
        rotation_row = rotation.loc[rotation["galaxy"].eq(galaxy)].iloc[0]
        endpoint_allowed = bool(row["endpoint_scores_allowed"])
        strict_replay = str(row["strict_replay_wrong_label_result"])
        prospective_population_use = (
            "candidate_for_population_protocol_after_freeze_review"
            if endpoint_allowed
            else "blocked_not_population_use"
        )
        if "does_not_beat_best_wrong_label" in strict_replay:
            prospective_population_use = "candidate_but_wrong_label_replay_caveated"
        if galaxy == "NGC4013":
            prospective_population_use = "retrospective_reference_case_not_fresh_population_validation"
        if galaxy == "NGC4088":
            prospective_population_use = "strong_visual_case_but_source_review_and_normalization_caveated"

        cases.append(
            {
                "galaxy": galaxy,
                "source_fields_used": source_fields,
                "source_frozen_projection_label": projection_label,
                "matched_enriched_lane": row["projection_enriched_lane"],
                "simpler_proxy": str(rotation_row["original_proxy"]).replace("original proxy: ", ""),
                "matched_rmse_km_s": row["matched_rmse_km_s"],
                "simpler_proxy_rmse_km_s": rotation_row["rmse_original_km_s"],
                "matched_minus_simpler_km_s": rotation_row["improved_minus_original_km_s"],
                "best_baseline_model": row["best_baseline_model"],
                "matched_minus_best_baseline_km_s": row["matched_minus_best_baseline_km_s"],
                "matched_minus_wrong_mean_km_s": row["matched_minus_wrong_mean_km_s"],
                "strict_wrong_label_status": strict_replay,
                "construction_used_vobs": bool(row["construction_used_vobs"]),
                "endpoint_scores_allowed": endpoint_allowed,
                "population_validation_use": prospective_population_use,
                "source_caveat": source_caveat,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    cases_df = pd.DataFrame(cases)

    endpoints = pd.DataFrame(
        [
            {
                "endpoint_id": "DELTA_ENRICHED_SIMPLER",
                "definition": "RMSE(simpler morphology-only proxy) - RMSE(matched projection-enriched kernel)",
                "pass_condition": "positive mean/median and positive family-balanced result on predeclared catalogue",
                "current_status": "four-object candidate audit positive; not population validation",
            },
            {
                "endpoint_id": "DELTA_ENRICHED_WRONG",
                "definition": "RMSE(wrong projection-enriched family mean) - RMSE(matched projection-enriched family)",
                "pass_condition": "positive on predeclared projection-enriched catalogue",
                "current_status": "caveated; NGC5907 and NGC7331 do not yet beat best wrong mixed labels",
            },
            {
                "endpoint_id": "SHUFFLED_PROJECTION_LABEL_NULL",
                "definition": "matched enriched score compared with shuffled observer/projection labels",
                "pass_condition": "predeclared p-value/effect-size threshold",
                "current_status": "not run for projection-enriched population catalogue",
            },
            {
                "endpoint_id": "BASELINE_COMPETITIVENESS",
                "definition": "matched enriched readout versus Newtonian, MOND/RAR, TPG/v6, and RMOND-facing comparators",
                "pass_condition": "reported without universal superiority unless population endpoint passes",
                "current_status": "four-object candidate audit positive against listed best baselines",
            },
            {
                "endpoint_id": "PATH_ENVIRONMENT_ABLATION",
                "definition": "compare source-only, source-plus-observer, and future path-environment kernels",
                "pass_condition": "observer/path layer improves only where source labels predict it",
                "current_status": "future; no path-environment catalogue in current paper",
            },
        ]
    )
    endpoints["claim_boundary"] = CLAIM_BOUNDARY

    min_catalogue_cases_required = 12
    min_fresh_cases_required = 8
    n_cases = len(cases_df)
    n_allowed = int(cases_df["endpoint_scores_allowed"].sum())
    n_beats_simpler = int((cases_df["matched_minus_simpler_km_s"] < 0).sum())
    n_beats_baseline = int((cases_df["matched_minus_best_baseline_km_s"] < 0).sum())
    n_strict_wrong_caveated = int(
        cases_df["strict_wrong_label_status"].astype(str).str.contains("does_not_beat").sum()
    )
    population_ready = n_cases >= min_catalogue_cases_required and n_strict_wrong_caveated == 0

    summary = pd.DataFrame(
        [
            {
                "validation_gate_status": (
                    "PROJECTION_ENRICHED_POPULATION_VALIDATION_READY"
                    if population_ready
                    else "PROJECTION_ENRICHED_POPULATION_VALIDATION_BLOCKED_CATALOGUE_AND_WRONG_LABEL_GATES"
                ),
                "n_projection_enriched_candidates_listed": n_cases,
                "n_endpoint_scores_allowed_single_object": n_allowed,
                "n_matched_beats_simpler_proxy": n_beats_simpler,
                "n_matched_beats_best_listed_baseline": n_beats_baseline,
                "n_cases_with_strict_wrong_label_caveat": n_strict_wrong_caveated,
                "min_catalogue_cases_required": min_catalogue_cases_required,
                "min_fresh_cases_required": min_fresh_cases_required,
                "endpoint_scores_run_here": False,
                "diagnostic_scores_used_as_label_input": False,
                "current_claim": (
                    "four-object audit motivates projection-enriched population validation "
                    "but remains kernel-development evidence"
                ),
                "next_required_action": (
                    "build a residual-blind projection-enriched catalogue with source-frozen "
                    "observer/projection labels, then run matched-vs-simpler, wrong-enriched, "
                    "shuffled-label, and baseline endpoints"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    protocol.to_csv(DATA / "projection_enriched_population_validation_protocol.csv", index=False)
    cases_df.to_csv(DATA / "projection_enriched_population_validation_cases.csv", index=False)
    endpoints.to_csv(DATA / "projection_enriched_population_validation_endpoints.csv", index=False)
    summary.to_csv(DATA / "projection_enriched_population_validation_summary.csv", index=False)

    report = [
        "# Projection-Enriched Population Validation Gate",
        "",
        "This gate turns the four-object projection-enriched audit into a",
        "predeclared population validation target.  It does not run endpoint",
        "scoring and does not promote the four-object audit to validation.",
        "",
        "## Protocol",
        "",
        markdown_table(protocol),
        "",
        "## Current Projection-Enriched Cases",
        "",
        markdown_table(cases_df),
        "",
        "## Endpoints To Run After Catalogue Freeze",
        "",
        markdown_table(endpoints),
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Claim Boundary",
        "",
        "The present four-object audit motivates, but does not establish,",
        "population validation.  A valid population test requires a predeclared",
        "projection-enriched catalogue in which source-frozen observer/projection",
        "labels select the enriched kernel family before endpoint scoring.",
    ]
    (REPORTS / "projection_enriched_population_validation_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(f"wrote {DATA / 'projection_enriched_population_validation_protocol.csv'}")
    print(f"wrote {DATA / 'projection_enriched_population_validation_cases.csv'}")
    print(f"wrote {DATA / 'projection_enriched_population_validation_endpoints.csv'}")
    print(f"wrote {DATA / 'projection_enriched_population_validation_summary.csv'}")
    print(f"wrote {REPORTS / 'projection_enriched_population_validation_gate.md'}")


if __name__ == "__main__":
    main()
