#!/usr/bin/env python3
"""Build the projection-enriched population-validation expansion ledger.

This script does not score rotation curves.  It asks whether the current
projection-enriched programme has enough residual-blind, source-frozen objects
to become a population validation run, and if not, which objects and source
fields are the next acquisition targets.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_enriched_population_expansion_ledger_not_endpoint"


SEED_CASES = [
    {
        "galaxy": "NGC4013",
        "role": "scored_seed_retrospective",
        "projection_label": "warp_vertical_overlay",
        "readout_lane": "expdisk_warp_vertical_overlay",
        "population_use": "reference_only_not_fresh",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "endpoint_scored_retrospective",
        "primary_blocker": "retrospective_reference_case",
        "next_action": "prospective replay only; do not count as fresh catalogue case",
    },
    {
        "galaxy": "NGC5907",
        "role": "scored_seed_wrong_label_caveated",
        "projection_label": "edge_on_projection_vertical_warp",
        "readout_lane": "expdisk_projection_vertical_warp_context",
        "population_use": "candidate_after_wrong_label_replay",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "accepted_single_object_freeze",
        "primary_blocker": "strict_wrong_label_margin_tight",
        "next_action": "predeclare wrong enriched label replay before population use",
    },
    {
        "galaxy": "NGC7331",
        "role": "scored_seed_wrong_label_caveated",
        "projection_label": "vertical_outer_warp_overlay",
        "readout_lane": "expdisk_vertical_outer_warp_overlay",
        "population_use": "candidate_after_wrong_label_replay",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "accepted_single_object_freeze",
        "primary_blocker": "strict_wrong_label_margin_tight_outer_window_broad",
        "next_action": "freeze narrower source-native outer-warp window and rerun wrong-label replay",
    },
    {
        "galaxy": "NGC4088",
        "role": "scored_seed_source_review_caveated",
        "projection_label": "warp_history_asymmetric_projection",
        "readout_lane": "warp_history_asymmetric_projection",
        "population_use": "candidate_after_source_review",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "accepted_single_object_freeze_caveated",
        "primary_blocker": "source_review_and_normalization_caveats",
        "next_action": "complete source review, epsilon/memory normalization, and wrong-label replay",
    },
]


KNOWN_BLOCKED_CANDIDATES = [
    {
        "galaxy": "NGC4183",
        "role": "weak_projection_null_control",
        "projection_label": "edge_on_outer_warp_caveated",
        "readout_lane": "K_expdisk_edge_on_projection_outer_warp_caveated",
        "population_use": "null_control_candidate",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "weak_projection_interval_control_complete",
        "primary_blocker": "strong_projection_not_supported",
        "next_action": "retain as weak/null projection control; do not count as positive enriched case",
    },
    {
        "galaxy": "NGC3198",
        "role": "frozen_protocol_transfer_seed_not_validation",
        "projection_label": "vertical_projection_constant_h_epg",
        "readout_lane": "K_thick_flared_constant_h_projection_context",
        "population_use": "transfer_rule_seed_not_fresh_validation",
        "fresh_population_case": False,
        "endpoint_score_available": True,
        "formula_freeze_status": "source_derived_constant_h_protocol_frozen_not_retroactive",
        "primary_blocker": "retroactive_diagnostic_history_transfer_required",
        "next_action": "apply frozen constant-H EPG rule to a future predeclared fresh case",
    },
    {
        "galaxy": "IC4202",
        "role": "formula_blocked_candidate",
        "projection_label": "edge_on_smooth_disk_projection",
        "readout_lane": "K_edge_on_smooth_disk_closure_projection_candidate",
        "population_use": "candidate_after_formula_values",
        "fresh_population_case": True,
        "endpoint_score_available": False,
        "formula_freeze_status": "formula_shell_derived_freeze_blocked",
        "primary_blocker": "projection_load_values_and_closure_normalization_unfrozen",
        "next_action": "resolve source-native H I regularity closure map or scalar-to-kernel theorem",
    },
]


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


def promotion_queue_from_memory_gate() -> pd.DataFrame:
    gate = pd.read_csv(DATA / "memory_projection_acceptance_gate.csv")
    holdout = gate[gate["split"].eq("holdout")].copy()

    candidates = holdout[
        holdout["projection_status"].eq("PROJECTION_ACCEPTANCE_READY_RESIDUAL_BLIND")
    ].copy()
    candidates = candidates[
        ~candidates["galaxy"].isin({row["galaxy"] for row in SEED_CASES + KNOWN_BLOCKED_CANDIDATES})
    ]

    def blocker(row: pd.Series) -> str:
        if row["orientation_gate_status"] != "ORIENTATION_PROMOTION_READY_FOR_ACTIVE_COMPONENTS":
            return "orientation_gate_blocked"
        if row["memory_status"] != "MEMORY_NOT_REQUIRED_CURRENT_READOUT_CONSISTENT":
            return "memory_or_history_acceptance_blocked"
        return "formula_shell_not_built"

    def next_action(row: pd.Series) -> str:
        b = blocker(row)
        if b == "orientation_gate_blocked":
            return "resolve source-native orientation promotion before projection catalogue use"
        if b == "memory_or_history_acceptance_blocked":
            return "replace inverse memory proxy with residual-blind source/history evidence or mark memory not required"
        return "derive projection-enriched formula shell and freeze source inputs"

    candidates["role"] = "fresh_projection_catalogue_queue"
    candidates["projection_label"] = candidates["formula_family"].map(
        lambda value: f"projection_review_for_{value}"
    )
    candidates["readout_lane"] = candidates["formula_family"].map(
        lambda value: f"{value}_projection_enriched_candidate"
    )
    candidates["population_use"] = "fresh_candidate_after_gate_resolution"
    candidates["fresh_population_case"] = True
    candidates["endpoint_score_available"] = False
    candidates["formula_freeze_status"] = "not_built"
    candidates["primary_blocker"] = candidates.apply(blocker, axis=1)
    candidates["next_action"] = candidates.apply(next_action, axis=1)

    cols = [
        "galaxy",
        "role",
        "projection_label",
        "readout_lane",
        "population_use",
        "fresh_population_case",
        "endpoint_score_available",
        "formula_freeze_status",
        "primary_blocker",
        "next_action",
        "formula_family",
        "orientation_gate_status",
        "memory_status",
        "inclination_deg",
        "manifest_confidence",
        "manifest_caveat",
    ]
    return candidates[cols].sort_values(["primary_blocker", "galaxy"])


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rows = SEED_CASES + KNOWN_BLOCKED_CANDIDATES
    base = pd.DataFrame(rows)
    base = base.assign(
        formula_family="",
        orientation_gate_status="",
        memory_status="",
        inclination_deg=float("nan"),
        manifest_confidence=float("nan"),
        manifest_caveat="",
    )

    queue = promotion_queue_from_memory_gate()
    ledger = pd.concat([base, queue], ignore_index=True, sort=False)
    ledger["uses_vobs_or_residual_for_label"] = False
    ledger["endpoint_scores_run_by_this_script"] = False
    ledger["claim_boundary"] = CLAIM_BOUNDARY

    min_catalogue_cases_required = 12
    min_fresh_cases_required = 8
    n_scored_seed = int(ledger["endpoint_score_available"].sum())
    n_fresh_queue = int(ledger["fresh_population_case"].sum())
    n_formula_blocked = int(
        ledger["formula_freeze_status"].astype(str).str.contains("blocked|not_built", case=False).sum()
    )
    n_source_blocked = int(
        ledger["primary_blocker"].astype(str).str.contains("orientation|memory|source", case=False).sum()
    )
    n_wrong_label_caveated = int(
        ledger["primary_blocker"].astype(str).str.contains("wrong_label", case=False).sum()
    )
    n_catalogue_candidates = int(len(ledger))
    ready_for_population = (
        n_catalogue_candidates >= min_catalogue_cases_required
        and n_fresh_queue >= min_fresh_cases_required
        and n_formula_blocked == 0
        and n_wrong_label_caveated == 0
    )

    summary = pd.DataFrame(
        [
            {
                "expansion_status": (
                    "PROJECTION_ENRICHED_POPULATION_CATALOGUE_READY"
                    if ready_for_population
                    else "PROJECTION_ENRICHED_POPULATION_CATALOGUE_EXPANSION_BLOCKED"
                ),
                "n_catalogue_rows_listed": n_catalogue_candidates,
                "n_scored_seed_or_control_rows": n_scored_seed,
                "n_fresh_population_candidate_rows": n_fresh_queue,
                "n_formula_or_kernel_blocked_rows": n_formula_blocked,
                "n_source_or_orientation_blocked_rows": n_source_blocked,
                "n_wrong_label_caveated_seed_rows": n_wrong_label_caveated,
                "min_catalogue_cases_required": min_catalogue_cases_required,
                "min_fresh_cases_required": min_fresh_cases_required,
                "endpoint_scores_run_here": False,
                "diagnostic_scores_used_as_label_input": False,
                "current_claim": (
                    "there are enough plausible projection-rich rows to define an expansion queue, "
                    "but not enough formula-frozen fresh rows for population validation"
                ),
                "next_required_action": (
                    "resolve source/orientation/memory blockers and build formula freeze manifests "
                    "for at least eight fresh projection-enriched candidates before endpoint scoring"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    acquisition_queue = ledger[
        ledger["fresh_population_case"].astype(bool)
        & ~ledger["endpoint_score_available"].astype(bool)
    ].copy()
    acquisition_queue = acquisition_queue[
        [
            "galaxy",
            "role",
            "projection_label",
            "readout_lane",
            "primary_blocker",
            "next_action",
            "formula_family",
            "inclination_deg",
            "manifest_confidence",
            "manifest_caveat",
            "claim_boundary",
        ]
    ]

    ledger.to_csv(DATA / "projection_enriched_population_expansion_ledger.csv", index=False)
    acquisition_queue.to_csv(
        DATA / "projection_enriched_population_expansion_acquisition_queue.csv", index=False
    )
    summary.to_csv(DATA / "projection_enriched_population_expansion_summary.csv", index=False)

    report = [
        "# Projection-Enriched Population Expansion Ledger",
        "",
        "This ledger is a population-validation preparation artifact.  It does not",
        "score rotation curves and it does not promote the four-object projection",
        "audit to population validation.",
        "",
        "Claim-boundary check: this ledger does not score rotation curves.",
        "Claim-boundary check: No endpoint scores are computed here.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Catalogue Ledger",
        "",
        markdown_table(
            ledger[
                [
                    "galaxy",
                    "role",
                    "projection_label",
                    "readout_lane",
                    "population_use",
                    "fresh_population_case",
                    "endpoint_score_available",
                    "formula_freeze_status",
                    "primary_blocker",
                    "next_action",
                ]
            ]
        ),
        "",
        "## Fresh Acquisition / Freeze Queue",
        "",
        markdown_table(acquisition_queue),
        "",
        "## Claim Boundary",
        "",
        "The listed rows are a source-side expansion queue.  A Paper 2 population",
        "validation run remains blocked until at least eight fresh candidates have",
        "source-frozen projection labels, formula-freeze manifests, wrong-label",
        "controls, and shuffled projection-label nulls.  No endpoint scores are",
        "computed here.",
    ]
    (REPORTS / "projection_enriched_population_expansion_ledger.md").write_text(
        "\n".join(report) + "\n"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
