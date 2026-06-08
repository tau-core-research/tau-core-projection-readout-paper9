# NGC4088 Time-Projection Double-Count Resolution Gate

This gate resolves the double-count risk between the additive warp/history
morphology kernel and the Xi_eff clock/readout control manifest. It uses
only frozen source-manifest information and does not inspect endpoint
residuals.

## Overlap Audit

| galaxy | xi_eff_feature | xi_eff_term_value | overlapping_additive_token | overlap_status | orthogonal_clock_residual_allowed | reason | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | f_PA | 0.25 | C_warp | SHARED_WARP_GEOMETRY | False | orientation mismatch is part of the same warp/history geometry family | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | f_R | 0.125 | x_w_formula_freeze | SHARED_ONSET_RADIAL_SUPPORT | False | radial onset/asymmetry information is already used by the additive kernel | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | f_q | 0.5 | q_warp | DIRECT_SOURCE_STRENGTH_OVERLAP | False | q_warp is already an additive-kernel source-strength factor | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | f_mem | 0.5 | sigma_warp | SHARED_HISTORY_PHASE | False | morphology-carried history phase is already assigned to the additive warp/history route | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |

## Policy

| galaxy | policy_id | accepted_combined_route | clock_only_route_status | additive_plus_clock_status | raw_clock_load_L | orthogonal_clock_load_L | epsilon_clock_candidate | epsilon_clock_orthogonal_combined | xi_eff_combined_policy | new_evidence_required_to_reopen_clock | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_TIME_PROJECTION_DOUBLE_COUNT_RESOLUTION_V1 | ADDITIVE_WARP_HISTORY_ONLY_FOR_COMBINED_ENDPOINT | CONTROL_ROUTE_ALLOWED_NOT_ENDPOINT | STRESS_TEST_REJECTED_FOR_ENDPOINT | 1.375 | 0 | 0.0202632 | 0 | Xi_eff=1 for additive-combined route until independent clock-only evidence exists | observer/path clock proxy or source-time observable that is not q_warp, x_w/onset, warp geometry, or morphology-history phase already used by additive kernel | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_DCR_G1_ADDITIVE_SOURCE_TOKENS_DECLARED | PASS | x_w_formula_freeze; q_warp; sigma_warp; C_warp | preserve additive-kernel provenance | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | N4088_DCR_G2_CLOCK_SOURCE_TOKENS_DECLARED | PASS | f_PA; f_R; f_q; f_mem | preserve Xi_eff source-term provenance | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | N4088_DCR_G3_OVERLAP_AUDIT | PASS_OVERLAP_COMPLETE | all current Xi_eff source terms overlap the additive warp/history route | set orthogonal clock residual to zero for combined route | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | N4088_DCR_G4_CLOCK_ONLY_CONTROL_ALLOWED | PASS_CONTROL_ONLY | ADDITIVE_PLUS_CLOCK_IMPROVES_BUT_DOUBLE_COUNT_BLOCKED | clock-only may be explored separately, not combined endpoint | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |
| NGC4088 | N4088_DCR_G5_COMBINED_ENDPOINT_POLICY | PASS_FREEZE_POLICY | accepted combined route uses Xi_eff=1 unless independent non-overlap clock evidence is supplied | build endpoint permission gate only for additive route or future non-overlap clock route | False | False | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |

## Summary

| double_count_resolution_status | galaxy | n_xi_eff_terms | n_overlapping_terms | raw_clock_load_L | orthogonal_clock_load_L | epsilon_clock_candidate | epsilon_clock_orthogonal_combined | accepted_combined_route | clock_only_control_preserved | additive_plus_clock_endpoint_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE | NGC4088 | 4 | 4 | 1.375 | 0 | 0.0202632 | 0 | additive_warp_history_with_Xi_eff_equal_one | True | False | False | False | if endpoint scoring is requested, score additive-only accepted route; reopen time endpoint only with independent non-overlap clock evidence | ngc4088_time_projection_double_count_resolution_gate_not_endpoint |

## Interpretation

The current NGC4088 Xi_eff terms are real source-side clock/readout
candidates, but they are not independent of the additive warp/history
morphology kernel. Therefore the accepted combined endpoint route sets
the orthogonal clock residual to zero. This preserves the time-projection
control result while preventing the same morphology/history evidence from
being counted twice.
