# Beta-transfer Source-Side Morphology Review Gate

This gate prevents the beta-transfer control score from becoming a curve-fitting selector.
Scores can trigger review, but they cannot choose the morphology/readout family.

## Summary

| review_gate_status | n_galaxies | n_negative_score_triggers | n_weak_or_neutral_triggers | n_positive_control_signals | n_review_targets | uses_vobs_or_residual_for_family_choice | scores_used_only_as_audit_trigger | endpoint_scores_allowed | endpoint_validation_claim | next_action | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BETA_TRANSFER_SOURCE_SIDE_MORPHOLOGY_REVIEW_GATE_BUILT_NO_REPLAY | 11 | 2 | 2 | 7 | 4 | False | True | False | False | run independent residual-blind morphology/source review for negative and weak triggers; only then freeze replacement labels and replay | beta_transfer_source_side_morphology_review_gate_not_endpoint |

## Review Queue

| galaxy | score_trigger_status | delta_carrier_minus_beta_km_s | current_proxy_family | source_side_review_target | source_review_status | needed_residual_blind_sources |
| --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | NEGATIVE_SCORE_TRIGGER_REVIEW_ONLY | -30.1919 | K_compact_finite | K_edgeon_compact_vertical_overlay_or_bulge_split | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED bulge-disk decomposition; vertical/dust-lane evidence; H I extent/asymmetry if available |
| NGC4217 | NEGATIVE_SCORE_TRIGGER_REVIEW_ONLY | -7.37854 | K_compact_finite | K_edgeon_compact_vertical_overlay_or_bulge_split | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED bulge-disk decomposition; vertical/dust-lane evidence; H I extent/asymmetry if available |
| NGC2841 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 6.09058 | K_compact_finite | K_beta_transfer_compatibility_review | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | spin route provenance; carrier provenance; external morphology source cross-check |
| NGC4157 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 16.7211 | K_thick_flared | K_thick_flared_or_projection_dominated | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED vertical morphology notes; DustPedia/HI support; optional path/projection caveat |
| NGC0801 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 19.046 | K_thick_flared | K_thick_flared_or_projection_dominated | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED vertical morphology notes; DustPedia/HI support; optional path/projection caveat |
| UGC11455 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 20.5667 | K_exponential_disk | K_beta_transfer_compatibility_review | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | spin route provenance; carrier provenance; external morphology source cross-check |
| NGC4013 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 30.8201 | K_compact_finite | K_beta_transfer_compatibility_review | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | spin route provenance; carrier provenance; external morphology source cross-check |
| ESO563-G021 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 35.5945 | K_thick_flared | K_thick_flared_or_projection_dominated | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED vertical morphology notes; DustPedia/HI support; optional path/projection caveat |
| IC4202 | POSITIVE_CONTROL_SIGNAL_REQUIRES_SOURCE_CONFIRMATION | 41.7992 | K_compact_finite | K_edgeon_compact_vertical_overlay_or_bulge_split | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | S4G/NED bulge-disk decomposition; vertical/dust-lane evidence; H I extent/asymmetry if available |
| NGC3521 | WEAK_OR_NEUTRAL_SCORE_TRIGGER_REVIEW_ONLY | 0 | K_thick_flared | K_distance_caveated_control_only | BLOCKED_DISTANCE_OR_PROVENANCE_REVIEW | NED distance provenance; SPARC distance uncertainty review; do not endpoint-score as clean case |
| NGC7331 | WEAK_OR_NEUTRAL_SCORE_TRIGGER_REVIEW_ONLY | 3.01281 | K_thick_flared | K_beta_transfer_compatibility_review | REVIEW_REQUIRED_SOURCE_SIDE_NO_REPLAY | spin route provenance; carrier provenance; external morphology source cross-check |

## Claim Boundary

- This is not endpoint validation.
- Negative beta-transfer cases are preserved as diagnostic triggers.
- Any replacement label must be source-frozen from residual-blind evidence before replay.
- Forbidden for review: rotation residuals, endpoint RMSE, wrong-family ranks, required-S diagnostics, and posthoc amplitude/sign/radial-window tuning.
