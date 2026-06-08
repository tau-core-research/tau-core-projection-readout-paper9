# Projection Channel Taxonomy

This taxonomy summarizes the projection/readout channels used in Paper 2.

## Summary

| taxonomy_id | n_channels | main_message | time_projection_status | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| PAPER2_PROJECTION_CHANNEL_TAXONOMY_V1 | 6 | Paper 2 uses several projection/readout layers, but only source-frozen, non-overlapping channels can be endpoint-active. | control/diagnostic until independent clock evidence survives T/A | False | False | projection_channel_taxonomy_not_endpoint |

## Channels

| channel | meaning | paper2_use | example_galaxies | status | guardrail | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| present morphology readout | projected present-day source structure used to select the base morphology kernel | main operational layer | NGC4013, NGC7331, NGC5907, NGC4088, UGC12506 | endpoint-active where source-frozen; otherwise proxy/control | must be source-selected before scoring; not inferred from residuals | False | False | projection_channel_taxonomy_not_endpoint |
| observer/path projection | how the source is read from the observer's line of sight or path geometry | edge-on, line-of-sight warp, vertical overlay, PV/envelope visibility | NGC5907, NGC4013, NGC7331, UGC12506 | partly endpoint-active in mixed/projection routes | image-plane coincidence is insufficient; needs source/path support | False | False | projection_channel_taxonomy_not_endpoint |
| morphology-history / trajectory phase | source-side phase, disturbance, relaxation, or history state carried by morphology | warp/history and disturbed/asymmetric lanes | NGC4088, UGC12506, NGC7331 | endpoint-active only when source-frozen; otherwise caveated | future-directed wording is trajectory/phase, not backward causation | False | False | projection_channel_taxonomy_not_endpoint |
| time / clock readout projection | effective time-slice or clock-readout mismatch multiplying the velocity readout | diagnostic Xi_t replays and interval controls | NGC4088, UGC12506, NGC4013, NGC5907, NGC7331, NGC4183 | control/diagnostic only in this paper | requires independent clock/readout evidence and a nonzero T/A remainder | False | False | projection_channel_taxonomy_not_endpoint |
| path/environment projection | null-geodesic bundle and metric/matter environment affecting the observed light path | protocol/future full-kernel layer; path audits | UGC12506 path/interloper audit; NGC4088 path not primary | not endpoint-modeled in this paper | must affect the source-observer bundle; not every foreground object qualifies | False | False | projection_channel_taxonomy_not_endpoint |
| mass/envelope / closure readout | deeper source/envelope or closure channel not reducible to local 4D baryonic density alone | stress/development routes for high-spin/envelope or vertical-halo systems | UGC12506, NGC0891, NGC4217, IC4202 | mostly control/prospective in this paper | requires source-native carrier/amplitude freeze; not a curve-rescue term | False | False | projection_channel_taxonomy_not_endpoint |
