#!/usr/bin/env python3
"""Record the NGC0891 direct spin-source hunt update for beta_cl transfer.

This gate extends the direct-source search with NGC891/NGC0891 literature
context found outside the local cache.  The checked sources strengthen the
halo/envelope/projection context, but they do not provide a direct
source-native halo/envelope lambda_spin value for the beta_cl slot.  Therefore
the transfer replay remains blocked.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint"


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

    sources = pd.DataFrame(
        [
            {
                "source_id": "OOSTERLOO2007_COLD_HI_HALO",
                "galaxy": "NGC0891",
                "source_reference": (
                    "Oosterloo, Fraternali & Sancisi 2007, AJ 134, 1019"
                ),
                "source_url": "https://arxiv.org/abs/0705.4034",
                "source_status": "CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA",
                "direct_lambda_spin_value": "",
                "accepted_context": (
                    "Huge H I halo, about 30 percent of total H I; lagging "
                    "differential rotation; possible low-angular-momentum accretion"
                ),
                "definition_issue": (
                    "Provides halo gas angular-momentum context, not a dimensionless "
                    "halo/envelope lambda_spin measurement for beta_cl"
                ),
                "accepted_as_beta_cl_lambda_spin": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "FRATERNALI_BINNEY2006_DYNAMICAL_MODEL",
                "galaxy": "NGC0891",
                "source_reference": (
                    "Fraternali & Binney 2006, MNRAS 366, 449"
                ),
                "source_url": "https://academic.oup.com/mnras/article/366/2/449/1214630",
                "source_status": "CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA",
                "direct_lambda_spin_value": "",
                "accepted_context": (
                    "Dynamical extraplanar-gas model; NGC 891 channel maps constrain "
                    "halo/fountain kinematics and kick geometry"
                ),
                "definition_issue": (
                    "Model parameters and kick geometry are not direct source-native "
                    "lambda_spin values"
                ),
                "accepted_as_beta_cl_lambda_spin": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "FRATERNALI_OOSTERLOO2004_EXTRA_PLANAR_NEUTRAL_GAS",
                "galaxy": "NGC0891",
                "source_reference": (
                    "Fraternali et al. 2004, extra-planar neutral gas in NGC 891"
                ),
                "source_url": "https://arxiv.org/abs/astro-ph/0410375",
                "source_status": "CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA",
                "direct_lambda_spin_value": "",
                "accepted_context": (
                    "3D modelling reports halo gas rotating more slowly than disk "
                    "and a vertical gradient of roughly -15 km/s/kpc"
                ),
                "definition_issue": (
                    "Kinematic lag supports envelope/projection context but does not "
                    "define beta_cl lambda_spin"
                ),
                "accepted_as_beta_cl_lambda_spin": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "source_id": "CIOTTI_FRATERNALI2009_STATIONARY_MODELS",
                "galaxy": "NGC0891",
                "source_reference": (
                    "Ciotti, Fraternali et al. 2009/2010, MNRAS 401, 2451"
                ),
                "source_url": "https://academic.oup.com/mnras/article/401/4/2451/1127410",
                "source_status": "CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA",
                "direct_lambda_spin_value": "",
                "accepted_context": (
                    "Stationary extraplanar-gas models are applied to NGC 891 to "
                    "test vertical rotation decrease"
                ),
                "definition_issue": (
                    "Potential/extraplanar-gas model context, not a halo-spin source"
                ),
                "accepted_as_beta_cl_lambda_spin": False,
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    sources.to_csv(
        DATA / "ugc12506_beta_closure_ngc0891_spin_source_hunt_update_sources.csv",
        index=False,
    )

    worklist = pd.DataFrame(
        [
            {
                "required_field": "ngc0891_direct_halo_or_envelope_lambda_spin",
                "current_status": "STILL_MISSING_AFTER_SOURCE_HUNT_UPDATE",
                "acceptable_evidence": (
                    "direct dimensionless halo/envelope spin parameter, or a "
                    "residual-blind conversion theorem from accepted source-native "
                    "kinematic/angular-momentum observables"
                ),
                "forbidden_inputs": (
                    "rotation residuals; endpoint RMSE; baseline rank; post-hoc "
                    "beta selection"
                ),
                "next_gate": "direct_source_search_or_independent_proxy_review_response",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "required_field": "ngc0891_proxy_review_decision",
                "current_status": "PENDING_INDEPENDENT_REVIEW_RESPONSE",
                "acceptable_evidence": (
                    "completed spin-proxy review response accepting source fields, "
                    "weight rule or caveated replacement, definition boundary, and "
                    "target scope"
                ),
                "forbidden_inputs": (
                    "rotation residuals; endpoint scores; direct disc-lambda insertion"
                ),
                "next_gate": "run_spin_proxy_review_response_intake",
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    worklist.to_csv(
        DATA / "ugc12506_beta_closure_ngc0891_spin_source_hunt_update_worklist.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "ngc0891_spin_source_hunt_status": (
                    "NGC0891_CONTEXT_STRENGTHENED_DIRECT_LAMBDA_STILL_BLOCKED"
                ),
                "n_sources_checked": int(len(sources)),
                "n_context_sources_accepted": int(
                    sources["source_status"].eq("CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA").sum()
                ),
                "n_direct_lambda_values_accepted": int(
                    sources["accepted_as_beta_cl_lambda_spin"].sum()
                ),
                "direct_lambda_spin_status": "still_missing",
                "proxy_review_status": "response_pending",
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": (
                    "independent_spin_proxy_review_response_or_new_direct_lambda_source"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_ngc0891_spin_source_hunt_update_summary.csv",
        index=False,
    )

    report = [
        "# NGC0891 Beta-Closure Spin Source Hunt Update",
        "",
        "This update checks NGC891/NGC0891 literature context for a direct",
        "halo/envelope `lambda_spin` value. The context strengthens the",
        "halo/envelope/projection motivation, but no checked source supplies the",
        "dimensionless beta_cl `lambda_spin` slot.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Sources Checked",
        "",
        markdown_table(sources),
        "",
        "## Remaining Worklist",
        "",
        markdown_table(worklist),
        "",
        "## Claim Boundary",
        "",
        "The source hunt strengthens context but does not unlock replay. The",
        "admissible next gate remains either an independent proxy-review response",
        "or a new direct source-native lambda/spin source.",
    ]
    (REPORTS / "ugc12506_beta_closure_ngc0891_spin_source_hunt_update.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
