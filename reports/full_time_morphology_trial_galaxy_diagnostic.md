# Full-Time Morphology Phase Diagnostic

Status: diagnostic/preflight only, not endpoint validation.

The added layer is source-frozen from morphology/projection status and existing carrier scale. Observed velocities are used only for scoring.

## Summary

| galaxy | source_status | source_note | n_points | phase_load_source_frozen | amplitude_full_time_km2_s2 | rmse_base_projection_morphology_km_s | rmse_full_time_morphology_km_s | full_time_minus_base_rmse_km_s | improves_base | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | warp_vertical_overlay | edge-on warp plus vertical-overlay source context | 36 | 0.18 | 116.695 | 11.4505 | 11.5106 | 0.0601457 | False | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | warp_history_asymmetric_projection | strong warp/history/asymmetry plus companion context | 12 | 0.35 | 1953.97 | 11.619 | 9.39119 | -2.22785 | True | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | weak_projection_null_control | weak projection/null-control case; phase effect expected to be small | 23 | 0.03 | 7.1589 | 6.24727 | 6.24536 | -0.00191093 | True | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | edgeon_projection_vertical_warp | edge-on projection and warp/truncation context | 19 | 0.12 | 116.746 | 15.4952 | 15.495 | -0.000153462 | True | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | vertical_outer_warp_overlay | outer warp / vertical-scale mixed readout context | 36 | 0.1 | 127.134 | 22.2557 | 22.2785 | 0.0228459 | False | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | base_projection_morphology_kernel | v_wvo_endpoint | 36 | 11.4505 | 11.8484 | 9.77258 | 5.68955 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4013 | full_time_morphology_phase_kernel | diagnostic_phase_enriched | 36 | 11.5106 | 11.8925 | 9.82495 | 5.91445 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4013 | carrier_reference | v_v6 | 36 | 12.2739 | 12.4369 | 10.5132 | 6.97616 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4013 | MOND_v_mond | baseline | 36 | 14.3342 | 14.8721 | 11.9405 | 11.6526 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4013 | NEWTONIAN_vn | baseline | 36 | 65.6913 | 62.217 | 61.8974 | -61.8974 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | full_time_morphology_phase_kernel | diagnostic_phase_enriched | 12 | 9.39119 | nan | 7.90641 | -2.48202 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | base_projection_morphology_kernel | v_warp_history_formula_freeze_km_s | 12 | 11.619 | nan | 9.64302 | -4.27668 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | carrier_reference | vn | 12 | 25.3963 | nan | 20.1483 | -14.8664 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | TPG_V6_v_v6 | baseline | 12 | 38.9877 | nan | 37.9843 | 37.9843 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4088 | MOND_v_mond | baseline | 12 | 42.1838 | nan | 41.2137 | 41.2137 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | carrier_reference | v_K_exponential_disk | 23 | 6.22458 | 6.22811 | 4.86106 | -2.84744 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | full_time_morphology_phase_kernel | diagnostic_phase_enriched | 23 | 6.24536 | 6.24635 | 4.87351 | -2.9031 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | base_projection_morphology_kernel | v_null_control_interval_midpoint_km_s | 23 | 6.24727 | 6.24644 | 4.87503 | -2.91431 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | TPG_V6_v_v6 | baseline | 23 | 6.48969 | 6.81416 | 5.6918 | 1.52555 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | MOND_v_mond | baseline | 23 | 10.355 | 10.759 | 9.23844 | 6.13375 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC4183 | NEWTONIAN_vn | baseline | 23 | 48.4109 | 48.3783 | 47.4836 | -47.4836 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | full_time_morphology_phase_kernel | diagnostic_phase_enriched | 19 | 15.495 | 8.75134 | 9.21683 | -6.20906 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | base_projection_morphology_kernel | v_projection_accepted | 19 | 15.4952 | 8.72696 | 9.25559 | -6.33278 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | carrier_reference | v_v6 | 19 | 16.7855 | 11.674 | 11.4745 | -1.00704 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | MOND_v_mond | baseline | 19 | 18.5954 | 15.3586 | 15.1311 | 4.3498 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC5907 | NEWTONIAN_vn | baseline | 19 | 86.4837 | 85.4673 | 85.6717 | -85.6717 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | base_projection_morphology_kernel | v_mixed_population | 36 | 22.2557 | 17.2117 | 17.631 | 16.2559 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | full_time_morphology_phase_kernel | diagnostic_phase_enriched | 36 | 22.2785 | 17.2705 | 17.6604 | 16.3732 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | carrier_reference | v_K_exponential_disk | 36 | 23.473 | 19.5953 | 19.5632 | 19.1914 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | TPG_V6_v_v6 | baseline | 36 | 25.4851 | 22.424 | 22.2152 | 22.2056 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | MOND_v_mond | baseline | 36 | 29.3117 | 26.0966 | 26.452 | 26.452 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |
| NGC7331 | NEWTONIAN_vn | baseline | 36 | 59.3544 | 61.3486 | 51.4592 | -42.0494 | False | True | False | full_time_morphology_kernel_trial_diagnostic_not_endpoint_validation |

Figure: `figures/endpoint_diagnostics/full_time_morphology_trial_galaxy_rotation_curves.png`
