# UGC12506 Beta-Closure Scoring Readiness Dashboard

This dashboard condenses the beta-closure transfer path into a single
pre-scoring ledger. It is not an endpoint and it does not read observed
rotation curves.

## Summary

| scoring_readiness_status | n_dashboard_stages | n_ready_stages | n_blocked_stages | dry_run_contract_ready | unlock_packet_ready | active_responses_present | installer_ready | launcher_control_scores_written | scoring_launch_allowed | formula_manifest_ready_for_scoring | scores_written | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | next_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_BETA_CLOSURE_SCORING_READINESS_CONTROL_SCORES_WRITTEN_REVIEW_REQUIRED | 7 | 7 | 0 | True | True | 2 | True | True | True | True | True | True | False | False | review_control_scores_before_any_endpoint_claim | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |

## Stage Ledger

| stage_id | status | ready_for_next_stage | blocked | artifact | evidence | next_action | construction_used_vobs | scoring_used_vobs | endpoint_scores_allowed | endpoint_validation_claim | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SCORING_CONTRACT_DRY_RUN | U12506_BETA_CLOSURE_TRANSFER_SCORING_CONTRACT_DRY_RUN_READY_REVIEWS_PENDING | True | False | data/derived/ugc12506_beta_closure_transfer_scoring_contract_dry_run_summary.csv | 2 scenarios; 656 no-vobs predictions | build_unlock_packet | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| REVIEW_UNLOCK_PACKET | U12506_BETA_CLOSURE_TRANSFER_SCORING_UNLOCK_PACKET_READY_ACTIVE_RESPONSES_PENDING | True | False | data/derived/ugc12506_beta_closure_transfer_scoring_unlock_packet_summary.csv | 2 active responses required; 3 example-only rows | send_unlock_packet_to_independent_reviewer | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| ACTIVE_RESPONSE_INSTALLER | U12506_BETA_ACTIVE_REVIEW_RESPONSES_INSTALLED_RUN_POST_REVIEW_LAUNCHER | True | False | data/derived/ugc12506_beta_closure_active_review_response_install_summary.csv | 2/2 incoming active responses | place_completed_review_csvs_in_incoming_dir_then_run_installer | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| POST_REVIEW_LAUNCHER | U12506_BETA_CLOSURE_POST_REVIEW_SCORING_LAUNCHED_CONTROL_ONLY | True | False | data/derived/ugc12506_beta_closure_post_review_scoring_launcher_summary.csv | 2/2 active responses present; chain_ok=True | run_post_review_launcher_after_active_responses | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| SCORING_LAUNCH_GATE | U12506_BETA_CLOSURE_SCORING_LAUNCH_READY_CONTROL_ONLY | True | False | data/derived/ugc12506_beta_closure_scoring_launch_summary.csv | pass_gates=5; blocked_gates=0 | resolve_review_prefreeze_launch_gates | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| FORMULA_FREEZE_GATE | U12506_BETA_CLOSURE_TRANSFER_FORMULA_FREEZE_READY_FOR_SCORING_RUNNER | True | False | data/derived/ugc12506_beta_closure_transfer_formula_freeze_summary.csv | formula_manifest_rows=11 | freeze_nonempty_formula_manifest_before_scoring | False | False | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |
| TRANSFER_SCORING_RUNNER | U12506_BETA_CLOSURE_TRANSFER_SCORING_COMPLETE_CONTROL_ONLY | True | False | data/derived/ugc12506_beta_closure_transfer_scoring_summary.csv | scores_written=True; scoring_used_vobs=True | review_control_scores_if_runner_executes | False | True | False | False | ugc12506_beta_closure_scoring_readiness_dashboard_not_endpoint |

## One Command Path After Independent Review Responses

Place the completed reviewer files here:

```text
review_bundles/incoming/ugc12506_beta_closure_transfer_scoring/
```

Expected filenames:

```text
ugc12506_beta_closure_spin_proxy_review_response.csv
ugc12506_beta_closure_carrier_review_response.csv
```

Then run:

```bash
python scripts/install_ugc12506_beta_closure_active_review_responses.py
python scripts/run_ugc12506_beta_closure_post_review_scoring_launcher.py
python scripts/build_ugc12506_beta_closure_scoring_readiness_dashboard.py
```

The installer rejects missing, placeholder, example-only, endpoint-flagged,
or residual-leaking response rows. Until both active responses validate,
the scoring runner remains blocked and `vobs` is not read.
