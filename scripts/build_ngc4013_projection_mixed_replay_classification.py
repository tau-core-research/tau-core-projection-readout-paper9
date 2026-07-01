#!/usr/bin/env python3
"""Classify the NGC4013 mixed-projection replay under the non-overlap ledger.

This is an audit builder, not a scorer. It reads already frozen NGC4013
scoring artifacts plus the source-token non-overlap ledger and writes the
current claim-safe interpretation. No observed velocities or residual arrays
are read here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ngc4013_projection_mixed_replay_classification_not_validation"


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
    wvo = pd.read_csv(DERIVED / "ngc4013_warp_vertical_overlay_endpoint_scores.csv").iloc[0]
    protocol = pd.read_csv(DERIVED / "ngc4013_expdisk_wvo_frozen_protocol_scores.csv").iloc[0]
    control = pd.read_csv(DERIVED / "ngc4013_warp_vertical_overlay_control_summary.csv")
    radial = pd.read_csv(DERIVED / "ngc4013_warp_vertical_overlay_radial_zone_summary.csv")
    gates = pd.read_csv(DERIVED / "ngc4013_projection_mixed_nonoverlap_gates_v1.csv")

    gate_status = dict(zip(gates["gate_id"], gates["gate_status"]))

    replay = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "route": "original_compact_proxy",
                "rmse_km_s": wvo["rmse_original_compact_family"],
                "previous_score_role": "baseline_for_morphology_refinement",
                "nonoverlap_classification": "SOURCE_REJECTED_STARTING_PROXY",
                "allowed_after_nonoverlap": False,
                "endpoint_validation_claim": False,
                "uses_vobs_or_residual_in_construction": False,
                "scoring_used_vobs": True,
                "reason": "Retained only as the rejected/refined-away starting proxy.",
                "claim_boundary": CLAIM,
            },
            {
                "galaxy": "NGC4013",
                "route": "warp_vertical_overlay",
                "rmse_km_s": wvo["rmse_warp_vertical_overlay"],
                "previous_score_role": "caveated_preliminary_endpoint_control",
                "nonoverlap_classification": "CAVEATED_WVO_MIXED_REPLAY_ALLOWED",
                "allowed_after_nonoverlap": gate_status.get(
                    "N4013_NONOVERLAP_G2_WVO_MIXED_ROUTE"
                )
                == "PASS_CAVEATED_REPLAY_ALLOWED",
                "endpoint_validation_claim": False,
                "uses_vobs_or_residual_in_construction": False,
                "scoring_used_vobs": True,
                "reason": (
                    "Warp, vertical, lag, and observer/path tokens are assigned "
                    "to one WVO/mixed projection contribution without independent Xi_t reuse."
                ),
                "claim_boundary": CLAIM,
            },
            {
                "galaxy": "NGC4013",
                "route": "exponential_disk_plus_wvo_frozen_protocol",
                "rmse_km_s": protocol["rmse_expdisk_wvo_frozen_protocol"],
                "previous_score_role": "prospective_protocol_score_not_retroactive_endpoint",
                "nonoverlap_classification": "PROSPECTIVE_PROTOCOL_ONLY",
                "allowed_after_nonoverlap": False,
                "endpoint_validation_claim": False,
                "uses_vobs_or_residual_in_construction": False,
                "scoring_used_vobs": True,
                "reason": (
                    "Best NGC4013 score in this packet, but the non-overlap ledger "
                    "does not retroactively promote it to endpoint validation."
                ),
                "claim_boundary": CLAIM,
            },
        ]
    )

    control_summary = control.copy()
    control_summary["claim_boundary"] = CLAIM
    radial_summary = radial.copy()
    radial_summary["claim_boundary"] = CLAIM

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4013",
                "status": "WVO_MIXED_REPLAY_ALLOWED_XIT_BLOCKED_EXPDISK_WVO_PROSPECTIVE",
                "allowed_replay_route": "warp_vertical_overlay",
                "blocked_route": "independent_Xi_t_clock_overlay",
                "prospective_only_route": "exponential_disk_plus_wvo_frozen_protocol",
                "wvo_rmse_km_s": float(
                    replay.loc[replay["route"] == "warp_vertical_overlay", "rmse_km_s"].iloc[0]
                ),
                "wvo_minus_tpg_v6_km_s": float(wvo["wvo_minus_tpg_v6"]),
                "wvo_minus_mond_km_s": float(wvo["wvo_minus_mond"]),
                "wvo_minus_compact_proxy_km_s": float(wvo["wvo_minus_original_compact"]),
                "matched_minus_wrong_mean_km_s": float(
                    control_summary["matched_minus_wrong_mean"].iloc[0]
                ),
                "matched_minus_wrong_best_km_s": float(
                    control_summary["matched_minus_wrong_best"].iloc[0]
                ),
                "matched_beats_all_wrong_families": bool(
                    control_summary["matched_beats_all_wrong_families"].iloc[0]
                ),
                "active_window_weighted_wvo_minus_tpg_rmse": float(
                    radial_summary["active_window_weighted_wvo_minus_tpg_rmse"].iloc[0]
                ),
                "compact_proxy_rmse_km_s": float(
                    replay.loc[replay["route"] == "original_compact_proxy", "rmse_km_s"].iloc[0]
                ),
                "expdisk_wvo_protocol_rmse_km_s": float(
                    replay.loc[
                        replay["route"] == "exponential_disk_plus_wvo_frozen_protocol",
                        "rmse_km_s",
                    ].iloc[0]
                ),
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    replay_path = DERIVED / "ngc4013_projection_mixed_replay_classification_v1.csv"
    summary_path = DERIVED / "ngc4013_projection_mixed_replay_classification_summary_v1.csv"
    report_path = REPORTS / "ngc4013_projection_mixed_replay_classification.md"

    replay.to_csv(replay_path, index=False)
    summary.to_csv(summary_path, index=False)

    report = [
        "# NGC4013 Projection/Mixed Replay Classification",
        "",
        "**Doc class:** replay classification audit",
        "",
        "**Reader role:** Paper 9 projection/mixed endpoint maintainer",
        "",
        "**Status:** `WVO_MIXED_REPLAY_ALLOWED_XIT_BLOCKED_EXPDISK_WVO_PROSPECTIVE`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "This audit applies the NGC4013 source-token non-overlap ledger to the",
        "existing score ladder. It does not introduce a new score and does not",
        "read observed velocities or residuals. Its role is to say which old",
        "number can be interpreted as a caveated replay/control result after the",
        "source channels have been separated.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Route Classification",
        "",
        markdown_table(replay),
        "",
        "## Wrong-Family Control",
        "",
        markdown_table(control_summary),
        "",
        "## Radial-Zone Diagnostic",
        "",
        markdown_table(radial_summary),
        "",
        "## Interpretation",
        "",
        "The source-supported route is the warp/vertical-overlay mixed projection",
        "route. It improves the rejected compact proxy from 16.99 km/s to 11.45",
        "km/s RMSE, and the source-token ledger permits it as a caveated replay",
        "because the warp, vertical, lag, and observer/path evidence are assigned",
        "to one shared mixed-projection contribution.",
        "",
        "The wrong-family control is deliberately preserved as a caveat: WVO beats",
        "the wrong-family mean but not the best wrong-family control. The correct",
        "status is therefore caveated replay/control evidence, not endpoint",
        "validation.",
        "",
        "The radial-zone diagnostic says the WVO lane is an outer-lane correction:",
        "it is inactive in the inner pre-warp window and improves the active outer",
        "window relative to the TPG/v6 carrier.",
        "",
        "The independent clock/time route remains blocked. The available facts",
        "are exactly the morphology/projection facts already used by WVO, so using",
        "them again as `Xi_t` would double-count the same source tokens.",
        "",
        "The exponential-disk plus WVO protocol remains prospective-only. Its",
        "10.61 km/s score is useful as a protocol target, but not retroactive",
        "endpoint validation.",
        "",
        "## Allowed Claim",
        "",
        "`NGC4013 shows source-supported morphology/projection refinement evidence",
        "for the WVO mixed route, under caveated single-galaxy replay/control",
        "status.`",
        "",
        "## Disallowed Claims",
        "",
        "- population validation",
        "- retroactive validation of the expdisk+WVO protocol score",
        "- independent `Xi_t` endpoint for NGC4013 from the same source tokens",
        "- a new gravitational-law claim",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
