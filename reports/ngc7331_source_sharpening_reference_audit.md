# NGC7331 Source-Sharpening Reference Audit

**Doc class:** reference-analogue consolidation audit

**Reader role:** Paper 9 projection/mixed replay maintainer

**Status:** `REFERENCE_ANALOG_SOURCE_SHARPENED_REPLAY_POSITIVE_EXACT_TRANSFER_BLOCKED`

**Claim boundary:** `ngc7331_source_sharpening_reference_not_new_validation`

## Purpose

This audit records what NGC7331 contributes after UGC07151 failed the
fast WVO holdout preflight. It does not run a new score. It consolidates
already generated Paper8 summary artifacts into the Paper9 source-completion
logic.

## Summary

| galaxy | status | reference_role | v1_caveated_rmse_km_s | v3_source_sharpened_rmse_km_s | v3_minus_v1_rmse_km_s | v3_minus_best_baseline_rmse_km_s | v3_minus_wrong_projection_rmse_km_s | fractional_onset_kpc | fractional_onset_over_rhi | exact_transfer_status | exact_transfer_blocker | construction_used_vobs | scoring_used_vobs_in_source_audit | new_endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC7331 | REFERENCE_ANALOG_SOURCE_SHARPENED_REPLAY_POSITIVE_EXACT_TRANSFER_BLOCKED | already_processed_expdisk_vertical_outer_warp_reference | 22.2557 | 22.1308 | -0.124817 | -1.34213 | -0.775549 | 14.4317 | 0.534309 | EXACT_TRANSFER_FORMULA_FREEZE_PREP_READY_INTERVAL_CARRIED_ENDPOINT_BLOCKED | build frozen exact-transfer manifest carrying q_warp interval and sign rule | False | False | False | ngc7331_source_sharpening_reference_not_new_validation |

## Layer Ledger

| layer | status | what_it_shows | allowed_use_in_paper9 | blocked_use | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| V1_caveated_mixed_endpoint | CAVEATED_ACCEPTED_MIXED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | The expdisk plus vertical/outer-warp family can beat the local baseline and wrong-family controls, but with a broad outer-window caveat. | reference analogue for NGC4013 completion pressure | fresh population validation | ngc7331_source_sharpening_reference_not_new_validation |
| fractional_onset_source_gate | FRACTIONAL_WARP_ONSET_SOURCE_READY_REPLAY_REQUIRED | A residual-blind outer-warp onset exists: 14.432 kpc (0.534 RHI). | source-sharpening evidence | retroactive change to V1 endpoint | ngc7331_source_sharpening_reference_not_new_validation |
| V2_V3_replay_holdout | NGC7331_V2_V3_REPLAY_HOLDOUT_PRELIMINARY_CONTROL_RESULT | V3 source-sharpened replay improves V1 by -0.125 km/s and beats the wrong projection control in the replay packet. | single-galaxy replay/control support | updating the accepted V1 endpoint | ngc7331_source_sharpening_reference_not_new_validation |
| exact_transfer_upgrade | EXACT_TRANSFER_FORMULA_FREEZE_PREP_READY_INTERVAL_CARRIED_ENDPOINT_BLOCKED | Complex warp context is confirmed. A q_warp interval and epsilon_cross bound can now be carried into freeze preparation, but endpoint scoring remains blocked until a manifest exists. | blocker ledger for full kernel | endpoint scoring before exact-transfer manifest freeze | ngc7331_source_sharpening_reference_not_new_validation |

## Gates

| gate_id | gate_status | reason | endpoint_scores_allowed_here | claim_boundary |
| --- | --- | --- | --- | --- |
| N7331_REF_G1_REFERENCE_ANALOG | PASS_REFERENCE_ANALOG | NGC7331 already has expdisk plus vertical/outer-warp mixed readout evidence. | False | ngc7331_source_sharpening_reference_not_new_validation |
| N7331_REF_G2_SOURCE_SHARPENING | PASS_REPLAY_CONTROL_POSITIVE | V3 source-sharpened replay improves V1 and beats the wrong projection control. | False | ngc7331_source_sharpening_reference_not_new_validation |
| N7331_REF_G3_EXACT_TRANSFER | PASS_FREEZE_PREP_ENDPOINT_BLOCKED | q_warp interval and epsilon_cross bound are carried; exact-transfer manifest still missing. | False | ngc7331_source_sharpening_reference_not_new_validation |
| N7331_REF_G4_POPULATION_VALIDATION | BLOCKED_NOT_A_FRESH_HOLDOUT | This is an already processed reference analogue, not an independent population test. | False | ngc7331_source_sharpening_reference_not_new_validation |

## Interpretation

NGC7331 is now the strongest reference analogue for the NGC4013 completion
pressure result. It has an exponential-disk carrier plus vertical/outer-warp
mixed route. The V1 accepted endpoint remains caveated by the broad outer
window, but the source-only fractional-onset gate and V3 replay show that
source-sharpening moves in the expected direction.

The stronger exact-transfer kernel has advanced but remains endpoint-blocked.
The relevant source terms are no longer completely missing: the q_warp
interval and epsilon_cross bound can be carried into formula-freeze
preparation. A frozen manifest is still required before any endpoint score.

## Allowed Claim

`NGC7331 supports the expdisk plus vertical/outer-warp family as a
source-sharpened reference analogue, while preserving exact-transfer
blockers and the no-population-validation boundary.`

## Disallowed Claims

- no new endpoint score is produced here
- no population validation is claimed here
- the accepted V1 endpoint is not retroactively updated
- exact-transfer formula freeze is not allowed yet
