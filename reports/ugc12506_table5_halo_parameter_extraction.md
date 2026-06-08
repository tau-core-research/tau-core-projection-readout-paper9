# UGC12506 Table 5 Halo Parameter Extraction

This source-native extraction replaces the earlier `R_d` NFW-scale proxy
with the published Table 5 NFW concentration and R200 values.

## Summary

| extraction_status | galaxy | nfw_c | nfw_c_err | nfw_r200_kpc | nfw_r200_err_kpc | chi2_nfw | chi2_iso | lambda_spin | nfw_preferred_over_iso | source_native_nfw_kernel_allowed | endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_TABLE5_HALO_PARAMETERS_EXTRACTED_SOURCE_NATIVE_REPLAY_READY | UGC12506 | 14.87 | 0.6 | 123 | 1.5 | 0.21 | 0.54 | 0.15 | True | True | False | build_ugc12506_source_native_nfw_hse_shell | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |

## Extracted Rows

| galaxy | nfw_c | nfw_c_err | nfw_r200_kpc | nfw_r200_err_kpc | chi2_nfw | iso_rho_c_1e_minus3_msun_pc3 | iso_rho_c_err | iso_rc_kpc | iso_rc_err_kpc | chi2_iso | lambda_spin | source_id | source_table | text_line_range | residual_blind_source_extraction | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC9037 | 2.67 | 0.5 | 121 | 12 | 1.29 | 18 | 2 | 5.16 | 0.4 | 0.65 | 0.07 | UGC12506_HI_SRC1_HIGHMASS_VLA | Hallenbeck2014 Table 5 | 1268-1330 | True | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |
| UGC12506 | 14.87 | 0.6 | 123 | 1.5 | 0.21 | 1150 | 360 | 0.91 | 0.15 | 0.54 | 0.15 | UGC12506_HI_SRC1_HIGHMASS_VLA | Hallenbeck2014 Table 5 | 1268-1330 | True | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |

## Gates

| gate_id | gate_status | evidence | remaining_obligation | galaxy | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| U12506_T5_G1_TABLE_PRESENT | PASS | Table 5 dark matter halo properties extracted from local source text | manual independent review recommended before accepted endpoint use | UGC12506 | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |
| U12506_T5_G2_NFW_PREFERENCE_NUMERIC | PASS | chi2_nfw=0.21, chi2_iso=0.54 | none for replay | UGC12506 | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |
| U12506_T5_G3_SOURCE_NATIVE_C_R200 | PASS | c=14.87±0.6, R200=123.0±1.5 kpc | propagate uncertainty later | UGC12506 | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |
| U12506_T5_G4_NO_RESIDUAL_USE | PASS | extraction uses published source table only | vobs enters only downstream scoring | UGC12506 | False | ugc12506_table5_halo_parameter_extraction_source_native_not_endpoint |

## Claim Boundary

The extraction is source-native and residual-blind. It is suitable for a
replay shell, not by itself an accepted endpoint validation.
