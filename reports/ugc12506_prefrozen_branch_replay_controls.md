# UGC12506 Prefrozen Branch Replay Controls

This is a caveated single-galaxy control replay. It reads `vobs` only
after the source-normalized formula inputs have been frozen. It is not
a population-validation endpoint.

## Summary

| replay_status | galaxy | n_points | carrier_rmse_km_s | best_prefrozen_branch_model | best_prefrozen_branch_role | best_prefrozen_branch_rmse_km_s | best_positive_prefrozen_model | best_positive_prefrozen_rmse_km_s | best_positive_minus_carrier_rmse_km_s | best_branch_minus_carrier_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | best_positive_minus_prior_best_diagnostic_rmse_km_s | outer_mean_observed_minus_baryonic_km_s_last8 | outer_mean_combined_positive_lift_km_s_last8 | lift_fraction_of_outer_gap_last8 | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | population_validation_claim | claim_boundary | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_PREFROZEN_BRANCH_REPLAY_COMPLETE_NOT_VALIDATION | UGC12506 | 31 | 116.023 | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN | combined_positive_branch | 109.372 | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN | 109.372 | -6.65185 | -6.65185 | TAU_BEST_FAMILY | 37.3633 | 72.0083 | 118.372 | 15.0917 | 0.127494 | False | True | False | False | ugc12506_prefrozen_branch_replay_controls_not_validation | prefrozen control replay; if weak, diagnose source-normalized amplitude/kernel strength rather than retuning from residuals |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN | combined_positive_branch | 31 | 109.372 | 110.333 | 109.041 | -109.041 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_PROJECTION_ASYMMETRY_POSITIVE_PREFROZEN | source_prefrozen_positive_branch | 31 | 110.869 | 111.752 | 110.548 | -110.548 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_SPLIT_HS_MINUS_PA_PLUS_CONTROL | split_sign_control | 31 | 112.416 | 113.219 | 112.089 | -112.089 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_HIGHS_PIN_POSITIVE_PREFROZEN | source_prefrozen_positive_branch | 31 | 114.351 | 115.052 | 113.992 | -113.992 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_HIGHS_PIN_NEGATIVE_ATTENUATION_CONTROL | negative_sign_control | 31 | 117.76 | 118.282 | 117.288 | -117.288 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_SPLIT_HS_PLUS_PA_MINUS_CONTROL | split_sign_control | 31 | 119.944 | 120.351 | 119.363 | -119.363 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_PROJECTION_ASYMMETRY_NEGATIVE_CONTROL | negative_sign_control | 31 | 121.844 | 122.152 | 121.147 | -121.147 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |
| UGC12506 | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_NEGATIVE_CONTROL | combined_negative_control | 31 | 123.832 | 124.037 | 122.994 | -122.994 | False | True | False | ugc12506_prefrozen_branch_replay_controls_not_validation |

## Diagnostics

| diagnostic_id | status | value | interpretation |
| --- | --- | --- | --- |
| D1_AMPLITUDE_STRENGTH | AMPLITUDE_TOO_WEAK_FOR_OUTER_GAP | 0.1274935939423399 | Compares the source-frozen combined positive branch lift to the outer observed-baryonic gap. Low values mean the replay is source-clean but underpowered. |
| D2_SIGN_BRANCH | POSITIVE_BRANCH_IS_BEST_PREFROZEN_BRANCH | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN | Sign is not promoted from this replay; this only diagnoses branch behavior. |
| D3_PRIOR_BASELINE_COMPARISON | POSITIVE_REPLAY_DOES_NOT_BEAT_PRIOR_BEST_DIAGNOSTIC | 72.0083 | Prior diagnostics are not identical baselines for this replay, but they expose whether the new frozen branch is numerically competitive. |

## Claim Boundary

Negative or weak results are preserved. Any change to the kernel, sign,
or amplitude after this score demotes the next run to diagnostic unless
it is justified by new residual-blind source evidence and replayed as a
new frozen protocol.
