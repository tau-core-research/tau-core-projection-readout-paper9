# UGC12506 Beta-Closure Transfer Formula Freeze Gate

This gate creates the frozen transfer formula manifest consumed by the
separate scoring runner. In the current state it writes only an empty
manifest with headers because the spin-route prefreeze is still blocked.

## Summary

| formula_freeze_status | selected_spin_normalization_route | n_formula_manifest_rows | n_pass_gates | n_blocked_gates | formula_manifest_written | formula_manifest_ready_for_scoring | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_READY_FOR_SCORING_RUNNER | BULLOCK_DISK_CONVERSION | 11 | 5 | 0 | True | True | False | False | False | False | run_ugc12506_beta_closure_transfer_scoring | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |

## Gates

| gate_id | gate_status | reason | formula_manifest_rows_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- |
| BETA_FORMULA_1_SPIN_ROUTE_PREFREEZE_READY | PASS | U12506_BETA_SPIN_ROUTE_PREFREEZE_READY_REPLAY_STILL_SEPARATE | True | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| BETA_FORMULA_2_PREFREEZE_VALUES_EXIST | PASS | n_prefreeze_values=11 | True | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| BETA_FORMULA_3_HALO_FIELDS_READY | PASS | n_halo_field_rows=11 | True | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| BETA_FORMULA_4_PRIORITY_FIELDS_READY | PASS | n_priority_rows=11 | True | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| BETA_FORMULA_5_CARRIER_MANIFEST_READY | PASS | carrier_status=U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST; n_carriers=1 | True | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |

## Formula Manifest

| galaxy | formula_id | carrier_id | carrier_expression | selected_spin_normalization_route | lambda_spin_value | nfw_preference_load | edgeon_load | beta_cl_formula | beta_cl_value | source_value_artifacts | formula_freeze_status | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ESO563-G021 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.00716317 | 0 | 0.533333 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.53333 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| IC4202 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0678522 | 0 | 1 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 2 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC0801 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0291447 | 0.0443131 | 0.333333 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.34625 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC0891 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0352494 | 0.225434 | 1 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 2.07946 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC2841 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0202436 | 0.0675676 | 0.0666667 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.08034 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC3521 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.00267756 | 0 | 0 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC4013 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.00631325 | 0.037037 | 0.933333 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.93567 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC4157 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.00563934 | 0 | 0.466667 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.46667 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC4217 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0231037 | 0 | 0.733333 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.73333 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| NGC7331 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.0325439 | 0.17284 | 0 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 1.05625 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |
| UGC11455 | BETA_CL_TRANSFER_SOURCE_FROZEN | BARYONIC_050_FAST_PACKET | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | BULLOCK_DISK_CONVERSION | 0.00660234 | 0 | 1 | 1 + (lambda_spin/lambda_ref)*nfw_preference_load + edgeon_load; lambda_ref=0.10 | 2 | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | SOURCE_FROZEN_FORMULA_READY_FOR_SEPARATE_SCORING | False | False | False | False | ugc12506_beta_closure_transfer_formula_freeze_gate_not_endpoint |

## Claim Boundary

This gate does not read observed rotation curves and does not score. It
only freezes the formula inputs that a later scoring runner may consume.
