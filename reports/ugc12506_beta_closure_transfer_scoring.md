# UGC12506 Beta-Closure Transfer Scoring Runner

This is the separate scoring runner. In the current state it blocks before
reading any rotation-curve observation because the launch gate has not
passed and the frozen transfer formula manifest is missing or empty.

## Summary

| transfer_scoring_status | selected_spin_normalization_route | launch_status | launch_allowed | formula_manifest_exists | formula_manifest_rows | blocked_reason | scores_written | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_TRANSFER_SCORING_COMPLETE_CONTROL_ONLY | BULLOCK_DISK_CONVERSION | U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY | True | True | 11 | not blocked; separate scoring runner consumed frozen manifest | True | True | False | False | review_control_only_scores_before_endpoint_claim | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |

## Gates

| gate_id | gate_status | reason | allowed_to_read_vobs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| BETA_TRANSFER_SCORE_1_LAUNCH_ALLOWED | PASS | U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY | False | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| BETA_TRANSFER_SCORE_2_FORMULA_MANIFEST_PRESENT | PASS | formula_manifest_exists=True; rows=11 | False | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| BETA_TRANSFER_SCORE_3_VOBS_READ_PERMISSION | PASS | vobs may be read only by this scoring runner after launch and formula freeze pass | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |

## Scores

| galaxy | model_id | route_id | selected_spin_normalization_route | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESO563-G021 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 30 | 82.3851 | 68.5627 | 75.5587 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| ESO563-G021 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 30 | 117.98 | 101.435 | 109.262 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| IC4202 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 32 | 33.1457 | 37.0042 | 21.1329 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| IC4202 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 32 | 74.9449 | 68.7414 | 72.7434 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC0801 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 13 | 34.9094 | 38.5503 | 29.6642 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC0801 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 13 | 53.9554 | 59.8419 | 48.5931 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC0891 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 18 | 44.1537 | 46.1584 | 40.3612 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC0891 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 18 | 74.3456 | 52.7398 | 56.6557 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC2841 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 50 | 132.311 | 145.033 | 129.327 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC2841 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 50 | 138.401 | 150.372 | 135.85 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC3521 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 41 | 35.2082 | 38.8106 | 29.2375 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC3521 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 41 | 35.2082 | 38.8106 | 29.2375 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4013 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 36 | 38.1373 | 37.543 | 32.256 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4013 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 36 | 68.9573 | 65.5054 | 65.6415 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4157 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 17 | 36.1603 | 29.8717 | 30.8343 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4157 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 17 | 52.8814 | 48.6191 | 45.8448 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4217 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 19 | 47.6208 | 45.1658 | 43.7178 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC4217 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 19 | 54.9994 | 52.5589 | 42.5024 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC7331 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 36 | 57.0089 | 58.4672 | 49.456 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| NGC7331 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 36 | 60.0217 | 62.3992 | 51.6057 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| UGC11455 | BETA_CL_TRANSFER_SOURCE_FROZEN | BETA_CL_TRANSFER_SOURCE_FROZEN | BULLOCK_DISK_CONVERSION | 36 | 39.4854 | 41.2726 | 35.9095 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |
| UGC11455 | BARYONIC_050_FAST_PACKET_CARRIER_REFERENCE | carrier_reference | BULLOCK_DISK_CONVERSION | 36 | 60.0521 | 59.0839 | 52.0731 | False | True | False | ugc12506_beta_closure_transfer_scoring_runner_not_endpoint |

## Scoring Points

Wrote 328 scored point rows to `data/derived/ugc12506_beta_closure_transfer_scoring_points.csv`.

## Claim Boundary

This artifact is either a scoring-path guard or, after all launch gates
pass, a control-only scoring artifact. It preserves the rule that
observed rotation curves may only be read by this separate scoring
script after all residual-blind freeze gates pass.
