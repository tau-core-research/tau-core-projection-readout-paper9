#!/usr/bin/env python3
"""Build a source-only Xi_t high-spin/envelope clock-readout shell for UGC12506.

This is a formula-shell step, not endpoint scoring.  It constructs a candidate
clock/readout factor

    Xi_t(R) = 1 + epsilon_t K_t(R)

from residual-blind UGC12506 source observables.  The foreground/path term is
set to zero because the current source audit does not establish a foreground
path object.
"""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint"


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
    m = float(np.nanmax(np.abs(x)))
    if m <= 1.0e-12:
        return x * 0.0
    return x / m


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    intake = pd.read_csv(DATA / "time_readout_xi_p1_source_review_intake.csv")
    row = intake.loc[intake["galaxy"].eq(GALAXY)].iloc[0]
    if bool(row["endpoint_scores_allowed"]):
        raise RuntimeError("P1 intake must not allow endpoint scoring")
    if row["path_term_status"] != "NOT_ESTABLISHED":
        raise RuntimeError("This shell assumes the foreground/path term is not established")

    obs = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    values = obs.set_index("symbol")["value"].to_dict()
    i_deg = float(values["i"])
    rd_kpc = float(values["R_d"])
    rhi_kpc = float(values["R_HI_source"])
    ropt_kpc = float(values["R_opt"])
    lambda_spin = float(values["lambda_spin"])
    extent_asymmetry = float(values["A_extent"])
    sigma_hi_range = float(values["Sigma_HI_range"])
    sigma_hi_unc = float(obs.set_index("symbol").loc["Sigma_HI_range", "uncertainty"])
    sigma_hi_min = max(sigma_hi_range - sigma_hi_unc, 0.0)

    grid = pd.read_csv(DATA / "ugc12506_source_native_nfw_hse_shell_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 source-native NFW-HSE shell grid")
    if bool(grid["construction_used_vobs_or_residual"].any()):
        raise RuntimeError("Input grid is not residual-blind")

    r = grid["radius_kpc"].to_numpy(dtype=float)
    span = max(rhi_kpc - rd_kpc, 1.0e-6)
    outer_window = smoothstep((r - rd_kpc) / span)
    highspin_load = float(np.clip(lambda_spin / 0.15, 0.0, 1.5))
    edgeon_load = float(np.sin(np.deg2rad(i_deg)) ** 2 * max((i_deg - 80.0) / 10.0, 0.0))
    envelope_settling_load = float(
        np.clip((rhi_kpc / max(rd_kpc, 1.0e-6) - 1.0) / 12.0, 0.0, 1.5)
        * np.clip((5.0 - sigma_hi_min) / 5.0, 0.0, 1.0)
    )
    asym_phase_load = float(0.5 * extent_asymmetry * np.sin(np.deg2rad(i_deg)) ** 2)
    path_load = 0.0

    k_spin = normalized(outer_window * np.sqrt(np.clip(r / max(rhi_kpc, 1.0e-6), 0.0, 1.0)))
    k_envelope = normalized(outer_window * np.clip((r - ropt_kpc) / max(rhi_kpc - ropt_kpc, 1.0e-6), 0.0, 1.0))
    k_asym = normalized(outer_window * np.clip((r - ropt_kpc) / max(rhi_kpc - ropt_kpc, 1.0e-6), 0.0, 1.0) ** 0.5)
    k_path = np.zeros_like(k_spin)

    load_total = max(highspin_load + edgeon_load + envelope_settling_load + asym_phase_load + path_load, 1.0e-12)
    w_spin = highspin_load / load_total
    w_edge = edgeon_load / load_total
    w_env = envelope_settling_load / load_total
    w_asym = asym_phase_load / load_total
    w_path = path_load / load_total
    k_t = normalized(w_spin * k_spin + w_edge * k_spin + w_env * k_envelope + w_asym * k_asym + w_path * k_path)

    gamma_clock = load_total / (1.0 + load_total)
    epsilon_cap = 0.035
    epsilon_t = min(epsilon_cap, 0.035 * gamma_clock)

    grid["K_t_highspin_clock_spin"] = k_spin
    grid["K_t_highspin_clock_envelope"] = k_envelope
    grid["K_t_highspin_clock_asymmetry"] = k_asym
    grid["K_t_path_environment"] = k_path
    grid["K_t_highspin_envelope_clock"] = k_t
    grid["epsilon_t_source_shell"] = epsilon_t
    grid["Xi_t_highspin_envelope_clock"] = 1.0 + epsilon_t * k_t
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_scores_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    components = pd.DataFrame(
        [
            {
                "component_id": "T_HIGHSPIN_SETTLING",
                "component_status": "INCLUDED_SOURCE_SUPPORTED",
                "source_load": highspin_load,
                "normalized_weight": w_spin,
                "kernel_column": "K_t_highspin_clock_spin",
                "source_basis": "reported high-spin state lambda=0.15",
            },
            {
                "component_id": "T_EDGEON_PV_CLOCK_SLICE",
                "component_status": "INCLUDED_SOURCE_SUPPORTED",
                "source_load": edgeon_load,
                "normalized_weight": w_edge,
                "kernel_column": "K_t_highspin_clock_spin",
                "source_basis": "high inclination and PV/envelope method required",
            },
            {
                "component_id": "T_ENVELOPE_SETTLING",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_CAVEATED",
                "source_load": envelope_settling_load,
                "normalized_weight": w_env,
                "kernel_column": "K_t_highspin_clock_envelope",
                "source_basis": "large diffuse low-density H I support",
            },
            {
                "component_id": "T_ASYMMETRIC_PV_PHASE",
                "component_status": "INCLUDED_SOURCE_SUPPORTED_CAVEATED",
                "source_load": asym_phase_load,
                "normalized_weight": w_asym,
                "kernel_column": "K_t_highspin_clock_asymmetry",
                "source_basis": "approaching/receding side shape and length asymmetry",
            },
            {
                "component_id": "T_PATH_ENVIRONMENT",
                "component_status": "EXCLUDED_NOT_ESTABLISHED",
                "source_load": path_load,
                "normalized_weight": w_path,
                "kernel_column": "K_t_path_environment",
                "source_basis": "foreground/path object evidence is not established",
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
                "formula_id": "UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL",
                "formula_text": "Xi_t(R)=1+epsilon_t K_t(R)",
                "velocity_readout_role": "v_obs^2 = Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2]",
                "kernel_text": "K_t=norm[w_spin K_spin + w_edge K_spin + w_env K_env + w_asym K_asym + 0*K_path]",
                "epsilon_rule": "epsilon_t=min(0.035, 0.035*Gamma_clock), Gamma_clock=L/(1+L)",
                "source_load_total": load_total,
                "gamma_clock": gamma_clock,
                "epsilon_t": epsilon_t,
                "path_load": path_load,
                "path_policy": "foreground/path term set to zero because path evidence is not established",
                "dimension_check": "PASS: Xi_t and K_t are dimensionless",
                "known_limits": "all source loads zero gives Xi_t=1; path evidence absent gives K_path coefficient zero",
                "formula_frozen_before_scoring": True,
                "accepted_xi_t_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "construction_used_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_XIT_G1_SOURCE_INTAKE",
                "gate_status": "PASS",
                "evidence": "P1 intake exists and endpoint is blocked",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_G2_PATH_ZERO_POLICY",
                "gate_status": "PASS",
                "evidence": "foreground/path object status is NOT_ESTABLISHED",
                "remaining_obligation": "new cone/path review required before any nonzero path term",
            },
            {
                "gate_id": "U12506_XIT_G3_DIMENSION_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "Xi_t, epsilon_t, and K_t are dimensionless; Xi_t=1 limit explicit",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_XIT_G4_ACCEPTED_MANIFEST",
                "gate_status": "BLOCKED",
                "evidence": "epsilon_t rule is a source-shell candidate, not an accepted Tau-side clock law",
                "remaining_obligation": "derive or externally review epsilon_t normalization before endpoint scoring",
            },
            {
                "gate_id": "U12506_XIT_G5_NO_ENDPOINT_SCORING",
                "gate_status": "PASS_RECORDED",
                "evidence": "no vobs/residual used; endpoint_scores_allowed=False",
                "remaining_obligation": "run only after accepted Xi_t manifest promotion",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["formula_id"] = manifest["formula_id"].iloc[0]
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "formula_id",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "formula_shell_status": "UGC12506_XI_T_SOURCE_SHELL_BUILT_ACCEPTED_MANIFEST_BLOCKED",
                "galaxy": GALAXY,
                "epsilon_t": epsilon_t,
                "source_load_total": load_total,
                "path_load": path_load,
                "accepted_xi_t_manifest_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_step": "independent review or Tau-side derivation of epsilon_t normalization; then accepted Xi_t manifest gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_grid.csv", index=False)
    components.to_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t High-Spin/Envelope Clock Shell",
            "",
            "This formula shell defines a source-only candidate `Xi_t(R)` for",
            "UGC12506. It does not score an endpoint and does not promote an",
            "accepted time-readout manifest.",
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
            "The shell is source-only and residual-blind. The foreground/path term",
            "is explicitly zero under the current source audit. The remaining blocker",
            "is the accepted origin of the `epsilon_t` normalization law.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_highspin_envelope_clock_shell.md").write_text(report, encoding="utf-8")
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
