# Projection Channel Source-Token Priority Protocol

This protocol decides how residual-blind source tokens are assigned when the same datum could support morphology/projection and time/clock projection.

## Summary

| protocol_id | main_rule | formal_test | reviewer_guardrail | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| PROJECTION_CHANNEL_SOURCE_TOKEN_PRIORITY_V1 | assign each source token to the most direct predeclared readout channel; time projection receives only independent clock/readout content or quotient-surviving remainder | time endpoint load is carried by T/A, where A is the active morphology/projection source subspace and T is the time-projection source ledger | endpoint RMSE cannot decide channel priority | False | False | projection_channel_priority_protocol_not_endpoint |

## Rules

| priority | rule_id | condition | endpoint_assignment | time_projection_allowed | reason | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | DIRECT_READOUT_FIRST | source token directly describes geometry, morphology, warp, asymmetry, bar/ring, vertical overlay, or observer/path appearance | morphology_or_observer_projection_kernel | no, unless an independent clock/readout aspect is separately frozen | the most direct readout consumes the token first | False | False | projection_channel_priority_protocol_not_endpoint |
| 2 | TIME_REQUIRES_CLOCK_CONTENT | source token describes component settling, relaxation state, multi-waveband phase offset, lag/clock mismatch, or path-clock evidence not already used by morphology | time_or_clock_projection_channel | yes, if non-overlap ledger passes | time projection needs clock/readout meaning beyond shape alone | False | False | projection_channel_priority_protocol_not_endpoint |
| 3 | ONE_TOKEN_ONE_ENDPOINT_CHANNEL | same token could be read by multiple projection channels | single predeclared channel only | only for quotient-surviving remainder T/A | prevents counting the same source evidence twice | False | False | projection_channel_priority_protocol_not_endpoint |
| 4 | LOWER_ONTOLOGICAL_LEVEL_WINS_TIES | source token supports both ordinary morphology/projection and deeper time/clock interpretation with no independent separator | morphology_or_projection_kernel | control only | deeper time/clock claims require stronger independent evidence | False | False | projection_channel_priority_protocol_not_endpoint |
| 5 | RESIDUAL_CANNOT_BREAK_TIES | two channel assignments remain ambiguous | block endpoint or keep weaker/direct channel | diagnostic/control only | rotation residuals and RMSE cannot decide the source assignment | False | False | projection_channel_priority_protocol_not_endpoint |

## Examples

| example_token | direct_assignment | time_assignment | ngc4088_status | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| warp onset / x_w | warp/history morphology kernel | blocked unless separate settling-clock evidence exists | assigned to additive warp/history; Xi_t overlap | False | projection_channel_priority_protocol_not_endpoint |
| q_warp / warp strength | warp/history source-strength factor | blocked as direct source-strength overlap | assigned to additive warp/history; Xi_t overlap | False | projection_channel_priority_protocol_not_endpoint |
| position-angle/orientation mismatch | observer/path or warp geometry projection | control unless source proves clock-slice mismatch | shared warp geometry; no orthogonal clock load | False | projection_channel_priority_protocol_not_endpoint |
| component lag or settling state independent of warp | not consumed by shape alone if separately measured | candidate clock/readout channel | not currently available as non-overlapping source token | False | projection_channel_priority_protocol_not_endpoint |
| line-of-sight foreground/path environment | path projection only if source-native causal-path evidence exists | candidate observer/path clock channel | not primary for current route | False | projection_channel_priority_protocol_not_endpoint |

Operationally, the time-projection endpoint load is measured in the quotient T/A. A is the active morphology/projection source subspace; T is the candidate time-projection source ledger. If a time token is already in A, it may remain a control but not an endpoint contribution.
