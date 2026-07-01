# UGC07151 Expdisk+WVO Source Preflight

**Doc class:** source-side preflight audit

**Reader role:** Paper 9 projection/mixed replay maintainer

**Status:** `EXPDISK_ORIENTATION_CONTEXT_PASS_WVO_BLOCKED`

**Claim boundary:** `ugc07151_expdisk_wvo_source_preflight_not_endpoint`

## Purpose

This preflight tests the fastest proposed fresh analogue from the NGC4013
expdisk+WVO selection audit. It does not run endpoint scoring. It asks only
whether UGC07151 has enough residual-blind source support to freeze an
exponential-disk carrier plus WVO route.

## Summary

| galaxy | status | formula_family | candidate_route | fast_priority_rank | priority_tier | inclination_deg | quality_Q | rhi_over_rdisk | wvo_source_support | recommended_role | endpoint_scores_allowed | endpoint_validation_claim | uses_vobs_or_residual_for_selection | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC07151 | EXPDISK_ORIENTATION_CONTEXT_PASS_WVO_BLOCKED | K_exponential_disk | exponential_disk_plus_wvo | 4 | P1_acquire_after_P0 | 90 | 1 | 5.112 | blocked_or_negative | edge_on_truncation_control_or_source_reacquisition | False | False | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |

## Source Evidence

| evidence_id | source | source_url | secondary_source_url | observable | value | source_side_status | interpretation | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1_SPARC_PACKET | SPARC fast packet / SPARC public database | https://astroweb.case.edu/SPARC/ | https://zenodo.org/records/16284118 | regular disk carrier and edge-on orientation | T=6; Q=1; inclination=90.0 deg; RHI/Rdisk=5.112; rotation_ref=Sw09,Sw02 | ACCEPTED_CONTEXT | Supports UGC07151 as a high-inclination regular disk candidate with extended H I context. This does not by itself prove WVO/warp support. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |
| E2_EDGEON_TRUNCATION_WARP_CONTEXT | Truncations of stellar disks and warps of HI-layers in edge-on spiral galaxies | https://www.astro.rug.nl/~vdkruit/jea3/homepage/warppaper.pdf | https://arxiv.org/pdf/astro-ph/0702486 | UGC 7151 H I extent / truncation-warps context | Paper notes UGC 7151 among systems whose H I distributions do not extend significantly farther than the optical image. | NEGATIVE_OR_CAVEATED_WVO_SUPPORT | This weakens the case for using UGC07151 as the first clean expdisk+WVO analogue. It is better treated as an orientation/truncation control unless independent WVO/onset evidence is found. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |

## Gates

| gate_id | gate_status | reason | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- |
| U7151_G1_REGULAR_EXPDISK_CARRIER | PASS_SOURCE_CONTEXT | SPARC/manifest context supports K_exponential_disk and no bulge-dominated caveat is active in the queue. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |
| U7151_G2_EDGEON_ORIENTATION | PASS_CAVEATED_SOURCE_CONTEXT | Inclination is 90 deg in the SPARC packet. This promotes observer/projection relevance, but not WVO by itself. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |
| U7151_G3_WVO_VERTICAL_WARP_ONSET | BLOCKED_NEGATIVE_OR_INSUFFICIENT_SOURCE_SUPPORT | The fastest located external source gives truncation/H I extent context rather than clean vertical/warp/onset support. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |
| U7151_G4_EXPDISK_WVO_PROSPECTIVE_REPLAY | BLOCKED_DO_NOT_SCORE_AS_WVO_ANALOGUE_YET | A source-native WVO/onset observable is missing. The galaxy can be retained as edge-on/truncation control or revisited if independent WVO evidence is acquired. | False | ugc07151_expdisk_wvo_source_preflight_not_endpoint |

## Interpretation

UGC07151 passes the fast regular-disk/orientation context: it is a high
inclination, quality-1 SPARC object with an exponential-disk family in the
projection queue. That is enough to keep it as an observer/projection
candidate.

It does not yet pass the WVO-specific gate. The quickest source-side check
found truncation/H I extent context rather than independent vertical-warp
or onset support. Therefore the honest fast route is not to score it as
an expdisk+WVO analogue now.

## Verdict

`UGC07151 is a useful edge-on/truncation control or source-reacquisition
target, but it is not yet the clean fresh expdisk+WVO holdout.`

## Next Finite Action

Either locate an independent source-native WVO/onset/vertical-overlay
observable for UGC07151, or move to the next candidate. If no such source
exists, preserve UGC07151 as a negative/quiet control rather than forcing
a WVO kernel.

## Disallowed Claims

- no endpoint score is run here
- no validation claim is made here
- edge-on orientation is not treated as WVO evidence by itself
- the NGC4013 residual shape is not used to promote UGC07151
