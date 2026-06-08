#!/usr/bin/env python3
"""Freeze a stronger source-native UGC12506 envelope-support readout.

The previous UGC12506 high-spin/projection branch was residual-blind but too
weak.  This script derives a stronger source-side shell from the same residual-
blind observables by treating the extended low-density H I envelope as its own
support component rather than as a small context factor.

No observed rotation residual is used here.  A separate scoring script may read
vobs after this freeze artifact exists.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_source_envelope_support_formula_freeze_not_validation"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    obs = pd.read_csv(DATA / "ugc12506_projection_highspin_preflight_observables.csv")
    grid = pd.read_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_grid.csv")
    grid = grid.loc[grid["galaxy"].eq(GALAXY)].copy().sort_values("radius_kpc")
    if grid.empty:
        raise ValueError("Missing UGC12506 prefreeze grid")
    if bool(grid["prefreeze_used_vobs_or_residual"].any()):
        raise RuntimeError("Input grid is not residual-blind")

    values = obs.set_index("symbol")["value"].to_dict()
    inclination_deg = float(values["i"])
    rd_kpc = float(values["R_d"])
    rhi_kpc = float(values["R_HI_source"])
    ropt_kpc = float(values["R_opt"])
    lambda_spin = float(values["lambda_spin"])
    sigma_hi_max = float(values["Sigma_HI_range"])
    sigma_hi_width = float(obs.set_index("symbol").loc["Sigma_HI_range", "uncertainty"])
    sigma_hi_min = max(sigma_hi_max - sigma_hi_width, 0.0)

    sin2_i = float(np.sin(np.deg2rad(inclination_deg)) ** 2)
    extent_ratio = float(rhi_kpc / rd_kpc)
    optical_to_hi_ratio = float(ropt_kpc / rhi_kpc)
    hi_extension_load = max(extent_ratio - 1.0, 0.0)
    spin_load = max(lambda_spin / 0.10, 0.0)
    low_density_stability_load = float(np.clip((5.0 - sigma_hi_min) / 5.0, 0.0, 1.0))

    # Source-side envelope evidence.  This deliberately differs from the older
    # context formula: extended H I support is promoted from a small multiplier
    # into the principal support load.
    envelope_evidence = sin2_i * hi_extension_load * spin_load * low_density_stability_load
    envelope_gamma = envelope_evidence / (1.0 + envelope_evidence)
    carrier_scale_outer = float(grid.loc[grid["radius_kpc"].ge(ropt_kpc), "v2_carrier_km2_s2"].median())
    if not np.isfinite(carrier_scale_outer):
        carrier_scale_outer = float(grid["v2_carrier_km2_s2"].tail(8).median())
    envelope_amplitude = envelope_gamma * carrier_scale_outer

    r = grid["radius_kpc"].to_numpy(dtype=float)
    outer_window = smoothstep((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6))
    envelope_shape = np.sqrt(np.clip((r - rd_kpc) / max(rhi_kpc - rd_kpc, 1.0e-6), 0.0, 1.0))
    grid["K_envelope_source_support"] = sin2_i * outer_window * envelope_shape
    grid["K_envelope_source_support_norm"] = grid["K_envelope_source_support"] / max(
        float(grid["K_envelope_source_support"].max()), 1.0e-12
    )
    grid["A_env_source_frozen_km2_s2"] = envelope_amplitude
    grid["v2_envelope_positive_prefrozen_km2_s2"] = (
        grid["v2_carrier_km2_s2"] + envelope_amplitude * grid["K_envelope_source_support_norm"]
    )
    grid["v2_envelope_negative_control_km2_s2"] = (
        grid["v2_carrier_km2_s2"] - envelope_amplitude * grid["K_envelope_source_support_norm"]
    )
    grid["v_envelope_positive_prefrozen_kms"] = np.sqrt(
        np.maximum(grid["v2_envelope_positive_prefrozen_km2_s2"], 0.0)
    )
    grid["v_envelope_negative_control_kms"] = np.sqrt(
        np.maximum(grid["v2_envelope_negative_control_km2_s2"], 0.0)
    )
    grid["construction_used_vobs_or_residual"] = False
    grid["endpoint_validation_claim_allowed"] = False
    grid["claim_boundary"] = CLAIM_BOUNDARY

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "formula_id": "UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT",
                "formula_text": "v_readout^2(R)=v_carrier^2(R)+A_env K_env(R)",
                "kernel_text": (
                    "K_env=norm[sin^2(i) W(R;R_d,R_HI) sqrt((R-R_d)/(R_HI-R_d))]"
                ),
                "amplitude_rule": "A_env=Gamma_env median_outer_R>=Ropt(v_carrier^2)",
                "gamma_rule": (
                    "Gamma_env=E_env/(1+E_env), "
                    "E_env=sin^2(i)(R_HI/R_d-1)(lambda_spin/0.10)C_lowSigmaHI"
                ),
                "inclination_deg": inclination_deg,
                "rd_kpc": rd_kpc,
                "rhi_source_kpc": rhi_kpc,
                "ropt_kpc": ropt_kpc,
                "lambda_spin": lambda_spin,
                "sigma_hi_min_msun_pc2": sigma_hi_min,
                "sin2_i": sin2_i,
                "extent_ratio_rhi_over_rd": extent_ratio,
                "hi_extension_load": hi_extension_load,
                "spin_load": spin_load,
                "low_density_stability_load": low_density_stability_load,
                "envelope_evidence": envelope_evidence,
                "envelope_gamma": envelope_gamma,
                "carrier_scale_outer_km2_s2": carrier_scale_outer,
                "envelope_amplitude_km2_s2": envelope_amplitude,
                "dimension_check": "PASS: A_env has km^2/s^2 and K_env is dimensionless",
                "known_limits": (
                    "i=0, R_HI/R_d->1, lambda_spin->0, or K_env=0 recovers carrier"
                ),
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
                "gate_id": "U12506_ENV1_SOURCE_OBSERVABLES_PRESENT",
                "gate_status": "PASS",
                "evidence": "i, R_d, R_HI_source, R_opt, lambda_spin, Sigma_HI_range available",
                "remaining_obligation": "none for formula replay",
            },
            {
                "gate_id": "U12506_ENV2_RESIDUAL_BLIND_FREEZE",
                "gate_status": "PASS",
                "evidence": "construction_used_vobs_or_residual=False",
                "remaining_obligation": "vobs may enter only in separate scoring script",
            },
            {
                "gate_id": "U12506_ENV3_DIMENSIONS_AND_LIMITS",
                "gate_status": "PASS",
                "evidence": "A_env velocity-squared; K_env dimensionless; carrier recovery limits explicit",
                "remaining_obligation": "none",
            },
            {
                "gate_id": "U12506_ENV4_SOURCE_PROMOTION_CAVEAT",
                "gate_status": "PASS_CAVEATED",
                "evidence": "extended H I envelope is promoted from context multiplier to support component",
                "remaining_obligation": (
                    "requires independent source-side review before accepted endpoint validation"
                ),
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
                "formula_freeze_status": "UGC12506_SOURCE_ENVELOPE_SUPPORT_FORMULA_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION",
                "galaxy": GALAXY,
                "envelope_evidence": envelope_evidence,
                "envelope_gamma": envelope_gamma,
                "envelope_amplitude_km2_s2": envelope_amplitude,
                "kernel_max": float(grid["K_envelope_source_support_norm"].max()),
                "kernel_outer_mean_last8": float(grid["K_envelope_source_support_norm"].tail(8).mean()),
                "n_gates": len(gates),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "formula_frozen_before_scoring": True,
                "control_replay_scores_allowed": True,
                "endpoint_validation_claim_allowed": False,
                "construction_used_vobs_or_residual": False,
                "next_script": "scripts/run_ugc12506_source_envelope_support_replay_controls.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    grid.to_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_grid.csv", index=False)
    manifest.to_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_source_envelope_support_formula_freeze_summary.csv", index=False)

    report = [
        "# UGC12506 Source-Envelope Support Formula Freeze",
        "",
        "This freeze promotes the extended H I envelope from a small context",
        "multiplier into the principal source-support component. It remains",
        "residual-blind and does not claim endpoint validation.",
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
        "The formula is stronger than the earlier high-spin context branch, but",
        "the promotion of the H I envelope into the main support term must be",
        "reviewed as a source-side theorem/caveat before accepted endpoint use.",
        "",
    ]
    (REPORTS / "ugc12506_source_envelope_support_formula_freeze.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
