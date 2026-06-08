# Problematic Projection-Channel Next Gates

This artifact converts the projection-channel ledger into executable next
gates. It does not run or authorize endpoint scoring.

## Summary

| next_gate_status | n_galaxies | n_control_or_scoring_allowed | n_endpoint_allowed | ugc12506_shell_status | ngc7331_qwarp_status | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PROBLEMATIC_PROJECTION_CHANNEL_NEXT_GATES_BUILT_NOT_ENDPOINT | 6 | 2 | 0 | UGC12506_SOURCE_NATIVE_NFW_HSE_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | NGC7331_THINGS_QWARP_FIRST_PASS_SOURCE_NATIVE_REVIEW_REQUIRED | UGC12506 and NGC4088 have control/replay paths; all endpoint promotions remain blocked by source-freeze or non-overlap gates | problematic_projection_channel_next_gates_not_endpoint |

## Gates

| galaxy | priority_channel | gate_status | required_comparison | endpoint_allowed_now |
| --- | --- | --- | --- | --- |
| UGC12506 | mass_distribution_plus_metric_closure | CONTROL_REPLAY_READY_ENDPOINT_BLOCKED | ablate source-native NFW/HSE against Theta_morph-only, Theta+Xi_t cap-only, and source-envelope controls | False |
| NGC4088 | trajectory_phase_asymmetry_history | NO_NEW_ENDPOINT_KEEP_ACCEPTED_ADDITIVE_ROUTE | preserve clock replay as control; reopen clock endpoint only with new non-overlapping source clock evidence | False |
| NGC4013 | mixed_warp_vertical_overlay | BLOCKED_CURRENT_XIT_REJECTED | find uninspected analogue or independent clock observable before any new scoring | False |
| NGC7331 | source_sharpened_vertical_outer_warp | REPLAY_PATH_EXISTS_ENDPOINT_NOT_PROMOTED | freeze narrower q_warp/vertical window before testing metric/closure or refined mixed replay | False |
| NGC5907 | observer_path_edgeon_projection | SATURATED_CONTROL_NO_NEW_LAYER | only source-native path/vertical-profile evidence can justify a richer kernel | False |
| NGC4183 | quiet_weak_projection_limit | RETAIN_NULL_CONTROL | no active projection channel without new source evidence | False |
