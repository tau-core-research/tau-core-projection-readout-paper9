# UGC12506 Theta_morph / Xi_t Source-Nonoverlap Gate

This audit separates source evidence by channel role. It does not score
an endpoint and does not choose a new amplitude from the rotation curve.

## Summary

| nonoverlap_status | galaxy | n_ledger_rows | n_shared_or_partial_rows | n_theta_only_rows | n_xit_only_rows | n_excluded_rows | assignment_counts | path_term_established | theta_endpoint_allowed | xit_standard_endpoint_allowed | combined_control_replay_allowed | combined_endpoint_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PARTIAL_NONOVERLAP_CONTROL_ALLOWED_COMBINED_ENDPOINT_BLOCKED | UGC12506 | 7 | 4 | 1 | 1 | 1 | EXCLUDED_UNTIL_SOURCE_PATH_REVIEW=1; PARTIALLY_SHARED_NEEDS_SPLIT=2; SHARED_CONTEXT_NOT_INDEPENDENT=1; THETA_ONLY=1; THETA_PRIMARY_XIT_CAVEATED_PHASE_ONLY=1; XIT_ONLY_PROTOCOL_CAP=1 | False | False | False | True | False | False | run optional combined-control replay with ledger assignments frozen, or acquire non-overlapping clock/path evidence before endpoint | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |

## Source Ledger

| galaxy | source_observable | source_basis | theta_role | xit_role | assignment | double_count_risk | allowed_in_combined_control | endpoint_permission | uses_vobs_or_residual | reason | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | high_spin_lambda | reported high-spin state lambda=0.15 | phase_load_context | core_clock_load_component | SHARED_CONTEXT_NOT_INDEPENDENT | HIGH | context_only_do_not_sum_twice | False | False | the same high-spin evidence supports both late-settling morphology phase and clock-load route | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | extended_low_density_hi_envelope | large diffuse low-density H I support | outer_late_settling_shape_and_load | envelope_settling_interval_component | PARTIALLY_SHARED_NEEDS_SPLIT | MEDIUM | split_shape_vs_clock_interval_only | False | False | outer H I can define a morphology phase shape, but its settling interpretation also enters Xi_t | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | high_inclination_edge_on_pv_geometry | high inclination and PV/envelope method required | projection_history_base_context | edgeon_pv_clock_slice | PARTIALLY_SHARED_NEEDS_SPLIT | MEDIUM | geometry_mask_for_theta_or_clock_slice_not_both_as_amplitude | False | False | edge-on geometry is necessary context for both readout visibility and clock-slice interpretation | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | approaching_receding_hi_asymmetry | approaching/receding side shape and length asymmetry | morphology_phase_component | caveated_phase_component_not_standalone | THETA_PRIMARY_XIT_CAVEATED_PHASE_ONLY | MEDIUM | theta_primary_xit_phase_caveat_only | False | False | review policy already forbids asymmetry as a standalone Xi_t route driver | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | late_settling_outer_radial_shape | Theta_morph late-settling outer-window construction | primary_kernel_shape | none | THETA_ONLY | LOW | theta_channel_only | False | False | this is a morphology-state shape assignment, not a clock/readout scale | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | epsilon_t_cap_protocol | epsilon_cap=0.035 is protocol cap only, not universal Tau Core constant | none | clock_interval_bound | XIT_ONLY_PROTOCOL_CAP | LOW | xit_interval_bound_only | False | False | cap controls the small clock interval and is not a morphology amplitude | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| UGC12506 | foreground_path_environment | path term fixed to zero unless later source path review establishes it | none | excluded_zero_path_term | EXCLUDED_UNTIL_SOURCE_PATH_REVIEW | LOW | zero_only | False | False | path/environment evidence is not established | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |

## Gates

| gate_id | gate_status | gate_text | galaxy | endpoint_permission | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| U12506_NONOVERLAP_G1_FORMULA_ROLE | PASS | Theta_morph is additive; Xi_t is multiplicative interval-control. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| U12506_NONOVERLAP_G2_UNIQUE_THETA_SHAPE | PASS_CONTROL_ONLY | late-settling outer radial shape can be assigned to Theta_morph only. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| U12506_NONOVERLAP_G3_UNIQUE_XIT_CAP | PASS_CONTROL_ONLY | epsilon_t cap is Xi_t-only protocol bound, not a morphology amplitude. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| U12506_NONOVERLAP_G4_SHARED_CONTEXT | BLOCK_COMBINED_ENDPOINT | high-spin/envelope/asymmetry context remains shared or partially shared. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| U12506_NONOVERLAP_G5_PATH_TERM | BLOCK_PATH_ENDPOINT | path/environment term remains zero unless source path review establishes it. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |
| U12506_NONOVERLAP_G6_ENDPOINT_BOUNDARY | CONTROL_ALLOWED_ENDPOINT_BLOCKED | combined-control replay may be recorded; combined endpoint is not permitted. | UGC12506 | False | False | ugc12506_theta_xit_source_nonoverlap_gate_not_endpoint |

## Interpretation

The current refinements make the UGC12506 channels separable enough for
a combined-control ledger: the late-settling radial shape is assigned to
`Theta_morph`, while the small cap is assigned to `Xi_t`.  However, the
high-spin/envelope/asymmetry context is not yet independent across the
two channels, and the path/environment term remains unestablished.  The
combined endpoint therefore remains blocked.

## Xi_t component policy snapshot

| galaxy | component_id | component_status | source_load | normalized_weight | kernel_column | source_basis | claim_boundary | control_policy | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | T_HIGHSPIN_SETTLING | INCLUDED_SOURCE_SUPPORTED | 1 | 0.467884 | K_t_highspin_clock_spin | reported high-spin state lambda=0.15 | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_as_source_supported_core_component | False |
| UGC12506 | T_EDGEON_PV_CLOCK_SLICE | INCLUDED_SOURCE_SUPPORTED | 0.59708 | 0.279365 | K_t_highspin_clock_spin | high inclination and PV/envelope method required | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_with_projection_caveat | False |
| UGC12506 | T_ENVELOPE_SETTLING | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.457272 | 0.21395 | K_t_highspin_clock_envelope | large diffuse low-density H I support | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_as_caveated_interval_component | False |
| UGC12506 | T_ASYMMETRIC_PV_PHASE | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.0829278 | 0.0388006 | K_t_highspin_clock_asymmetry | approaching/receding side shape and length asymmetry | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_only_as_caveated_phase_component | False |
| UGC12506 | T_PATH_ENVIRONMENT | EXCLUDED_NOT_ESTABLISHED | 0 | 0 | K_t_path_environment | foreground/path object evidence is not established | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | exclude_keep_zero_until_source_path_review | False |

