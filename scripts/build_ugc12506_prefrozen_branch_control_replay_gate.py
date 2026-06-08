#!/usr/bin/env python3
"""Build the UGC12506 prefrozen-branch control replay gate.

This gate does not promote UGC12506 to a population-validation endpoint.  It
only checks whether the source-cached high-spin/projection preflight and the
source-normalized amplitude prefreeze are internally consistent enough for a
separate scoring script to replay the frozen branches.  The scoring script is
the only step allowed to read vobs.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_prefrozen_branch_control_replay_gate_not_validation"


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


def load_first(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError(f"Empty required input: {path}")
    return df.iloc[0]


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    source = load_first(DATA / "ugc12506_highmass_fast_source_context_summary.csv")
    preflight = load_first(DATA / "ugc12506_projection_highspin_preflight_summary.csv")
    prefreeze = load_first(DATA / "ugc12506_source_normalized_amplitude_prefreeze_summary.csv")
    rules = pd.read_csv(DATA / "ugc12506_source_normalized_amplitude_prefreeze_rules.csv")

    source_cached = bool(source["source_cached"])
    source_no_curve_use = not bool(source["uses_vobs_or_residual_in_acquisition"])
    preflight_ready = bool(preflight["source_observables_frozen"]) and bool(
        preflight["context_prekernel_built"]
    )
    preflight_blind = not bool(preflight["uses_vobs_or_residual_in_preflight"])
    amplitude_ready = bool(prefreeze["formula_prefreeze_allowed_for_future_controls"])
    amplitude_blind = not bool(prefreeze["uses_vobs_or_residual_in_prefreeze"])
    sign_not_selected = set(rules["sign_options_for_future_controls"].unique()) == {
        "positive_added_readout;negative_attenuation_control"
    }
    dimensions_ready = (
        float(prefreeze["highspin_amplitude_km2_s2"]) > 0
        and float(prefreeze["asymmetry_amplitude_km2_s2"]) > 0
    )

    replay_allowed = bool(
        source_cached
        and source_no_curve_use
        and preflight_ready
        and preflight_blind
        and amplitude_ready
        and amplitude_blind
        and sign_not_selected
        and dimensions_ready
    )

    manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "replay_formula_manifest_id": "UGC12506_PREFROZEN_HIGHS_PIN_PROJECTION_BRANCH_REPLAY",
                "source_context_status": str(source["context_status"]),
                "preflight_status": str(preflight["preflight_status"]),
                "amplitude_prefreeze_status": str(prefreeze["amplitude_prefreeze_status"]),
                "preferred_branch_family": "K_projection_highspin_outer_support",
                "secondary_branch_family": "K_projection_asymmetry_outer_support",
                "carrier_column": "v_baryon_050_kms",
                "highspin_kernel_column": "K_context_highspin",
                "asymmetry_kernel_column": "K_context_projection_asymmetry",
                "highspin_amplitude_km2_s2": float(prefreeze["highspin_amplitude_km2_s2"]),
                "asymmetry_amplitude_km2_s2": float(prefreeze["asymmetry_amplitude_km2_s2"]),
                "sign_policy": (
                    "both positive added-readout and negative attenuation branches "
                    "must be replayed; sign is not endpoint-selected here"
                ),
                "control_replay_scores_allowed": replay_allowed,
                "endpoint_validation_claim_allowed": False,
                "population_validation_claim_allowed": False,
                "uses_vobs_or_residual_in_gate": False,
                "posthoc_retuning_allowed": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_CR1_SOURCE_CONTEXT_CACHED",
                "gate_status": "PASS" if source_cached else "BLOCKED",
                "evidence": str(source["context_status"]),
                "remaining_obligation": "none for control replay",
            },
            {
                "gate_id": "U12506_CR2_SOURCE_CONTEXT_RESIDUAL_BLIND",
                "gate_status": "PASS" if source_no_curve_use else "BLOCKED",
                "evidence": (
                    "uses_vobs_or_residual_in_acquisition="
                    f"{bool(source['uses_vobs_or_residual_in_acquisition'])}"
                ),
                "remaining_obligation": "source acquisition must remain independent of endpoint residuals",
            },
            {
                "gate_id": "U12506_CR3_PREFLIGHT_READY",
                "gate_status": "PASS" if preflight_ready else "BLOCKED",
                "evidence": str(preflight["preflight_status"]),
                "remaining_obligation": "all source observables and context kernels must be present",
            },
            {
                "gate_id": "U12506_CR4_PREFLIGHT_RESIDUAL_BLIND",
                "gate_status": "PASS" if preflight_blind else "BLOCKED",
                "evidence": f"uses_vobs_or_residual_in_preflight={bool(preflight['uses_vobs_or_residual_in_preflight'])}",
                "remaining_obligation": "vobs may enter only in the scoring script",
            },
            {
                "gate_id": "U12506_CR5_AMPLITUDE_PREFROZEN",
                "gate_status": "PASS" if amplitude_ready and dimensions_ready else "BLOCKED",
                "evidence": str(prefreeze["amplitude_prefreeze_status"]),
                "remaining_obligation": "amplitudes must have velocity-squared units and be positive",
            },
            {
                "gate_id": "U12506_CR6_AMPLITUDE_RESIDUAL_BLIND",
                "gate_status": "PASS" if amplitude_blind else "BLOCKED",
                "evidence": f"uses_vobs_or_residual_in_prefreeze={bool(prefreeze['uses_vobs_or_residual_in_prefreeze'])}",
                "remaining_obligation": "no observed residual may determine amplitude",
            },
            {
                "gate_id": "U12506_CR7_SIGN_BRANCHES_NOT_SELECTED",
                "gate_status": "PASS_CAVEATED" if sign_not_selected else "BLOCKED",
                "evidence": "; ".join(rules["sign_options_for_future_controls"].astype(str).unique()),
                "remaining_obligation": "score both signs as controls; do not promote sign from this gate",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["control_replay_scores_allowed"] = replay_allowed
    gates["endpoint_validation_claim_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY
    gates = gates[
        [
            "galaxy",
            "gate_id",
            "gate_status",
            "evidence",
            "remaining_obligation",
            "control_replay_scores_allowed",
            "endpoint_validation_claim_allowed",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "control_replay_gate_status": (
                    "UGC12506_PREFROZEN_BRANCH_CONTROL_REPLAY_ALLOWED_NOT_VALIDATION"
                    if replay_allowed
                    else "UGC12506_PREFROZEN_BRANCH_CONTROL_REPLAY_BLOCKED"
                ),
                "galaxy": GALAXY,
                "n_gates": len(gates),
                "n_pass_like": int(gates["gate_status"].str.startswith("PASS").sum()),
                "n_blocked": int(gates["gate_status"].eq("BLOCKED").sum()),
                "n_caveated": int(gates["gate_status"].eq("PASS_CAVEATED").sum()),
                "control_replay_scores_allowed": replay_allowed,
                "endpoint_validation_claim_allowed": False,
                "population_validation_claim_allowed": False,
                "next_script": "scripts/run_ugc12506_prefrozen_branch_replay_controls.py",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    manifest.to_csv(DATA / "ugc12506_prefrozen_branch_control_replay_gate_manifest.csv", index=False)
    gates.to_csv(DATA / "ugc12506_prefrozen_branch_control_replay_gate_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_prefrozen_branch_control_replay_gate_summary.csv", index=False)

    report = [
        "# UGC12506 Prefrozen Branch Control Replay Gate",
        "",
        "This gate allows a caveated single-galaxy control replay of the",
        "source-frozen high-spin/projection branches. It does not promote a",
        "population-validation endpoint and it does not select the sign from",
        "the rotation residual.",
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
        "The replay may read `vobs` only in the separate scoring script. The",
        "result must be reported as a prefrozen branch control replay, not as",
        "accepted population validation.",
        "",
    ]
    (REPORTS / "ugc12506_prefrozen_branch_control_replay_gate.md").write_text(
        "\n".join(report), encoding="utf-8"
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
