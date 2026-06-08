#!/usr/bin/env python3
"""Build the multichannel time-projection endpoint preflight gate.

This script turns the fundamental multichannel time-projection shell into an
endpoint-readiness ledger.  It separates the source-intrinsic morphology time
channel, the observer/projection time channel, and the optional path channel.
No rotation residuals are used and no endpoint scoring is authorized here.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "time_projection_endpoint_preflight_gate_not_endpoint"


def read_csv(name: str) -> pd.DataFrame:
    path = DATA / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


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


def bool_from_value(value: object) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "pass_caveated"}


def build_source_channel(readiness: pd.DataFrame, intake: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in readiness.iterrows():
        galaxy = row["galaxy"]
        intake_row = intake[intake["galaxy"].eq(galaxy)]
        source_level = ""
        blocked = row["required_observables_for_accepted_xi_t"]
        source_basis = row["source_status"]
        if not intake_row.empty:
            source_level = str(intake_row.iloc[0]["source_support_level"])
            blocked = str(intake_row.iloc[0]["blocked_fields"])
            source_basis = str(intake_row.iloc[0]["filled_source_evidence"])

        if galaxy == "UGC12506":
            status = "CAVEATED_INTERVAL_SOURCE_CHANNEL_READY_CONTROL_ONLY"
            frozen = True
            reason = (
                "high-spin/envelope source channel exists as a caveated interval "
                "control, but not as an accepted endpoint manifest"
            )
        elif galaxy == "NGC4088" and "SOURCE_REVIEWED_QMEM" in source_level:
            status = "SOURCE_CHANNEL_QMEM_REVIEWED_NORMALIZATION_BLOCKED"
            frozen = False
            reason = (
                "q_warp and m_history are accepted for protocol numeric bounds, "
                "but the residual-blind B_i / epsilon_t normalization rule remains open"
            )
        elif galaxy == "NGC4088":
            status = "SOURCE_CHANNEL_BLOCKED_MEASUREMENT_REVIEW_REQUIRED"
            frozen = False
            reason = "qualitative warp/asymmetry context exists, but q_warp, history load, and independent review remain open"
        elif str(row["xi_trial_status"]).startswith("P3"):
            status = "SOURCE_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE"
            frozen = False
            reason = "current Xi_t proxy worsens or double-counts an already saturated morphology/projection kernel"
        elif str(row["xi_trial_status"]).startswith("P2"):
            status = "SOURCE_CHANNEL_WEAK_NULL_CONTROL"
            frozen = False
            reason = "weak/null control; no strong source reason to activate time projection"
        else:
            status = "SOURCE_CHANNEL_NOT_READY"
            frozen = False
            reason = "no accepted source-time manifest"

        rows.append(
            {
                "galaxy": galaxy,
                "xi_morph_channel_status": status,
                "xi_morph_source_basis": source_basis,
                "source_support_level": source_level or row["source_status"],
                "blocked_or_caveated_fields": blocked,
                "xi_morph_frozen_before_scoring": frozen,
                "endpoint_scores_allowed": False,
                "reason": reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_observer_channel(readiness: pd.DataFrame, intake: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in readiness.iterrows():
        galaxy = row["galaxy"]
        intake_row = intake[intake["galaxy"].eq(galaxy)]
        path_status = "UNKNOWN"
        if not intake_row.empty:
            path_status = str(intake_row.iloc[0]["path_term_status"])

        if galaxy == "UGC12506":
            status = "OBSERVER_CHANNEL_CAVEATED_EDGEON_PV_CONTROL_READY"
            frozen = True
            basis = "edge-on high inclination; PV/envelope visibility; path term rejected/zero in current review"
            reason = "observer/PV slice can be carried as caveated control, but not endpoint validation"
        elif galaxy == "NGC4088":
            status = "OBSERVER_CHANNEL_SECONDARY_BLOCKED"
            frozen = False
            basis = "warp/asymmetry visibility context; not the primary blocker"
            reason = "clock phase must first be separated from additive warp-history morphology"
        elif str(row["xi_trial_status"]).startswith("P3"):
            status = "OBSERVER_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE"
            frozen = False
            basis = row["source_status"]
            reason = "ordinary projection is already represented by the base kernel or lacks independent clock evidence"
        else:
            status = "OBSERVER_CHANNEL_WEAK_NULL_CONTROL"
            frozen = False
            basis = row["source_status"]
            reason = "no strong source-reviewed observer-clock activation"

        rows.append(
            {
                "galaxy": galaxy,
                "xi_obs_channel_status": status,
                "xi_obs_source_basis": basis,
                "xi_path_status": path_status,
                "xi_obs_frozen_before_scoring": frozen,
                "endpoint_scores_allowed": False,
                "reason": reason,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    return pd.DataFrame(rows)


def build_preflight(source: pd.DataFrame, observer: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ngc4088_xieff = read_csv("ngc4088_time_projection_xi_eff_manifest_summary.csv")
    ngc4088_double_count = read_csv(
        "ngc4088_time_projection_double_count_resolution_summary.csv"
    )
    merged = source.merge(observer, on=["galaxy", "endpoint_scores_allowed", "claim_boundary"])
    rows = []
    for _, row in merged.iterrows():
        morph_frozen = bool_from_value(row["xi_morph_frozen_before_scoring"])
        obs_frozen = bool_from_value(row["xi_obs_frozen_before_scoring"])
        path_ok = str(row["xi_path_status"]) in {"NOT_ESTABLISHED", "NOT_PRIMARY_FOR_THIS_ROUTE", "UNKNOWN"}
        if row["galaxy"] == "UGC12506" and morph_frozen and obs_frozen and path_ok:
            status = "CONTROL_REPLAY_ALLOWED_ENDPOINT_BLOCKED"
            next_gate = "derive accepted source-only Xi_eff normalization or keep caveated interval as control-only"
            endpoint_allowed = False
            control_allowed = True
        elif (
            row["galaxy"] == "NGC4088"
            and not ngc4088_double_count.empty
            and str(ngc4088_double_count.iloc[0].get("double_count_resolution_status", ""))
            == "NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE"
        ):
            status = "DOUBLE_COUNT_RESOLVED_COMBINED_XI_ONE_TIME_ENDPOINT_INACTIVE"
            next_gate = (
                "score additive-only accepted route if endpoint scoring is requested; "
                "reopen time endpoint only with independent non-overlap clock evidence"
            )
            endpoint_allowed = False
            control_allowed = True
        elif (
            row["galaxy"] == "NGC4088"
            and not ngc4088_xieff.empty
            and bool(ngc4088_xieff.iloc[0].get("control_manifest_allowed", False))
        ):
            status = "XIEFF_CONTROL_READY_DOUBLECOUNT_BLOCKED"
            next_gate = "resolve additive-warp/history versus Xi_eff clock double-count separation before endpoint scoring"
            endpoint_allowed = False
            control_allowed = True
        elif (
            row["galaxy"] == "NGC4088"
            and "QMEM_REVIEWED_NORMALIZATION_BLOCKED" in str(row["xi_morph_channel_status"])
        ):
            status = "SOURCE_QMEM_REVIEWED_NORMALIZATION_BLOCKED"
            next_gate = "freeze residual-blind B_i / epsilon_t normalization rule before any time endpoint"
            endpoint_allowed = False
            control_allowed = False
        elif row["galaxy"] == "NGC4088":
            status = "MEASUREMENT_REVIEW_BLOCKED"
            next_gate = "fill q_warp/m_history and independent review before any time endpoint"
            endpoint_allowed = False
            control_allowed = False
        elif "REJECT_CURRENT_PROXY" in str(row["xi_morph_channel_status"]):
            status = "CURRENT_PROXY_REJECTED_KEEP_XI_ONE"
            next_gate = "do not score time endpoint unless independent clock evidence appears"
            endpoint_allowed = False
            control_allowed = False
        else:
            status = "NOT_ENDPOINT_READY"
            next_gate = "retain as weak/null or source-review case"
            endpoint_allowed = False
            control_allowed = False

        rows.append(
            {
                "galaxy": row["galaxy"],
                "time_projection_preflight_status": status,
                "xi_eff_formula": "Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R)",
                "xi_path_policy": row["xi_path_status"],
                "control_replay_allowed": control_allowed,
                "endpoint_scores_allowed": endpoint_allowed,
                "next_gate": next_gate,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    preflight = pd.DataFrame(rows)
    summary = pd.DataFrame(
        [
            {
                "preflight_status": "TIME_PROJECTION_ENDPOINT_PREFLIGHT_BUILT_NO_ENDPOINTS_ALLOWED",
                "n_galaxies": int(len(preflight)),
                "n_control_replay_allowed": int(preflight["control_replay_allowed"].sum()),
                "n_endpoint_scores_allowed": int(preflight["endpoint_scores_allowed"].sum()),
                "strongest_current_route": (
                    "UGC12506 caveated interval/control replay; "
                    "NGC4088 additive warp-history route with Xi_eff=1 in the combined endpoint"
                ),
                "main_blocker": (
                    "no source-complete accepted time endpoint with clock evidence orthogonal "
                    "to the active morphology kernel"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    return preflight, summary


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    readiness = read_csv("time_readout_xi_manifest_readiness.csv")
    intake = read_csv("time_readout_xi_p1_source_review_intake.csv")
    if readiness.empty:
        raise SystemExit("missing data/derived/time_readout_xi_manifest_readiness.csv")

    source = build_source_channel(readiness, intake)
    observer = build_observer_channel(readiness, intake)
    preflight, summary = build_preflight(source, observer)

    source.to_csv(DATA / "time_projection_source_morphology_time_manifest.csv", index=False)
    observer.to_csv(DATA / "time_projection_observer_projection_time_manifest.csv", index=False)
    preflight.to_csv(DATA / "time_projection_endpoint_preflight_gate.csv", index=False)
    summary.to_csv(DATA / "time_projection_endpoint_preflight_summary.csv", index=False)

    report = "\n".join(
        [
            "# Time Projection Endpoint Preflight Gate",
            "",
            "This artifact moves the multichannel time-projection shell toward an",
            "endpoint calculation without allowing endpoint scoring. It separates",
            "`Xi_morph`, `Xi_obs`, and `Xi_path` so that a future endpoint cannot",
            "hide missing morphology-time or observer-time evidence inside one fitted",
            "`Xi_t` factor.",
            "",
            "## Source-Morphology Time Manifest",
            "",
            markdown_table(source),
            "",
            "## Observer / Projection Time Manifest",
            "",
            markdown_table(observer),
            "",
            "## Endpoint Preflight",
            "",
            markdown_table(preflight),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Interpretation",
            "",
            "The current executable time-projection routes remain control routes, not",
            "accepted time endpoints.  UGC12506 has a caveated interval/control replay.",
            "For NGC4088, the source-space double-count audit resolves the combined",
            "endpoint by assigning the overlapping clock evidence to the already active",
            "additive warp-history route; the combined endpoint therefore uses",
            "`Xi_eff=1`, while the clock-only route is preserved as a control.",
            "A real time-projection endpoint requires source-complete clock evidence",
            "orthogonal to the active morphology kernel, with `Xi_morph`, `Xi_obs`,",
            "and `Xi_path` independently frozen before the scoring script reads the",
            "rotation curve.",
            "",
        ]
    )
    (REPORTS / "time_projection_endpoint_preflight_gate.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
