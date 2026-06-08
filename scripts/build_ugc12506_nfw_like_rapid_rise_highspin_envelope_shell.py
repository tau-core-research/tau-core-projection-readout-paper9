#!/usr/bin/env python3
"""Freeze an UGC12506 NFW-like rapid-rise/high-spin envelope shell.

This shell follows the source-route audit: UGC12506 should not promote the
prior diagnostic K_compact_finite label, because the source reports significant
NFW preference and rapid rise.  Instead, this residual-blind freeze builds a
source-side shell that combines a rapid-rise NFW-like kernel with the high-spin
extended-envelope support.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation"


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


def nfw_like_rise(r: np.ndarray, rs: float) -> np.ndarray:
    x = np.maximum(r / max(rs, 1.0e-6), 1.0e-6)
    profile = (np.log1p(x) - x / (1.0 + x)) / x
    return normalized(profile)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    route = pd.read_csv(DATA / "ugc12506_prior_best_source_route_audit_summary.csv").iloc[0]
    if bool(route["endpoint_scores_allowed"]):
        raise RuntimeError("Prior-best source-route audit should not allow endpoint scoring")
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

    r = grid["radius_kpc"].to_numpy(dtype=float)
    sin2_i = float(np.sin(np.deg2rad(i_deg)) ** 2)
    low_sigma_load = float(np.clip((5.0 - sigma_hi_min) / 5.0, 0.0, 1.0))
    spin_load = max(lambda_spin / 0.10, 0.0)
    envelope_load = sin2_i * max(rhi_kpc / rd_kpc - 1.0, 0.0) * spin_load * low_sigma_load

    # Source-side rapid-rise scale: the paper states the curve rises quickly
    # and reaches the maximum by the inner disk; use the disk scale as the
    # residual-blind concentration proxy.
    rs_nfw_proxy = rd_kpc
    k_nfw = nfw_like_rise(r, rs_nfw_proxy)
    outer_window = smoothstep((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6))
    k_env = grid["K_envelope_source_support_norm"].to_numpy(dtype=float)
    k_hybrid = normalized((1.0 - outer_window) * k_nfw + outer_window * np.maximum(k_nfw, k_env))

    nfw_preference_load = 1.0
    edgeon_load = sin2_i * max((i_deg - 80.0) / 10.0, 0.0)
    evidence_total = nfw_preference_load + envelope_load + edgeon_load
    gamma_total = evidence_total / (1.0 + evidence_total)
    carrier_scale_outer = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), "v2_carrier_km2_s2"].median())
    if not np.isfinite(carrier_scale_outer):
        carrier_scale_outer = float(grid["v2_carrier_km2_s2"].tail(8).median())
    amplitude_total = gamma_total * carrier_scale_outer

    grid["K_nfw_like_rapid_rise"] = k_nfw
    grid["K_highspin_envelope"] = k_env
    grid["K_nfw_like_rapid_rise_highspin_envelope"] = k_hybrid
    grid["A_nfw_hse_source_frozen_km2_s2"] = amplitude_total
    grid["v2_nfw_hse_positive_prefrozen_km2_s2"] = grid["v2_carrier_km2_s2"] + amplitude_total * k_hybrid
    grid["v2_nfw_hse_negative_control_km2_s2"] = grid["v2_carrier_km2_s2"] - amplitude_total * k_hybrid
    grid["v_nfw_hse_positive_prefrozen_kms"] = np.sqrt(
        np.maximum(grid["v2_nfw_hse_positive_prefrozen_km2_s2"], 0.0)
    )
    grid["v_nfw_hse_negative_control_kms"] = np.sqrt(
        np.maximum(grid["v2_nfw_hse_negative_control_km2_s2"], 0.0)
    )
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_validation_claim_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": "UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE",
                "formula_text": "v_readout^2(R)=v_carrier^2(R)+A_nfw_hse K_nfw_hse(R)",
                "kernel_text": (
                    "K_nfw_hse=norm[(1-W_outer)K_NFWlike(R;R_d)+W_outer max(K_NFWlike,K_env)]"
                ),
                "amplitude_rule": "A_nfw_hse=Gamma_nfw_hse median_outer_R>=Ropt(v_carrier^2)",
                "gamma_rule": (
                    "Gamma=E/(1+E), E=1_NFW_preference + E_highspin_envelope + E_edgeon"
                ),
                "rs_nfw_proxy_kpc": rs_nfw_proxy,
                "nfw_preference_load": nfw_preference_load,
                "envelope_load": envelope_load,
                "edgeon_load": edgeon_load,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "carrier_scale_outer_km2_s2": carrier_scale_outer,
                "amplitude_total_km2_s2": amplitude_total,
                "dimension_check": "PASS: A has km^2/s^2 and K is dimensionless",
                "known_limits": (
                    "no NFW preference, no high-spin envelope, or K=0 recovers carrier; "
                    "outer_window=0 leaves rapid-rise seed"
                ),
                "compact_finite_policy": "prior K_compact_finite remains diagnostic only",
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
                "gate_id": "U12506_NHSE_G1_ROUTE_AUDIT",
                "gate_status": "PASS",
                "evidence": str(route["audit_status"]),
                "remaining_obligation": "none for formula replay",
            },
            {
                "gate_id": "U12506_NHSE_G2_COMPACT_NOT_PROMOTED",
                "gate_status": "PASS",
                "evidence": "prior K_compact_finite diagnostic is not used as source label",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_NHSE_G3_NFW_RAPID_RISE_SEED",
                "gate_status": "PASS_CAVEATED",
                "evidence": "NFW preference and rapid rise source statements; R_d used as concentration proxy",
                "remaining_obligation": "source-native NFW parameters would strengthen this route",
            },
            {
                "gate_id": "U12506_NHSE_G4_DIMENSIONS_LIMITS",
                "gate_status": "PASS",
                "evidence": "A velocity-squared; K dimensionless; carrier recovery stated",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_NHSE_G5_RESIDUAL_BLIND",
                "gate_status": "PASS",
                "evidence": "construction_used_vobs_or_residual=False",
                "remaining_obligation": "vobs may enter only in replay scoring script",
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
                "formula_shell_status": "UGC12506_NFW_HSE_FORMULA_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION",
                "galaxy": GALAXY,
                "rs_nfw_proxy_kpc": rs_nfw_proxy,
                "evidence_total": evidence_total,
                "gamma_total": gamma_total,
                "amplitude_total_km2_s2": amplitude_total,
                "kernel_inner_mean_first8": float(grid["K_nfw_like_rapid_rise_highspin_envelope"].head(8).mean()),
                "kernel_outer_mean_last8": float(grid["K_nfw_like_rapid_rise_highspin_envelope"].tail(8).mean()),
                "n_gates": len(gates),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "formula_frozen_before_scoring": True,
                "control_replay_scores_allowed": True,
                "endpoint_validation_claim_allowed": False,
                "construction_used_vobs_or_residual": False,
                "next_script": "scripts/run_ugc12506_nfw_like_rapid_rise_highspin_envelope_replay.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_grid.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_summary.csv", index=False)

    report = [
        "# UGC12506 NFW-like Rapid-Rise + High-Spin Envelope Shell",
        "",
        "This shell follows the source-route audit and keeps the prior",
        "`K_compact_finite` result diagnostic-only. It uses source evidence for",
        "NFW preference, rapid rise, high spin, and extended H I envelope.",
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
    (REPORTS / "ugc12506_nfw_like_rapid_rise_highspin_envelope_shell.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
