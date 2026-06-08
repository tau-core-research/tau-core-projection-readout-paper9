#!/usr/bin/env python3
"""Build strengthened residual-blind source reviews for NGC4088 and NGC4013."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
REPORTS = ROOT / "reports"

CLAIM_BOUNDARY = "ngc4088_ngc4013_strengthened_source_review_not_endpoint"


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
        lines.append("| " + " | ".join(str(row[column]).replace("\n", " ") for column in display.columns) + " |")
    return "\n".join(lines)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    evidence = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "field_id": "N4088_S1_DISTORTED_DISK",
                "channel": "warp_history",
                "observable": "strongly_distorted_disk",
                "value": "strongly distorted disk; strong star-formation/radio context",
                "source": "Verheijen & Sancisi 2001 Ursa Major H I atlas",
                "source_ref": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11498-11503",
                "status": "ACCEPTED_QUALITATIVE_SOURCE_FIELD",
                "review_effect": "supports warp/history class and rejects quiet regular disk interpretation",
            },
            {
                "galaxy": "NGC4088",
                "field_id": "N4088_S2_PV_ASYMMETRY",
                "channel": "warp_history",
                "observable": "strong_position_velocity_asymmetry",
                "value": "PV diagram shows strong asymmetry",
                "source": "Verheijen & Sancisi 2001 Ursa Major H I atlas",
                "source_ref": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11502-11505",
                "status": "ACCEPTED_QUALITATIVE_SOURCE_FIELD",
                "review_effect": "supports asymmetry/history component but not numeric q_warp amplitude",
            },
            {
                "galaxy": "NGC4088",
                "field_id": "N4088_S3_ASYMMETRIC_WARP",
                "channel": "warp_history",
                "observable": "asymmetric_warp_side_dependence",
                "value": "channel maps at 618 and 899 km/s show asymmetric warp; PA changes more in southern part",
                "source": "Verheijen & Sancisi 2001 Ursa Major H I atlas",
                "source_ref": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11503-11508",
                "status": "ACCEPTED_QUALITATIVE_SOURCE_FIELD",
                "review_effect": "strengthens q_warp direction; numeric side-amplitude still requires measurement",
            },
            {
                "galaxy": "NGC4088",
                "field_id": "N4088_S4_COMPANION_HISTORY",
                "channel": "morphological_history",
                "observable": "near_companion_context",
                "value": "NGC4085 located 10 arcmin south",
                "source": "Verheijen & Sancisi 2001 Ursa Major H I atlas",
                "source_ref": "data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11508-11512",
                "status": "ACCEPTED_CONTEXT_SOURCE_FIELD",
                "review_effect": "supports history/context, not standalone amplitude",
            },
            {
                "galaxy": "NGC4088",
                "field_id": "N4088_B1_XW_NUMERIC",
                "channel": "numeric_precision",
                "observable": "warp_onset_fraction_x_w",
                "value": "first-pass x_w=0.2823529411764706",
                "source": "existing internal digitization plus H I radius",
                "source_ref": "data/derived/ngc4088_source_review_gate_decisions.csv",
                "status": "STILL_BLOCKED_INDEPENDENT_NUMERIC_REVIEW_REQUIRED",
                "review_effect": "classification strengthened, endpoint-grade numeric precision not yet accepted",
            },
            {
                "galaxy": "NGC4013",
                "field_id": "N4013_S1_LINE_OF_SIGHT_WARP",
                "channel": "warp_vertical_overlay",
                "observable": "line_of_sight_warp_component",
                "value": "line-of-sight warp begins near 1.2 arcmin / 10 kpc and is about a quarter of the other warp component",
                "source": "Zschaechner & Rand 2015 H I kinematics",
                "source_ref": "data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:404-413",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "review_effect": "strengthens radial warp window and projection-aware morphology label",
            },
            {
                "galaxy": "NGC4013",
                "field_id": "N4013_S2_WARP_ORIENTATION",
                "channel": "observer_projection",
                "observable": "warp_orientation_angle",
                "value": "total warp oriented approximately 70 degrees from the line of sight",
                "source": "Zschaechner & Rand 2015 H I kinematics",
                "source_ref": "data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:408-413",
                "status": "ACCEPTED_CAVEATED_SOURCE_FIELD",
                "review_effect": "supports morphology-dependent observer/projection interpretation; near/far degeneracy caveat retained",
            },
            {
                "galaxy": "NGC4013",
                "field_id": "N4013_S3_FLARE_SCALEHEIGHT",
                "channel": "vertical_overlay",
                "observable": "H_I_scaleheight_and_flare",
                "value": "1C scale height 7 arcsec/500 pc; W model 5 arcsec/350 pc; WF final central scale height 3 arcsec/210 pc",
                "source": "Zschaechner & Rand 2015 H I kinematics",
                "source_ref": "data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:390-430",
                "status": "ACCEPTED_NUMERIC_MODEL_SOURCE_FIELD",
                "review_effect": "strengthens vertical-overlay and flare channel; model-resolution caveat retained",
            },
            {
                "galaxy": "NGC4013",
                "field_id": "N4013_S4_LAG_PROFILE",
                "channel": "vertical_overlay",
                "observable": "radially_shallowing_vertical_lag",
                "value": "lag shallows from -35 km/s/kpc at 1.4 arcmin / 5.8 kpc to zero near R25 / 11.2 kpc",
                "source": "Zschaechner & Rand 2015 H I kinematics",
                "source_ref": "data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:13-22",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "review_effect": "upgrades lag profile from context-only to source-numeric kernel support",
            },
            {
                "galaxy": "NGC4013",
                "field_id": "N4013_S5_EXTENDED_COMPONENT",
                "channel": "vertical_mass_overlay",
                "observable": "extended_component_mass_and_scaleheight",
                "value": "extra flattened component z_EC about 3 kpc; about 20-26 percent of disk mass",
                "source": "Comeron et al. 2011 Spitzer vertical decomposition",
                "source_ref": "data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt:180-192;392-403",
                "status": "ACCEPTED_NUMERIC_SOURCE_FIELD",
                "review_effect": "cross-checks vertical overlay normalization and rejects pure thin+thick-only morphology",
            },
        ]
    )
    evidence["uses_vobs_or_residual"] = False
    evidence["endpoint_scores_allowed"] = False
    evidence["claim_boundary"] = CLAIM_BOUNDARY

    summary = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "review_status": "BROAD_CLASS_STRENGTHENED_NUMERIC_PRECISION_STILL_BLOCKED",
                "classification_strength": "STRONG_QUALITATIVE_SOURCE_SUPPORT",
                "what_changed": "warp/history classification is now explicitly supported by accepted qualitative H I/PV/companion fields",
                "what_remains_open": "x_warp, numeric q_warp, memory/history decomposition, epsilon_cross bound",
                "endpoint_grade_label_now": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
            {
                "galaxy": "NGC4013",
                "review_status": "MIXED_OVERLAY_LABEL_STRENGTHENED_SOURCE_NUMERIC",
                "classification_strength": "CAVEATED_PROSPECTIVE_PROTOCOL_STRONGER",
                "what_changed": "lag, line-of-sight warp, flare/scaleheight, and extended vertical component are now recorded as source-numeric support",
                "what_remains_open": "not retroactive validation; near/far projection degeneracy; lag-map digitization can still sharpen the kernel",
                "endpoint_grade_label_now": False,
                "uses_vobs_or_residual": False,
                "claim_boundary": CLAIM_BOUNDARY,
            },
        ]
    )

    gates = pd.DataFrame(
        [
            {
                "galaxy": "NGC4088",
                "gate_id": "N4088_STR1_BROAD_WARP_HISTORY",
                "gate_status": "PASS_STRENGTHENED",
                "evidence": "distorted disk, strong PV asymmetry, asymmetric warp, companion context",
                "remaining_obligation": "none at broad class level",
            },
            {
                "galaxy": "NGC4088",
                "gate_id": "N4088_STR2_NUMERIC_KERNEL_FIELDS",
                "gate_status": "BLOCKED",
                "evidence": "qualitative source support exists, but x_warp/q_warp not independently numeric accepted",
                "remaining_obligation": "independent H I map/PV digitization or source-native product extraction",
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "N4013_STR1_SOURCE_NUMERIC_WARP_LAG",
                "gate_status": "PASS_STRENGTHENED",
                "evidence": "line-of-sight warp onset, orientation, flare/scaleheight, radial lag profile",
                "remaining_obligation": "none for source-numeric mixed-overlay support",
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "N4013_STR2_VERTICAL_COMPONENT_CROSSCHECK",
                "gate_status": "PASS_STRENGTHENED",
                "evidence": "Comeron extended component z_EC and mass fraction support vertical overlay",
                "remaining_obligation": "keep EC separate from H I flare; use as cross-check, not duplicate count",
            },
            {
                "galaxy": "NGC4013",
                "gate_id": "N4013_STR3_RETROACTIVE_VALIDATION",
                "gate_status": "BLOCKED",
                "evidence": "strengthened source label does not make old diagnostic score independent",
                "remaining_obligation": "future prospective replay/holdout or uninspected analogue",
            },
        ]
    )
    gates["uses_vobs_or_residual"] = False
    gates["endpoint_scores_allowed"] = False
    gates["claim_boundary"] = CLAIM_BOUNDARY

    evidence.to_csv(DATA / "ngc4088_ngc4013_strengthened_source_review_evidence.csv", index=False)
    summary.to_csv(DATA / "ngc4088_ngc4013_strengthened_source_review_summary.csv", index=False)
    gates.to_csv(DATA / "ngc4088_ngc4013_strengthened_source_review_gates.csv", index=False)

    report = "\n".join(
        [
            "# NGC4088 / NGC4013 Strengthened Source Review",
            "",
            f"Claim boundary: `{CLAIM_BOUNDARY}`",
            "",
            "This packet strengthens the source-side morphology classifications without",
            "using observed rotation residuals or endpoint scores.",
            "",
            "## Summary",
            "",
            markdown_table(summary),
            "",
            "## Gates",
            "",
            markdown_table(gates),
            "",
            "## Evidence",
            "",
            markdown_table(evidence),
            "",
            "## Verdict",
            "",
            "- **NGC4088:** strengthened at broad class level.  The source literature",
            "  supports a distorted/asymmetric warp/history classification, but the",
            "  numeric kernel fields remain blocked until independent H I map/PV",
            "  measurements accept `x_warp` and `q_warp`.",
            "- **NGC4013:** strengthened at source-numeric mixed-overlay level.  The",
            "  line-of-sight warp, radial lag, flare/scaleheight, and extended",
            "  vertical component now provide stronger residual-blind support for the",
            "  mixed morphology label.  This still does not make the earlier diagnostic",
            "  score a retroactive validation.",
            "",
        ]
    )
    (REPORTS / "ngc4088_ngc4013_strengthened_source_review.md").write_text(
        report, encoding="utf-8"
    )

    print("STRENGTHENED_SOURCE_REVIEW_COMPLETE")
    print(summary[["galaxy", "review_status", "classification_strength"]].to_string(index=False))


if __name__ == "__main__":
    main()
