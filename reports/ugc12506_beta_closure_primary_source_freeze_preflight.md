# UGC12506 Beta-Closure Primary Source-Freeze Preflight

This preflight inspects the two primary NFW-preference targets after the
post-halo priority gate. It preserves the endpoint blocker: PV/envelope
context is acceptable as source context, but no direct source-native spin
value has been frozen for either galaxy.

## Summary

| primary_source_freeze_status | n_primary_targets | n_pv_envelope_context_accepted | n_lambda_spin_frozen | n_beta_cl_replay_allowed | n_endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_BETA_CLOSURE_PRIMARY_SOURCE_FREEZE_PREFLIGHT_BUILT_SPIN_BLOCKED | 2 | 2 | 0 | 0 | 0 | spin_freeze_or_source_declared_spin_proxy_gate | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |

## Primary Targets

| galaxy | post_halo_rank | nfw_preference_load | pv_envelope_status | lambda_spin_status | beta_cl_replay_allowed | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | 1 | 0.225434 | ACCEPTED_CONTEXT_NOT_NUMERIC_FREEZE | BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED | False | False | freeze_lambda_spin_or_construct_declared_spin_proxy_from_source_observables | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |
| NGC7331 | 2 | 0.17284 | ACCEPTED_CONTEXT_CACHED_THINGS_PRODUCTS | BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED | False | False | freeze_lambda_spin_or_construct_declared_spin_proxy_from_source_observables | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |

## Evidence Ledger

| galaxy | field | field_status | source_value | source_reference | source_url | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | PV/envelope evidence | ACCEPTED_CONTEXT_NOT_NUMERIC_FREEZE | edge-on H I XV/PV modelling and envelope-tracing route present; rotation curve derived from envelope tracing/XV fitting | Fraternali & Binney 2006 MNRAS 366, 449; Kregel & van der Kruit 2004 MNRAS 352, 787 | https://academic.oup.com/mnras/article/366/2/449/1214630 ; https://academic.oup.com/mnras/article/352/3/787/1211373 | False | False | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |
| NGC0891 | lambda_spin | BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED |  | no accepted direct source-native spin value cached |  | False | False | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |
| NGC7331 | PV/envelope evidence | ACCEPTED_CONTEXT_CACHED_THINGS_PRODUCTS | THINGS H I rotation/velocity-field context and local MOM0/MOM1/MOM2 products are cached; inner points include PV-diagram lineage and outer differences depend on inclination choices | de Blok et al. 2008 AJ/ApJ THINGS; local THINGS products; Patra 2018 MNRAS 478, 4931 | https://arxiv.org/abs/0810.2100 ; https://academic.oup.com/mnras/article/478/4/4931/5045978 | False | False | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |
| NGC7331 | lambda_spin | BLOCKED_SOURCE_NATIVE_VALUE_REQUIRED |  | no accepted direct source-native spin value cached |  | False | False | ugc12506_beta_closure_primary_source_freeze_preflight_not_endpoint |

## Claim Boundary

No beta_cl replay or endpoint scoring is allowed by this gate. The next
allowed step is to freeze a direct spin value or predeclare a source-only
spin proxy before inspecting any transfer endpoint residual.
