# UGC12506 Source-Native NFW + High-Spin Envelope Replay

This replay scores the source-native NFW/HSE shell frozen from published
Table 5 halo parameters. It is a replay/control result, not endpoint
validation.

## Summary

| replay_status | galaxy | n_points | carrier_rmse_km_s | source_envelope_rmse_km_s | eea_rmse_km_s | old_rd_proxy_nfw_hse_rmse_km_s | source_native_nfw_hse_rmse_km_s | source_native_minus_old_rd_proxy_rmse_km_s | source_native_minus_eea_rmse_km_s | source_native_minus_envelope_rmse_km_s | source_native_minus_carrier_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | source_native_minus_prior_best_diagnostic_rmse_km_s | inner_mean_lift_km_s_first30pct | middle_mean_lift_km_s | outer_mean_lift_km_s_last30pct | outer_gap_coverage_fraction | formula_frozen_before_scoring | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NATIVE_NFW_HSE_REPLAY_IMPROVES_RD_PROXY_NOT_PRIOR_DIAGNOSTICS | UGC12506 | 31 | 116.023 | 102.479 | 102.432 | 77.8617 | 77.5409 | -0.320772 | -24.8912 | -24.9379 | -38.4826 | TAU_BEST_FAMILY | 37.3633 | 40.1776 | 37.8679 | 38.5139 | 39.3457 | 0.329458 | True | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE | source_native_nfw_highspin_envelope_positive_replay | 31 | 77.5409 | 77.8953 | 77.0438 | -77.0438 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |
| UGC12506 | UGC12506_OLD_RD_PROXY_NFW_HSE_POSITIVE | old_rd_proxy_nfw_hse_reference | 31 | 77.8617 | 78.2393 | 77.264 | -77.264 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |
| UGC12506 | UGC12506_EEA_POSITIVE_PREFROZEN | eea_reference | 31 | 102.432 | 103.914 | 101.542 | -101.542 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN | envelope_reference | 31 | 102.479 | 103.966 | 101.596 | -101.596 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_NEGATIVE | negative_sign_control | 31 | 178.269 | 178.819 | 177.57 | -177.57 | False | True | False | ugc12506_source_native_nfw_hse_replay_not_validation |

## Diagnostics

| diagnostic_id | status | value | claim_type |
| --- | --- | --- | --- |
| D1_SOURCE_NATIVE_VS_RD_PROXY | SOURCE_NATIVE_IMPROVES_RD_PROXY | -0.320772 | source_native_replay_comparison_not_validation |
| D2_SOURCE_FROZEN_BRANCH_IMPROVEMENT | SOURCE_NATIVE_IMPROVES_EEA | -24.8912 | replay_numerical_evidence_not_validation |
| D3_PRIOR_DIAGNOSTIC_GAP | SOURCE_NATIVE_DOES_NOT_REACH_PRIOR_TAU_BEST_DIAGNOSTIC | 40.1776 | diagnostic_reference_comparison |
| D4_OUTER_GAP_COVERAGE | OUTER_GAP_PARTIALLY_COVERED | 0.329458 | radial_zone_diagnostic |

![UGC12506 source-native NFW-HSE replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_source_native_nfw_hse_replay.png)
