#!/usr/bin/env python3
"""Record the formula and gate requirements for the time-readout channel."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_readout_projection_channel_formula_conditional_not_endpoint"


def markdown_table(df: pd.DataFrame) -> str:
    lines = [
        "| " + " | ".join(df.columns) + " |",
        "| " + " | ".join(["---"] * len(df.columns)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in df.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    formulas = pd.DataFrame(
        [
            {
                "formula_id": "TIME_READOUT_FULL_SHELL",
                "formula": "v_obs^2(R)=Xi_t^2(R;O_obs/path,Theta_morph,E_proj/history)[v_Newt^2(R)+delta_v_grav/morph^2(R)]",
                "status": "FORMULA_CONDITIONAL",
                "interpretation": "projection-dependent clock/readout mismatch, not an extra force",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "formula_id": "TIME_READOUT_LINEARIZED_SHELL",
                "formula": "Xi_t(R)=1+epsilon_t(R); delta_v_t^2(R) ~= 2 epsilon_t(R)[v_Newt^2(R)+delta_v_grav/morph^2(R)]",
                "status": "FORMULA_CONDITIONAL_SMALL_MISMATCH",
                "interpretation": "first-order diagnostic form for small clock/readout mismatch",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "TIME_G1_SOURCE_FROZEN_XI_T",
                "required_condition": "Xi_t(R) or epsilon_t(R) is fixed from source-side observer/path, morphology-trajectory, or clock-readout evidence before scoring",
                "forbidden_inputs": "rotation residual, best Tau family, MOND/RAR/TPG rank, per-galaxy residual tuning",
                "current_status": "OPEN_NO_ACCEPTED_XI_T_MANIFEST",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TIME_G2_NEWTONIAN_CLOCK_LIMIT",
                "required_condition": "Xi_t -> 1 in regular quiet systems or in source states with no projection-time evidence",
                "forbidden_inputs": "post-hoc suppression chosen after seeing endpoint score",
                "current_status": "THEORY_REQUIREMENT_RECORDED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TIME_G3_SEPARATE_FROM_GRAVITY_AMPLITUDE",
                "required_condition": "time-readout factor is multiplicative and separated from additive morphology/gravity residual amplitude",
                "forbidden_inputs": "absorbing failed amplitude normalization into Xi_t",
                "current_status": "FORMULA_SEPARATION_RECORDED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "TIME_G4_ABLATION_REQUIRED",
                "required_condition": "future endpoint must compare base morphology, observer/path, trajectory phase, and time-readout layers as separate ablations",
                "forbidden_inputs": "claiming a full time-projection success from a morphology-phase-only replay",
                "current_status": "OPEN_NEXT_PROTOCOL_STEP",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    subchannels = pd.DataFrame(
        [
            {
                "subchannel": "observer_path_projection",
                "what_changes": "which source clock slice is visible along the line of sight or light bundle",
                "formula_role": "argument of Xi_t through O_obs/path",
                "source_freeze_requirement": "inclination, edge-on overlay, warp visibility, beam/path geometry, foreground or path-environment audit",
                "current_status": "PROXY_PARTIAL_IN_PAPER2",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "subchannel": "morphology_trajectory_phase",
                "what_changes": "whether the current 4D morphology is a settled or phase-shifted readout slice",
                "formula_role": "argument of Xi_t through Theta_morph",
                "source_freeze_requirement": "settling state, warp/asymmetry stage, interaction history, relaxation or future-directed phase proxies",
                "current_status": "DIAGNOSTIC_PROXY_ONLY",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "subchannel": "gravity_readout_projection",
                "what_changes": "morphology/gravity residual is multiplied by the clock factor",
                "formula_role": "Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2]",
                "source_freeze_requirement": "separate morphology/gravity residual shell frozen before time-readout scoring",
                "current_status": "FORMULA_SEPARATION_RECORDED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "subchannel": "clock_rate_time_slice_projection",
                "what_changes": "effective time parameter used in the observed velocity quotient",
                "formula_role": "Xi_t=1+epsilon_t; delta_v_t^2 ~= 2 epsilon_t (...)",
                "source_freeze_requirement": "residual-blind clock/readout mismatch proxy",
                "current_status": "OPEN_NO_ACCEPTED_PROXY",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "subchannel": "path_environment_projection",
                "what_changes": "metric/matter environment of the observed light bundle can affect the clock/readout factor",
                "formula_role": "possible E_proj/history dependence in Xi_t",
                "source_freeze_requirement": "source-observer null-geodesic bundle environment; reject image-plane coincidences without path evidence",
                "current_status": "OPEN_PATH_AWARE_KERNEL_NOT_MODELED",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "channel_status": "TIME_READOUT_PROJECTION_BRANCH_DEFINED_NOT_VALIDATED",
                "accepted_endpoint_ready": False,
                "reason": "No residual-blind Xi_t(R) manifest is accepted yet; current full-time morphology replay is only a diagnostic proxy.",
                "next_step": "Define source observables for Xi_t, freeze a per-galaxy manifest, then run staged ablation endpoints.",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    formulas.to_csv(DATA / "time_readout_projection_channel_formulas.csv", index=False)
    gates.to_csv(DATA / "time_readout_projection_channel_gates.csv", index=False)
    subchannels.to_csv(DATA / "time_readout_projection_subchannels.csv", index=False)
    summary.to_csv(DATA / "time_readout_projection_channel_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time-Readout Projection Channel Gate",
            "",
            "This artifact records the formula-conditional Tau Core branch in which "
            "projection can modify the effective clock/readout factor used in the "
            "observed rotation curve.",
            "",
            "It is not an endpoint validation and does not define an accepted "
            "`Xi_t(R)` manifest.",
            "",
            "## Formulas",
            "",
            markdown_table(formulas),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Projection Subchannels",
            "",
            markdown_table(subchannels),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
        ]
    )
    (REPORTS / "time_readout_projection_channel_gate.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
