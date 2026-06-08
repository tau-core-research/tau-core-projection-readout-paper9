#!/usr/bin/env python3
"""Build source-freeze preflight for the beta-closure primary targets.

This gate inspects the two primary NFW-preference transfer targets selected by
the post-halo priority gate (NGC0891 and NGC7331).  It records independent
PV/envelope evidence and the remaining spin blockers.  It does not compute a
beta value and does not score rotation curves.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint"


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

    priority = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_priority_gate.csv")
    primary = priority[
        priority["transfer_priority_class"].eq("PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET")
    ].copy()

    source_rows = [
        {
            "galaxy": "NGC0891",
            "field": "PV/envelope evidence",
            "field_status": "ACCEPTED_CONTEXT_NOT_NUMERIC_FREEZE",
            "source_value": (
                "edge-on H I XV/PV modelling and envelope-tracing route present; "
                "rotation curve derived from envelope tracing/XV fitting"
            ),
            "source_reference": (
                "Fraternali & Binney 2006 MNRAS 366, 449; "
                "Kregel & van der Kruit 2004 MNRAS 352, 787"
            ),
            "source_url": (
                "https://academic.oup.com/mnras/article/366/2/449/1214630 ; "
                "https://academic.oup.com/mnras/article/352/3/787/1211373"
            ),
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
        },
        {
            "galaxy": "NGC0891",
            "field": "lambda_spin",
            "field_status": "BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED",
            "source_value": "",
            "source_reference": "no accepted direct source-native spin value cached",
            "source_url": "",
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
        },
        {
            "galaxy": "NGC7331",
            "field": "PV/envelope evidence",
            "field_status": "ACCEPTED_CONTEXT_CACHED_THINGS_PRODUCTS",
            "source_value": (
                "THINGS H I rotation/velocity-field context and local MOM0/MOM1/MOM2 "
                "products are cached; inner points include PV-diagram lineage and outer "
                "differences depend on inclination choices"
            ),
            "source_reference": "de Blok et al. 2008 AJ/ApJ THINGS; local THINGS products; Patra 2018 MNRAS 478, 4931",
            "source_url": (
                "https://arxiv.org/abs/0810.2100 ; "
                "https://academic.oup.com/mnras/article/478/4/4931/5045978"
            ),
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
        },
        {
            "galaxy": "NGC7331",
            "field": "lambda_spin",
            "field_status": "BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED",
            "source_value": "",
            "source_reference": "no accepted direct source-native spin value cached",
            "source_url": "",
            "uses_vobs_or_residual": False,
            "endpoint_scores_allowed": False,
        },
    ]
    evidence = pd.DataFrame(source_rows)
    evidence["claim_boundary"] = CLAIM_BOUNDARY
    evidence.to_csv(
        DATA / "ugc12506_beta_closure_primary_source_freeze_evidence.csv",
        index=False,
    )

    rows = []
    for _, row in primary.iterrows():
        galaxy = row["galaxy"]
        ev = evidence[evidence["galaxy"].eq(galaxy)]
        pv_status = ev.loc[ev["field"].eq("PV/envelope evidence"), "field_status"].iloc[0]
        spin_status = ev.loc[ev["field"].eq("lambda_spin"), "field_status"].iloc[0]
        beta_replay_allowed = (
            pv_status.startswith("ACCEPTED") and spin_status.startswith("ACCEPTED")
        )
        rows.append(
            {
                "galaxy": galaxy,
                "post_halo_rank": int(row["post_halo_rank"]),
                "nfw_preference_load": float(row["nfw_preference_load"]),
                "pv_envelope_status": pv_status,
                "lambda_spin_status": spin_status,
                "beta_cl_replay_allowed": beta_replay_allowed,
                "endpoint_scores_allowed": False,
                "next_gate": (
                    "freeze_lambda_spin_or_construct_declared_spin_proxy_from_source_observables"
                    if not beta_replay_allowed
                    else "build_beta_cl_formula_freeze_manifest_before_scoring"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )
    preflight = pd.DataFrame(rows)
    preflight.to_csv(
        DATA / "ugc12506_beta_closure_primary_source_freeze_preflight.csv",
        index=False,
    )

    summary = pd.DataFrame(
        [
            {
                "primary_source_freeze_status": (
                    "UGC12506_BETA_CLOSURE_PRIMARY_SOURCE_FREEZE_PREFLIGHT_BUILT_SPIN_BLOCKED"
                ),
                "n_primary_targets": int(len(preflight)),
                "n_pv_envelope_context_accepted": int(
                    preflight["pv_envelope_status"].str.startswith("ACCEPTED").sum()
                ),
                "n_lambda_spin_frozen": int(
                    preflight["lambda_spin_status"].str.startswith("ACCEPTED").sum()
                ),
                "n_beta_cl_replay_allowed": int(preflight["beta_cl_replay_allowed"].sum()),
                "n_endpoint_scores_allowed": 0,
                "next_gate": "spin_freeze_or_source_declared_spin_proxy_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_primary_source_freeze_preflight_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Primary Source-Freeze Preflight",
        "",
        "This preflight inspects the two primary NFW-preference targets after the",
        "post-halo priority gate. It preserves the endpoint blocker: PV/envelope",
        "context is acceptable as source context, but no direct source-native spin",
        "value has been frozen for either galaxy.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Primary Targets",
        "",
        markdown_table(preflight),
        "",
        "## Evidence Ledger",
        "",
        markdown_table(evidence),
        "",
        "## Claim Boundary",
        "",
        "No beta_cl replay or endpoint scoring is allowed by this gate. The next",
        "allowed step is to freeze a direct spin value or predeclare a source-only",
        "spin proxy before inspecting any transfer endpoint residual.",
    ]
    (REPORTS / "ugc12506_beta_closure_primary_source_freeze_preflight.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(preflight.to_string(index=False))


if __name__ == "__main__":
    main()
