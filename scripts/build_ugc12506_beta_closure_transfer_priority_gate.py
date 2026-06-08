#!/usr/bin/env python3
"""Build the beta-closure transfer priority gate after halo-field acquisition.

The predeclaration selected high-inclination, extended-HI, massive-gas systems
without using residuals.  After the Li et al. (2020) halo-fit fields are
available, this gate narrows the source-acquisition queue to systems with a
positive NFW-preference load.  It still does not score endpoints and does not
infer missing spin or PV/envelope evidence.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "ugc12506_beta_closure_transfer_priority_gate_not_endpoint"


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


def priority_class(load: float) -> str:
    if load >= 0.10:
        return "PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET"
    if load > 0.0:
        return "WEAK_NFW_PREFERENCE_TRANSFER_TARGET"
    return "PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH"


def next_action(row: pd.Series) -> str:
    klass = row["transfer_priority_class"]
    if klass == "PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET":
        return "acquire_lambda_spin_and_pv_envelope_evidence_first"
    if klass == "WEAK_NFW_PREFERENCE_TRANSFER_TARGET":
        return "hold_as_secondary_transfer_or_control_until_spin_pv_available"
    return "do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    candidates = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_candidates.csv")
    halo = pd.read_csv(DATA / "ugc12506_beta_closure_transfer_halo_fit_fields.csv")
    merged = candidates.merge(
        halo[
            [
                "galaxy",
                "chi2_ISO",
                "chi2_NFW",
                "chi2_ISO_over_NFW",
                "nfw_preference_load",
                "halo_fit_field_status",
                "source",
            ]
        ],
        on="galaxy",
        how="left",
    )
    merged["transfer_priority_class"] = merged["nfw_preference_load"].map(priority_class)
    merged["next_source_gate"] = merged.apply(next_action, axis=1)
    merged["still_missing_fields"] = "lambda_spin;PV/envelope method notes;independent replay freeze"
    merged["endpoint_scores_allowed"] = False
    merged["uses_vobs_or_residual_for_priority"] = False
    merged["claim_boundary"] = CLAIM_BOUNDARY
    merged = merged.sort_values(
        ["nfw_preference_load", "transfer_priority_score"],
        ascending=[False, False],
    ).reset_index(drop=True)
    merged["post_halo_rank"] = range(1, len(merged) + 1)

    cols = [
        "post_halo_rank",
        "predeclared_rank",
        "galaxy",
        "transfer_priority_score",
        "chi2_ISO",
        "chi2_NFW",
        "chi2_ISO_over_NFW",
        "nfw_preference_load",
        "transfer_priority_class",
        "still_missing_fields",
        "next_source_gate",
        "endpoint_scores_allowed",
        "uses_vobs_or_residual_for_priority",
        "claim_boundary",
    ]
    priority = merged[cols]
    priority.to_csv(DATA / "ugc12506_beta_closure_transfer_priority_gate.csv", index=False)

    summary = pd.DataFrame(
        [
            {
                "priority_gate_status": (
                    "UGC12506_BETA_CLOSURE_TRANSFER_PRIORITY_GATE_BUILT_ENDPOINT_BLOCKED"
                ),
                "n_candidates": int(len(priority)),
                "n_primary_nfw_preference_targets": int(
                    priority["transfer_priority_class"]
                    .eq("PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET")
                    .sum()
                ),
                "n_weak_nfw_preference_targets": int(
                    priority["transfer_priority_class"]
                    .eq("WEAK_NFW_PREFERENCE_TRANSFER_TARGET")
                    .sum()
                ),
                "n_piso_preferred_controls": int(
                    priority["transfer_priority_class"]
                    .eq("PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH")
                    .sum()
                ),
                "primary_targets": ";".join(
                    priority.loc[
                        priority["transfer_priority_class"].eq(
                            "PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET"
                        ),
                        "galaxy",
                    ].astype(str)
                ),
                "n_endpoint_scores_allowed": 0,
                "next_gate": "source_freeze_lambda_spin_and_pv_for_primary_targets",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )
    summary.to_csv(
        DATA / "ugc12506_beta_closure_transfer_priority_gate_summary.csv",
        index=False,
    )

    report = [
        "# UGC12506 Beta-Closure Transfer Priority Gate",
        "",
        "This gate narrows the predeclared transfer queue after source-native",
        "pISO/NFW halo-fit fields have been acquired. It does not score endpoint",
        "curves and does not infer the still-missing spin or PV/envelope fields.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Priority Ledger",
        "",
        markdown_table(priority),
        "",
        "## Interpretation",
        "",
        "The UGC12506 beta-closure route is not licensed by edge-on geometry and",
        "large H I extent alone. A positive source-side NFW-preference load is",
        "also required. Rows with pISO-preferred halo fits are preserved as",
        "controls or alternative-branch candidates rather than forced through",
        "the UGC12506 beta_cl replay.",
    ]
    (REPORTS / "ugc12506_beta_closure_transfer_priority_gate.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(priority.to_string(index=False))


if __name__ == "__main__":
    main()
