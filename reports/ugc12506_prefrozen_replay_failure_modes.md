# UGC12506 Prefrozen Replay Failure-Mode Audit

This diagnostic reads `vobs` and therefore cannot freeze a new formula.
It is used only to decide what residual-blind source evidence would be
needed before a new endpoint attempt.

## Zone Summary

| galaxy | outer_radius_threshold_kpc | outer_mean_observed_minus_baryonic_km_s | outer_mean_prefrozen_lift_km_s | outer_mean_required_delta_v2_km2_s2 | outer_mean_prefrozen_delta_v2_km2_s2 | outer_delta_v2_fraction | best_prefrozen_rmse_km_s | best_prior_diagnostic_model | best_prior_diagnostic_rmse_km_s | diagnostic_scaled_shape_rmse_km_s | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | 35.24 | 119.426 | 14.311 | 41416.3 | 3458.12 | 0.0834965 | 109.372 | PRIOR_DIAGNOSTIC_TAU_BEST_FAMILY | 37.3633 | 70.9922 | ugc12506_prefrozen_replay_failure_modes_diagnostic_only |

## Diagnostics

| diagnostic | status | value | claim_type |
| --- | --- | --- | --- |
| direction | CORRECT_SIGN_WEAK_MAGNITUDE | UGC12506_COMBINED_HIGHS_PIN_ASYMMETRY_POSITIVE_PREFROZEN | diagnostic_only |
| shape_correlation_v2 | KERNEL_SHAPE_MISALIGNED | -0.0877996341840898 | diagnostic_only |
| required_multiplier_on_prefrozen_delta_v2 | PREFROZEN_AMPLITUDE_UNDERPOWERED | 14.53099799932998 | diagnostic_only |
| outer_lift_fraction | OUTER_LIFT_TOO_SMALL | 0.11983198302988467 | diagnostic_only |
| prior_best_gap | PREFROZEN_REPLAY_NOT_BASELINE_COMPETITIVE | 72.00830916017448 | diagnostic_only |

## Diagnostic Scaled Shape

| galaxy | model_id | rmse_km_s | scale_multiplier | uses_vobs_for_scale | endpoint_validation_claim | claim_boundary | interpretation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | DIAGNOSTIC_ONLY_SCALED_PREFROZEN_SHAPE | 70.9922 | 14.531 | True | False | ugc12506_prefrozen_replay_failure_modes_diagnostic_only | If this is much better than the frozen replay, the kernel shape has information but the source-normalized amplitude rule is too weak. This is not an endpoint result. |

## Interpretation

The positive prefrozen branch has the expected direction but the
source-normalized amplitude is too small for the observed outer gap.
The scaled-shape row is not an endpoint result; it only shows whether
the current kernel shape could become competitive if a stronger
residual-blind amplitude theorem or source-native normalization were
derived.

![UGC12506 diagnostic](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_prefrozen_branch_replay_failure_modes.png)
