#!/usr/bin/env python3
"""Consolidate NGC7331 as the expdisk+vertical/outer-warp reference analogue.

This is not a new scorer. It reads small Paper8-derived summary ledgers copied
into Paper9 and records what NGC7331 contributes to the NGC4013 expdisk+WVO
completion path.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM = "ngc7331_source_sharpening_reference_not_new_validation"


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
    onset = pd.read_csv(DATA / "ngc7331_fractional_warp_onset_source_summary.csv").iloc[0]
    freeze = pd.read_csv(DATA / "ngc7331_fractional_onset_v2_replay_freeze_summary.csv").iloc[0]
    replay = pd.read_csv(DATA / "ngc7331_v2_v3_replay_holdout_endpoint_summary.csv").iloc[0]
    exact = pd.read_csv(DATA / "ngc7331_b2_exact_transfer_source_evidence_summary.csv").iloc[0]
    v1 = pd.read_csv(
        DATA / "ngc7331_expdisk_vertical_outer_warp_mixed_accepted_endpoint_summary.csv"
    ).iloc[0]

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "status": "REFERENCE_ANALOG_SOURCE_SHARPENED_REPLAY_POSITIVE_EXACT_TRANSFER_BLOCKED",
                "reference_role": "already_processed_expdisk_vertical_outer_warp_reference",
                "v1_caveated_rmse_km_s": float(v1["rmse_mixed_accepted"]),
                "v3_source_sharpened_rmse_km_s": float(replay["v3_source_sharpened_rmse_km_s"]),
                "v3_minus_v1_rmse_km_s": float(replay["v3_minus_v1_rmse_km_s"]),
                "v3_minus_best_baseline_rmse_km_s": float(
                    replay["v3_minus_best_baseline_rmse_km_s"]
                ),
                "v3_minus_wrong_projection_rmse_km_s": float(
                    replay["v3_minus_wrong_projection_rmse_km_s"]
                ),
                "fractional_onset_kpc": float(onset["approx_warp_onset_kpc"]),
                "fractional_onset_over_rhi": float(onset["approx_warp_onset_over_RHI"]),
                "exact_transfer_blocker": str(exact["next_required_action"]),
                "construction_used_vobs": False,
                "scoring_used_vobs_in_source_audit": False,
                "new_endpoint_validation_claim": False,
                "claim_boundary": CLAIM,
            }
        ]
    )

    layers = pd.DataFrame(
        [
            {
                "layer": "V1_caveated_mixed_endpoint",
                "status": str(v1["endpoint_status"]),
                "what_it_shows": (
                    "The expdisk plus vertical/outer-warp family can beat the "
                    "local baseline and wrong-family controls, but with a broad "
                    "outer-window caveat."
                ),
                "allowed_use_in_paper9": "reference analogue for NGC4013 completion pressure",
                "blocked_use": "fresh population validation",
            },
            {
                "layer": "fractional_onset_source_gate",
                "status": str(onset["source_gate_status"]),
                "what_it_shows": (
                    "A residual-blind outer-warp onset exists: "
                    f"{float(onset['approx_warp_onset_kpc']):.3f} kpc "
                    f"({float(onset['approx_warp_onset_over_RHI']):.3f} RHI)."
                ),
                "allowed_use_in_paper9": "source-sharpening evidence",
                "blocked_use": "retroactive change to V1 endpoint",
            },
            {
                "layer": "V2_V3_replay_holdout",
                "status": str(replay["endpoint_status"]),
                "what_it_shows": (
                    "V3 source-sharpened replay improves V1 by "
                    f"{float(replay['v3_minus_v1_rmse_km_s']):.3f} km/s and "
                    "beats the wrong projection control in the replay packet."
                ),
                "allowed_use_in_paper9": "single-galaxy replay/control support",
                "blocked_use": "updating the accepted V1 endpoint",
            },
            {
                "layer": "exact_transfer_upgrade",
                "status": str(exact["source_evidence_review_status"]),
                "what_it_shows": (
                    "Complex warp context is confirmed, but q_warp amplitude, "
                    "sign, and epsilon_cross bounds are not closed."
                ),
                "allowed_use_in_paper9": "blocker ledger for full kernel",
                "blocked_use": "exact-transfer formula freeze",
            },
        ]
    )
    layers["claim_boundary"] = CLAIM

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N7331_REF_G1_REFERENCE_ANALOG",
                "gate_status": "PASS_REFERENCE_ANALOG",
                "reason": "NGC7331 already has expdisk plus vertical/outer-warp mixed readout evidence.",
            },
            {
                "gate_id": "N7331_REF_G2_SOURCE_SHARPENING",
                "gate_status": "PASS_REPLAY_CONTROL_POSITIVE",
                "reason": "V3 source-sharpened replay improves V1 and beats the wrong projection control.",
            },
            {
                "gate_id": "N7331_REF_G3_EXACT_TRANSFER",
                "gate_status": "BLOCKED_MEASUREMENTS_PENDING",
                "reason": "q_warp amplitude, sign convention, and epsilon_cross bound remain open.",
            },
            {
                "gate_id": "N7331_REF_G4_POPULATION_VALIDATION",
                "gate_status": "BLOCKED_NOT_A_FRESH_HOLDOUT",
                "reason": "This is an already processed reference analogue, not an independent population test.",
            },
        ]
    )
    gates["endpoint_scores_allowed_here"] = False
    gates["claim_boundary"] = CLAIM

    summary_path = DATA / "ngc7331_source_sharpening_reference_summary_v1.csv"
    layers_path = DATA / "ngc7331_source_sharpening_reference_layers_v1.csv"
    gates_path = DATA / "ngc7331_source_sharpening_reference_gates_v1.csv"
    report_path = REPORTS / "ngc7331_source_sharpening_reference_audit.md"

    summary.to_csv(summary_path, index=False)
    layers.to_csv(layers_path, index=False)
    gates.to_csv(gates_path, index=False)

    report = [
        "# NGC7331 Source-Sharpening Reference Audit",
        "",
        "**Doc class:** reference-analogue consolidation audit",
        "",
        "**Reader role:** Paper 9 projection/mixed replay maintainer",
        "",
        "**Status:** `REFERENCE_ANALOG_SOURCE_SHARPENED_REPLAY_POSITIVE_EXACT_TRANSFER_BLOCKED`",
        "",
        f"**Claim boundary:** `{CLAIM}`",
        "",
        "## Purpose",
        "",
        "This audit records what NGC7331 contributes after UGC07151 failed the",
        "fast WVO holdout preflight. It does not run a new score. It consolidates",
        "already generated Paper8 summary artifacts into the Paper9 source-completion",
        "logic.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Layer Ledger",
        "",
        markdown_table(layers),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "NGC7331 is now the strongest reference analogue for the NGC4013 completion",
        "pressure result. It has an exponential-disk carrier plus vertical/outer-warp",
        "mixed route. The V1 accepted endpoint remains caveated by the broad outer",
        "window, but the source-only fractional-onset gate and V3 replay show that",
        "source-sharpening moves in the expected direction.",
        "",
        "The stronger exact-transfer kernel is still blocked. The relevant missing",
        "items are not arbitrary: the complex H I warp context means q_warp amplitude,",
        "sign convention, and cross-term bounds matter and cannot be silently assumed.",
        "",
        "## Allowed Claim",
        "",
        "`NGC7331 supports the expdisk plus vertical/outer-warp family as a",
        "source-sharpened reference analogue, while preserving exact-transfer",
        "blockers and the no-population-validation boundary.`",
        "",
        "## Disallowed Claims",
        "",
        "- no new endpoint score is produced here",
        "- no population validation is claimed here",
        "- the accepted V1 endpoint is not retroactively updated",
        "- exact-transfer formula freeze is not allowed yet",
    ]
    report_path.write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
