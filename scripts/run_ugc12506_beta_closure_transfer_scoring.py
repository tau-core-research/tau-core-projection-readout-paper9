#!/usr/bin/env python3
"""Run or block UGC12506 beta-closure transfer scoring.

This is the separate scoring runner for the beta_cl transfer route.  It is
allowed to read rotation-curve observations only after a non-scoring launch
gate has passed and a frozen transfer formula manifest exists with non-empty
rows.  In the current state the launch gate is blocked, so this script writes
a blocked scoring artifact and does not read any rotation-curve table.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_scoring_runner_not_endpoint"


LAUNCH_SUMMARY = DATA / "ugc12506_beta_closure_scoring_launch_summary.csv"
FORMULA_MANIFEST = DATA / "ugc12506_beta_closure_transfer_formula_manifest.csv"
FAST_SPARC_POINTS = DATA / "fast_sparc_rotation_curve_packet_points.csv"

SCORE_COLUMNS = [
    "galaxy",
    "model_id",
    "route_id",
    "selected_spin_normalization_route",
    "n_points",
    "rmse_km_s",
    "weighted_rmse_km_s",
    "mae_km_s",
    "construction_used_vobs",
    "scoring_used_vobs",
    "endpoint_validation_claim",
    "claim_boundary",
]

POINT_COLUMNS = [
    "galaxy",
    "radius_kpc",
    "vobs_kms",
    "errv_kms",
    "carrier_id",
    "formula_id",
    "selected_spin_normalization_route",
    "beta_cl_value",
    "v_carrier_kms",
    "v_beta_cl_transfer_kms",
    "construction_used_vobs",
    "scoring_used_vobs",
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


def bool_value(value: object) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return bool(value)


def rmse(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(pred - obs))))


def mae(obs: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(pred - obs)))


def wrmse(obs: np.ndarray, pred: np.ndarray, err: np.ndarray) -> float:
    weights = 1.0 / np.square(np.maximum(err, 1.0e-6))
    return float(np.sqrt(np.sum(weights * np.square(pred - obs)) / np.sum(weights)))


def score_row(
    galaxy: str,
    model_id: str,
    route_id: str,
    selected_route: str,
    obs: np.ndarray,
    pred: np.ndarray,
    err: np.ndarray,
) -> dict[str, object]:
    return {
        "galaxy": galaxy,
        "model_id": model_id,
        "route_id": route_id,
        "selected_spin_normalization_route": selected_route,
        "n_points": int(len(obs)),
        "rmse_km_s": rmse(obs, pred),
        "weighted_rmse_km_s": wrmse(obs, pred, err),
        "mae_km_s": mae(obs, pred),
        "construction_used_vobs": False,
        "scoring_used_vobs": True,
        "endpoint_validation_claim": False,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    if not LAUNCH_SUMMARY.exists():
        launch_allowed = False
        launch_status = "MISSING_LAUNCH_SUMMARY"
        selected_route = "UNKNOWN"
    else:
        launch = pd.read_csv(LAUNCH_SUMMARY).iloc[0]
        launch_allowed = bool_value(launch["beta_cl_transfer_scoring_allowed"])
        launch_status = str(launch["scoring_launch_status"])
        selected_route = str(launch["selected_spin_normalization_route"])

    formula_manifest_exists = FORMULA_MANIFEST.exists()
    formula_manifest_rows = 0
    if formula_manifest_exists:
        formula_manifest_rows = len(pd.read_csv(FORMULA_MANIFEST))

    scores = pd.DataFrame(columns=SCORE_COLUMNS)
    scoring_points = pd.DataFrame(columns=POINT_COLUMNS)

    if not launch_allowed:
        scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_LAUNCH_GATE"
        blocked_reason = launch_status
        scores_written = False
        scoring_used_vobs = False
    elif not formula_manifest_exists or formula_manifest_rows == 0:
        scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_FORMULA_MANIFEST"
        blocked_reason = "frozen transfer formula manifest missing or empty"
        scores_written = False
        scoring_used_vobs = False
    else:
        manifest = pd.read_csv(FORMULA_MANIFEST)
        carrier_ids = set(manifest["carrier_id"].dropna().astype(str))
        supported_carrier = carrier_ids == {"BARYONIC_050_FAST_PACKET"}
        if not supported_carrier:
            scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_UNSUPPORTED_CARRIER"
            blocked_reason = f"supported carrier set is {{BARYONIC_050_FAST_PACKET}}; got {sorted(carrier_ids)}"
            scores_written = False
            scoring_used_vobs = False
        elif not FAST_SPARC_POINTS.exists():
            scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_MISSING_FAST_SPARC_PACKET"
            blocked_reason = "fast SPARC rotation-curve packet is missing"
            scores_written = False
            scoring_used_vobs = False
        else:
            fast_points = pd.read_csv(FAST_SPARC_POINTS)
            manifest = manifest.copy()
            manifest["galaxy"] = manifest["galaxy"].astype(str)
            point_rows = []
            score_rows = []
            missing_galaxies = []
            for _, formula in manifest.iterrows():
                galaxy = str(formula["galaxy"])
                points = (
                    fast_points.loc[fast_points["galaxy"].astype(str).eq(galaxy)]
                    .copy()
                    .sort_values("radius_kpc")
                )
                if points.empty:
                    missing_galaxies.append(galaxy)
                    continue
                beta_cl = float(formula["beta_cl_value"])
                carrier_v2 = points["v_baryon_050_squared_km2_s2"].to_numpy(dtype=float)
                beta_v2 = np.maximum(beta_cl * carrier_v2, 0.0)
                carrier = np.sqrt(np.maximum(carrier_v2, 0.0))
                predicted = np.sqrt(beta_v2)
                obs = points["vobs_kms"].to_numpy(dtype=float)
                err = points["errv_kms"].to_numpy(dtype=float)
                route_id = str(formula["formula_id"])
                selected_formula_route = str(formula["selected_spin_normalization_route"])

                score_rows.append(
                    score_row(
                        galaxy,
                        "BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE",
                        "carrier_reference",
                        selected_formula_route,
                        obs,
                        carrier,
                        err,
                    )
                )
                score_rows.append(
                    score_row(
                        galaxy,
                        "BETA_CL_TRANSFER_SOURCE_FROZEN",
                        route_id,
                        selected_formula_route,
                        obs,
                        predicted,
                        err,
                    )
                )
                for point, carrier_value, predicted_value in zip(
                    points.to_dict("records"),
                    carrier,
                    predicted,
                ):
                    point_rows.append(
                        {
                            "galaxy": galaxy,
                            "radius_kpc": point["radius_kpc"],
                            "vobs_kms": point["vobs_kms"],
                            "errv_kms": point["errv_kms"],
                            "carrier_id": formula["carrier_id"],
                            "formula_id": formula["formula_id"],
                            "selected_spin_normalization_route": selected_formula_route,
                            "beta_cl_value": beta_cl,
                            "v_carrier_kms": carrier_value,
                            "v_beta_cl_transfer_kms": predicted_value,
                            "construction_used_vobs": False,
                            "scoring_used_vobs": True,
                            "endpoint_validation_claim": False,
                            "claim_boundary": CLAIM_BOUNDARY,
                        }
                    )

            if missing_galaxies:
                scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_BLOCKED_MISSING_GALAXY_POINTS"
                blocked_reason = f"missing fast SPARC rows for {sorted(missing_galaxies)}"
                scores_written = False
                scoring_used_vobs = False
                score_rows = []
                point_rows = []
            else:
                scoring_status = "U12506_BETA_CLOSURE_TRANSFER_SCORING_COMPLETE_CONTROL_ONLY"
                blocked_reason = "not blocked; separate scoring runner consumed frozen manifest"
                scores_written = True
                scoring_used_vobs = True
                scores = pd.DataFrame(score_rows, columns=SCORE_COLUMNS).sort_values(
                    ["galaxy", "rmse_km_s", "model_id"]
                )
                scoring_points = pd.DataFrame(point_rows, columns=POINT_COLUMNS)

    summary = pd.DataFrame(
        [
            {
                "transfer_scoring_status": scoring_status,
                "selected_spin_normalization_route": selected_route,
                "launch_status": launch_status,
                "launch_allowed": launch_allowed,
                "formula_manifest_exists": formula_manifest_exists,
                "formula_manifest_rows": formula_manifest_rows,
                "blocked_reason": blocked_reason,
                "scores_written": scores_written,
                "scoring_used_vobs": scoring_used_vobs,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "obtain_review_response_then_prefreeze_spin_route_values"
                    if not launch_allowed
                    else "build_frozen_beta_cl_transfer_formula_manifest"
                    if not formula_manifest_exists or formula_manifest_rows == 0
                    else "review_control_only_scores_before_endpoint_claim"
                    if scores_written
                    else "resolve_scoring_blocker"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "BETA_TRANSFER_SCORE_1_LAUNCH_ALLOWED",
                "gate_status": "PASS" if launch_allowed else "BLOCKED",
                "reason": launch_status,
                "allowed_to_read_vobs": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_TRANSFER_SCORE_2_FORMULA_MANIFEST_PRESENT",
                "gate_status": "PASS"
                if formula_manifest_exists and formula_manifest_rows > 0
                else "BLOCKED",
                "reason": f"formula_manifest_exists={formula_manifest_exists}; rows={formula_manifest_rows}",
                "allowed_to_read_vobs": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "gate_id": "BETA_TRANSFER_SCORE_3_VOBS_READ_PERMISSION",
                "gate_status": "PASS"
                if launch_allowed and formula_manifest_exists and formula_manifest_rows > 0
                else "BLOCKED",
                "reason": "vobs may be read only by this scoring runner after launch and formula freeze pass",
                "allowed_to_read_vobs": bool(
                    launch_allowed and formula_manifest_exists and formula_manifest_rows > 0
                ),
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    summary.to_csv(DATA / "ugc12506_beta_closure_transfer_scoring_summary.csv", index=False)
    gates.to_csv(DATA / "ugc12506_beta_closure_transfer_scoring_gates.csv", index=False)
    scores.to_csv(DATA / "ugc12506_beta_closure_transfer_scoring_scores.csv", index=False)
    scoring_points.to_csv(
        DATA / "ugc12506_beta_closure_transfer_scoring_points.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Transfer Scoring Runner",
        "",
        "This is the separate scoring runner. In the current state it blocks before",
        "reading any rotation-curve observation because the launch gate has not",
        "passed and the frozen transfer formula manifest is missing or empty.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Scores",
        "",
        markdown_table(scores) if not scores.empty else "No scores were written in the current blocked state.",
        "",
        "## Scoring Points",
        "",
        (
            f"Wrote {len(scoring_points)} scored point rows to "
            "`data/derived/ugc12506_beta_closure_transfer_scoring_points.csv`."
            if not scoring_points.empty
            else "No point-level scoring rows were written."
        ),
        "",
        "## Claim Boundary",
        "",
        "This artifact is either a scoring-path guard or, after all launch gates",
        "pass, a control-only scoring artifact. It preserves the rule that",
        "observed rotation curves may only be read by this separate scoring",
        "script after all residual-blind freeze gates pass.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_scoring.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
