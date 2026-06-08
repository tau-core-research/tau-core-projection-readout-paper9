# UGC12506 Beta-Closure Source-Declared Spin Proxy Gate

This gate declares a residual-blind spin/envelope exposure proxy for
the beta-closure transfer route. It is a protocol candidate, not an
accepted literature spin measurement and not an endpoint replay.

## Summary

| spin_proxy_gate_status | n_proxy_rows | n_transfer_rows | n_primary_proxy_review_targets | n_secondary_proxy_review_targets | primary_targets | secondary_targets | lambda_ref | proxy_formula | proxy_promotion_status | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_BETA_CLOSURE_SOURCE_DECLARED_SPIN_PROXY_BUILT_ENDPOINT_BLOCKED | 12 | 11 | 1 | 4 | NGC0891 | NGC7331;NGC2841;NGC0801;NGC4013 | 0.1 | lambda_spin_proxy=lambda_ref*(1 + 0.35*extent_load + 0.25*velocity_load + 0.25*gas_load + 0.15*edgeon_load) | not_accepted_as_lambda_spin_measurement | False | independent_review_or_direct_spin_values_before_beta_cl_transfer_replay | ugc12506_beta_closure_source_declared_spin_proxy_gate_not_endpoint |

## Proxy Definition

All loads are dimensionless source observables from SPARC master-table
fields. The protocol candidate is

`lambda_spin_proxy = lambda_ref * (1 + 0.35 extent_load + 0.25 velocity_load + 0.25 gas_load + 0.15 edgeon_load)`,

with `lambda_ref = 0.1`. The loads use only RHI/Rdisk, Vflat,
H I mass, and inclination. No rotation residual, endpoint score,
wrong-family rank, or best-fit Tau family enters the construction.

## Transfer Queue

| proxy_rank | galaxy | spin_envelope_exposure_proxy | lambda_spin_proxy_candidate | nfw_preference_load | transfer_proxy_priority | transfer_proxy_class |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | NGC0891 | 0.492671 | 0.149267 | 0.225434 | 0.111065 | PRIMARY_PROXY_TRANSFER_REVIEW_TARGET |
| 2 | NGC7331 | 0.357578 | 0.135758 | 0.17284 | 0.0618037 | SECONDARY_PROXY_TRANSFER_REVIEW_TARGET |
| 3 | NGC2841 | 0.720845 | 0.172084 | 0.0675676 | 0.0487057 | SECONDARY_PROXY_TRANSFER_REVIEW_TARGET |
| 4 | NGC0801 | 0.416925 | 0.141693 | 0.0443131 | 0.0184753 | SECONDARY_PROXY_TRANSFER_REVIEW_TARGET |
| 5 | NGC4013 | 0.469836 | 0.146984 | 0.037037 | 0.0174013 | SECONDARY_PROXY_TRANSFER_REVIEW_TARGET |
| 6 | ESO563-G021 | 0.819164 | 0.181916 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |
| 7 | UGC11455 | 0.652187 | 0.165219 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |
| 8 | IC4202 | 0.578808 | 0.157881 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |
| 9 | NGC4157 | 0.542894 | 0.154289 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |
| 10 | NGC3521 | 0.366923 | 0.136692 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |
| 11 | NGC4217 | 0.305416 | 0.130542 | 0 | 0 | CONTROL_OR_ALTERNATIVE_BRANCH |

## Claim Boundary

This gate reduces the blocker from an undefined spin slot to a declared
source-only proxy candidate. It does not promote the proxy to an accepted
lambda_spin measurement. Beta-closure replay and endpoint scoring remain
blocked until an independent source review accepts this proxy rule or
direct source-native spin values are acquired.
