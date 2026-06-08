# UGC12506 Incremental Projection-History Formula Shell

This shell is incremental on top of the source-native NFW-HSE readout.
It includes only the source-supported internal projection and caveated
asymmetry/history terms, and avoids double-counting the extended H I
envelope already present in the NFW-HSE base.

## Summary

| formula_shell_status | galaxy | edgeon_weight | asymmetry_weight | evidence_total | gamma_total | amplitude_ph_km2_s2 | kernel_inner_mean_first8 | kernel_outer_mean_last8 | n_gates | n_blocked | n_caveated | formula_frozen_before_scoring | control_replay_scores_allowed | endpoint_validation_claim_allowed | construction_used_vobs_or_residual | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_INCREMENTAL_PROJECTION_HISTORY_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 0.827586 | 0.172414 | 0.721472 | 0.419102 | 9586.67 | 0.00221005 | 0.751943 | 5 | 0 | 2 | True | True | False | False | scripts/run_ugc12506_projection_history_incremental_replay.py | ugc12506_projection_history_incremental_formula_shell_not_validation |

## Manifest

| galaxy | formula_id | formula_text | kernel_text | amplitude_rule | gamma_rule | edgeon_load | asymmetry_history_load | edgeon_weight | asymmetry_weight | evidence_total | gamma_total | source_native_outer_scale_km2_s2 | amplitude_ph_km2_s2 | dimension_check | known_limits | double_counting_policy | formula_frozen_before_scoring | construction_used_vobs_or_residual | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | v_readout^2(R)=v_source_native_nfw_hse^2(R)+A_PH K_PH(R) | K_PH=norm[w_edge K_edgeon_increment + w_asym K_asymmetry_history_increment] | A_PH=Gamma_PH median_outer_R>=Ropt(v_source_native_nfw_hse^2) | Gamma_PH=E_PH/(1+E_PH), E_PH=w_edge_source+w_asym_history_source | 0.59708 | 0.124392 | 0.827586 | 0.172414 | 0.721472 | 0.419102 | 22874.3 | 9586.67 | PASS: A_PH has km^2/s^2 and K_PH is dimensionless | i<=80 deg and A_extent=0 recover the source-native NFW-HSE base; no foreground/path object term is included | extended H I envelope excluded from increment because NFW-HSE base already includes it | True | False | False | ugc12506_projection_history_incremental_formula_shell_not_validation |

## Components

| galaxy | component_id | component_status | source_load | normalized_weight | kernel_column | source_basis | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | K_edgeon_disk_integration_increment | INCLUDED_SOURCE_SUPPORTED_STRONG | 0.59708 | 0.827586 | K_projection_history_edgeon_increment | i=86 deg and PV/envelope method required | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | K_arm_asymmetry_history_increment | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.124392 | 0.172414 | K_projection_history_asymmetry_increment | approaching/receding extent asymmetry coupled to high-spin context | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | K_extended_hi_envelope_main | EXCLUDED_FROM_INCREMENT_ALREADY_IN_NFW_HSE | 0 | 0 |  | included in source-native NFW-HSE base shell | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | K_foreground_path_object | EXCLUDED_NOT_ESTABLISHED | 0 | 0 |  | no source-supported foreground/path object | ugc12506_projection_history_incremental_formula_shell_not_validation |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | U12506_PHI_G1_CANDIDATE_GATE | PASS_CAVEATED | UGC12506_PROJECTION_HISTORY_ENRICHED_READOUT_CANDIDATE_SOURCE_SUPPORTED_CAVEATED | not endpoint validation | False | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | U12506_PHI_G2_SIGN_RULE | PASS_CAVEATED | edge-on PV/envelope and extent asymmetry enter as positive 1D readout broadening terms | resolved velocity-field review for side-specific sign | False | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | U12506_PHI_G3_NO_DOUBLE_COUNT_ENVELOPE | PASS | extended envelope is excluded from the incremental PH term because it is already in NFW-HSE | none | False | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | U12506_PHI_G4_DIMENSIONS_LIMITS | PASS | A_PH velocity-squared; K_PH dimensionless; base recovery limits explicit | none | False | ugc12506_projection_history_incremental_formula_shell_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_ON_SOURCE_NATIVE_NFW_HSE | U12506_PHI_G5_RESIDUAL_BLIND | PASS | construction_used_vobs_or_residual=False | vobs may enter only in separate replay scoring script | False | ugc12506_projection_history_incremental_formula_shell_not_validation |

## Claim Boundary

This is a caveated control replay shell, not endpoint validation. The
positive sign is justified only at the 1D readout-broadening level; a
resolved velocity-field review is still required for a side-specific
projection/history sign rule.
