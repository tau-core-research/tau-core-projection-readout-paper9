# UGC12506 Beta-Closure Spin Route Prefreeze Gate

This gate is downstream of the independent spin-proxy review intake.
It does not select a route and it does not run replay scores.

## Summary

| spin_route_prefreeze_status | selected_spin_normalization_route | n_prefrozen_transfer_rows | beta_cl_transfer_prefreeze_allowed | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE | BULLOCK_DISK_CONVERSION | 11 | True | False | False | False | build_beta_cl_transfer_replay_prefreeze_manifest | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |

## Gate

| gate_id | gate_status | reason | selected_spin_normalization_route | beta_cl_transfer_prefreeze_allowed | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BSP_PREFREEZE_1_INTAKE_ACCEPTED | PASS | independent review accepted a supported spin route | BULLOCK_DISK_CONVERSION | True | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |

## Prefrozen Values

| galaxy | selected_spin_normalization_route | lambda_spin_prefreeze_value | source_value_column | source_artifact | prefreeze_value_status | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | BULLOCK_DISK_CONVERSION | 0.0352494 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC7331 | BULLOCK_DISK_CONVERSION | 0.0325439 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC2841 | BULLOCK_DISK_CONVERSION | 0.0202436 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC0801 | BULLOCK_DISK_CONVERSION | 0.0291447 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC4013 | BULLOCK_DISK_CONVERSION | 0.00631325 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| ESO563-G021 | BULLOCK_DISK_CONVERSION | 0.00716317 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| UGC11455 | BULLOCK_DISK_CONVERSION | 0.00660234 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| IC4202 | BULLOCK_DISK_CONVERSION | 0.0678522 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC4157 | BULLOCK_DISK_CONVERSION | 0.00563934 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC3521 | BULLOCK_DISK_CONVERSION | 0.00267756 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |
| NGC4217 | BULLOCK_DISK_CONVERSION | 0.0231037 | lambda_bullock_disk_proxy | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | CAVEATED_BULLOCK_DISK_CONVERSION_REVIEW_ACCEPTED | False | False | False | ugc12506_beta_closure_spin_route_prefreeze_gate_not_endpoint |

## Claim Boundary

A passed route prefreeze would only create a source-frozen input map
for a later beta_cl transfer preflight. Endpoint scoring remains false
in this gate.
