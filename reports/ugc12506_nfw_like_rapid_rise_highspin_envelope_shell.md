# UGC12506 NFW-like Rapid-Rise + High-Spin Envelope Shell

This shell follows the source-route audit and keeps the prior
`K_compact_finite` result diagnostic-only. It uses source evidence for
NFW preference, rapid rise, high spin, and extended H I envelope.

## Summary

| formula_shell_status | galaxy | rs_nfw_proxy_kpc | evidence_total | gamma_total | amplitude_total_km2_s2 | kernel_inner_mean_first8 | kernel_outer_mean_last8 | n_gates | n_blocked | n_caveated | formula_frozen_before_scoring | control_replay_scores_allowed | endpoint_validation_claim_allowed | construction_used_vobs_or_residual | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_NFW_HSE_FORMULA_SHELL_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 7.38 | 9.78792 | 0.907304 | 11489.5 | 0.757783 | 0.887328 | 5 | 0 | 1 | True | True | False | False | scripts/run_ugc12506_nfw_like_rapid_rise_highspin_envelope_replay.py | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |

## Manifest

| galaxy | formula_id | formula_text | kernel_text | amplitude_rule | gamma_rule | rs_nfw_proxy_kpc | nfw_preference_load | envelope_load | edgeon_load | evidence_total | gamma_total | carrier_scale_outer_km2_s2 | amplitude_total_km2_s2 | dimension_check | known_limits | compact_finite_policy | formula_frozen_before_scoring | construction_used_vobs_or_residual | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | v_readout^2(R)=v_carrier^2(R)+A_nfw_hse K_nfw_hse(R) | K_nfw_hse=norm[(1-W_outer)K_NFWlike(R;R_d)+W_outer max(K_NFWlike,K_env)] | A_nfw_hse=Gamma_nfw_hse median_outer_R>=Ropt(v_carrier^2) | Gamma=E/(1+E), E=1_NFW_preference + E_highspin_envelope + E_edgeon | 7.38 | 1 | 8.19084 | 0.59708 | 9.78792 | 0.907304 | 12663.3 | 11489.5 | PASS: A has km^2/s^2 and K is dimensionless | no NFW preference, no high-spin envelope, or K=0 recovers carrier; outer_window=0 leaves rapid-rise seed | prior K_compact_finite remains diagnostic only | True | False | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | U12506_NHSE_G1_ROUTE_AUDIT | PASS | UGC12506_PRIOR_BEST_AUDIT_COMPLETE_NFW_RAPID_RISE_ROUTE_OPENED | none for formula replay | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | U12506_NHSE_G2_COMPACT_NOT_PROMOTED | PASS | prior K_compact_finite diagnostic is not used as source label | none | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | U12506_NHSE_G3_NFW_RAPID_RISE_SEED | PASS_CAVEATED | NFW preference and rapid rise source statements; R_d used as concentration proxy | source-native NFW parameters would strengthen this route | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | U12506_NHSE_G4_DIMENSIONS_LIMITS | PASS | A velocity-squared; K dimensionless; carrier recovery stated | none | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |
| UGC12506 | UGC12506_NFW_LIKE_RAPID_RISE_HIGHS_PIN_ENVELOPE | U12506_NHSE_G5_RESIDUAL_BLIND | PASS | construction_used_vobs_or_residual=False | vobs may enter only in replay scoring script | False | ugc12506_nfw_like_rapid_rise_highspin_envelope_shell_not_validation |
