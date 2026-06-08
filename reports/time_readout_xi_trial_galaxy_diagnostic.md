# Time-Readout Xi_t Trial Diagnostic

Status: diagnostic only, not endpoint validation.

The run applies a small residual-blind clock/readout factor to the existing base and full-time morphology curves.

## Summary

| galaxy | n_points | source_status | epsilon_0_source_frozen | rmse_base_km_s | rmse_full_time_additive_km_s | rmse_xi_on_base_km_s | rmse_xi_on_full_time_km_s | best_trial_model | best_trial_rmse_km_s | xi_improves_base | xi_improves_full_time | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 36 | warp_vertical_overlay | 0.0108 | 11.4505 | 11.5106 | 11.9532 | 12.0425 | base_projection_morphology | 11.4505 | False | False | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4088 | 12 | warp_history_asymmetric_projection | 0.021 | 11.619 | 9.39119 | 10.4561 | 8.34902 | xi_t_on_full_time_morphology | 8.34902 | True | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4183 | 23 | weak_projection_null_control | 0.0018 | 6.24727 | 6.24536 | 6.24002 | 6.23832 | xi_t_on_full_time_morphology | 6.23832 | True | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC5907 | 19 | edgeon_projection_vertical_warp | 0.0072 | 15.4952 | 15.495 | 15.5203 | 15.5294 | full_time_morphology_additive_proxy | 15.495 | False | False | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC7331 | 36 | vertical_outer_warp_overlay | 0.006 | 22.2557 | 22.2785 | 22.4106 | 22.4393 | base_projection_morphology | 22.2557 | False | False | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| UGC12506 | 31 | edgeon_highspin_projection_history_theta | 0.029456 | 69.1788 | 64.1192 | 67.9037 | 62.9679 | xi_t_on_full_time_morphology | 62.9679 | True | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |

## Scores

| galaxy | model_id | model_role | n_points | rmse_km_s | weighted_rmse_km_s | mae_km_s | bias_km_s | construction_used_vobs | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | base_projection_morphology | reference | 36 | 11.4505 | 11.8484 | 9.77258 | 5.68955 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4013 | full_time_morphology_additive_proxy | reference | 36 | 11.5106 | 11.8925 | 9.82495 | 5.91445 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4013 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 36 | 11.9532 | 12.2212 | 10.1791 | 7.00097 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4013 | xi_t_on_full_time_morphology | time_readout_diagnostic | 36 | 12.0425 | 12.2905 | 10.2352 | 7.22799 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4088 | xi_t_on_full_time_morphology | time_readout_diagnostic | 12 | 8.34902 | nan | 7.0529 | -1.50464 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4088 | full_time_morphology_additive_proxy | reference | 12 | 9.39119 | nan | 7.90641 | -2.48202 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4088 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 12 | 10.4561 | nan | 8.69602 | -3.32456 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4088 | base_projection_morphology | reference | 12 | 11.619 | nan | 9.64302 | -4.27668 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4183 | xi_t_on_full_time_morphology | time_readout_diagnostic | 23 | 6.23832 | 6.25011 | 4.86765 | -2.83619 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4183 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 23 | 6.24002 | 6.25001 | 4.86917 | -2.84741 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4183 | full_time_morphology_additive_proxy | reference | 23 | 6.24536 | 6.24635 | 4.87351 | -2.9031 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC4183 | base_projection_morphology | reference | 23 | 6.24727 | 6.24644 | 4.87503 | -2.91431 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC5907 | full_time_morphology_additive_proxy | reference | 19 | 15.495 | 8.75134 | 9.21683 | -6.20906 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC5907 | base_projection_morphology | reference | 19 | 15.4952 | 8.72696 | 9.25559 | -6.33278 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC5907 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 19 | 15.5203 | 8.91096 | 9.13931 | -5.6125 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC5907 | xi_t_on_full_time_morphology | time_readout_diagnostic | 19 | 15.5294 | 8.95041 | 9.11957 | -5.48812 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC7331 | base_projection_morphology | reference | 36 | 22.2557 | 17.2117 | 17.631 | 16.2559 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC7331 | full_time_morphology_additive_proxy | reference | 36 | 22.2785 | 17.2705 | 17.6604 | 16.3732 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC7331 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 36 | 22.4106 | 17.5777 | 17.8863 | 16.9074 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| NGC7331 | xi_t_on_full_time_morphology | time_readout_diagnostic | 36 | 22.4393 | 17.6439 | 17.9302 | 17.0252 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| UGC12506 | xi_t_on_full_time_morphology | time_readout_diagnostic | 31 | 62.9679 | 64.2629 | 60.8865 | -60.8865 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| UGC12506 | full_time_morphology_additive_proxy | reference | 31 | 64.1192 | 65.3242 | 62.4477 | -62.4477 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| UGC12506 | xi_t_on_base_projection_morphology | time_readout_diagnostic | 31 | 67.9037 | 68.8153 | 66.9705 | -66.9705 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |
| UGC12506 | base_projection_morphology | reference | 31 | 69.1788 | 70.0189 | 68.4276 | -68.4276 | False | True | False | time_readout_xi_trial_diagnostic_not_endpoint_validation |

Figure: `figures/endpoint_diagnostics/time_readout_xi_trial_galaxy_rotation_curves.png`
