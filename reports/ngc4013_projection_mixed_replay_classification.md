# NGC4013 Projection/Mixed Replay Classification

**Doc class:** replay classification audit

**Reader role:** Paper 9 projection/mixed endpoint maintainer

**Status:** `WVO_MIXED_REPLAY_ALLOWED_XIT_BLOCKED_EXPDISK_WVO_PROSPECTIVE`

**Claim boundary:** `ngc4013_projection_mixed_replay_classification_not_validation`

## Purpose

This audit applies the NGC4013 source-token non-overlap ledger to the
existing score ladder. It does not introduce a new score and does not
read observed velocities or residuals. Its role is to say which old
number can be interpreted as a caveated replay/control result after the
source channels have been separated.

## Summary

| galaxy | status | allowed_replay_route | blocked_route | prospective_only_route | wvo_rmse_km_s | wvo_minus_tpg_v6_km_s | wvo_minus_mond_km_s | wvo_minus_compact_proxy_km_s | matched_minus_wrong_mean_km_s | matched_minus_wrong_best_km_s | matched_beats_all_wrong_families | active_window_weighted_wvo_minus_tpg_rmse | compact_proxy_rmse_km_s | expdisk_wvo_protocol_rmse_km_s | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | WVO_MIXED_REPLAY_ALLOWED_XIT_BLOCKED_EXPDISK_WVO_PROSPECTIVE | warp_vertical_overlay | independent_Xi_t_clock_overlay | exponential_disk_plus_wvo_frozen_protocol | 11.4505 | -0.823417 | -2.88373 | -5.54307 | -1.5493 | 0.570288 | False | -1.03689 | 16.9936 | 10.6148 | False | ngc4013_projection_mixed_replay_classification_not_validation |

## Route Classification

| galaxy | route | rmse_km_s | previous_score_role | nonoverlap_classification | allowed_after_nonoverlap | endpoint_validation_claim | uses_vobs_or_residual_in_construction | scoring_used_vobs | reason | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | original_compact_proxy | 16.9936 | baseline_for_morphology_refinement | SOURCE_REJECTED_STARTING_PROXY | False | False | False | True | Retained only as the rejected/refined-away starting proxy. | ngc4013_projection_mixed_replay_classification_not_validation |
| NGC4013 | warp_vertical_overlay | 11.4505 | caveated_preliminary_endpoint_control | CAVEATED_WVO_MIXED_REPLAY_ALLOWED | True | False | False | True | Warp, vertical, lag, and observer/path tokens are assigned to one WVO/mixed projection contribution without independent Xi_t reuse. | ngc4013_projection_mixed_replay_classification_not_validation |
| NGC4013 | exponential_disk_plus_wvo_frozen_protocol | 10.6148 | prospective_protocol_score_not_retroactive_endpoint | PROSPECTIVE_PROTOCOL_ONLY | False | False | False | True | Best NGC4013 score in this packet, but the non-overlap ledger does not retroactively promote it to endpoint validation. | ngc4013_projection_mixed_replay_classification_not_validation |

## Wrong-Family Control

| galaxy | matched_candidate | n_wrong_family_controls | matched_rmse | wrong_family_mean_rmse | wrong_family_best_rmse | matched_minus_wrong_mean | matched_minus_wrong_best | matched_beats_all_wrong_families | family_label_null_mean_rmse | matched_minus_family_label_null_mean | matched_rank_among_family_labels | n_family_label_candidates | uniform_label_null_best_probability | control_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | matched_K_warp_vertical_overlay | 4 | 11.4505 | 12.9998 | 10.8802 | -1.5493 | 0.570288 | False | 12.6899 | -1.23944 | 3 | 5 | 0.2 | NEGATIVE_RESULT_MATCHED_DOES_NOT_BEAT_ALL_WRONG_FAMILIES | ngc4013_projection_mixed_replay_classification_not_validation |

## Radial-Zone Diagnostic

| galaxy | r_warp_kpc | r_outer_kpc | inner_n_points | inner_K_wvo_mean | inner_rmse_warp_vertical_overlay | inner_rmse_tpg_v6 | inner_wvo_minus_tpg_rmse | active_window_points | active_window_weighted_wvo_minus_tpg_rmse | outer_lane_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | 10 | 11.2 | 7 | 0 | 12.7954 | 12.7954 | 0 | 29 | -1.03689 | WARP_VERTICAL_OVERLAY_ENDPOINT_IS_OUTER_LANE_NOT_FULL_PROFILE | ngc4013_projection_mixed_replay_classification_not_validation |

## Interpretation

The source-supported route is the warp/vertical-overlay mixed projection
route. It improves the rejected compact proxy from 16.99 km/s to 11.45
km/s RMSE, and the source-token ledger permits it as a caveated replay
because the warp, vertical, lag, and observer/path evidence are assigned
to one shared mixed-projection contribution.

The wrong-family control is deliberately preserved as a caveat: WVO beats
the wrong-family mean but not the best wrong-family control. The correct
status is therefore caveated replay/control evidence, not endpoint
validation.

The radial-zone diagnostic says the WVO lane is an outer-lane correction:
it is inactive in the inner pre-warp window and improves the active outer
window relative to the TPG/v6 carrier.

The independent clock/time route remains blocked. The available facts
are exactly the morphology/projection facts already used by WVO, so using
them again as `Xi_t` would double-count the same source tokens.

The exponential-disk plus WVO protocol remains prospective-only. Its
10.61 km/s score is useful as a protocol target, but not retroactive
endpoint validation.

## Allowed Claim

`NGC4013 shows source-supported morphology/projection refinement evidence
for the WVO mixed route, under caveated single-galaxy replay/control
status.`

## Disallowed Claims

- population validation
- retroactive validation of the expdisk+WVO protocol score
- independent `Xi_t` endpoint for NGC4013 from the same source tokens
- a new gravitational-law claim
