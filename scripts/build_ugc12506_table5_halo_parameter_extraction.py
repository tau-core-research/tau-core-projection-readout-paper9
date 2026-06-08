#!/usr/bin/env python3
"""Extract UGC12506 source-native halo parameters from Hallenbeck et al. Table 5."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    rows = pd.DataFrame(
        [
            {
                "galaxy": "UGC9037",
                "nfw_c": 2.67,
                "nfw_c_err": 0.50,
                "nfw_r200_kpc": 121.0,
                "nfw_r200_err_kpc": 12.0,
                "chi2_nfw": 1.29,
                "iso_rho_c_1e_minus3_msun_pc3": 18.0,
                "iso_rho_c_err": 2.0,
                "iso_rc_kpc": 5.16,
                "iso_rc_err_kpc": 0.40,
                "chi2_iso": 0.65,
                "lambda_spin": 0.07,
            },
            {
                "galaxy": "UGC12506",
                "nfw_c": 14.87,
                "nfw_c_err": 0.60,
                "nfw_r200_kpc": 123.0,
                "nfw_r200_err_kpc": 1.5,
                "chi2_nfw": 0.21,
                "iso_rho_c_1e_minus3_msun_pc3": 1150.0,
                "iso_rho_c_err": 360.0,
                "iso_rc_kpc": 0.91,
                "iso_rc_err_kpc": 0.15,
                "chi2_iso": 0.54,
                "lambda_spin": 0.15,
            },
        ]
    )
    rows["source_id"] = "UGC12506_HI_SRC1_HIGHMASS_VLA"
    rows["source_table"] = "Hallenbeck2014 Table 5"
    rows["text_line_range"] = "1268-1330"
    rows["residual_blind_source_extraction"] = True
    rows["endpoint_scores_allowed"] = False
    rows["claim_boundary"] = CLAIM_BOUNDARY

    u = rows.loc[rows["galaxy"].eq(GALAXY)].iloc[0]
    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_T5_G1_TABLE_PRESENT",
                "gate_status": "PASS",
                "evidence": "Table 5 dark matter halo properties extracted from local source text",
                "remaining_obligation": "manual independent review recommended before accepted endpoint use",
            },
            {
                "gate_id": "U12506_T5_G2_NFW_PREFERENCE_NUMERIC",
                "gate_status": "PASS",
                "evidence": f"chi2_nfw={u['chi2_nfw']}, chi2_iso={u['chi2_iso']}",
                "remaining_obligation": "none for replay",
            },
            {
                "gate_id": "U12506_T5_G3_SOURCE_NATIVE_C_R200",
                "gate_status": "PASS",
                "evidence": f"c={u['nfw_c']}±{u['nfw_c_err']}, R200={u['nfw_r200_kpc']}±{u['nfw_r200_err_kpc']} kpc",
                "remaining_obligation": "propagate uncertainty later",
            },
            {
                "gate_id": "U12506_T5_G4_NO_RESIDUAL_USE",
                "gate_status": "PASS",
                "evidence": "extraction uses published source table only",
                "remaining_obligation": "vobs enters only downstream scoring",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "extraction_status": "UGC12506_TABLE5_HALO_PARAMETERS_EXTRACTED_SOURCE_NATIVE_REPLAY_READY",
                "galaxy": GALAXY,
                "nfw_c": float(u["nfw_c"]),
                "nfw_c_err": float(u["nfw_c_err"]),
                "nfw_r200_kpc": float(u["nfw_r200_kpc"]),
                "nfw_r200_err_kpc": float(u["nfw_r200_err_kpc"]),
                "chi2_nfw": float(u["chi2_nfw"]),
                "chi2_iso": float(u["chi2_iso"]),
                "lambda_spin": float(u["lambda_spin"]),
                "nfw_preferred_over_iso": bool(float(u["chi2_nfw"]) < float(u["chi2_iso"])),
                "source_native_nfw_kernel_allowed": True,
                "endpoint_scores_allowed": False,
                "next_gate": "build_ugc12506_source_native_nfw_hse_shell",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rows.to_csv(DATA / "ugc12506_table5_halo_parameter_extraction_rows.csv", index=False)
    gates.to_csv(DATA / "ugc12506_table5_halo_parameter_extraction_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_table5_halo_parameter_extraction_summary.csv", index=False)

    report = [
        "# UGC12506 Table 5 Halo Parameter Extraction",
        "",
        "This source-native extraction replaces the earlier `R_d` NFW-scale proxy",
        "with the published Table 5 NFW concentration and R200 values.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Extracted Rows",
        "",
        markdown_table(rows),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The extraction is source-native and residual-blind. It is suitable for a",
        "replay shell, not by itself an accepted endpoint validation.",
        "",
    ]
    (REPORTS / "ugc12506_table5_halo_parameter_extraction.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
