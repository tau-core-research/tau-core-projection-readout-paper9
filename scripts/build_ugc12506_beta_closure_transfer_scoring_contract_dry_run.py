#!/usr/bin/env python3
"""Build a no-vobs dry-run contract for UGC12506 beta-closure transfer scoring.

This script does not accept reviewer decisions and does not run endpoint
scores.  It answers a narrower engineering/science-contract question:
if an independent reviewer later accepts one of the already implemented
spin-normalization routes and the BARYONIC_050_FAST_PACKET carrier, would the
separate scoring runner have all non-observed inputs needed to execute?

The dry run deliberately reads only source/proxy fields and baryonic carrier
columns from the fast SPARC packet.  It does not read vobs or residual columns.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_scoring_contract_dry_run_not_endpoint"

EXPOSURE_VALUES = DATA / "ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv"
SOURCE_PROXY_FIELDS = DATA / "ugc12506_beta_closure_source_declared_spin_proxy_fields.csv"
BULLOCK_VALUES = DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv"
PRIORITY_GATE = DATA / "ugc12506_beta_closure_transfer_priority_gate.csv"
FAST_SPARC_POINTS = DATA / "fast_sparc_rotation_curve_packet_points.csv"

SCENARIOS = [
    {
        "dry_run_scenario_id": "IF_REVIEW_ACCEPTS_EXPOSURE_PROXY_AND_BARYONIC_CARRIER",
        "selected_spin_normalization_route": "EXPOSURE_PROXY",
        "source_value_column": "lambda_spin_proxy_candidate",
        "source_artifact": "data/derived/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv",
    },
    {
        "dry_run_scenario_id": "IF_REVIEW_ACCEPTS_BULLOCK_DISK_CONVERSION_AND_BARYONIC_CARRIER",
        "selected_spin_normalization_route": "BULLOCK_DISK_CONVERSION",
        "source_value_column": "lambda_bullock_disk_proxy",
        "source_artifact": "data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv",
    },
]

PREDICTION_COLUMNS = [
    "dry_run_scenario_id",
    "galaxy",
    "radius_kpc",
    "carrier_id",
    "formula_id",
    "selected_spin_normalization_route",
    "lambda_spin_value",
    "nfw_preference_load",
    "edgeon_load",
    "beta_cl_value",
    "v_carrier_kms",
    "v_beta_cl_transfer_kms",
    "construction_used_vobs",
    "scoring_used_vobs",
    "endpoint_scores_allowed",
    "endpoint_validation_claim",
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


def source_values_for_route(route: str) -> pd.DataFrame:
    if route == "EXPOSURE_PROXY":
        values = pd.read_csv(EXPOSURE_VALUES)
        return values[["galaxy", "lambda_spin_proxy_candidate"]].rename(
            columns={"lambda_spin_proxy_candidate": "lambda_spin_value"}
        )
    if route == "BULLOCK_DISK_CONVERSION":
        values = pd.read_csv(BULLOCK_VALUES)
        return values[["galaxy", "lambda_bullock_disk_proxy"]].rename(
            columns={"lambda_bullock_disk_proxy": "lambda_spin_value"}
        )
    return pd.DataFrame(columns=["galaxy", "lambda_spin_value"])


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    priority = pd.read_csv(PRIORITY_GATE)
    source_fields = pd.read_csv(SOURCE_PROXY_FIELDS)
    source_loads = source_fields[["galaxy", "edgeon_load"]].drop_duplicates("galaxy")
    # Read only non-observed carrier and radius fields.  Do not read vobs.
    fast = pd.read_csv(
        FAST_SPARC_POINTS,
        usecols=[
            "galaxy",
            "radius_kpc",
            "v_baryon_050_squared_km2_s2",
            "construction_used_vobs_or_residual",
        ],
    )
    fast["galaxy"] = fast["galaxy"].astype(str)

    scenario_rows = []
    manifest_rows = []
    prediction_rows = []
    for scenario in SCENARIOS:
        route = scenario["selected_spin_normalization_route"]
        values = source_values_for_route(route)
        joined = (
            values.merge(
                priority[["galaxy", "nfw_preference_load"]],
                on="galaxy",
                how="inner",
            )
            .merge(source_loads, on="galaxy", how="left")
            .sort_values("galaxy")
            .reset_index(drop=True)
        )
        joined["edgeon_load"] = joined["edgeon_load"].fillna(0.0)
        joined["beta_cl_value"] = (
            1.0
            + (joined["lambda_spin_value"] / 0.10) * joined["nfw_preference_load"]
            + joined["edgeon_load"]
        )
        joined["dry_run_scenario_id"] = scenario["dry_run_scenario_id"]
        joined["selected_spin_normalization_route"] = route
        joined["carrier_id"] = "BARYONIC_050_FAST_PACKET"
        joined["formula_id"] = "BETA_CL_TRANSFER_SOURCE_FROZEN_DRY_RUN"
        joined["source_value_column"] = scenario["source_value_column"]
        joined["source_artifact"] = scenario["source_artifact"]
        joined["construction_used_vobs"] = False
        joined["scoring_used_vobs"] = False
        joined["endpoint_scores_allowed"] = False
        joined["endpoint_validation_claim"] = False
        joined["claim_boundary"] = CLAIM_BOUNDARY
        manifest_rows.append(joined)

        available_galaxies = set(fast["galaxy"])
        missing_galaxies = sorted(set(joined["galaxy"]) - available_galaxies)
        covered = joined.loc[joined["galaxy"].isin(available_galaxies)].copy()
        n_prediction_points = 0
        for _, formula in covered.iterrows():
            points = (
                fast.loc[fast["galaxy"].eq(str(formula["galaxy"]))]
                .copy()
                .sort_values("radius_kpc")
            )
            carrier_v2 = points["v_baryon_050_squared_km2_s2"].to_numpy(dtype=float)
            carrier = np.sqrt(np.maximum(carrier_v2, 0.0))
            predicted = np.sqrt(np.maximum(float(formula["beta_cl_value"]) * carrier_v2, 0.0))
            n_prediction_points += len(points)
            for point, carrier_value, predicted_value in zip(
                points.to_dict("records"),
                carrier,
                predicted,
            ):
                prediction_rows.append(
                    {
                        "dry_run_scenario_id": scenario["dry_run_scenario_id"],
                        "galaxy": formula["galaxy"],
                        "radius_kpc": point["radius_kpc"],
                        "carrier_id": formula["carrier_id"],
                        "formula_id": formula["formula_id"],
                        "selected_spin_normalization_route": route,
                        "lambda_spin_value": formula["lambda_spin_value"],
                        "nfw_preference_load": formula["nfw_preference_load"],
                        "edgeon_load": formula["edgeon_load"],
                        "beta_cl_value": formula["beta_cl_value"],
                        "v_carrier_kms": carrier_value,
                        "v_beta_cl_transfer_kms": predicted_value,
                        "construction_used_vobs": False,
                        "scoring_used_vobs": False,
                        "endpoint_scores_allowed": False,
                        "endpoint_validation_claim": False,
                        "claim_boundary": CLAIM_BOUNDARY,
                    }
                )

        scenario_rows.append(
            {
                "dry_run_scenario_id": scenario["dry_run_scenario_id"],
                "selected_spin_normalization_route": route,
                "selected_carrier_id": "BARYONIC_050_FAST_PACKET",
                "n_formula_rows_if_accepted": len(joined),
                "n_fast_sparc_covered_galaxies": len(covered),
                "n_missing_fast_sparc_galaxies": len(missing_galaxies),
                "missing_fast_sparc_galaxies": ";".join(missing_galaxies),
                "n_prediction_rows_without_vobs": n_prediction_points,
                "min_beta_cl_value": float(joined["beta_cl_value"].min()) if not joined.empty else np.nan,
                "max_beta_cl_value": float(joined["beta_cl_value"].max()) if not joined.empty else np.nan,
                "mean_beta_cl_value": float(joined["beta_cl_value"].mean()) if not joined.empty else np.nan,
                "contract_ready_if_reviews_accept": len(missing_galaxies) == 0 and not joined.empty,
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    scenario_summary = pd.DataFrame(scenario_rows)
    manifest = pd.concat(manifest_rows, ignore_index=True) if manifest_rows else pd.DataFrame()
    predictions = pd.DataFrame(prediction_rows, columns=PREDICTION_COLUMNS)
    summary = pd.DataFrame(
        [
            {
                "dry_run_status": (
                    "U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_READY_REVIEWS_PENDING"
                    if scenario_summary["contract_ready_if_reviews_accept"].all()
                    else "U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_HAS_COVERAGE_BLOCKERS"
                ),
                "n_scenarios": len(scenario_summary),
                "n_contract_ready_scenarios": int(
                    scenario_summary["contract_ready_if_reviews_accept"].sum()
                ),
                "n_dry_run_manifest_rows": len(manifest),
                "n_prediction_rows_without_vobs": len(predictions),
                "construction_used_vobs": False,
                "scoring_used_vobs": False,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": "obtain_independent_spin_and_carrier_review_responses",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv",
        index=False,
    )
    scenario_summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_scenarios.csv",
        index=False,
    )
    manifest.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_manifest.csv",
        index=False,
    )
    predictions.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_contract_dry_run_predictions.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Transfer Scoring Contract Dry Run",
        "",
        "This artifact moves toward scoring without scoring. It checks whether",
        "the already implemented spin-route and carrier combinations would have",
        "the non-observed inputs needed by the separate scoring runner if later",
        "accepted by independent review.",
        "",
        "It reads source/proxy fields, priority loads, and baryonic carrier",
        "columns only. It does not read observed rotation velocities or",
        "residuals.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Scenario Summary",
        "",
        markdown_table(scenario_summary),
        "",
        "## Dry-Run Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Claim Boundary",
        "",
        "This is not an endpoint score, not a replay, and not reviewer acceptance.",
        "It is a pre-scoring contract check showing that the scoring runner can",
        "execute after the independent review and freeze gates pass.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_scoring_contract_dry_run.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
