# Distributed Vertical/Halo Beta Formula Freeze

This V2 formula is a source-side morphology refinement, not a residual fit.

`v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_DVH(R)]`

`K_DVH(R)=smoothstep((R-R_s)/(2R_s-R_s))`.

The earlier EVH kernel used a far-outer activation window. The source review
instead identifies distributed edge-on extraplanar dust/halo structure, so the
activation is moved to one-to-two disk scale lengths as a source rule.

## Summary

| formula_freeze_status | n_galaxies | n_gates | n_pass_gates | uses_vobs_or_residual_in_construction | control_replay_allowed | endpoint_scores_allowed | endpoint_validation_claim | next_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DISTRIBUTED_VERTICAL_HALO_BETA_FORMULA_FROZEN_CONTROL_REPLAY_ALLOWED | 2 | 8 | 8 | False | True | False | False | run_distributed_vertical_halo_control_replay | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |

## Manifest

| galaxy | formula_id | source_supported_lock_type | carrier_id | spin_route | beta_cl_value | formula_text | kernel_text | source_window_rule | source_reason | r_s_source_proxy_kpc | r_on_kpc | r_full_kpc | r_max_kpc | inclination_deg | thickness_h_over_rs_proxy | mean_bulge | max_bulge | amplitude_rule | dimension_check | inner_limit | outer_limit | zero_beta_limit | uses_vobs_or_residual_in_construction | formula_frozen_before_scoring | endpoint_scores_allowed | endpoint_validation_claim | source_provenance | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | NGC0891_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | K_edgeon_vertical_dust_hi_halo_mixed | BARYONIC_050_FAST_PACKET | BULLOCK_DISK_CONVERSION | 2.07946 | v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_DVH(R)] | K_DVH(R)=smoothstep((R-R_on)/(R_full-R_on)); R_on=R_s, R_full=min(2 R_s,R_max) | distributed edge-on extraplanar dust/halo layer activates over one-to-two disk scale lengths | NGC0891 and NGC4217 source ledgers show distributed extraplanar dust/halo structures, not only a far-outer warp | 5.52145 | 5.52145 | 11.0429 | 17.11 | 90 | 0.0949773 | 0.223557 | 0.861005 | beta_cl fixed by accepted Bullock disk conversion; no endpoint amplitude fit | PASS: beta_cl and K_DVH are dimensionless; correction multiplies v_carrier^2 | R <= R_on gives K_DVH=0 and recovers v_carrier | R >= R_full gives K_DVH=1 and recovers beta-transfer component | beta_cl=1 gives v_lock=v_carrier | False | True | False | False | available_data_proxy:r_median+r_max+type_bin+bulge_frac+gas_fraction+surface_brightness | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | K_edgeon_vertical_dust_radio_halo_mixed | BARYONIC_050_FAST_PACKET | BULLOCK_DISK_CONVERSION | 1.73333 | v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_DVH(R)] | K_DVH(R)=smoothstep((R-R_on)/(R_full-R_on)); R_on=R_s, R_full=min(2 R_s,R_max) | distributed edge-on extraplanar dust/halo layer activates over one-to-two disk scale lengths | NGC0891 and NGC4217 source ledgers show distributed extraplanar dust/halo structures, not only a far-outer warp | 5.19666 | 5.19666 | 10.3933 | 16.72 | 86 | 0.0933188 | 0.844349 | 0.98436 | beta_cl fixed by accepted Bullock disk conversion; no endpoint amplitude fit | PASS: beta_cl and K_DVH are dimensionless; correction multiplies v_carrier^2 | R <= R_on gives K_DVH=0 and recovers v_carrier | R >= R_full gives K_DVH=1 and recovers beta-transfer component | beta_cl=1 gives v_lock=v_carrier | False | True | False | False | available_data_proxy:r_median+r_max+type_bin+bulge_frac+gas_fraction+surface_brightness | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | NGC0891_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH1_LOCK_REVIEW | PASS | K_edgeon_vertical_dust_hi_halo_mixed | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH2_DISTRIBUTED_SOURCE_WINDOW | PASS | R_on=R_s=5.521 kpc; R_full=2R_s=11.043 kpc | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH3_BETA_COMPONENT_SOURCE_FIXED | PASS | beta_cl=2.07946 from BULLOCK_DISK_CONVERSION | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH4_DIMENSIONS_AND_LIMITS | PASS | dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1 | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH1_LOCK_REVIEW | PASS | K_edgeon_vertical_dust_radio_halo_mixed | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH2_DISTRIBUTED_SOURCE_WINDOW | PASS | R_on=R_s=5.197 kpc; R_full=2R_s=10.393 kpc | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH3_BETA_COMPONENT_SOURCE_FIXED | PASS | beta_cl=1.73333 from BULLOCK_DISK_CONVERSION | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_DISTRIBUTED_VERTICAL_HALO_BETA_V2 | DVH4_DIMENSIONS_AND_LIMITS | PASS | dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1 | False | False | beta_transfer_distributed_vertical_halo_formula_freeze_not_endpoint |
