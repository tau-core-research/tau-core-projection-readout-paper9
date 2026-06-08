# UGC12506 Prior-Best Source Route Audit

The previous diagnostic Tau-best row is useful, but it cannot promote
a source label. This audit checks whether its K_compact_finite hint is
source-supported for UGC12506.

## Summary

| audit_status | galaxy | prior_best_family | prior_best_rmse_km_s | compact_source_promotion | nfw_rapid_rise_route | highspin_envelope_coupling | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_PRIOR_BEST_AUDIT_COMPLETE_NFW_RAPID_RISE_ROUTE_OPENED | UGC12506 | K_compact_finite | 37.3633 | BLOCKED_DIAGNOSTIC_ONLY | SOURCE_SUPPORTED_CANDIDATE | SOURCE_SUPPORTED_CANDIDATE | False | derive_ugc12506_nfw_like_rapid_rise_highspin_envelope_shell | ugc12506_prior_best_source_route_audit_not_endpoint |

## Evidence

| galaxy | evidence_id | evidence_class | source | statement | route_interpretation | status | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_PB_E1_PRIOR_DIAGNOSTIC | diagnostic_score_reference | multigalaxy_fit_inspection_scores.csv | Prior diagnostic TAU_BEST_FAMILY has RMSE 37.36 km/s and reports best_family=K_compact_finite, but validation_claim_allowed=False. | Useful signal about missing readout shape, not a source-accepted morphology label. | DIAGNOSTIC_ONLY_NOT_SOURCE_LABEL | True | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_E2_NFW_PREFERENCE | source_halo_fit_context | Hallenbeck2014 lines 730-738 | UGC12506 has a very significant preference for the NFW halo model over the pseudo-isothermal model in the source discussion. | Source pressure points toward rapid-rise / NFW-like halo-concentration readout, not toward a cored compact-support interpretation. | SOURCE_SUPPORTED_NFW_LIKE_ROUTE | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_E3_FAST_RISE | source_rotation_shape_context | Hallenbeck2014 lines 679-681, 736-738 | The rotation curve rises quickly to about 250 km/s, and the source notes this is unlike the slowly rising curves expected for many LSBs. | Supports a steep inner/halo-concentration shell rather than simply amplifying the outer envelope. | SOURCE_SUPPORTED_RAPID_RISE_ROUTE | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_E4_HIGH_SPIN | source_spin_context | Hallenbeck2014 lines 800-811, 834-839 | UGC12506 has high spin lambda=0.15 and a diffuse stable H I reservoir. | Supports coupling the rapid-rise shell to high-spin envelope support rather than using a generic compact family. | SOURCE_SUPPORTED_HIGH_SPIN_ROUTE | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_E5_COMPACT_CORED_ROUTE | negative_source_route | Hallenbeck2014 lines 326-344, 730-738 | The source defines a pseudo-isothermal cored halo option, but UGC12506 is reported to prefer NFW significantly. | Do not promote K_compact_finite as source-native for UGC12506 from the current evidence. | COMPACT_CORED_ROUTE_NOT_SOURCE_PROMOTED | False | ugc12506_prior_best_source_route_audit_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | decision | evidence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_PB_G1_PRIOR_DIAGNOSTIC_NOT_LABEL | PASS | preserve prior K_compact_finite as diagnostic only | validation_claim_allowed=False | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_G2_COMPACT_SOURCE_PROMOTION | BLOCKED | do not promote compact/cored source label | source reports significant NFW preference for UGC12506 | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_G3_NFW_RAPID_RISE_ROUTE | PASS_CANDIDATE | open source-side NFW-like rapid-rise / concentration shell | NFW preference plus rapid rotation-curve rise | False | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | U12506_PB_G4_HIGH_SPIN_COUPLING | PASS_CANDIDATE | couple rapid-rise shell to high-spin extended-envelope route | lambda=0.15 and stable diffuse H I reservoir | False | ugc12506_prior_best_source_route_audit_not_endpoint |

## Route Plan

| galaxy | route_id | route_status | formula_family_hint | source_basis | not_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_ROUTE_A_SOURCE_NATIVE_NFW_RAPID_RISE | NEXT_FORMULA_SHELL_CANDIDATE | K_nfw_like_rapid_rise_highspin_envelope | NFW preference, rapid rise, high spin, extended H I envelope | using prior K_compact_finite score as source label | ugc12506_prior_best_source_route_audit_not_endpoint |
| UGC12506 | UGC12506_ROUTE_B_COMPACT_FINITE | BLOCKED_AS_SOURCE_LABEL_DIAGNOSTIC_ONLY | K_compact_finite | diagnostic score only; source prefers NFW over pseudo-isothermal | promotion without independent compact/cored source evidence | ugc12506_prior_best_source_route_audit_not_endpoint |

## Interpretation

The current source evidence does not support promoting the prior
K_compact_finite diagnostic as an accepted UGC12506 morphology/readout
label.  Instead, Hallenbeck et al. report a significant NFW preference,
rapid rotation-curve rise, high spin, and an extended H I envelope.  The
claim-safe next route is therefore an NFW-like rapid-rise/high-spin
envelope shell.
