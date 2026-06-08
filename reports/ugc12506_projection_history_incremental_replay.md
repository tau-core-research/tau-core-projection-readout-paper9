# UGC12506 Incremental Projection-History Replay

This replay scores the caveated incremental projection-history shell on
top of the source-native NFW-HSE base. It is not endpoint validation.

## Summary

| replay_status | galaxy | n_points | carrier_rmse_km_s | source_native_nfw_hse_rmse_km_s | projection_history_incremental_rmse_km_s | projection_history_minus_source_native_rmse_km_s | projection_history_minus_carrier_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | projection_history_minus_prior_best_diagnostic_rmse_km_s | inner_mean_increment_km_s_first30pct | middle_mean_increment_km_s | outer_mean_increment_km_s_last30pct | outer_gap_after_source_native_coverage_fraction | formula_frozen_before_scoring | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_INCREMENTAL_PROJECTION_HISTORY_IMPROVES_SOURCE_NATIVE_BASE_NOT_PRIOR_DIAGNOSTICS | UGC12506 | 31 | 116.023 | 77.5409 | 69.1788 | -8.36204 | -46.8446 | TAU_BEST_FAMILY | 37.3633 | 31.8155 | 0.212245 | 5.67734 | 20.2529 | 0.252909 | True | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE | incremental_projection_history_positive_replay | 31 | 69.1788 | 70.0189 | 68.4276 | -68.4276 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE | source_native_base_reference | 31 | 77.5409 | 77.8953 | 77.0438 | -77.0438 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | UGC12506_OLD_RD_PROXY_NFW_HSE_POSITIVE | old_rd_proxy_reference | 31 | 77.8617 | 78.2393 | 77.264 | -77.264 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_NEGATIVE | negative_sign_control | 31 | 88.2861 | 88.2192 | 86.8561 | -86.8561 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | UGC12506_EEA_POSITIVE_PREFROZEN | eea_reference | 31 | 102.432 | 103.914 | 101.542 | -101.542 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN | envelope_reference | 31 | 102.479 | 103.966 | 101.596 | -101.596 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_projection_history_incremental_replay_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |

## Diagnostics

| diagnostic_id | status | value | claim_type |
| --- | --- | --- | --- |
| D1_INCREMENTAL_IMPROVEMENT | IMPROVES_SOURCE_NATIVE_BASE | -8.36204 | caveated_control_replay_not_validation |
| D2_PRIOR_DIAGNOSTIC_GAP | GAP_REMAINS_TO_PRIOR_DIAGNOSTIC | 31.8155 | diagnostic_reference_comparison |
| D3_OUTER_GAP_AFTER_SOURCE_NATIVE_COVERAGE | OUTER_GAP_PARTIALLY_COVERED | 0.252909 | radial_zone_diagnostic |

![UGC12506 incremental projection-history replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_projection_history_incremental_replay.png)
