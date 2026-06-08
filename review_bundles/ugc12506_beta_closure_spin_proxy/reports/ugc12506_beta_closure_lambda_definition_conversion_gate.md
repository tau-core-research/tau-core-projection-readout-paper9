# NGC7331 Lambda Definition-Conversion Gate

This gate audits whether the Marr (2015) NGC7331 disc-spin value can
fill the beta_cl halo/envelope lambda_spin slot. It cannot be directly
substituted.

## Summary

| definition_conversion_status | direct_disc_lambda_context_accepted | direct_substitution_allowed | conversion_rule_available | beta_cl_replay_allowed | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331_DISC_LAMBDA_CONTEXT_ACCEPTED_DIRECT_SUBSTITUTION_REJECTED | True | False | False | False | False | derive_residual_blind_disc_to_halo_envelope_conversion_or_keep_proxy_review | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |

## Checks

| check_id | question | result | reason | endpoint_permission | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| C1_same_physical_object | Does the source lambda measure the same halo/envelope spin slot as beta_cl? | FAIL | Marr lambda is a disc-spin parameter in a lognormal self-gravitating disc model. | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |
| C2_same_normalization_role | Can lambda=0.423 be used against lambda_ref=0.10 without conversion? | FAIL | The beta_cl lambda slot is a source-normalization amplifier, not a universal disc-spin constant. | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |
| C3_residual_blind_source | Is the Marr value source-side and residual-blind? | PASS_CONTEXT | The value is literature source context and does not use the endpoint residual. | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |
| C4_conversion_rule_available | Is there a predeclared disc-to-halo/envelope conversion rule? | FAIL | No residual-blind conversion functional from disc lambda to beta_cl lambda_spin is accepted. | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |

## Numeric Comparison

| galaxy | lambda_disc_marr2015 | lambda_spin_proxy_candidate | lambda_ref | nfw_preference_load | edgeon_load | beta_if_direct_disc_lambda_substituted | beta_if_proxy_candidate_used | direct_minus_proxy_beta | direct_substitution_allowed | proxy_replay_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | 0.423 | 0.135758 | 0.1 | 0.17284 | 0 | 1.73111 | 1.23464 | 0.496468 | False | False | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |

## Required Conversion Worklist

| required_object | required_evidence | forbidden_inputs | status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| disc_to_halo_envelope_lambda_conversion | source-side relation between disc angular-momentum lambda and halo/envelope lambda_spin for the beta_cl closure slot | rotation residual; endpoint score; best-fit beta; wrong-family rank | MISSING | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |
| ngc7331_direct_halo_or_envelope_spin | direct source-native halo/envelope spin or accepted kinematic proxy | rotation residual; endpoint score | MISSING | False | ugc12506_beta_closure_lambda_definition_conversion_gate_not_endpoint |

## Claim Boundary

Marr (2015) is accepted as source-side angular-momentum context for
NGC7331. It is not accepted as the beta_cl lambda_spin value because
the beta_cl slot is a halo/envelope closure-normalization quantity.
No replay or endpoint score is allowed by this gate.
