#!/usr/bin/env python3
"""Build a source-normalized amplitude prefreeze for UGC12506.

This is a fast, claim-bounded attempt to turn UGC12506 source context into a
candidate amplitude rule without using the observed rotation residual.  It
freezes a provisional source-normalized amplitude for future control/replay, but
does not run endpoint scoring and does not claim validation.
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
CLAIM_BOUNDARY = "ugc12506_source_normalized_amplitude_prefreeze_not_endpoint"


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    preflight = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_summary.csv").iloc[0]
    grid = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_kernel_grid.csv")

    outer = grid.loc[grid["radius_kpc"].ge(float(preflight["rhi_source_kpc"]) * 0.5)].copy()
    if outer.empty:
        outer = grid.copy()

    # Protocol constants are declared here so this remains auditable.  They are
    # source-normalization constants, not fitted endpoint parameters.
    lambda_reference_high_spin = 0.10
    hi_surface_density_norm = 10.0
    source_load_denominator_offset = 1.0

    lambda_spin = float(preflight["lambda_spin_source"])
    projection_exposure = float(preflight["projection_exposure_sin2_i"])
    extent_asymmetry = float(preflight["extent_asymmetry"])

    # The stability context came from the preflight grid as a source-context
    # scalar, not from the endpoint residual.
    c_stable = float(grid["C_stable_hi_context_not_amplitude"].iloc[0])
    h_spin_excess = max((lambda_spin - lambda_reference_high_spin) / lambda_reference_high_spin, 0.0)
    asym_load = max(extent_asymmetry / 0.25, 0.0)

    source_load_hs = projection_exposure * h_spin_excess * c_stable
    source_load_asym = projection_exposure * asym_load
    gamma_hs = source_load_hs / (source_load_denominator_offset + source_load_hs)
    gamma_asym = source_load_asym / (source_load_denominator_offset + source_load_asym)

    carrier_scale_outer = float(np.median(outer["v_baryon_050_kms"].astype(float) ** 2))
    amplitude_hs = gamma_hs * carrier_scale_outer
    amplitude_asym = gamma_asym * carrier_scale_outer

    rules = pd.DataFrame(
        [
            {
                "rule_id": "UGC12506_AMP_RULE_HIGHS_PIN",
                "rule_status": "PREFROZEN_FOR_CONTROL_REPLAY_NOT_VALIDATION",
                "formula": "A_hs = Gamma_hs * median_outer(v_baryon_050^2)",
                "source_load_formula": (
                    "E_hs=sin^2(i)*max((lambda_spin-0.10)/0.10,0)*C_stableHI"
                ),
                "gamma_formula": "Gamma_hs=E_hs/(1+E_hs)",
                "source_load": source_load_hs,
                "gamma": gamma_hs,
                "carrier_scale_km2_s2": carrier_scale_outer,
                "amplitude_km2_s2": amplitude_hs,
                "sign_options_for_future_controls": "positive_added_readout;negative_attenuation_control",
                "uses_vobs_or_residual": False,
            },
            {
                "rule_id": "UGC12506_AMP_RULE_ASYMMETRY",
                "rule_status": "PREFROZEN_FOR_CONTROL_REPLAY_NOT_VALIDATION",
                "formula": "A_pa = Gamma_pa * median_outer(v_baryon_050^2)",
                "source_load_formula": "E_pa=sin^2(i)*max(A_extent/0.25,0)",
                "gamma_formula": "Gamma_pa=E_pa/(1+E_pa)",
                "source_load": source_load_asym,
                "gamma": gamma_asym,
                "carrier_scale_km2_s2": carrier_scale_outer,
                "amplitude_km2_s2": amplitude_asym,
                "sign_options_for_future_controls": "positive_added_readout;negative_attenuation_control",
                "uses_vobs_or_residual": False,
            },
        ]
    )
    rules["galaxy"] = GALAXY
    rules["endpoint_scores_allowed"] = False
    rules["claim_boundary"] = CLAIM_BOUNDARY
    rules = rules[
        [
            "galaxy",
            "rule_id",
            "rule_status",
            "formula",
            "source_load_formula",
            "gamma_formula",
            "source_load",
            "gamma",
            "carrier_scale_km2_s2",
            "amplitude_km2_s2",
            "sign_options_for_future_controls",
            "uses_vobs_or_residual",
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    replay_grid = grid.copy()
    replay_grid["A_hs_prefrozen_km2_s2"] = amplitude_hs
    replay_grid["A_pa_prefrozen_km2_s2"] = amplitude_asym
    replay_grid["v2_carrier_km2_s2"] = replay_grid["v_baryon_050_kms"] ** 2
    replay_grid["v2_hs_positive_control_km2_s2"] = (
        replay_grid["v2_carrier_km2_s2"]
        + amplitude_hs * replay_grid["K_context_highspin"]
    )
    replay_grid["v2_hs_negative_control_km2_s2"] = np.maximum(
        replay_grid["v2_carrier_km2_s2"]
        - amplitude_hs * replay_grid["K_context_highspin"],
        0.0,
    )
    replay_grid["v2_asym_positive_control_km2_s2"] = (
        replay_grid["v2_carrier_km2_s2"]
        + amplitude_asym * replay_grid["K_context_projection_asymmetry"]
    )
    replay_grid["v_hs_positive_control_kms"] = np.sqrt(
        np.maximum(replay_grid["v2_hs_positive_control_km2_s2"], 0.0)
    )
    replay_grid["v_hs_negative_control_kms"] = np.sqrt(
        np.maximum(replay_grid["v2_hs_negative_control_km2_s2"], 0.0)
    )
    replay_grid["v_asym_positive_control_kms"] = np.sqrt(
        np.maximum(replay_grid["v2_asym_positive_control_km2_s2"], 0.0)
    )
    replay_grid["prefreeze_used_vobs_or_residual"] = False
    replay_grid["endpoint_scores_allowed"] = False
    replay_grid["claim_boundary"] = CLAIM_BOUNDARY

    gates = pd.DataFrame(
        [
            {
                "gate_id": "UGC12506_AMP_G1_PREFLIGHT",
                "gate_status": "PASS_PREFLIGHT_AVAILABLE",
                "evidence": str(preflight["preflight_status"]),
                "remaining_obligation": "none for preflight",
            },
            {
                "gate_id": "UGC12506_AMP_G2_SOURCE_LOAD",
                "gate_status": "PASS_SOURCE_LOAD_DECLARED",
                "evidence": "projection, high-spin, stability, and asymmetry loads use source-side observables",
                "remaining_obligation": "audit protocol constants before endpoint use",
            },
            {
                "gate_id": "UGC12506_AMP_G3_DIMENSIONS",
                "gate_status": "PASS_DIMENSIONAL_CHECK",
                "evidence": "Gamma dimensionless; median outer carrier scale supplies km^2/s^2",
                "remaining_obligation": "none at prefreeze level",
            },
            {
                "gate_id": "UGC12506_AMP_G4_SIGN",
                "gate_status": "BLOCKED_SIGN_TO_BE_CONTROL_REPLAYED",
                "evidence": "positive and negative branches are frozen as future controls, not selected here",
                "remaining_obligation": "run both branches in a separate scoring script if endpoint gates pass",
            },
            {
                "gate_id": "UGC12506_AMP_G5_ENDPOINT",
                "gate_status": "BLOCKED_ENDPOINT_NOT_ALLOWED",
                "evidence": "this script does not score vobs and does not claim validation",
                "remaining_obligation": "label gate and replay protocol required before scoring",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["uses_vobs_or_residual"] = False
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
            "endpoint_scores_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "amplitude_prefreeze_status": "UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT",
                "galaxy": GALAXY,
                "highspin_source_load": source_load_hs,
                "highspin_gamma": gamma_hs,
                "highspin_amplitude_km2_s2": amplitude_hs,
                "asymmetry_source_load": source_load_asym,
                "asymmetry_gamma": gamma_asym,
                "asymmetry_amplitude_km2_s2": amplitude_asym,
                "carrier_scale_outer_km2_s2": carrier_scale_outer,
                "formula_prefreeze_allowed_for_future_controls": True,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual_in_prefreeze": False,
                "recommended_next_gate": "run_ugc12506_prefrozen_branch_replay_controls_after_label_gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    rules.to_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_rules.csv", index=False)
    replay_grid.to_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_grid.csv", index=False)
    gates.to_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_summary.csv", index=False)

    report = [
        "# UGC12506 Source-Normalized Amplitude Prefreeze",
        "",
        "`UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT`",
        "",
        "This gate freezes a source-normalized amplitude rule for future control",
        "replay.  It does not score the endpoint and does not select the final sign",
        "from the observed residual.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Rules",
        "",
        markdown_table(rules),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Claim Boundary",
        "",
        "The amplitude is built from source-side projection/high-spin/stability",
        "context and the baryonic carrier scale.  It is ready for future branch",
        "control replay only after the label gate is resolved.  It is not a",
        "validation result.",
    ]
    (REPORTS / "ugc12506_source_normalized_amplitude_prefreeze.md").write_text(
        "\n".join(report) + "\n", encoding="utf-8"
    )

    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
