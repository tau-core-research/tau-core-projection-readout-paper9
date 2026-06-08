# UGC12506 Beta-Closure Transfer Carrier Freeze Gate

This gate records that beta_cl is only an amplitude/closure factor until
a velocity-squared carrier is source-frozen. It does not score and does
not read observed rotation curves.

## Summary

| carrier_freeze_status | selected_carrier_id | n_carrier_routes | n_reviewable_not_accepted | n_control_only_routes | n_preferred_missing_routes | n_frozen_carrier_rows | carrier_manifest_ready_for_scoring | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_TRANSFER_CARRIER_FREEZE_READY_FOR_FORMULA_MANIFEST | BARYONIC_050_FAST_PACKET | 3 | 1 | 1 | 1 | 1 | True | False | False | False | False | build_beta_cl_transfer_formula_manifest | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |

## Carrier Routes

| carrier_id | route_status | carrier_expression | source_artifacts | scientific_role | limitation | review_obligation | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BARYONIC_050_FAST_PACKET | REVIEWABLE_NOT_ACCEPTED | v_carrier^2 = v_baryon_050^2 from fast SPARC packet | data/derived/fast_sparc_rotation_curve_packet_points.csv | endpoint-safe minimal stress carrier if independently accepted | not the same as the UGC12506 source-native NFW/HSE carrier | ACCEPT_AS_MINIMAL_TRANSFER_STRESS_CARRIER_OR_REJECT | False | False | False | False | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |
| LI2020_NFW_FIT_CARRIER | DIAGNOSTIC_OR_CONTROL_ONLY_NOT_ENDPOINT_SAFE | NFW halo-fit curve reconstructed from Li et al. parameters | data/external/literature/li2020_sparc_halo_catalog/table1_vizier.tsv | useful diagnostic control for NFW-preference transfer context | published halo parameters are rotation-curve fit products | KEEP_CONTROL_ONLY_UNLESS_ENDPOINT_LEAKAGE_POLICY_ACCEPTS | True | False | False | False | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |
| SOURCE_NATIVE_NFW_HSE_TRANSFER_CARRIER | PREFERRED_BUT_CURRENTLY_MISSING | source-native envelope/closure carrier analogous to UGC12506 NFW/HSE | missing independent source-native transfer carrier manifests | closest scientific continuation of the UGC12506 beta_cl derivation | requires per-galaxy residual-blind source-native carrier construction | ACQUIRE_OR_DERIVE_SOURCE_NATIVE_TRANSFER_CARRIER | False | False | False | False | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |

## Gates

| gate_id | gate_status | reason | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| BETA_CARRIER_1_ROUTE_ACCEPTED | PASS | U12506_BETA_CARRIER_REVIEW_ACCEPTED_PREFREEZE_ALLOWED | False | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |
| BETA_CARRIER_2_NO_ENDPOINT_LEAKAGE | PASS | accepted carrier is endpoint-blind BARYONIC_050_FAST_PACKET | False | ugc12506_beta_closure_transfer_carrier_freeze_gate_not_endpoint |

## Frozen Carrier Manifest

No carrier rows are frozen.

## Claim Boundary

A future scoring runner must read a carrier from the frozen manifest.
It may not choose the carrier from endpoint residuals.
