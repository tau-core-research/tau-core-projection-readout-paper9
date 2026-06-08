#!/usr/bin/env python3
"""Build the residual-blind spin-route decision matrix for UGC12506 beta_cl.

The matrix is a reviewer-facing guardrail.  It compares the currently available
routes for filling the beta_cl spin/envelope normalization slot, but it does
not choose a route and it does not score a rotation curve.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint"


EXPOSURE_QUEUE = DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv"
BULLOCK_COMPARISON = DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv"
DIRECT_SUMMARY = DATA / "ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv"
INTAKE_SUMMARY = DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv"
PREFREEZE_SUMMARY = DATA / "ugc12506_beta_closure_spin_route_prefreeze_summary.csv"


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


def scalar_from_csv(path: Path, column: str, default: object = "") -> object:
    if not path.exists():
        return default
    df = pd.read_csv(path)
    if df.empty or column not in df.columns:
        return default
    return df.iloc[0][column]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    exposure = pd.read_csv(EXPOSURE_QUEUE)
    bullock = pd.read_csv(BULLOCK_COMPARISON)
    exposure_primary = exposure[exposure["galaxy"].eq("NGC0891")].iloc[0]
    exposure_secondary = exposure[exposure["galaxy"].eq("NGC7331")].iloc[0]
    bullock_primary = bullock[bullock["galaxy"].eq("NGC0891")].iloc[0]
    bullock_secondary = bullock[bullock["galaxy"].eq("NGC7331")].iloc[0]

    matrix = pd.DataFrame(
        [
            {
                "route_id": "EXPOSURE_PROXY",
                "route_status": "REVIEWABLE_NOT_ACCEPTED",
                "normalization_definition": (
                    "lambda_ref*(1+0.35 extent+0.25 velocity+0.25 gas+0.15 edgeon)"
                ),
                "ngc0891_lambda_value": exposure_primary["lambda_spin_proxy_candidate"],
                "ngc7331_lambda_value": exposure_secondary["lambda_spin_proxy_candidate"],
                "source_basis": "SPARC RHI/Rdisk, Vflat, H I mass, inclination",
                "main_strength": "captures envelope/exposure load explicitly",
                "main_risk": "weight coefficients are protocol candidates, not derived spin theory",
                "review_decision_needed": "ACCEPT_EXPOSURE_RULE or reject/replace",
                "prefreeze_if_accepted": True,
                "replay_if_accepted_here": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "forbidden_interpretation": "not a direct lambda_spin measurement",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "route_id": "BULLOCK_DISK_CONVERSION",
                "route_status": "REVIEWABLE_NOT_ACCEPTED",
                "normalization_definition": (
                    "lambda'_disk=(2 Rdisk Vflat)/(sqrt(2) R200 V200)"
                ),
                "ngc0891_lambda_value": bullock_primary["lambda_bullock_disk_proxy"],
                "ngc7331_lambda_value": bullock_secondary["lambda_bullock_disk_proxy"],
                "source_basis": "SPARC Rdisk,Vflat plus Li2020 NFW-flat V200",
                "main_strength": "standard angular-momentum conversion control",
                "main_risk": "disk specific angular momentum may not fill halo/envelope closure slot",
                "review_decision_needed": "ACCEPT_BULLOCK_CONVERSION or reject/replace",
                "prefreeze_if_accepted": True,
                "replay_if_accepted_here": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "forbidden_interpretation": "not accepted as Tau-side beta_cl spin slot without review",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "route_id": "DIRECT_SOURCE_NATIVE_SPIN",
                "route_status": "PREFERRED_BUT_CURRENTLY_MISSING",
                "normalization_definition": "source-native halo/envelope lambda_spin",
                "ngc0891_lambda_value": "",
                "ngc7331_lambda_value": "",
                "source_basis": "future direct source-native spin measurement or accepted conversion",
                "main_strength": "cleanest definition match",
                "main_risk": "not currently available for the beta_cl slot",
                "review_decision_needed": "supply direct source or keep route blocked",
                "prefreeze_if_accepted": True,
                "replay_if_accepted_here": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "forbidden_interpretation": "Marr disc lambda cannot be inserted directly",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "route_id": "REJECT_ROUTE",
                "route_status": "VALID_NEGATIVE_REVIEW_OUTCOME",
                "normalization_definition": "none",
                "ngc0891_lambda_value": "",
                "ngc7331_lambda_value": "",
                "source_basis": "review rejects all available spin-normalization routes",
                "main_strength": "preserves negative result and blocks amplitude rescue",
                "main_risk": "UGC12506 beta_cl transfer remains unresolved",
                "review_decision_needed": "reject proxy route or require new residual-blind rule",
                "prefreeze_if_accepted": False,
                "replay_if_accepted_here": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "forbidden_interpretation": "not a Tau Core failure; only route failure",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    direct_status = scalar_from_csv(
        DIRECT_SUMMARY,
        "direct_lambda_spin_gate_status",
        "UNKNOWN_DIRECT_SOURCE_STATUS",
    )
    intake_status = scalar_from_csv(
        INTAKE_SUMMARY,
        "review_intake_status",
        "UNKNOWN_REVIEW_INTAKE_STATUS",
    )
    prefreeze_status = scalar_from_csv(
        PREFREEZE_SUMMARY,
        "spin_route_prefreeze_status",
        "UNKNOWN_PREFREEZE_STATUS",
    )

    summary = pd.DataFrame(
        [
            {
                "spin_route_decision_matrix_status": (
                    "U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED"
                ),
                "n_routes": len(matrix),
                "n_reviewable_not_accepted": int(
                    matrix["route_status"].eq("REVIEWABLE_NOT_ACCEPTED").sum()
                ),
                "direct_source_status": direct_status,
                "review_intake_status": intake_status,
                "prefreeze_status": prefreeze_status,
                "preferred_scientific_route": "DIRECT_SOURCE_NATIVE_SPIN",
                "current_practical_routes": "EXPOSURE_PROXY;BULLOCK_DISK_CONVERSION",
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": "external_review_select_or_reject_spin_normalization_route",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    matrix.to_csv(DATA / "ugc12506_beta_closure_spin_route_decision_matrix.csv", index=False)
    summary.to_csv(
        DATA / "ugc12506_beta_closure_spin_route_decision_matrix_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Spin Route Decision Matrix",
        "",
        "This matrix compares residual-blind spin-normalization routes for the",
        "UGC12506 beta_cl transfer problem. It does not choose a route, run a",
        "replay, or authorize endpoint scoring.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Route Matrix",
        "",
        markdown_table(matrix),
        "",
        "## Claim Boundary",
        "",
        "The cleanest scientific route remains a direct source-native halo/envelope",
        "spin measurement. The two currently computable routes are reviewable",
        "controls only. If all routes are rejected, that is a preserved route-level",
        "negative result rather than a Tau Core endpoint failure.",
    ]
    (REPORTS / "ugc12506_beta_closure_spin_route_decision_matrix.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
