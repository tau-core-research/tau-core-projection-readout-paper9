# UGC12506 Beta-Closure Direct Lambda/Spin Source Gate

This gate records a direct-source search for the two primary
beta-closure transfer targets. It does not authorize a replay.

## Summary

| direct_lambda_spin_gate_status | n_primary_targets_checked | n_direct_values_accepted_for_beta_cl | n_candidate_definition_mismatch_values | n_model_analogue_context_values | ngc7331_status | ngc0891_status | endpoint_scores_allowed | beta_cl_replay_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_BETA_CLOSURE_DIRECT_LAMBDA_SOURCE_GATE_PARTIAL_ENDPOINT_BLOCKED | 2 | 0 | 1 | 1 | disc_lambda_candidate_definition_conversion_required | direct_lambda_blocked_proxy_or_new_source_required | False | False | definition_conversion_review_for_ngc7331_or_direct_spin_source_for_ngc0891 | ugc12506_beta_closure_direct_lambda_spin_source_gate_not_endpoint |

## Evidence

| galaxy | source_field | source_status | source_value | source_uncertainty | definition | source_reference | source_url | accepted_as_beta_cl_lambda_spin | uses_vobs_or_residual | endpoint_scores_allowed | notes | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | disc_spin_lambda | CANDIDATE_DIRECT_DISC_LAMBDA_DEFINITION_MISMATCH | 0.423 |  | disc spin parameter from lognormal self-gravitating disc model; not the same object as the beta_cl halo/envelope lambda_spin slot | Marr 2015, MNRAS 453, 2214, Table 1; NGC 7331 row | https://academic.oup.com/mnras/article/453/2/2214/1146982 | False | False | False | Useful as a direct angular-momentum reference. Requires a definition-conversion review before it can replace lambda_spin_proxy. | ugc12506_beta_closure_direct_lambda_spin_source_gate_not_endpoint |
| NGC0891 | halo_spin_lambda | BLOCKED_NO_DIRECT_SOURCE_NATIVE_VALUE_FOUND |  |  | direct source-native halo/envelope spin value | No accepted direct NGC0891 lambda_spin value cached by this gate |  | False | False | False | PV/envelope context is accepted from earlier source-freeze preflight, but the spin slot remains blocked or proxy-review dependent. | ugc12506_beta_closure_direct_lambda_spin_source_gate_not_endpoint |
| NGC0891 | model_analogue_lambda | MODEL_ANALOGUE_CONTEXT_NOT_SOURCE_NATIVE_FREEZE | 0.038 |  | Milky-Way-like simulation/model analogue spin parameter discussed for NGC891-like extraplanar H I context; not a direct observed NGC0891 value | Kaufmann/Mayer-style NGC891 analogue context as summarized in lecture/source material | https://www.mpifr-bonn.mpg.de/1180177/tue_Lucio.pdf | False | False | False | May inform source review, but cannot be inserted into beta_cl replay. | ugc12506_beta_closure_direct_lambda_spin_source_gate_not_endpoint |

## Interpretation

NGC7331 has a published disc-spin-like value in Marr (2015), but its
definition is not the same as the beta_cl halo/envelope lambda_spin
slot. NGC0891 remains blocked for a direct lambda_spin value; the
available NGC891-like lambda context is model-analogue material only.
Therefore the admissible next step is either a definition-conversion
review for NGC7331, direct source-native spin acquisition for NGC0891,
or independent review of the already declared source-only proxy rule.
