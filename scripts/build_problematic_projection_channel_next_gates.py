#!/usr/bin/env python3
"""Build next-gate execution plan for problematic projection channels.

This script follows the problematic projection-channel ledger and converts the
route interpretation into executable next gates. It does not score new
endpoints. Rows either point to an already runnable control replay, a
source-freeze obligation, or a blocked route.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "problematic_projection_channel_next_gates_not_endpoint"


def exists(name: str) -> bool:
    return (DATA / name).exists()


def read_status(name: str, column: str, default: str = "MISSING") -> str:
    path = DATA / name
    if not path.exists():
        return default
    df = pd.read_csv(path)
    if df.empty or column not in df.columns:
        return default
    return str(df.iloc[0][column])


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
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    ledger = pd.read_csv(DATA / "problematic_galaxy_projection_channel_ledger.csv")

    rows = [
        {
            "galaxy": "UGC12506",
            "next_gate_id": "U12506_MASS_ENVELOPE_METRIC_CLOSURE_ABLATION_GATE",
            "priority_channel": "mass_distribution_plus_metric_closure",
            "gate_status": (
                "CONTROL_REPLAY_READY_ENDPOINT_BLOCKED"
                if exists("ugc12506_source_native_nfw_hse_replay_summary.csv")
                else "SOURCE_NATIVE_REPLAY_MISSING"
            ),
            "ready_scripts": (
                "build_ugc12506_source_native_nfw_hse_shell.py; "
                "run_ugc12506_source_native_nfw_hse_replay.py"
            ),
            "required_comparison": (
                "ablate source-native NFW/HSE against Theta_morph-only, "
                "Theta+Xi_t cap-only, and source-envelope controls"
            ),
            "scoring_allowed_now": exists("ugc12506_source_native_nfw_hse_replay_summary.csv"),
            "endpoint_allowed_now": False,
            "reason": (
                "strong stress case remains underpredicted; existing source-native "
                "NFW/HSE control is the concrete mass/envelope plus closure seed"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4088",
            "next_gate_id": "N4088_CLOCK_NONOVERLAP_EVIDENCE_GATE",
            "priority_channel": "trajectory_phase_asymmetry_history",
            "gate_status": "NO_NEW_ENDPOINT_KEEP_ACCEPTED_ADDITIVE_ROUTE",
            "ready_scripts": (
                "run_ngc4088_warp_history_accepted_endpoint.py; "
                "run_ngc4088_time_projection_ablation_control_replay.py"
            ),
            "required_comparison": (
                "preserve clock replay as control; reopen clock endpoint only with "
                "new non-overlapping source clock evidence"
            ),
            "scoring_allowed_now": True,
            "endpoint_allowed_now": False,
            "reason": (
                "accepted additive warp/history route already exists; clock replay "
                "improves but overlaps additive evidence"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4013",
            "next_gate_id": "N4013_FRESH_ANALOGUE_OR_CLOCK_OBSERVABLE_GATE",
            "priority_channel": "mixed_warp_vertical_overlay",
            "gate_status": "BLOCKED_CURRENT_XIT_REJECTED",
            "ready_scripts": "build_ngc4013_predeclared_replay_holdout_gate.py",
            "required_comparison": (
                "find uninspected analogue or independent clock observable before "
                "any new scoring"
            ),
            "scoring_allowed_now": False,
            "endpoint_allowed_now": False,
            "reason": "current Xi_t proxy double-counts the mixed warp/vertical-overlay kernel",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC7331",
            "next_gate_id": "N7331_SOURCE_SHARPENED_OUTER_WARP_GATE",
            "priority_channel": "source_sharpened_vertical_outer_warp",
            "gate_status": (
                "REPLAY_PATH_EXISTS_ENDPOINT_NOT_PROMOTED"
                if exists("ngc7331_things_qwarp_first_pass_summary.csv")
                else "QWARP_SOURCE_MEASUREMENT_MISSING"
            ),
            "ready_scripts": (
                "build_ngc7331_things_qwarp_first_pass_measurement.py; "
                "build_ngc7331_qwarp_observable_choice_review_gate.py; "
                "build_ngc7331_qwarp_review_intake_formula_freeze_gate.py"
            ),
            "required_comparison": (
                "freeze narrower q_warp/vertical window before testing metric/closure "
                "or refined mixed replay"
            ),
            "scoring_allowed_now": False,
            "endpoint_allowed_now": False,
            "reason": (
                "current broad outer-warp window is saturated; source sharpening "
                "must precede any extra clock or closure layer"
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC5907",
            "next_gate_id": "N5907_PATH_VERTICAL_PROFILE_ONLY_GATE",
            "priority_channel": "observer_path_edgeon_projection",
            "gate_status": "SATURATED_CONTROL_NO_NEW_LAYER",
            "ready_scripts": "run_ngc5907_projection_accepted_endpoint.py",
            "required_comparison": (
                "only source-native path/vertical-profile evidence can justify "
                "a richer kernel"
            ),
            "scoring_allowed_now": False,
            "endpoint_allowed_now": False,
            "reason": "current projection kernel is already saturated at proxy level",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        {
            "galaxy": "NGC4183",
            "next_gate_id": "N4183_NULL_CONTROL_KEEP_LOW_CHANNEL_GATE",
            "priority_channel": "quiet_weak_projection_limit",
            "gate_status": "RETAIN_NULL_CONTROL",
            "ready_scripts": "run_ngc4183_weak_projection_null_control_accepted_endpoint.py",
            "required_comparison": "no active projection channel without new source evidence",
            "scoring_allowed_now": False,
            "endpoint_allowed_now": False,
            "reason": "weak/null projection control should remain low-channel",
            "claim_boundary": CLAIM_BOUNDARY,
        },
    ]
    gates = pd.DataFrame(rows)
    gates = gates.merge(
        ledger[["galaxy", "current_role", "evidence_status"]],
        on="galaxy",
        how="left",
    )
    gates = gates[
        [
            "galaxy",
            "current_role",
            "priority_channel",
            "next_gate_id",
            "gate_status",
            "evidence_status",
            "required_comparison",
            "ready_scripts",
            "scoring_allowed_now",
            "endpoint_allowed_now",
            "reason",
            "claim_boundary",
        ]
    ]
    summary = pd.DataFrame(
        [
            {
                "next_gate_status": "PROBLEMATIC_PROJECTION_CHANNEL_NEXT_GATES_BUILT_NOT_ENDPOINT",
                "n_galaxies": int(len(gates)),
                "n_control_or_scoring_allowed": int(gates["scoring_allowed_now"].sum()),
                "n_endpoint_allowed": int(gates["endpoint_allowed_now"].sum()),
                "ugc12506_shell_status": read_status(
                    "ugc12506_source_native_nfw_hse_shell_summary.csv",
                    "formula_shell_status",
                ),
                "ngc7331_qwarp_status": read_status(
                    "ngc7331_things_qwarp_first_pass_summary.csv",
                    "qwarp_first_pass_status",
                ),
                "interpretation": (
                    "UGC12506 and NGC4088 have control/replay paths; all endpoint "
                    "promotions remain blocked by source-freeze or non-overlap gates"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates.to_csv(DATA / "problematic_projection_channel_next_gates.csv", index=False)
    summary.to_csv(DATA / "problematic_projection_channel_next_gates_summary.csv", index=False)

    report = [
        "# Problematic Projection-Channel Next Gates",
        "",
        "This artifact converts the projection-channel ledger into executable next",
        "gates. It does not run or authorize endpoint scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(
            gates[
                [
                    "galaxy",
                    "priority_channel",
                    "gate_status",
                    "required_comparison",
                    "endpoint_allowed_now",
                ]
            ]
        ),
        "",
    ]
    (REPORTS / "problematic_projection_channel_next_gates.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(gates.to_string(index=False))


if __name__ == "__main__":
    main()
