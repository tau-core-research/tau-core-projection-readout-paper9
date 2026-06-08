# Projection-Enriched Population Expansion Ledger

This ledger is a population-validation preparation artifact.  It does not
score rotation curves and it does not promote the four-object projection
audit to population validation.

Claim-boundary check: this ledger does not score rotation curves.
Claim-boundary check: No endpoint scores are computed here.

## Summary

| expansion_status | n_catalogue_rows_listed | n_scored_seed_or_control_rows | n_fresh_population_candidate_rows | n_formula_or_kernel_blocked_rows | n_source_or_orientation_blocked_rows | n_wrong_label_caveated_seed_rows | min_catalogue_cases_required | min_fresh_cases_required | endpoint_scores_run_here | diagnostic_scores_used_as_label_input | current_claim | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PROJECTION_ENRICHED_POPULATION_CATALOGUE_EXPANSION_BLOCKED | 18 | 6 | 12 | 12 | 12 | 2 | 12 | 8 | False | False | there are enough plausible projection-rich rows to define an expansion queue, but not enough formula-frozen fresh rows for population validation | resolve source/orientation/memory blockers and build formula freeze manifests for at least eight fresh projection-enriched candidates before endpoint scoring | projection_enriched_population_expansion_ledger_not_endpoint |

## Catalogue Ledger

| galaxy | role | projection_label | readout_lane | population_use | fresh_population_case | endpoint_score_available | formula_freeze_status | primary_blocker | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | scored_seed_retrospective | warp_vertical_overlay | expdisk_warp_vertical_overlay | reference_only_not_fresh | False | True | endpoint_scored_retrospective | retrospective_reference_case | prospective replay only; do not count as fresh catalogue case |
| NGC5907 | scored_seed_wrong_label_caveated | edge_on_projection_vertical_warp | expdisk_projection_vertical_warp_context | candidate_after_wrong_label_replay | False | True | accepted_single_object_freeze | strict_wrong_label_margin_tight | predeclare wrong enriched label replay before population use |
| NGC7331 | scored_seed_wrong_label_caveated | vertical_outer_warp_overlay | expdisk_vertical_outer_warp_overlay | candidate_after_wrong_label_replay | False | True | accepted_single_object_freeze | strict_wrong_label_margin_tight_outer_window_broad | freeze narrower source-native outer-warp window and rerun wrong-label replay |
| NGC4088 | scored_seed_source_review_caveated | warp_history_asymmetric_projection | warp_history_asymmetric_projection | candidate_after_source_review | False | True | accepted_single_object_freeze_caveated | source_review_and_normalization_caveats | complete source review, epsilon/memory normalization, and wrong-label replay |
| NGC4183 | weak_projection_null_control | edge_on_outer_warp_caveated | K_expdisk_edge_on_projection_outer_warp_caveated | null_control_candidate | False | True | weak_projection_interval_control_complete | strong_projection_not_supported | retain as weak/null projection control; do not count as positive enriched case |
| NGC3198 | frozen_protocol_transfer_seed_not_validation | vertical_projection_constant_h_epg | K_thick_flared_constant_h_projection_context | transfer_rule_seed_not_fresh_validation | False | True | source_derived_constant_h_protocol_frozen_not_retroactive | retroactive_diagnostic_history_transfer_required | apply frozen constant-H EPG rule to a future predeclared fresh case |
| IC4202 | formula_blocked_candidate | edge_on_smooth_disk_projection | K_edge_on_smooth_disk_closure_projection_candidate | candidate_after_formula_values | True | False | formula_shell_derived_freeze_blocked | projection_load_values_and_closure_normalization_unfrozen | resolve source-native H I regularity closure map or scalar-to-kernel theorem |
| UGC06917 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required |
| UGC07577 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required |
| CamB | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| IC2574 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| NGC6789 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGC04305 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGC06818 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGC06983 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGC07151 | fresh_projection_catalogue_queue | projection_review_for_K_exponential_disk | K_exponential_disk_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGC12506 | fresh_projection_catalogue_queue | projection_review_for_K_exponential_disk | K_exponential_disk_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| UGCA444 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | fresh_candidate_after_gate_resolution | True | False | not_built | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |

## Fresh Acquisition / Freeze Queue

| galaxy | role | projection_label | readout_lane | primary_blocker | next_action | formula_family | inclination_deg | manifest_confidence | manifest_caveat | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IC4202 | formula_blocked_candidate | edge_on_smooth_disk_projection | K_edge_on_smooth_disk_closure_projection_candidate | projection_load_values_and_closure_normalization_unfrozen | resolve source-native H I regularity closure map or scalar-to-kernel theorem |  | nan | nan |  | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC06917 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required | K_scale_tail_spiral | 56 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC07577 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required | K_scale_tail_spiral | 63 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| CamB | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 65 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| IC2574 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 75 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| NGC6789 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 43 | 0.8 | few_rotation_points | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC04305 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 40 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC06818 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 75 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC06983 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 49 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC07151 | fresh_projection_catalogue_queue | projection_review_for_K_exponential_disk | K_exponential_disk_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_exponential_disk | 90 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGC12506 | fresh_projection_catalogue_queue | projection_review_for_K_exponential_disk | K_exponential_disk_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_exponential_disk | 86 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |
| UGCA444 | fresh_projection_catalogue_queue | projection_review_for_K_scale_tail_spiral | K_scale_tail_spiral_projection_enriched_candidate | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use | K_scale_tail_spiral | 78 | 1 | none | projection_enriched_population_expansion_ledger_not_endpoint |

## Claim Boundary

The listed rows are a source-side expansion queue.  A Paper 2 population
validation run remains blocked until at least eight fresh candidates have
source-frozen projection labels, formula-freeze manifests, wrong-label
controls, and shuffled projection-label nulls.  No endpoint scores are
computed here.
