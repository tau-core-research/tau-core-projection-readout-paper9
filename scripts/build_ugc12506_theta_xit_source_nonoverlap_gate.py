#!/usr/bin/env python3
"""Build a source-nonoverlap ledger for UGC12506 Theta_morph vs Xi_t.

The previous gate separated the two routes by formula role.  This gate asks a
stricter question: which source observables may be assigned uniquely to
Theta_morph, which may be assigned uniquely to Xi_t, and which remain shared
context that cannot support a combined endpoint without double-count controls.

No rotation residuals or endpoint scores are used.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint"


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


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    separation = pd.read_csv(DATA / "ugc12506_theta_xit_separation_summary.csv").iloc[0]
    theta = pd.read_csv(DATA / "ugc12506_theta_morph_phase_replay_summary.csv").iloc[0]
    xit = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_manifest.csv").iloc[0]
    xit_components = pd.read_csv(DATA / "ugc12506_xi_t_caveated_interval_control_components.csv")
    path_audit = pd.read_csv(DATA / "ugc12506_observer_path_interloper_audit_summary.csv").iloc[0]

    if not bool(separation["formula_roles_distinct"]):
        raise RuntimeError("Cannot build source-nonoverlap gate before formula-role separation")
    if bool(separation["combined_endpoint_allowed"]):
        raise RuntimeError("Separation gate should not already allow a combined endpoint")
    if bool(theta["construction_used_vobs"]) or bool(xit["uses_vobs_or_residual"]):
        raise RuntimeError("Input channels are not residual-blind")

    ledger_rows = [
        {
            "source_observable": "high_spin_lambda",
            "source_basis": "reported high-spin state lambda=0.15",
            "theta_role": "phase_load_context",
            "xit_role": "core_clock_load_component",
            "assignment": "SHARED_CONTEXT_NOT_INDEPENDENT",
            "double_count_risk": "HIGH",
            "allowed_in_combined_control": "context_only_do_not_sum_twice",
            "endpoint_permission": False,
            "reason": "the same high-spin evidence supports both late-settling morphology phase and clock-load route",
        },
        {
            "source_observable": "extended_low_density_hi_envelope",
            "source_basis": "large diffuse low-density H I support",
            "theta_role": "outer_late_settling_shape_and_load",
            "xit_role": "envelope_settling_interval_component",
            "assignment": "PARTIALLY_SHARED_NEEDS_SPLIT",
            "double_count_risk": "MEDIUM",
            "allowed_in_combined_control": "split_shape_vs_clock_interval_only",
            "endpoint_permission": False,
            "reason": "outer H I can define a morphology phase shape, but its settling interpretation also enters Xi_t",
        },
        {
            "source_observable": "high_inclination_edge_on_pv_geometry",
            "source_basis": "high inclination and PV/envelope method required",
            "theta_role": "projection_history_base_context",
            "xit_role": "edgeon_pv_clock_slice",
            "assignment": "PARTIALLY_SHARED_NEEDS_SPLIT",
            "double_count_risk": "MEDIUM",
            "allowed_in_combined_control": "geometry_mask_for_theta_or_clock_slice_not_both_as_amplitude",
            "endpoint_permission": False,
            "reason": "edge-on geometry is necessary context for both readout visibility and clock-slice interpretation",
        },
        {
            "source_observable": "approaching_receding_hi_asymmetry",
            "source_basis": "approaching/receding side shape and length asymmetry",
            "theta_role": "morphology_phase_component",
            "xit_role": "caveated_phase_component_not_standalone",
            "assignment": "THETA_PRIMARY_XIT_CAVEATED_PHASE_ONLY",
            "double_count_risk": "MEDIUM",
            "allowed_in_combined_control": "theta_primary_xit_phase_caveat_only",
            "endpoint_permission": False,
            "reason": "review policy already forbids asymmetry as a standalone Xi_t route driver",
        },
        {
            "source_observable": "late_settling_outer_radial_shape",
            "source_basis": "Theta_morph late-settling outer-window construction",
            "theta_role": "primary_kernel_shape",
            "xit_role": "none",
            "assignment": "THETA_ONLY",
            "double_count_risk": "LOW",
            "allowed_in_combined_control": "theta_channel_only",
            "endpoint_permission": False,
            "reason": "this is a morphology-state shape assignment, not a clock/readout scale",
        },
        {
            "source_observable": "epsilon_t_cap_protocol",
            "source_basis": str(xit["cap_policy"]),
            "theta_role": "none",
            "xit_role": "clock_interval_bound",
            "assignment": "XIT_ONLY_PROTOCOL_CAP",
            "double_count_risk": "LOW",
            "allowed_in_combined_control": "xit_interval_bound_only",
            "endpoint_permission": False,
            "reason": "cap controls the small clock interval and is not a morphology amplitude",
        },
        {
            "source_observable": "foreground_path_environment",
            "source_basis": str(xit["path_policy"]),
            "theta_role": "none",
            "xit_role": "excluded_zero_path_term",
            "assignment": "EXCLUDED_UNTIL_SOURCE_PATH_REVIEW",
            "double_count_risk": "LOW",
            "allowed_in_combined_control": "zero_only",
            "endpoint_permission": False,
            "reason": "path/environment evidence is not established",
        },
    ]
    ledger = pd.DataFrame(ledger_rows)
    ledger["galaxy"] = GALAXY
    ledger["uses_vobs_or_residual"] = False
    ledger["claim_boundary"] = CLAIM_BOUNDARY
    ledger = ledger[
        [
            "galaxy",
            "source_observable",
            "source_basis",
            "theta_role",
            "xit_role",
            "assignment",
            "double_count_risk",
            "allowed_in_combined_control",
            "endpoint_permission",
            "uses_vobs_or_residual",
            "reason",
            "claim_boundary",
        ]
    ]

    counts = ledger["assignment"].value_counts().to_dict()
    n_shared_or_partial = int(
        ledger["assignment"].isin(
            [
                "SHARED_CONTEXT_NOT_INDEPENDENT",
                "PARTIALLY_SHARED_NEEDS_SPLIT",
                "THETA_PRIMARY_XIT_CAVEATED_PHASE_ONLY",
            ]
        ).sum()
    )
    n_theta_only = int(ledger["assignment"].eq("THETA_ONLY").sum())
    n_xit_only = int(ledger["assignment"].str.startswith("XIT_ONLY").sum())
    n_excluded = int(ledger["assignment"].str.startswith("EXCLUDED").sum())
    path_established = str(path_audit["foreground_path_status"]) != "NOT_ESTABLISHED"
    combined_control_allowed = True
    combined_endpoint_allowed = False
    status = "PARTIAL_NONOVERLAP_CONTROL_ALLOWED_COMBINED_ENDPOINT_BLOCKED"

    gates = pd.DataFrame(
        [
            {
                "gate_id": "U12506_NONOVERLAP_G1_FORMULA_ROLE",
                "gate_status": "PASS",
                "gate_text": "Theta_morph is additive; Xi_t is multiplicative interval-control.",
            },
            {
                "gate_id": "U12506_NONOVERLAP_G2_UNIQUE_THETA_SHAPE",
                "gate_status": "PASS_CONTROL_ONLY" if n_theta_only >= 1 else "BLOCKED",
                "gate_text": "late-settling outer radial shape can be assigned to Theta_morph only.",
            },
            {
                "gate_id": "U12506_NONOVERLAP_G3_UNIQUE_XIT_CAP",
                "gate_status": "PASS_CONTROL_ONLY" if n_xit_only >= 1 else "BLOCKED",
                "gate_text": "epsilon_t cap is Xi_t-only protocol bound, not a morphology amplitude.",
            },
            {
                "gate_id": "U12506_NONOVERLAP_G4_SHARED_CONTEXT",
                "gate_status": "BLOCK_COMBINED_ENDPOINT" if n_shared_or_partial else "PASS",
                "gate_text": "high-spin/envelope/asymmetry context remains shared or partially shared.",
            },
            {
                "gate_id": "U12506_NONOVERLAP_G5_PATH_TERM",
                "gate_status": "BLOCK_PATH_ENDPOINT" if not path_established else "PASS",
                "gate_text": "path/environment term remains zero unless source path review establishes it.",
            },
            {
                "gate_id": "U12506_NONOVERLAP_G6_ENDPOINT_BOUNDARY",
                "gate_status": "CONTROL_ALLOWED_ENDPOINT_BLOCKED",
                "gate_text": "combined-control replay may be recorded; combined endpoint is not permitted.",
            },
        ]
    )
    gates["galaxy"] = GALAXY
    gates["endpoint_permission"] = False
    gates["uses_vobs_or_residual"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "nonoverlap_status": status,
                "galaxy": GALAXY,
                "n_ledger_rows": int(len(ledger)),
                "n_shared_or_partial_rows": n_shared_or_partial,
                "n_theta_only_rows": n_theta_only,
                "n_xit_only_rows": n_xit_only,
                "n_excluded_rows": n_excluded,
                "assignment_counts": "; ".join(f"{k}={v}" for k, v in sorted(counts.items())),
                "path_term_established": path_established,
                "theta_endpoint_allowed": False,
                "xit_standard_endpoint_allowed": False,
                "combined_control_replay_allowed": combined_control_allowed,
                "combined_endpoint_allowed": combined_endpoint_allowed,
                "endpoint_validation_claim": False,
                "next_gate": (
                    "run optional combined-control replay with ledger assignments frozen, "
                    "or acquire non-overlapping clock/path evidence before endpoint"
                ),
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    ledger.to_csv(DATA / "ugc12506_theta_xit_source_nonoverlap_ledger.csv", index=False)
    gates.to_csv(DATA / "ugc12506_theta_xit_source_nonoverlap_gates.csv", index=False)
    summary.to_csv(DATA / "ugc12506_theta_xit_source_nonoverlap_summary.csv", index=False)

    report = [
        "# UGC12506 Theta_morph / Xi_t Source-Nonoverlap Gate",
        "",
        "This audit separates source evidence by channel role. It does not score",
        "an endpoint and does not choose a new amplitude from the rotation curve.",
        "",
        "## Summary",
        "",
        markdown_table(summary),
        "",
        "## Source Ledger",
        "",
        markdown_table(ledger),
        "",
        "## Gates",
        "",
        markdown_table(gates),
        "",
        "## Interpretation",
        "",
        "The current refinements make the UGC12506 channels separable enough for",
        "a combined-control ledger: the late-settling radial shape is assigned to",
        "`Theta_morph`, while the small cap is assigned to `Xi_t`.  However, the",
        "high-spin/envelope/asymmetry context is not yet independent across the",
        "two channels, and the path/environment term remains unestablished.  The",
        "combined endpoint therefore remains blocked.",
        "",
        "## Xi_t component policy snapshot",
        "",
        markdown_table(xit_components),
        "",
    ]
    (REPORTS / "ugc12506_theta_xit_source_nonoverlap_gate.md").write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
