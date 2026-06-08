# Tau Projection Kernel Rotation Comparison

This report compares available simple Tau, observer/projection Tau,
morphology-history observer/projection Tau, and baseline rotation curves.
The current artifacts provide Newtonian, TPG/v6, and MOND curves. They do
not provide a separate explicit RMOND curve, so no RMOND line is drawn.

## Curve Definitions

| galaxy | simple_tau_definition | observer_projection_definition | morph_observer_projection_definition | rmond_curve_status | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| UGC12506 | source-envelope support | edge-on/envelope/asymmetry projection | source-native NFW/HSE + incremental projection-history | not_available_as_explicit_curve_in_current_artifacts | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | thick/flared Tau proxy | accepted projection endpoint | mixed exponential/projection readout | not_available_as_explicit_curve_in_current_artifacts | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | exponential-disk Tau proxy | warp/vertical-overlay endpoint | expdisk + WVO frozen protocol | not_available_as_explicit_curve_in_current_artifacts | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | exponential-disk Tau proxy | broad outer-warp window | source-sharpened vertical/outer-warp replay | not_available_as_explicit_curve_in_current_artifacts | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | thick/flared Tau proxy | not separately frozen in this artifact | warp-history accepted endpoint | not_available_as_explicit_curve_in_current_artifacts | tau_projection_kernel_rotation_comparison_not_population_validation |

## RMSE Scores

| galaxy | curve | rmse_km_s | n_points | claim_boundary |
| --- | --- | --- | --- | --- |
| NGC4013 | Tau morph-observer projection | 10.6148 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | Tau simple | 10.8802 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | Tau observer projection | 11.4505 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | TPG/v6 | 12.2739 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | MOND | 14.3342 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4013 | Newtonian | 65.6913 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | Tau morph-observer projection | 11.619 | 12 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | Newtonian | 25.3963 | 12 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | Tau simple | 38.4554 | 12 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | TPG/v6 | 38.9877 | 12 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC4088 | MOND | 42.1838 | 12 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | Tau observer projection | 15.4952 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | Tau morph-observer projection | 16.3725 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | TPG/v6 | 16.7855 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | Tau simple | 17.0253 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | MOND | 18.5954 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC5907 | Newtonian | 86.4837 | 19 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | Tau morph-observer projection | 22.1308 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | Tau observer projection | 22.2557 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | Tau simple | 23.473 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | TPG/v6 | 25.4851 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | MOND | 29.3117 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| NGC7331 | Newtonian | 59.3544 | 36 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | MOND | 38.1227 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | TPG/v6 | 40.6978 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | Tau morph-observer projection | 69.1788 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | Tau source-native NFW/HSE | 77.5409 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | Tau observer projection | 102.432 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | Tau simple | 102.479 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |
| UGC12506 | Newtonian | 116.023 | 31 | tau_projection_kernel_rotation_comparison_not_population_validation |

![Tau projection kernel comparison grid](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/tau_projection_kernel_rotation_comparison_grid.png)

## Claim Boundary

This is a visualization and already-existing artifact comparison. It is
not a new population validation and does not promote caveated replays to
accepted endpoints.
