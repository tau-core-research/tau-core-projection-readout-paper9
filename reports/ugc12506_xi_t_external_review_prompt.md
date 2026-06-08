# External Review Prompt: UGC12506 Xi_t Time-Readout Source Route

You are asked to perform a residual-blind source review of the UGC12506
time-readout candidate route.  Do not inspect or use rotation-curve residuals,
endpoint RMSE, baseline ranks, wrong-family Tau scores, or any post-hoc fit
quality.  Your task is only to decide whether the source evidence supports the
candidate source-side readout route.

## Candidate route

- Galaxy: `UGC12506`
- Candidate formula: `Xi_t(R)=1+epsilon_t K_t(R)`
- Candidate kernel: `K_t=norm[w_spin K_spin + w_edge K_spin + w_env K_env + w_asym K_asym + 0*K_path]`
- Epsilon rule: `epsilon_t=min(0.035, 0.035*Gamma_clock), Gamma_clock=L/(1+L)`
- Current epsilon_t: `0.0238438`
- Path policy: `foreground/path term set to zero because path evidence is not established`

## What to review

1. Is the high-spin, low-density H I envelope context admissible as a
   clock/readout settling proxy?
2. Is the high-inclination PV/envelope-method context admissible as a
   time-slice/readout proxy, rather than only an ordinary projection proxy?
3. Is the radial K_t envelope ramp from disk scale / optical radius toward
   H I support radius acceptable as a source-side mapping?
4. Should the approaching/receding side asymmetry remain as a caveated
   clock-phase component, be demoted, or be excluded?
5. Is the zero path/environment term correct unless a cone/path review
   establishes a foreground/path object?
6. May `epsilon_cap=0.035` be carried only as a predeclared small-mismatch
   protocol cap, not as a universal Tau Core constant?

## Allowed route-level responses

Choose exactly one value for `allowed_response` in the response CSV:

| allowed_response | response_meaning | effect_on_endpoint_path | requires_extra_source_work | endpoint_scores_allowed_by_response_alone | galaxy | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ACCEPT_SOURCE_ONLY_XIT_MANIFEST_WITH_PROTOCOL_CAP | accept K_t(R), clock proxy, zero-path policy, and epsilon_cap as protocol cap | allows a future accepted-manifest gate, but not endpoint scoring by response alone | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| ACCEPT_KT_CARRY_CAP_AS_CAVEATED_INTERVAL | accept K_t(R) shape but carry cap or asymmetry as interval/control uncertainty | requires interval manifest and controls before scoring | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| ACCEPT_CORE_COMPONENTS_DROP_ASYMMETRY | accept high-spin, edge-on PV, and envelope terms, but exclude asymmetry phase component | rebuild source shell without asymmetry before accepted-manifest gate | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| REQUEST_SOURCE_NATIVE_REMEASUREMENT | request new source-native measurement of envelope window, asymmetry, or clock proxy | keeps endpoint blocked and creates a source acquisition/reduction task | True | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |
| REJECT_XIT_CLOCK_ROUTE | reject UGC12506 Xi_t time-readout route as insufficiently source-grounded | preserve as negative route result; do not run Xi_t endpoint | False | False | UGC12506 | False | ugc12506_xi_t_source_review_packet_not_endpoint |

## Forbidden inputs

The following inputs must not be used:

| forbidden_input_id | forbidden_input | reason | galaxy | claim_boundary |
| --- | --- | --- | --- | --- |
| U12506_XIT_FORBID_1_ROTATION_RESIDUALS | v_obs residuals, endpoint RMSE, or radial residual zones | would turn source review into residual-selected clock tuning | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_2_BASELINE_RANKS | Newton/MOND/RAR/RMOND/TPG baseline ranks | baseline comparison can only be post-score diagnostic context | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_3_TAU_WRONG_FAMILY_SCORES | wrong-family Tau score ranks or best Tau family | readout route must be selected from source morphology/projection evidence | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_4_POSTHOC_CAP_CHANGE | changing epsilon_cap after endpoint scoring | would convert the protocol cap into amplitude rescue | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |
| U12506_XIT_FORBID_5_FOREGROUND_RESCUE | activating path term from a residual deficit without cone/path evidence | path/environment term must remain zero unless source review supports it | UGC12506 | ugc12506_xi_t_source_review_packet_not_endpoint |

## Required response file

Fill:

`data/derived/ugc12506_xi_t_source_review_response_blank.csv`

Then save a copy as:

`data/derived/ugc12506_xi_t_source_review_response.csv`

After that, run:

`python scripts/run_ugc12506_xi_t_source_review_response_intake.py`

The response may feed a later accepted-manifest gate.  It cannot by itself
authorize endpoint scoring or promote `epsilon_cap` to a universal constant.
