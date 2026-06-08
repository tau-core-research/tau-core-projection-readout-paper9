#!/usr/bin/env python3
"""Freeze a UGC12506 source-native NFW/high-spin-envelope replay shell.

This replaces the earlier R_d-based NFW-like concentration proxy with the
published Hallenbeck et al. Table 5 NFW concentration and R200 values.  It is a
residual-blind replay shell: observed velocities are present in the inherited
grid for downstream plotting/scoring compatibility, but they are not used to
select the kernel, sign, amplitude, or source label.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_source_native_nfw_hse_shell_replay_not_validation"


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


def normalized(x: np.ndarray) -> np.ndarray:
    m = float(np.max(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def nfw_velocity2_shape(r_kpc: np.ndarray, concentration: float, r200_kpc: float) -> np.ndarray:
    y = np.maximum(r_kpc / max(r200_kpc, 1.0e-9), 1.0e-9)
    cy = concentration * y
    denom = np.log1p(concentration) - concentration / (1.0 + concentration)
    profile = (np.log1p(cy) - cy / (1.0 + cy)) / np.maximum(y * denom, 1.0e-12)
    return normalized(profile)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    table_summary = pd.read_csv(DATA / "ugc12506_table5_halo_parameter_extraction_summary.csv").iloc[0]
    if bool(table_summary["endpoint_scores_allowed"]):
        raise RuntimeError("Table 5 extraction should not allow endpoint scoring")
    if not bool(table_summary["source_native_nfw_kernel_allowed"]):
        raise RuntimeError("Source-native NFW kernel is not allowed by Table 5 gate")

    route = pd.read_csv(DATA / "ugc12506_prior_best_source_route_audit_summary.csv").iloc[0]
    if str(route["nfw_rapid_rise_route"]) != "SOURCE_SUPPORTED_CANDIDATE":
        raise RuntimeError("NFW rapid-rise route is not source-supported")

    obs = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    grid = pd.read_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 envelope grid")
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

    nfw_c = float(table_summary["nfw_c"])
    nfw_c_err = float(table_summary["nfw_c_err"])
    nfw_r200_kpc = float(table_summary["nfw_r200_kpc"])
    nfw_r200_err_kpc = float(table_summary["nfw_r200_err_kpc"])
    chi2_nfw = float(table_summary["chi2_nfw"])
    chi2_iso = float(table_summary["chi2_iso"])
    rs_nfw_kpc = nfw_r200_kpc / nfw_c

    r = grid["radius_kpc"].to_numpy(dtype=float)
    sin2_i = float(np.sin(np.deg2rad(i_deg)) ** 2)
    low_sigma_load = float(np.clip((5.0 - sigma_hi_min) / 5.0, 0.0, 1.0))
    spin_load = max(lambda_spin / 0.10, 0.0)
    envelope_load = sin2_i * max(rhi_kpc / rd_kpc - 1.0, 0.0) * spin_load * low_sigma_load

    k_nfw = nfw_velocity2_shape(r, nfw_c, nfw_r200_kpc)
    outer_window = smoothstep((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6))
    k_env = grid["K_envelope_source_support_norm"].to_numpy(dtype=float)
    k_hybrid = normalized((1.0 - outer_window) * k_nfw + outer_window * np.maximum(k_nfw, k_env))

    nfw_preference_load = max(chi2_iso / max(chi2_nfw, 1.0e-9) - 1.0, 0.0)
    edgeon_load = sin2_i * max((i_deg - 80.0) / 10.0, 0.0)
    evidence_total = nfw_preference_load + envelope_load + edgeon_load
    gamma_total = evidence_total / (1.0 + evidence_total)
    carrier_scale_outer = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), "v2_carrier_km2_s2"].median())
    if not np.isfinite(carrier_scale_outer):
        carrier_scale_outer = float(grid["v2_carrier_km2_s2"].tail(8).median())
    amplitude_total = gamma_total * carrier_scale_outer

    grid["K_source_native_nfw_velocity2"] = k_nfw
    grid["K_highspin_envelope"] = k_env
    grid["W_outer_Rd_to_RHI_source"] = outer_window
    grid["K_source_native_nfw_hse"] = k_hybrid
    grid["A_source_native_nfw_hse_km2_s2"] = amplitude_total
    grid["v2_source_native_nfw_hse_positive_km2_s2"] = grid["v2_carrier_km2_s2"] + amplitude_total * k_hybrid
    grid["v2_source_native_nfw_hse_negative_km2_s2"] = grid["v2_carrier_km2_s2"] - amplitude_total * k_hybrid
    grid["v_source_native_nfw_hse_positive_kms"] = np.sqrt(
        np.maximum(grid["v2_source_native_nfw_hse_positive_km2_s2"], 0.0)
    )
    grid["v_source_native_nfw_hse_negative_kms"] = np.sqrt(
        np.maximum(grid["v2_source_native_nfw_hse_negative_km2_s2"], 0.0)
    )
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_validation_claim_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": "UGC12506_SOURCE_NATIVE_NFW_HSE",
                "formula_text": "v_readout^2(R)=v_carrier^2(R)+A_source_native_nfw_hse K_source_native_nfw_hse(R)",
                "kernel_text": (
                    "K=norm[(1-W_outer)K_NFW_V2(R;c,R200)+W_outer max(K_NFW_V2,K_env)]"
                ),
                "nfw_v2_shape": (
                    "K_NFW_V2=norm({ln(1+cR/R200)-cR/R200/(1+cR/R200)} / "
                    "{(R/R200)[ln(1+c)-c/(1+c)]})"
                ),
                "amplitude_rule": "A=Gamma median_outer_R>=Ropt(v_carrier^2)",
                "gamma_rule": (
                    "Gamma=E/(1+E), E=(chi2_iso/chi2_nfw-1)_+ + E_highspin_envelope + E_edgeon"
                ),
                "nfw_c": nfw_c,
                "nfw_c_err": nfw_c_err,
                "nfw_r200_kpc": nfw_r200_kpc,
                "nfw_r200_err_kpc": nfw_r200_err_kpc,
                "rs_nfw_kpc": rs_nfw_kpc,
                "chi2_nfw": chi2_nfw,
                "chi2_iso": chi2_iso,
                "nfw_preference_load": nfw_preference_load,
                "envelope_load": envelope_load,
                "edgeon_load": edgeon_load,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "carrier_scale_outer_km2_s2": carrier_scale_outer,
                "amplitude_total_km2_s2": amplitude_total,
                "dimension_check": "PASS: A has km^2/s^2; K is dimensionless",
                "known_limits": (
                    "K=0, Gamma=0, or absent NFW/envelope evidence recovers carrier; "
                    "outer_window=0 leaves source-native NFW seed"
                ),
                "source_native_upgrade": "replaces R_d proxy with Hallenbeck2014 Table 5 c,R200",
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
                "gate_id": "U12506_SNFW_G1_TABLE5_PARAMETERS",
                "gate_status": "PASS",
                "evidence": f"c={nfw_c}±{nfw_c_err}, R200={nfw_r200_kpc}±{nfw_r200_err_kpc} kpc",
                "remaining_obligation": "uncertainty propagation later",
            },
            {
                "gate_id": "U12506_SNFW_G2_NFW_PREFERENCE_LOAD",
                "gate_status": "PASS",
                "evidence": f"chi2_nfw={chi2_nfw}, chi2_iso={chi2_iso}, load={nfw_preference_load:.6g}",
                "remaining_obligation": "independent reviewer can confirm table extraction",
            },
            {
                "gate_id": "U12506_SNFW_G3_HIGHSPIN_ENVELOPE",
                "gate_status": "PASS",
                "evidence": f"lambda={lambda_spin}, RHI/Rd={rhi_kpc / rd_kpc:.6g}",
                "remaining_obligation": "none for replay",
            },
            {
                "gate_id": "U12506_SNFW_G4_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "velocity-squared amplitude times dimensionless kernel",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_SNFW_G5_RESIDUAL_BLIND",
                "gate_status": "PASS",
                "evidence": "kernel and amplitude use source tables and carrier only; no vobs/residual",
                "remaining_obligation": "vobs may enter only in scoring replay",
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
                "formula_shell_status": "UGC12506_SOURCE_NATIVE_NFW_HSE_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION",
                "galaxy": GALAXY,
                "nfw_c": nfw_c,
                "nfw_r200_kpc": nfw_r200_kpc,
                "rs_nfw_kpc": rs_nfw_kpc,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "amplitude_total_km2_s2": amplitude_total,
                "kernel_inner_mean_first8": float(grid["K_source_native_nfw_hse"].head(8).mean()),
                "kernel_outer_mean_last8": float(grid["K_source_native_nfw_hse"].tail(8).mean()),
                "n_gates": len(gates),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "formula_frozen_before_scoring": True,
                "control_replay_scores_allowed": True,
                "endpoint_validation_claim_allowed": False,
                "construction_used_vobs_or_residual": False,
                "next_script": "scripts/run_ugc12506_source_native_nfw_hse_replay.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_source_native_nfw_hse_shell_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_source_native_nfw_hse_shell_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_native_nfw_hse_shell_summary.csv", index=False)

    report = [
        "# UGC12506 Source-Native NFW + High-Spin Envelope Shell",
        "",
        "This shell replaces the earlier disk-scale NFW proxy with the published",
        "Hallenbeck et al. Table 5 NFW concentration and R200.  It remains a",
        "replay shell rather than endpoint validation.",
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
        "## Claim Boundary",
        "",
        "The formula is frozen from source-native halo, H I envelope, inclination,",
        "and carrier quantities. Observed rotation velocities may enter only in",
        "the downstream replay scoring script.",
        "",
    ]
    (REPORTS / "ugc12506_source_native_nfw_hse_shell.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
