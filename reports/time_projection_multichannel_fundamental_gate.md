# Time Projection Multichannel Fundamental Gate

This artifact separates the broader Tau Core time-projection idea from the narrow Xi_t control factors used in the current numerical tests.

## Definitions

| object_id | definition | meaning | inactive_limit | status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| XI_MORPH | Xi_morph(R;Theta_src^tau) | source-intrinsic morphology clock/phase readout factor | Xi_morph -> 1 for settled regular source morphology | FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL | time_projection_multichannel_fundamental_gate_not_endpoint |
| XI_OBS | Xi_obs(R;O_obs/path) | observer/path-selected clock slice and visibility factor | Xi_obs -> 1 for ordinary projection with no independent clock evidence | FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL | time_projection_multichannel_fundamental_gate_not_endpoint |
| XI_PATH | Xi_path(R;E_proj/history) | null-bundle/path-environment clock-readout factor | Xi_path -> 1 when path/environment evidence is absent | FUNDAMENTAL_CHANNEL_PROPOSED_FORMULA_CONDITIONAL | time_projection_multichannel_fundamental_gate_not_endpoint |
| XI_EFF | Xi_eff = Xi_morph Xi_obs Xi_path | effective total time-readout factor used by the observed velocity quotient | Xi_eff -> 1 if all time-projection channels are inactive | DERIVED_FROM_FACTOR_DEFINITION | time_projection_multichannel_fundamental_gate_not_endpoint |

## Formula Shells

| formula_id | formula | claim_type | dimension_check | known_limit | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| MULTICHANNEL_TIME_READOUT_SHELL | v_obs^2=Xi_eff^2(R)[v_Newt^2+delta_v_morph^2(R;Theta_src^tau,O_obs/path)] | formula_conditional_shell | PASS: Xi_eff dimensionless; bracket has velocity squared units | Xi_morph=Xi_obs=Xi_path=1 recovers morphology/gravity readout without time projection | time_projection_multichannel_fundamental_gate_not_endpoint |
| LINEARIZED_MULTICHANNEL_TIME_READOUT | Xi_i=1+epsilon_i; delta_v_t^2 ~= 2(epsilon_morph+epsilon_obs+epsilon_path)[v_Newt^2+delta_v_morph^2] | first_order_small_mismatch | PASS: epsilon_i are dimensionless | all epsilons zero gives delta_v_t^2=0 | time_projection_multichannel_fundamental_gate_not_endpoint |
| KERNEL_DEFORMATION_CHANNEL | K_readout(R)=K_0(R;K_present)+deltaK_morph_time(R;Theta_src^tau)+deltaK_obs_time(R;O_obs/path) | kernel_shape_channel | PASS if K terms are dimensionless and amplitudes carry velocity squared units | deltaK terms vanish for settled morphology and inactive observer/path clock evidence | time_projection_multichannel_fundamental_gate_not_endpoint |

## Theorem Audit

| theorem_id | verdict | formal_claim | proven_part | unproven_part | weakest_step | minimal_corrected_statement | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TIME_PROJECTION_MULTICHANNEL_FACTORIZATION | PLAUSIBLE_BUT_NOT_FULLY_DERIVED | If time projection is a readout-level mismatch rather than an added force, it must be allowed to act both on source morphology phase and on observer/path clock slicing. | A dimensionless multiplicative clock factor gives the correct velocity-squared scaling and Newtonian limit. | The Tau-side origin and normalization of Xi_morph, Xi_obs, and Xi_path are not yet derived from a completed clock geometry. | mapping source observables to epsilon_morph, epsilon_obs, and epsilon_path without residual leakage | Time projection should be treated as a multichannel formula-conditional readout layer; current Xi_t tests only instantiate a narrow source-reviewed control slice. | time_projection_multichannel_fundamental_gate_not_endpoint |

## Current Implementation Audit

| implementation | covers_xi_morph | covers_xi_obs | covers_xi_path | covers_kernel_deformation | status | consequence | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| current_trial_Xi_t | partial | partial | no | no | diagnostic_proxy_only | cannot test full fundamental time-projection branch | time_projection_multichannel_fundamental_gate_not_endpoint |
| UGC12506_caveated_interval_control | partial_highspin_envelope_clock | partial_edgeon_pv_clock_slice | explicitly_zero | no | source_reviewed_narrow_control_not_endpoint | small improvement does not falsify broader time-projection channel | time_projection_multichannel_fundamental_gate_not_endpoint |
| future_full_time_projection_kernel | required | required | optional_source_evidence_dependent | required | not_built | needed before strong claim about time projection strength | time_projection_multichannel_fundamental_gate_not_endpoint |

## Gates

| gate_id | gate_status | required_condition | forbidden_shortcut | claim_boundary |
| --- | --- | --- | --- | --- |
| TPMULTI_G1_CHANNEL_SEPARATION | REQUIRED | Freeze Xi_morph, Xi_obs, and Xi_path separately, with Xi_path allowed to be exactly one. | one fitted epsilon_t absorbing all missing amplitude | time_projection_multichannel_fundamental_gate_not_endpoint |
| TPMULTI_G2_SOURCE_MORPHOLOGY_TIME | OPEN | Define source-intrinsic morphology clock/phase observables: settling, warp phase, high-spin envelope state, interaction history. | infer source time phase from rotation residual | time_projection_multichannel_fundamental_gate_not_endpoint |
| TPMULTI_G3_OBSERVER_PROJECTION_TIME | OPEN | Define observer/path clock-slice observables: inclination, edge-on overlay, PV/envelope visibility, beam/null-bundle geometry. | treat generic inclination as clock evidence without source-review support | time_projection_multichannel_fundamental_gate_not_endpoint |
| TPMULTI_G4_KERNEL_AND_CLOCK_ABLATION | OPEN | Run ablations: morphology kernel only, +source time, +observer time, +path time, +kernel deformation. | claim full time projection from a single combined replay | time_projection_multichannel_fundamental_gate_not_endpoint |

## Summary

| multichannel_status | current_xi_t_tests_status | main_conclusion | next_step | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| TIME_PROJECTION_FUNDAMENTAL_MULTICHANNEL_GATE_RECORDED_NOT_DERIVED | narrow_proxy_or_control_only | The weak UGC12506 Xi_t control improvement does not test the full fundamental time-projection branch. | build separate source-morphology-time and observer-projection-time manifests before any full time-projection endpoint | False | time_projection_multichannel_fundamental_gate_not_endpoint |
