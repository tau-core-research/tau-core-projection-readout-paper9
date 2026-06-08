# NGC4088 / NGC4013 Strengthened Source Review

Claim boundary: `ngc4088_ngc4013_strengthened_source_review_not_endpoint`

This packet strengthens the source-side morphology classifications without
using observed rotation residuals or endpoint scores.

## Summary

| galaxy | review_status | classification_strength | what_changed | what_remains_open | endpoint_grade_label_now | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | BROAD_CLASS_STRENGTHENED_NUMERIC_PRECISION_STILL_BLOCKED | STRONG_QUALITATIVE_SOURCE_SUPPORT | warp/history classification is now explicitly supported by accepted qualitative H I/PV/companion fields | x_warp, numeric q_warp, memory/history decomposition, epsilon_cross bound | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | MIXED_OVERLAY_LABEL_STRENGTHENED_SOURCE_NUMERIC | CAVEATED_PROSPECTIVE_PROTOCOL_STRONGER | lag, line-of-sight warp, flare/scaleheight, and extended vertical component are now recorded as source-numeric support | not retroactive validation; near/far projection degeneracy; lag-map digitization can still sharpen the kernel | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_STR1_BROAD_WARP_HISTORY | PASS_STRENGTHENED | distorted disk, strong PV asymmetry, asymmetric warp, companion context | none at broad class level | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4088 | N4088_STR2_NUMERIC_KERNEL_FIELDS | BLOCKED | qualitative source support exists, but x_warp/q_warp not independently numeric accepted | independent H I map/PV digitization or source-native product extraction | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_STR1_SOURCE_NUMERIC_WARP_LAG | PASS_STRENGTHENED | line-of-sight warp onset, orientation, flare/scaleheight, radial lag profile | none for source-numeric mixed-overlay support | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_STR2_VERTICAL_COMPONENT_CROSSCHECK | PASS_STRENGTHENED | Comeron extended component z_EC and mass fraction support vertical overlay | keep EC separate from H I flare; use as cross-check, not duplicate count | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_STR3_RETROACTIVE_VALIDATION | BLOCKED | strengthened source label does not make old diagnostic score independent | future prospective replay/holdout or uninspected analogue | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |

## Evidence

| galaxy | field_id | channel | observable | value | source | source_ref | status | review_effect | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_S1_DISTORTED_DISK | warp_history | strongly_distorted_disk | strongly distorted disk; strong star-formation/radio context | Verheijen & Sancisi 2001 Ursa Major H I atlas | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11498-11503 | ACCEPTED_QUALITATIVE_SOURCE_FIELD | supports warp/history class and rejects quiet regular disk interpretation | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4088 | N4088_S2_PV_ASYMMETRY | warp_history | strong_position_velocity_asymmetry | PV diagram shows strong asymmetry | Verheijen & Sancisi 2001 Ursa Major H I atlas | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11502-11505 | ACCEPTED_QUALITATIVE_SOURCE_FIELD | supports asymmetry/history component but not numeric q_warp amplitude | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4088 | N4088_S3_ASYMMETRIC_WARP | warp_history | asymmetric_warp_side_dependence | channel maps at 618 and 899 km/s show asymmetric warp; PA changes more in southern part | Verheijen & Sancisi 2001 Ursa Major H I atlas | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11503-11508 | ACCEPTED_QUALITATIVE_SOURCE_FIELD | strengthens q_warp direction; numeric side-amplitude still requires measurement | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4088 | N4088_S4_COMPANION_HISTORY | morphological_history | near_companion_context | NGC4085 located 10 arcmin south | Verheijen & Sancisi 2001 Ursa Major H I atlas | data/external/literature/2001_verheijen_sancisi_ursa_major_hi.txt:11508-11512 | ACCEPTED_CONTEXT_SOURCE_FIELD | supports history/context, not standalone amplitude | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4088 | N4088_B1_XW_NUMERIC | numeric_precision | warp_onset_fraction_x_w | first-pass x_w=0.2823529411764706 | existing internal digitization plus H I radius | data/derived/ngc4088_source_review_gate_decisions.csv | STILL_BLOCKED_INDEPENDENT_NUMERIC_REVIEW_REQUIRED | classification strengthened, endpoint-grade numeric precision not yet accepted | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_S1_LINE_OF_SIGHT_WARP | warp_vertical_overlay | line_of_sight_warp_component | line-of-sight warp begins near 1.2 arcmin / 10 kpc and is about a quarter of the other warp component | Zschaechner & Rand 2015 H I kinematics | data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:404-413 | ACCEPTED_NUMERIC_SOURCE_FIELD | strengthens radial warp window and projection-aware morphology label | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_S2_WARP_ORIENTATION | observer_projection | warp_orientation_angle | total warp oriented approximately 70 degrees from the line of sight | Zschaechner & Rand 2015 H I kinematics | data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:408-413 | ACCEPTED_CAVEATED_SOURCE_FIELD | supports morphology-dependent observer/projection interpretation; near/far degeneracy caveat retained | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_S3_FLARE_SCALEHEIGHT | vertical_overlay | H_I_scaleheight_and_flare | 1C scale height 7 arcsec/500 pc; W model 5 arcsec/350 pc; WF final central scale height 3 arcsec/210 pc | Zschaechner & Rand 2015 H I kinematics | data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:390-430 | ACCEPTED_NUMERIC_MODEL_SOURCE_FIELD | strengthens vertical-overlay and flare channel; model-resolution caveat retained | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_S4_LAG_PROFILE | vertical_overlay | radially_shallowing_vertical_lag | lag shallows from -35 km/s/kpc at 1.4 arcmin / 5.8 kpc to zero near R25 / 11.2 kpc | Zschaechner & Rand 2015 H I kinematics | data/external/literature/ngc4013_zschaechner_rand_2015_hi_kinematics.txt:13-22 | ACCEPTED_NUMERIC_SOURCE_FIELD | upgrades lag profile from context-only to source-numeric kernel support | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |
| NGC4013 | N4013_S5_EXTENDED_COMPONENT | vertical_mass_overlay | extended_component_mass_and_scaleheight | extra flattened component z_EC about 3 kpc; about 20-26 percent of disk mass | Comeron et al. 2011 Spitzer vertical decomposition | data/external/literature/ngc4013_comeron_2011_unusual_vertical_mass_distribution.txt:180-192;392-403 | ACCEPTED_NUMERIC_SOURCE_FIELD | cross-checks vertical overlay normalization and rejects pure thin+thick-only morphology | False | False | ngc4088_ngc4013_strengthened_source_review_not_endpoint |

## Verdict

- **NGC4088:** strengthened at broad class level.  The source literature
  supports a distorted/asymmetric warp/history classification, but the
  numeric kernel fields remain blocked until independent H I map/PV
  measurements accept `x_warp` and `q_warp`.
- **NGC4013:** strengthened at source-numeric mixed-overlay level.  The
  line-of-sight warp, radial lag, flare/scaleheight, and extended
  vertical component now provide stronger residual-blind support for the
  mixed morphology label.  This still does not make the earlier diagnostic
  score a retroactive validation.
