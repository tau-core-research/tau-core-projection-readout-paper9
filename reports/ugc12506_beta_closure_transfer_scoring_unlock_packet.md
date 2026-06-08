# UGC12506 Beta-Closure Transfer Scoring Unlock Packet

This is the final pre-scoring handoff packet. It does not accept review
decisions and does not create active response files. It gives the
external reviewer exact response schemas and example-only rows.

## Summary

| unlock_packet_status | n_contract_ready_scenarios | n_required_active_response_files | n_active_response_files_present | n_example_only_response_files | zip_path | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING | 2 | 2 | 2 | 3 | review_bundles/ugc12506_beta_closure_transfer_scoring_unlock_packet.zip | False | False | False | False | external_reviewer_writes_active_response_files_then_run_intakes | ugc12506_beta_closure_transfer_scoring_unlock_packet_not_endpoint |

## Required Active Responses

| required_active_response | response_type | accepted_values | example_only_files | active_file_exists_now | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| data/derived/ugc12506_beta_closure_spin_proxy_review_response.csv | spin_route_review | source_fields_decision=ACCEPT_SOURCE_FIELDS; weight_rule_decision in {ACCEPT_EXPOSURE_RULE,ACCEPT_BULLOCK_CONVERSION}; selected_spin_normalization_route in {EXPOSURE_PROXY,BULLOCK_DISK_CONVERSION}; definition_boundary_decision=ACCEPT_CONTEXT_ONLY; transfer_scope_decision=ACCEPT_TARGET_SET; forbidden_inputs_used=False | data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_exposure_proxy.csv;data/derived/ugc12506_beta_closure_spin_proxy_review_response_example_only_bullock_conversion.csv | True | False | False | ugc12506_beta_closure_transfer_scoring_unlock_packet_not_endpoint |
| data/derived/ugc12506_beta_closure_carrier_review_response.csv | carrier_review | carrier_route_decision=ACCEPT_BARYONIC_STRESS_CARRIER; selected_carrier_id=BARYONIC_050_FAST_PACKET; li2020_policy_decision=KEEP_LI2020_CONTROL_ONLY; forbidden_inputs_used=False; endpoint_scores_allowed=False; uses_vobs_or_residual=False | data/derived/ugc12506_beta_closure_carrier_review_response_example_only_baryonic_stress.csv | True | False | False | ugc12506_beta_closure_transfer_scoring_unlock_packet_not_endpoint |

## Contract-Ready Dry-Run Scenarios

| dry_run_scenario_id | selected_spin_normalization_route | selected_carrier_id | n_formula_rows_if_accepted | n_fast_sparc_covered_galaxies | n_missing_fast_sparc_galaxies | missing_fast_sparc_galaxies | n_prediction_rows_without_vobs | min_beta_cl_value | max_beta_cl_value | mean_beta_cl_value | contract_ready_if_reviews_accept | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IF_REVIEW_ACCEPTS_EXPOSURE_PROXY_AND_BARYONIC_CARRIER | EXPOSURE_PROXY | BARYONIC_050_FAST_PACKET | 11 | 11 | 0 |  | 328 | 1 | 2.3365 | 1.62466 | True | False | False | False | False | ugc12506_beta_closure_transfer_scoring_contract_dry_run_not_endpoint |
| IF_REVIEW_ACCEPTS_BULLOCK_DISK_CONVERSION_AND_BARYONIC_CARRIER | BULLOCK_DISK_CONVERSION | BARYONIC_050_FAST_PACKET | 11 | 11 | 0 |  | 328 | 1 | 2.07946 | 1.56648 | True | False | False | False | False | ugc12506_beta_closure_transfer_scoring_contract_dry_run_not_endpoint |

## Claim Boundary

The example-only rows are not active review responses. Scoring remains
blocked until an independent reviewer writes the active response files
and the standard intake, prefreeze, formula-freeze, and scoring-launch
gates pass.
