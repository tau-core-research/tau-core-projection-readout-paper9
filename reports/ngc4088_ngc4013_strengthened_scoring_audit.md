# NGC4088/NGC4013 Strengthened Scoring Audit

This audit records the numerical consequence of the strengthened source review.  It does not use scores to choose morphology labels. It only summarizes frozen endpoint/control score artifacts after the source-side review has been recorded.

## Summary

| galaxy | score_verdict | headline | endpoint_reading | source_review_effect | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4013 | SOURCE_REFINEMENT_IMPROVES_BUT_STRONGEST_ROUTE_PROSPECTIVE | Compact proxy 16.99 -> WVO 11.45 -> expdisk+WVO 10.61 km/s. | WVO is caveated preliminary; expdisk+WVO is prospective protocol, not retroactive endpoint validation. | Strengthened numeric lag/warp/vertical-component source evidence supports the mixed-overlay direction. | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | BASE_ENDPOINT_STRONG_CONTROLS_IMPROVE_BUT_NUMERIC_KERNEL_STILL_BLOCKED | Accepted warp/history 11.62 km/s beats best baseline 25.40 km/s; controls can reach 9.39/10.50/8.38 km/s. | Accepted warp/history remains endpoint-readable as a caveated single-galaxy control; additive/clock refinements are controls. | Strengthened qualitative H I/PV evidence supports the broad class, but not new endpoint-grade numeric x_warp/q_warp fields. | ngc4088_ngc4013_strengthened_scoring_audit |

## Scores

| galaxy | route | rmse_km_s | reference_rmse_km_s | delta_vs_reference_km_s | reference | score_role | endpoint_scores_allowed | endpoint_validation_claim | interpretation | construction_used_vobs | scoring_used_vobs | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4013 | original_compact_proxy | 16.9936 |  |  | starting compact proxy | baseline_for_morphology_refinement | False | False | Original simple morphology proxy; retained as source-rejected starting point. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4013 | warp_vertical_overlay | 11.4505 | 16.99356852880305 | -5.543073115591316 | original compact proxy | caveated_preliminary_endpoint_control | True | False | Source-supported WVO refinement improves strongly over compact proxy and also beats the local TPG/v6 and MOND comparators in this artifact. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4013 | exponential_disk_plus_wvo_frozen_protocol | 10.6148 | 11.450495413211732 | -0.8357371244374345 | WVO endpoint route | prospective_protocol_score_not_retroactive_endpoint | False | False | Strongest NGC4013 score in this packet, but it is a prospective source-frozen protocol reference, not retroactive validation. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | accepted_warp_history | 11.619 | 25.396289301523897 | -13.7772513124978 | NEWTONIAN_vn | caveated_accepted_endpoint_preliminary_control | True | False | Accepted warp/history route remains strong and beats all local baselines and wrong-family controls; this is still a single-galaxy caveated control result. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | additive_warp_history_control | 9.39119 | 11.619037989026095 | -2.2278484573332626 | base projection | control_replay_not_new_endpoint | False | False | Improves over the base projection, but the strengthened review did not supply new endpoint-grade numeric x_warp/q_warp fields. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | clock_only_control | 10.4959 | 11.619037989026095 | -1.1231371605423721 | base projection | diagnostic_control_not_endpoint | False | False | Clock-only replay improves modestly, but remains diagnostic because independent non-overlap clock evidence is not frozen. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | additive_plus_clock_stress | 8.38352 | 11.619037989026095 | -3.2355184458973554 | base projection | stress_control_double_count_blocked | False | False | Best numerical stress score, but explicitly blocked from endpoint interpretation because additive and clock channels overlap. | False | True | ngc4088_ngc4013_strengthened_scoring_audit |

## Gates

| galaxy | gate | status | evidence | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| NGC4013 | WVO_SOURCE_REFINEMENT_SCORE | PASS_CAVEATED_SCORE | WVO improves over source-rejected compact proxy by 5.54 km/s RMSE. | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4013 | EXPDISK_WVO_STRONGEST_SCORE | PROSPECTIVE_ONLY | 10.61 km/s RMSE is best in this packet, but retrospective endpoint scores remain disallowed. | False | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | BROAD_CLASS_ACCEPTED_ENDPOINT | PASS_CAVEATED_SCORE | Accepted route beats all baselines and all wrong-family controls. | True | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | NUMERIC_KERNEL_PROMOTION | BLOCKED | New source review is qualitative; x_warp/q_warp/memory/epsilon_cross are not newly accepted numeric fields. | False | ngc4088_ngc4013_strengthened_scoring_audit |
| NGC4088 | ADDITIVE_PLUS_CLOCK_STRESS | CONTROL_ONLY_DOUBLE_COUNT_BLOCKED | RMSE improves to 8.38 km/s, but source-channel overlap blocks endpoint interpretation. | False | ngc4088_ngc4013_strengthened_scoring_audit |

## Interpretation

NGC4013 shows a clear source-refinement ladder: the source-supported warp/vertical-overlay route improves over the compact proxy, and the exponential-disk plus WVO frozen protocol improves further.  The latter is still prospective/protocol-only, not retroactive validation.

NGC4088 remains strong on the accepted warp/history endpoint route. The source-strengthening packet supports the broad class but does not yet promote new numeric kernel fields, so the additive and clock improvements remain controls or stress tests.
