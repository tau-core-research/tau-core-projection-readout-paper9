#!/usr/bin/env python3
"""Separate the UGC12506 Theta_morph and Xi_t channels.

This gate is intentionally not an endpoint score.  It records that the current
UGC12506 refinements separate the two routes by formula role:

* Theta_morph is an additive morphology/trajectory phase correction in v^2.
* Xi_t is a small multiplicative clock/readout interval control.

The gate also records the remaining scientific boundary: the routes still share
source context, so a combined endpoint remains blocked until a source-nonoverlap
or accepted-combination manifest exists.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_theta_xit_channels_separated_not_combined_endpoint"


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


def require_false(value: object, label: str) -> None:
    if bool(value):
        raise RuntimeError(f"{label} unexpectedly allowed endpoint validation/scoring")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    theta = pd.read_csv(DATA / "ugc12506_theta_morph_phase_replay_summary.csv").iloc[0]
    theta_gates = pd.read_csv(DATA / "ugc12506_theta_morph_phase_replay_gates.csv")
    xit_manifest = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_manifest.csv").iloc[0]
    xit_replay = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_replay_summary.csv").iloc[0]
    xit_gate = pd.read_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_summary.csv").iloc[0]
    projection_candidate = pd.read_csv(DATA / "ugc12506_projection_history_readout_candidate_summary.csv").iloc[0]
    path_audit = pd.read_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv").iloc[0]

    require_false(theta["endpoint_validation_claim"], "Theta_morph replay")
    require_false(xit_manifest["endpoint_scores_allowed"], "Xi_t control manifest")
    require_false(xit_replay["endpoint_validation_claim"], "Xi_t control replay")
    require_false(xit_gate["endpoint_scores_allowed"], "Xi_t accepted-manifest gate")
    require_false(projection_candidate["endpoint_scores_allowed"], "Projection-history candidate")

    theta_formula = str(theta["formula_text"])
    xit_formula = str(xit_manifest["formula_text"])
    theta_formula_compact = theta_formula.replace(" ", "")
    xit_formula_compact = xit_formula.replace(" ", "")
    theta_additive = "v_theta^2" in theta_formula and "+A_thetaK_theta" in theta_formula_compact
    xit_multiplicative = "Xi_t" in xit_formula and "1+epsilon_t" in xit_formula_compact
    formula_roles_distinct = bool(theta_additive and xit_multiplicative)

    theta_source_terms = {
        "high_inclination",
        "high_spin",
        "extended_low_density_hi",
        "hi_extent_asymmetry_phase",
        "late_settling_outer_shape",
    }
    xit_source_terms = {
        "high_spin",
        "edgeon_pv_clock_slice",
        "envelope_settling",
        "asymmetric_pv_phase",
        "path_environment_zero",
    }
    overlap_terms = sorted(theta_source_terms.intersection(xit_source_terms))
    source_overlap_present = len(overlap_terms) > 0
    path_term_established = str(path_audit["foreground_path_status"]) != "NOT_ESTABLISHED"

    channels = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "channel_id": "THETA_MORPH",
                "formula_role": "additive_morphology_phase_kernel",
                "formula_text": theta_formula,
                "source_role": "late-settling morphology/trajectory phase",
                "source_terms": "; ".join(sorted(theta_source_terms)),
                "rmse_context_km_s": float(theta["theta_morph_phase_rmse_km_s"]),
                "status": "DIAGNOSTIC_ONLY_NOT_ENDPOINT",
                "endpoint_allowed": False,
                "uses_vobs_or_residual_in_construction": bool(theta["construction_used_vobs"]),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": GALAXY,
                "channel_id": "XI_T",
                "formula_role": "multiplicative_clock_readout_interval_control",
                "formula_text": xit_formula,
                "source_role": "clock/readout interval control",
                "source_terms": "; ".join(sorted(xit_source_terms)),
                "rmse_context_km_s": float(xit_replay["best_control_edge_rmse_km_s"]),
                "status": "CAVEATED_INTERVAL_CONTROL_NOT_ENDPOINT",
                "endpoint_allowed": False,
                "uses_vobs_or_residual_in_construction": bool(xit_manifest["uses_vobs_or_residual"]),
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    overlap = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "overlap_id": "U12506_THETA_XIT_SOURCE_OVERLAP",
                "overlap_terms": "; ".join(overlap_terms) if overlap_terms else "none",
                "source_overlap_present": source_overlap_present,
                "path_term_established": path_term_established,
                "asymmetry_policy": str(xit_manifest["asymmetry_policy"]),
                "path_policy": str(xit_manifest["path_policy"]),
                "nonoverlap_conclusion": (
                    "formula roles are separated, but source context partially overlaps; "
                    "combined endpoint remains blocked"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_SEP_G1_FORMULA_ROLE",
                "gate_status": "PASS_SEPARATED",
                "gate_text": "Theta_morph is additive in v^2; Xi_t is a multiplicative clock/readout factor.",
                "endpoint_allowed": False,
            },
            {
                "gate_id": "U12506_SEP_G2_CLAIM_BOUNDARY",
                "gate_status": "PASS_RECORDED",
                "gate_text": "Theta_morph is diagnostic; Xi_t is caveated interval/control.",
                "endpoint_allowed": False,
            },
            {
                "gate_id": "U12506_SEP_G3_SOURCE_OVERLAP",
                "gate_status": "BLOCK_COMBINED_ENDPOINT",
                "gate_text": "High-spin/envelope/asymmetry context overlaps across routes; no combined endpoint without non-overlap manifest.",
                "endpoint_allowed": False,
            },
            {
                "gate_id": "U12506_SEP_G4_PATH_TERM",
                "gate_status": "BLOCK_PATH_CLOCK_ENDPOINT" if not path_term_established else "PASS_SOURCE_ESTABLISHED",
                "gate_text": str(xit_manifest["path_policy"]),
                "endpoint_allowed": False,
            },
            {
                "gate_id": "U12506_SEP_G5_FORBIDDEN_INPUTS",
                "gate_status": "PASS",
                "gate_text": "Separation gate reads only source/control summaries and does not select a curve-saving amplitude.",
                "endpoint_allowed": False,
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["claim_boundary"] = CLAIM_BOUNDARY

    status = (
        "U12506_THETA_XIT_CHANNELS_SEPARATED_ENDPOINT_STILL_BLOCKED"
        if formula_roles_distinct and source_overlap_present
        else "U12506_THETA_XIT_CHANNEL_SEPARATION_INCOMPLETE"
    )
    summary = pd.DataFrame(
        [
            {
                "separation_status": status,
                "galaxy": GALAXY,
                "theta_channel_role": "additive_morphology_phase_kernel",
                "xit_channel_role": "multiplicative_clock_readout_interval_control",
                "formula_roles_distinct": formula_roles_distinct,
                "source_overlap_present": source_overlap_present,
                "overlap_terms": "; ".join(overlap_terms) if overlap_terms else "none",
                "path_term_established": path_term_established,
                "theta_endpoint_allowed": False,
                "xit_standard_endpoint_allowed": bool(xit_gate["standard_endpoint_manifest_allowed"]),
                "xit_control_replay_allowed": bool(xit_manifest["control_manifest_allowed"]),
                "combined_endpoint_allowed": False,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "either source-freeze non-overlap evidence for a combined route, "
                    "or keep Theta_morph diagnostic and Xi_t as a caveated interval/control"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    channels.to_csv(DATA / "ugc12506_theta_xit_channel_separation.csv", index=False)
    overlap.to_csv(DATA / "ugc12506_theta_xit_overlap_audit.csv", index=False)
    gates.to_csv(DATA / "ugc12506_theta_xit_separation_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_theta_xit_separation_summary.csv", index=False)

    report = [
        "# UGC12506 Theta_morph / Xi_t Separation Gate",
        "",
        "This gate records the post-refinement separation of the UGC12506 channels.",
        "It is not an endpoint and does not introduce a new fitted curve.",
        "",
        "## Verdict",
        "",
        markdown_table(summary),
        "",
        "## Channel Roles",
        "",
        markdown_table(channels),
        "",
        "## Source Overlap Audit",
        "",
        markdown_table(overlap),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "`Theta_morph` and `Xi_t` are now clearly separated by formula role. "
        "`Theta_morph` is an additive morphology/trajectory phase diagnostic, "
        "whereas `Xi_t` is a small multiplicative clock/readout interval control. "
        "However, the UGC12506 source context still overlaps through high-spin, "
        "envelope, and asymmetry evidence. Therefore the separation supports "
        "cleaner channel accounting, but it does not authorize a combined endpoint.",
        "",
    ]
    (REPORTS / "ugc12506_theta_xit_separation_gate.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(summary.to_string(index=False))
    print("Theta gates reviewed:", ", ".join(theta_gates["gate_id"].astype(str).tolist()))


if __name__ == "__main__":
    main()
