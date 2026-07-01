#!/usr/bin/env python3
"""Select prospective expdisk+WVO analogues after the NGC4013 completion audit.

This is not a scorer. It consolidates existing source/projection ledgers to
identify where the NGC4013 mixed readout can be tested prospectively without
using the NGC4013 residual shape to promote a retrospective endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ngc4013_expdisk_wvo_analog_selection_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = [
        "| " + " | ".join(cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        vals: list[str] = []
        for col in cols:
            value = row[col]
            if pd.isna(value):
                vals.append("")
            elif isinstance(value, float):
                vals.append(f"{value:.6g}")
            else:
                vals.append(str(value))
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


def main() -> None:
    completion = pd.read_csv(DATA / "ngc4013_morphology_completion_pressure_summary_v1.csv").iloc[0]
    population = pd.read_csv(DATA / "projection_enriched_population_validation_cases.csv")
    queue = pd.read_csv(DATA / "projection_queue_fast_priority.csv")
    trial = pd.read_csv(DATA / "full_time_morphology_trial_galaxy_summary.csv")
    ugc07151_preflight_path = DATA / "ugc07151_expdisk_wvo_source_preflight_summary_v1.csv"
    ugc07151_preflight = (
        pd.read_csv(ugc07151_preflight_path).iloc[0]
        if ugc07151_preflight_path.exists()
        else None
    )

    def population_row(galaxy: str) -> pd.Series | None:
        match = population[population["galaxy"] == galaxy]
        return None if match.empty else match.iloc[0]

    def queue_row(galaxy: str) -> pd.Series | None:
        match = queue[queue["galaxy"] == galaxy]
        return None if match.empty else match.iloc[0]

    def trial_row(galaxy: str) -> pd.Series | None:
        match = trial[trial["galaxy"] == galaxy]
        return None if match.empty else match.iloc[0]

    candidates: list[dict[str, object]] = []

    for galaxy, role, selection_status, next_action in [
        (
            "NGC7331",
            "closest already-scored expdisk plus vertical/outer-warp analogue",
            "REFERENCE_ANALOG_ALREADY_SCORED_CAVEATED_NOT_FRESH_HOLDOUT",
            "use as logic/reference analogue only; source-sharpen the outer-warp window before any stronger claim",
        ),
        (
            "NGC5907",
            "edge-on projection/vertical-warp analogue",
            "PROJECTION_ANALOG_NOT_EXPDISK_WVO_EXACT",
            "retain as projection-saturated control unless source-native vertical profile data justify a richer replay",
        ),
        (
            "NGC4183",
            "quiet exponential-disk / weak-projection control",
            "QUIET_OR_WEAK_PROJECTION_CONTROL",
            "retain as null/weak-projection control; do not force WVO if source morphology remains quiet",
        ),
        (
            "UGC07151",
            "fresh exponential-disk projection queue candidate",
            (
                "FAST_PREFLIGHT_WVO_BLOCKED_EDGEON_TRUNCATION_CONTROL"
                if ugc07151_preflight is not None
                else "SOURCE_ACQUISITION_REQUIRED_ORIENTATION_GATE_BLOCKED"
            ),
            (
                "preserve as edge-on/truncation control unless independent WVO/onset evidence is acquired"
                if ugc07151_preflight is not None
                else "resolve source-native orientation plus vertical/warp evidence before any expdisk+WVO replay"
            ),
        ),
        (
            "UGC12506",
            "stress exponential-disk projection candidate",
            "STRESS_CASE_NOT_CLEAN_WVO_ANALOG",
            "keep as stress/path-closure case; not the clean first test of NGC4013 expdisk+WVO completion",
        ),
    ]:
        prow = population_row(galaxy)
        qrow = queue_row(galaxy)
        trow = trial_row(galaxy)

        candidates.append(
            {
                "galaxy": galaxy,
                "analog_role": role,
                "selection_status": selection_status,
                "source_fields_or_label": (
                    "" if prow is None else str(prow.get("source_fields_used", ""))
                ),
                "projection_label": (
                    str(prow.get("source_frozen_projection_label", ""))
                    if prow is not None
                    else ("" if qrow is None else str(qrow.get("projection_label", "")))
                ),
                "available_rmse_context": (
                    ""
                    if prow is None
                    else f"matched={float(prow['matched_rmse_km_s']):.3f}; "
                    f"delta_simpler={float(prow['matched_minus_simpler_km_s']):.3f}; "
                    f"delta_wrong_mean={float(prow['matched_minus_wrong_mean_km_s']):.3f}"
                ),
                "queue_priority": "" if qrow is None else str(qrow.get("priority_tier", "")),
                "primary_blocker": (
                    str(ugc07151_preflight["wvo_source_support"])
                    if galaxy == "UGC07151" and ugc07151_preflight is not None
                    else (
                        str(qrow.get("primary_blocker", ""))
                        if qrow is not None
                        else (
                            "" if prow is None else str(prow.get("source_caveat", ""))
                        )
                    )
                ),
                "full_time_trial_context": (
                    ""
                    if trow is None
                    else f"source={trow['source_status']}; "
                    f"delta={float(trow['full_time_minus_base_rmse_km_s']):.6f}"
                ),
                "recommended_next_action": next_action,
                "allowed_endpoint_use_now": False,
                "uses_vobs_or_residual_for_selection": False,
                "claim_boundary": CLAIM,
            }
        )

    candidates_df = pd.DataFrame(candidates)

    summary = pd.DataFrame(
        [
            {
                "status": "EXPDISK_WVO_ANALOG_SELECTION_READY_NOT_ENDPOINT",
                "ngc4013_completion_verdict": completion["completion_verdict"],
                "ngc4013_matched_minus_best_wrong_km_s": completion[
                    "matched_minus_best_wrong_km_s"
                ],
                "ngc4013_prospective_mixed_rmse_km_s": completion[
                    "prospective_mixed_rmse_km_s"
                ],
                "primary_reference_analog": "NGC7331",
                "fresh_holdout_candidate": "UGC07151_if_source_orientation_and_warp_pass",
                "fresh_holdout_status": (
                    "UGC07151_fast_preflight_blocks_WVO"
                    if ugc07151_preflight is not None
                    else "UGC07151_unresolved"
                ),
                "quiet_control": "NGC4183",
                "stress_not_clean_analog": "UGC12506",
                "endpoint_scores_run_here": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    rules = pd.DataFrame(
        [
            {
                "rule_id": "A1",
                "rule": "An analog may be selected from source morphology/projection ledgers, not from residual shape.",
                "status": "ACTIVE",
            },
            {
                "rule_id": "A2",
                "rule": "NGC4013 expdisk+WVO remains prospective-only and cannot be retroactively promoted.",
                "status": "ACTIVE",
            },
            {
                "rule_id": "A3",
                "rule": "Existing scored analogues can serve as references, but not as fresh holdout validation.",
                "status": "ACTIVE",
            },
            {
                "rule_id": "A4",
                "rule": "A fresh candidate needs source-native regular disk carrier plus independent vertical/warp/onset support.",
                "status": "ACTIVE",
            },
            {
                "rule_id": "A5",
                "rule": "Quiet disks and stress/path-closure cases are controls, not forced WVO successes.",
                "status": "ACTIVE",
            },
        ]
    )
    rules["claim_boundary"] = CLAIM

    candidates_path = DATA / "ngc4013_expdisk_wvo_analog_selection_v1.csv"
    summary_path = DATA / "ngc4013_expdisk_wvo_analog_selection_summary_v1.csv"
    rules_path = DATA / "ngc4013_expdisk_wvo_analog_selection_rules_v1.csv"
    report_path = REPORTS / "ngc4013_expdisk_wvo_analog_selection.md"

    candidates_df.to_csv(candidates_path, index=False)
    summary.to_csv(summary_path, index=False)
    rules.to_csv(rules_path, index=False)

    report = [
        "# NGC4013 Expdisk+WVO Prospective Analog Selection",
        "",
        "**Doc class:** source-side analog selection audit",
        "",
        "**Reader role:** Paper 9 projection/mixed replay maintainer",
        "",
        "**Status:** `EXPDISK_WVO_ANALOG_SELECTION_READY_NOT_ENDPOINT`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "NGC4013 showed a useful but dangerous pattern: the pure WVO route is",
        "source-supported in the outer lane, while the best wrong-family control is",
        "`K_exponential_disk`. The correct interpretation is not that a wrong label",
        "wins, but that the source-supported readout is undercomplete unless a",
        "regular disk carrier is combined with the WVO correction.",
        "",
        "This audit therefore selects prospective analogues and controls for testing",
        "the mixed `exponential disk + WVO` idea without promoting the existing",
        "NGC4013 score retroactively.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Selection Rules",
        "",
        markdown_table(rules),
        "",
        "## Candidate Ledger",
        "",
        markdown_table(candidates_df),
        "",
        "## Verdict",
        "",
        "The strongest already processed analogue is NGC7331, because it already has",
        "an exponential-disk carrier plus vertical/outer-warp mixed route. It is not",
        "a fresh holdout, so it should be used as a reference analogue and not as",
        "new validation.",
        "",
        "NGC5907 is useful as an edge-on projection analogue, but not an exact",
        "expdisk+WVO analogue. NGC4183 is useful as a quiet/weak-projection control.",
        "UGC12506 is a stress/path-closure case, not the clean first test of this",
        "specific completion. UGC07151 was the fastest fresh queue candidate; the",
        "fast preflight now treats it as edge-on/truncation control unless",
        "independent WVO/onset evidence is acquired.",
        "",
        "## Next Finite Action",
        "",
        "For a clean prospective test, either source-sharpen the already processed",
        "NGC7331 vertical/outer-warp reference analogue, or acquire a new",
        "exponential-disk candidate with independent vertical/warp/onset support.",
        "The candidate can then freeze the expdisk+WVO formula before scoring.",
        "Until that source freeze exists, NGC4013 remains a morphology",
        "completion-pressure case rather than a validation endpoint.",
        "",
        "## Disallowed Claims",
        "",
        "- no endpoint validation is claimed here",
        "- no population validation is claimed here",
        "- NGC4013 expdisk+WVO is not retroactively promoted",
        "- quiet controls are not forced into WVO",
        "- stress/path-closure galaxies are not treated as clean WVO analogues",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
