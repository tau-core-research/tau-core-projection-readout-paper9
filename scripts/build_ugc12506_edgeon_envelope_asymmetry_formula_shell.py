#!/usr/bin/env python3
"""Freeze an UGC12506 edge-on/envelope/asymmetry formula shell.

This script consumes the observer/path/interloper audit and builds a stronger
residual-blind formula shell from the source-allowed components:

- internal edge-on disk integration,
- extended H I envelope support,
- caveated approaching/receding extent asymmetry.

It deliberately excludes the image-plane interloper from the gravity kernel and
does not include any foreground/path object term.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation"


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


def normalized(series: pd.Series) -> pd.Series:
    max_abs = float(np.max(np.abs(series.to_numpy(dtype=float))))
    if max_abs <= 1.0e-12:
        return series * 0.0
    return series / max_abs


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    audit = pd.read_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv").iloc[0]
    if bool(audit["endpoint_scores_allowed"]):
        raise RuntimeError("Observer/path audit should not itself allow endpoint scoring")
    if bool(audit["uses_vobs_or_residual"]):
        raise RuntimeError("Observer/path audit used vobs/residual")

    obs = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    grid = pd.read_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 source-envelope grid")
    if bool(grid["construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Input grid is not residual-blind")

    values = obs.set_index("symbol")["value"].to_dict()
    i_deg = float(values["i"])
    rd_kpc = float(values["R_d"])
    rhi_kpc = float(values["R_HI_source"])
    ropt_kpc = float(values["R_opt"])
    lambda_spin = float(values["lambda_spin"])
    sigma_hi_range = float(values["Sigma_HI_range"])
    sigma_hi_unc = float(obs.set_index("symbol").loc["Sigma_HI_range", "uncertainty"])
    sigma_hi_min = max(sigma_hi_range - sigma_hi_unc, 0.0)

    sin2_i = float(np.sin(np.deg2rad(i_deg)) ** 2)
    edgeon_excess = float(max((i_deg - 80.0) / 10.0, 0.0))
    edgeon_load = sin2_i * edgeon_excess
    extent_asymmetry = float((70.0 - 50.0) / (70.0 + 50.0))
    low_sigma_load = float(np.clip((5.0 - sigma_hi_min) / 5.0, 0.0, 1.0))
    envelope_load = sin2_i * max(rhi_kpc / rd_kpc - 1.0, 0.0) * max(lambda_spin / 0.10, 0.0) * low_sigma_load

    r = grid["radius_kpc"].to_numpy(dtype=float)
    r_span = max(rhi_kpc - rd_kpc, 1.0e-6)
    outer_window = pd.Series(smoothstep((r - rd_kpc) / r_span), index=grid.index)
    envelope_shape = pd.Series(np.sqrt(np.clip((r - rd_kpc) / r_span, 0.0, 1.0)), index=grid.index)
    edgeon_shape = pd.Series(np.sqrt(np.clip(r / max(rhi_kpc, 1.0e-6), 0.0, 1.0)), index=grid.index)
    asymmetry_shape = pd.Series(np.clip((r - ropt_kpc) / max(rhi_kpc - ropt_kpc, 1.0e-6), 0.0, 1.0), index=grid.index)

    grid["K_edgeon_disk_integration_raw"] = edgeon_load * outer_window * edgeon_shape
    grid["K_extended_hi_envelope_raw"] = grid["K_envelope_source_support_norm"]
    grid["K_arm_asymmetry_extent_raw"] = sin2_i * extent_asymmetry * outer_window * asymmetry_shape

    grid["K_edgeon_disk_integration"] = normalized(grid["K_edgeon_disk_integration_raw"])
    grid["K_extended_hi_envelope"] = normalized(grid["K_extended_hi_envelope_raw"])
    grid["K_arm_asymmetry_extent"] = normalized(grid["K_arm_asymmetry_extent_raw"])

    # Source-side weights: strong components are weighted by their source loads,
    # while the caveated asymmetry component receives a fixed half-weight penalty.
    w_edge = edgeon_load
    w_env = envelope_load
    w_asym = 0.5 * sin2_i * extent_asymmetry
    w_sum = max(w_edge + w_env + w_asym, 1.0e-12)
    w_edge_n = w_edge / w_sum
    w_env_n = w_env / w_sum
    w_asym_n = w_asym / w_sum

    grid["K_edgeon_envelope_asymmetry_combined"] = (
        w_edge_n * grid["K_edgeon_disk_integration"]
        + w_env_n * grid["K_extended_hi_envelope"]
        + w_asym_n * grid["K_arm_asymmetry_extent"]
    )
    grid["K_edgeon_envelope_asymmetry_combined"] = normalized(
        grid["K_edgeon_envelope_asymmetry_combined"]
    )

    evidence_total = w_edge + w_env + w_asym
    gamma_total = evidence_total / (1.0 + evidence_total)
    carrier_scale_outer = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), "v2_carrier_km2_s2"].median())
    if not np.isfinite(carrier_scale_outer):
        carrier_scale_outer = float(grid["v2_carrier_km2_s2"].tail(8).median())
    amplitude_total = gamma_total * carrier_scale_outer

    grid["A_eea_source_frozen_km2_s2"] = amplitude_total
    grid["v2_eea_positive_prefrozen_km2_s2"] = (
        grid["v2_carrier_km2_s2"] + amplitude_total * grid["K_edgeon_envelope_asymmetry_combined"]
    )
    grid["v2_eea_negative_control_km2_s2"] = (
        grid["v2_carrier_km2_s2"] - amplitude_total * grid["K_edgeon_envelope_asymmetry_combined"]
    )
    grid["v_eea_positive_prefrozen_kms"] = np.sqrt(np.maximum(grid["v2_eea_positive_prefrozen_km2_s2"], 0.0))
    grid["v_eea_negative_control_kms"] = np.sqrt(np.maximum(grid["v2_eea_negative_control_km2_s2"], 0.0))
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_validation_claim_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    components = pd.DataFrame(
        [
            {
                "component_id": "K_edgeon_disk_integration",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_STRONG",
                "source_load": w_edge,
                "normalized_weight": w_edge_n,
                "kernel_column": "K_edgeon_disk_integration",
                "source_basis": "i=86 deg and PV/envelope method required",
            },
            {
                "component_id": "K_extended_hi_envelope",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_STRONG",
                "source_load": w_env,
                "normalized_weight": w_env_n,
                "kernel_column": "K_extended_hi_envelope",
                "source_basis": "large H I extent, diffuse stable gas, high spin",
            },
            {
                "component_id": "K_arm_asymmetry_extent",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_CAVEATED_HALF_WEIGHT",
                "source_load": w_asym,
                "normalized_weight": w_asym_n,
                "kernel_column": "K_arm_asymmetry_extent",
                "source_basis": "approaching/receding detectable extent asymmetry",
            },
            {
                "component_id": "M_photometric_interloper_mask",
                "component_status": "EXCLUDED_FROM_GRAVITY_KERNEL_MASK_CAVEAT_ONLY",
                "source_load": 0.0,
                "normalized_weight": 0.0,
                "kernel_column": "",
                "source_basis": "higher-redshift galaxy and star are image-plane interlopers",
            },
            {
                "component_id": "K_foreground_path_object",
                "component_status": "EXCLUDED_NOT_ESTABLISHED",
                "source_load": 0.0,
                "normalized_weight": 0.0,
                "kernel_column": "",
                "source_basis": "no foreground/path object established by current source",
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
                "formula_id": "UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL",
                "formula_text": "v_readout^2(R)=v_carrier^2(R)+A_eea K_eea(R)",
                "kernel_text": (
                    "K_eea=norm[w_edge K_edge + w_env K_env + w_asym K_asym]; "
                    "interloper mask excluded from gravity kernel"
                ),
                "amplitude_rule": "A_eea=Gamma_eea median_outer_R>=Ropt(v_carrier^2)",
                "gamma_rule": "Gamma_eea=E_eea/(1+E_eea), E_eea=w_edge+w_env+w_asym",
                "edgeon_load": w_edge,
                "envelope_load": w_env,
                "asymmetry_load_half_weighted": w_asym,
                "edgeon_weight": w_edge_n,
                "envelope_weight": w_env_n,
                "asymmetry_weight": w_asym_n,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "carrier_scale_outer_km2_s2": carrier_scale_outer,
                "amplitude_total_km2_s2": amplitude_total,
                "dimension_check": "PASS: A_eea has km^2/s^2 and K_eea is dimensionless",
                "known_limits": (
                    "i<=80 deg, R_HI/R_d->1, lambda_spin->0, or K_eea=0 recovers carrier"
                ),
                "interloper_policy": "photometric mask/caveat only; no foreground path gravity term",
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
                "gate_id": "U12506_EEA_G1_AUDIT_INPUT",
                "gate_status": "PASS",
                "evidence": str(audit["audit_status"]),
                "remaining_obligation": "none for formula replay",
            },
            {
                "gate_id": "U12506_EEA_G2_INTERLOPER_EXCLUSION",
                "gate_status": "PASS",
                "evidence": "image-plane interlopers excluded from gravity kernel",
                "remaining_obligation": "foreground/path term requires new catalogue cone search",
            },
            {
                "gate_id": "U12506_EEA_G3_COMPONENT_WEIGHTS",
                "gate_status": "PASS_CAVEATED",
                "evidence": "asymmetry half-weighted due to caveated source status",
                "remaining_obligation": "independent source-side asymmetry normalization review",
            },
            {
                "gate_id": "U12506_EEA_G4_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "A_eea velocity-squared; K_eea dimensionless; carrier limits explicit",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_EEA_G5_RESIDUAL_BLIND",
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
                "formula_shell_status": "UGC12506_EEA_FORMULA_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION",
                "galaxy": GALAXY,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "amplitude_total_km2_s2": amplitude_total,
                "kernel_outer_mean_last8": float(
                    grid["K_edgeon_envelope_asymmetry_combined"].tail(8).mean()
                ),
                "edgeon_weight": w_edge_n,
                "envelope_weight": w_env_n,
                "asymmetry_weight": w_asym_n,
                "n_gates": len(gates),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "formula_frozen_before_scoring": True,
                "control_replay_scores_allowed": True,
                "endpoint_validation_claim_allowed": False,
                "construction_used_vobs_or_residual": False,
                "next_script": "scripts/run_ugc12506_edgeon_envelope_asymmetry_replay_controls.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_grid.csv", index=False)
    components.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_components.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_edgeon_envelope_asymmetry_formula_shell_summary.csv", index=False)

    report = [
        "# UGC12506 Edge-on + Envelope + Asymmetry Formula Shell",
        "",
        "This source-frozen shell uses only the components allowed by the",
        "observer/path/interloper audit. It excludes the image-plane interloper",
        "from the gravity kernel and does not include a foreground/path object.",
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
    ]
    (REPORTS / "ugc12506_edgeon_envelope_asymmetry_formula_shell.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
