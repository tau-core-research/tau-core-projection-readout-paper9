# UGC12506 Beta-Closure Transfer Predeclaration

This gate predeclares independent transfer candidates for the UGC12506
source-derived beta-closure rule. It does not score any endpoint.

## Summary

| transfer_predeclaration_status | n_candidates | n_endpoint_scores_allowed | n_replay_scores_allowed_now | selection_inputs | top_candidates | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_BETA_CLOSURE_TRANSFER_CANDIDATES_PREDECLARED_SOURCE_ACQUISITION_REQUIRED | 11 | 0 | 0 | SPARC inclination, RHI/Rdisk, MHI, Vflat, quality flag; no rotation residuals | UGC11455;ESO563-G021;IC4202;NGC0891;NGC4013;NGC2841;NGC4157;NGC4217 | acquire_source_native_spin_and_halo_fit_fields_for_top_candidates | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |

## Candidates

| predeclared_rank | galaxy | transfer_priority_score | inclination_deg | rhi_over_rdisk | mhi_1e9_msun | vflat_km_s | quality_q | gas_to_l36 | candidate_reason | missing_source_native_fields | beta_cl_replay_status | endpoint_scores_allowed | uses_vobs_or_residual_for_selection | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | UGC11455 | 0.901631 | 90 | 7.32546 | 13.335 | 269.4 | 1 | 0.0356244 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 2 | ESO563-G021 | 0.845233 | 83 | 10.222 | 24.298 | 314.6 | 1 | 0.0780842 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 3 | IC4202 | 0.816178 | 90 | 6.72176 | 12.326 | 242.6 | 1 | 0.0685734 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 4 | NGC0891 | 0.759666 | 90 | 7.12157 | 4.462 | 216.1 | 1 | 0.0322539 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 5 | NGC4013 | 0.709181 | 89 | 8.88102 | 2.967 | 172.9 | 2 | 0.0375123 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 6 | NGC2841 | 0.669507 | 76 | 12.3956 | 9.775 | 284.8 | 1 | 0.0519612 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 7 | NGC4157 | 0.624177 | 82 | 10.3836 | 8.226 | 184.7 | 1 | 0.077883 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 8 | NGC4217 | 0.513691 | 86 | 5.68027 | 2.562 | 181.3 | 1 | 0.0300355 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 9 | NGC0801 | 0.506006 | 80 | 5.1594 | 23.201 | 220.1 | 1 | 0.0742266 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 10 | NGC3521 | 0.499024 | 75 | 7.85417 | 4.154 | 213.7 | 1 | 0.0489651 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| 11 | NGC7331 | 0.422194 | 75 | 5.38048 | 11.067 | 239 | 1 | 0.0441565 | high-inclination/extended-HI/massive-gas source proxy for beta_cl transfer | lambda_spin;chi2_NFW;chi2_ISO;source-native halo fit reference;PV/envelope method notes | SOURCE_ACQUISITION_REQUIRED_BEFORE_REPLAY | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |

## Source Worklist

| galaxy | predeclared_rank | required_field | source_hint | field_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC11455 | 1 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| UGC11455 | 1 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| UGC11455 | 1 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| UGC11455 | 1 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| UGC11455 | 1 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| ESO563-G021 | 2 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| ESO563-G021 | 2 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| ESO563-G021 | 2 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| ESO563-G021 | 2 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| ESO563-G021 | 2 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| IC4202 | 3 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| IC4202 | 3 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| IC4202 | 3 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| IC4202 | 3 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| IC4202 | 3 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC0891 | 4 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC0891 | 4 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC0891 | 4 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC0891 | 4 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC0891 | 4 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4013 | 5 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4013 | 5 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4013 | 5 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4013 | 5 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4013 | 5 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC2841 | 6 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC2841 | 6 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC2841 | 6 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC2841 | 6 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC2841 | 6 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4157 | 7 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4157 | 7 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4157 | 7 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4157 | 7 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4157 | 7 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4217 | 8 | lambda_spin | literature halo/spin or HIghMass-like dynamical modelling | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4217 | 8 | chi2_NFW | source-native dark-matter halo fit table | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4217 | 8 | chi2_ISO | same source-native halo fit table as chi2_NFW | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4217 | 8 | PV/envelope notes | HI velocity-field or PV/envelope-tracing source | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |
| NGC4217 | 8 | independent replay freeze | freeze beta_cl before endpoint scoring | MISSING_SOURCE_NATIVE_REVIEW_REQUIRED | False | False | ugc12506_beta_closure_transfer_predeclaration_not_endpoint |

## Claim Boundary

Selection uses only residual-blind SPARC source proxies. Candidate rows
must acquire source-native spin and NFW/ISO closure-preference fields
before any beta_cl replay can be promoted beyond source acquisition.
