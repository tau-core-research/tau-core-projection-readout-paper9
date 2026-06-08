# UGC12506 Beta-Closure Spin Proxy Review Bundle

This bundle prepares an independent, residual-blind review of the
source-declared beta_cl spin/envelope exposure proxy. It is not a
review response, not a replay manifest, and not an endpoint.

## Summary

| review_bundle_status | review_packet_id | bundle_dir | bundle_zip | n_files_listed | n_missing_inputs | missing_inputs | review_response_received | proxy_promotion_allowed | beta_cl_replay_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_SPIN_PROXY_REVIEW_BUNDLE_READY_RESPONSE_PENDING | U12506_BETA_SPIN_PROXY_REVIEW_PACKET_V1 | review_bundles/ugc12506_beta_closure_spin_proxy | review_bundles/ugc12506_beta_closure_spin_proxy_review_bundle.zip | 26 | 0 | none | False | False | False | False | False | intake_independent_spin_proxy_review_response | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |

## Review Packet

| review_packet_id | packet_status | review_subject | proxy_formula | bullock_like_conversion_formula | lambda_ref | primary_review_target | secondary_review_targets | direct_lambda_status | definition_conversion_status | endpoint_scores_allowed | beta_cl_replay_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_SPIN_PROXY_REVIEW_PACKET_V1 | READY_FOR_INDEPENDENT_REVIEW_RESPONSE | source-only beta_cl spin/envelope normalization route | lambda_spin_proxy=lambda_ref*(1 + 0.35*extent_load + 0.25*velocity_load + 0.25*gas_load + 0.15*edgeon_load) | lambda'_disk=(2*Rdisk*Vflat)/(sqrt(2)*R200*V200); R200=V200/(10*H0) | 0.1 | NGC0891 | NGC7331;NGC2841;NGC0801;NGC4013 | no_beta_cl_direct_lambda_accepted | ngc7331_disc_lambda_context_only | False | False | False | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |

## Review Obligations

| obligation_id | review_question | required_decision | allowed_evidence | forbidden_inputs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| BSP_REV_1_SOURCE_FIELDS | Are RHI/Rdisk, Vflat, H I mass, and inclination acceptable source-side observables for a spin/envelope exposure proxy? | ACCEPT_FIELDS_OR_REJECT_PROXY | SPARC source fields; source-native H I/kinematic context; literature spin/envelope context | rotation residuals; endpoint RMSE; baseline ranks | False | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_REV_2_WEIGHT_RULE | Is the predeclared exposure load-weight rule defensible as a protocol candidate, should the Bullock-like disk-conversion proxy be preferred, or must both be replaced before replay? | ACCEPT_EXPOSURE_RULE_OR_BULLOCK_RULE_OR_REQUIRE_NEW_RULE | source-side dimensional and monotonicity audit; Bullock-like disk-inferred conversion report | best-fit beta; endpoint score; wrong-family rank | False | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_REV_3_DEFINITION_BOUNDARY | Does the reviewer agree that Marr (2015) NGC7331 disc lambda is context only and cannot directly fill beta_cl lambda_spin? | ACCEPT_CONTEXT_ONLY_OR_SUPPLY_CONVERSION | definition comparison; source-side conversion theorem | choosing the larger lambda because it improves a curve | False | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_REV_4_TRANSFER_SCOPE | Which targets, if any, may carry the proxy as a caveated transfer-review input? | ACCEPT_TARGET_SET_OR_RESTRICT_TARGET_SET | proxy transfer queue and source evidence only | post-score target promotion | False | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |

## Forbidden Inputs

| forbidden_input_id | forbidden_input | reason | claim_boundary |
| --- | --- | --- | --- |
| BSP_FORBID_1_ROTATION_RESIDUALS | v_obs residuals or residual-zone plots | would turn the proxy into residual rescue | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_FORBID_2_ENDPOINT_SCORES | endpoint RMSE, beat fractions, or rank after scoring | proxy promotion must precede any replay | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_FORBID_3_BASELINE_RANKS | Newton/MOND/RAR/RMOND/TPG baseline comparison ranks | baseline weakness can motivate audit but not define the proxy | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| BSP_FORBID_4_DISC_DIRECT_INSERTION | direct insertion of disc lambda into halo/envelope slot | definition conversion gate rejected direct substitution | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |

## Bundle Manifest

| bundle_relative_path | source_repo_path | exists | sha256 | claim_boundary |
| --- | --- | --- | --- | --- |
| reports/ugc12506_beta_closure_source_declared_spin_proxy_gate.md | reports/ugc12506_beta_closure_source_declared_spin_proxy_gate.md | True | 7a12e16df9752817d565c2d8d14a2aabf898ec31207e03a87339111bec2dff75 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| reports/ugc12506_beta_closure_direct_lambda_spin_source_gate.md | reports/ugc12506_beta_closure_direct_lambda_spin_source_gate.md | True | e41dd635d6b151e6ce8be8fc18e1b584e65861d62a87d96522e1085cd4384e87 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| reports/ugc12506_beta_closure_lambda_definition_conversion_gate.md | reports/ugc12506_beta_closure_lambda_definition_conversion_gate.md | True | e85d2cb300694ea53eaabf39eb4270f8a07e3f8fcff0064231b75a6eb050b086 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| reports/ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md | reports/ugc12506_beta_closure_bullock_spin_conversion_proxy_gate.md | True | 064c7f12ade578142a9ca1af26fa328b800d4cd7845bf3919a4fe3ac0061e8bd | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_source_declared_spin_proxy_fields.csv | data/derived/ugc12506_beta_closure_source_declared_spin_proxy_fields.csv | True | 6186dfa2a19d80904c05593603564d9578097b91c8f1f24800a63e5df731451d | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv | data/derived/ugc12506_beta_closure_source_declared_spin_proxy_transfer_queue.csv | True | 40b10cb94fd6cbfe5946a178665dd2d2a0eaea4e5df5ddbe3f701b8e35f493cb | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv | data/derived/ugc12506_beta_closure_source_declared_spin_proxy_gate_summary.csv | True | 3ad5d2b22076c5494156a2ecc47d8442250299afe302af1c45c060d0a34b9f8a | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv | data/derived/ugc12506_beta_closure_direct_lambda_spin_source_evidence.csv | True | 8d35bebd6da82d1e0a5877bfa27fc83982753b73fc5b8e31e8a9b8497a0f6f3a | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv | data/derived/ugc12506_beta_closure_direct_lambda_spin_source_gate_summary.csv | True | 0194b78f124fe0c81b25333783b6ebb50224203be8fd7204763e6bc5612c1fa2 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_lambda_definition_conversion_checks.csv | data/derived/ugc12506_beta_closure_lambda_definition_conversion_checks.csv | True | 1417f6603babd7643b75184182c5185143f1e1432c88e53f4fb277eda0f8bb61 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_lambda_definition_conversion_comparison.csv | data/derived/ugc12506_beta_closure_lambda_definition_conversion_comparison.csv | True | 7eabf313ef5c1a94e1b05f9f2b881d3c13e8ada30d257438a21fa41d1b67db0f | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_lambda_definition_conversion_worklist.csv | data/derived/ugc12506_beta_closure_lambda_definition_conversion_worklist.csv | True | cf3197e906a19dbd3e096f09deb13d7c777b2504b59718547a33f9cdc7b8485b | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_values.csv | True | 97887518a6b7767e4fcea32e484a9a226f87bbbf62c9676848c90d6e2f3d00b6 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_comparison.csv | True | 70ca3d042361e3531655b22ed6956d875ae925845133189d783fda3211466e5a | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_checks.csv | True | 0e4e2f3db2ae902d963e1b79bc03c5e6e2986b5340e1697e64a974f1355fa9a3 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv | data/derived/ugc12506_beta_closure_bullock_spin_conversion_proxy_summary.csv | True | 34dd51c193b7f44aa886ad95c5410b39780ed07983bcaef6083093229ed2bc1e | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_candidates.csv | data/derived/ugc12506_beta_closure_transfer_candidates.csv | True | 2086838604251df9334f4df58911e1a34238e633778c76b8133d6cd8a1dd06a3 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_halo_fit_fields.csv | data/derived/ugc12506_beta_closure_transfer_halo_fit_fields.csv | True | d2fcbd6db6e5aae4b922cd854d218de8395e682399155a6af74e143d813fe38d | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_priority_gate.csv | data/derived/ugc12506_beta_closure_transfer_priority_gate.csv | True | 98f4c248679bc6ad3a35cb94002cb049b5348149c252b82bef341558db9e844c | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| README.md | reports/ugc12506_beta_closure_spin_proxy_review_prompt.md | True | 39abd2b736f145f55bf2d3d9b58f3e602b2b2e6ae1d88d4b4ea1b696d6c9c94c | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| response/ugc12506_beta_closure_spin_proxy_review_response_blank.csv | data/derived/ugc12506_beta_closure_spin_proxy_review_response_blank.csv | True | 55c7e305322fdf1872130ae17104d14170ccc832a24a5eea303f64e21a34d306 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_spin_proxy_review_packet.csv | data/derived/ugc12506_beta_closure_spin_proxy_review_packet.csv | True | f87cc63948eb278b34680aba25156d43760d74755b4f74dc8cd52dbd59e88b88 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_spin_proxy_review_obligations.csv | data/derived/ugc12506_beta_closure_spin_proxy_review_obligations.csv | True | 0baa0a19fa78f8d7a52193f1d25d1b5890c34496f225e3b4658c7e9d9eed9bc9 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv | data/derived/ugc12506_beta_closure_spin_proxy_review_forbidden_inputs.csv | True | a9f2a4f562f2a0a313c5ca11e8cfe5a4d0866e70c57a55443be82afbab192619 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_spin_proxy_review_response_template.csv | data/derived/ugc12506_beta_closure_spin_proxy_review_response_template.csv | True | 55c7e305322fdf1872130ae17104d14170ccc832a24a5eea303f64e21a34d306 | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |
| USAGE.md | generated_by_bundle_builder | True | 0073d29b3466ef50d4025a6618626d19436ccdd50e90f8747d0a849e8034048d | ugc12506_beta_closure_spin_proxy_review_bundle_not_endpoint |

## Claim Boundary

The proxy can only move forward after a completed independent response
passes an intake validator. This script does not authorize beta_cl replay
or endpoint scoring.
