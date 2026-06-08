#!/usr/bin/env python3
"""Build the problematic-galaxy projection-channel candidate ledger.

This is a source/route interpretation artifact, not an endpoint scoring script.
It records which Tau morphology-state projection channels are currently
plausible for the inspected stress, improving, neutral, and worsened galaxies.
No observed residuals are used to promote a channel; the listed next gates are
source-freeze or ablation tasks.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "problematic_projection_channel_ledger_not_endpoint"


ROWS = [
    {
        "galaxy": "UGC12506",
        "current_role": "primary_stress_case_underpredicted",
        "current_response": "time/projection control improves but leaves large gap",
        "priority_channel": "mass_distribution_plus_metric_closure",
        "secondary_channels": "observer_path_edgeon_projection; clock_readout_interval",
        "why_plausible": (
            "high inclination, high spin, extended low-density H I envelope, and "
            "source-native NFW/HSE context point to an envelope/closure readout "
            "that is stronger than the current small Xi_t cap"
        ),
        "blocked_or_forbidden": (
            "do not raise Xi_t amplitude from the rotation residual; path term "
            "remains zero until source/path evidence establishes it"
        ),
        "next_gate": (
            "derive source-frozen mass/envelope plus metric-closure readout and "
            "run ablation against Theta_morph and Xi_t cap-only controls"
        ),
        "endpoint_allowed_now": False,
        "evidence_status": "candidate_channel_strong_stress_not_endpoint",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC4088",
        "current_role": "improving_warp_history_asymmetry_case",
        "current_response": "time/projection control improves clearly",
        "priority_channel": "trajectory_phase_asymmetry_history",
        "secondary_channels": "clock_readout_control_only",
        "why_plausible": (
            "source-side warp, asymmetry, and history context make an unsettled "
            "trajectory/phase readout natural; the clock replay improves but "
            "overlaps the accepted additive warp/history kernel"
        ),
        "blocked_or_forbidden": (
            "do not promote lower-RMSE additive-plus-clock stress curve until "
            "clock evidence is non-overlapping with the additive morphology route"
        ),
        "next_gate": (
            "keep accepted additive warp/history endpoint with Xi_eff=1; use "
            "clock replay as control unless independent clock evidence appears"
        ),
        "endpoint_allowed_now": False,
        "evidence_status": "accepted_additive_route_clock_control_only",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC4013",
        "current_role": "worsened_mixed_overlay_case",
        "current_response": "current Xi_t proxy worsens by double-counting",
        "priority_channel": "mixed_warp_vertical_overlay",
        "secondary_channels": "none_for_current_Xi_t",
        "why_plausible": (
            "edge-on warp and vertical overlay source context already enter the "
            "mixed kernel; the generic clock factor rescales the same geometry"
        ),
        "blocked_or_forbidden": (
            "no new Xi_t endpoint from current proxy; keep Xi_t=1 unless a fresh "
            "non-overlapping clock/readout observable is source-frozen"
        ),
        "next_gate": (
            "seek a fresh uninspected analogue or independent clock observable; "
            "otherwise preserve as retrospective mixed-reference control"
        ),
        "endpoint_allowed_now": False,
        "evidence_status": "current_clock_proxy_rejected_double_count",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC7331",
        "current_role": "worsened_broad_outer_warp_case",
        "current_response": "current Xi_t proxy worsens mildly by over-rescaling",
        "priority_channel": "source_sharpened_vertical_outer_warp",
        "secondary_channels": "metric_closure_after_window_sharpening",
        "why_plausible": (
            "the present broad vertical/outer-warp mixed window already carries "
            "the available phase information; a sharper source-native outer-warp "
            "onset is needed before adding any clock or closure layer"
        ),
        "blocked_or_forbidden": (
            "do not add Xi_t on the broad-window proxy; do not interpret the mild "
            "degradation as a Tau Core failure"
        ),
        "next_gate": (
            "source-sharpen outer-warp/vertical window, then test metric/closure "
            "or refined mixed readout by replay before endpoint promotion"
        ),
        "endpoint_allowed_now": False,
        "evidence_status": "broad_window_saturated_refinement_required",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC5907",
        "current_role": "near_neutral_projection_saturated_case",
        "current_response": "time/projection proxy nearly neutral to slightly worse",
        "priority_channel": "observer_path_edgeon_projection",
        "secondary_channels": "warp_truncation_projection",
        "why_plausible": (
            "edge-on line-of-sight stacking and warp/truncation make observer "
            "projection the natural channel, but the current projection kernel "
            "appears saturated"
        ),
        "blocked_or_forbidden": (
            "no clock/time promotion from present neutral replay"
        ),
        "next_gate": (
            "treat as projection-saturated control; only source-native path or "
            "vertical-profile data can justify a richer channel"
        ),
        "endpoint_allowed_now": False,
        "evidence_status": "projection_channel_saturated_control",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC4183",
        "current_role": "weak_null_projection_control",
        "current_response": "time/projection layer nearly null",
        "priority_channel": "quiet_weak_projection_limit",
        "secondary_channels": "none",
        "why_plausible": (
            "weak-projection tilted-ring source context supports a quiet/null "
            "limit rather than an extra active projection channel"
        ),
        "blocked_or_forbidden": (
            "do not introduce active time, mass, or closure channels without new "
            "source evidence"
        ),
        "next_gate": "retain as null/weak-projection control",
        "endpoint_allowed_now": False,
        "evidence_status": "null_control_keep_low_channel",
        "claim_boundary": CLAIM_BOUNDARY,
    },
]


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in df.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    ledger = pd.DataFrame(ROWS)
    summary = pd.DataFrame(
        [
            {
                "ledger_status": "PROBLEMATIC_GALAXY_PROJECTION_CHANNEL_LEDGER_BUILT_NOT_ENDPOINT",
                "n_galaxies": int(len(ledger)),
                "n_endpoint_allowed_now": int(ledger["endpoint_allowed_now"].sum()),
                "interpretation": (
                    "candidate projection channels are identified, but every "
                    "new channel remains source-freeze/ablation gated"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    ledger.to_csv(DATA / "problematic_galaxy_projection_channel_ledger.csv", index=False)
    summary.to_csv(DATA / "problematic_galaxy_projection_channel_summary.csv", index=False)

    compact_cols = [
        "galaxy",
        "current_role",
        "priority_channel",
        "secondary_channels",
        "evidence_status",
        "next_gate",
    ]
    report = [
        "# Problematic Galaxy Projection-Channel Candidate Ledger",
        "",
        "This ledger records which additional Tau morphology-state projection",
        "channels are plausible for the inspected problematic or caveated",
        "galaxies. It is not endpoint scoring and it does not promote any new",
        "rotation-curve correction.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Compact Ledger",
        "",
        markdown_table(ledger[compact_cols]),
        "",
        "## Guardrail",
        "",
        "A channel is not allowed into endpoint scoring merely because it is",
        "plausible. It must be source-frozen, assigned to a distinct ledger",
        "channel, checked for overlap with active kernels, and tested by ablation.",
        "",
    ]
    (REPORTS / "problematic_galaxy_projection_channel_ledger.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(ledger[compact_cols].to_string(index=False))


if __name__ == "__main__":
    main()
