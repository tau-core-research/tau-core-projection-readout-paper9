#!/usr/bin/env python3
"""Build a compact taxonomy of projection/readout channels used in Paper 2.

This is a documentation artifact: it records where each channel is used,
whether it is endpoint-active, control-only, or future/protocol-only, and what
guardrail prevents overclaiming.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "projection_channel_taxonomy_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in df.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rows = [
        {
            "channel": "present morphology readout",
            "meaning": "projected present-day source structure used to select the base morphology kernel",
            "paper2_use": "main operational layer",
            "example_galaxies": "NGC4013, NGC7331, NGC5907, NGC4088, UGC12506",
            "status": "endpoint-active where source-frozen; otherwise proxy/control",
            "guardrail": "must be source-selected before scoring; not inferred from residuals",
        },
        {
            "channel": "observer/path projection",
            "meaning": "how the source is read from the observer's line of sight or path geometry",
            "paper2_use": "edge-on, line-of-sight warp, vertical overlay, PV/envelope visibility",
            "example_galaxies": "NGC5907, NGC4013, NGC7331, UGC12506",
            "status": "partly endpoint-active in mixed/projection routes",
            "guardrail": "image-plane coincidence is insufficient; needs source/path support",
        },
        {
            "channel": "morphology-history / trajectory phase",
            "meaning": "source-side phase, disturbance, relaxation, or history state carried by morphology",
            "paper2_use": "warp/history and disturbed/asymmetric lanes",
            "example_galaxies": "NGC4088, UGC12506, NGC7331",
            "status": "endpoint-active only when source-frozen; otherwise caveated",
            "guardrail": "future-directed wording is trajectory/phase, not backward causation",
        },
        {
            "channel": "time / clock readout projection",
            "meaning": "effective time-slice or clock-readout mismatch multiplying the velocity readout",
            "paper2_use": "diagnostic Xi_t replays and interval controls",
            "example_galaxies": "NGC4088, UGC12506, NGC4013, NGC5907, NGC7331, NGC4183",
            "status": "control/diagnostic only in this paper",
            "guardrail": "requires independent clock/readout evidence and a nonzero T/A remainder",
        },
        {
            "channel": "path/environment projection",
            "meaning": "null-geodesic bundle and metric/matter environment affecting the observed light path",
            "paper2_use": "protocol/future full-kernel layer; path audits",
            "example_galaxies": "UGC12506 path/interloper audit; NGC4088 path not primary",
            "status": "not endpoint-modeled in this paper",
            "guardrail": "must affect the source-observer bundle; not every foreground object qualifies",
        },
        {
            "channel": "mass/envelope / closure readout",
            "meaning": "deeper source/envelope or closure channel not reducible to local 4D baryonic density alone",
            "paper2_use": "stress/development routes for high-spin/envelope or vertical-halo systems",
            "example_galaxies": "UGC12506, NGC0891, NGC4217, IC4202",
            "status": "mostly control/prospective in this paper",
            "guardrail": "requires source-native carrier/amplitude freeze; not a curve-rescue term",
        },
    ]
    taxonomy = pd.DataFrame(rows)
    taxonomy["uses_vobs_or_residual"] = False
    taxonomy["endpoint_scores_allowed"] = False
    taxonomy["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "taxonomy_id": "PAPER2_PROJECTION_CHANNEL_TAXONOMY_V1",
                "n_channels": len(taxonomy),
                "main_message": "Paper 2 uses several projection/readout layers, but only source-frozen, non-overlapping channels can be endpoint-active.",
                "time_projection_status": "control/diagnostic until independent clock evidence survives T/A",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    taxonomy.to_csv(DATA / "projection_channel_taxonomy.csv", index=False)
    summary.to_csv(DATA / "projection_channel_taxonomy_summary.csv", index=False)

    report = "\n\n".join(
        [
            "# Projection Channel Taxonomy",
            "This taxonomy summarizes the projection/readout channels used in Paper 2.",
            "## Summary",
            markdown_table(summary),
            "## Channels",
            markdown_table(taxonomy),
        ]
    )
    (REPORTS / "projection_channel_taxonomy.md").write_text(report + "\n")
    print("PROJECTION_CHANNEL_TAXONOMY_COMPLETE")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
