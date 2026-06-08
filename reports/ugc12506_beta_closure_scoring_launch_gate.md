# UGC12506 Beta-Closure Scoring Launch Gate

This gate moves the beta_cl route toward scoring without scoring it.
It verifies whether the independent spin-route review and prefreeze
contracts are complete. In the current state the launch is blocked.

## Summary

| scoring_launch_status | selected_spin_normalization_route | n_required_inputs | n_missing_inputs | n_pass_gates | n_blocked_gates | n_prefrozen_transfer_rows | n_frozen_carrier_rows | beta_cl_transfer_scoring_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY | BULLOCK_DISK_CONVERSION | 9 | 0 | 5 | 0 | 11 | 1 | True | False | False | run_beta_cl_transfer_control_replay_scoring | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |

## Gates

| gate_id | gate_status | reason | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| BSP_SCORE_1_INPUTS_PRESENT | PASS | all required scoring-launch inputs exist | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| BSP_SCORE_2_REVIEW_ROUTE_ACCEPTED | PASS | review_intake_status=U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| BSP_SCORE_3_PREFREEZE_VALUES_EXIST | PASS | prefreeze_status=U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE; n_values=11 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| BSP_SCORE_4_DECISION_MATRIX_READY | PASS | decision_matrix_status=U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| BSP_SCORE_5_CARRIER_MANIFEST_READY | PASS | carrier_freeze_status=U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST; n_carriers=1 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |

## Required Inputs

| input_id | path | exists | n_rows | n_columns | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| decision_matrix_summary | data/derived/ugc12506_beta_closure_spin_route_decision_matrix_summary.csv | True | 1 | 13 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| review_intake_summary | data/derived/ugc12506_beta_closure_spin_proxy_review_response_intake_summary.csv | True | 1 | 10 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| spin_route_prefreeze_summary | data/derived/ugc12506_beta_closure_spin_route_prefreeze_summary.csv | True | 1 | 9 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| spin_route_prefreeze_values | data/derived/ugc12506_beta_closure_spin_route_prefreeze_values.csv | True | 11 | 10 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| transfer_carrier_freeze_summary | data/derived/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv | True | 1 | 14 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| transfer_carrier_manifest | data/derived/ugc12506_beta_closure_transfer_carrier_manifest.csv | True | 1 | 9 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| transfer_candidates | data/derived/ugc12506_beta_closure_transfer_candidates.csv | True | 11 | 15 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| halo_fit_fields | data/derived/ugc12506_beta_closure_transfer_halo_fit_fields.csv | True | 11 | 12 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| priority_gate | data/derived/ugc12506_beta_closure_transfer_priority_gate.csv | True | 11 | 14 | False | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |

## Scoring Protocol Skeleton

| protocol_step | required_artifact | allowed_to_read_vobs | status_now | claim_boundary |
| --- | --- | --- | --- | --- |
| SCORING_1_READ_FROZEN_VALUES | ugc12506_beta_closure_spin_route_prefreeze_values.csv | False | READY | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| SCORING_2_BUILD_TRANSFER_FORMULA_MANIFEST | future_beta_cl_transfer_formula_manifest.csv | False | BLOCKED_UNTIL_PREFREEZE_AND_CARRIER_READY | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |
| SCORING_3_RUN_SEPARATE_SCORING_SCRIPT | future_beta_cl_transfer_scores.csv | True | BLOCKED_UNTIL_FORMULA_MANIFEST_FROZEN | ugc12506_beta_closure_scoring_launch_gate_not_endpoint |

## Claim Boundary

This artifact does not read rotation curves and does not compute endpoint
scores. It only defines the final non-scoring launch gate before a future
separate scoring script.
