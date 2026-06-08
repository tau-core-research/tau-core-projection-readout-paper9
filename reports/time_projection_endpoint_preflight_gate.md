# Time Projection Endpoint Preflight Gate

This artifact moves the multichannel time-projection shell toward an
endpoint calculation without allowing endpoint scoring. It separates
`Xi_morph`, `Xi_obs`, and `Xi_path` so that a future endpoint cannot
hide missing morphology-time or observer-time evidence inside one fitted
`Xi_t` factor.

## Source-Morphology Time Manifest

| galaxy | xi_morph_channel_status | xi_morph_source_basis | source_support_level | blocked_or_caveated_fields | xi_morph_frozen_before_scoring | endpoint_scores_allowed | reason | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | SOURCE_CHANNEL_QMEM_REVIEWED_NORMALIZATION_BLOCKED | warp flag; PV asymmetry flag; PA asymmetry flag | STRONG_SOURCE_REVIEWED_QMEM_NORMALIZATION_BLOCKED | accepted epsilon_t normalization law; residual-blind B_i coefficient rule | False | False | q_warp and m_history are accepted for protocol numeric bounds, but the residual-blind B_i / epsilon_t normalization rule remains open | time_projection_endpoint_preflight_gate_not_endpoint |
| UGC12506 | CAVEATED_INTERVAL_SOURCE_CHANNEL_READY_CONTROL_ONLY | high inclination PV/envelope; extended HI support; asymmetric PV; low-density stable HI; high-spin context | STRONG_CONTEXT_PATH_FOREGROUND_REJECTED | accepted K_t(R) envelope mapping; epsilon_t normalization law; clock/readout settling proxy | True | False | high-spin/envelope source channel exists as a caveated interval control, but not as an accepted endpoint manifest | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4183 | SOURCE_CHANNEL_WEAK_NULL_CONTROL | weak_projection_null_control | weak_projection_null_control | quiet-control confirmation; no strong Xi_t promotion unless new source evidence appears | False | False | weak/null control; no strong source reason to activate time projection | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4013 | SOURCE_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | warp_vertical_overlay | warp_vertical_overlay | separate vertical overlay from clock-readout; do not promote Xi_t without independent clock evidence | False | False | current Xi_t proxy worsens or double-counts an already saturated morphology/projection kernel | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC5907 | SOURCE_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | edgeon_projection_vertical_warp | edgeon_projection_vertical_warp | path-specific clock evidence beyond ordinary edge-on projection; otherwise keep Xi_t=1 | False | False | current Xi_t proxy worsens or double-counts an already saturated morphology/projection kernel | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC7331 | SOURCE_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | vertical_outer_warp_overlay | vertical_outer_warp_overlay | narrow outer-warp clock proxy and independent H I history coherence before any Xi_t promotion | False | False | current Xi_t proxy worsens or double-counts an already saturated morphology/projection kernel | time_projection_endpoint_preflight_gate_not_endpoint |

## Observer / Projection Time Manifest

| galaxy | xi_obs_channel_status | xi_obs_source_basis | xi_path_status | xi_obs_frozen_before_scoring | endpoint_scores_allowed | reason | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | OBSERVER_CHANNEL_SECONDARY_BLOCKED | warp/asymmetry visibility context; not the primary blocker | NOT_PRIMARY_FOR_THIS_ROUTE | False | False | clock phase must first be separated from additive warp-history morphology | time_projection_endpoint_preflight_gate_not_endpoint |
| UGC12506 | OBSERVER_CHANNEL_CAVEATED_EDGEON_PV_CONTROL_READY | edge-on high inclination; PV/envelope visibility; path term rejected/zero in current review | NOT_ESTABLISHED | True | False | observer/PV slice can be carried as caveated control, but not endpoint validation | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4183 | OBSERVER_CHANNEL_WEAK_NULL_CONTROL | weak_projection_null_control | UNKNOWN | False | False | no strong source-reviewed observer-clock activation | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4013 | OBSERVER_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | warp_vertical_overlay | UNKNOWN | False | False | ordinary projection is already represented by the base kernel or lacks independent clock evidence | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC5907 | OBSERVER_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | edgeon_projection_vertical_warp | UNKNOWN | False | False | ordinary projection is already represented by the base kernel or lacks independent clock evidence | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC7331 | OBSERVER_CHANNEL_REJECT_CURRENT_PROXY_KEEP_XI_ONE | vertical_outer_warp_overlay | UNKNOWN | False | False | ordinary projection is already represented by the base kernel or lacks independent clock evidence | time_projection_endpoint_preflight_gate_not_endpoint |

## Endpoint Preflight

| galaxy | time_projection_preflight_status | xi_eff_formula | xi_path_policy | control_replay_allowed | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | DOUBLE_COUNT_RESOLVED_COMBINED_XI_ONE_TIME_ENDPOINT_INACTIVE | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | NOT_PRIMARY_FOR_THIS_ROUTE | True | False | score additive-only accepted route if endpoint scoring is requested; reopen time endpoint only with independent non-overlap clock evidence | time_projection_endpoint_preflight_gate_not_endpoint |
| UGC12506 | CONTROL_REPLAY_ALLOWED_ENDPOINT_BLOCKED | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | NOT_ESTABLISHED | True | False | derive accepted source-only Xi_eff normalization or keep caveated interval as control-only | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4183 | NOT_ENDPOINT_READY | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | UNKNOWN | False | False | retain as weak/null or source-review case | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC4013 | CURRENT_PROXY_REJECTED_KEEP_XI_ONE | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | UNKNOWN | False | False | do not score time endpoint unless independent clock evidence appears | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC5907 | CURRENT_PROXY_REJECTED_KEEP_XI_ONE | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | UNKNOWN | False | False | do not score time endpoint unless independent clock evidence appears | time_projection_endpoint_preflight_gate_not_endpoint |
| NGC7331 | CURRENT_PROXY_REJECTED_KEEP_XI_ONE | Xi_eff(R)=Xi_morph(R)*Xi_obs(R)*Xi_path(R) | UNKNOWN | False | False | do not score time endpoint unless independent clock evidence appears | time_projection_endpoint_preflight_gate_not_endpoint |

## Summary

| preflight_status | n_galaxies | n_control_replay_allowed | n_endpoint_scores_allowed | strongest_current_route | main_blocker | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| TIME_PROJECTION_ENDPOINT_PREFLIGHT_BUILT_NO_ENDPOINTS_ALLOWED | 6 | 2 | 0 | UGC12506 caveated interval/control replay; NGC4088 additive warp-history route with Xi_eff=1 in the combined endpoint | no source-complete accepted time endpoint with clock evidence orthogonal to the active morphology kernel | time_projection_endpoint_preflight_gate_not_endpoint |

## Interpretation

The current executable time-projection routes remain control routes, not
accepted time endpoints.  UGC12506 has a caveated interval/control replay.
For NGC4088, the source-space double-count audit resolves the combined
endpoint by assigning the overlapping clock evidence to the already active
additive warp-history route; the combined endpoint therefore uses
`Xi_eff=1`, while the clock-only route is preserved as a control.
A real time-projection endpoint requires source-complete clock evidence
orthogonal to the active morphology kernel, with `Xi_morph`, `Xi_obs`,
and `Xi_path` independently frozen before the scoring script reads the
rotation curve.
