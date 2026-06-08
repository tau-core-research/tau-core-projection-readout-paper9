# UGC12506 Source-Native NFW/HSE Normalization Diagnostic

This is a residual-aware shape diagnostic. It keeps the source-native
NFW/HSE kernel fixed and fits only one scalar velocity-squared amplitude
multiplier. Because the multiplier uses v_obs, it is not endpoint
evidence and not a source-frozen Tau Core normalization law.

## Summary

| normalization_diagnostic_status | galaxy | n_points | beta_all_point_v2 | beta_train_split_v2 | nominal_rmse_km_s | all_point_normalized_rmse_km_s | train_normalized_holdout_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | all_point_minus_prior_best_diagnostic_rmse_km_s | diagnostic_used_vobs_or_residual | source_frozen_normalization_law_derived | endpoint_validation_claim | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NATIVE_NFW_HSE_SHAPE_NORMALIZES_WELL_DIAGNOSTIC_ONLY | UGC12506 | 31 | 3.8761 | 3.91021 | 77.5409 | 7.4787 | 8.86153 | TAU_BEST_FAMILY | 37.3633 | -29.8846 | True | False | False | fixed source-native NFW/HSE shape can be made competitive only by a residual-aware scalar normalization; this identifies the missing source-side amplitude law and is not endpoint evidence | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |

## Scores

| galaxy | model_id | normalization_role | beta | n_points | rmse_km_s | weighted_rmse_km_s | holdout_rmse_km_s | uses_vobs_for_normalization | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_ALL_POINT_NORMALIZED | residual_aware_shape_diagnostic | 3.8761 | 31 | 7.4787 | 7.60674 | 8.72841 | True | False | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_TRAIN_NORMALIZED | train_split_residual_aware_shape_diagnostic | 3.91021 | 31 | 7.51467 | 7.72747 | 8.86153 | True | False | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | nan | 31 | 37.3633 | nan | nan | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | nan | 31 | 38.1227 | nan | nan | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | nan | 31 | 40.6978 | nan | nan | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | nan | 31 | 44.9992 | nan | nan | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_NOMINAL | source_frozen_nominal_reference | 1 | 31 | 77.5409 | 77.8953 | 75.4993 | False | False | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 0 | 31 | 116.023 | 116.637 | 113.635 | False | False | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | nan | 31 | 116.023 | nan | nan | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |

![UGC12506 source-native NFW/HSE normalization diagnostic](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_source_native_nfw_hse_normalization_diagnostic.png)
