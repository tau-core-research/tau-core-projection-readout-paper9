# NGC4088 Time-Projection Accepted Combined-Route Handoff

This artifact records the route policy after the double-count audit. It
does not compute a new endpoint score. The accepted combined route is
the caveated accepted additive warp/history endpoint with `Xi_eff=1`.

## Summary

| handoff_status | galaxy | accepted_combined_route | accepted_combined_rmse_km_s | clock_only_control_rmse_km_s | additive_plus_clock_stress_rmse_km_s | stress_test_improves_over_accepted_route | stress_test_endpoint_allowed | clock_only_control_preserved | time_endpoint_reopened | requires_new_nonoverlap_clock_evidence | construction_used_vobs | reads_endpoint_scores_for_handoff | endpoint_scores_allowed_for_accepted_combined_route | endpoint_validation_claim | claim_status | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088_ACCEPTED_COMBINED_ROUTE_HANDOFF_READY | NGC4088 | additive_warp_history_endpoint_with_Xi_eff_equal_one | 11.619 | 10.4959 | 8.38352 | True | False | True | False | True | False | True | True | False | single-galaxy caveated accepted route plus time-projection control; not population validation | ngc4088_time_projection_accepted_combined_route_handoff |

## Routes

| galaxy | route_id | route_status | xi_eff_policy | rmse_km_s | control_replay_allowed | endpoint_scores_allowed | endpoint_validation_claim | interpretation | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | ACCEPTED_COMBINED_ADDITIVE_WARP_HISTORY_XI_ONE | ACCEPTED_ENDPOINT_ROUTE | Xi_eff=1 | 11.619 | False | True | False | same numerical curve as the caveated accepted additive warp/history endpoint after double-count resolution | ngc4088_time_projection_accepted_combined_route_handoff |
| NGC4088 | CLOCK_ONLY_XIEFF_ON_BASE_PROJECTION | CONTROL_ROUTE_ALLOWED_NOT_ENDPOINT | active only on the base projection control | 10.4959 | True | False | False | useful clock/readout control signal, not an accepted endpoint | ngc4088_time_projection_accepted_combined_route_handoff |
| NGC4088 | ADDITIVE_WARP_HISTORY_PLUS_XIEFF | STRESS_TEST_REJECTED_FOR_ENDPOINT | forbidden with the additive kernel until non-overlap clock evidence exists | 8.38352 | False | False | False | improves numerically but double-counts source evidence | ngc4088_time_projection_accepted_combined_route_handoff |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| N4088_TPH_G1_ADDITIVE_ENDPOINT_EXISTS | PASS | CAVEATED_ACCEPTED_ENDPOINT_PRELIMINARY_CONTROL_RESULT | retain single-galaxy caveated status | NGC4088 | ngc4088_time_projection_accepted_combined_route_handoff |
| N4088_TPH_G2_DOUBLE_COUNT_RESOLVED | PASS | NGC4088_DOUBLE_COUNT_RESOLVED_ACCEPTED_COMBINED_XI_ONE | keep Xi_eff=1 for the combined route | NGC4088 | ngc4088_time_projection_accepted_combined_route_handoff |
| N4088_TPH_G3_CLOCK_CONTROL_PRESERVED | PASS_CONTROL_ONLY | ADDITIVE_PLUS_CLOCK_IMPROVES_BUT_DOUBLE_COUNT_BLOCKED | do not present clock-only replay as endpoint validation | NGC4088 | ngc4088_time_projection_accepted_combined_route_handoff |
| N4088_TPH_G4_STRESS_TEST_NOT_ENDPOINT | PASS_GUARDRAIL | additive-plus-clock stress RMSE is lower but endpoint permission is false | new endpoint requires independent non-overlap clock evidence | NGC4088 | ngc4088_time_projection_accepted_combined_route_handoff |

## Claim Boundary

The clock-only route remains a useful control signal. The additive-plus-
clock stress curve is not endpoint-permitted, even though it improves
the RMSE, because every current `Xi_eff` source term overlaps the active
additive warp/history morphology route.
