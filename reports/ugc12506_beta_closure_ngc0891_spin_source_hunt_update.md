# NGC0891 Beta-Closure Spin Source Hunt Update

This update checks NGC891/NGC0891 literature context for a direct
halo/envelope `lambda_spin` value. The context strengthens the
halo/envelope/projection motivation, but no checked source supplies the
dimensionless beta_cl `lambda_spin` slot.

## Summary

| ngc0891_spin_source_hunt_status | n_sources_checked | n_context_sources_accepted | n_direct_lambda_values_accepted | direct_lambda_spin_status | proxy_review_status | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891_CONTEXT_STRENGTHENED_DIRECT_LAMBDA_STILL_BLOCKED | 4 | 4 | 0 | still_missing | response_pending | False | False | False | independent_spin_proxy_review_response_or_new_direct_lambda_source | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |

## Sources Checked

| source_id | galaxy | source_reference | source_url | source_status | direct_lambda_spin_value | accepted_context | definition_issue | accepted_as_beta_cl_lambda_spin | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OOSTERLOO2007_COLD_HI_HALO | NGC0891 | Oosterloo, Fraternali & Sancisi 2007, AJ 134, 1019 | https://arxiv.org/abs/0705.4034 | CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA |  | Huge H I halo, about 30 percent of total H I; lagging differential rotation; possible low-angular-momentum accretion | Provides halo gas angular-momentum context, not a dimensionless halo/envelope lambda_spin measurement for beta_cl | False | False | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |
| FRATERNALI_BINNEY2006_DYNAMICAL_MODEL | NGC0891 | Fraternali & Binney 2006, MNRAS 366, 449 | https://academic.oup.com/mnras/article/366/2/449/1214630 | CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA |  | Dynamical extraplanar-gas model; NGC 891 channel maps constrain halo/fountain kinematics and kick geometry | Model parameters and kick geometry are not direct source-native lambda_spin values | False | False | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |
| FRATERNALI_OOSTERLOO2004_EXTRA_PLANAR_NEUTRAL_GAS | NGC0891 | Fraternali et al. 2004, extra-planar neutral gas in NGC 891 | https://arxiv.org/abs/astro-ph/0410375 | CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA |  | 3D modelling reports halo gas rotating more slowly than disk and a vertical gradient of roughly -15 km/s/kpc | Kinematic lag supports envelope/projection context but does not define beta_cl lambda_spin | False | False | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |
| CIOTTI_FRATERNALI2009_STATIONARY_MODELS | NGC0891 | Ciotti, Fraternali et al. 2009/2010, MNRAS 401, 2451 | https://academic.oup.com/mnras/article/401/4/2451/1127410 | CONTEXT_ACCEPTED_NO_DIRECT_LAMBDA |  | Stationary extraplanar-gas models are applied to NGC 891 to test vertical rotation decrease | Potential/extraplanar-gas model context, not a halo-spin source | False | False | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |

## Remaining Worklist

| required_field | current_status | acceptable_evidence | forbidden_inputs | next_gate | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| ngc0891_direct_halo_or_envelope_lambda_spin | STILL_MISSING_AFTER_SOURCE_HUNT_UPDATE | direct dimensionless halo/envelope spin parameter, or a residual-blind conversion theorem from accepted source-native kinematic/angular-momentum observables | rotation residuals; endpoint RMSE; baseline rank; post-hoc beta selection | direct_source_search_or_independent_proxy_review_response | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |
| ngc0891_proxy_review_decision | PENDING_INDEPENDENT_REVIEW_RESPONSE | completed spin-proxy review response accepting source fields, weight rule or caveated replacement, definition boundary, and target scope | rotation residuals; endpoint scores; direct disc-lambda insertion | run_spin_proxy_review_response_intake | False | ugc12506_beta_closure_ngc0891_spin_source_hunt_update_not_endpoint |

## Claim Boundary

The source hunt strengthens context but does not unlock replay. The
admissible next gate remains either an independent proxy-review response
or a new direct source-native lambda/spin source.
