# UGC12506 Theta_morph / Xi_t Separation Gate

This gate records the post-refinement separation of the UGC12506 channels.
It is not an endpoint and does not introduce a new fitted curve.

## Verdict

| separation_status | galaxy | theta_channel_role | xit_channel_role | formula_roles_distinct | source_overlap_present | overlap_terms | path_term_established | theta_endpoint_allowed | xit_standard_endpoint_allowed | xit_control_replay_allowed | combined_endpoint_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_THETA_XIT_CHANNELS_SEPARATED_ENDPOINT_STILL_BLOCKED | UGC12506 | additive_morphology_phase_kernel | multiplicative_clock_readout_interval_control | True | True | high_spin | False | False | False | True | False | False | either source-freeze non-overlap evidence for a combined route, or keep Theta_morph diagnostic and Xi_t as a caveated interval/control | ugc12506_theta_xit_channels_separated_not_combined_endpoint |

## Channel Roles

| galaxy | channel_id | formula_role | formula_text | source_role | source_terms | rmse_context_km_s | status | endpoint_allowed | uses_vobs_or_residual_in_construction | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | THETA_MORPH | additive_morphology_phase_kernel | v_theta^2(R)=v_projection_history^2(R)+A_theta K_theta(R); K_theta is source-frozen late-settling morphology phase | late-settling morphology/trajectory phase | extended_low_density_hi; hi_extent_asymmetry_phase; high_inclination; high_spin; late_settling_outer_shape | 64.1192 | DIAGNOSTIC_ONLY_NOT_ENDPOINT | False | False | ugc12506_theta_xit_channels_separated_not_combined_endpoint |
| UGC12506 | XI_T | multiplicative_clock_readout_interval_control | Xi_t(R)=1+epsilon_t K_t(R) | clock/readout interval control | asymmetric_pv_phase; edgeon_pv_clock_slice; envelope_settling; high_spin; path_environment_zero | 76.4856 | CAVEATED_INTERVAL_CONTROL_NOT_ENDPOINT | False | False | ugc12506_theta_xit_channels_separated_not_combined_endpoint |

## Source Overlap Audit

| galaxy | overlap_id | overlap_terms | source_overlap_present | path_term_established | asymmetry_policy | path_policy | nonoverlap_conclusion | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_THETA_XIT_SOURCE_OVERLAP | high_spin | True | False | asymmetry remains caveated phase component, not standalone route driver | path term fixed to zero unless later source path review establishes it | formula roles are separated, but source context partially overlaps; combined endpoint remains blocked | ugc12506_theta_xit_channels_separated_not_combined_endpoint |

## Gates

| gate_id | gate_status | gate_text | endpoint_allowed | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| U12506_SEP_G1_FORMULA_ROLE | PASS_SEPARATED | Theta_morph is additive in v^2; Xi_t is a multiplicative clock/readout factor. | False | UGC12506 | ugc12506_theta_xit_channels_separated_not_combined_endpoint |
| U12506_SEP_G2_CLAIM_BOUNDARY | PASS_RECORDED | Theta_morph is diagnostic; Xi_t is caveated interval/control. | False | UGC12506 | ugc12506_theta_xit_channels_separated_not_combined_endpoint |
| U12506_SEP_G3_SOURCE_OVERLAP | BLOCK_COMBINED_ENDPOINT | High-spin/envelope/asymmetry context overlaps across routes; no combined endpoint without non-overlap manifest. | False | UGC12506 | ugc12506_theta_xit_channels_separated_not_combined_endpoint |
| U12506_SEP_G4_PATH_TERM | BLOCK_PATH_CLOCK_ENDPOINT | path term fixed to zero unless later source path review establishes it | False | UGC12506 | ugc12506_theta_xit_channels_separated_not_combined_endpoint |
| U12506_SEP_G5_FORBIDDEN_INPUTS | PASS | Separation gate reads only source/control summaries and does not select a curve-saving amplitude. | False | UGC12506 | ugc12506_theta_xit_channels_separated_not_combined_endpoint |

## Interpretation

`Theta_morph` and `Xi_t` are now clearly separated by formula role. `Theta_morph` is an additive morphology/trajectory phase diagnostic, whereas `Xi_t` is a small multiplicative clock/readout interval control. However, the UGC12506 source context still overlaps through high-spin, envelope, and asymmetry evidence. Therefore the separation supports cleaner channel accounting, but it does not authorize a combined endpoint.

