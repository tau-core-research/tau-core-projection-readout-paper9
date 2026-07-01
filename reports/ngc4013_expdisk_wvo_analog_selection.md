# NGC4013 Expdisk+WVO Prospective Analog Selection

**Doc class:** source-side analog selection audit

**Reader role:** Paper 9 projection/mixed replay maintainer

**Status:** `EXPDISK_WVO_ANALOG_SELECTION_READY_NOT_ENDPOINT`

**Claim boundary:** `ngc4013_expdisk_wvo_analog_selection_not_endpoint`

## Purpose

NGC4013 showed a useful but dangerous pattern: the pure WVO route is
source-supported in the outer lane, while the best wrong-family control is
`K_exponential_disk`. The correct interpretation is not that a wrong label
wins, but that the source-supported readout is undercomplete unless a
regular disk carrier is combined with the WVO correction.

This audit therefore selects prospective analogues and controls for testing
the mixed `exponential disk + WVO` idea without promoting the existing
NGC4013 score retroactively.

## Summary

| status | ngc4013_completion_verdict | ngc4013_matched_minus_best_wrong_km_s | ngc4013_prospective_mixed_rmse_km_s | primary_reference_analog | primary_reference_status | fresh_holdout_candidate | fresh_holdout_status | quiet_control | stress_not_clean_analog | endpoint_scores_run_here | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXPDISK_WVO_ANALOG_SELECTION_READY_NOT_ENDPOINT | PURE_WVO_UNDERCOMPLETE_EXPONENTIAL_CARRIER_NEEDED | 0.570288 | 10.6148 | NGC7331 | NGC7331_source_sharpened_replay_positive_exact_transfer_blocked | UGC07151_if_source_orientation_and_warp_pass | UGC07151_fast_preflight_blocks_WVO | NGC4183 | UGC12506 | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |

## Selection Rules

| rule_id | rule | status | claim_boundary |
| --- | --- | --- | --- |
| A1 | An analog may be selected from source morphology/projection ledgers, not from residual shape. | ACTIVE | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| A2 | NGC4013 expdisk+WVO remains prospective-only and cannot be retroactively promoted. | ACTIVE | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| A3 | Existing scored analogues can serve as references, but not as fresh holdout validation. | ACTIVE | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| A4 | A fresh candidate needs source-native regular disk carrier plus independent vertical/warp/onset support. | ACTIVE | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| A5 | Quiet disks and stress/path-closure cases are controls, not forced WVO successes. | ACTIVE | ngc4013_expdisk_wvo_analog_selection_not_endpoint |

## Candidate Ledger

| galaxy | analog_role | selection_status | source_fields_or_label | projection_label | available_rmse_context | queue_priority | primary_blocker | full_time_trial_context | reference_sharpening_context | recommended_next_action | allowed_endpoint_use_now | uses_vobs_or_residual_for_selection | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | closest already-scored expdisk plus vertical/outer-warp analogue | REFERENCE_ANALOG_ALREADY_SCORED_CAVEATED_NOT_FRESH_HOLDOUT | H I warp/history plus vertical-scale source context | vertical_outer_warp_overlay | matched=22.256; delta_simpler=-1.217; delta_wrong_mean=-0.417 |  | broad outer-warp window and wrong-label replay caveats | source=vertical_outer_warp_overlay; delta=0.022846 | v3_rmse=22.131; v3_minus_v1=-0.125; exact_blocker=build frozen exact-transfer manifest carrying q_warp interval and sign rule | use as logic/reference analogue only; source-sharpen the outer-warp window before any stronger claim | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| NGC5907 | edge-on projection/vertical-warp analogue | PROJECTION_ANALOG_NOT_EXPDISK_WVO_EXACT | edge-on geometry, warp/truncation, projection/ISM source context | edge_on_projection_vertical_warp | matched=16.373; delta_simpler=-0.997; delta_wrong_mean=-0.683 |  | fresh single-galaxy preliminary control; wrong-label replay remains tight | source=edgeon_projection_vertical_warp; delta=-0.000153 |  | retain as projection-saturated control unless source-native vertical profile data justify a richer replay | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| NGC4183 | quiet exponential-disk / weak-projection control | QUIET_OR_WEAK_PROJECTION_CONTROL |  |  |  |  |  | source=weak_projection_null_control; delta=-0.001911 |  | retain as null/weak-projection control; do not force WVO if source morphology remains quiet | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| UGC07151 | fresh exponential-disk projection queue candidate | FAST_PREFLIGHT_WVO_BLOCKED_EDGEON_TRUNCATION_CONTROL |  | projection_review_for_K_exponential_disk |  | P1_acquire_after_P0 | blocked_or_negative |  |  | preserve as edge-on/truncation control unless independent WVO/onset evidence is acquired | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |
| UGC12506 | stress exponential-disk projection candidate | STRESS_CASE_NOT_CLEAN_WVO_ANALOG |  | projection_review_for_K_exponential_disk |  | P0_acquire_first | orientation_gate_blocked |  |  | keep as stress/path-closure case; not the clean first test of NGC4013 expdisk+WVO completion | False | False | ngc4013_expdisk_wvo_analog_selection_not_endpoint |

## Verdict

The strongest already processed analogue is NGC7331, because it already has
an exponential-disk carrier plus vertical/outer-warp mixed route. It is not
a fresh holdout, so it should be used as a reference analogue and not as
new validation. The source-sharpened V3 replay is positive, but the
exact-transfer upgrade is still blocked by source-native warp-amplitude,
sign, and cross-term requirements.

NGC5907 is useful as an edge-on projection analogue, but not an exact
expdisk+WVO analogue. NGC4183 is useful as a quiet/weak-projection control.
UGC12506 is a stress/path-closure case, not the clean first test of this
specific completion. UGC07151 was the fastest fresh queue candidate; the
fast preflight now treats it as edge-on/truncation control unless
independent WVO/onset evidence is acquired.

## Next Finite Action

For a clean prospective test, either source-sharpen the already processed
NGC7331 vertical/outer-warp reference analogue, or acquire a new
exponential-disk candidate with independent vertical/warp/onset support.
The candidate can then freeze the expdisk+WVO formula before scoring.
Until that source freeze exists, NGC4013 remains a morphology
completion-pressure case rather than a validation endpoint.

## Disallowed Claims

- no endpoint validation is claimed here
- no population validation is claimed here
- NGC4013 expdisk+WVO is not retroactively promoted
- quiet controls are not forced into WVO
- stress/path-closure galaxies are not treated as clean WVO analogues
