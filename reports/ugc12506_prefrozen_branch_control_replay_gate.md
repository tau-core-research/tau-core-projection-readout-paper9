# UGC12506 Prefrozen Branch Control Replay Gate

This gate allows a caveated single-galaxy control replay of the
source-frozen high-spin/projection branches. It does not promote a
population-validation endpoint and it does not select the sign from
the rotation residual.

## Summary

| control_replay_gate_status | galaxy | n_gates | n_pass_like | n_blocked | n_caveated | control_replay_scores_allowed | endpoint_validation_claim_allowed | population_validation_claim_allowed | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_PREFROZEN_BRANCH_CONTROL_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 7 | 7 | 0 | 1 | True | False | False | scripts/run_ugc12506_prefrozen_branch_replay_controls.py | ugc12506_prefrozen_branch_control_replay_gate_not_validation |

## Manifest

| galaxy | replay_formula_manifest_id | source_context_status | preflight_status | amplitude_prefreeze_status | preferred_branch_family | secondary_branch_family | carrier_column | highspin_kernel_column | asymmetry_kernel_column | highspin_amplitude_km2_s2 | asymmetry_amplitude_km2_s2 | sign_policy | control_replay_scores_allowed | endpoint_validation_claim_allowed | population_validation_claim_allowed | uses_vobs_or_residual_in_gate | posthoc_retuning_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_PREFROZEN_HIGHS_PIN_PROJECTION_BRANCH_REPLAY | UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN | UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED | UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT | K_projection_highspin_outer_support | K_projection_asymmetry_outer_support | v_baryon_050_kms | K_context_highspin | K_context_projection_asymmetry | 2150.25 | 5166.47 | both positive added-readout and negative attenuation branches must be replayed; sign is not endpoint-selected here | True | False | False | False | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | control_replay_scores_allowed | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_CR1_SOURCE_CONTEXT_CACHED | PASS | UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN | none for control replay | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR2_SOURCE_CONTEXT_RESIDUAL_BLIND | PASS | uses_vobs_or_residual_in_acquisition=False | source acquisition must remain independent of endpoint residuals | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR3_PREFLIGHT_READY | PASS | UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED | all source observables and context kernels must be present | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR4_PREFLIGHT_RESIDUAL_BLIND | PASS | uses_vobs_or_residual_in_preflight=False | vobs may enter only in the scoring script | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR5_AMPLITUDE_PREFROZEN | PASS | UGC12506_SOURCE_NORMALIZED_AMPLITUDE_PREFROZEN_CONTROL_REPLAY_READY_NOT_ENDPOINT | amplitudes must have velocity-squared units and be positive | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR6_AMPLITUDE_RESIDUAL_BLIND | PASS | uses_vobs_or_residual_in_prefreeze=False | no observed residual may determine amplitude | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |
| UGC12506 | U12506_CR7_SIGN_BRANCHES_NOT_SELECTED | PASS_CAVEATED | positive_added_readout;negative_attenuation_control | score both signs as controls; do not promote sign from this gate | True | False | ugc12506_prefrozen_branch_control_replay_gate_not_validation |

## Claim Boundary

The replay may read `vobs` only in the separate scoring script. The
result must be reported as a prefrozen branch control replay, not as
accepted population validation.
