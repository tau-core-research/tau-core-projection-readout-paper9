# UGC12506 Beta-Closure Transfer Priority Gate

This gate narrows the predeclared transfer queue after source-native
pISO/NFW halo-fit fields have been acquired. It does not score endpoint
curves and does not infer the still-missing spin or PV/envelope fields.

## Summary

| priority_gate_status | n_candidates | n_primary_nfw_preference_targets | n_weak_nfw_preference_targets | n_piso_preferred_controls | primary_targets | n_endpoint_scores_allowed | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_BETA_CLOSURE_TRANSFER_PRIORITY_GATE_BUILT_ENDPOINT_BLOCKED | 11 | 2 | 3 | 6 | NGC0891;NGC7331 | 0 | source_freeze_lambda_spin_and_pv_for_primary_targets | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |

## Priority Ledger

| post_halo_rank | predeclared_rank | galaxy | transfer_priority_score | chi2_ISO | chi2_NFW | chi2_ISO_over_NFW | nfw_preference_load | transfer_priority_class | still_missing_fields | next_source_gate | endpoint_scores_allowed | uses_vobs_or_residual_for_priority | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | NGC0891 | 0.759666 | 4.24 | 3.46 | 1.22543 | 0.225434 | PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET | lambda_spin;PV/envelope method notes;independent replay freeze | acquire_lambda_spin_and_pv_envelope_evidence_first | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 2 | 11 | NGC7331 | 0.422194 | 0.95 | 0.81 | 1.17284 | 0.17284 | PRIMARY_NFW_PREFERENCE_TRANSFER_TARGET | lambda_spin;PV/envelope method notes;independent replay freeze | acquire_lambda_spin_and_pv_envelope_evidence_first | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 3 | 6 | NGC2841 | 0.669507 | 1.58 | 1.48 | 1.06757 | 0.0675676 | WEAK_NFW_PREFERENCE_TRANSFER_TARGET | lambda_spin;PV/envelope method notes;independent replay freeze | hold_as_secondary_transfer_or_control_until_spin_pv_available | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 4 | 9 | NGC0801 | 0.506006 | 7.07 | 6.77 | 1.04431 | 0.0443131 | WEAK_NFW_PREFERENCE_TRANSFER_TARGET | lambda_spin;PV/envelope method notes;independent replay freeze | hold_as_secondary_transfer_or_control_until_spin_pv_available | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 5 | 5 | NGC4013 | 0.709181 | 0.84 | 0.81 | 1.03704 | 0.037037 | WEAK_NFW_PREFERENCE_TRANSFER_TARGET | lambda_spin;PV/envelope method notes;independent replay freeze | hold_as_secondary_transfer_or_control_until_spin_pv_available | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 6 | 1 | UGC11455 | 0.901631 | 2.4 | 5.4 | 0.444444 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 7 | 2 | ESO563-G021 | 0.845233 | 12.37 | 19.15 | 0.645953 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 8 | 3 | IC4202 | 0.816178 | 8.67 | 20.17 | 0.429846 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 9 | 7 | NGC4157 | 0.624177 | 0.45 | 0.49 | 0.918367 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 10 | 8 | NGC4217 | 0.513691 | 2.23 | 3.74 | 0.596257 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |
| 11 | 10 | NGC3521 | 0.499024 | 0.2 | 0.25 | 0.8 | 0 | PISO_PREFERRED_CONTROL_OR_ALTERNATIVE_BRANCH | lambda_spin;PV/envelope method notes;independent replay freeze | do_not_run_beta_cl_replay; use_as_control_or_reclassify_branch | False | False | ugc12506_beta_closure_transfer_priority_gate_not_endpoint |

## Interpretation

The UGC12506 beta-closure route is not licensed by edge-on geometry and
large H I extent alone. A positive source-side NFW-preference load is
also required. Rows with pISO-preferred halo fits are preserved as
controls or alternative-branch candidates rather than forced through
the UGC12506 beta_cl replay.
