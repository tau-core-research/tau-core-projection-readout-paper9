#!/usr/bin/env python3
"""Freeze a caveated incremental projection-history shell for UGC12506.

The shell is incremental on top of the source-native NFW-HSE replay. It avoids
double-counting the already included NFW/envelope support and admits only the
source-supported internal projection and caveated asymmetry/history terms.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_projection_history_incremental_formula_shell_not_validation"


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


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def normalized(x: np.ndarray) -> np.ndarray:
    m = float(np.max(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    candidate = pd.read_csv(DATA / "ugc12506_projection_history_readout_candidate_summary.csv").iloc[0]
    if bool(candidate["endpoint_scores_allowed"]):
        raise RuntimeError("Projection-history candidate gate should not allow endpoint scoring")
    if "SOURCE_SUPPORTED_CAVEATED" not in str(candidate["candidate_status"]):
        raise RuntimeError("Projection-history candidate gate is not source-supported caveated")

    obs = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    grid = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 source-native NFW-HSE grid")
    if bool(grid["construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Input source-native NFW-HSE grid is not residual-blind")

    values = obs.set_index("symbol")["value"].to_dict()
    i_deg = float(values["i"])
    rd_kpc = float(values["R_d"])
    rhi_kpc = float(values["R_HI_source"])
    ropt_kpc = float(values["R_opt"])
    lambda_spin = float(values["lambda_spin"])
    extent_asymmetry = float(values["A_extent"])

    r = grid["radius_kpc"].to_numpy(dtype=float)
    sin2_i = float(np.sin(np.deg2rad(i_deg)) ** 2)
    edgeon_excess = float(max((i_deg - 80.0) / 10.0, 0.0))
    edgeon_load = sin2_i * edgeon_excess
    spin_history_factor = float(np.clip(lambda_spin / 0.10, 0.0, 2.0))
    asym_history_load = 0.5 * sin2_i * extent_asymmetry * spin_history_factor
    evidence_total = edgeon_load + asym_history_load
    gamma_total = evidence_total / (1.0 + evidence_total)

    outer_window = smoothstep((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6))
    edgeon_shape = outer_window * np.sqrt(np.clip(r / max(rhi_kpc, 1.0e-6), 0.0, 1.0))
    asym_shape = outer_window * np.clip((r - ropt_kpc) / max(rhi_kpc - ropt_kpc, 1.0e-6), 0.0, 1.0)

    k_edge = normalized(edgeon_shape)
    k_asym = normalized(asym_shape)
    w_sum = max(edgeon_load + asym_history_load, 1.0e-12)
    w_edge = edgeon_load / w_sum
    w_asym = asym_history_load / w_sum
    k_ph = normalized(w_edge * k_edge + w_asym * k_asym)

    # Incremental amplitude uses the already frozen source-native NFW-HSE
    # carrier/readout scale, not endpoint residuals.
    base_v2_col = "v2_source_native_nfw_hse_positive_km2_s2"
    source_native_outer_scale = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), base_v2_col].median())
    if not np.isfinite(source_native_outer_scale):
        source_native_outer_scale = float(grid[base_v2_col].tail(8).median())
    amplitude_ph = gamma_total * source_native_outer_scale

    grid["K_projection_history_edgeon_increment"] = k_edge
    grid["K_projection_history_asymmetry_increment"] = k_asym
    grid["K_projection_history_incremental"] = k_ph
    grid["A_projection_history_incremental_km2_s2"] = amplitude_ph
    grid["v2_projection_history_incremental_positive_km2_s2"] = (
        grid[base_v2_col] + amplitude_ph * k_ph
    )
    grid["v2_projection_history_incremental_negative_km2_s2"] = (
        grid[base_v2_col] - amplitude_ph * k_ph
    )
    grid["v_projection_history_incremental_positive_kms"] = np.sqrt(
        np.maximum(grid["v2_projection_history_incremental_positive_km2_s2"], 0.0)
    )
    grid["v_projection_history_incremental_negative_kms"] = np.sqrt(
        np.maximum(grid["v2_projection_history_incremental_negative_km2_s2"], 0.0)
    )
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_validation_claim_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    components = pd.DataFrame(
        [
            {
                "component_id": "K_edgeon_disk_integration_increment",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_STRONG",
                "source_load": edgeon_load,
                "normalized_weight": w_edge,
                "kernel_column": "K_projection_history_edgeon_increment",
                "source_basis": "i=86 deg and PV/envelope method required",
            },
            {
                "component_id": "K_arm_asymmetry_history_increment",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_CAVEATED",
                "source_load": asym_history_load,
                "normalized_weight": w_asym,
                "kernel_column": "K_projection_history_asymmetry_increment",
                "source_basis": "approaching/receding extent asymmetry coupled to high-spin context",
            },
            {
                "component_id": "K_extended_hi_envelope_main",
                "component_status": "EXCLUDED_FROM_INCREMENT_ALREADY_IN_NFW_HSE",
                "source_load": 0.0,
                "normalized_weight": 0.0,
                "kernel_column": "",
                "source_basis": "included in source-native NFW-HSE base shell",
            },
            {
                "component_id": "K_foreground_path_object",
                "component_status": "EXCLUDED_NOT_ESTABLISHED",
                "source_load": 0.0,
                "normalized_weight": 0.0,
                "kernel_column": "",
                "source_basis": "no source-supported foreground/path object",
            },
        ]
    )
    components["galaxy"] = GALAXY
    components["claim_boundary"] = CLAIM_BOUNDARY
    components = components[
        [
            "galaxy",
            "component_id",
            "component_status",
            "source_load",
            "normalized_weight",
            "kernel_column",
            "source_basis",
            "claim_boundary",
        ]
    ]

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": "UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE",
                "formula_text": (
                    "v_readout^2(R)=v_source_native_nfw_hse^2(R)+A_PH K_PH(R)"
                ),
                "kernel_text": (
                    "K_PH=norm[w_edge K_edgeon_increment + w_asym K_asymmetry_history_increment]"
                ),
                "amplitude_rule": "A_PH=Gamma_PH median_outer_R>=Ropt(v_source_native_nfw_hse^2)",
                "gamma_rule": "Gamma_PH=E_PH/(1+E_PH), E_PH=w_edge_source+w_asym_history_source",
                "edgeon_load": edgeon_load,
                "asymmetry_history_load": asym_history_load,
                "edgeon_weight": w_edge,
                "asymmetry_weight": w_asym,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "source_native_outer_scale_km2_s2": source_native_outer_scale,
                "amplitude_ph_km2_s2": amplitude_ph,
                "dimension_check": "PASS: A_PH has km^2/s^2 and K_PH is dimensionless",
                "known_limits": (
                    "i<=80 deg and A_extent=0 recover the source-native NFW-HSE base; "
                    "no foreground/path object term is included"
                ),
                "double_counting_policy": "extended H I envelope excluded from increment because NFW-HSE base already includes it",
                "formula_frozen_before_scoring": True,
                "construction_used_vobs_or_residual": False,
                "endpoint_validation_claim_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_PHI_G1_CANDIDATE_GATE",
                "gate_status": "PASS_CAVEATED",
                "evidence": str(candidate["candidate_status"]),
                "remaining_obligation": "not endpoint validation",
            },
            {
                "gate_id": "U12506_PHI_G2_SIGN_RULE",
                "gate_status": "PASS_CAVEATED",
                "evidence": "edge-on PV/envelope and extent asymmetry enter as positive 1D readout broadening terms",
                "remaining_obligation": "resolved velocity-field review for side-specific sign",
            },
            {
                "gate_id": "U12506_PHI_G3_NO_DOUBLE_COUNT_ENVELOPE",
                "gate_status": "PASS",
                "evidence": "extended envelope is excluded from the incremental PH term because it is already in NFW-HSE",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_PHI_G4_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "A_PH velocity-squared; K_PH dimensionless; base recovery limits explicit",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_PHI_G5_RESIDUAL_BLIND",
                "gate_status": "PASS",
                "evidence": "construction_used_vobs_or_residual=False",
                "remaining_obligation": "vobs may enter only in separate replay scoring script",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["formula_id"] = str(manifest["formula_id"].iloc[0])
    gates["endpoint_validation_claim_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_validation_claim_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "formula_shell_status": "UGC12506_INCREMENTAL_PROJECTION_HISTORY_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION",
                "galaxy": GALAXY,
                "edgeon_weight": w_edge,
                "asymmetry_weight": w_asym,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "amplitude_ph_km2_s2": amplitude_ph,
                "kernel_inner_mean_first8": float(np.mean(k_ph[:8])),
                "kernel_outer_mean_last8": float(np.mean(k_ph[-8:])),
                "n_gates": len(gates),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].str.contains("CAVEATED").sum()),
                "formula_frozen_before_scoring": True,
                "control_replay_scores_allowed": True,
                "endpoint_validation_claim_allowed": False,
                "construction_used_vobs_or_residual": False,
                "next_script": "scripts/run_ugc12506_projection_history_incremental_replay.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_grid.csv", index=False)
    components.to_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_components.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_projection_history_incremental_formula_shell_summary.csv", index=False)

    report = [
        "# UGC12506 Incremental Projection-History Formula Shell",
        "",
        "This shell is incremental on top of the source-native NFW-HSE readout.",
        "It includes only the source-supported internal projection and caveated",
        "asymmetry/history terms, and avoids double-counting the extended H I",
        "envelope already present in the NFW-HSE base.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Manifest",
        "",
        markdown_table(manifest),
        "",
        "## Components",
        "",
        markdown_table(components),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "This is a caveated control replay shell, not endpoint validation. The",
        "positive sign is justified only at the 1D readout-broadening level; a",
        "resolved velocity-field review is still required for a side-specific",
        "projection/history sign rule.",
        "",
    ]
    (REPORTS / "ugc12506_projection_history_incremental_formula_shell.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
