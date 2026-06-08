#!/usr/bin/env python3
"""Summarize the UGC12506 source-native NFW-HSE replay decision gate."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_source_native_nfw_hse_decision_gate_not_validation"


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
    REPORTS.mkdir(parents=True, exist_ok=True)

    replay = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_replay_summary.csv").iloc[0]
    scan = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_uncertainty_scan_summary.csv").iloc[0]
    route = pd.read_csv(DATA / "ugc12506_prior_best_source_route_audit_summary.csv").iloc[0]
    interloper = pd.read_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv").iloc[0]

    decision = pd.DataFrame(
        [
            {
                "decision_status": "UGC12506_SOURCE_NATIVE_NFW_HSE_PARTIAL_SUCCESS_GAP_REMAINS",
                "galaxy": GALAXY,
                "source_native_nfw_hse_rmse_km_s": float(replay["source_native_nfw_hse_rmse_km_s"]),
                "old_rd_proxy_nfw_hse_rmse_km_s": float(replay["old_rd_proxy_nfw_hse_rmse_km_s"]),
                "source_native_minus_old_proxy_rmse_km_s": float(
                    replay["source_native_minus_old_rd_proxy_rmse_km_s"]
                ),
                "best_uncertainty_rmse_km_s": float(scan["best_uncertainty_rmse_km_s"]),
                "prior_best_diagnostic_rmse_km_s": float(replay["prior_best_diagnostic_rmse_km_s"]),
                "gap_to_prior_best_after_uncertainty_km_s": float(
                    scan["best_uncertainty_minus_prior_best_diagnostic_rmse_km_s"]
                ),
                "nfw_route_status": str(route["nfw_rapid_rise_route"]),
                "internal_projection_status": str(interloper["internal_projection_status"]),
                "foreground_path_object_status": str(interloper["foreground_path_status"]),
                "decision": (
                    "keep source-native NFW-HSE as cleaner partial source route; do not promote to accepted "
                    "endpoint; search for an additional residual-blind mass/readout normalization or "
                    "projection-history component before another scoring attempt"
                ),
                "negative_result_preserved": True,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    obligations = pd.DataFrame(
        [
            {
                "obligation_id": "U12506_NEXT_1_AMPLITUDE_SOURCE",
                "status": "OPEN",
                "why_it_matters": "the source-native shape improves branches but remains under-amplified",
                "allowed_sources": "stellar/gas mass scale, halo velocity scale, distance/inclination audit, or source-native baryonic carrier audit",
                "forbidden_sources": "endpoint residual multiplier, post-hoc curve rescue",
            },
            {
                "obligation_id": "U12506_NEXT_2_PROJECTION_HISTORY",
                "status": "OPEN",
                "why_it_matters": "edge-on projection is strong, but foreground/path object evidence is not established",
                "allowed_sources": "source-native warp, vertical overlay, H I asymmetry, resolved velocity-field context",
                "forbidden_sources": "assigning line-of-sight gravity from optical overlay caveats alone",
            },
            {
                "obligation_id": "U12506_NEXT_3_CARRIER_AUDIT",
                "status": "OPEN",
                "why_it_matters": "all compared baselines underpredict, suggesting carrier/source normalization may be low",
                "allowed_sources": "published distance, inclination, M/L, gas scale, and SPARC carrier variants",
                "forbidden_sources": "choosing carrier from best endpoint RMSE after scoring",
            },
        ]
    )
    obligations["galaxy"] = GALAXY
    obligations["claim_boundary"] = CLAIM_BOUNDARY

    decision.to_csv(DATA / "ugc12506_source_native_nfw_hse_decision_gate_summary.csv", index=False)
    obligations.to_csv(DATA / "ugc12506_source_native_nfw_hse_decision_gate_obligations.csv", index=False)

    report = [
        "# UGC12506 Source-Native NFW-HSE Decision Gate",
        "",
        "The source-native NFW/HSE replay is a cleaner partial success, but not an",
        "accepted endpoint. It improves the old proxy route slightly and the older",
        "source-frozen branches substantially, while the gap to the prior diagnostic",
        "best remains large.",
        "",
        "## Decision",
        "",
        markdown_table(decision),
        "",
        "## Open Obligations",
        "",
        markdown_table(obligations),
        "",
        "## Interpretation",
        "",
        "UGC12506 should be preserved as a useful weak/negative replay case rather",
        "than forced into a successful endpoint. The next honest route is not to",
        "increase the amplitude from the residual, but to determine whether an",
        "independent source-native carrier normalization, halo-velocity scale, or",
        "projection-history component is justified.",
        "",
    ]
    (REPORTS / "ugc12506_source_native_nfw_hse_decision_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(decision.to_string(index=False))
    print(obligations.to_string(index=False))


if __name__ == "__main__":
    main()
