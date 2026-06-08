# UGC12506 Beta-Closure Bullock-Like Spin Conversion Proxy Gate

This gate computes a source-side, Bullock-like disk-inferred spin proxy
for beta_cl transfer candidates. It is a conditional conversion proxy,
not a direct halo/envelope spin measurement and not replay permission.

## Formula

\[
j_{\rm disk}=2R_dV_{\rm flat},\quad
R_{200}=V_{200}/(10H_0),\quad
\lambda'_{\rm disk}={j_{\rm disk}\over \sqrt{2}R_{200}V_{200}}.
\]

The formula is dimensionless and residual-blind. Its open assumption is
whether the disk-inferred specific angular momentum can stand in for the
Tau-side halo/envelope closure-normalization slot.

## Summary

| bullock_conversion_proxy_status | n_targets_computed | ngc0891_lambda_bullock_disk_proxy | ngc7331_lambda_bullock_disk_proxy | accepted_as_beta_cl_lambda_spin | proxy_review_required | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BULLOCK_DISK_INFERRED_SPIN_PROXY_COMPUTED_REVIEW_REQUIRED | 11 | 0.0352494 | 0.0325439 | False | True | False | False | False | independent_review_choose_exposure_proxy_or_bullock_conversion_or_direct_spin_source | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint |

## Primary Comparison

| galaxy | conversion_proxy_status | Rdisk_kpc | Vflat_km_s | V200_NFW_flat_km_s | R200_NFW_flat_kpc | j_disk_kpc_km_s | lambda_bullock_disk_proxy | lambda_ref | nfw_preference_load | edgeon_load | beta_if_bullock_disk_proxy_used | accepted_as_beta_cl_lambda_spin | proxy_review_required | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary | lambda_spin_proxy_candidate | spin_envelope_exposure_proxy | transfer_proxy_class | exposure_minus_bullock_lambda |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | CONVERSION_PROXY_COMPUTED_REVIEW_REQUIRED | 2.55 | 216.1 | 127.04 | 174.027 | 1102.11 | 0.0352494 | 0.1 | 0.225434 | 1 | 2.07946 | False | True | False | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint | 0.149267 | 0.492671 | PRIMARY_PROXY_TRANSFER_REVIEW_TARGET | 0.114018 |
| NGC7331 | CONVERSION_PROXY_COMPUTED_REVIEW_REQUIRED | 5.02 | 239 | 195.09 | 267.247 | 2399.56 | 0.0325439 | 0.1 | 0.17284 | 0 | 1.05625 | False | True | False | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint | 0.135758 | 0.357578 | SECONDARY_PROXY_TRANSFER_REVIEW_TARGET | 0.103214 |

## Checks

| check_id | result | reason | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| BSP_BULLOCK_1_DIMENSIONLESS | PASS_FORMULA | j_disk and R200*V200 both have kpc km/s units | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint |
| BSP_BULLOCK_2_RESIDUAL_BLIND | PASS_SOURCE_SIDE | uses SPARC source fields plus Li2020 NFW V200; no vobs residual or endpoint score | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint |
| BSP_BULLOCK_3_ASSUMPTION_DEPENDENCE | REVIEW_REQUIRED | requires disk specific angular momentum to trace the relevant halo/envelope closure-normalization slot | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint |
| BSP_BULLOCK_4_REPLAY_PERMISSION | BLOCKED | conversion proxy is not accepted as beta_cl lambda_spin without independent review | False | ugc12506_beta_closure_bullock_spin_conversion_proxy_gate_not_endpoint |

## Claim Boundary

The gate produces a more standard spin-proxy candidate than the exposure
load proxy, but it does not promote either candidate. An independent
review must choose or reject the conversion before any beta_cl preflight
or replay.
