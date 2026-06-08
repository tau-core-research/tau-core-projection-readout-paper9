# UGC12506 Source-Normalized Amplitude Prefreeze

`UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT`

This gate freezes a source-normalized amplitude rule for future control
replay.  It does not score the endpoint and does not select the final sign
from the observed residual.

## Summary

| amplitude_prefreeze_status | galaxy | highspin_source_load | highspin_gamma | highspin_amplitude_km2_s2 | asymmetry_source_load | asymmetry_gamma | asymmetry_amplitude_km2_s2 | carrier_scale_outer_km2_s2 | formula_prefreeze_allowed_for_future_controls | endpoint_scores_allowed | uses_vobs_or_residual_in_prefreeze | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT | UGC12506 | 0.199027 | 0.16599 | 2150.25 | 0.663423 | 0.39883 | 5166.47 | 12954.1 | True | False | False | run_ugc12506_prefrozen_branch_replay_controls_after_label_gate | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |

## Rules

| galaxy | rule_id | rule_status | formula | source_load_formula | gamma_formula | source_load | gamma | carrier_scale_km2_s2 | amplitude_km2_s2 | sign_options_for_future_controls | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_AMP_RULE_HIGHS_PIN | PREFROZEN_FOR_CONTROL_REPLAY_NOT_VALIDATION | A_hs = Gamma_hs * median_outer(v_baryon_050^2) | E_hs=sin^2(i)*max((lambda_spin-0.10)/0.10,0)*C_stableHI | Gamma_hs=E_hs/(1+E_hs) | 0.199027 | 0.16599 | 12954.1 | 2150.25 | positive_added_readout;negative_attenuation_control | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |
| UGC12506 | UGC12506_AMP_RULE_ASYMMETRY | PREFROZEN_FOR_CONTROL_REPLAY_NOT_VALIDATION | A_pa = Gamma_pa * median_outer(v_baryon_050^2) | E_pa=sin^2(i)*max(A_extent/0.25,0) | Gamma_pa=E_pa/(1+E_pa) | 0.663423 | 0.39883 | 12954.1 | 5166.47 | positive_added_readout;negative_attenuation_control | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_AMP_G1_PREFLIGHT | PASS_PREFLIGHT_AVAILABLE | UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED | none for preflight | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |
| UGC12506 | UGC12506_AMP_G2_SOURCE_LOAD | PASS_SOURCE_LOAD_DECLARED | projection, high-spin, stability, and asymmetry loads use source-side observables | audit protocol constants before endpoint use | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |
| UGC12506 | UGC12506_AMP_G3_DIMENSIONS | PASS_DIMENSIONAL_CHECK | Gamma dimensionless; median outer carrier scale supplies km^2/s^2 | none at prefreeze level | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |
| UGC12506 | UGC12506_AMP_G4_SIGN | BLOCKED_SIGN_TO_BE_CONTROL_REPLAYED | positive and negative branches are frozen as future controls, not selected here | run both branches in a separate scoring script if endpoint gates pass | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |
| UGC12506 | UGC12506_AMP_G5_ENDPOINT | BLOCKED_ENDPOINT_NOT_ALLOWED | this script does not score vobs and does not claim validation | label gate and replay protocol required before scoring | False | False | ugc12506_source_normalized_amplitude_prefreeze_not_endpoint |

## Claim Boundary

The amplitude is built from source-side projection/high-spin/stability
context and the baryonic carrier scale.  It is ready for future branch
control replay only after the label gate is resolved.  It is not a
validation result.
