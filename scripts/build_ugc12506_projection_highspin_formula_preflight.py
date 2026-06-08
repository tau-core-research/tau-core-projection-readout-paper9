#!/usr/bin/env python3
"""Build a fast UGC12506 projection/high-spin formula preflight.

This gate turns the cached HIghMass source context into a source-side formula
preflight.  It freezes only source-native observables and a dimensionless
prekernel; it does not freeze an amplitude, does not choose the final sign from
the rotation residual, and does not score an endpoint.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from run_source_native_readout_formula_endpoint import markdown_table


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_projection_highspin_formula_preflight_not_endpoint"


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source_summary = pd.read_csv(
        DATA / "ugc12506_highmass_fast_source_context_summary.csv"
    ).iloc[0]
    evidence = pd.read_csv(DATA / "ugc12506_highmass_fast_source_context_evidence.csv")
    queue = pd.read_csv(DATA / "projection_queue_fast_priority.csv")
    queue_row = queue.loc[queue["galaxy"].eq(GALAXY)].iloc[0]
    points = pd.read_csv(DATA / "fast_sparc_rotation_curve_packet_points.csv")
    points = points.loc[points["galaxy"].eq(GALAXY)].sort_values("radius_kpc").copy()
    galaxy_summary = pd.read_csv(DATA / "fast_sparc_rotation_curve_packet_galaxy_summary.csv")
    sparc = galaxy_summary.loc[galaxy_summary["galaxy"].eq(GALAXY)].iloc[0]

    inc_deg = float(sparc["inclination_deg"])
    projection_exposure = float(np.sin(np.deg2rad(inc_deg)) ** 2)
    rdisk_kpc = float(sparc["rdisk_kpc"])
    rhi_sparc_kpc = float(sparc["rhi_kpc"])
    rhi_source_kpc = 58.0
    rhi_source_err_kpc = 2.0
    ropt_source_kpc = 40.0
    hi_trace_beyond_kpc = 60.0
    approaching_extent_kpc = 70.0
    receding_extent_kpc = 50.0
    lambda_spin_source = 0.15
    hi_sigma_low = 1.0
    hi_sigma_high = 5.0

    asym_extent = (approaching_extent_kpc - receding_extent_kpc) / (
        approaching_extent_kpc + receding_extent_kpc
    )
    source_rhi_consistency = abs(rhi_source_kpc - rhi_sparc_kpc) / rhi_source_kpc

    observables = pd.DataFrame(
        [
            {
                "observable_id": "UGC12506_OBS_1_INCLINATION",
                "symbol": "i",
                "value": inc_deg,
                "uncertainty": float(sparc["inclination_error_deg"]),
                "unit": "deg",
                "source": "SPARC_Lelli2016c",
                "role": "projection exposure P_i=sin^2(i)",
                "freeze_status": "SOURCE_FROZEN",
            },
            {
                "observable_id": "UGC12506_OBS_2_RDISK",
                "symbol": "R_d",
                "value": rdisk_kpc,
                "uncertainty": np.nan,
                "unit": "kpc",
                "source": "SPARC_Lelli2016c",
                "role": "inner disk support scale",
                "freeze_status": "SOURCE_FROZEN",
            },
            {
                "observable_id": "UGC12506_OBS_3_RHI_SPARC",
                "symbol": "R_HI_SPARC",
                "value": rhi_sparc_kpc,
                "uncertainty": np.nan,
                "unit": "kpc",
                "source": "SPARC_Lelli2016c",
                "role": "SPARC H I support scale",
                "freeze_status": "SOURCE_FROZEN",
            },
            {
                "observable_id": "UGC12506_OBS_4_RHI_SOURCE",
                "symbol": "R_HI_source",
                "value": rhi_source_kpc,
                "uncertainty": rhi_source_err_kpc,
                "unit": "kpc",
                "source": "Hallenbeck2014_HIghMass",
                "role": "source-native H I support scale",
                "freeze_status": "SOURCE_FROZEN",
            },
            {
                "observable_id": "UGC12506_OBS_5_ROPT_SOURCE",
                "symbol": "R_opt",
                "value": ropt_source_kpc,
                "uncertainty": np.nan,
                "unit": "kpc",
                "source": "Hallenbeck2014_HIghMass",
                "role": "optical support scale",
                "freeze_status": "SOURCE_FROZEN_CONTEXT",
            },
            {
                "observable_id": "UGC12506_OBS_6_EXTENT_ASYMMETRY",
                "symbol": "A_extent",
                "value": asym_extent,
                "uncertainty": np.nan,
                "unit": "dimensionless",
                "source": "Hallenbeck2014_HIghMass",
                "role": "approaching/receding H I extent asymmetry context",
                "freeze_status": "SOURCE_DERIVED_CONTEXT",
            },
            {
                "observable_id": "UGC12506_OBS_7_SPIN",
                "symbol": "lambda_spin",
                "value": lambda_spin_source,
                "uncertainty": np.nan,
                "unit": "dimensionless",
                "source": "Hallenbeck2014_HIghMass",
                "role": "high-spin/history context",
                "freeze_status": "SOURCE_FROZEN_CONTEXT",
            },
            {
                "observable_id": "UGC12506_OBS_8_HI_SURFACE_DENSITY_RANGE",
                "symbol": "Sigma_HI_range",
                "value": hi_sigma_high,
                "uncertainty": hi_sigma_high - hi_sigma_low,
                "unit": "Msun pc^-2",
                "source": "Hallenbeck2014_HIghMass",
                "role": "low-density stable H I closure context",
                "freeze_status": "SOURCE_FROZEN_CONTEXT",
            },
        ]
    )
    observables["galaxy"] = GALAXY
    observables["uses_vobs_or_residual"] = False
    observables["endpoint_scores_allowed"] = False
    observables["claim_boundary"] = CLAIM_BOUNDARY
    observables = observables[
        [
            "galaxy",
            "observable_id",
            "symbol",
            "value",
            "uncertainty",
            "unit",
            "source",
            "role",
            "freeze_status",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    r = points["radius_kpc"].to_numpy(float)
    w_outer = smoothstep((r - rdisk_kpc) / max(rhi_source_kpc - rdisk_kpc, 1.0e-9))
    c_stable_context = np.clip((hi_sigma_high - hi_sigma_low) / 10.0, 0.0, 1.0)
    h_spin_context = np.clip((lambda_spin_source - 0.10) / 0.10, 0.0, 1.0)
    asym_context = np.clip(asym_extent / 0.25, 0.0, 1.0)
    k_pre = projection_exposure * w_outer
    k_highspin_context = k_pre * max(h_spin_context, 0.0)
    k_projection_asym_context = k_pre * max(asym_context, 0.0)
    k_stable_hi_context = k_pre * max(c_stable_context, 0.0)

    prekernel_grid = points[
        [
            "galaxy",
            "radius_kpc",
            "vobs_kms",
            "errv_kms",
            "v_baryon_050_kms",
        ]
    ].copy()
    prekernel_grid["P_i_sin2_inclination"] = projection_exposure
    prekernel_grid["W_outer_smoothstep_Rd_to_RHI_source"] = w_outer
    prekernel_grid["H_spin_context_not_amplitude"] = h_spin_context
    prekernel_grid["A_extent_context_not_amplitude"] = asym_context
    prekernel_grid["C_stable_hi_context_not_amplitude"] = c_stable_context
    prekernel_grid["K_pre_projection_outer"] = k_pre
    prekernel_grid["K_context_highspin"] = k_highspin_context
    prekernel_grid["K_context_projection_asymmetry"] = k_projection_asym_context
    prekernel_grid["K_context_stable_hi"] = k_stable_hi_context
    prekernel_grid["kernel_value_freeze_status"] = "CONTEXT_PREKERNEL_ONLY_NOT_EXECUTABLE"
    prekernel_grid["construction_used_vobs_or_residual"] = False
    prekernel_grid["endpoint_scores_allowed"] = False
    prekernel_grid["claim_boundary"] = CLAIM_BOUNDARY

    formula_shells = pd.DataFrame(
        [
            {
                "formula_id": "UGC12506_PROJECTION_HIGHS_PIN_OUTER_SUPPORT_SHELL",
                "formula_role": "preferred preflight shell",
                "formula_text": (
                    "v_readout^2(R)=v_carrier^2(R)+A_hs K_hs(R)"
                ),
                "kernel_text": (
                    "K_hs(R)=sin^2(i) W_outer(R;R_d,R_HI) "
                    "H_spin(lambda) C_stableHI"
                ),
                "sign_status": "FORMULA_CONDITIONAL_NOT_ENDPOINT_SELECTED",
                "amplitude_status": "BLOCKED_NO_SOURCE_NORMALIZED_A_hs",
                "dimension_check": "PASS if A_hs has km^2/s^2 and K_hs is dimensionless",
                "known_limits": "i=0 or W_outer=0 or A_hs=0 recovers carrier",
            },
            {
                "formula_id": "UGC12506_PROJECTION_ASYMMETRY_CONTEXT_SHELL",
                "formula_role": "secondary preflight shell",
                "formula_text": (
                    "v_readout^2(R)=v_carrier^2(R)+A_pa K_pa(R)"
                ),
                "kernel_text": (
                    "K_pa(R)=sin^2(i) W_outer(R;R_d,R_HI) A_extent"
                ),
                "sign_status": "FORMULA_CONDITIONAL_NOT_ENDPOINT_SELECTED",
                "amplitude_status": "BLOCKED_NO_SOURCE_NORMALIZED_A_pa",
                "dimension_check": "PASS if A_pa has km^2/s^2 and K_pa is dimensionless",
                "known_limits": "zero asymmetry or zero amplitude recovers carrier",
            },
        ]
    )
    formula_shells["galaxy"] = GALAXY
    formula_shells["uses_vobs_or_residual_in_derivation"] = False
    formula_shells["formula_freeze_allowed"] = False
    formula_shells["endpoint_scores_allowed"] = False
    formula_shells["claim_boundary"] = CLAIM_BOUNDARY
    formula_shells = formula_shells[
        [
            "galaxy",
            "formula_id",
            "formula_role",
            "formula_text",
            "kernel_text",
            "sign_status",
            "amplitude_status",
            "dimension_check",
            "known_limits",
            "uses_vobs_or_residual_in_derivation",
            "formula_freeze_allowed",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    gates = pd.DataFrame(
        [
            {
                "gate_id": "UGC12506_PHF_G1_SOURCE_CONTEXT",
                "gate_status": "PASS_SOURCE_CONTEXT_CACHED",
                "evidence": str(source_summary["context_status"]),
                "remaining_obligation": "none for context cache",
            },
            {
                "gate_id": "UGC12506_PHF_G2_ROTATION_PACKET",
                "gate_status": "PASS_ROTATION_PACKET_READY",
                "evidence": (
                    f"n={len(points)} points; fast priority rank={int(queue_row['fast_priority_rank'])}"
                ),
                "remaining_obligation": "do not use residual gap for label or amplitude",
            },
            {
                "gate_id": "UGC12506_PHF_G3_SOURCE_OBSERVABLES",
                "gate_status": "PASS_PARTIAL_SOURCE_OBSERVABLES_FROZEN",
                "evidence": "inclination, R_d, R_HI, R_opt, extent asymmetry, spin context, H I density context",
                "remaining_obligation": "extract or derive normalized active loads",
            },
            {
                "gate_id": "UGC12506_PHF_G4_PREKERNEL",
                "gate_status": "PASS_CONTEXT_PREKERNEL_BUILT",
                "evidence": "dimensionless K_pre and context kernels are built on SPARC radial grid",
                "remaining_obligation": "not executable until amplitude/load rule is frozen",
            },
            {
                "gate_id": "UGC12506_PHF_G5_AMPLITUDE",
                "gate_status": "BLOCKED_NO_SOURCE_NORMALIZED_AMPLITUDE",
                "evidence": "A_hs and A_pa are not source-normalized",
                "remaining_obligation": "derive amplitude from source/Tau-side scale, not from observed residual",
            },
            {
                "gate_id": "UGC12506_PHF_G6_SIGN",
                "gate_status": "BLOCKED_SIGN_NOT_ENDPOINT_SELECTED",
                "evidence": "source suggests projection/high-spin context but not a final sign convention",
                "remaining_obligation": "derive sign from readout theorem or freeze both branches as controls",
            },
            {
                "gate_id": "UGC12506_PHF_G7_ENDPOINT",
                "gate_status": "BLOCKED_ENDPOINT_NOT_ALLOWED",
                "evidence": "formula is preflight only; no endpoint scoring here",
                "remaining_obligation": "freeze amplitude/sign/label before endpoint",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
    gates["formula_freeze_allowed"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "uses_vobs_or_residual",
            "formula_freeze_allowed",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "preflight_status": "UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED",
                "galaxy": GALAXY,
                "source_context_cached": True,
                "rotation_packet_ready": True,
                "source_observables_frozen": True,
                "context_prekernel_built": True,
                "rhi_source_kpc": rhi_source_kpc,
                "rhi_sparc_kpc": rhi_sparc_kpc,
                "source_rhi_consistency_fraction": source_rhi_consistency,
                "projection_exposure_sin2_i": projection_exposure,
                "extent_asymmetry": asym_extent,
                "lambda_spin_source": lambda_spin_source,
                "formula_freeze_allowed": False,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_preflight": False,
                "recommended_next_gate": "derive_ugc12506_source_normalized_highspin_amplitude_or_freeze_control_branches",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    observables.to_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv", index=False)
    prekernel_grid.to_csv(DATA / "ugc12506_projection_highspin_preflight_kernel_grid.csv", index=False)
    formula_shells.to_csv(DATA / "ugc12506_projection_highspin_preflight_formula_shells.csv", index=False)
    gates.to_csv(DATA / "ugc12506_projection_highspin_preflight_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_projection_highspin_preflight_summary.csv", index=False)

    report = [
        "# UGC12506 Projection/High-Spin Formula Preflight",
        "",
        "`UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED`",
        "",
        "This is a fast source-side formula preflight.  It freezes source-native",
        "observables and builds dimensionless context prekernels, but it does not",
        "freeze a nonzero executable formula and does not score an endpoint.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source-Frozen Observables",
        "",
        markdown_table(observables),
        "",
        "## Formula Shells",
        "",
        markdown_table(formula_shells),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Evidence Used",
        "",
        markdown_table(evidence[["galaxy", "evidence_id", "evidence_type", "paraphrased_evidence"]]),
        "",
        "## Claim Boundary",
        "",
        "The prekernel uses no endpoint residuals and no fitted amplitude.  The",
        "observed rotation curve is present in the grid only for provenance and",
        "future scoring.  The active UGC12506 endpoint remains blocked until a",
        "source-normalized amplitude/sign rule and label gate are frozen.",
    ]
    (REPORTS / "ugc12506_projection_highspin_formula_preflight.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
