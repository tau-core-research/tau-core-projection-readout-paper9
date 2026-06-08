# Edge-on Vertical/Halo Gated Beta Formula Freeze

The pure beta-transfer branch is source-rejected as the primary lock for NGC0891 and NGC4217.
This formula keeps beta as an accepted component but gates it by an outer vertical/halo source window.

## Formula

`v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_EVH(R)]`

`K_EVH(R)=smoothstep((R-R_on)/(R_full-R_on))`, with `R_on=2R_s` and `R_full=min(3R_s,R_max)`.

## Summary

| formula_freeze_status | n_galaxies | n_gates | n_pass_gates | uses_vobs_or_residual_in_construction | control_replay_allowed | endpoint_scores_allowed | endpoint_validation_claim | next_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EDGEON_VERTICAL_HALO_GATED_BETA_FORMULA_FROZEN_CONTROL_REPLAY_ALLOWED | 2 | 8 | 8 | False | True | False | False | run_control_replay_scoring_script | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |

## Manifest

| galaxy | formula_id | source_supported_lock_type | carrier_id | spin_route | beta_cl_value | formula_text | kernel_text | source_window_rule | r_s_source_proxy_kpc | r_on_kpc | r_full_kpc | r_max_kpc | inclination_deg | thickness_h_over_rs_proxy | mean_bulge | max_bulge | amplitude_rule | dimension_check | inner_limit | outer_limit | zero_beta_limit | uses_vobs_or_residual_in_construction | formula_frozen_before_scoring | endpoint_scores_allowed | endpoint_validation_claim | source_provenance | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | NGC0891_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | K_edgeon_vertical_dust_hi_halo_mixed | BARYONIC_050_FAST_PACKET | BULLOCK_DISK_CONVERSION | 2.07946 | v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_EVH(R)] | K_EVH(R)=smoothstep((R-R_on)/(R_full-R_on)); R_on=2 R_s, R_full=min(3 R_s,R_max) | outer vertical/halo component activates after two disk scale lengths | 5.52145 | 11.0429 | 16.5644 | 17.11 | 90 | 0.0949773 | 0.223557 | 0.861005 | beta_cl fixed by accepted Bullock disk conversion; no endpoint amplitude fit | PASS: beta_cl and K_EVH are dimensionless; correction multiplies v_carrier^2 | R <= R_on gives K_EVH=0 and recovers v_carrier | R >= R_full gives K_EVH=1 and recovers beta-transfer component | beta_cl=1 gives v_lock=v_carrier | False | True | False | False | available_data_proxy:r_median+r_max+type_bin+bulge_frac+gas_fraction+surface_brightness | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | K_edgeon_vertical_dust_radio_halo_mixed | BARYONIC_050_FAST_PACKET | BULLOCK_DISK_CONVERSION | 1.73333 | v_lock^2(R)=v_carrier^2(R)*[1+(beta_cl-1)*K_EVH(R)] | K_EVH(R)=smoothstep((R-R_on)/(R_full-R_on)); R_on=2 R_s, R_full=min(3 R_s,R_max) | outer vertical/halo component activates after two disk scale lengths | 5.19666 | 10.3933 | 15.59 | 16.72 | 86 | 0.0933188 | 0.844349 | 0.98436 | beta_cl fixed by accepted Bullock disk conversion; no endpoint amplitude fit | PASS: beta_cl and K_EVH are dimensionless; correction multiplies v_carrier^2 | R <= R_on gives K_EVH=0 and recovers v_carrier | R >= R_full gives K_EVH=1 and recovers beta-transfer component | beta_cl=1 gives v_lock=v_carrier | False | True | False | False | available_data_proxy:r_median+r_max+type_bin+bulge_frac+gas_fraction+surface_brightness | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | NGC0891_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH1_LOCK_REVIEW | PASS | K_edgeon_vertical_dust_hi_halo_mixed | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH1_LOCK_REVIEW | PASS | K_edgeon_vertical_dust_radio_halo_mixed | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH2_SOURCE_WINDOW | PASS | R_on=2R_s=11.043 kpc; R_full=16.564 kpc | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH2_SOURCE_WINDOW | PASS | R_on=2R_s=10.393 kpc; R_full=15.590 kpc | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH3_BETA_COMPONENT_SOURCE_FIXED | PASS | beta_cl=2.07946 from BULLOCK_DISK_CONVERSION | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH3_BETA_COMPONENT_SOURCE_FIXED | PASS | beta_cl=1.73333 from BULLOCK_DISK_CONVERSION | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC0891 | NGC0891_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH4_DIMENSIONS_AND_LIMITS | PASS | dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1 | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
| NGC4217 | NGC4217_EDGEON_VERTICAL_HALO_GATED_BETA_V1 | EVH4_DIMENSIONS_AND_LIMITS | PASS | dimensionless kernel and beta; carrier recovery at K=0 or beta_cl=1 | False | False | beta_transfer_edgeon_vertical_halo_formula_freeze_not_endpoint |
