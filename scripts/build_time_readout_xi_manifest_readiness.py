#!/usr/bin/env python3
"""Build a readiness manifest for future accepted Xi_t time-readout endpoints."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_readout_xi_manifest_readiness_not_endpoint"


MANUAL = {
    "NGC4088": {
        "readiness": "P1_PROMOTE_AFTER_SOURCE_REVIEW",
        "reason": "Xi_t improves and source status has strong warp/history/asymmetry context, but q/history and normalization caveats remain.",
        "required_observables": "independent warp/asymmetry phase proxy; interaction/companion context; accepted normalization law",
    },
    "UGC12506": {
        "readiness": "P1_PROMOTE_AFTER_SOURCE_REVIEW",
        "reason": "Xi_t improves high-spin edge-on stress case; UGC12506 remains underpredicted but direction is source-consistent.",
        "required_observables": "clock/readout proxy from high-spin settling; edge-on PV/envelope time-slice consistency; path/foreground review",
    },
    "NGC4183": {
        "readiness": "P2_NULL_CONTROL_KEEP_WEAK",
        "reason": "Xi_t is nearly neutral and the object is a weak-projection/null-control case.",
        "required_observables": "quiet-control confirmation; no strong Xi_t promotion unless new source evidence appears",
    },
    "NGC4013": {
        "readiness": "P3_REJECT_CURRENT_XI_T_PROXY",
        "reason": "Xi_t worsens an already strong warp/vertical-overlay curve; current proxy likely double-counts or over-rescales.",
        "required_observables": "separate vertical overlay from clock-readout; do not promote Xi_t without independent clock evidence",
    },
    "NGC5907": {
        "readiness": "P3_REJECT_CURRENT_XI_T_PROXY",
        "reason": "Xi_t slightly worsens a saturated projection kernel; edge-on projection is already captured by the base kernel.",
        "required_observables": "path-specific clock evidence beyond ordinary edge-on projection; otherwise keep Xi_t=1",
    },
    "NGC7331": {
        "readiness": "P3_REJECT_CURRENT_XI_T_PROXY",
        "reason": "Xi_t worsens the broad vertical/outer-warp mixed curve; current mixed kernel likely already carries available phase signal.",
        "required_observables": "narrow outer-warp clock proxy and independent H I history coherence before any Xi_t promotion",
    },
}


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

    summary = pd.read_csv(DATA / "time_readout_xi_trial_galaxy_summary.csv")
    rows = []
    for _, row in summary.iterrows():
        galaxy = row["galaxy"]
        meta = MANUAL[galaxy]
        rows.append(
            {
                "galaxy": galaxy,
                "xi_trial_status": meta["readiness"],
                "source_status": row["source_status"],
                "epsilon_0_source_frozen": row["epsilon_0_source_frozen"],
                "xi_improves_full_time": row["xi_improves_full_time"],
                "best_trial_model": row["best_trial_model"],
                "best_trial_rmse_km_s": row["best_trial_rmse_km_s"],
                "readiness_reason": meta["reason"],
                "required_observables_for_accepted_xi_t": meta["required_observables"],
                "accepted_xi_t_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    manifest = pd.DataFrame(rows).sort_values(["xi_trial_status", "galaxy"])

    gates = pd.DataFrame(
        [
            {
                "gate_id": "XI_MANIFEST_G1_NO_RESIDUAL_PROMOTION",
                "gate_status": "PASS_RECORDED",
                "required_condition": "Xi_t candidates cannot be promoted because they improved a rotation curve.",
                "current_result": "All current rows remain non-endpoint readiness rows.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "XI_MANIFEST_G2_TRUE_NULL_ALLOWED",
                "gate_status": "PASS_RECORDED",
                "required_condition": "If Xi_t worsens or is neutral without source evidence, the manifest must permit Xi_t=1.",
                "current_result": "NGC4013, NGC5907, and NGC7331 reject the current Xi_t proxy; NGC4183 remains weak/null.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "XI_MANIFEST_G3_P1_REQUIRES_SOURCE_REVIEW",
                "gate_status": "PASS_RECORDED",
                "required_condition": "Positive diagnostic cases need independent source observables before any accepted endpoint.",
                "current_result": "NGC4088 and UGC12506 are P1 source-review targets, not accepted Xi_t endpoints.",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    readiness_summary = pd.DataFrame(
        [
            {
                "readiness_status": "XI_T_MANIFEST_READINESS_BUILT_NO_ACCEPTED_ENDPOINTS",
                "n_p1_promote_after_source_review": int((manifest["xi_trial_status"] == "P1_PROMOTE_AFTER_SOURCE_REVIEW").sum()),
                "n_p2_null_control": int((manifest["xi_trial_status"] == "P2_NULL_CONTROL_KEEP_WEAK").sum()),
                "n_p3_reject_current_proxy": int((manifest["xi_trial_status"] == "P3_REJECT_CURRENT_XI_T_PROXY").sum()),
                "accepted_xi_t_manifests": 0,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "time_readout_xi_manifest_readiness.csv", index=False)
    gates.to_csv(DATA / "time_readout_xi_manifest_readiness_gates.csv", index=False)
    readiness_summary.to_csv(DATA / "time_readout_xi_manifest_readiness_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time-Readout Xi_t Manifest Readiness",
            "",
            "This artifact converts the diagnostic Xi_t replay into a future source-freeze worklist. It does not promote any accepted Xi_t endpoint.",
            "",
            "## Manifest",
            "",
            markdown_table(manifest),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(readiness_summary),
            "",
        ]
    )
    (REPORTS / "time_readout_xi_manifest_readiness.md").write_text(report, encoding="utf-8")
    print(readiness_summary.to_string(index=False))


if __name__ == "__main__":
    main()
