# UGC12506 Projection/High-Spin Formula Preflight

`UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED`

This is a fast source-side formula preflight.  It freezes source-native
observables and builds dimensionless context prekernels, but it does not
freeze a nonzero executable formula and does not score an endpoint.

## Summary

| preflight_status | galaxy | source_context_cached | rotation_packet_ready | source_observables_frozen | context_prekernel_built | rhi_source_kpc | rhi_sparc_kpc | source_rhi_consistency_fraction | projection_exposure_sin2_i | extent_asymmetry | lambda_spin_source | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual_in_preflight | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_PROJECTION_HIGHS_PIN_FORMULA_PREFLIGHT_READY_AMPLITUDE_BLOCKED | UGC12506 | True | True | True | True | 58 | 59.01 | 0.0174138 | 0.995134 | 0.166667 | 0.15 | False | False | False | derive_ugc12506_source_normalized_highspin_amplitude_or_freeze_control_branches | ugc12506_projection_highspin_formula_preflight_not_endpoint |

## Source-Frozen Observables

| galaxy | observable_id | symbol | value | uncertainty | unit | source | role | freeze_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_OBS_1_INCLINATION | i | 86 | 4 | deg | SPARC_Lelli2016c | projection exposure P_i=sin^2(i) | SOURCE_FROZEN | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_2_RDISK | R_d | 7.38 | nan | kpc | SPARC_Lelli2016c | inner disk support scale | SOURCE_FROZEN | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_3_RHI_SPARC | R_HI_SPARC | 59.01 | nan | kpc | SPARC_Lelli2016c | SPARC H I support scale | SOURCE_FROZEN | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_4_RHI_SOURCE | R_HI_source | 58 | 2 | kpc | Hallenbeck2014_HIghMass | source-native H I support scale | SOURCE_FROZEN | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_5_ROPT_SOURCE | R_opt | 40 | nan | kpc | Hallenbeck2014_HIghMass | optical support scale | SOURCE_FROZEN_CONTEXT | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_6_EXTENT_ASYMMETRY | A_extent | 0.166667 | nan | dimensionless | Hallenbeck2014_HIghMass | approaching/receding H I extent asymmetry context | SOURCE_DERIVED_CONTEXT | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_7_SPIN | lambda_spin | 0.15 | nan | dimensionless | Hallenbeck2014_HIghMass | high-spin/history context | SOURCE_FROZEN_CONTEXT | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_OBS_8_HI_SURFACE_DENSITY_RANGE | Sigma_HI_range | 5 | 4 | Msun pc^-2 | Hallenbeck2014_HIghMass | low-density stable H I closure context | SOURCE_FROZEN_CONTEXT | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |

## Formula Shells

| galaxy | formula_id | formula_role | formula_text | kernel_text | sign_status | amplitude_status | dimension_check | known_limits | uses_vobs_or_residual_in_derivation | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_PROJECTION_HIGHS_PIN_OUTER_SUPPORT_SHELL | preferred preflight shell | v_readout^2(R)=v_carrier^2(R)+A_hs K_hs(R) | K_hs(R)=sin^2(i) W_outer(R;R_d,R_HI) H_spin(lambda) C_stableHI | FORMULA_CONDITIONAL_NOT_ENDPOINT_SELECTED | BLOCKED_NO_SOURCE_NORMALIZED_A_hs | PASS if A_hs has km^2/s^2 and K_hs is dimensionless | i=0 or W_outer=0 or A_hs=0 recovers carrier | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PROJECTION_ASYMMETRY_CONTEXT_SHELL | secondary preflight shell | v_readout^2(R)=v_carrier^2(R)+A_pa K_pa(R) | K_pa(R)=sin^2(i) W_outer(R;R_d,R_HI) A_extent | FORMULA_CONDITIONAL_NOT_ENDPOINT_SELECTED | BLOCKED_NO_SOURCE_NORMALIZED_A_pa | PASS if A_pa has km^2/s^2 and K_pa is dimensionless | zero asymmetry or zero amplitude recovers carrier | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | remaining_obligation | uses_vobs_or_residual | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_PHF_G1_SOURCE_CONTEXT | PASS_SOURCE_CONTEXT_CACHED | UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN | none for context cache | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G2_ROTATION_PACKET | PASS_ROTATION_PACKET_READY | n=31 points; fast priority rank=1 | do not use residual gap for label or amplitude | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G3_SOURCE_OBSERVABLES | PASS_PARTIAL_SOURCE_OBSERVABLES_FROZEN | inclination, R_d, R_HI, R_opt, extent asymmetry, spin context, H I density context | extract or derive normalized active loads | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G4_PREKERNEL | PASS_CONTEXT_PREKERNEL_BUILT | dimensionless K_pre and context kernels are built on SPARC radial grid | not executable until amplitude/load rule is frozen | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G5_AMPLITUDE | BLOCKED_NO_SOURCE_NORMALIZED_AMPLITUDE | A_hs and A_pa are not source-normalized | derive amplitude from source/Tau-side scale, not from observed residual | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G6_SIGN | BLOCKED_SIGN_NOT_ENDPOINT_SELECTED | source suggests projection/high-spin context but not a final sign convention | derive sign from readout theorem or freeze both branches as controls | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |
| UGC12506 | UGC12506_PHF_G7_ENDPOINT | BLOCKED_ENDPOINT_NOT_ALLOWED | formula is preflight only; no endpoint scoring here | freeze amplitude/sign/label before endpoint | False | False | False | ugc12506_projection_highspin_formula_preflight_not_endpoint |

## Evidence Used

| galaxy | evidence_id | evidence_type | paraphrased_evidence |
| --- | --- | --- | --- |
| UGC12506 | UGC12506_HM_E1_HIGH_INCLINATION_PV_REQUIRED | projection_context | The galaxy is highly inclined, so velocity-field curves underestimate rotation and the authors use a position-velocity/envelope method. |
| UGC12506 | UGC12506_HM_E2_EXTENDED_HI_SUPPORT | hi_extent_context | The H I disk is traced beyond 60 kpc and the observed H I radius is reported as 58 +/- 2 kpc, consistent with the expected radius. |
| UGC12506 | UGC12506_HM_E3_ORDERED_BUT_ASYMMETRIC_PV | projection_asymmetry_context | The galaxy shows ordered rotation to the detectable edge, but the approaching and receding sides differ in shape and length. |
| UGC12506 | UGC12506_HM_E4_LOW_DENSITY_STABLE_HI | closure_stability_context | UGC12506 has low H I surface densities, typically 1-5 Msun/pc^2 out to 60 kpc, and is described as stable over most of the disk. |
| UGC12506 | UGC12506_HM_E5_HIGH_SPIN_CONTEXT | history_memory_context | The paper reports a very high spin parameter for UGC12506, interpreted as an unusual gas-rich high-spin state. |

## Claim Boundary

The prekernel uses no endpoint residuals and no fitted amplitude.  The
observed rotation curve is present in the grid only for provenance and
future scoring.  The active UGC12506 endpoint remains blocked until a
source-normalized amplitude/sign rule and label gate are frozen.
