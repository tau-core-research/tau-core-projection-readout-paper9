# UGC12506 Source-Native NFW-HSE Decision Gate

The source-native NFW/HSE replay is a cleaner partial success, but not an
accepted endpoint. It improves the old proxy route slightly and the older
source-frozen branches substantially, while the gap to the prior diagnostic
best remains large.

## Decision

| decision_status | galaxy | source_native_nfw_hse_rmse_km_s | old_rd_proxy_nfw_hse_rmse_km_s | source_native_minus_old_proxy_rmse_km_s | best_uncertainty_rmse_km_s | prior_best_diagnostic_rmse_km_s | gap_to_prior_best_after_uncertainty_km_s | nfw_route_status | internal_projection_status | foreground_path_object_status | decision | negative_result_preserved | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NATIVE_NFW_HSE_PARTIAL_SUCCESS_GAP_REMAINS | UGC12506 | 77.5409 | 77.8617 | -0.320772 | 77.517 | 37.3633 | 40.1537 | SOURCE_SUPPORTED_CANDIDATE | SOURCE_SUPPORTED_STRONG | NOT_ESTABLISHED | keep source-native NFW-HSE as cleaner partial source route; do not promote to accepted endpoint; search for an additional residual-blind mass/readout normalization or projection-history component before another scoring attempt | True | False | ugc12506_source_native_nfw_hse_decision_gate_not_validation |

## Open Obligations

| obligation_id | status | why_it_matters | allowed_sources | forbidden_sources | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| U12506_NEXT_1_AMPLITUDE_SOURCE | OPEN | the source-native shape improves branches but remains under-amplified | stellar/gas mass scale, halo velocity scale, distance/inclination audit, or source-native baryonic carrier audit | endpoint residual multiplier, post-hoc curve rescue | UGC12506 | ugc12506_source_native_nfw_hse_decision_gate_not_validation |
| U12506_NEXT_2_PROJECTION_HISTORY | OPEN | edge-on projection is strong, but foreground/path object evidence is not established | source-native warp, vertical overlay, H I asymmetry, resolved velocity-field context | assigning line-of-sight gravity from optical overlay caveats alone | UGC12506 | ugc12506_source_native_nfw_hse_decision_gate_not_validation |
| U12506_NEXT_3_CARRIER_AUDIT | OPEN | all compared baselines underpredict, suggesting carrier/source normalization may be low | published distance, inclination, M/L, gas scale, and SPARC carrier variants | choosing carrier from best endpoint RMSE after scoring | UGC12506 | ugc12506_source_native_nfw_hse_decision_gate_not_validation |

## Interpretation

UGC12506 should be preserved as a useful weak/negative replay case rather
than forced into a successful endpoint. The next honest route is not to
increase the amplitude from the residual, but to determine whether an
independent source-native carrier normalization, halo-velocity scale, or
projection-history component is justified.
