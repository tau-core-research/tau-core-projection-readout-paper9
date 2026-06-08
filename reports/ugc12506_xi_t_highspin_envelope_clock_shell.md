# UGC12506 Xi_t High-Spin/Envelope Clock Shell

This formula shell defines a source-only candidate `Xi_t(R)` for
UGC12506. It does not score an endpoint and does not promote an
accepted time-readout manifest.

## Summary

| formula_shell_status | galaxy | epsilon_t | source_load_total | path_load | accepted_xi_t_manifest_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_XI_T_SOURCE_SHELL_BUILT_ACCEPTED_MANIFEST_BLOCKED | UGC12506 | 0.0238438 | 2.13728 | 0 | False | False | False | independent review or Tau-side derivation of epsilon_t normalization; then accepted Xi_t manifest gate | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |

## Manifest

| galaxy | formula_id | formula_text | velocity_readout_role | kernel_text | epsilon_rule | source_load_total | gamma_clock | epsilon_t | path_load | path_policy | dimension_check | known_limits | formula_frozen_before_scoring | accepted_xi_t_manifest_allowed | endpoint_scores_allowed | construction_used_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | Xi_t(R)=1+epsilon_t K_t(R) | v_obs^2 = Xi_t^2 [v_Newt^2 + delta_v_grav/morph^2] | K_t=norm[w_spin K_spin + w_edge K_spin + w_env K_env + w_asym K_asym + 0*K_path] | epsilon_t=min(0.035, 0.035*Gamma_clock), Gamma_clock=L/(1+L) | 2.13728 | 0.681253 | 0.0238438 | 0 | foreground/path term set to zero because path evidence is not established | PASS: Xi_t and K_t are dimensionless | all source loads zero gives Xi_t=1; path evidence absent gives K_path coefficient zero | True | False | False | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |

## Components

| galaxy | component_id | component_status | source_load | normalized_weight | kernel_column | source_basis | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | T_HIGHSPIN_SETTLING | INCLUDED_SOURCE_SUPPORTED | 1 | 0.467884 | K_t_highspin_clock_spin | reported high-spin state lambda=0.15 | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | T_EDGEON_PV_CLOCK_SLICE | INCLUDED_SOURCE_SUPPORTED | 0.59708 | 0.279365 | K_t_highspin_clock_spin | high inclination and PV/envelope method required | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | T_ENVELOPE_SETTLING | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.457272 | 0.21395 | K_t_highspin_clock_envelope | large diffuse low-density H I support | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | T_ASYMMETRIC_PV_PHASE | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.0829278 | 0.0388006 | K_t_highspin_clock_asymmetry | approaching/receding side shape and length asymmetry | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | T_PATH_ENVIRONMENT | EXCLUDED_NOT_ESTABLISHED | 0 | 0 | K_t_path_environment | foreground/path object evidence is not established | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | U12506_XIT_G1_SOURCE_INTAKE | PASS | P1 intake exists and endpoint is blocked | none | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | U12506_XIT_G2_PATH_ZERO_POLICY | PASS | foreground/path object status is NOT_ESTABLISHED | new cone/path review required before any nonzero path term | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | U12506_XIT_G3_DIMENSION_AND_LIMITS | PASS | Xi_t, epsilon_t, and K_t are dimensionless; Xi_t=1 limit explicit | none | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | U12506_XIT_G4_ACCEPTED_MANIFEST | BLOCKED | epsilon_t rule is a source-shell candidate, not an accepted Tau-side clock law | derive or externally review epsilon_t normalization before endpoint scoring | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |
| UGC12506 | UGC12506_XI_T_HIGHS_PIN_ENVELOPE_CLOCK_SHELL | U12506_XIT_G5_NO_ENDPOINT_SCORING | PASS_RECORDED | no vobs/residual used; endpoint_scores_allowed=False | run only after accepted Xi_t manifest promotion | False | ugc12506_xi_t_highspin_envelope_clock_shell_not_endpoint |

## Claim Boundary

The shell is source-only and residual-blind. The foreground/path term
is explicitly zero under the current source audit. The remaining blocker
is the accepted origin of the `epsilon_t` normalization law.
