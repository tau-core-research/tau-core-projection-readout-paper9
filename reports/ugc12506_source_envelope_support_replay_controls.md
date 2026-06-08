# UGC12506 Source-Envelope Support Replay

This replay scores the residual-blind source-envelope support freeze.
It is not accepted endpoint validation.

## Summary

| replay_status | galaxy | n_points | carrier_rmse_km_s | old_prefrozen_combined_rmse_km_s | source_envelope_rmse_km_s | source_envelope_minus_old_prefrozen_rmse_km_s | source_envelope_minus_carrier_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | source_envelope_minus_prior_best_diagnostic_rmse_km_s | outer_mean_observed_minus_baryonic_km_s_last30pct | outer_mean_old_prefrozen_lift_km_s_last30pct | outer_mean_source_envelope_lift_km_s_last30pct | source_envelope_lift_fraction_of_outer_gap | formula_frozen_before_scoring | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_ENVELOPE_REPLAY_IMPROVES_OLD_PREFROZEN_BUT_NOT_PRIOR_DIAGNOSTICS | UGC12506 | 31 | 116.023 | 109.372 | 102.479 | -6.89286 | -13.5447 | TAU_BEST_FAMILY | 37.3633 | 65.1155 | 119.426 | 14.311 | 32.6762 | 0.273611 | True | False | True | False | ugc12506_source_envelope_support_replay_controls_not_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_PREFROZEN | source_envelope_positive_replay | 31 | 102.479 | 103.966 | 101.596 | -101.596 | False | True | False | ugc12506_source_envelope_support_replay_controls_not_validation |
| UGC12506 | UGC12506_OLD_HIGHS_PIN_PROJECTION_COMBINED_POSITIVE | old_prefrozen_reference | 31 | 109.372 | 110.333 | 109.041 | -109.041 | False | True | False | ugc12506_source_envelope_support_replay_controls_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_source_envelope_support_replay_controls_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_NEGATIVE_CONTROL | negative_sign_control | 31 | 138.036 | 137.748 | 135.314 | -135.314 | False | True | False | ugc12506_source_envelope_support_replay_controls_not_validation |

## Diagnostics

| diagnostic_id | status | value | claim_type |
| --- | --- | --- | --- |
| D1_STRENGTHENING | ENVELOPE_SUPPORT_STRONGER_THAN_OLD_PREFROZEN | -6.89286 | replay_numerical_evidence_not_validation |
| D2_BASELINE_COMPETITION | DOES_NOT_BEAT_PRIOR_BEST_DIAGNOSTIC | 65.1155 | diagnostic_reference_comparison |
| D3_OUTER_GAP_COVERAGE | OUTER_GAP_PARTIALLY_COVERED | 0.273611 | radial_zone_diagnostic |

![UGC12506 source-envelope replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_source_envelope_support_replay.png)
