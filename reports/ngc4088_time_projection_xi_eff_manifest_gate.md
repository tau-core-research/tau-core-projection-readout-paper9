# NGC4088 Time-Projection Xi_eff Manifest Gate

This promotion gate uses the accepted q_warp/m_history source review
and the residual-blind B_i coefficient protocol. It does not read
rotation residuals and does not permit endpoint scoring.

## Manifest

| galaxy | manifest_status | formula_text | kernel_text | raw_source_bound_L | gamma_clock | epsilon_cap_protocol | epsilon_clock_candidate | xi_eff_min | xi_eff_max | xi_path_policy | source_review_ready | bi_rule_ready | small_mismatch_ready | double_count_blocker | control_manifest_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | NGC4088_XI_EFF_CONTROL_MANIFEST_READY_ENDPOINT_BLOCKED | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R); Xi_path=1 for this route | Xi_eff(R)=1+epsilon_clock*K_t(R); K_t inherits reviewed warp-history phase shape | 1.375 | 0.578947 | 0.035 | 0.0202632 | 1 | 1.02026 | Xi_path=1; no path term is primary for NGC4088 route | True | True | True | True | True | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |

## Source Terms

| galaxy | feature_symbol | feature_value | coefficient_B_i | term_value | term_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | f_PA | 0.5 | 0.5 | 0.25 | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | f_R | 0.25 | 0.5 | 0.125 | ACCEPTED_FROM_FROZEN_DIGITIZATION_VALIDATION | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | f_q | 1 | 0.5 | 0.5 | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | f_mem | 1 | 0.5 | 0.5 | ACCEPTED_FOR_PROTOCOL_NUMERIC_BOUND | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | N4088_XIEFF_G1_QMEM_SOURCE_REVIEW | PASS | SOURCE_RESPONSES_ACCEPTED_FOR_PROTOCOL_BOUND | none | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | N4088_XIEFF_G2_BI_RULE_READY | PASS | NUMERIC_EPSILON_PROTOCOL_BOUND_READY | none | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | N4088_XIEFF_G3_SMALL_MISMATCH_PROTOCOL | PASS_PROTOCOL | epsilon_clock_candidate=0.0202632 <= 0.035 | derive the cap from Tau-side clock geometry before universal claim | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | N4088_XIEFF_G4_PATH_POLICY | PASS_ZERO_PATH | Xi_path fixed to one for this NGC4088 warp-history route | do not activate path term without independent path evidence | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | N4088_XIEFF_G5_DOUBLE_COUNT_SEPARATION | BLOCKED | NGC4088 already has an additive warp-history morphology kernel; the clock/readout contribution must be separated by an ablation manifest | build additive-kernel vs Xi_eff clock ablation before endpoint scoring | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |
| NGC4088 | N4088_XIEFF_G6_ENDPOINT_PERMISSION | BLOCKED | endpoint_scores_allowed=False | endpoint scoring requires a separate accepted endpoint permission gate | False | False | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |

## Summary

| xi_eff_manifest_status | galaxy | raw_source_bound_L | epsilon_clock_candidate | xi_trial_status | control_manifest_allowed | endpoint_scores_allowed | blocking_gate | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088_XI_EFF_CONTROL_READY_ENDPOINT_BLOCKED | NGC4088 | 1.375 | 0.0202632 | P1_PROMOTE_AFTER_SOURCE_REVIEW | True | False | N4088_XIEFF_G5_DOUBLE_COUNT_SEPARATION | build additive-warp/history vs Xi_eff clock ablation manifest; no endpoint scoring yet | ngc4088_time_projection_xi_eff_manifest_gate_not_endpoint |

## Interpretation

NGC4088 has moved beyond the q_warp/m_history blocker: the source
terms and B_i rule are now available for a control manifest. The
remaining scientific blocker is double-count separation: the Xi_eff
clock/readout layer must be separated from the already active additive
warp-history morphology kernel before any endpoint score is allowed.
