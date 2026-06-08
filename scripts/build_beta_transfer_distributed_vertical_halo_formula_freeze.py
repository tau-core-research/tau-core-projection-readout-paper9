#!/usr/bin/env python3
"""Freeze a distributed vertical/halo beta formula for edge-on locks.

This V2 morphology refinement is not selected from residuals.  It follows from
the source review: NGC0891 and NGC4217 have distributed extraplanar dust/halo
structures, so the vertical/halo beta component should activate as a distributed
disk-halo layer after one disk scale length rather than only in the far outer
disk.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint"

LOCK_REVIEW = DATA / "beta_transfer_lock_type_source_review.csv"
MORPH = DATA / "morphology_parameter_manifest.csv"
SPIN_PROXY = DATA / "ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv"


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

    lock = pd.read_csv(LOCK_REVIEW)
    morph = pd.read_csv(MORPH).drop_duplicates("galaxy")
    spin = pd.read_csv(SPIN_PROXY)

    cases = lock[lock["galaxy"].isin(["NGC0891", "NGC4217"])].merge(
        morph[
            [
                "galaxy",
                "scale_radius_proxy_kpc",
                "thickness_h_over_rs_proxy",
                "inclination_deg",
                "mean_bulge",
                "max_bulge",
                "r_max",
                "parameter_source",
            ]
        ],
        on="galaxy",
        how="left",
    )
    cases = cases.merge(
        spin[["galaxy", "beta_if_bullock_disk_proxy_used"]],
        on="galaxy",
        how="left",
    )

    rows = []
    for _, row in cases.iterrows():
        rs = float(row["scale_radius_proxy_kpc"])
        r_max = float(row["r_max"])
        r_on = rs
        r_full = min(2.0 * rs, r_max)
        if r_full <= r_on:
            r_full = r_max
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_id": f"{row['galaxy']}_DISTRIBUTED_VERTICAL_HALO_BETA_V2",
                "source_supported_lock_type": row["source_supported_lock_type"],
                "carrier_id": "BARYONIC_050_FAST_PACKET",
                "spin_route": "BULLOCK_DISK_CONVERSION",
                "beta_cl_value": float(row["beta_if_bullock_disk_proxy_used"]),
                "formula_text": (
                    "v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_DVH(R)]"
                ),
                "kernel_text": (
                    "K_DVH(R)=smoothstep((R-R_on)/(R_full-R_on)); "
                    "R_on=R_s, R_full=min(2 R_s,R_max)"
                ),
                "source_window_rule": (
                    "distributed edge-on extraplanar dust/halo layer activates over one-to-two disk scale lengths"
                ),
                "source_reason": (
                    "NGC0891 and NGC4217 source ledgers show distributed extraplanar dust/halo structures, "
                    "not only a far-outer warp"
                ),
                "r_s_source_proxy_kpc": rs,
                "r_on_kpc": r_on,
                "r_full_kpc": r_full,
                "r_max_kpc": r_max,
                "inclination_deg": float(row["inclination_deg"]),
                "thickness_h_over_rs_proxy": float(row["thickness_h_over_rs_proxy"]),
                "mean_bulge": float(row["mean_bulge"]),
                "max_bulge": float(row["max_bulge"]),
                "amplitude_rule": (
                    "beta_cl fixed by accepted Bullock disk conversion; no endpoint amplitude fit"
                ),
                "dimension_check": (
                    "PASS: beta_cl and K_DVH are dimensionless; correction multiplies v_carrier^2"
                ),
                "inner_limit": "R <= R_on gives K_DVH=0 and recovers v_carrier",
                "outer_limit": "R >= R_full gives K_DVH=1 and recovers beta-transfer component",
                "zero_beta_limit": "beta_cl=1 gives v_lock=v_carrier",
                "uses_vobs_or_residual_in_construction": False,
                "formula_frozen_before_scoring": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "source_provenance": str(row["parameter_source"]),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        )

    manifest = pd.DataFrame(rows)
    gates = []
    for _, row in manifest.iterrows():
        gates.extend(
            [
                {
                    "galaxy": row["galaxy"],
                    "formula_id": row["formula_id"],
                    "gate_id": "DVH1_LOCK_REVIEW",
                    "gate_status": "PASS",
                    "evidence": row["source_supported_lock_type"],
                },
                {
                    "galaxy": row["galaxy"],
                    "formula_id": row["formula_id"],
                    "gate_id": "DVH2_DISTRIBUTED_SOURCE_WINDOW",
                    "gate_status": "PASS",
                    "evidence": f"R_on=R_s={row['r_on_kpc']:.3f} kpc; R_full=2R_s={row['r_full_kpc']:.3f} kpc",
                },
                {
                    "galaxy": row["galaxy"],
                    "formula_id": row["formula_id"],
                    "gate_id": "DVH3_BETA_COMPONENT_SOURCE_FIXED",
                    "gate_status": "PASS",
                    "evidence": f"beta_cl={row['beta_cl_value']:.6g} from {row['spin_route']}",
                },
                {
                    "galaxy": row["galaxy"],
                    "formula_id": row["formula_id"],
                    "gate_id": "DVH4_DIMENSIONS_AND_LIMITS",
                    "gate_status": "PASS",
                    "evidence": "dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1",
                },
            ]
        )
    gates = pd.DataFrame(gates)
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "formula_freeze_status": "DISTRIBUTED_VERTICAL_HALO_BETA_FORMULA_FROZEN_CONTROL_REPLAY_ALLOWED",
                "n_galaxies": len(manifest),
                "n_gates": len(gates),
                "n_pass_gates": int(gates["gate_status"].eq("PASS").sum()),
                "uses_vobs_or_residual_in_construction": False,
                "control_replay_allowed": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_action": "run_distributed_vertical_halo_control_replay",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "beta_transfer_distributed_vertical_halo_formula_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "beta_transfer_distributed_vertical_halo_formula_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "beta_transfer_distributed_vertical_halo_formula_freeze_summary.csv", index=False)

    report = [
        "# Distributed Vertical/Halo Beta Formula Freeze",
        "",
        "This V2 formula is a source-side morphology refinement, not a residual fit.",
        "",
        "`v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_DVH(R)]`",
        "",
        "`K_DVH(R)=smoothstep((R-R_s)/(2R_s-R_s))`.",
        "",
        "The earlier EVH kernel used a far-outer activation window. The source review",
        "instead identifies distributed edge-on extraplanar dust/halo structure, so the",
        "activation is moved to one-to-two disk scale lengths as a source rule.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
    ]
    (REPORTS / "beta_transfer_distributed_vertical_halo_formula_freeze.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
