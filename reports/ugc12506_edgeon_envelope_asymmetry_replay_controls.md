# UGC12506 Edge-on + Envelope + Asymmetry Replay

This replay scores the frozen EEA formula shell. It is not accepted
endpoint validation and it does not include the image-plane interloper
as a gravity/path kernel.

## Summary

| replay_status | galaxy | n_points | carrier_rmse_km_s | old_prefrozen_combined_rmse_km_s | source_envelope_rmse_km_s | eea_positive_rmse_km_s | eea_minus_source_envelope_rmse_km_s | eea_minus_old_prefrozen_rmse_km_s | eea_minus_carrier_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | eea_minus_prior_best_diagnostic_rmse_km_s | outer_mean_observed_minus_baryonic_km_s_last30pct | outer_mean_source_envelope_lift_km_s_last30pct | outer_mean_eea_lift_km_s_last30pct | eea_lift_fraction_of_outer_gap | formula_frozen_before_scoring | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_EEA_REPLAY_IMPROVES_SOURCE_FROZEN_KERNELS_NOT_PRIOR_DIAGNOSTICS | UGC12506 | 31 | 116.023 | 109.372 | 102.479 | 102.432 | -0.0466523 | -6.93951 | -13.5914 | TAU_BEST_FAMILY | 37.3633 | 65.0688 | 119.426 | 32.6762 | 32.7925 | 0.274585 | True | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_EEA_POSITIVE_PREFROZEN | edgeon_envelope_asymmetry_positive_replay | 31 | 102.432 | 103.914 | 101.542 | -101.542 | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN | source_envelope_reference | 31 | 102.479 | 103.966 | 101.596 | -101.596 | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |
| UGC12506 | UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE | old_prefrozen_reference | 31 | 109.372 | 110.333 | 109.041 | -109.041 | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_EEA_NEGATIVE_CONTROL | negative_sign_control | 31 | 138.196 | 137.934 | 135.444 | -135.444 | False | True | False | ugc12506_edgeon_envelope_asymmetry_replay_controls_not_validation |

## Diagnostics

| diagnostic_id | status | value | claim_type |
| --- | --- | --- | --- |
| D1_SOURCE_FROZEN_IMPROVEMENT | EEA_IMPROVES_ENVELOPE_SUPPORT | -0.0466523 | replay_numerical_evidence_not_validation |
| D2_PRIOR_DIAGNOSTIC_GAP | EEA_DOES_NOT_REACH_PRIOR_TAU_BEST_DIAGNOSTIC | 65.0688 | diagnostic_reference_comparison |
| D3_OUTER_GAP_COVERAGE | EEA_PARTIALLY_COVERS_OUTER_GAP | 0.274585 | radial_zone_diagnostic |

![UGC12506 EEA replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_edgeon_envelope_asymmetry_replay.png)
