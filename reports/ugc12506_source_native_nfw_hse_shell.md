# UGC12506 Source-Native NFW + High-Spin Envelope Shell

This shell replaces the earlier disk-scale NFW proxy with the published
Hallenbeck et al. Table 5 NFW concentration and R200.  It remains a
replay shell rather than endpoint validation.

## Summary

| formula_shell_status | galaxy | nfw_c | nfw_r200_kpc | rs_nfw_kpc | evidence_total | gamma_total | amplitude_total_km2_s2 | kernel_inner_mean_first8 | kernel_outer_mean_last8 | n_gates | n_blocked | n_caveated | formula_frozen_before_scoring | control_replay_scores_allowed | endpoint_validation_claim_allowed | construction_used_vobs_or_residual | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_NATIVE_NFW_HSE_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 14.87 | 123 | 8.27169 | 10.3594 | 0.911967 | 11548.5 | 0.729442 | 0.905661 | 5 | 0 | 0 | True | True | False | False | scripts/run_ugc12506_source_native_nfw_hse_replay.py | ugc12506_source_native_nfw_hse_shell_replay_not_validation |

## Manifest

| galaxy | formula_id | formula_text | kernel_text | nfw_v2_shape | amplitude_rule | gamma_rule | nfw_c | nfw_c_err | nfw_r200_kpc | nfw_r200_err_kpc | rs_nfw_kpc | chi2_nfw | chi2_iso | nfw_preference_load | envelope_load | edgeon_load | evidence_total | gamma_total | carrier_scale_outer_km2_s2 | amplitude_total_km2_s2 | dimension_check | known_limits | source_native_upgrade | formula_frozen_before_scoring | construction_used_vobs_or_residual | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | v_readout^2(R)=v_carrier^2(R)+A_source_native_nfw_hse K_source_native_nfw_hse(R) | K=norm[(1-W_outer)K_NFW_V2(R;c,R200)+W_outer max(K_NFW_V2,K_env)] | K_NFW_V2=norm({ln(1+cR/R200)-cR/R200/(1+cR/R200)} / {(R/R200)[ln(1+c)-c/(1+c)]}) | A=Gamma median_outer_R>=Ropt(v_carrier^2) | Gamma=E/(1+E), E=(chi2_iso/chi2_nfw-1)_+ + E_highspin_envelope + E_edgeon | 14.87 | 0.6 | 123 | 1.5 | 8.27169 | 0.21 | 0.54 | 1.57143 | 8.19084 | 0.59708 | 10.3594 | 0.911967 | 12663.3 | 11548.5 | PASS: A has km^2/s^2; K is dimensionless | K=0, Gamma=0, or absent NFW/envelope evidence recovers carrier; outer_window=0 leaves source-native NFW seed | replaces R_d proxy with Hallenbeck2014 Table 5 c,R200 | True | False | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | U12506_SNFW_G1_TABLE5_PARAMETERS | PASS | c=14.87±0.6, R200=123.0±1.5 kpc | uncertainty propagation later | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | U12506_SNFW_G2_NFW_PREFERENCE_LOAD | PASS | chi2_nfw=0.21, chi2_iso=0.54, load=1.57143 | independent reviewer can confirm table extraction | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | U12506_SNFW_G3_HIGHSPIN_ENVELOPE | PASS | lambda=0.15, RHI/Rd=7.85908 | none for replay | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | U12506_SNFW_G4_DIMENSIONS_LIMITS | PASS | velocity-squared amplitude times dimensionless kernel | none | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |
| UGC12506 | UGC12506_SOURCE_NATIVE_NFW_HSE | U12506_SNFW_G5_RESIDUAL_BLIND | PASS | kernel and amplitude use source tables and carrier only; no vobs/residual | vobs may enter only in scoring replay | False | ugc12506_source_native_nfw_hse_shell_replay_not_validation |

## Claim Boundary

The formula is frozen from source-native halo, H I envelope, inclination,
and carrier quantities. Observed rotation velocities may enter only in
the downstream replay scoring script.
