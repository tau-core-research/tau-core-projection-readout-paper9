#!/usr/bin/env python3
"""Audit whether a literature disc lambda can fill the beta_cl lambda slot.

NGC7331 has a published disc-spin-like lambda value from Marr (2015).  This
gate checks whether that value can be inserted into the beta_cl halo/envelope
lambda_spin slot.  It preserves the value as source context, but rejects direct
substitution because the definitions and normalization roles differ.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint"
LAMBDA_REF = 0.10


def markdown_table(df: pd.DataFrame) -> str:
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(
                lambda value: "" if pd.isna(value) else f"{value:.6g}"
            )
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

    direct = pd.read_csv(DATA / "ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv")
    proxy = pd.read_csv(DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv")
    ngc7331_direct = direct[
        (direct["galaxy"].eq("NGC7331"))
        & direct["source_field"].eq("disc_spin_lambda")
    ].iloc[0]
    ngc7331_proxy = proxy[proxy["galaxy"].eq("NGC7331")].iloc[0]

    lambda_disc = float(ngc7331_direct["source_value"])
    lambda_proxy = float(ngc7331_proxy["lambda_spin_proxy_candidate"])
    nfw_load = float(ngc7331_proxy["nfw_preference_load"])
    edgeon_load = float(ngc7331_proxy["edgeon_load"])
    beta_if_direct = 1.0 + (lambda_disc / LAMBDA_REF) * nfw_load + edgeon_load
    beta_if_proxy = 1.0 + (lambda_proxy / LAMBDA_REF) * nfw_load + edgeon_load

    checks = pd.DataFrame(
        [
            {
                "check_id": "C1_same_physical_object",
                "question": "Does the source lambda measure the same halo/envelope spin slot as beta_cl?",
                "result": "FAIL",
                "reason": "Marr lambda is a disc-spin parameter in a lognormal self-gravitating disc model.",
                "endpoint_permission": False,
            },
            {
                "check_id": "C2_same_normalization_role",
                "question": "Can lambda=0.423 be used against lambda_ref=0.10 without conversion?",
                "result": "FAIL",
                "reason": "The beta_cl lambda slot is a source-normalization amplifier, not a universal disc-spin constant.",
                "endpoint_permission": False,
            },
            {
                "check_id": "C3_residual_blind_source",
                "question": "Is the Marr value source-side and residual-blind?",
                "result": "PASS_CONTEXT",
                "reason": "The value is literature source context and does not use the endpoint residual.",
                "endpoint_permission": False,
            },
            {
                "check_id": "C4_conversion_rule_available",
                "question": "Is there a predeclared disc-to-halo/envelope conversion rule?",
                "result": "FAIL",
                "reason": "No residual-blind conversion functional from disc lambda to beta_cl lambda_spin is accepted.",
                "endpoint_permission": False,
            },
        ]
    )
    checks["claim_boundary"] = CLAIM_BOUNDARY

    comparison = pd.DataFrame(
        [
            {
                "galaxy": "NGC7331",
                "lambda_disc_marr2015": lambda_disc,
                "lambda_spin_proxy_candidate": lambda_proxy,
                "lambda_ref": LAMBDA_REF,
                "nfw_preference_load": nfw_load,
                "edgeon_load": edgeon_load,
                "beta_if_direct_disc_lambda_substituted": beta_if_direct,
                "beta_if_proxy_candidate_used": beta_if_proxy,
                "direct_minus_proxy_beta": beta_if_direct - beta_if_proxy,
                "direct_substitution_allowed": False,
                "proxy_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    worklist = pd.DataFrame(
        [
            {
                "required_object": "disc_to_halo_envelope_lambda_conversion",
                "required_evidence": (
                    "source-side relation between disc angular-momentum lambda and "
                    "halo/envelope lambda_spin for the beta_cl closure slot"
                ),
                "forbidden_inputs": "rotation residual; endpoint score; best-fit beta; wrong-family rank",
                "status": "MISSING",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "required_object": "ngc7331_direct_halo_or_envelope_spin",
                "required_evidence": "direct source-native halo/envelope spin or accepted kinematic proxy",
                "forbidden_inputs": "rotation residual; endpoint score",
                "status": "MISSING",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "definition_conversion_status": (
                    "NGC7331_DISC_LAMBDA_CONTEXT_ACCEPTED_DIRECT_SUBSTITUTION_REJECTED"
                ),
                "direct_disc_lambda_context_accepted": True,
                "direct_substitution_allowed": False,
                "conversion_rule_available": False,
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "next_gate": (
                    "derive_residual_blind_disc_to_halo_envelope_conversion_or_keep_proxy_review"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    checks.to_csv(
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_checks.csv",
        index=False,
    )
    comparison.to_csv(
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_comparison.csv",
        index=False,
    )
    worklist.to_csv(
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_worklist.csv",
        index=False,
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_lambda_definition_conversion_summary.csv",
        index=False,
    )

    report = [
        "# NGC7331 Lambda Definition-Conversion Gate",
        "",
        "This gate audits whether the Marr (2015) NGC7331 disc-spin value can",
        "fill the beta_cl halo/envelope lambda_spin slot. It cannot be directly",
        "substituted.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Checks",
        "",
        markdown_table(checks),
        "",
        "## Numeric Comparison",
        "",
        markdown_table(comparison),
        "",
        "## Required Conversion Worklist",
        "",
        markdown_table(worklist),
        "",
        "## Claim Boundary",
        "",
        "Marr (2015) is accepted as source-side angular-momentum context for",
        "NGC7331. It is not accepted as the beta_cl lambda_spin value because",
        "the beta_cl slot is a halo/envelope closure-normalization quantity.",
        "No replay or endpoint score is allowed by this gate.",
    ]
    (REPORTS / "ugc12506_beta_closure_lambda_definition_conversion_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(checks.to_string(index=False))
    print(comparison.to_string(index=False))


if __name__ == "__main__":
    main()
