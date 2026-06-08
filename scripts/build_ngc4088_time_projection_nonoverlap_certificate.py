#!/usr/bin/env python3
"""Build an explicit NGC4088 time-projection non-overlap certificate.

This is a proof/certificate artifact, not a new scoring run.  It formalizes the
question: can the current NGC4088 Xi_t/time-projection layer be promoted as an
independent endpoint contribution on top of the accepted additive warp/history
kernel?

The answer with the current source ledger is negative: every current Xi_t term
maps to an already-active additive warp/history source token.  Therefore the
orthogonal clock load is zero and the additive-plus-clock curve remains a
stress/control curve, not an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ngc4088_time_projection_nonoverlap_certificate_not_endpoint"


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
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    overlap = pd.read_csv(DATA / "ngc4088_time_projection_double_count_overlap_audit.csv")
    policy = pd.read_csv(DATA / "ngc4088_time_projection_double_count_policy.csv").iloc[0]
    scores = pd.read_csv(DATA / "ngc4088_time_projection_ablation_control_scores.csv")
    summary = pd.read_csv(DATA / "ngc4088_time_projection_ablation_control_summary.csv").iloc[0]

    certificate_rows = []
    for _, row in overlap.iterrows():
        allowed = bool(row["orthogonal_clock_residual_allowed"])
        certificate_rows.append(
            {
                "galaxy": row["galaxy"],
                "xi_eff_feature": row["xi_eff_feature"],
                "term_value": float(row["xi_eff_term_value"]),
                "additive_token": row["overlapping_additive_token"],
                "overlap_status": row["overlap_status"],
                "belongs_to_orthogonal_clock_subspace": allowed,
                "orthogonal_term_value": float(row["xi_eff_term_value"]) if allowed else 0.0,
                "proof_reason": row["reason"],
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    certificate = pd.DataFrame(certificate_rows)
    raw_load = float(certificate["term_value"].sum())
    orthogonal_load = float(certificate["orthogonal_term_value"].sum())
    n_terms = int(len(certificate))
    n_orthogonal = int(certificate["belongs_to_orthogonal_clock_subspace"].sum())
    epsilon_candidate = float(policy["epsilon_clock_candidate"])

    theorem = pd.DataFrame(
        [
            {
                "theorem_id": "NGC4088_TIME_NONOVERLAP_CERTIFICATE_001",
                "statement": (
                    "Given the current source-frozen NGC4088 Xi_t ledger, the "
                    "orthogonal clock/readout contribution on top of the accepted "
                    "additive warp/history route is zero."
                ),
                "assumption_A1": "Additive route uses warp geometry, radial onset, q_warp strength, and morphology-history phase.",
                "assumption_A2": "Current Xi_t terms are f_PA, f_R, f_q, and f_mem from the frozen source ledger.",
                "derived_D1": "Each Xi_t term overlaps one additive route source token.",
                "derived_D2": "Orthogonal clock load is the sum of only non-overlapping Xi_t terms.",
                "numeric_certificate": f"n_terms={n_terms}; n_orthogonal={n_orthogonal}; raw_load={raw_load:.6g}; orthogonal_load={orthogonal_load:.6g}",
                "conclusion": (
                    "The accepted combined route must set Xi_eff=1; additive-plus-clock "
                    "is a stress/control curve, not endpoint evidence."
                ),
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    consequences = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "route": "accepted_warp_history",
                "rmse_km_s": float(
                    scores.loc[
                        scores["model_id"].eq("N4088_BASE_PROJECTION"), "rmse_km_s"
                    ].iloc[0]
                ),
                "status_after_certificate": "endpoint_readable_caveated_control",
                "reason": "This route contains the accepted source-supported additive warp/history information.",
            },
            {
                "galaxy": "NGC4088",
                "route": "clock_only_control",
                "rmse_km_s": float(summary["clock_only_rmse_km_s"]),
                "status_after_certificate": "diagnostic_control_only",
                "reason": "Clock-only signal is informative but not independent endpoint evidence.",
            },
            {
                "galaxy": "NGC4088",
                "route": "additive_plus_clock_stress",
                "rmse_km_s": float(summary["additive_plus_clock_rmse_km_s"]),
                "status_after_certificate": "stress_control_double_count_blocked",
                "reason": "Lower RMSE cannot be promoted because orthogonal clock load is zero.",
            },
        ]
    )
    consequences["endpoint_scores_allowed"] = False
    consequences.loc[
        consequences["route"].eq("accepted_warp_history"), "endpoint_scores_allowed"
    ] = True
    consequences["endpoint_validation_claim"] = False
    consequences["claim_boundary"] = CLAIM_BOUNDARY

    certificate.to_csv(DATA / "ngc4088_time_projection_nonoverlap_certificate_terms.csv", index=False)
    theorem.to_csv(DATA / "ngc4088_time_projection_nonoverlap_certificate_theorem.csv", index=False)
    consequences.to_csv(DATA / "ngc4088_time_projection_nonoverlap_certificate_consequences.csv", index=False)

    proof_text = "\n\n".join(
        [
            "# NGC4088 Time-Projection Non-Overlap Certificate",
            (
                "This certificate proves the current status of the NGC4088 time-projection "
                "layer.  It is not a new fit and it does not read rotation residuals."
            ),
            "## Theorem",
            markdown_table(theorem),
            "## Term Certificate",
            markdown_table(certificate),
            "## Consequences",
            markdown_table(consequences),
            "## Proof",
            (
                "Let A be the source subspace already assigned to the accepted additive "
                "warp/history morphology route.  In the current ledger A is generated by "
                "warp geometry, radial onset, q_warp source strength, and morphology-history "
                "phase.  Let T be the current Xi_t/time-projection source ledger with terms "
                "f_PA, f_R, f_q, and f_mem.  The overlap audit maps f_PA to shared warp "
                "geometry, f_R to shared radial onset support, f_q to q_warp source strength, "
                "and f_mem to the shared morphology-history phase.  Hence every generator "
                "of T lies in A for the currently frozen source ledger."
            ),
            (
                "Define the endpoint-admissible clock load as the load carried by the "
                "quotient T/A, i.e. only by Xi_t terms that do not overlap A.  Since all "
                "current terms lie in A, T/A has zero current load.  Numerically the raw "
                f"clock load is {raw_load:.6g}, but the orthogonal load is {orthogonal_load:.6g}. "
                "Therefore the endpoint-admissible clock multiplier on top of the accepted "
                "additive route is Xi_eff=1."
            ),
            (
                "The lower RMSE of the additive-plus-clock stress curve is therefore not "
                "evidence for an endpoint time-projection contribution.  It is evidence that "
                "the clock-shaped control is correlated with the same source morphology "
                "already used by the accepted additive kernel.  A future endpoint would "
                "require a new residual-blind clock/path observable that survives this "
                "quotient test."
            ),
        ]
    )
    (REPORTS / "ngc4088_time_projection_nonoverlap_certificate.md").write_text(
        proof_text + "\n", encoding="utf-8"
    )

    print("NGC4088_TIME_PROJECTION_NONOVERLAP_CERTIFICATE_COMPLETE")
    print(theorem[["theorem_id", "numeric_certificate", "conclusion"]].to_string(index=False))


if __name__ == "__main__":
    main()
