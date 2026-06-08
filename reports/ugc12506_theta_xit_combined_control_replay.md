# UGC12506 Theta_morph + Xi_t Combined-Control Replay

This replay is controlled by the source-nonoverlap ledger. It is not an endpoint.

## Summary

| combined_control_status | galaxy | n_points | epsilon_t_cap | theta_rmse_km_s | combined_cap_only_rmse_km_s | combined_shared_kt_high_rmse_km_s | cap_only_minus_theta_rmse_km_s | shared_kt_high_minus_theta_rmse_km_s | best_scored_model | best_scored_rmse_km_s | combined_control_replay_allowed | combined_endpoint_allowed | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_THETA_XIT_COMBINED_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT | UGC12506 | 31 | 0.0238438 | 64.1192 | 60.3087 | 63.2141 | -3.81049 | -0.905044 | UGC12506_THETA_XIT_CAP_ONLY_COMBINED_CONTROL | 60.3087 | True | False | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |

## Scores

| galaxy | model_id | model_role | channel_policy | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_THETA_XIT_CAP_ONLY_COMBINED_CONTROL | ledger_strict_combined_control | theta_only_shape_plus_xit_only_cap | 31 | 60.3087 | 61.4278 | 58.4795 | -58.4795 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | UGC12506_THETA_XIT_SHARED_KT_HIGH_STRESS_CONTROL | shared_context_stress_control_high | theta_shape_plus_caveated_shared_context_xit_shape | 31 | 63.2141 | 64.4873 | 61.2108 | -61.2108 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | UGC12506_THETA_XIT_SHARED_KT_MID_STRESS_CONTROL | shared_context_stress_control_mid | theta_shape_plus_caveated_shared_context_xit_shape | 31 | 63.6614 | 64.9001 | 61.8292 | -61.8292 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | UGC12506_THETA_MORPH_PHASE | theta_additive_diagnostic_base | theta_only_late_settling_shape | 31 | 64.1192 | 65.3242 | 62.4477 | -62.4477 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | UGC12506_PROJECTION_HISTORY | projection_history_reference | reference_only | 31 | 69.1788 | 70.0189 | 68.4276 | -68.4276 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | source_native_reference | reference_only | 31 | 77.5409 | 77.8953 | 77.0438 | -77.0438 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| UGC12506 | NEWTONIAN_BARYONIC_V050 | baseline_reference | reference_only | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |

## Gates

| gate_id | gate_status | evidence | endpoint_scores_allowed | galaxy | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| U12506_COMBINED_G1_NONOVERLAP_LEDGER | PASS_CONTROL_ONLY | PARTIAL_NONOVERLAP_CONTROL_ALLOWED_COMBINED_ENDPOINT_BLOCKED | False | UGC12506 | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| U12506_COMBINED_G2_LEDGER_STRICT_ROUTE | PASS_CONTROL_ONLY | Theta-only late-settling shape plus Xi_t-only epsilon cap | False | UGC12506 | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| U12506_COMBINED_G3_SHARED_KT_ROUTE | CAVEATED_STRESS_CONTROL_ONLY | shaped K_t(R) still uses shared source context | False | UGC12506 | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |
| U12506_COMBINED_G4_ENDPOINT_BOUNDARY | BLOCK_ENDPOINT | combined_endpoint_allowed=False in nonoverlap summary | False | UGC12506 | False | ugc12506_theta_xit_combined_control_replay_not_endpoint |

## Ledger interpretation

The primary combined-control curve uses the Theta_morph late-settling shape
and only the Xi_t protocol cap.  The shaped K_t curve is retained as a
caveated stress control because the current K_t shape still uses shared
high-spin/envelope/asymmetry source context.

## Figure

![UGC12506 combined control replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_theta_xit_combined_control_replay.png)

