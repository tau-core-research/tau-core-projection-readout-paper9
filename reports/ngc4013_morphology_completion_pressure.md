# NGC4013 Morphology-Completion Pressure Audit

**Doc class:** claim-boundary audit

**Reader role:** Paper 9 projection/mixed replay maintainer

**Status:** `PURE_WVO_UNDERCOMPLETE_EXPONENTIAL_CARRIER_NEEDED`

**Claim boundary:** `ngc4013_morphology_completion_pressure_not_validation`

## Purpose

This audit explains why the best wrong-family control can beat the pure
NGC4013 WVO route without making the result a true negative against the
Tau Core morphology-readout program. It reads frozen score summaries only;
it does not fit a new curve.

## Summary

| galaxy | matched_route | matched_rmse_km_s | best_wrong_family | best_wrong_rmse_km_s | matched_minus_best_wrong_km_s | matched_minus_wrong_mean_km_s | prospective_mixed_protocol | prospective_mixed_rmse_km_s | inner_prewarp_kernel_active | outer_window_wvo_minus_tpg_km_s | completion_verdict | true_negative_against_tau_core | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | matched_K_warp_vertical_overlay | 11.4505 | wrong_K_exponential_disk | 10.8802 | 0.570288 | -1.5493 | exponential_disk_plus_wvo | 10.6148 | False | -1.03689 | PURE_WVO_UNDERCOMPLETE_EXPONENTIAL_CARRIER_NEEDED | False | False | ngc4013_morphology_completion_pressure_not_validation |

## Candidate Ranking

| galaxy | candidate_id | candidate_role | rmse | endpoint_scores_allowed | claim_boundary | rank_all_candidates |
| --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | wrong_K_exponential_disk | wrong_family_control | 10.8802 | True | ngc4013_morphology_completion_pressure_not_validation | 1 |
| NGC4013 | wrong_K_thick_flared | wrong_family_control | 11.3922 | True | ngc4013_morphology_completion_pressure_not_validation | 2 |
| NGC4013 | matched_K_warp_vertical_overlay | matched_caveated_replacement_family | 11.4505 | True | ngc4013_morphology_completion_pressure_not_validation | 3 |
| NGC4013 | baseline_TPG_v6 | external_baseline | 12.2739 | True | ngc4013_morphology_completion_pressure_not_validation | 4 |
| NGC4013 | wrong_K_scale_tail_spiral | wrong_family_control | 12.7332 | True | ngc4013_morphology_completion_pressure_not_validation | 5 |
| NGC4013 | baseline_MOND | external_baseline | 14.3342 | True | ngc4013_morphology_completion_pressure_not_validation | 6 |
| NGC4013 | wrong_K_compact_finite_rejected | wrong_family_control_rejected_original | 16.9936 | True | ngc4013_morphology_completion_pressure_not_validation | 7 |
| NGC4013 | baseline_Newtonian | external_baseline | 65.6913 | True | ngc4013_morphology_completion_pressure_not_validation | 8 |

## Component Assignment

| component | source_role | current_status | allowed_use | blocked_use | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| regular_exponential_disk_carrier | global disk carrier / inner-to-full-curve support | suggested by best wrong-family control and prospective protocol | prospective mixed kernel component on future holdout/analogue | retroactive NGC4013 endpoint validation from the old score | ngc4013_morphology_completion_pressure_not_validation |
| warp_vertical_overlay | outer warp / vertical-overlay correction | caveated replay-allowed after non-overlap ledger | NGC4013 caveated replay/control evidence | full-profile standalone morphology claim | ngc4013_morphology_completion_pressure_not_validation |
| observer_path_projection | line-of-sight orientation and projection caveat | context component assigned to WVO/mixed route | projection context inside the shared WVO contribution | independent amplitude or clock factor | ngc4013_morphology_completion_pressure_not_validation |
| time_clock_projection_Xi_t | independent clock/readout route | blocked for NGC4013 | diagnostic only until independent non-overlap clock source exists | reuse of warp/vertical/lag evidence already assigned to WVO | ngc4013_morphology_completion_pressure_not_validation |

## Interpretation

The best wrong-family control is `wrong_K_exponential_disk`. This is not
surprising for NGC4013: a regular exponential-disk carrier can describe the
global disk trend better than a pure outer warp/vertical-overlay correction.
The WVO kernel is source-supported, but the radial-zone audit shows it is an
outer-lane correction: it is inactive before the warp window and improves the
active outer window.

Therefore the result is not a true negative. It is morphology-completion
pressure: the source-supported full readout should likely be a mixed kernel
with an exponential-disk carrier plus WVO/observer-path correction. The
existing expdisk+WVO protocol score points in that direction, but remains
prospective-only for NGC4013.

## Allowed Claim

`NGC4013 supports the need for a mixed morphology readout: regular disk
carrier plus warp/vertical-overlay projection. Pure WVO is undercomplete,
but source-supported in its active outer lane.`

## Disallowed Claims

- endpoint validation of expdisk+WVO on NGC4013
- population validation
- treating `wrong_K_exponential_disk` as a literal wrong-family defeat
- promoting independent `Xi_t` from the same source facts
