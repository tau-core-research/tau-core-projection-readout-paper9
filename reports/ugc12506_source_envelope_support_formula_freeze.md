# UGC12506 Source-Envelope Support Formula Freeze

This freeze promotes the extended H I envelope from a small context
multiplier into the principal source-support component. It remains
residual-blind and does not claim endpoint validation.

## Summary

| formula_freeze_status | galaxy | envelope_evidence | envelope_gamma | envelope_amplitude_km2_s2 | kernel_max | kernel_outer_mean_last8 | n_gates | n_blocked | n_caveated | formula_frozen_before_scoring | control_replay_scores_allowed | endpoint_validation_claim_allowed | construction_used_vobs_or_residual | next_script | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_SOURCE_ENVELOPE_SUPPORT_FORMULA_FROZEN_REPLAY_ALLOWED_NOT_VALIDATION | UGC12506 | 8.19084 | 0.891196 | 11285.5 | 1 | 0.812509 | 4 | 0 | 1 | True | True | False | False | scripts/run_ugc12506_source_envelope_support_replay_controls.py | ugc12506_source_envelope_support_formula_freeze_not_validation |

## Manifest

| galaxy | formula_id | formula_text | kernel_text | amplitude_rule | gamma_rule | inclination_deg | rd_kpc | rhi_source_kpc | ropt_kpc | lambda_spin | sigma_hi_min_msun_pc2 | sin2_i | extent_ratio_rhi_over_rd | hi_extension_load | spin_load | low_density_stability_load | envelope_evidence | envelope_gamma | carrier_scale_outer_km2_s2 | envelope_amplitude_km2_s2 | dimension_check | known_limits | formula_frozen_before_scoring | construction_used_vobs_or_residual | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT | v_readout^2(R)=v_carrier^2(R)+A_env K_env(R) | K_env=norm[sin^2(i) W(R;R_d,R_HI) sqrt((R-R_d)/(R_HI-R_d))] | A_env=Gamma_env median_outer_R>=Ropt(v_carrier^2) | Gamma_env=E_env/(1+E_env), E_env=sin^2(i)(R_HI/R_d-1)(lambda_spin/0.10)C_lowSigmaHI | 86 | 7.38 | 58 | 40 | 0.15 | 1 | 0.995134 | 7.85908 | 6.85908 | 1.5 | 0.8 | 8.19084 | 0.891196 | 12663.3 | 11285.5 | PASS: A_env has km^2/s^2 and K_env is dimensionless | i=0, R_HI/R_d->1, lambda_spin->0, or K_env=0 recovers carrier | True | False | False | ugc12506_source_envelope_support_formula_freeze_not_validation |

## Gates

| galaxy | formula_id | gate_id | gate_status | evidence | remaining_obligation | endpoint_validation_claim_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT | U12506_ENV1_SOURCE_OBSERVABLES_PRESENT | PASS | i, R_d, R_HI_source, R_opt, lambda_spin, Sigma_HI_range available | none for formula replay | False | ugc12506_source_envelope_support_formula_freeze_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT | U12506_ENV2_RESIDUAL_BLIND_FREEZE | PASS | construction_used_vobs_or_residual=False | vobs may enter only in separate scoring script | False | ugc12506_source_envelope_support_formula_freeze_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT | U12506_ENV3_DIMENSIONS_AND_LIMITS | PASS | A_env velocity-squared; K_env dimensionless; carrier recovery limits explicit | none | False | ugc12506_source_envelope_support_formula_freeze_not_validation |
| UGC12506 | UGC12506_SOURCE_ENVELOPE_SUPPORT_POSITIVE_READOUT | U12506_ENV4_SOURCE_PROMOTION_CAVEAT | PASS_CAVEATED | extended H I envelope is promoted from context multiplier to support component | requires independent source-side review before accepted endpoint validation | False | ugc12506_source_envelope_support_formula_freeze_not_validation |

## Claim Boundary

The formula is stronger than the earlier high-spin context branch, but
the promotion of the H I envelope into the main support term must be
reviewed as a source-side theorem/caveat before accepted endpoint use.
