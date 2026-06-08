# UGC12506 Source-Native NFW-HSE Uncertainty Scan

This diagnostic varies only the published Table 5 NFW concentration and
R200 within their quoted one-sigma source uncertainties. It does not
retune labels, signs, kernels, or amplitudes from endpoint residuals.

## Summary

| scan_status | galaxy | n_variants | nominal_rmse_km_s | best_uncertainty_variant | best_uncertainty_rmse_km_s | best_minus_nominal_rmse_km_s | prior_best_diagnostic_model | prior_best_diagnostic_rmse_km_s | best_uncertainty_minus_prior_best_diagnostic_rmse_km_s | interpretation | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NATIVE_NFW_HSE_UNCERTAINTY_SCAN_COMPLETE_GAP_REMAINS | UGC12506 | 9 | 77.5409 | cm1_r200p1 | 77.517 | -0.0238897 | TAU_BEST_FAMILY | 37.3633 | 40.1537 | quoted c/R200 uncertainty cannot close the gap to prior diagnostic references | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |

## Variants

| galaxy | variant_id | nfw_c | nfw_r200_kpc | rs_nfw_kpc | rmse_km_s | mean_kernel | inner_kernel_mean_first8 | outer_kernel_mean_last8 | uses_only_source_uncertainty_box | construction_used_vobs_or_residual | scoring_used_vobs | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | cm1_r200p1 | 14.27 | 124.5 | 8.7246 | 77.517 | 0.891583 | 0.715306 | 0.914021 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | cm1_r2000 | 14.27 | 123 | 8.61948 | 77.5213 | 0.891436 | 0.718524 | 0.912128 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | cm1_r200m1 | 14.27 | 121.5 | 8.51437 | 77.5254 | 0.8913 | 0.721802 | 0.910225 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | c0_r200p1 | 14.87 | 124.5 | 8.37256 | 77.5305 | 0.891132 | 0.726322 | 0.907642 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | c0_r2000 | 14.87 | 123 | 8.27169 | 77.5409 | 0.890842 | 0.729442 | 0.905661 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | c0_r200m1 | 14.87 | 121.5 | 8.17081 | 77.5566 | 0.890414 | 0.732488 | 0.903565 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | cp1_r200p1 | 15.47 | 124.5 | 8.04783 | 77.5755 | 0.889903 | 0.736279 | 0.900996 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | cp1_r2000 | 15.47 | 123 | 7.95087 | 77.5903 | 0.889509 | 0.73933 | 0.898959 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |
| UGC12506 | cp1_r200m1 | 15.47 | 121.5 | 7.85391 | 77.605 | 0.889122 | 0.742437 | 0.896913 | True | False | True | False | ugc12506_source_native_nfw_hse_uncertainty_scan_diagnostic_not_endpoint |

![UGC12506 source-native NFW-HSE uncertainty scan](/Users/jolcsak/Projects/tau-core-morphology-forward-readout-paper8/figures/endpoint_diagnostics/ugc12506_source_native_nfw_hse_uncertainty_scan.png)
