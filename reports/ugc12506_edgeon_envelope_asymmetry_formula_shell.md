# UGC12506 Edge-on + Envelope + Asymmetry Formula Shell

This source-frozen shell uses only the components allowed by the
observer/path/interloper audit. It excludes the image-plane interloper
from the gravity kernel and does not include a foreground/path object.

## Summary

| formula_shell_status | galaxy | evidence_total | gamma_total | amplitude_total_km2_s2 | kernel_outer_mean_last8 | edgeon_weight | envelope_weight | asymmetry_weight | n_gates | n_blocked | n_caveated | formula_frozen_before_scoring | control_replay_scores_allowed | endpoint_validation_claim_allowed | construction_used_vobs_or_residual | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_EEA_FORMULA_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 8.87085 | 0.898692 | 11380.4 | 0.809424 | 0.0673081 | 0.923344 | 0.00934835 | 5 | 0 | 1 | True | True | False | False | scripts/run_ugc12506_edgeon_envelope_asymmetry_replay_controls.py | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |

## Manifest

| galaxy | formula_id | formula_text | kernel_text | amplitude_rule | gamma_rule | edgeon_load | envelope_load | asymmetry_load_half_weighted | edgeon_weight | envelope_weight | asymmetry_weight | evidence_total | gamma_total | carrier_scale_outer_km2_s2 | amplitude_total_km2_s2 | dimension_check | known_limits | interloper_policy | formula_frozen_before_scoring | construction_used_vobs_or_residual | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | v_readout^2(R)=v_carrier^2(R)+A_eea K_eea(R) | K_eea=norm[w_edge K_edge + w_env K_env + w_asym K_asym]; interloper mask excluded from gravity kernel | A_eea=Gamma_eea median_outer_R>=Ropt(v_carrier^2) | Gamma_eea=E_eea/(1+E_eea), E_eea=w_edge+w_env+w_asym | 0.59708 | 8.19084 | 0.0829278 | 0.0673081 | 0.923344 | 0.00934835 | 8.87085 | 0.898692 | 12663.3 | 11380.4 | PASS: A_eea has km^2/s^2 and K_eea is dimensionless | i<=80 deg, R_HI/R_d->1, lambda_spin->0, or K_eea=0 recovers carrier | photometric mask/caveat only; no foreground path gravity term | True | False | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |

## Components

| galaxy | component_id | component_status | source_load | normalized_weight | kernel_column | source_basis | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | K_edgeon_disk_integration | INCLUDED_SOURCE_SUPPORTED_STRONG | 0.59708 | 0.0673081 | K_edgeon_disk_integration | i=86 deg and PV/envelope method required | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | K_extended_hi_envelope | INCLUDED_SOURCE_SUPPORTED_STRONG | 8.19084 | 0.923344 | K_extended_hi_envelope | large H I extent, diffuse stable gas, high spin | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | K_arm_asymmetry_extent | INCLUDED_SOURCE_SUPPORTED_CAVEATED_HALF_WEIGHT | 0.0829278 | 0.00934835 | K_arm_asymmetry_extent | approaching/receding detectable extent asymmetry | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | M_photometric_interloper_mask | EXCLUDED_FROM_GRAVITY_KERNEL_MASK_CAVEAT_ONLY | 0 | 0 |  | higher-redshift galaxy and star are image-plane interlopers | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | K_foreground_path_object | EXCLUDED_NOT_ESTABLISHED | 0 | 0 |  | no foreground/path object established by current source | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | U12506_EEA_G1_AUDIT_INPUT | PASS | UGC12506_OBSERVER_PATH_INTERLOPER_AUDIT_COMPLETE_KERNEL_REVISION_REQUIRED | none for formula replay | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | U12506_EEA_G2_INTERLOPER_EXCLUSION | PASS | image-plane interlopers excluded from gravity kernel | foreground/path term requires new catalogue cone search | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | U12506_EEA_G3_COMPONENT_WEIGHTS | PASS_CAVEATED | asymmetry half-weighted due to caveated source status | independent source-side asymmetry normalization review | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | U12506_EEA_G4_DIMENSIONS_LIMITS | PASS | A_eea velocity-squared; K_eea dimensionless; carrier limits explicit | none | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
| UGC12506 | UGC12506_EDGEON_ENVELOPE_ASYMMETRY_SOURCE_SHELL | U12506_EEA_G5_RESIDUAL_BLIND | PASS | construction_used_vobs_or_residual=False | vobs may enter only in separate replay scoring script | False | ugc12506_edgeon_envelope_asymmetry_formula_shell_not_validation |
