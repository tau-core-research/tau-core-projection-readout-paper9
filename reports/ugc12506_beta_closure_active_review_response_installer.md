# UGC12506 Beta-Closure Active Review Response Installer

This installer validates completed reviewer response CSVs from the
incoming directory and copies them into active response paths only when
both files are present, non-placeholder, one-row, schema-valid, and
free of endpoint/residual flags.

## Summary

| active_response_install_status | incoming_dir | n_required_responses | n_existing_incoming_responses | n_install_allowed_responses | spin_response_installed | carrier_response_installed | active_spin_response_exists | active_carrier_response_exists | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_ACTIVE_REVIEW_RESPONSES_INSTALLED_RUN_POST_REVIEW_LAUNCHER | review_bundles/incoming/ugc12506_beta_closure_transfer_scoring | 2 | 2 | 2 | True | True | True | True | False | False | False | False | run_ugc12506_beta_closure_post_review_scoring_launcher | ugc12506_beta_closure_active_review_response_installer_not_endpoint |

## Checks

| response_type | incoming_path | exists | schema_pass | single_row_pass | not_placeholder_pass | forbidden_flags_pass | install_allowed | reason | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| spin_route_review | review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/ugc12506_beta_closure_spin_proxy_review_response.csv | True | True | True | True | True | True | validated active response | False | False | ugc12506_beta_closure_active_review_response_installer_not_endpoint |
| carrier_review | review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/ugc12506_beta_closure_carrier_review_response.csv | True | True | True | True | True | True | validated active response | False | False | ugc12506_beta_closure_active_review_response_installer_not_endpoint |

## Claim Boundary

This script does not create review decisions. Missing or placeholder
responses keep scoring blocked.
