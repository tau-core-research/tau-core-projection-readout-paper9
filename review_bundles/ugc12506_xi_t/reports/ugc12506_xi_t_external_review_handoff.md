# UGC12506 Xi_t External Review Handoff

This handoff converts the UGC12506 Xi_t source-review packet into a fillable response form and reviewer prompt. It is not an accepted manifest and not an endpoint.

## Handoff Summary

| handoff_status | galaxy | response_form_path | response_intake_script | current_intake_status | n_review_tasks | n_allowed_route_responses | n_forbidden_inputs | endpoint_scores_allowed | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_XI_T_EXTERNAL_REVIEW_HANDOFF_READY | UGC12506 | data/derived/ugc12506_xi_t_source_review_response_blank.csv | scripts/run_ugc12506_xi_t_source_review_response_intake.py | U12506_XI_T_SOURCE_REVIEW_RESPONSE_USABLE_MANIFEST_GATE_REQUIRED | 6 | 5 | 5 | False | False | ugc12506_xi_t_external_review_handoff_not_endpoint |

## Review Tasks

| obligation_id | obligation_status | question | accepted_evidence | forbidden_evidence | response_fields | allowed_field_values | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| U12506_XIT_REV_1_HIGHSPIN_CLOCK_STATUS | REVIEW_REQUIRED | Is the reported high-spin, low-density H I envelope source context admissible as a clock/readout settling proxy? | HIghMass or source-native H I context: high spin, low-density extended H I, stable/settling interpretation | rotation-curve residual size or best-fitting readout family | highspin_clock_status_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |
| U12506_XIT_REV_2_EDGEON_PV_CLOCK_SLICE | REVIEW_REQUIRED | Is the high-inclination PV/envelope-method context admissible as a time-slice/readout proxy rather than only an ordinary projection proxy? | source statements that velocity-field curves underestimate rotation and PV/envelope method is required | choosing the clock channel because it improves the endpoint curve | edgeon_pv_clock_slice_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |
| U12506_XIT_REV_3_ENVELOPE_MAPPING | REVIEW_REQUIRED | Is the radial K_t envelope ramp from disk scale to H I support radius acceptable as source-side mapping? | source-frozen R_d, R_opt, R_HI, H I extent, and low-density envelope support | moving the active radius or ramp shape after inspecting residual zones | envelope_mapping_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |
| U12506_XIT_REV_4_ASYMMETRY_PHASE | REVIEW_REQUIRED_CAVEATED | Should the approaching/receding side asymmetry remain as a caveated clock-phase component, be demoted, or be excluded? | source-native PV/envelope asymmetry statements and source-side extent asymmetry | including asymmetry only where the curve underpredicts | asymmetry_phase_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |
| U12506_XIT_REV_5_PATH_ZERO_POLICY | REVIEW_REQUIRED_FOR_NONZERO_PATH_ONLY | Is the current zero path/environment term correct until a cone/path review establishes a foreground/path object? | observer-path interloper audit and catalogue cone/path review | activating path load from image-plane coincidence or residual rescue | path_zero_policy_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |
| U12506_XIT_REV_6_CAP_POLICY | PROTOCOL_REVIEW_REQUIRED | May epsilon_cap=0.035 be carried as a predeclared small-mismatch protocol cap for this source shell? | For Xi_t=1+epsilon_t, the neglected quadratic term in Xi_t^2 is epsilon_t^2.  Relative to the linear correction 2 epsilon_t, this is epsilon_t/2.  Requiring a <=2% second-order-to-linear ratio gives epsilon_t <= 0.04. The protocol cap epsilon_cap=0.035 is a conservative predeclared value inside that admissible interval. | claiming epsilon_cap is a universal Tau Core constant | cap_policy_decision | ACCEPT; ACCEPT_WITH_CAVEAT; DEMOTE_OR_EXCLUDE; REQUEST_REMEASUREMENT; REJECT; PENDING | False | ugc12506_xi_t_external_review_handoff_not_endpoint |

## Response Form

| galaxy | reviewer_id | review_timestamp_utc | allowed_response | source_inputs_used | forbidden_inputs_used | endpoint_scores_allowed_after_response | accepted_manifest_allowed_after_response | claims_universal_tau_constant | highspin_clock_status_decision | edgeon_pv_clock_slice_decision | envelope_mapping_decision | asymmetry_phase_decision | path_zero_policy_decision | cap_policy_decision | review_notes | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | FILL_ME | FILL_ME | PENDING_INDEPENDENT_REVIEW | PENDING | none | False | False | False | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | FILL_ME | ugc12506_xi_t_external_review_handoff_not_endpoint |

## Allowed Route Responses

| allowed_response | response_meaning | effect_on_endpoint_path | requires_extra_source_work | endpoint_scores_allowed_by_response_alone | galaxy | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACCEPT_SOURCE_ONLY_XIT_MANIFEST_WITH_PROTOCOL_CAP | accept K_t(R), clock proxy, zero-path policy, and epsilon_cap as protocol cap | allows a future accepted-manifest gate, but not endpoint scoring by response alone | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL | accept K_t(R) shape but carry cap or asymmetry as interval/control uncertainty | requires interval manifest and controls before scoring | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| ACCEPT_CORE_COMPONENTS_DROP_ASYMMETRY | accept high-spin, edge-on PV, and envelope terms, but exclude asymmetry phase component | rebuild source shell without asymmetry before accepted-manifest gate | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| REQUEST_SOURCE_NATIVE_REMEASUREMENT | request new source-native measurement of envelope window, asymmetry, or clock proxy | keeps endpoint blocked and creates a source acquisition/reduction task | True | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| REJECT_XIT_CLOCK_ROUTE | reject UGC12506 Xi_t time-readout route as insufficiently source-grounded | preserve as negative route result; do not run Xi_t endpoint | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |

## Forbidden Inputs

| forbidden_input_id | forbidden_input | reason | galaxy | claim_boundary |
| --- | --- | --- | --- | --- |
| U12506_XIT_FORBID_1_ROTATION_RESIDUALS | v_obs residuals, endpoint RMSE, or radial residual zones | would turn source review into residual-selected clock tuning | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_2_BASELINE_RANKS | Newton/MOND/RAR/RMOND/TPG baseline ranks | baseline comparison can only be post-score diagnostic context | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_3_TAU_WRONG_FAMILY_SCORES | wrong-family Tau score ranks or best Tau family | readout route must be selected from source morphology/projection evidence | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_4_POSTHOC_CAP_CHANGE | changing epsilon_cap after endpoint scoring | would convert the protocol cap into amplitude rescue | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_5_FOREGROUND_RESCUE | activating path term from a residual deficit without cone/path evidence | path/environment term must remain zero unless source review supports it | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |

## Input Hashes

| input_file | exists | sha256 | claim_boundary |
| --- | --- | --- | --- |
| ugc12506_highmass_fast_source_context_evidence.csv | True | 4bfc834bed9535ee024840f86be15715b7c61c84537f05d7b2bbf6c9c009f3bc | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_observer_path_interloper_audit_summary.csv | True | 7544081480d20eca5fc125d53fda42a8741b2f110de9999ee102e8c1006a0ea6 | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_projection_highspin_preflight_observables.csv | True | 1bea38d3768ee5afc13bfe30ba99b7611ba2af924a0272d2dd072f86dca100c2 | ugc12506_xi_t_source_review_packet_not_endpoint |
| time_readout_xi_p1_source_review_intake.csv | True | 05a57594420def81d8585c6cff7eafe8a20231ddd57d3a65eab9146226f462ef | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_highspin_envelope_clock_shell_components.csv | True | 7cf0cc7a2125f6eeb62dbd6aebe76b05fb9e527fa84a2dbb64b93378cfdc1796 | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_highspin_envelope_clock_shell_manifest.csv | True | fd16bcbdc02f4e1b0ccb967be3bae4dd5b573471a4326e36e13dfc81fc532d1b | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_highspin_envelope_clock_shell_gates.csv | True | 3e6057b8ea3301f26bf76d985f670d2c01bbdd75d90d28c552224f09313c283f | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_normalization_theorem.csv | True | 8adfe96ead99916edc5d8e75cda57be68fe33b08b4797bfc0b91f40a1fe40120 | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_epsilon_cap_protocol_theorem.csv | True | 959e79dc304c35c9f5b2d762c46ed6c81df2837bc3a6d1b15c75a32308647ea5 | ugc12506_xi_t_source_review_packet_not_endpoint |
| ugc12506_xi_t_accepted_manifest_gate_items.csv | True | 8fc40138e85e8146675d699b681268f9e5a6264e8439fe45380c8eec604ff50e | ugc12506_xi_t_source_review_packet_not_endpoint |

## Claim Boundary

The handoff is ready for residual-blind external review. A filled response must be passed through the response-intake validator before any accepted-manifest gate can be rerun.
