# UGC12506 HIghMass Fast Source Context

This acquisition cache records residual-blind source context for UGC12506
from Hallenbeck et al. 2014.  It supports a projection-enriched/high-spin
candidate route, but does not freeze a Tau Core formula and does not score
an endpoint.

## Summary

| context_status | galaxy | source_cached | text_extracted | n_evidence_rows | supports_projection_context | supports_outer_hi_context | supports_closure_stability_context | supports_history_memory_context | formula_freeze_allowed | endpoint_scores_allowed | uses_vobs_or_residual_in_acquisition | recommended_next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_HIGHMASS_FAST_SOURCE_CONTEXT_CACHED_FORMULA_VALUES_OPEN | UGC12506 | True | True | 5 | True | True | True | True | False | False | False | build_ugc12506_projection_highspin_formula_preflight_from_source_context | ugc12506_highmass_fast_source_context_not_kernel_freeze |

## Source

| galaxy | source_id | source_name | source_url | pdf_url | doi | local_pdf | local_text | source_status | machine_readable_text | machine_readable_radial_profile | residual_blind | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_HI_SRC1_HIGHMASS_VLA | Hallenbeck et al. 2014 HIghMass VLA imaging | https://arxiv.org/abs/1407.1744 | https://arxiv.org/pdf/1407.1744 | 10.1088/0004-6256/148/4/69 | data/external/literature/ugc12506_highmass_hi_context/hallenbeck_2014_highmass_ugc12506.pdf | data/external/literature/ugc12506_highmass_hi_context/hallenbeck_2014_highmass_ugc12506.txt | CACHED_AND_TEXT_EXTRACTED | True | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |

## Evidence

| galaxy | evidence_id | source_id | evidence_type | text_line_range | paraphrased_evidence | supports_field | freezes_kernel_value | residual_blind | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | UGC12506_HM_E1_HIGH_INCLINATION_PV_REQUIRED | UGC12506_HI_SRC1_HIGHMASS_VLA | projection_context | 206-225,681-690 | The galaxy is highly inclined, so velocity-field curves underestimate rotation and the authors use a position-velocity/envelope method. | projection_enriched_kernel_candidate | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | UGC12506_HM_E2_EXTENDED_HI_SUPPORT | UGC12506_HI_SRC1_HIGHMASS_VLA | hi_extent_context | 666-673 | The H I disk is traced beyond 60 kpc and the observed H I radius is reported as 58 +/- 2 kpc, consistent with the expected radius. | outer_support_window | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | UGC12506_HM_E3_ORDERED_BUT_ASYMMETRIC_PV | UGC12506_HI_SRC1_HIGHMASS_VLA | projection_asymmetry_context | 680-696 | The galaxy shows ordered rotation to the detectable edge, but the approaching and receding sides differ in shape and length. | projection_or_lopsided_support_context | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | UGC12506_HM_E4_LOW_DENSITY_STABLE_HI | UGC12506_HI_SRC1_HIGHMASS_VLA | closure_stability_context | 719-735 | UGC12506 has low H I surface densities, typically 1-5 Msun/pc^2 out to 60 kpc, and is described as stable over most of the disk. | closure_load_context | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | UGC12506_HM_E5_HIGH_SPIN_CONTEXT | UGC12506_HI_SRC1_HIGHMASS_VLA | history_memory_context | 768-774 | The paper reports a very high spin parameter for UGC12506, interpreted as an unusual gas-rich high-spin state. | memory_history_or_high_spin_context | False | True | ugc12506_highmass_fast_source_context_not_kernel_freeze |

## Candidate Fields

| galaxy | candidate_field | field_status | source_basis | why_open | uses_vobs_or_residual | formula_freeze_allowed | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | projection_load_from_high_inclination_pv | CONTEXT_SUPPORTED_VALUES_OPEN | high-inclination PV/envelope-tracing method | no predeclared normalized e_proj value has been extracted | False | False | False | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | outer_hi_support_window | NUMERIC_CONTEXT_AVAILABLE_NOT_FORMULA_FREEZE | H I traced beyond 60 kpc; observed H I radius 58 +/- 2 kpc in source | needs mapping into a kernel window and amplitude rule | False | False | False | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | closure_stability_load | CONTEXT_SUPPORTED_VALUES_OPEN | low density stable H I disk, stability thresholds discussed | no normalized z_cl(R) field is frozen | False | False | False | ugc12506_highmass_fast_source_context_not_kernel_freeze |
| UGC12506 | history_memory_high_spin_load | CONTEXT_SUPPORTED_VALUES_OPEN | reported high spin parameter lambda=0.15 | needs residual-blind Tau-side mapping before use in a kernel | False | False | False | ugc12506_highmass_fast_source_context_not_kernel_freeze |

## Claim Boundary

The source provides strong context for high-inclination projection, extended
H I support, low-density stable gas, and high-spin/history interpretation.
It does not by itself freeze `e_proj`, `z_cl(R)`, a kernel amplitude, or an
endpoint-ready formula.
