# UGC12506 Beta-Closure Carrier Review Response Intake

This intake validates a completed independent carrier review response if
one is present. It does not score.

## Summary

| carrier_review_intake_status | response_received | response_source | selected_carrier_id | carrier_prefreeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CARRIER_REVIEW_ACCEPTED_PREFREEZE_ALLOWED | True | data/derived/ugc12506_beta_closure_carrier_review_response.csv | BARYONIC_050_FAST_PACKET | True | False | False | build_beta_cl_transfer_carrier_prefreeze_manifest | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |

## Checks

| check_id | result | reason | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| BCR_INTAKE_1_CARRIER_DECISION | PASS | carrier_route_decision=ACCEPT_BARYONIC_STRESS_CARRIER | False | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |
| BCR_INTAKE_2_SUPPORTED_CARRIER | PASS | selected_carrier_id=BARYONIC_050_FAST_PACKET | False | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |
| BCR_INTAKE_3_LI2020_POLICY | PASS | li2020_policy_decision=KEEP_LI2020_CONTROL_ONLY | False | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |
| BCR_INTAKE_4_FORBIDDEN_INPUTS | PASS | forbidden_inputs_used=False | False | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |
| BCR_INTAKE_5_NO_ENDPOINT_FLAGS | PASS | endpoint_scores_allowed=False; uses_vobs_or_residual=False | False | ugc12506_beta_closure_carrier_review_response_intake_not_endpoint |

## Claim Boundary

Only a passed independent carrier response can move the carrier toward a
prefreeze manifest. Endpoint scoring remains false here.
