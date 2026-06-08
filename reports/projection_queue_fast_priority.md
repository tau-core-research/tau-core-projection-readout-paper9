# Projection Queue Fast Priority

This is a source-acquisition triage artifact, not an endpoint score.  It
uses the fast SPARC packet to decide where expensive source hunting is
most likely to pay off.  The baryonic-carrier gap is used only as a
descriptive acquisition-priority signal; it does not choose morphology
labels, kernels, amplitudes, or endpoint outcomes.

## Summary

| priority_status | n_queue_galaxies | n_p0 | n_p1 | n_low_efficiency | top_galaxy | top_three | selection_used_vobs_or_residual | contains_vobs_gap_for_acquisition_triage | endpoint_scores_run_here | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PROJECTION_QUEUE_FAST_PRIORITY_READY_NOT_ENDPOINT | 12 | 3 | 3 | 4 | UGC12506 | UGC12506,IC4202,IC2574 | False | True | False | projection_queue_fast_priority_acquisition_triage_not_endpoint |

## Ranked Queue

| fast_priority_rank | priority_tier | galaxy | projection_label | n_rotmod_points | quality_Q | inclination_deg | rhi_over_rdisk | fast_baryonic_gap_rmse_km_s | primary_blocker | next_action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | P0_acquire_first | UGC12506 | projection_review_for_K_exponential_disk | 31 | 2 | 86 | 7.99593 | 116.023 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 2 | P0_acquire_first | IC4202 | edge_on_smooth_disk_projection | 32 | 1 | 90 | 6.72176 | 74.9449 | projection_load_values_and_closure_normalization_unfrozen | resolve source-native H I regularity closure map or scalar-to-kernel theorem |
| 3 | P0_acquire_first | IC2574 | projection_review_for_K_scale_tail_spiral | 34 | 2 | 75 | 3.88849 | 23.7835 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 4 | P1_acquire_after_P0 | UGC07151 | projection_review_for_K_exponential_disk | 11 | 1 | 90 | 5.112 | 27.2224 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 5 | P1_acquire_after_P0 | UGCA444 | projection_review_for_K_scale_tail_spiral | 36 | 2 | 78 | 2.50602 | 14.4713 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 6 | P1_acquire_after_P0 | UGC06818 | projection_review_for_K_scale_tail_spiral | 8 | 2 | 75 | 5.00719 | 27.0704 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 7 | P3_low_efficiency_or_weak_data | UGC06983 | projection_review_for_K_scale_tail_spiral | 17 | 1 | 49 | 5.00623 | 54.5413 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 8 | P3_low_efficiency_or_weak_data | UGC06917 | projection_review_for_K_scale_tail_spiral | 11 | 1 | 56 | 4.59058 | 46.4399 | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required |
| 9 | P2_keep_in_queue | CamB | projection_review_for_K_scale_tail_spiral | 9 | 2 | 65 | 2.57447 | 3.35561 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 10 | P2_keep_in_queue | UGC07577 | projection_review_for_K_scale_tail_spiral | 9 | 2 | 63 | 2.3 | 2.44423 | memory_or_history_acceptance_blocked | replace inverse memory proxy with residual-blind source/history evidence or mark memory not required |
| 11 | P3_low_efficiency_or_weak_data | UGC04305 | projection_review_for_K_scale_tail_spiral | 22 | 3 | 40 | 6.38793 | 6.36156 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |
| 12 | P3_low_efficiency_or_weak_data | NGC6789 | projection_review_for_K_scale_tail_spiral | 4 | 2 | 43 | 3.12903 | 26.4984 | orientation_gate_blocked | resolve source-native orientation promotion before projection catalogue use |

## Claim Boundary

This queue is allowed to accelerate source acquisition.  It is not allowed
to promote a morphology/readout label, freeze a kernel, select an
amplitude, or claim empirical validation.
