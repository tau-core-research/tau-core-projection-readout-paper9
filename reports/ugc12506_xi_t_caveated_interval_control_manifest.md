# UGC12506 Xi_t Caveated Interval/Control Manifest

This artifact records a source-reviewed caveated interval/control manifest. It is not an endpoint and does not score the rotation curve.

## Control Manifest

| galaxy | manifest_status | manifest_kind | review_decision | formula_text | kernel_text | epsilon_rule | epsilon_t_nominal | epsilon_t_interval_min | epsilon_t_interval_max | epsilon_cap_protocol | xi_t_interval_min | xi_t_interval_max | xi_t_squared_fractional_shift_max | path_policy | asymmetry_policy | cap_policy | standard_endpoint_manifest_allowed | control_manifest_allowed | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY | caveated_interval_control | ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL | Xi_t(R)=1+epsilon_t K_t(R) | K_t=norm[w_spin K_spin + w_edge K_spin + w_env K_env + w_asym K_asym + 0*K_path] | epsilon_t=min(0.035, 0.035*Gamma_clock), Gamma_clock=L/(1+L) | 0.0238438 | 0 | 0.0238438 | 0.035 | 1 | 1.02384 | 0.0482562 | path term fixed to zero unless later source path review establishes it | asymmetry remains caveated phase component, not standalone route driver | epsilon_cap=0.035 is protocol cap only, not universal Tau Core constant | False | True | False | False | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |

## Component Policy

| galaxy | component_id | component_status | source_load | normalized_weight | kernel_column | source_basis | claim_boundary | control_policy | endpoint_scores_allowed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | T_HIGHSPIN_SETTLING | INCLUDED_SOURCE_SUPPORTED | 1 | 0.467884 | K_t_highspin_clock_spin | reported high-spin state lambda=0.15 | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_as_source_supported_core_component | False |
| UGC12506 | T_EDGEON_PV_CLOCK_SLICE | INCLUDED_SOURCE_SUPPORTED | 0.59708 | 0.279365 | K_t_highspin_clock_spin | high inclination and PV/envelope method required | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_with_projection_caveat | False |
| UGC12506 | T_ENVELOPE_SETTLING | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.457272 | 0.21395 | K_t_highspin_clock_envelope | large diffuse low-density H I support | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_as_caveated_interval_component | False |
| UGC12506 | T_ASYMMETRIC_PV_PHASE | INCLUDED_SOURCE_SUPPORTED_CAVEATED | 0.0829278 | 0.0388006 | K_t_highspin_clock_asymmetry | approaching/receding side shape and length asymmetry | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | carry_only_as_caveated_phase_component | False |
| UGC12506 | T_PATH_ENVIRONMENT | EXCLUDED_NOT_ESTABLISHED | 0 | 0 | K_t_path_environment | foreground/path object evidence is not established | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint | exclude_keep_zero_until_source_path_review | False |

## Review Policy

| galaxy | policy_id | policy_status | policy_text | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_XIT_CTRL_P1_REVIEW_ROUTE | PASS | ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL | False | False | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |
| UGC12506 | U12506_XIT_CTRL_P2_FORBIDDEN_INPUTS | PASS | forbidden_inputs_used=none | False | False | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |
| UGC12506 | U12506_XIT_CTRL_P3_ENDPOINT_BLOCK | PASS_RECORDED | endpoint scoring remains blocked after control manifest creation | False | False | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |
| UGC12506 | U12506_XIT_CTRL_P4_CAP_BOUNDARY | PASS_RECORDED | epsilon_cap is protocol cap only; deeper Tau-side origin remains open | False | False | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |

## Summary

| control_manifest_status | galaxy | manifest_kind | epsilon_t_interval | xi_t_interval | endpoint_scores_allowed | uses_vobs_or_residual | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_XI_T_CAVEATED_INTERVAL_CONTROL_MANIFEST_READY | UGC12506 | caveated_interval_control | [0, 0.0238438] | [1, 1.02384] | False | False | optional control replay protocol; standard endpoint still requires a separate endpoint permission gate | ugc12506_xi_t_caveated_interval_control_manifest_not_endpoint |

## Claim Boundary

The reviewer accepted the high-spin edge-on envelope route only as a caveated interval/control route. The path term remains zero, the asymmetry term remains caveated, and epsilon_cap remains a protocol cap rather than a universal Tau Core constant.
