# NGC4088 Time-Projection Ablation Control Replay

This is a control replay, not an accepted endpoint.  The manifest was
frozen before scoring; observed velocities are used only inside this
script to compute control RMSEs.

## Summary

| ablation_replay_status | galaxy | epsilon_clock_candidate | best_control_model | best_control_rmse_km_s | base_rmse_km_s | additive_rmse_km_s | clock_only_rmse_km_s | additive_plus_clock_rmse_km_s | interpretation | endpoint_scores_allowed | endpoint_validation_claim | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088_XIEFF_ABLATION_CONTROL_REPLAY_COMPLETE_NOT_ENDPOINT | NGC4088 | 0.0202632 | N4088_ADDITIVE_PLUS_XIEFF_STRESS | 8.38352 | 11.619 | 9.39119 | 10.4959 | 8.38352 | ADDITIVE_PLUS_CLOCK_IMPROVES_BUT_DOUBLE_COUNT_BLOCKED | False | False | if clock-only is useful, build a separate accepted clock-only endpoint route; otherwise keep Xi_eff as diagnostic/control | ngc4088_time_projection_ablation_control_replay_not_endpoint |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_ADDITIVE_PLUS_XIEFF_STRESS | double_count_stress_control | 12 | 8.38352 | nan | 7.08285 | -1.53893 | False | True | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |
| NGC4088 | N4088_ADDITIVE_WARP_HISTORY | additive_reference | 12 | 9.39119 | nan | 7.90641 | -2.48202 | False | True | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |
| NGC4088 | N4088_XIEFF_CLOCK_ONLY_ON_BASE | clock_ablation_control | 12 | 10.4959 | nan | 8.72925 | -3.35797 | False | True | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |
| NGC4088 | N4088_BASE_PROJECTION | reference | 12 | 11.619 | nan | 9.64302 | -4.27668 | False | True | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |

## Gates

| gate_id | gate_status | evidence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| N4088_ABL_G1_MANIFEST_FROZEN | PASS | NGC4088_XI_EFF_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |
| N4088_ABL_G2_ENDPOINT_BLIND_CONSTRUCTION | PASS | scoring script reads vobs only after manifest construction | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |
| N4088_ABL_G3_DOUBLE_COUNT_NOT_RESOLVED | BLOCKED | additive_plus_clock remains stress test, not accepted endpoint model | False | ngc4088_time_projection_ablation_control_replay_not_endpoint |

## Claim Boundary

The additive-plus-clock curve is explicitly a double-count stress test.
It cannot be promoted until the clock/readout channel is separated from
the additive warp-history morphology kernel by a predeclared endpoint
route.

Figure: `/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ngc4088_time_projection_ablation_control_replay.png`
