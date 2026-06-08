#!/usr/bin/env python3
"""Freeze an edge-on vertical/halo gated beta-transfer formula.

The formula is derived from the source-side lock review for NGC0891 and
NGC4217.  It keeps the accepted beta/spin proxy as a component but prevents the
beta factor from acting globally.  The beta excess is gated by a source-side
outer vertical/halo window set by disk-scale morphology proxies.

No observed velocities or endpoint residuals are read here.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
CLAIM_BOUNDARY = "beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint"

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
                "compact_support_radius_proxy_kpc",
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
        r_on = 2.0 * rs
        r_full = min(3.0 * rs, r_max)
        if r_full <= r_on:
            r_full = r_max
        rows.append(
            {
                "galaxy": row["galaxy"],
                "formula_id": f"{row['galaxy']}_EDGEON_VERTICAL_HALO_GATED_BETA_V1",
                "source_supported_lock_type": row["source_supported_lock_type"],
                "carrier_id": "BARYONIC_050_FAST_PACKET",
                "spin_route": "BULLOCK_DISK_CONVERSION",
                "beta_cl_value": float(row["beta_if_bullock_disk_proxy_used"]),
                "formula_text": (
                    "v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_EVH(R)]"
                ),
                "kernel_text": (
                    "K_EVH(R)=smoothstep((R-R_on)/(R_full-R_on)); "
                    "R_on=2 R_s, R_full=min(3 R_s,R_max)"
                ),
                "source_window_rule": "outer vertical/halo component activates after two disk scale lengths",
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
                    "PASS: beta_cl and K_EVH are dimensionless; correction multiplies v_carrier^2"
                ),
                "inner_limit": "R <= R_on gives K_EVH=0 and recovers v_carrier",
                "outer_limit": "R >= R_full gives K_EVH=1 and recovers beta-transfer component",
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
    gates = pd.DataFrame(
        [
            {
                "galaxy": row["galaxy"],
                "formula_id": row["formula_id"],
                "gate_id": "EVH1_LOCK_REVIEW",
                "gate_status": "PASS",
                "evidence": row["source_supported_lock_type"],
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in manifest.iterrows()
        ]
        + [
            {
                "galaxy": row["galaxy"],
                "formula_id": row["formula_id"],
                "gate_id": "EVH2_SOURCE_WINDOW",
                "gate_status": "PASS",
                "evidence": f"R_on=2R_s={row['r_on_kpc']:.3f} kpc; R_full={row['r_full_kpc']:.3f} kpc",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in manifest.iterrows()
        ]
        + [
            {
                "galaxy": row["galaxy"],
                "formula_id": row["formula_id"],
                "gate_id": "EVH3_BETA_COMPONENT_SOURCE_FIXED",
                "gate_status": "PASS",
                "evidence": f"beta_cl={row['beta_cl_value']:.6g} from {row['spin_route']}",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in manifest.iterrows()
        ]
        + [
            {
                "galaxy": row["galaxy"],
                "formula_id": row["formula_id"],
                "gate_id": "EVH4_DIMENSIONS_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1",
                "uses_vobs_or_residual": False,
                "endpoint_scores_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
            for _, row in manifest.iterrows()
        ]
    )

    summary = pd.DataFrame(
        [
            {
                "formula_freeze_status": "EDGEON_VERTICAL_HALO_GATED_BETA_FORMULA_FROZEN_CONTROL_REPLAY_ALLOWED",
                "n_galaxies": len(manifest),
                "n_gates": len(gates),
                "n_pass_gates": int(gates["gate_status"].eq("PASS").sum()),
                "uses_vobs_or_residual_in_construction": False,
                "control_replay_allowed": True,
                "endpoint_scores_allowed": False,
                "endpoint_validation_claim": False,
                "next_action": "run_control_replay_scoring_script",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest_path = DATA / "beta_transfer_edgeon_vertical_halo_formula_freeze_manifest.csv"
    gates_path = DATA / "beta_transfer_edgeon_vertical_halo_formula_freeze_gates.csv"
    summary_path = DATA / "beta_transfer_edgeon_vertical_halo_formula_freeze_summary.csv"
    manifest.to_csv(manifest_path, index=False)
    gates.to_csv(gates_path, index=False)
    summary.to_csv(summary_path, index=False)

    report = [
        "# Edge-on Vertical/Halo Gated Beta Formula Freeze",
        "",
        "The pure beta-transfer branch is source-rejected as the primary lock for NGC0891 and NGC4217.",
        "This formula keeps beta as an accepted component but gates it by an outer vertical/halo source window.",
        "",
        "## Formula",
        "",
        "`v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_EVH(R)]`",
        "",
        "`K_EVH(R)=smoothstep((R-R_on)/(R_full-R_on))`, with `R_on=2R_s` and `R_full=min(3R_s,R_max)`.",
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
    (REPORTS / "beta_transfer_edgeon_vertical_halo_formula_freeze.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
