# UGC12506 Projection/History-Enriched Readout Candidate Gate

This gate tests whether the source record justifies treating UGC12506 as
a projection/history-enriched readout candidate after the source-native
NFW-HSE replay leaves a large gap. It does not score an endpoint.

## Summary

| candidate_status | galaxy | highmass_context_status | source_native_nfw_hse_rmse_km_s | gap_to_prior_best_after_uncertainty_km_s | projection_history_formula_allowed | why_not_allowed_yet | next_gate | endpoint_scores_allowed | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_PROJECTION_HISTORY_ENRICHED_READOUT_CANDIDATE_SOURCE_SUPPORTED_CAVEATED | UGC12506 | UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN | 77.5409 | 40.1537 | False | asymmetry/history radial sign and weight are not source-frozen; foreground/path gravity term is not established | derive source-side projection-history component with no residual-selected sign, weight, or amplitude | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |

## Evidence

| galaxy | evidence_id | source_basis | source_status | bridge_interpretation | supports_projection_history_candidate | allowed_kernel_role | forbidden_role | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_PH_E1_EDGEON_PROJECTION | Hallenbeck2014 high-inclination PV/envelope method context | SOURCE_SUPPORTED_STRONG | strong observer/projection layer from edge-on disk integration | True | internal_edgeon_projection_component | none | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_E2_EXTENDED_HI_HIGHSPIN | R_HI about 58 kpc, diffuse stable H I, lambda_spin=0.15 | SOURCE_SUPPORTED_STRONG | morphology-carried persistence/high-spin envelope support | True | extended_hi_envelope_persistence_component | endpoint-residual amplitude multiplier | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_E3_ARM_ASYMMETRY | approaching/receding sides differ in shape and detectable extent | SOURCE_SUPPORTED_CAVEATED | caveated lopsided/projection-asymmetry history proxy | True | secondary_asymmetry_component_after_source_weight_rule | residual-selected radial sign or hand-tuned weight | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_E4_IMAGE_INTERLOPER_OVERLAY | star and higher-redshift galaxy overlap the optical image | SOURCE_SUPPORTED_OVERLAY_CAVEAT | K_obs-to-K_readout mask/caveat, not a path-gravity term | True | photometric_overlay_mask_or_caveat | foreground/path gravity kernel | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_E5_FOREGROUND_PATH_OBJECT | no foreground massive object along the path is established | NOT_ESTABLISHED | full observer/path gravity component remains blocked | False | none until catalogue cone/path search | line-of-sight gravity kernel from current evidence | False | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_E6_SOURCE_NATIVE_REPLAY_GAP | source-native NFW-HSE improves branches but leaves large gap | UGC12506_SOURCE_NATIVE_NFW_HSE_PARTIAL_SUCCESS_GAP_REMAINS | gap motivates source acquisition for projection-history/carrier layers; it does not itself define the component | False | worklist_priority_signal_only | using endpoint residual to choose label or amplitude | True | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | decision | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_PH_G1_INTERNAL_PROJECTION | PASS_STRONG | high inclination and PV/envelope method requirement | include as projection-history candidate ingredient | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_G2_MORPHOLOGY_HISTORY_ENVELOPE | PASS_STRONG | extended diffuse stable H I and high spin | include as morphology-carried persistence candidate ingredient | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_G3_ASYMMETRY_HISTORY | PASS_CAVEATED | approaching/receding asymmetry; radial rule not frozen | allow only after source-side sign/weight rule | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_G4_FOREGROUND_PATH | BLOCKED_NOT_ESTABLISHED | known galaxy interloper is higher-redshift; no foreground/path object established | do not include full foreground/path gravity term | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |
| UGC12506 | U12506_PH_G5_ENDPOINT_BLINDNESS | PASS_WITH_CAUTION | candidate support comes from source context; replay gap is worklist priority only | no endpoint score allowed from this gate | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |

## Formula Skeleton

| galaxy | skeleton_id | not_yet_frozen_formula | candidate_component | allowed_source_inputs | blocked_inputs | formula_freeze_status | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_PROJECTION_HISTORY_ENRICHED_SKELETON | v_readout^2 = v_carrier^2 + A_NFW_HSE K_NFW_HSE + A_PH K_projection_history | K_projection_history = combine(K_edgeon_disk_integration, K_HI_envelope_persistence, K_arm_asymmetry_history) | inclination/PV envelope method, H I extent, high-spin context, approaching/receding extent asymmetry, resolved H I/velocity-field morphology | foreground/path gravity without cone/path source; residual-selected sign; endpoint-selected amplitude | BLOCKED_SOURCE_SIDE_RULE_REQUIRED | False | ugc12506_projection_history_readout_candidate_gate_not_endpoint |

## Claim Boundary

The source record supports internal edge-on projection, extended H I
envelope persistence, high spin, and caveated asymmetry/history context.
It does not yet support a full foreground/path gravity kernel. The next
honest step is a residual-blind source-side sign/weight rule for the
projection-history component.
