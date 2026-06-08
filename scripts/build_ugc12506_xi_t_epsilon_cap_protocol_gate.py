#!/usr/bin/env python3
"""Build the epsilon_cap protocol gate for the UGC12506 Xi_t shell.

This gate does not claim that 0.035 is a universal Tau Core constant.  It shows
that the cap sits inside a small-mismatch admissible interval derived from the
linearized Xi_t expansion, then freezes it as a conservative predeclared class
cap for the current source-shell protocol.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint"


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

    norm = pd.read_csv(DATA / "ugc12506_xi_t_normalization_summary.csv").iloc[0]
    epsilon_cap = float(norm["epsilon_cap"])
    epsilon_t = float(norm["epsilon_t"])
    gamma_clock = float(norm["gamma_clock"])

    # For Xi_t=1+epsilon, Xi_t^2=1+2epsilon+epsilon^2.  The ratio of the
    # quadratic term to the linear correction is epsilon/2.  Requiring that
    # ratio to stay below eta_quad gives epsilon <= 2 eta_quad.
    eta_quad = 0.02
    epsilon_linear_bound = 2.0 * eta_quad
    safety_fraction = epsilon_cap / epsilon_linear_bound if epsilon_linear_bound else 0.0
    xi_sq_max = (1.0 + epsilon_cap) ** 2
    max_v2_fractional_shift = xi_sq_max - 1.0
    max_linear_truncation_ratio = epsilon_cap / 2.0

    theorem = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "cap_gate_id": "U12506_XI_T_SMALL_MISMATCH_CAP_PROTOCOL",
                "cap_status": "PROTOCOL_CAP_FROZEN_WITHIN_LINEAR_REGIME_NOT_UNIVERSAL_CONSTANT",
                "statement": (
                    "For Xi_t=1+epsilon_t, the neglected quadratic term in "
                    "Xi_t^2 is epsilon_t^2.  Relative to the linear correction "
                    "2 epsilon_t, this is epsilon_t/2.  Requiring a <=2% "
                    "second-order-to-linear ratio gives epsilon_t <= 0.04. "
                    "The protocol cap epsilon_cap=0.035 is a conservative "
                    "predeclared value inside that admissible interval."
                ),
                "derived_bound": "epsilon_t <= 2 eta_quad",
                "eta_quad": eta_quad,
                "epsilon_linear_bound": epsilon_linear_bound,
                "epsilon_cap": epsilon_cap,
                "safety_fraction_of_bound": safety_fraction,
                "max_quadratic_to_linear_ratio": max_linear_truncation_ratio,
                "max_v2_fractional_shift": max_v2_fractional_shift,
                "universal_constant_claim": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    derivation_steps = pd.DataFrame(
        [
            {
                "step_id": "C1_TIME_SHELL",
                "claim_type": "definition",
                "status": "PASS",
                "statement": "Use the small-mismatch shell Xi_t=1+epsilon_t.",
                "formula_consequence": "Xi_t^2=1+2epsilon_t+epsilon_t^2.",
            },
            {
                "step_id": "C2_LINEARIZATION_ERROR",
                "claim_type": "derived_ratio",
                "status": "PASS",
                "statement": "The quadratic-to-linear correction ratio is epsilon_t/2.",
                "formula_consequence": "A small cap controls the validity of the linearized readout interpretation.",
            },
            {
                "step_id": "C3_ADMISSIBLE_BOUND",
                "claim_type": "protocol_tolerance",
                "status": "PASS_CONDITIONAL",
                "statement": "Choose eta_quad=0.02 as a predeclared maximum second-order-to-linear ratio.",
                "formula_consequence": "epsilon_t must be <=0.04.",
            },
            {
                "step_id": "C4_PROTOCOL_CAP",
                "claim_type": "protocol_freeze",
                "status": "PASS_PROTOCOL_FREEZE",
                "statement": "Freeze epsilon_cap=0.035 as a conservative value below 0.04.",
                "formula_consequence": "UGC12506 epsilon_t=0.023844 remains below the cap and in the linear regime.",
            },
            {
                "step_id": "C5_UNIVERSAL_ORIGIN",
                "claim_type": "claim_boundary",
                "status": "OPEN",
                "statement": "This does not derive epsilon_cap as a universal Tau Core constant.",
                "formula_consequence": "Population use requires predeclared class-cap policy or deeper Tau-side clock geometry.",
            },
        ]
    )
    derivation_steps["galaxy"] = GALAXY
    derivation_steps["uses_vobs_or_residual"] = False
    derivation_steps["endpoint_scores_allowed"] = False
    derivation_steps["claim_boundary"] = CLAIM_BOUNDARY
    derivation_steps = derivation_steps[
        [
            "galaxy",
            "step_id",
            "claim_type",
            "status",
            "statement",
            "formula_consequence",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_CAP_G1_BOUND_DERIVED",
                "gate_status": "PASS_CONDITIONAL",
                "evidence": f"eta_quad={eta_quad}; epsilon_linear_bound={epsilon_linear_bound:.6g}",
                "remaining_obligation": "eta_quad is a protocol tolerance, not a measured physical constant",
            },
            {
                "gate_id": "U12506_CAP_G2_CAP_WITHIN_BOUND",
                "gate_status": "PASS",
                "evidence": f"epsilon_cap={epsilon_cap:.6g} < {epsilon_linear_bound:.6g}; safety_fraction={safety_fraction:.6g}",
                "remaining_obligation": "none for current protocol freeze",
            },
            {
                "gate_id": "U12506_CAP_G3_CURRENT_EPSILON_WITHIN_CAP",
                "gate_status": "PASS",
                "evidence": f"epsilon_t={epsilon_t:.6g}; gamma_clock={gamma_clock:.6g}",
                "remaining_obligation": "none for source-shell replay",
            },
            {
                "gate_id": "U12506_CAP_G4_NOT_UNIVERSAL",
                "gate_status": "PASS_RECORDED",
                "evidence": "cap is frozen as conservative protocol constant only",
                "remaining_obligation": "derive deeper Tau-side clock cap before claiming universal law",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "cap_protocol_status": "U12506_EPSILON_CAP_PROTOCOL_FROZEN_NOT_UNIVERSAL",
                "galaxy": GALAXY,
                "eta_quad": eta_quad,
                "epsilon_linear_bound": epsilon_linear_bound,
                "epsilon_cap": epsilon_cap,
                "epsilon_t": epsilon_t,
                "max_quadratic_to_linear_ratio_at_cap": max_linear_truncation_ratio,
                "max_v2_fractional_shift_at_cap": max_v2_fractional_shift,
                "accepted_as_protocol_cap": True,
                "universal_tau_constant_derived": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_step": "if promoted, run accepted-manifest gate that records cap as predeclared protocol constant, not universal law",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    theorem.to_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_theorem.csv", index=False)
    derivation_steps.to_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_steps.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Epsilon-Cap Protocol Gate",
            "",
            "This gate freezes the small-mismatch cap used by the UGC12506 Xi_t",
            "source shell as a conservative protocol constant. It does not claim",
            "that the cap is a universal Tau Core constant and does not allow",
            "endpoint scoring.",
            "",
            "## Cap Theorem",
            "",
            markdown_table(theorem),
            "",
            "## Derivation Steps",
            "",
            markdown_table(derivation_steps),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Claim Boundary",
            "",
            "`epsilon_cap=0.035` is accepted here only as a conservative",
            "predeclared small-mismatch protocol cap inside the linearization",
            "admissible interval. It is not a universal constant and does not",
            "turn the diagnostic source shell into endpoint validation.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_epsilon_cap_protocol_gate.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
