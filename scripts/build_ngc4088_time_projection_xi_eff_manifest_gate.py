#!/usr/bin/env python3
"""Build the NGC4088 Xi_eff time-projection manifest gate.

This is a promotion gate, not an endpoint run.  It uses the residual-blind
q_warp/m_history independent review and the frozen B_i coefficient protocol to
ask whether a source-complete Xi_eff manifest can be accepted before scoring.

The answer is intentionally conservative: the source and coefficient gates now
pass, but a full endpoint remains blocked until the clock/readout channel is
separated from the already active additive warp-history morphology kernel and a
small-mismatch normalization is frozen.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "NGC4088"
CLAIM_BOUNDARY = "ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint"


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


def build_gate() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    source_review = pd.read_csv(
        DATA / "s4g75_ngc4088_source_response_independent_review_summary.csv"
    ).iloc[0]
    features = pd.read_csv(DATA / "s4g75_ngc4088_bi_feature_normalization.csv")
    coeffs = pd.read_csv(DATA / "s4g75_ngc4088_bi_sharp_coefficients.csv")
    bi_summary = pd.read_csv(DATA / "s4g75_ngc4088_bi_coefficient_rule_summary.csv").iloc[0]
    xi_readiness = pd.read_csv(DATA / "time_readout_xi_manifest_readiness.csv")
    xi_row = xi_readiness.loc[xi_readiness["galaxy"].eq(GALAXY)].iloc[0]

    coeff_by_feature = {
        str(row["multiplies_feature"]): float(row["sharp_value"]) for _, row in coeffs.iterrows()
    }
    terms = []
    for _, row in features.iterrows():
        symbol = str(row["feature_symbol"])
        feature_value = float(row["feature_value"])
        b_value = coeff_by_feature[symbol]
        term_value = b_value * feature_value
        terms.append(
            {
                "galaxy": GALAXY,
                "feature_symbol": symbol,
                "feature_value": feature_value,
                "coefficient_B_i": b_value,
                "term_value": term_value,
                "term_status": str(row["status"]),
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    terms_df = pd.DataFrame(terms)
    raw_epsilon_bound = float(terms_df["term_value"].sum())
    small_mismatch_cap = 0.035
    # Keep the same bounded rational form used elsewhere, but apply it to the
    # reviewed NGC4088 source load. This is still a protocol normalization, not
    # a final Tau-side clock-geometry derivation.
    gamma_clock = raw_epsilon_bound / (1.0 + raw_epsilon_bound)
    epsilon_candidate = small_mismatch_cap * gamma_clock

    source_ready = bool(source_review["numeric_bound_source_authorization"])
    bi_ready = str(bi_summary["numeric_bound_status"]) == "NUMERIC_EPSILON_PROTOCOL_BOUND_READY"
    small_mismatch_ready = 0.0 <= epsilon_candidate <= small_mismatch_cap
    double_count_blocker = True
    endpoint_allowed = False
    control_allowed = source_ready and bi_ready and small_mismatch_ready

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "manifest_status": "NGC4088_XI_EFF_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED"
                if control_allowed
                else "NGC4088_XI_EFF_MANIFEST_BLOCKED",
                "formula_text": "Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R); Xi_path=1 for this route",
                "kernel_text": "Xi_eff(R)=1+epsilon_clock*K_t(R); K_t inherits reviewed warp-history phase shape",
                "raw_source_bound_L": raw_epsilon_bound,
                "gamma_clock": gamma_clock,
                "epsilon_cap_protocol": small_mismatch_cap,
                "epsilon_clock_candidate": epsilon_candidate,
                "xi_eff_min": 1.0,
                "xi_eff_max": 1.0 + epsilon_candidate,
                "xi_path_policy": "Xi_path=1; no path term is primary for NGC4088 route",
                "source_review_ready": source_ready,
                "bi_rule_ready": bi_ready,
                "small_mismatch_ready": small_mismatch_ready,
                "double_count_blocker": double_count_blocker,
                "control_manifest_allowed": control_allowed,
                "endpoint_scores_allowed": endpoint_allowed,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "N4088_XIEFF_G1_QMEM_SOURCE_REVIEW",
                "gate_status": "PASS" if source_ready else "BLOCKED",
                "evidence": str(source_review["source_review_status"]),
                "remaining_obligation": "none" if source_ready else "complete q_warp/m_history review",
            },
            {
                "gate_id": "N4088_XIEFF_G2_BI_RULE_READY",
                "gate_status": "PASS" if bi_ready else "BLOCKED",
                "evidence": str(bi_summary["numeric_bound_status"]),
                "remaining_obligation": "none" if bi_ready else "freeze residual-blind B_i coefficient rule",
            },
            {
                "gate_id": "N4088_XIEFF_G3_SMALL_MISMATCH_PROTOCOL",
                "gate_status": "PASS_PROTOCOL",
                "evidence": f"epsilon_clock_candidate={epsilon_candidate:.6g} <= {small_mismatch_cap:.6g}",
                "remaining_obligation": "derive the cap from Tau-side clock geometry before universal claim",
            },
            {
                "gate_id": "N4088_XIEFF_G4_PATH_POLICY",
                "gate_status": "PASS_ZERO_PATH",
                "evidence": "Xi_path fixed to one for this NGC4088 warp-history route",
                "remaining_obligation": "do not activate path term without independent path evidence",
            },
            {
                "gate_id": "N4088_XIEFF_G5_DOUBLE_COUNT_SEPARATION",
                "gate_status": "BLOCKED",
                "evidence": (
                    "NGC4088 already has an additive warp-history morphology kernel; "
                    "the clock/readout contribution must be separated by an ablation manifest"
                ),
                "remaining_obligation": "build additive-kernel vs Xi_eff clock ablation before endpoint scoring",
            },
            {
                "gate_id": "N4088_XIEFF_G6_ENDPOINT_PERMISSION",
                "gate_status": "BLOCKED",
                "evidence": "endpoint_scores_allowed=False",
                "remaining_obligation": "endpoint scoring requires a separate accepted endpoint permission gate",
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
                "xi_eff_manifest_status": "NGC4088_XI_EFF_CONTROL_READY_ENDPOINT_BLOCKED"
                if control_allowed
                else "NGC4088_XI_EFF_BLOCKED",
                "galaxy": GALAXY,
                "raw_source_bound_L": raw_epsilon_bound,
                "epsilon_clock_candidate": epsilon_candidate,
                "xi_trial_status": str(xi_row["xi_trial_status"]),
                "control_manifest_allowed": control_allowed,
                "endpoint_scores_allowed": endpoint_allowed,
                "blocking_gate": "N4088_XIEFF_G5_DOUBLE_COUNT_SEPARATION",
                "next_step": "build additive-warp/history vs Xi_eff clock ablation manifest; no endpoint scoring yet",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return manifest, terms_df, gates, summary


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    manifest, terms, gates, summary = build_gate()
    manifest.to_csv(DATA / "ngc4088_time_projection_xi_eff_manifest_gate.csv", index=False)
    terms.to_csv(DATA / "ngc4088_time_projection_xi_eff_terms.csv", index=False)
    gates.to_csv(DATA / "ngc4088_time_projection_xi_eff_manifest_gate_items.csv", index=False)
    summary.to_csv(DATA / "ngc4088_time_projection_xi_eff_manifest_summary.csv", index=False)

    report = "\n".join(
        [
            "# NGC4088 Time-Projection Xi_eff Manifest Gate",
            "",
            "This promotion gate uses the accepted q_warp/m_history source review",
            "and the residual-blind B_i coefficient protocol. It does not read",
            "rotation residuals and does not permit endpoint scoring.",
            "",
            "## Manifest",
            "",
            markdown_table(manifest),
            "",
            "## Source Terms",
            "",
            markdown_table(terms),
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
            "NGC4088 has moved beyond the q_warp/m_history blocker: the source",
            "terms and B_i rule are now available for a control manifest. The",
            "remaining scientific blocker is double-count separation: the Xi_eff",
            "clock/readout layer must be separated from the already active additive",
            "warp-history morphology kernel before any endpoint score is allowed.",
            "",
        ]
    )
    (REPORTS / "ngc4088_time_projection_xi_eff_manifest_gate.md").write_text(
        report, encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
