# UGC12506 Theta Morphology Phase Replay

This diagnostic computes a trajectory/phase-enriched UGC12506 rotation curve.
The construction does not treat future-directed morphology as backward
causality. It treats `Theta_morph` as a source-frozen trajectory/phase
proxy supported by high spin, extended low-density H I, high inclination,
and mild H I extent asymmetry.

Status: `DIAGNOSTIC_ONLY_NOT_ENDPOINT_VALIDATION`.

## Summary

| diagnostic_status | galaxy | n_points | carrier_rmse_km_s | source_native_nfw_hse_rmse_km_s | projection_history_rmse_km_s | theta_morph_phase_rmse_km_s | theta_minus_projection_history_rmse_km_s | theta_minus_source_native_rmse_km_s | best_scored_model | best_scored_rmse_km_s | theta_load | gamma_theta | q_spin | q_low_density_stability | q_asymmetry_phase | amplitude_theta_km2_s2 | formula_text | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_THETA_MORPH_PHASE_IMPROVES_PROJECTION_HISTORY_DIAGNOSTIC | UGC12506 | 31 | 116.023 | 77.5409 | 69.1788 | 64.1192 | -5.05967 | -13.4217 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | 37.3633 | 0.490933 | 0.329279 | 1 | 0.4 | 0.666667 | 7532.03 | v_theta^2(R)=v_projection_history^2(R)+A_theta K_theta(R); K_theta is source-frozen late-settling morphology phase | False | True | False | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | prior_diagnostic_reference_not_same_carrier | 31 | 37.3633 | nan | 31.2433 | -30.4602 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_MOND | prior_diagnostic_reference_not_same_carrier | 31 | 38.1227 | nan | 32.1727 | -30.6564 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TPG_V6 | prior_diagnostic_reference_not_same_carrier | 31 | 40.6978 | nan | 35.8406 | -35.5699 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_TAU_MATCHED | prior_diagnostic_reference_not_same_carrier | 31 | 44.9992 | nan | 41.0543 | -41.0543 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |
| UGC12506 | UGC12506_THETA_MORPH_PHASE_POSITIVE | trajectory_phase_enriched_diagnostic | 31 | 64.1192 | 65.3242 | 62.4477 | -62.4477 | False | True | False | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| UGC12506 | UGC12506_INCREMENTAL_PROJECTION_HISTORY_POSITIVE | projection_history_reference | 31 | 69.1788 | 70.0189 | 68.4276 | -68.4276 | False | True | False | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE_POSITIVE | source_native_base_reference | 31 | 77.5409 | 77.8953 | 77.0438 | -77.0438 | False | True | False | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| UGC12506 | BARYONIC_CARRIER_V050 | carrier_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| UGC12506 | PRIOR_DIAGNOSTIC_NEWTONIAN_vn | prior_diagnostic_reference_not_same_carrier | 31 | 116.023 | nan | 115.618 | -115.618 | False | True | False | prior_multigalaxy_fit_inspection_reference_not_endpoint_validation |

## Gates

| gate_id | gate_status | evidence | endpoint_claim_allowed | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| U12506_THETA_G1_SOURCE_PROXY | PASS_DIAGNOSTIC_SOURCE_SUPPORTED | lambda_spin=0.15, extended low-density H I, high inclination, and mild H I asymmetry | False | UGC12506 | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| U12506_THETA_G2_NO_BACKWARD_CAUSAL_CLAIM | PASS_CLAIM_BOUNDARY | Theta_morph is treated as trajectory/phase, not future-to-present 4D causality | False | UGC12506 | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| U12506_THETA_G3_RESIDUAL_BLIND_CONSTRUCTION | PASS | kernel, load, sign, and amplitude use source observables and source-native carrier scale | False | UGC12506 | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |
| U12506_THETA_G4_STATUS | DIAGNOSTIC_ONLY | theta phase proxy is not yet accepted population observable | False | UGC12506 | ugc12506_theta_morph_phase_replay_diagnostic_not_validation |

## Figure

![UGC12506 theta morphology phase replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_theta_morph_phase_replay.png)

## Claim boundary

A positive or negative score here is kernel-development evidence only.
The trajectory/phase proxy must still be promoted to an accepted
source-side observable before endpoint-style claims.
