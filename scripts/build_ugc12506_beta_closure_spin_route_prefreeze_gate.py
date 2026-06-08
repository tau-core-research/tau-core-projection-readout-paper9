#!/usr/bin/env python3
"""Build the beta-closure spin-route prefreeze gate.

This gate is intentionally downstream of the independent spin-proxy review
intake.  It does not choose a spin-normalization route itself.  It only records
whether a route has been independently selected and, if so, which frozen inputs
would be carried into a later beta_cl transfer preflight.

In the current repository state the review response is still pending, so this
script should produce a blocked gate and no replay permission.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint"


INTAKE_SUMMARY = DATA / "ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv"
EXPOSURE_VALUES = DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv"
BULLOCK_VALUES = DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv"
VALUE_COLUMNS = [
    "galaxy",
    "selected_spin_normalization_route",
    "lambda_spin_prefreeze_value",
    "source_value_column",
    "source_artifact",
    "prefreeze_value_status",
    "beta_cl_replay_allowed",
    "endpoint_scores_allowed",
    "uses_vobs_or_residual",
    "claim_boundary",
]


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


def norm_upper(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().upper()


def make_blocked(reason: str, selected_route: str = "PENDING_INDEPENDENT_REVIEW") -> tuple[pd.DataFrame, pd.DataFrame]:
    gate = pd.DataFrame(
        [
            {
                "gate_id": "BSP_PREFREEZE_1_INTAKE_ACCEPTED",
                "gate_status": "BLOCKED",
                "reason": reason,
                "selected_spin_normalization_route": selected_route,
                "beta_cl_transfer_prefreeze_allowed": False,
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary = pd.DataFrame(
        [
            {
                "spin_route_prefreeze_status": (
                    "U12506_BETA_SPIN_ROUTE_PREFREEZE_BLOCKED_REVIEW_ROUTE_PENDING"
                ),
                "selected_spin_normalization_route": selected_route,
                "n_prefrozen_transfer_rows": 0,
                "beta_cl_transfer_prefreeze_allowed": False,
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_gate": "obtain_independent_spin_route_review_response",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return gate, summary


def route_values(selected_route: str) -> pd.DataFrame:
    if selected_route == "EXPOSURE_PROXY":
        queue = pd.read_csv(EXPOSURE_VALUES)
        return pd.DataFrame(
            {
                "galaxy": queue["galaxy"],
                "selected_spin_normalization_route": selected_route,
                "lambda_spin_prefreeze_value": queue["lambda_spin_proxy_candidate"],
                "source_value_column": "lambda_spin_proxy_candidate",
                "source_artifact": str(EXPOSURE_VALUES.relative_to(ROOT)),
                "prefreeze_value_status": "CAVEATED_EXPOSURE_PROXY_REVIEW_ACCEPTED",
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    if selected_route in {"BULLOCK_DISK_CONVERSION", "BULLOCK_LIKE_CONVERSION"}:
        values = pd.read_csv(BULLOCK_VALUES)
        return pd.DataFrame(
            {
                "galaxy": values["galaxy"],
                "selected_spin_normalization_route": selected_route,
                "lambda_spin_prefreeze_value": values["lambda_bullock_disk_proxy"],
                "source_value_column": "lambda_bullock_disk_proxy",
                "source_artifact": str(BULLOCK_VALUES.relative_to(ROOT)),
                "prefreeze_value_status": "CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED",
                "beta_cl_replay_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(columns=VALUE_COLUMNS)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    if not INTAKE_SUMMARY.exists():
        gate, summary = make_blocked("review response intake summary missing")
        values = pd.DataFrame(columns=VALUE_COLUMNS)
    else:
        intake = pd.read_csv(INTAKE_SUMMARY).iloc[0]
        selected_route = norm_upper(intake.get("selected_spin_normalization_route", ""))
        preflight_allowed = bool(intake.get("beta_cl_replay_preflight_allowed", False))
        if not preflight_allowed:
            gate, summary = make_blocked(
                "independent review has not accepted a spin-normalization route",
                selected_route or "PENDING_INDEPENDENT_REVIEW",
            )
            values = pd.DataFrame(columns=VALUE_COLUMNS)
        else:
            values = route_values(selected_route)
            route_supported = not values.empty
            gate = pd.DataFrame(
                [
                    {
                        "gate_id": "BSP_PREFREEZE_1_INTAKE_ACCEPTED",
                        "gate_status": "PASS" if route_supported else "BLOCKED",
                        "reason": (
                            "independent review accepted a supported spin route"
                            if route_supported
                            else f"selected route {selected_route} has no implemented value map"
                        ),
                        "selected_spin_normalization_route": selected_route,
                        "beta_cl_transfer_prefreeze_allowed": route_supported,
                        "beta_cl_replay_allowed": False,
                        "endpoint_scores_allowed": False,
                        "uses_vobs_or_residual": False,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                ]
            )
            summary = pd.DataFrame(
                [
                    {
                        "spin_route_prefreeze_status": (
                            "U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE"
                            if route_supported
                            else "U12506_BETA_SPIN_ROUTE_PREFREEZE_BLOCKED_UNSUPPORTED_ROUTE"
                        ),
                        "selected_spin_normalization_route": selected_route,
                        "n_prefrozen_transfer_rows": len(values),
                        "beta_cl_transfer_prefreeze_allowed": route_supported,
                        "beta_cl_replay_allowed": False,
                        "endpoint_scores_allowed": False,
                        "uses_vobs_or_residual": False,
                        "next_gate": (
                            "build_beta_cl_transfer_replay_prefreeze_manifest"
                            if route_supported
                            else "implement_selected_spin_route_value_map"
                        ),
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                ]
            )

    gate.to_csv(DATA / "ugc12506_beta_closure_spin_route_prefreeze_gate.csv", index=False)
    summary.to_csv(
        DATA / "ugc12506_beta_closure_spin_route_prefreeze_summary.csv",
        index=False,
    )
    values.to_csv(
        DATA / "ugc12506_beta_closure_spin_route_prefreeze_values.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Spin Route Prefreeze Gate",
        "",
        "This gate is downstream of the independent spin-proxy review intake.",
        "It does not select a route and it does not run replay scores.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gate",
        "",
        markdown_table(gate),
        "",
    ]
    if not values.empty:
        report += ["## Prefrozen Values", "", markdown_table(values), ""]
    report += [
        "## Claim Boundary",
        "",
        "A passed route prefreeze would only create a source-frozen input map",
        "for a later beta_cl transfer preflight. Endpoint scoring remains false",
        "in this gate.",
    ]
    (REPORTS / "ugc12506_beta_closure_spin_route_prefreeze_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
