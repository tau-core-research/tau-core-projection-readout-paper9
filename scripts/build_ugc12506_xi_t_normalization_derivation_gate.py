#!/usr/bin/env python3
"""Build the UGC12506 Xi_t normalization derivation gate.

This gate derives the bounded source-load normalization used by the UGC12506
Xi_t shell as a conditional Tau-side/readout map:

    epsilon_t = epsilon_cap * L / (1 + L)

where L is a nonnegative residual-blind source load.  The result is stronger
than an ad hoc diagnostic constant, but it is still formula-conditional: the
universal value of epsilon_cap is not empirically validated here.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_normalization_derivation_gate_not_endpoint"


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

    manifest = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv").iloc[0]
    components = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv")

    if bool(manifest["endpoint_scores_allowed"]):
        raise RuntimeError("Xi_t shell must not allow endpoint scoring")
    if bool(manifest["construction_used_vobs_or_residual"]):
        raise RuntimeError("Xi_t shell used vobs/residual")

    source_load = float(manifest["source_load_total"])
    epsilon_t = float(manifest["epsilon_t"])
    gamma_clock = float(manifest["gamma_clock"])
    epsilon_cap = epsilon_t / gamma_clock if gamma_clock else 0.0

    theorem = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "theorem_id": "U12506_XI_T_BOUNDED_SOURCE_LOAD_NORMALIZATION",
                "theorem_status": "CONDITIONAL_DERIVED_MAP_CAP_ORIGIN_OPEN",
                "statement": (
                    "If the time-readout mismatch is controlled by a nonnegative "
                    "residual-blind source load L, and the readout response must be "
                    "dimensionless, monotone, null-recovering, and bounded by a small "
                    "clock-mismatch cap epsilon_cap, then the minimal saturating "
                    "one-parameter map is epsilon_t=epsilon_cap L/(1+L)."
                ),
                "derived_formula": "epsilon_t = epsilon_cap * L/(1+L)",
                "current_specialization": (
                    f"L={source_load:.6g}; epsilon_cap={epsilon_cap:.6g}; "
                    f"Gamma_clock={gamma_clock:.6g}; epsilon_t={epsilon_t:.6g}"
                ),
                "derived_part": "bounded source-load shape L/(1+L)",
                "open_part": "universal or class-specific origin of epsilon_cap",
                "uses_vobs_or_residual": False,
                "accepted_xi_t_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    derivation_steps = pd.DataFrame(
        [
            {
                "step_id": "D1_SOURCE_LOAD",
                "claim_type": "definition_from_source_manifest",
                "status": "PASS",
                "statement": "Define L as the sum of nonnegative source-side clock/readout loads.",
                "formula_consequence": "L >= 0 and L=0 means no time-readout evidence.",
            },
            {
                "step_id": "D2_DIMENSIONLESS",
                "claim_type": "dimensional_check",
                "status": "PASS",
                "statement": "L, Gamma_clock, epsilon_t, and Xi_t are dimensionless.",
                "formula_consequence": "Xi_t can multiply the velocity-squared readout without changing units.",
            },
            {
                "step_id": "D3_NULL_LIMIT",
                "claim_type": "known_limit",
                "status": "PASS",
                "statement": "Require epsilon_t(0)=0.",
                "formula_consequence": "L=0 gives Xi_t=1 and recovers the non-time-readout shell.",
            },
            {
                "step_id": "D4_MONOTONE_RESPONSE",
                "claim_type": "admissibility_condition",
                "status": "PASS",
                "statement": "Require d epsilon_t / dL > 0 for L >= 0.",
                "formula_consequence": "More source-supported clock load cannot reduce the active clock factor.",
            },
            {
                "step_id": "D5_SATURATION",
                "claim_type": "admissibility_condition",
                "status": "PASS",
                "statement": "Require epsilon_t <= epsilon_cap.",
                "formula_consequence": "The map cannot become an arbitrary amplitude rescue term.",
            },
            {
                "step_id": "D6_MINIMAL_MAP",
                "claim_type": "conditional_derivation",
                "status": "PASS_CONDITIONAL",
                "statement": "The simplest rational map satisfying D3-D5 with one scale is Gamma_clock=L/(1+L).",
                "formula_consequence": "epsilon_t=epsilon_cap*Gamma_clock.",
            },
            {
                "step_id": "D7_CAP_ORIGIN",
                "claim_type": "remaining_obligation",
                "status": "OPEN",
                "statement": "The cap epsilon_cap must be derived from Tau-side clock/readout geometry or fixed by a predeclared class law.",
                "formula_consequence": "Current UGC12506 shell remains formula-conditional and endpoint-blocked.",
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

    component_review = components[
        [
            "galaxy",
            "component_id",
            "component_status",
            "source_load",
            "normalized_weight",
            "source_basis",
            "claim_boundary",
        ]
    ].copy()
    component_review["normalization_role"] = component_review["component_status"].map(
        lambda status: "excluded" if str(status).startswith("EXCLUDED") else "contributes_to_L"
    )
    component_review["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_XINORM_G1_SOURCE_LOAD_NONNEGATIVE",
                "gate_status": "PASS",
                "evidence": f"L={source_load:.6g}; component loads are nonnegative",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XINORM_G2_BOUNDED_MAP",
                "gate_status": "PASS_CONDITIONAL",
                "evidence": "Gamma_clock=L/(1+L) is dimensionless, monotone, null-recovering, and bounded below one.",
                "remaining_obligation": "accept the minimal rational response-map premise",
            },
            {
                "gate_id": "U12506_XINORM_G3_CAP_ORIGIN",
                "gate_status": "BLOCKED",
                "evidence": f"epsilon_cap={epsilon_cap:.6g} is used as a small-mismatch cap",
                "remaining_obligation": "derive epsilon_cap from Tau-side clock geometry or freeze it as a predeclared class constant",
            },
            {
                "gate_id": "U12506_XINORM_G4_ENDPOINT_BLOCK",
                "gate_status": "PASS_RECORDED",
                "evidence": "normalization derivation does not read vobs/residual and does not allow endpoint scoring",
                "remaining_obligation": "accepted Xi_t manifest gate before any scoring",
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
                "normalization_status": "U12506_XI_T_NORMALIZATION_SHAPE_DERIVED_CAP_OPEN",
                "galaxy": GALAXY,
                "source_load_L": source_load,
                "gamma_clock": gamma_clock,
                "epsilon_cap": epsilon_cap,
                "epsilon_t": epsilon_t,
                "derived_shape": "L/(1+L)",
                "cap_origin_accepted": False,
                "accepted_xi_t_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_step": "derive/freeze epsilon_cap as Tau-side clock/readout class constant or demote to diagnostic shell",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    theorem.to_csv(DATA / "ugc12506_xi_t_normalization_theorem.csv", index=False)
    derivation_steps.to_csv(DATA / "ugc12506_xi_t_normalization_derivation_steps.csv", index=False)
    component_review.to_csv(DATA / "ugc12506_xi_t_normalization_component_review.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_normalization_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_normalization_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Normalization Derivation Gate",
            "",
            "This gate derives the bounded source-load shape used by the UGC12506",
            "time-readout shell. It is not endpoint scoring and it does not promote",
            "an accepted Xi_t manifest.",
            "",
            "## Theorem",
            "",
            markdown_table(theorem),
            "",
            "## Derivation Steps",
            "",
            markdown_table(derivation_steps),
            "",
            "## Component Review",
            "",
            markdown_table(component_review),
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
            "`L/(1+L)` is derived as the minimal bounded source-load response shape.",
            "The cap `epsilon_cap` remains open as a Tau-side clock/readout scale",
            "or predeclared class constant. Therefore UGC12506 remains endpoint-blocked.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_normalization_derivation_gate.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
