# UGC12506 Source-Derived Beta-Closure Replay

This replay tests a source-only candidate for the missing NFW/HSE
normalization factor. It uses spin, NFW preference, and edge-on
projection exposure. It does not use vobs to compute beta, but the
candidate was formulated after the residual-aware normalization
diagnostic, so it remains post-diagnostic and not endpoint evidence.

## Summary

| source_beta_replay_status | galaxy | beta_source_closure | beta_diagnostic_all_point | beta_source_minus_diagnostic | beta_error_fraction | source_beta_rmse_km_s | source_beta_holdout_rmse_km_s | nominal_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | source_beta_minus_prior_best_diagnostic_rmse_km_s | uses_vobs_or_residual_for_beta | post_diagnostic_candidate | source_frozen_normalization_law_derived | endpoint_validation_claim | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_DERIVED_BETA_CLOSURE_REPLAY_MATCHES_DIAGNOSTIC_SHAPE_NOT_ENDPOINT | UGC12506 | 3.95422 | 3.8761 | 0.078121 | 0.0201545 | 7.67208 | 9.12084 | 77.5409 | TAU_BEST_FAMILY | 37.3633 | -29.6912 | False | True | False | False | source-only beta_cl reproduces the required normalization scale within five percent and beats prior diagnostic references, but it was formulated after the diagnostic and must be promoted only by independent source-side review or transfer tests | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |

## Derivation

| step | expression | value | status | galaxy | uses_vobs_or_residual | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BETA_0_LIMIT | beta_cl = 1 + source loads | 1 | PASS: no NFW preference and no edge-on load recovers nominal shell | UGC12506 | False | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |
| NFW_CLOSURE_LOAD | (lambda_spin/lambda_ref)*(chi2_iso/chi2_nfw - 1)_+ | 2.35714 | PASS: dimensionless source-side closure preference amplified by high spin | UGC12506 | False | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |
| EDGEON_PROJECTION_LOAD | sin^2(i)*max((i-80 deg)/10 deg,0) | 0.59708 | PASS: dimensionless edge-on projection exposure | UGC12506 | False | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |
| SOURCE_BETA | 1 + spin_load*nfw_preference_load + edgeon_load | 3.95422 | FORMULA_CANDIDATE: source-only but post-diagnostic | UGC12506 | False | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |

## Scores

| galaxy | model_id | role | beta | n_points | rmse_km_s | weighted_rmse_km_s | holdout_rmse_km_s | uses_vobs_for_beta | post_diagnostic_candidate | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_DIAGNOSTIC_ALL_POINT_BETA_REFERENCE | residual_aware_beta_reference | 3.8761 | 31 | 7.4787 | nan | 8.86153 | True | False | False | ugc12506_source_native_nfw_hse_residual_normalization_diagnostic_only |
| UGC12506 | UGC12506_SOURCE_DERIVED_BETA_CLOSURE_NFW_HSE | source_derived_beta_closure_candidate | 3.95422 | 31 | 7.67208 | 7.99069 | 9.12084 | False | True | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | nan | 31 | 37.3633 | nan | nan | False | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | nan | 31 | 38.1227 | nan | nan | False | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | nan | 31 | 40.6978 | nan | nan | False | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | nan | 31 | 44.9992 | nan | nan | False | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_NOMINAL | nominal_source_frozen_reference | 1 | 31 | 77.5409 | 77.8953 | 75.4993 | False | False | False | ugc12506_source_derived_beta_closure_post_diagnostic_candidate_not_endpoint |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | nan | 31 | 116.023 | nan | nan | False | False | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |

![UGC12506 source-derived beta-closure replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_source_derived_beta_closure_replay.png)
