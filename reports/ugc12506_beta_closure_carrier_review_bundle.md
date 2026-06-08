# UGC12506 Beta-Closure Carrier Review Bundle

This bundle packages the carrier decision matrix and review obligations.
It does not accept a carrier and does not score.

## Summary

| carrier_review_bundle_status | review_packet_id | bundle_root | zip_path | n_bundle_files | n_missing_inputs | review_response_received | carrier_prefreeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CARRIER_REVIEW_BUNDLE_READY_RESPONSE_PENDING | U12506_BETA_CARRIER_REVIEW_PACKET_V1 | review_bundles/ugc12506_beta_closure_carrier | review_bundles/ugc12506_beta_closure_carrier_review_bundle.zip | 10 | 0 | False | False | False | False | intake_independent_carrier_review_response | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |

## Obligations

| obligation_id | review_question | required_decision | allowed_evidence | forbidden_inputs | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| BCR_REV_1_CARRIER_ROUTE | Which carrier route, if any, may be frozen before beta_cl transfer scoring? | ACCEPT_BARYONIC_STRESS_CARRIER_OR_REQUIRE_SOURCE_NATIVE_CARRIER_OR_REJECT | carrier route decision matrix; SPARC fast-packet provenance; source-native carrier derivation artifacts if supplied | endpoint residuals; score ranks; curve-saving amplitude choices | False | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| BCR_REV_2_LEAKAGE_POLICY | Should Li et al. NFW-fit products remain control-only, or has a separate leakage policy justified their use? | KEEP_LI2020_CONTROL_ONLY_OR_SUPPLY_POLICY | provenance and leakage-policy arguments | selecting NFW carrier because it improves endpoint score | False | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |

## Forbidden Inputs

| forbidden_input_id | forbidden_input | reason | claim_boundary |
| --- | --- | --- | --- |
| BCR_FORBID_1_ENDPOINT_RESIDUALS | rotation residuals or endpoint RMSE | carrier selection must precede scoring | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| BCR_FORBID_2_BASELINE_RANKS | Newton/MOND/RAR/RMOND/TPG rank comparisons | baseline weakness may motivate stress testing but cannot choose carrier | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| BCR_FORBID_3_NFW_SCORE_SELECTION | choosing Li2020 NFW carrier from fit quality or endpoint advantage | Li2020 halo-fit products are control-only without explicit leakage policy | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |

## Bundle Manifest

| bundle_relative_path | source_path | exists | sha256 | claim_boundary |
| --- | --- | --- | --- | --- |
| reports/ugc12506_beta_closure_transfer_carrier_freeze_gate.md | reports/ugc12506_beta_closure_transfer_carrier_freeze_gate.md | True | 2e358ebdca0d7c78607dc9d61bc415925cbf1cbba8e5e1e679f01da62e882329 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv | data/derived/ugc12506_beta_closure_transfer_carrier_route_decision_matrix.csv | True | d406741458954e5cd310bdb075e5da8a28ac4428356d61845a84612d5bb29ab6 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv | data/derived/ugc12506_beta_closure_transfer_carrier_freeze_summary.csv | True | af6cf037770887b9ae6cc786b5b2c30d1e57b538e2c866646eaad2265f4c9c31 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_carrier_freeze_gates.csv | data/derived/ugc12506_beta_closure_transfer_carrier_freeze_gates.csv | True | 70ef7b3554b07f6e0fa08a311ddca8b8b5db168338ed1d7a0a6a80b05cbf442d | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_candidates.csv | data/derived/ugc12506_beta_closure_transfer_candidates.csv | True | 2086838604251df9334f4df58911e1a34238e633778c76b8133d6cd8a1dd06a3 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_transfer_priority_gate.csv | data/derived/ugc12506_beta_closure_transfer_priority_gate.csv | True | 98f4c248679bc6ad3a35cb94002cb049b5348149c252b82bef341558db9e844c | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/fast_sparc_rotation_curve_packet_galaxy_summary.csv | data/derived/fast_sparc_rotation_curve_packet_galaxy_summary.csv | True | 46e8d96ae14527545d4c3055e7f4dcc2b718db4aa6125150198557664e7b6296 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_carrier_review_obligations.csv | data/derived/ugc12506_beta_closure_carrier_review_obligations.csv | True | 4d07da4e1363339f6beb8796aef9cc70deccaded4fb69945b1c4a77b65a5df87 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| data/ugc12506_beta_closure_carrier_review_forbidden_inputs.csv | data/derived/ugc12506_beta_closure_carrier_review_forbidden_inputs.csv | True | b1497f5706b02b5b0484d78a6ed2a7c2fa8ff497ed85ce1b636319a6d1be5430 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
| response/ugc12506_beta_closure_carrier_review_response_blank.csv | data/derived/ugc12506_beta_closure_carrier_review_response_blank.csv | True | 435bc638f968354da64b915a180de2a028083fbc11a0fc64137fdaae1b064d18 | ugc12506_beta_closure_carrier_review_bundle_not_endpoint |
