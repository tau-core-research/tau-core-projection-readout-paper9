#!/usr/bin/env python3
"""Record the multichannel Tau Core time-projection gate.

The current Xi_t tests use a narrow source-reviewed control factor.  This gate
separates the broader theoretical statement: time projection is not a single
amplitude knob.  It can enter through the source morphology clock/phase, the
observer/path clock slice, and the path/environment clock channel, while also
deforming morphology kernels and observer visibility weights.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_projection_multichannel_fundamental_gate_not_endpoint"


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

    definitions = pd.DataFrame(
        [
            {
                "object_id": "XI_MORPH",
                "definition": "Xi_morph(R;Theta_src^tau)",
                "meaning": "source-intrinsic morphology clock/phase readout factor",
                "inactive_limit": "Xi_morph -> 1 for settled regular source morphology",
                "status": "FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "object_id": "XI_OBS",
                "definition": "Xi_obs(R;O_obs/path)",
                "meaning": "observer/path-selected clock slice and visibility factor",
                "inactive_limit": "Xi_obs -> 1 for ordinary projection with no independent clock evidence",
                "status": "FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "object_id": "XI_PATH",
                "definition": "Xi_path(R;E_proj/history)",
                "meaning": "null-bundle/path-environment clock-readout factor",
                "inactive_limit": "Xi_path -> 1 when path/environment evidence is absent",
                "status": "FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "object_id": "XI_EFF",
                "definition": "Xi_eff = Xi_morph Xi_obs Xi_path",
                "meaning": "effective total time-readout factor used by the observed velocity quotient",
                "inactive_limit": "Xi_eff -> 1 if all time-projection channels are inactive",
                "status": "DERIVED_FROM_FACTOR_DEFINITION",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    formulas = pd.DataFrame(
        [
            {
                "formula_id": "MULTICHANNEL_TIME_READOUT_SHELL",
                "formula": "v_obs^2=Xi_eff^2(R)[v_Newt^2+delta_v_morph^2(R;Theta_src^tau,O_obs/path)]",
                "claim_type": "formula_conditional_shell",
                "dimension_check": "PASS: Xi_eff dimensionless; bracket has velocity squared units",
                "known_limit": "Xi_morph=Xi_obs=Xi_path=1 recovers morphology/gravity readout without time projection",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "formula_id": "LINEARIZED_MULTICHANNEL_TIME_READOUT",
                "formula": "Xi_i=1+epsilon_i; delta_v_t^2 ~= 2(epsilon_morph+epsilon_obs+epsilon_path)[v_Newt^2+delta_v_morph^2]",
                "claim_type": "first_order_small_mismatch",
                "dimension_check": "PASS: epsilon_i are dimensionless",
                "known_limit": "all epsilons zero gives delta_v_t^2=0",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "formula_id": "KERNEL_DEFORMATION_CHANNEL",
                "formula": "K_readout(R)=K_0(R;K_present)+deltaK_morph_time(R;Theta_src^tau)+deltaK_obs_time(R;O_obs/path)",
                "claim_type": "kernel_shape_channel",
                "dimension_check": "PASS if K terms are dimensionless and amplitudes carry velocity squared units",
                "known_limit": "deltaK terms vanish for settled morphology and inactive observer/path clock evidence",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    theorem = pd.DataFrame(
        [
            {
                "theorem_id": "TIME_PROJECTION_MULTICHANNEL_FACTORIZATION",
                "verdict": "PLAUSIBLE_BUT_NOT_FULLY_DERIVED",
                "formal_claim": "If time projection is a readout-level mismatch rather than an added force, it must be allowed to act both on source morphology phase and on observer/path clock slicing.",
                "proven_part": "A dimensionless multiplicative clock factor gives the correct velocity-squared scaling and Newtonian limit.",
                "unproven_part": "The Tau-side origin and normalization of Xi_morph, Xi_obs, and Xi_path are not yet derived from a completed clock geometry.",
                "weakest_step": "mapping source observables to epsilon_morph, epsilon_obs, and epsilon_path without residual leakage",
                "minimal_corrected_statement": "Time projection should be treated as a multichannel formula-conditional readout layer; current Xi_t tests only instantiate a narrow source-reviewed control slice.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    implementation_audit = pd.DataFrame(
        [
            {
                "implementation": "current_trial_Xi_t",
                "covers_xi_morph": "partial",
                "covers_xi_obs": "partial",
                "covers_xi_path": "no",
                "covers_kernel_deformation": "no",
                "status": "diagnostic_proxy_only",
                "consequence": "cannot test full fundamental time-projection branch",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "implementation": "UGC12506_caveated_interval_control",
                "covers_xi_morph": "partial_highspin_envelope_clock",
                "covers_xi_obs": "partial_edgeon_pv_clock_slice",
                "covers_xi_path": "explicitly_zero",
                "covers_kernel_deformation": "no",
                "status": "source_reviewed_narrow_control_not_endpoint",
                "consequence": "small improvement does not falsify broader time-projection channel",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "implementation": "future_full_time_projection_kernel",
                "covers_xi_morph": "required",
                "covers_xi_obs": "required",
                "covers_xi_path": "optional_source_evidence_dependent",
                "covers_kernel_deformation": "required",
                "status": "not_built",
                "consequence": "needed before strong claim about time projection strength",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "TPMULTI_G1_CHANNEL_SEPARATION",
                "gate_status": "REQUIRED",
                "required_condition": "Freeze Xi_morph, Xi_obs, and Xi_path separately, with Xi_path allowed to be exactly one.",
                "forbidden_shortcut": "one fitted epsilon_t absorbing all missing amplitude",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TPMULTI_G2_SOURCE_MORPHOLOGY_TIME",
                "gate_status": "OPEN",
                "required_condition": "Define source-intrinsic morphology clock/phase observables: settling, warp phase, high-spin envelope state, interaction history.",
                "forbidden_shortcut": "infer source time phase from rotation residual",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TPMULTI_G3_OBSERVER_PROJECTION_TIME",
                "gate_status": "OPEN",
                "required_condition": "Define observer/path clock-slice observables: inclination, edge-on overlay, PV/envelope visibility, beam/null-bundle geometry.",
                "forbidden_shortcut": "treat generic inclination as clock evidence without source-review support",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TPMULTI_G4_KERNEL_AND_CLOCK_ABLATION",
                "gate_status": "OPEN",
                "required_condition": "Run ablations: morphology kernel only, +source time, +observer time, +path time, +kernel deformation.",
                "forbidden_shortcut": "claim full time projection from a single combined replay",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "multichannel_status": "TIME_PROJECTION_FUNDAMENTAL_MULTICHANNEL_GATE_RECORDED_NOT_DERIVED",
                "current_xi_t_tests_status": "narrow_proxy_or_control_only",
                "main_conclusion": "The weak UGC12506 Xi_t control improvement does not test the full fundamental time-projection branch.",
                "next_step": "build separate source-morphology-time and observer-projection-time manifests before any full time-projection endpoint",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    definitions.to_csv(DATA / "time_projection_multichannel_definitions.csv", index=False)
    formulas.to_csv(DATA / "time_projection_multichannel_formulas.csv", index=False)
    theorem.to_csv(DATA / "time_projection_multichannel_theorem_audit.csv", index=False)
    implementation_audit.to_csv(DATA / "time_projection_multichannel_implementation_audit.csv", index=False)
    gates.to_csv(DATA / "time_projection_multichannel_gates.csv", index=False)
    summary.to_csv(DATA / "time_projection_multichannel_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time Projection Multichannel Fundamental Gate",
            "",
            "This artifact separates the broader Tau Core time-projection idea from the narrow Xi_t control factors used in the current numerical tests.",
            "",
            "## Definitions",
            "",
            markdown_table(definitions),
            "",
            "## Formula Shells",
            "",
            markdown_table(formulas),
            "",
            "## Theorem Audit",
            "",
            markdown_table(theorem),
            "",
            "## Current Implementation Audit",
            "",
            markdown_table(implementation_audit),
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
    (REPORTS / "time_projection_multichannel_fundamental_gate.md").write_text(
        report,
        encoding="utf-8",
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
