#!/usr/bin/env python3
"""Resolve NGC4088 additive-kernel / Xi_eff double-count risk.

The NGC4088 Xi_eff control manifest uses source observables that substantially
overlap the already active additive warp/history morphology kernel.  This gate
therefore builds a source-space overlap audit and freezes the accepted combined
route policy:

* clock-only Xi_eff may remain a control/diagnostic route;
* additive-plus-Xi_eff remains a stress test;
* the accepted combined route sets the orthogonal clock residual to zero unless
  new source evidence supplies a clock/readout observable not already used by
  the additive morphology kernel.

No rotation residuals are used here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_time_projection_double_count_resolution_gate_not_endpoint"


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

    additive = pd.read_csv(DATA / "ngc4088_warp_history_formula_freeze_manifest.csv").iloc[0]
    xieff = pd.read_csv(DATA / "ngc4088_time_projection_xi_eff_manifest_gate.csv").iloc[0]
    xieff_terms = pd.read_csv(DATA / "ngc4088_time_projection_xi_eff_terms.csv")
    ablation = pd.read_csv(DATA / "ngc4088_time_projection_ablation_control_summary.csv").iloc[0]

    additive_tokens = {
        "x_w_formula_freeze": "warp onset / radial activation",
        "q_warp": "warp/asymmetry source strength",
        "sigma_warp": "source-side warp/history sign",
        "C_warp": "same radial warp/history kernel shape",
    }
    clock_tokens = {
        "f_PA": "orientation mismatch / warp geometry",
        "f_R": "onset-side asymmetry / radial activation uncertainty",
        "f_q": "q_warp source strength",
        "f_mem": "morphology-carried warp/history source phase",
    }

    overlap_rows = []
    overlap_map = {
        "f_PA": ("C_warp", "SHARED_WARP_GEOMETRY", "orientation mismatch is part of the same warp/history geometry family"),
        "f_R": ("x_w_formula_freeze", "SHARED_ONSET_RADIAL_SUPPORT", "radial onset/asymmetry information is already used by the additive kernel"),
        "f_q": ("q_warp", "DIRECT_SOURCE_STRENGTH_OVERLAP", "q_warp is already an additive-kernel source-strength factor"),
        "f_mem": ("sigma_warp", "SHARED_HISTORY_PHASE", "morphology-carried history phase is already assigned to the additive warp/history route"),
    }
    for _, row in xieff_terms.iterrows():
        feature = str(row["feature_symbol"])
        additive_token, status, reason = overlap_map[feature]
        overlap_rows.append(
            {
                "galaxy": GALAXY,
                "xi_eff_feature": feature,
                "xi_eff_term_value": float(row["term_value"]),
                "overlapping_additive_token": additive_token,
                "overlap_status": status,
                "orthogonal_clock_residual_allowed": False,
                "reason": reason,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    overlap = pd.DataFrame(overlap_rows)
    raw_clock_load = float(overlap["xi_eff_term_value"].sum())
    orthogonal_clock_load = float(
        overlap.loc[overlap["orthogonal_clock_residual_allowed"], "xi_eff_term_value"].sum()
    )
    epsilon_candidate = float(xieff["epsilon_clock_candidate"])
    epsilon_orthogonal = 0.0 if orthogonal_clock_load == 0.0 else epsilon_candidate

    policy = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "policy_id": "NGC4088_TIME_PROJECTION_DOUBLE_COUNT_RESOLUTION_V1",
                "accepted_combined_route": "ADDITIVE_WARP_HISTORY_ONLY_FOR_COMBINED_ENDPOINT",
                "clock_only_route_status": "CONTROL_ROUTE_ALLOWED_NOT_ENDPOINT",
                "additive_plus_clock_status": "STRESS_TEST_REJECTED_FOR_ENDPOINT",
                "raw_clock_load_L": raw_clock_load,
                "orthogonal_clock_load_L": orthogonal_clock_load,
                "epsilon_clock_candidate": epsilon_candidate,
                "epsilon_clock_orthogonal_combined": epsilon_orthogonal,
                "xi_eff_combined_policy": "Xi_eff=1 for additive-combined route until independent clock-only evidence exists",
                "new_evidence_required_to_reopen_clock": (
                    "observer/path clock proxy or source-time observable that is not q_warp, "
                    "x_w/onset, warp geometry, or morphology-history phase already used by additive kernel"
                ),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4088_DCR_G1_ADDITIVE_SOURCE_TOKENS_DECLARED",
                "gate_status": "PASS",
                "evidence": "; ".join(additive_tokens.keys()),
                "remaining_obligation": "preserve additive-kernel provenance",
            },
            {
                "gate_id": "N4088_DCR_G2_CLOCK_SOURCE_TOKENS_DECLARED",
                "gate_status": "PASS",
                "evidence": "; ".join(clock_tokens.keys()),
                "remaining_obligation": "preserve Xi_eff source-term provenance",
            },
            {
                "gate_id": "N4088_DCR_G3_OVERLAP_AUDIT",
                "gate_status": "PASS_OVERLAP_COMPLETE",
                "evidence": "all current Xi_eff source terms overlap the additive warp/history route",
                "remaining_obligation": "set orthogonal clock residual to zero for combined route",
            },
            {
                "gate_id": "N4088_DCR_G4_CLOCK_ONLY_CONTROL_ALLOWED",
                "gate_status": "PASS_CONTROL_ONLY",
                "evidence": str(ablation["interpretation"]),
                "remaining_obligation": "clock-only may be explored separately, not combined endpoint",
            },
            {
                "gate_id": "N4088_DCR_G5_COMBINED_ENDPOINT_POLICY",
                "gate_status": "PASS_FREEZE_POLICY",
                "evidence": "accepted combined route uses Xi_eff=1 unless independent non-overlap clock evidence is supplied",
                "remaining_obligation": "build endpoint permission gate only for additive route or future non-overlap clock route",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "double_count_resolution_status": "NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE",
                "galaxy": GALAXY,
                "n_xi_eff_terms": int(len(overlap)),
                "n_overlapping_terms": int((~overlap["orthogonal_clock_residual_allowed"]).sum()),
                "raw_clock_load_L": raw_clock_load,
                "orthogonal_clock_load_L": orthogonal_clock_load,
                "epsilon_clock_candidate": epsilon_candidate,
                "epsilon_clock_orthogonal_combined": epsilon_orthogonal,
                "accepted_combined_route": "additive_warp_history_with_Xi_eff_equal_one",
                "clock_only_control_preserved": True,
                "additive_plus_clock_endpoint_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_step": "if endpoint scoring is requested, score additive-only accepted route; reopen time endpoint only with independent non-overlap clock evidence",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    overlap.to_csv(DATA / "ngc4088_time_projection_double_count_overlap_audit.csv", index=False)
    policy.to_csv(DATA / "ngc4088_time_projection_double_count_policy.csv", index=False)
    gates.to_csv(DATA / "ngc4088_time_projection_double_count_resolution_gates.csv", index=False)
    summary.to_csv(DATA / "ngc4088_time_projection_double_count_resolution_summary.csv", index=False)

    report = "\n".join(
        [
            "# NGC4088 Time-Projection Double-Count Resolution Gate",
            "",
            "This gate resolves the double-count risk between the additive warp/history",
            "morphology kernel and the Xi_eff clock/readout control manifest. It uses",
            "only frozen source-manifest information and does not inspect endpoint",
            "residuals.",
            "",
            "## Overlap Audit",
            "",
            markdown_table(overlap),
            "",
            "## Policy",
            "",
            markdown_table(policy),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Interpretation",
            "",
            "The current NGC4088 Xi_eff terms are real source-side clock/readout",
            "candidates, but they are not independent of the additive warp/history",
            "morphology kernel. Therefore the accepted combined endpoint route sets",
            "the orthogonal clock residual to zero. This preserves the time-projection",
            "control result while preventing the same morphology/history evidence from",
            "being counted twice.",
            "",
        ]
    )
    (REPORTS / "ngc4088_time_projection_double_count_resolution_gate.md").write_text(
        report, encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
