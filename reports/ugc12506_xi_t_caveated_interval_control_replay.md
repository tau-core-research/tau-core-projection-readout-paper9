# UGC12506 Xi_t Caveated Interval/Control Replay

This is a control replay, not a standard endpoint validation.

## Summary

| control_replay_status | galaxy | n_points | epsilon_t_max | xi_t_max_max | control_low_rmse_km_s | control_mid_rmse_km_s | control_high_rmse_km_s | best_control_edge_rmse_km_s | rmse_improvement_vs_low_km_s | interval_clipped_diagnostic_rmse_km_s | obs_inside_interval_fraction | obs_inside_interval_with_err_fraction | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_XI_T_CAVEATED_INTERVAL_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT | UGC12506 | 31 | 0.0238438 | 1.02384 | 77.5409 | 77.0114 | 76.4856 | 76.4856 | 1.05527 | 76.4856 | 0 | 0 | False | True | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | diagnostic_clipped_to_obs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_XIT_CONTROL_HIGH | control_interval_upper_edge | 31 | 76.4856 | 76.8751 | 76.0123 | -76.0123 | False | True | False | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | UGC12506_XIT_INTERVAL_CLIPPED_DIAGNOSTIC | best_possible_within_frozen_interval_not_model | 31 | 76.4856 | 76.8751 | 76.0123 | -76.0123 | False | True | True | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | UGC12506_XIT_CONTROL_MID | control_interval_midpoint | 31 | 77.0114 | 77.3831 | 76.5281 | -76.5281 | False | True | False | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | UGC12506_XIT_CONTROL_LOW_EPS0 | control_interval_lower_edge | 31 | 77.5409 | 77.8953 | 77.0438 | -77.0438 | False | True | False | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | NEWTONIAN_BARYONIC_V050 | baseline_reference | 31 | 116.023 | 116.637 | 115.618 | -115.618 | False | True | False | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_XIT_REPLAY_G1_MANIFEST_KIND | PASS | caveated_interval_control | none | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | U12506_XIT_REPLAY_G2_ENDPOINT_BLOCK | PASS_RECORDED | endpoint_scores_allowed=False | do not report as endpoint validation | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | U12506_XIT_REPLAY_G3_SCORING_SEPARATION | PASS | manifest/grid construction forbids vobs; this script reads vobs only for control scoring | none | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |
| UGC12506 | U12506_XIT_REPLAY_G4_INTERVAL_CLAIM_BOUNDARY | PASS_RECORDED | interval-clipped curve is diagnostic only and marked as such | separate endpoint-permission gate before endpoint claim | False | ugc12506_xi_t_caveated_interval_control_replay_not_endpoint |

## Claim Boundary

The lower, midpoint, and upper curves are fixed by the source-reviewed caveated interval/control manifest. The interval-clipped diagnostic reports the best possible within-band residual and is not a fitted model.

![UGC12506 Xi_t control replay](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_xi_t_caveated_interval_control_replay.png)
