#!/usr/bin/env python3
"""Build the residual-blind P1 source-review worklist for Xi_t manifests.

The diagnostic Xi_t replay identifies P1 targets, but it cannot promote a
time-readout endpoint.  This artifact spells out the source observables needed
before an accepted Xi_t(R) manifest can exist.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_readout_xi_p1_source_review_not_endpoint"


WORKLIST_ROWS = [
    {
        "galaxy": "NGC4088",
        "p1_route": "warp_history_asymmetry_clock_phase",
        "source_question": "Does the source literature support a clock/readout phase proxy distinct from the already accepted warp/history morphology kernel?",
        "required_observable": "warp/asymmetry phase proxy",
        "acceptable_source_types": "H I velocity-field asymmetry; channel-map warp phase; optical/H I disturbance classification; companion/interaction context",
        "freeze_rule_needed": "map source-side asymmetry/history phase to K_t(R) shape and epsilon_t sign without using rotation residuals",
        "forbidden_endpoint_inputs": "v_obs residual; previous Xi_t improvement; best wrong-family score; post-hoc epsilon increase",
        "acceptance_condition": "independent sources identify a time/phase-like warp-history component not already counted by the additive morphology kernel",
        "failure_policy": "keep Xi_t=1 or retain NGC4088 as additive morphology-only endpoint if evidence is not independent",
        "priority": "P1",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "NGC4088",
        "p1_route": "warp_history_asymmetry_clock_phase",
        "source_question": "Can the normalization law be frozen before scoring?",
        "required_observable": "accepted epsilon_t normalization law",
        "acceptable_source_types": "source-side bounded asymmetry index; source-side interaction load; predeclared coefficient rule derived from source observables",
        "freeze_rule_needed": "epsilon_0 = f(source_load) with cap and sign fixed before endpoint replay",
        "forbidden_endpoint_inputs": "RMSE minimization; amplitude scan; residual-tail matching",
        "acceptance_condition": "normalization is computable from source manifest alone and has dimensionless status",
        "failure_policy": "do not score an accepted Xi_t endpoint; keep diagnostic result only",
        "priority": "P1",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "UGC12506",
        "p1_route": "edgeon_highspin_clock_envelope",
        "source_question": "Does the high-spin edge-on H I envelope support a clock/readout proxy rather than only a spatial projection proxy?",
        "required_observable": "edge-on PV/envelope time-slice consistency proxy",
        "acceptable_source_types": "resolved H I position-velocity envelope; high-spin settling evidence; inclination/envelope coherence; source-native halo/envelope tables",
        "freeze_rule_needed": "map high-spin envelope stress to K_t(R) shape without using the rotation residual",
        "forbidden_endpoint_inputs": "using the underprediction gap to choose the radial shape; amplitude rescue by residual matching",
        "acceptance_condition": "source data support a broad clock/readout layer tied to high-spin edge-on envelope structure",
        "failure_policy": "retain UGC12506 as underpredicted stress test, not a successful Xi_t endpoint",
        "priority": "P1",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "galaxy": "UGC12506",
        "p1_route": "edgeon_highspin_clock_envelope",
        "source_question": "Is there a path/environment reason to activate Xi_t beyond ordinary edge-on projection?",
        "required_observable": "path/foreground review",
        "acceptable_source_types": "microwave/dust foreground audit; nearby projected interloper audit; source-observer bundle environment notes",
        "freeze_rule_needed": "decide whether path term enters epsilon_t, remains a caveat, or is rejected",
        "forbidden_endpoint_inputs": "image-plane coincidence without path evidence; treating generic foreground as accepted clock evidence",
        "acceptance_condition": "path evidence is independently non-negligible or explicitly rejected with Xi_t driven only by source envelope",
        "failure_policy": "set path term to zero and test only source-envelope clock proxy if otherwise accepted",
        "priority": "P1",
        "claim_boundary": CLAIM_BOUNDARY,
    },
]


GATES = [
    {
        "gate_id": "XI_P1_G1_SOURCE_ONLY",
        "gate_status": "OPEN",
        "required_condition": "Every Xi_t observable must be filled from source-side morphology, path, or clock/readout evidence before endpoint scoring.",
        "blocked_by": "no accepted Xi_t source manifest yet",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "gate_id": "XI_P1_G2_NO_DOUBLE_COUNT",
        "gate_status": "OPEN",
        "required_condition": "The Xi_t proxy must be shown distinct from the additive morphology/projection kernel already used for the galaxy.",
        "blocked_by": "NGC4088 and UGC12506 need separation of clock/readout phase from spatial morphology amplitude",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "gate_id": "XI_P1_G3_NORMALIZATION_FREEZE",
        "gate_status": "OPEN",
        "required_condition": "epsilon_t normalization and cap must be frozen from source rules, not residual improvement.",
        "blocked_by": "current epsilon_0 is diagnostic source-load proxy, not an accepted theory/source law",
        "claim_boundary": CLAIM_BOUNDARY,
    },
    {
        "gate_id": "XI_P1_G4_NULL_ALLOWED",
        "gate_status": "PASS_RECORDED",
        "required_condition": "The protocol must allow Xi_t=1 for galaxies without independent time-readout evidence.",
        "blocked_by": "none; P3 and P2 rows already enforce this policy",
        "claim_boundary": CLAIM_BOUNDARY,
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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    worklist = pd.DataFrame(WORKLIST_ROWS)
    gates = pd.DataFrame(GATES)
    summary = pd.DataFrame(
        [
            {
                "source_review_status": "XI_T_P1_SOURCE_REVIEW_WORKLIST_CREATED_NO_ENDPOINT",
                "p1_targets": "NGC4088; UGC12506",
                "n_required_review_items": len(worklist),
                "accepted_xi_t_manifests": 0,
                "endpoint_scores_allowed": False,
                "next_step": "fill P1 source observables, freeze epsilon_t/K_t rules, then run a predeclared Xi_t ablation endpoint",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    worklist.to_csv(DATA / "time_readout_xi_p1_source_review_worklist.csv", index=False)
    gates.to_csv(DATA / "time_readout_xi_p1_source_review_gates.csv", index=False)
    summary.to_csv(DATA / "time_readout_xi_p1_source_review_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time-Readout Xi_t P1 Source-Review Worklist",
            "",
            "This artifact operationalizes the P1 rows from the diagnostic Xi_t",
            "readiness manifest. It is not an endpoint score and does not promote",
            "any accepted Xi_t(R) manifest.",
            "",
            "## Worklist",
            "",
            markdown_table(worklist),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
        ]
    )
    (REPORTS / "time_readout_xi_p1_source_review_worklist.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
