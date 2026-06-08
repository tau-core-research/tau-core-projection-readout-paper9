# Time-Readout Projection Channel Gate

This artifact records the formula-conditional Tau Core branch in which projection can modify the effective clock/readout factor used in the observed rotation curve.

It is not an endpoint validation and does not define an accepted `Xi_t(R)` manifest.

## Formulas

| formula_id | formula | status | interpretation | claim_boundary |
| --- | --- | --- | --- | --- |
| TIME_READOUT_FULL_SHELL | v_obs^2(R)=Xi_t^2(R;O_obs/path,Theta_morph,E_proj/history)[v_Newt^2(R)+delta_v_grav/morph^2(R)] | FORMULA_CONDITIONAL | projection-dependent clock/readout mismatch, not an extra force | time_readout_projection_channel_formula_conditional_not_endpoint |
| TIME_READOUT_LINEARIZED_SHELL | Xi_t(R)=1+epsilon_t(R); delta_v_t^2(R) ~= 2 epsilon_t(R)[v_Newt^2(R)+delta_v_grav/morph^2(R)] | FORMULA_CONDITIONAL_SMALL_MISMATCH | first-order diagnostic form for small clock/readout mismatch | time_readout_projection_channel_formula_conditional_not_endpoint |

## Gates

| gate_id | required_condition | forbidden_inputs | current_status | claim_boundary |
| --- | --- | --- | --- | --- |
| TIME_G1_SOURCE_FROZEN_XI_T | Xi_t(R) or epsilon_t(R) is fixed from source-side observer/path, morphology-trajectory, or clock-readout evidence before scoring | rotation residual, best Tau family, MOND/RAR/TPG rank, per-galaxy residual tuning | OPEN_NO_ACCEPTED_XI_T_MANIFEST | time_readout_projection_channel_formula_conditional_not_endpoint |
| TIME_G2_NEWTONIAN_CLOCK_LIMIT | Xi_t -> 1 in regular quiet systems or in source states with no projection-time evidence | post-hoc suppression chosen after seeing endpoint score | THEORY_REQUIREMENT_RECORDED | time_readout_projection_channel_formula_conditional_not_endpoint |
| TIME_G3_SEPARATE_FROM_GRAVITY_AMPLITUDE | time-readout factor is multiplicative and separated from additive morphology/gravity residual amplitude | absorbing failed amplitude normalization into Xi_t | FORMULA_SEPARATION_RECORDED | time_readout_projection_channel_formula_conditional_not_endpoint |
| TIME_G4_ABLATION_REQUIRED | future endpoint must compare base morphology, observer/path, trajectory phase, and time-readout layers as separate ablations | claiming a full time-projection success from a morphology-phase-only replay | OPEN_NEXT_PROTOCOL_STEP | time_readout_projection_channel_formula_conditional_not_endpoint |

## Projection Subchannels

| subchannel | what_changes | formula_role | source_freeze_requirement | current_status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| observer_path_projection | which source clock slice is visible along the line of sight or light bundle | argument of Xi_t through O_obs/path | inclination, edge-on overlay, warp visibility, beam/path geometry, foreground or path-environment audit | PROXY_PARTIAL_IN_PAPER2 | time_readout_projection_channel_formula_conditional_not_endpoint |
| morphology_trajectory_phase | whether the current 4D morphology is a settled or phase-shifted readout slice | argument of Xi_t through Theta_morph | settling state, warp/asymmetry stage, interaction history, relaxation or future-directed phase proxies | DIAGNOSTIC_PROXY_ONLY | time_readout_projection_channel_formula_conditional_not_endpoint |
| gravity_readout_projection | morphology/gravity residual is multiplied by the clock factor | Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2] | separate morphology/gravity residual shell frozen before time-readout scoring | FORMULA_SEPARATION_RECORDED | time_readout_projection_channel_formula_conditional_not_endpoint |
| clock_rate_time_slice_projection | effective time parameter used in the observed velocity quotient | Xi_t=1+epsilon_t; delta_v_t^2 ~= 2 epsilon_t (...) | residual-blind clock/readout mismatch proxy | OPEN_NO_ACCEPTED_PROXY | time_readout_projection_channel_formula_conditional_not_endpoint |
| path_environment_projection | metric/matter environment of the observed light bundle can affect the clock/readout factor | possible E_proj/history dependence in Xi_t | source-observer null-geodesic bundle environment; reject image-plane coincidences without path evidence | OPEN_PATH_AWARE_KERNEL_NOT_MODELED | time_readout_projection_channel_formula_conditional_not_endpoint |

## Summary

| channel_status | accepted_endpoint_ready | reason | next_step | claim_boundary |
| --- | --- | --- | --- | --- |
| TIME_READOUT_PROJECTION_BRANCH_DEFINED_NOT_VALIDATED | False | No residual-blind Xi_t(R) manifest is accepted yet; current full-time morphology replay is only a diagnostic proxy. | Define source observables for Xi_t, freeze a per-galaxy manifest, then run staged ablation endpoints. | time_readout_projection_channel_formula_conditional_not_endpoint |
