# Beta-Transfer Negative Trigger Lock-Type Source Review

This review asks what kind of lock the negative beta-transfer galaxies appear to be from source morphology alone.
It does not use rotation residuals to choose a replacement readout.

## Verdict

| galaxy | previous_proxy_family | lock_type_verdict | source_supported_lock_type | readout_lane_pressure | why_not_curve_fitting | required_next_sources | replay_allowed_now | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NGC0891 | K_compact_finite | SOURCE_REJECTS_PURE_BETA_COMPACT_AS_PRIMARY_LOCK | K_edgeon_vertical_dust_hi_halo_mixed | projection/vertical overlay plus H I halo/history component before any beta-transfer replay | classification follows edge-on/dust/H I halo literature, not endpoint residual shape | source-native vertical dust/halo support window; H I halo/load profile; bulge/disk split if compact lane is retained as subcomponent | False | False | beta_transfer_lock_type_source_review_residual_blind_not_replay |
| NGC4217 | K_compact_finite | SOURCE_REJECTS_PURE_BETA_COMPACT_AS_PRIMARY_LOCK | K_edgeon_vertical_dust_radio_halo_mixed | projection/vertical dust overlay with halo/radio-bubble context; compact lane may only be a component | classification follows edge-on/extraplanar dust/radio halo source evidence, not endpoint score | vertical dust extent/window; S4G/NED bulge-disk decomposition; H I or radio-halo support context | False | False | beta_transfer_lock_type_source_review_residual_blind_not_replay |

## Evidence Ledger

| galaxy | source_id | source_url | residual_blind_field | supports_lock_component | source_strength |
| --- | --- | --- | --- | --- | --- |
| NGC0891 | NASA_HUBBLE_NGC891_EDGE_ON_DUST_GAS | https://science.nasa.gov/missions/hubble/hubble-spies-edge-on-beauty/ | edge_on_dust_gas_halo_filaments | observer_projection;vertical_dust_gas_overlay;halo_fountain | HIGH |
| NGC0891 | HOWK_SAVAGE_1997_EXTRAPLANAR_DUST | https://arxiv.org/abs/astro-ph/9709197 | extraplanar_dust_massive_high_z_structures | vertical_dust_overlay;thick_disk_halo_source | HIGH |
| NGC0891 | MOUHCINE_REJKUBA_IBATA_2009_NGC891_STRUCTURE | https://academic.oup.com/mnras/article/395/1/126/1079019 | edge_on_disc_halo_hi_halo_structural_complexity | hi_halo;thick_disc_halo;history_or_accretion_context | HIGH |
| NGC4217 | ESA_HUBBLE_NGC4217_DUST_FILAMENTS | https://esahubble.org/images/potw1503a/ | edge_on_extraplanar_dust_filaments | observer_projection;vertical_dust_gas_overlay | HIGH |
| NGC4217 | ESA_HUBBLE_NGC4217_FILAMENT_GEOMETRY | https://esahubble.org/images/potw1503a/ | dust_filament_heights_and_shapes | vertical_overlay;outflow_or_fountain_geometry | HIGH |
| NGC4217 | CHANGES_2024_NGC4217_RADIO_BUBBLE | https://arxiv.org/abs/2409.15449 | extra_planar_radio_halo_bubble | halo_bubble;magnetic_or_cosmic_ray_projection_context | MEDIUM_HIGH |

## Claim Boundary

- Pure beta/compact transfer is rejected as the primary lock type for these negative-trigger cases.
- This is a source-side morphology/readout review, not a replay and not endpoint validation.
- Any new scoring run must first freeze a replacement formula from source-native fields.
- Forbidden inputs remain rotation residuals, endpoint RMSE, wrong-family ranks, required-S diagnostics, and posthoc kernel tuning.
