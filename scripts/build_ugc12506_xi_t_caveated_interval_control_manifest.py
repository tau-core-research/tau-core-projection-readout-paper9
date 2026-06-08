#!/usr/bin/env python3
"""Build the UGC12506 Xi_t caveated interval/control manifest.

This artifact records what the independent source-review response allows:
the high-spin edge-on envelope clock route may be carried as a caveated
interval/control manifest, but not as standard endpoint permission.  No
rotation residuals, endpoint RMSE values, or baseline ranks are used here.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"
GALAXY = "UGC12506"
CLAIM_BOUNDARY = "ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint"


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

    accepted = pd.read_csv(DATA / "ugc12506_xi_t_accepted_manifest_gate_summary.csv").iloc[0]
    manifest_shell = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv").iloc[0]
    components = pd.read_csv(DATA / "ugc12506_xi_t_highspin_envelope_clock_shell_components.csv")
    cap = pd.read_csv(DATA / "ugc12506_xi_t_epsilon_cap_protocol_summary.csv").iloc[0]
    response = pd.read_csv(DATA / "ugc12506_xi_t_source_review_response.csv").iloc[0]

    if not bool(accepted["caveated_interval_manifest_allowed"]):
        raise RuntimeError("Caveated interval/control manifest is not allowed by accepted-manifest gate")
    if bool(accepted["endpoint_scores_allowed"]):
        raise RuntimeError("This manifest builder must not run when endpoint scoring is already allowed")
    if bool(manifest_shell["construction_used_vobs_or_residual"]):
        raise RuntimeError("Xi_t shell construction used forbidden rotation residuals")

    epsilon_t_nominal = float(manifest_shell["epsilon_t"])
    epsilon_cap = float(cap["epsilon_cap"])
    epsilon_t_min = 0.0
    epsilon_t_max = epsilon_t_nominal
    xi_t_min = 1.0
    xi_t_max = 1.0 + epsilon_t_max
    xi2_shift_max = xi_t_max * xi_t_max - 1.0

    control_manifest = pd.DataFrame(
        [
            {
                "galaxy": GALAXY,
                "manifest_status": "U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY",
                "manifest_kind": "caveated_interval_control",
                "review_decision": accepted["review_decision"],
                "formula_text": manifest_shell["formula_text"],
                "kernel_text": manifest_shell["kernel_text"],
                "epsilon_rule": manifest_shell["epsilon_rule"],
                "epsilon_t_nominal": epsilon_t_nominal,
                "epsilon_t_interval_min": epsilon_t_min,
                "epsilon_t_interval_max": epsilon_t_max,
                "epsilon_cap_protocol": epsilon_cap,
                "xi_t_interval_min": xi_t_min,
                "xi_t_interval_max": xi_t_max,
                "xi_t_squared_fractional_shift_max": xi2_shift_max,
                "path_policy": "path term fixed to zero unless later source path review establishes it",
                "asymmetry_policy": "asymmetry remains caveated phase component, not standalone route driver",
                "cap_policy": "epsilon_cap=0.035 is protocol cap only, not universal Tau Core constant",
                "standard_endpoint_manifest_allowed": False,
                "control_manifest_allowed": True,
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    component_policy = components.copy()
    component_policy["control_policy"] = component_policy["component_id"].map(
        {
            "T_HIGHSPIN_SETTLING": "carry_as_source_supported_core_component",
            "T_EDGEON_PV_CLOCK_SLICE": "carry_with_projection_caveat",
            "T_ENVELOPE_SETTLING": "carry_as_caveated_interval_component",
            "T_ASYMMETRIC_PV_PHASE": "carry_only_as_caveated_phase_component",
            "T_PATH_ENVIRONMENT": "exclude_keep_zero_until_source_path_review",
        }
    )
    component_policy["endpoint_scores_allowed"] = False
    component_policy["claim_boundary"] = CLAIM_BOUNDARY

    review_policy = pd.DataFrame(
        [
            {
                "policy_id": "U12506_XIT_CTRL_P1_REVIEW_ROUTE",
                "policy_status": "PASS",
                "policy_text": str(response["allowed_response"]),
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "policy_id": "U12506_XIT_CTRL_P2_FORBIDDEN_INPUTS",
                "policy_status": "PASS",
                "policy_text": f"forbidden_inputs_used={response['forbidden_inputs_used']}",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "policy_id": "U12506_XIT_CTRL_P3_ENDPOINT_BLOCK",
                "policy_status": "PASS_RECORDED",
                "policy_text": "endpoint scoring remains blocked after control manifest creation",
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "policy_id": "U12506_XIT_CTRL_P4_CAP_BOUNDARY",
                "policy_status": "PASS_RECORDED",
                "policy_text": "epsilon_cap is protocol cap only; deeper Tau-side origin remains open",
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )
    review_policy["galaxy"] = GALAXY
    review_policy["endpoint_scores_allowed"] = False
    review_policy["uses_vobs_or_residual"] = False
    review_policy = review_policy[
        [
            "galaxy",
            "policy_id",
            "policy_status",
            "policy_text",
            "endpoint_scores_allowed",
            "uses_vobs_or_residual",
            "claim_boundary",
        ]
    ]

    summary = pd.DataFrame(
        [
            {
                "control_manifest_status": "U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY",
                "galaxy": GALAXY,
                "manifest_kind": "caveated_interval_control",
                "epsilon_t_interval": f"[{epsilon_t_min:.6g}, {epsilon_t_max:.6g}]",
                "xi_t_interval": f"[{xi_t_min:.6g}, {xi_t_max:.6g}]",
                "endpoint_scores_allowed": False,
                "uses_vobs_or_residual": False,
                "next_step": "optional control replay protocol; standard endpoint still requires a separate endpoint permission gate",
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ]
    )

    control_manifest.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_manifest.csv", index=False)
    component_policy.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_components.csv", index=False)
    review_policy.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_policies.csv", index=False)
    summary.to_csv(DATA / "ugc12506_xi_t_caveated_interval_control_summary.csv", index=False)

    report = "\n".join(
        [
            "# UGC12506 Xi_t Caveated Interval/Control Manifest",
            "",
            "This artifact records a source-reviewed caveated interval/control manifest. It is not an endpoint and does not score the rotation curve.",
            "",
            "## Control Manifest",
            "",
            markdown_table(control_manifest),
            "",
            "## Component Policy",
            "",
            markdown_table(component_policy),
            "",
            "## Review Policy",
            "",
            markdown_table(review_policy),
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Claim Boundary",
            "",
            "The reviewer accepted the high-spin edge-on envelope route only as a caveated interval/control route. The path term remains zero, the asymmetry term remains caveated, and epsilon_cap remains a protocol cap rather than a universal Tau Core constant.",
            "",
        ]
    )
    (REPORTS / "ugc12506_xi_t_caveated_interval_control_manifest.md").write_text(
        report,
        encoding="utf-8",
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
