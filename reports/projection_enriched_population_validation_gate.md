# Projection-Enriched Population Validation Gate

This gate turns the four-object projection-enriched audit into a
predeclared population validation target.  It does not run endpoint
scoring and does not promote the four-object audit to validation.

## Protocol

| gate_id | required_condition | pass_measure | failure_mode | claim_boundary |
| --- | --- | --- | --- | --- |
| PEV1_SOURCE_FROZEN_PROJECTION_LABEL | observer/projection labels are assigned from external source fields before scoring | projection_label_source_status is accepted_or_caveated_source_frozen and construction_used_vobs=False | projection label inferred from residual shape, RMSE, or endpoint score | projection_enriched_population_validation_gate_not_endpoint |
| PEV2_ENRICHED_KERNEL_FREEZE | component kernels, observer weights, signs, windows, carrier, and amplitude policy are frozen before scoring | formula_freeze_manifest exists and forbidden endpoint fields are absent | component weight or activation window changed after seeing residuals | projection_enriched_population_validation_gate_not_endpoint |
| PEV3_MATCHED_VS_SIMPLER_PROXY | matched projection-enriched kernel beats the simpler pre-enrichment morphology proxy | RMSE_original_proxy - RMSE_projection_enriched > 0 | projection layer adds flexibility without improving the source-matched simpler proxy | projection_enriched_population_validation_gate_not_endpoint |
| PEV4_MATCHED_VS_WRONG_ENRICHED | correct enriched label beats wrong enriched families under the same scoring rules | RMSE_wrong_enriched_mean - RMSE_matched_enriched > 0 and correct rank is high | wrong enriched labels perform as well as the source-matched label | projection_enriched_population_validation_gate_not_endpoint |
| PEV5_SHUFFLED_PROJECTION_NULL | source-frozen projection labels beat shuffled observer/projection labels | matched-vs-shuffled p-value and effect size pass predeclared threshold | signal survives random projection-label assignment | projection_enriched_population_validation_gate_not_endpoint |
| PEV6_BASELINE_COMPARISON | matched enriched readout is compared with Newtonian, MOND/RAR, TPG/v6, and RMOND-facing comparators | baseline competitiveness reported without claiming universal superiority unless population endpoint passes | baseline comparison omitted or overclaimed | projection_enriched_population_validation_gate_not_endpoint |
| PEV7_PATH_AWARE_CLAIM_BOUNDARY | approximate source-plus-observer kernels are separated from the full path-aware Tau Core kernel | path-environment term is marked not modeled unless a path catalogue exists | four-object source/projection audit is overread as full path-aware validation | projection_enriched_population_validation_gate_not_endpoint |

## Current Projection-Enriched Cases

| galaxy | source_fields_used | source_frozen_projection_label | matched_enriched_lane | simpler_proxy | matched_rmse_km_s | simpler_proxy_rmse_km_s | matched_minus_simpler_km_s | best_baseline_model | matched_minus_best_baseline_km_s | matched_minus_wrong_mean_km_s | strict_wrong_label_status | construction_used_vobs | endpoint_scores_allowed | population_validation_use | source_caveat | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | H I lag/warp context plus vertical-structure source support | warp_vertical_overlay | expdisk_warp_vertical_overlay | compact | 11.4505 | 16.9936 | -5.54307 | TPG_V6_v_v6 | -0.823417 | -1.5493 | not_run | False | True | retrospective_reference_case_not_fresh_population_validation | retrospective mixed-reference case; needs prospective replay | projection_enriched_population_validation_gate_not_endpoint |
| NGC5907 | edge-on geometry, warp/truncation, projection/ISM source context | edge_on_projection_vertical_warp | expdisk_projection_vertical_warp_context | exponential disk | 16.3725 | 17.3695 | -0.99701 | TPG_V6_v_v6 | -0.412978 | -0.682634 | does_not_beat_best_wrong_label; margin=0.0238 km/s | False | True | candidate_but_wrong_label_replay_caveated | fresh single-galaxy preliminary control; wrong-label replay remains tight | projection_enriched_population_validation_gate_not_endpoint |
| NGC7331 | H I warp/history plus vertical-scale source context | vertical_outer_warp_overlay | expdisk_vertical_outer_warp_overlay | exponential disk | 22.2557 | 23.473 | -1.21731 | EXPONENTIAL_DISK_CARRIER | -1.21731 | -0.417405 | does_not_beat_best_wrong_label; margin=0.0641 km/s | False | True | candidate_but_wrong_label_replay_caveated | broad outer-warp window and wrong-label replay caveats | projection_enriched_population_validation_gate_not_endpoint |
| NGC4088 | H I geometry, strong distortion, P-V asymmetry, asymmetric warp, companion context | warp_history_asymmetric_projection | warp_history_asymmetric_projection | thick/flared | 11.619 | 38.4554 | -26.8363 | NEWTONIAN_vn | -13.7773 | -30.2389 | not_run | False | True | strong_visual_case_but_source_review_and_normalization_caveated | source-review, memory/asymmetry, epsilon_cross, and normalization-law caveats | projection_enriched_population_validation_gate_not_endpoint |

## Endpoints To Run After Catalogue Freeze

| endpoint_id | definition | pass_condition | current_status | claim_boundary |
| --- | --- | --- | --- | --- |
| DELTA_ENRICHED_SIMPLER | RMSE(simpler morphology-only proxy) - RMSE(matched projection-enriched kernel) | positive mean/median and positive family-balanced result on predeclared catalogue | four-object candidate audit positive; not population validation | projection_enriched_population_validation_gate_not_endpoint |
| DELTA_ENRICHED_WRONG | RMSE(wrong projection-enriched family mean) - RMSE(matched projection-enriched family) | positive on predeclared projection-enriched catalogue | caveated; NGC5907 and NGC7331 do not yet beat best wrong mixed labels | projection_enriched_population_validation_gate_not_endpoint |
| SHUFFLED_PROJECTION_LABEL_NULL | matched enriched score compared with shuffled observer/projection labels | predeclared p-value/effect-size threshold | not run for projection-enriched population catalogue | projection_enriched_population_validation_gate_not_endpoint |
| BASELINE_COMPETITIVENESS | matched enriched readout versus Newtonian, MOND/RAR, TPG/v6, and RMOND-facing comparators | reported without universal superiority unless population endpoint passes | four-object candidate audit positive against listed best baselines | projection_enriched_population_validation_gate_not_endpoint |
| PATH_ENVIRONMENT_ABLATION | compare source-only, source-plus-observer, and future path-environment kernels | observer/path layer improves only where source labels predict it | future; no path-environment catalogue in current paper | projection_enriched_population_validation_gate_not_endpoint |

## Summary

| validation_gate_status | n_projection_enriched_candidates_listed | n_endpoint_scores_allowed_single_object | n_matched_beats_simpler_proxy | n_matched_beats_best_listed_baseline | n_cases_with_strict_wrong_label_caveat | min_catalogue_cases_required | min_fresh_cases_required | endpoint_scores_run_here | diagnostic_scores_used_as_label_input | current_claim | next_required_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PROJECTION_ENRICHED_POPULATION_VALIDATION_BLOCKED_CATALOGUE_AND_WRONG_LABEL_GATES | 4 | 4 | 4 | 4 | 2 | 12 | 8 | False | False | four-object audit motivates projection-enriched population validation but remains kernel-development evidence | build a residual-blind projection-enriched catalogue with source-frozen observer/projection labels, then run matched-vs-simpler, wrong-enriched, shuffled-label, and baseline endpoints | projection_enriched_population_validation_gate_not_endpoint |

## Claim Boundary

The present four-object audit motivates, but does not establish,
population validation.  A valid population test requires a predeclared
projection-enriched catalogue in which source-frozen observer/projection
labels select the enriched kernel family before endpoint scoring.
