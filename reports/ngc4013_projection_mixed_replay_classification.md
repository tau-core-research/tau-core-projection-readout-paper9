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

| galaxy | status | allowed_replay_route | blocked_route | prospective_only_route | wvo_rmse_km_s | compact_proxy_rmse_km_s | expdisk_wvo_protocol_rmse_km_s | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | WVO_MIXED_REPLAY_ALLOWED_XIT_BLOCKED_EXPDISK_WVO_PROSPECTIVE | warp_vertical_overlay | independent_Xi_t_clock_overlay | exponential_disk_plus_wvo_frozen_protocol | 11.4505 | 16.9936 | 10.6148 | False | ngc4013_projection_mixed_replay_classification_not_validation |

## Route Classification

| galaxy | route | rmse_km_s | previous_score_role | nonoverlap_classification | allowed_after_nonoverlap | endpoint_validation_claim | uses_vobs_or_residual_in_construction | scoring_used_vobs | reason | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | original_compact_proxy | 16.9936 | baseline_for_morphology_refinement | SOURCE_REJECTED_STARTING_PROXY | False | False | False | True | Retained only as the rejected/refined-away starting proxy. | ngc4013_projection_mixed_replay_classification_not_validation |
| NGC4013 | warp_vertical_overlay | 11.4505 | caveated_preliminary_endpoint_control | CAVEATED_WVO_MIXED_REPLAY_ALLOWED | True | False | False | True | Warp, vertical, lag, and observer/path tokens are assigned to one WVO/mixed projection contribution without independent Xi_t reuse. | ngc4013_projection_mixed_replay_classification_not_validation |
| NGC4013 | exponential_disk_plus_wvo_frozen_protocol | 10.6148 | prospective_protocol_score_not_retroactive_endpoint | PROSPECTIVE_PROTOCOL_ONLY | False | False | False | True | Best NGC4013 score in the old packet, but the non-overlap ledger does not retroactively promote it to endpoint validation. | ngc4013_projection_mixed_replay_classification_not_validation |

## Interpretation

The source-supported route is the warp/vertical-overlay mixed projection
route. It improves the rejected compact proxy from 16.99 km/s to 11.45
km/s RMSE, and the source-token ledger permits it as a caveated replay
because the warp, vertical, lag, and observer/path evidence are assigned
to one shared mixed-projection contribution.

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
