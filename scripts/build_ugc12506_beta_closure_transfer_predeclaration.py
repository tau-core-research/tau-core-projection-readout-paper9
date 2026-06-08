#!/usr/bin/env python3
"""Predeclare transfer candidates for the UGC12506 beta-closure rule.

The UGC12506 beta-closure candidate uses source-native quantities that are not
available in the SPARC master table for every galaxy: spin and NFW-vs-ISO
closure preference.  This gate therefore does not score anything.  It uses only
residual-blind SPARC source proxies to identify high-priority galaxies for
source acquisition, then records which source-native fields must be obtained
before the beta rule can be replayed independently.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_predeclaration_not_endpoint"


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


def safe_div(num: pd.Series, den: pd.Series) -> pd.Series:
    den = den.replace(0, np.nan)
    return num / den


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    master = pd.read_csv(DATA / "external_sparc_master_table.csv")
    df = master.copy()
    df["galaxy"] = df["Galaxy"].astype(str)
    df["inclination_deg"] = pd.to_numeric(df["Inc_deg"], errors="coerce")
    df["rhi_over_rdisk"] = safe_div(
        pd.to_numeric(df["RHI_kpc"], errors="coerce"),
        pd.to_numeric(df["Rdisk_kpc"], errors="coerce"),
    )
    df["mhi_1e9_msun"] = pd.to_numeric(df["MHI_1e9Msun"], errors="coerce")
    df["vflat_km_s"] = pd.to_numeric(df["Vflat_kms"], errors="coerce")
    df["quality_q"] = pd.to_numeric(df["Q"], errors="coerce")
    df["lum36_1e9_lsun"] = pd.to_numeric(df["L36_1e9Lsun"], errors="coerce")
    df["gas_to_l36"] = safe_div(df["mhi_1e9_msun"], df["lum36_1e9_lsun"])

    df["edgeon_score"] = np.clip((df["inclination_deg"] - 75.0) / 15.0, 0.0, 1.0)
    df["extent_score"] = np.clip((df["rhi_over_rdisk"] - 4.0) / 4.0, 0.0, 1.0)
    df["massive_score"] = np.clip((df["vflat_km_s"] - 160.0) / 120.0, 0.0, 1.0)
    df["gas_score"] = np.clip(np.log1p(df["mhi_1e9_msun"]) / np.log1p(35.0), 0.0, 1.0)
    df["quality_score"] = np.where(df["quality_q"].le(2), 1.0, 0.5)
    df["transfer_priority_score"] = (
        0.30 * df["edgeon_score"]
        + 0.25 * df["extent_score"]
        + 0.20 * df["massive_score"]
        + 0.15 * df["gas_score"]
        + 0.10 * df["quality_score"]
    )
    df["candidate_reason"] = (
        "high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer"
    )
    df["missing_source_native_fields"] = (
        "lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;"
        "PV/envelope method notes"
    )
    df["beta_cl_replay_status"] = "SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY"
    df["endpoint_scores_allowed"] = False
    df["uses_vobs_or_residual_for_selection"] = False
    df["claim_boundary"] = CLAIM_BOUNDARY

    criteria = (
        df["galaxy"].ne("UGC12506")
        & df["inclination_deg"].ge(75.0)
        & df["rhi_over_rdisk"].ge(4.0)
        & df["vflat_km_s"].ge(160.0)
        & df["mhi_1e9_msun"].ge(2.0)
        & df["quality_q"].le(2)
    )
    candidates = (
        df.loc[criteria]
        .sort_values("transfer_priority_score", ascending=False)
        .head(20)
        .reset_index(drop=True)
    )
    candidates["predeclared_rank"] = np.arange(1, len(candidates) + 1)
    candidates = candidates[
        [
            "predeclared_rank",
            "galaxy",
            "transfer_priority_score",
            "inclination_deg",
            "rhi_over_rdisk",
            "mhi_1e9_msun",
            "vflat_km_s",
            "quality_q",
            "gas_to_l36",
            "candidate_reason",
            "missing_source_native_fields",
            "beta_cl_replay_status",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual_for_selection",
            "claim_boundary",
        ]
    ]

    worklist_rows = []
    for _, row in candidates.iterrows():
        for field, source_hint in [
            ("lambda_spin", "literature halo/spin or HIghMass-like dynamical modelling"),
            ("chi2_NFW", "source-native dark-matter halo fit table"),
            ("chi2_ISO", "same source-native halo fit table as chi2_NFW"),
            ("PV/envelope notes", "HI velocity-field or PV/envelope-tracing source"),
            ("independent replay freeze", "freeze beta_cl before endpoint scoring"),
        ]:
            worklist_rows.append(
                {
                    "galaxy": row["galaxy"],
                    "predeclared_rank": int(row["predeclared_rank"]),
                    "required_field": field,
                    "source_hint": source_hint,
                    "field_status": "MISSING_SOURCE_NATIVE_REVIEW_REQUIRED",
                    "uses_vobs_or_residual": False,
                    "endpoint_scores_allowed": False,
                    "claim_boundary": CLAIM_BOUNDARY,
                }
            )
    worklist = pd.DataFrame(worklist_rows)

    summary = pd.DataFrame(
        [
            {
                "transfer_predeclaration_status": (
                    "UGC12506_BETA_CLOSURE_TRANSFER_CANDIDATES_PREDECLARED_SOURCE_ACQUISITION_REQUIRED"
                ),
                "n_candidates": int(len(candidates)),
                "n_endpoint_scores_allowed": 0,
                "n_replay_scores_allowed_now": 0,
                "selection_inputs": (
                    "SPARC inclination, RHI/Rdisk, MHI, Vflat, quality flag; no rotation residuals"
                ),
                "top_candidates": ";".join(candidates["galaxy"].head(8).astype(str)),
                "next_gate": "acquire_source_native_spin_and_halo_fit_fields_for_top_candidates",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    candidates.to_csv(DATA / "ugc12506_beta_closure_transfer_candidates.csv", index=False)
    worklist.to_csv(DATA / "ugc12506_beta_closure_transfer_source_worklist.csv", index=False)
    summary.to_csv(DATA / "ugc12506_beta_closure_transfer_predeclaration_summary.csv", index=False)

    report = [
        "# UGC12506 Beta-Closure Transfer Predeclaration",
        "",
        "This gate predeclares independent transfer candidates for the UGC12506",
        "source-derived beta-closure rule. It does not score any endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Candidates",
        "",
        markdown_table(candidates),
        "",
        "## Source Worklist",
        "",
        markdown_table(worklist.head(40)),
        "",
        "## Claim Boundary",
        "",
        "Selection uses only residual-blind SPARC source proxies. Candidate rows",
        "must acquire source-native spin and NFW/ISO closure-preference fields",
        "before any beta_cl replay can be promoted beyond source acquisition.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_predeclaration.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )
    print(summary.to_string(index=False))
    print(candidates.to_string(index=False))


if __name__ == "__main__":
    main()
