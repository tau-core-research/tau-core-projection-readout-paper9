# Time-Readout Xi_t P1 Source-Review Worklist

This artifact operationalizes the P1 rows from the diagnostic Xi_t
readiness manifest. It is not an endpoint score and does not promote
any accepted Xi_t(R) manifest.

## Worklist

| galaxy | p1_route | source_question | required_observable | acceptable_source_types | freeze_rule_needed | forbidden_endpoint_inputs | acceptance_condition | failure_policy | priority | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC4088 | warp_history_asymmetry_clock_phase | Does the source literature support a clock/readout phase proxy distinct from the already accepted warp/history morphology kernel? | warp/asymmetry phase proxy | H I velocity-field asymmetry; channel-map warp phase; optical/H I disturbance classification; companion/interaction context | map source-side asymmetry/history phase to K_t(R) shape and epsilon_t sign without using rotation residuals | v_obs residual; previous Xi_t improvement; best wrong-family score; post-hoc epsilon increase | independent sources identify a time/phase-like warp-history component not already counted by the additive morphology kernel | keep Xi_t=1 or retain NGC4088 as additive morphology-only endpoint if evidence is not independent | P1 | time_readout_xi_p1_source_review_not_endpoint |
| NGC4088 | warp_history_asymmetry_clock_phase | Can the normalization law be frozen before scoring? | accepted epsilon_t normalization law | source-side bounded asymmetry index; source-side interaction load; predeclared coefficient rule derived from source observables | epsilon_0 = f(source_load) with cap and sign fixed before endpoint replay | RMSE minimization; amplitude scan; residual-tail matching | normalization is computable from source manifest alone and has dimensionless status | do not score an accepted Xi_t endpoint; keep diagnostic result only | P1 | time_readout_xi_p1_source_review_not_endpoint |
| UGC12506 | edgeon_highspin_clock_envelope | Does the high-spin edge-on H I envelope support a clock/readout proxy rather than only a spatial projection proxy? | edge-on PV/envelope time-slice consistency proxy | resolved H I position-velocity envelope; high-spin settling evidence; inclination/envelope coherence; source-native halo/envelope tables | map high-spin envelope stress to K_t(R) shape without using the rotation residual | using the underprediction gap to choose the radial shape; amplitude rescue by residual matching | source data support a broad clock/readout layer tied to high-spin edge-on envelope structure | retain UGC12506 as underpredicted stress test, not a successful Xi_t endpoint | P1 | time_readout_xi_p1_source_review_not_endpoint |
| UGC12506 | edgeon_highspin_clock_envelope | Is there a path/environment reason to activate Xi_t beyond ordinary edge-on projection? | path/foreground review | microwave/dust foreground audit; nearby projected interloper audit; source-observer bundle environment notes | decide whether path term enters epsilon_t, remains a caveat, or is rejected | image-plane coincidence without path evidence; treating generic foreground as accepted clock evidence | path evidence is independently non-negligible or explicitly rejected with Xi_t driven only by source envelope | set path term to zero and test only source-envelope clock proxy if otherwise accepted | P1 | time_readout_xi_p1_source_review_not_endpoint |

## Gates

| gate_id | gate_status | required_condition | blocked_by | claim_boundary |
| --- | --- | --- | --- | --- |
| XI_P1_G1_SOURCE_ONLY | OPEN | Every Xi_t observable must be filled from source-side morphology, path, or clock/readout evidence before endpoint scoring. | no accepted Xi_t source manifest yet | time_readout_xi_p1_source_review_not_endpoint |
| XI_P1_G2_NO_DOUBLE_COUNT | OPEN | The Xi_t proxy must be shown distinct from the additive morphology/projection kernel already used for the galaxy. | NGC4088 and UGC12506 need separation of clock/readout phase from spatial morphology amplitude | time_readout_xi_p1_source_review_not_endpoint |
| XI_P1_G3_NORMALIZATION_FREEZE | OPEN | epsilon_t normalization and cap must be frozen from source rules, not residual improvement. | current epsilon_0 is diagnostic source-load proxy, not an accepted theory/source law | time_readout_xi_p1_source_review_not_endpoint |
| XI_P1_G4_NULL_ALLOWED | PASS_RECORDED | The protocol must allow Xi_t=1 for galaxies without independent time-readout evidence. | none; P3 and P2 rows already enforce this policy | time_readout_xi_p1_source_review_not_endpoint |

## Summary

| source_review_status | p1_targets | n_required_review_items | accepted_xi_t_manifests | endpoint_scores_allowed | next_step | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| XI_T_P1_SOURCE_REVIEW_WORKLIST_CREATED_NO_ENDPOINT | NGC4088; UGC12506 | 4 | 0 | False | fill P1 source observables, freeze epsilon_t/K_t rules, then run a predeclared Xi_t ablation endpoint | time_readout_xi_p1_source_review_not_endpoint |
