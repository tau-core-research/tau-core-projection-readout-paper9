# UGC12506 Beta-Closure Post-Review Scoring Launcher

This launcher runs the standard post-review chain if active response
files are present. It never writes review responses and it never treats
example-only rows as active decisions.

## Summary

| post_review_launcher_status | n_required_active_responses | n_active_responses_present | chain_returncodes_all_zero | spin_intake_status | carrier_intake_status | spin_prefreeze_status | carrier_freeze_status | scoring_launch_status | formula_freeze_status | transfer_scoring_status | scores_written | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_POST_REVIEW_SCORING_LAUNCHED_CONTROL_ONLY | 2 | 2 | True | U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED | U12506_BETA_CARRIER_REVIEW_ACCEPTED_PREFREEZE_ALLOWED | U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE | U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST | U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY | U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_READY_FOR_SCORING_RUNNER | U12506_BETA_CLOSURE_TRANSFER_SCORING_COMPLETE_CONTROL_ONLY | True | True | False | False | review_control_only_scores_before_any_endpoint_claim | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |

## Active Inputs

| active_response | response_type | exists | example_only_accepted | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| data/derived/ugc12506_beta_closure_spin_proxy_review_response.csv | spin_route_review | True | False | False | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| data/derived/ugc12506_beta_closure_carrier_review_response.csv | carrier_review | True | False | False | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |

## Chain Results

| script | returncode | stdout_tail | stderr_tail | claim_boundary |
| --- | --- | --- | --- | --- |
| scripts/run_ugc12506_beta_closure_spin_proxy_review_response_intake.py | 0 | U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED               True data/derived/ugc12506_beta_closure_spin_proxy_review_response.csv           BULLOCK_DISK_CONVERSION                     True                              True                    False                  False build_beta_cl_transfer_prefreeze_manifest ugc12506_beta_closure_spin_proxy_review_response_intake_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/build_ugc12506_beta_closure_spin_route_prefreeze_gate.py | 0 | U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE           BULLOCK_DISK_CONVERSION                         11                                True                   False                    False                  False build_beta_cl_transfer_replay_prefreeze_manifest ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/build_ugc12506_beta_closure_spin_route_decision_matrix.py | 0 | U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED         4                          2 UGC12506_BETA_CLOSURE_DIRECT_LAMBDA_SOURCE_GATE_PARTIAL_ENDPOINT_BLOCKED U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE  DIRECT_SOURCE_NATIVE_SPIN EXPOSURE_PROXY;BULLOCK_DISK_CONVERSION                   False                    False                  False external_review_select_or_reject_spin_normalization_route ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/run_ugc12506_beta_closure_carrier_review_response_intake.py | 0 | U12506_BETA_CARRIER_REVIEW_ACCEPTED_PREFREEZE_ALLOWED               True data/derived/ugc12506_beta_closure_carrier_review_response.csv BARYONIC_050_FAST_PACKET                       True                    False                  False build_beta_cl_transfer_carrier_prefreeze_manifest ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/build_ugc12506_beta_closure_transfer_carrier_freeze_gate.py | 0 | U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST BARYONIC_050_FAST_PACKET                 3                          1                      1                           1                      1                                True                   False              False                    False                      False build_beta_cl_transfer_formula_manifest ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/build_ugc12506_beta_closure_scoring_launch_gate.py | 0 | U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY           BULLOCK_DISK_CONVERSION                  9                 0             5                0                         11                      1                              True                    False                  False run_beta_cl_transfer_control_replay_scoring ugc12506_beta_closure_scoring_launch_gate_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/build_ugc12506_beta_closure_transfer_formula_freeze_gate.py | 0 | U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_READY_FOR_SCORING_RUNNER           BULLOCK_DISK_CONVERSION                       11             5                0                      True                                True                   False              False                    False                      False run_ugc12506_beta_closure_transfer_scoring ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |
| scripts/run_ugc12506_beta_closure_transfer_scoring.py | 0 | U12506_BETA_CLOSURE_TRANSFER_SCORING_COMPLETE_CONTROL_ONLY           BULLOCK_DISK_CONVERSION U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY            True                     True                     11 not blocked; separate scoring runner consumed frozen manifest            True               True                    False                      False review_control_only_scores_before_endpoint_claim ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |  | ugc12506_beta_closure_post_review_scoring_launcher_not_endpoint |

## Claim Boundary

If active responses are absent, this is only a blocked pre-scoring
artifact. If scoring later executes, it remains a control-only scoring
run until separately reviewed; no endpoint validation claim is made here.
