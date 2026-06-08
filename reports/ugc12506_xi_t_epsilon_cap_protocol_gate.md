# UGC12506 Xi_t Epsilon-Cap Protocol Gate

This gate freezes the small-mismatch cap used by the UGC12506 Xi_t
source shell as a conservative protocol constant. It does not claim
that the cap is a universal Tau Core constant and does not allow
endpoint scoring.

## Cap Theorem

| galaxy | cap_gate_id | cap_status | statement | derived_bound | eta_quad | epsilon_linear_bound | epsilon_cap | safety_fraction_of_bound | max_quadratic_to_linear_ratio | max_v2_fractional_shift | universal_constant_claim | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_XI_T_SMALL_MISMATCH_CAP_PROTOCOL | PROTOCOL_CAP_FROZEN_WITHIN_LINEAR_REGIME_NOT_UNIVERSAL_CONSTANT | For Xi_t=1+epsilon_t, the neglected quadratic term in Xi_t^2 is epsilon_t^2.  Relative to the linear correction 2 epsilon_t, this is epsilon_t/2.  Requiring a <=2% second-order-to-linear ratio gives epsilon_t <= 0.04. The protocol cap epsilon_cap=0.035 is a conservative predeclared value inside that admissible interval. | epsilon_t <= 2 eta_quad | 0.02 | 0.04 | 0.035 | 0.875 | 0.0175 | 0.071225 | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |

## Derivation Steps

| galaxy | step_id | claim_type | status | statement | formula_consequence | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | C1_TIME_SHELL | definition | PASS | Use the small-mismatch shell Xi_t=1+epsilon_t. | Xi_t^2=1+2epsilon_t+epsilon_t^2. | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | C2_LINEARIZATION_ERROR | derived_ratio | PASS | The quadratic-to-linear correction ratio is epsilon_t/2. | A small cap controls the validity of the linearized readout interpretation. | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | C3_ADMISSIBLE_BOUND | protocol_tolerance | PASS_CONDITIONAL | Choose eta_quad=0.02 as a predeclared maximum second-order-to-linear ratio. | epsilon_t must be <=0.04. | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | C4_PROTOCOL_CAP | protocol_freeze | PASS_PROTOCOL_FREEZE | Freeze epsilon_cap=0.035 as a conservative value below 0.04. | UGC12506 epsilon_t=0.023844 remains below the cap and in the linear regime. | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | C5_UNIVERSAL_ORIGIN | claim_boundary | OPEN | This does not derive epsilon_cap as a universal Tau Core constant. | Population use requires predeclared class-cap policy or deeper Tau-side clock geometry. | False | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_CAP_G1_BOUND_DERIVED | PASS_CONDITIONAL | eta_quad=0.02; epsilon_linear_bound=0.04 | eta_quad is a protocol tolerance, not a measured physical constant | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | U12506_CAP_G2_CAP_WITHIN_BOUND | PASS | epsilon_cap=0.035 < 0.04; safety_fraction=0.875 | none for current protocol freeze | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | U12506_CAP_G3_CURRENT_EPSILON_WITHIN_CAP | PASS | epsilon_t=0.0238438; gamma_clock=0.681253 | none for source-shell replay | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |
| UGC12506 | U12506_CAP_G4_NOT_UNIVERSAL | PASS_RECORDED | cap is frozen as conservative protocol constant only | derive deeper Tau-side clock cap before claiming universal law | False | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |

## Summary

| cap_protocol_status | galaxy | eta_quad | epsilon_linear_bound | epsilon_cap | epsilon_t | max_quadratic_to_linear_ratio_at_cap | max_v2_fractional_shift_at_cap | accepted_as_protocol_cap | universal_tau_constant_derived | endpoint_scores_allowed | uses_vobs_or_residual | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_EPSILON_CAP_PROTOCOL_FROZEN_NOT_UNIVERSAL | UGC12506 | 0.02 | 0.04 | 0.035 | 0.0238438 | 0.0175 | 0.071225 | True | False | False | False | if promoted, run accepted-manifest gate that records cap as predeclared protocol constant, not universal law | ugc12506_xi_t_epsilon_cap_protocol_gate_not_endpoint |

## Claim Boundary

`epsilon_cap=0.035` is accepted here only as a conservative
predeclared small-mismatch protocol cap inside the linearization
admissible interval. It is not a universal constant and does not
turn the diagnostic source shell into endpoint validation.
