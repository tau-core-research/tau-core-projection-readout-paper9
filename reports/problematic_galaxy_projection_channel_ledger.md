# Problematic Galaxy Projection-Channel Candidate Ledger

This ledger records which additional Tau morphology-state projection
channels are plausible for the inspected problematic or caveated
galaxies. It is not endpoint scoring and it does not promote any new
rotation-curve correction.

## Summary

| ledger_status | n_galaxies | n_endpoint_allowed_now | interpretation | claim_boundary |
| --- | --- | --- | --- | --- |
| PROBLEMATIC_GALAXY_PROJECTION_CHANNEL_LEDGER_BUILT_NOT_ENDPOINT | 6 | 0 | candidate projection channels are identified, but every new channel remains source-freeze/ablation gated | problematic_projection_channel_ledger_not_endpoint |

## Compact Ledger

| galaxy | current_role | priority_channel | secondary_channels | evidence_status | next_gate |
| --- | --- | --- | --- | --- | --- |
| UGC12506 | primary_stress_case_underpredicted | mass_distribution_plus_metric_closure | observer_path_edgeon_projection; clock_readout_interval | candidate_channel_strong_stress_not_endpoint | derive source-frozen mass/envelope plus metric-closure readout and run ablation against Theta_morph and Xi_t cap-only controls |
| NGC4088 | improving_warp_history_asymmetry_case | trajectory_phase_asymmetry_history | clock_readout_control_only | accepted_additive_route_clock_control_only | keep accepted additive warp/history endpoint with Xi_eff=1; use clock replay as control unless independent clock evidence appears |
| NGC4013 | worsened_mixed_overlay_case | mixed_warp_vertical_overlay | none_for_current_Xi_t | current_clock_proxy_rejected_double_count | seek a fresh uninspected analogue or independent clock observable; otherwise preserve as retrospective mixed-reference control |
| NGC7331 | worsened_broad_outer_warp_case | source_sharpened_vertical_outer_warp | metric_closure_after_window_sharpening | broad_window_saturated_refinement_required | source-sharpen outer-warp/vertical window, then test metric/closure or refined mixed readout by replay before endpoint promotion |
| NGC5907 | near_neutral_projection_saturated_case | observer_path_edgeon_projection | warp_truncation_projection | projection_channel_saturated_control | treat as projection-saturated control; only source-native path or vertical-profile data can justify a richer channel |
| NGC4183 | weak_null_projection_control | quiet_weak_projection_limit | none | null_control_keep_low_channel | retain as null/weak-projection control |

## Guardrail

A channel is not allowed into endpoint scoring merely because it is
plausible. It must be source-frozen, assigned to a distinct ledger
channel, checked for overlap with active kernels, and tested by ablation.
