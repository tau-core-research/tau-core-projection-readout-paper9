# UGC12506 Beta-Closure Spin Route Decision Matrix

This matrix compares residual-blind spin-normalization routes for the
UGC12506 beta_cl transfer problem. It does not choose a route, run a
replay, or authorize endpoint scoring.

## Summary

| spin_route_decision_matrix_status | n_routes | n_reviewable_not_accepted | direct_source_status | review_intake_status | prefreeze_status | preferred_scientific_route | current_practical_routes | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_SPIN_ROUTE_DECISION_MATRIX_READY_REVIEW_REQUIRED | 4 | 2 | UGC12506_BETA_CLOSURE_DIRECT_LAMBDA_SOURCE_GATE_PARTIAL_ENDPOINT_BLOCKED | U12506_BETA_SPIN_PROXY_REVIEW_ACCEPTED_PREFLIGHT_ALLOWED | U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE | DIRECT_SOURCE_NATIVE_SPIN | EXPOSURE_PROXY;BULLOCK_DISK_CONVERSION | False | False | False | external_review_select_or_reject_spin_normalization_route | ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |

## Route Matrix

| route_id | route_status | normalization_definition | ngc0891_lambda_value | ngc7331_lambda_value | source_basis | main_strength | main_risk | review_decision_needed | prefreeze_if_accepted | replay_if_accepted_here | endpoint_scores_allowed | uses_vobs_or_residual | forbidden_interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPOSURE_PROXY | REVIEWABLE_NOT_ACCEPTED | lambda_ref*(1+0.35 extent+0.25 velocity+0.25 gas+0.15 edgeon) | 0.1492670953236405 | 0.1357578448582519 | SPARC RHI/Rdisk, Vflat, H I mass, inclination | captures envelope/exposure load explicitly | weight coefficients are protocol candidates, not derived spin theory | ACCEPT_EXPOSURE_RULE or reject/replace | True | False | False | False | not a direct lambda_spin measurement | ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |
| BULLOCK_DISK_CONVERSION | REVIEWABLE_NOT_ACCEPTED | lambda'_disk=(2 Rdisk Vflat)/(sqrt(2) R200 V200) | 0.0352494086104112 | 0.0325438896465119 | SPARC Rdisk,Vflat plus Li2020 NFW-flat V200 | standard angular-momentum conversion control | disk specific angular momentum may not fill halo/envelope closure slot | ACCEPT_BULLOCK_CONVERSION or reject/replace | True | False | False | False | not accepted as Tau-side beta_cl spin slot without review | ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |
| DIRECT_SOURCE_NATIVE_SPIN | PREFERRED_BUT_CURRENTLY_MISSING | source-native halo/envelope lambda_spin |  |  | future direct source-native spin measurement or accepted conversion | cleanest definition match | not currently available for the beta_cl slot | supply direct source or keep route blocked | True | False | False | False | Marr disc lambda cannot be inserted directly | ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |
| REJECT_ROUTE | VALID_NEGATIVE_REVIEW_OUTCOME | none |  |  | review rejects all available spin-normalization routes | preserves negative result and blocks amplitude rescue | UGC12506 beta_cl transfer remains unresolved | reject proxy route or require new residual-blind rule | False | False | False | False | not a Tau Core failure; only route failure | ugc12506_beta_closure_spin_route_decision_matrix_not_endpoint |

## Claim Boundary

The cleanest scientific route remains a direct source-native halo/envelope
spin measurement. The two currently computable routes are reviewable
controls only. If all routes are rejected, that is a preserved route-level
negative result rather than a Tau Core endpoint failure.
