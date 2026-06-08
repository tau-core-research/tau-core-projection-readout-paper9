# UGC12506 Observer/Path/Interloper Audit Gate

This source gate separates internal edge-on projection, source-native
H I envelope support, arm asymmetry, image-plane interlopers, and
foreground/path-object evidence. It does not score the rotation curve.

## Summary

| audit_status | galaxy | internal_projection_status | envelope_support_status | arm_asymmetry_status | image_interloper_status | foreground_path_status | recommended_kernel_revision | do_not_include | endpoint_scores_allowed | uses_vobs_or_residual | next_gate | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506_OBSERVER_PATH_INTERLOPER_AUDIT_COMPLETE_KERNEL_REVISION_REQUIRED | UGC12506 | SOURCE_SUPPORTED_STRONG | SOURCE_SUPPORTED_STRONG | SOURCE_SUPPORTED_CAVEATED | SOURCE_SUPPORTED_OVERLAY_CAVEAT | NOT_ESTABLISHED | K_edgeon_disk_integration + K_extended_hi_envelope + caveated K_arm_asymmetry_extent; photometric interloper as mask/caveat | foreground/path-object gravity kernel without new catalogue cone search | False | False | derive_ugc12506_edgeon_envelope_asymmetry_formula_shell | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |

## Evidence

| galaxy | evidence_id | evidence_class | source_id | line_range | source_statement | tau_core_readout_interpretation | evidence_status | kernel_role | uses_vobs_or_residual | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_OPI_E1_EDGEON_INTERNAL_PROJECTION | internal_disk_projection | UGC12506_HI_SRC1_HIGHMASS_VLA | 206-225, 666-675 | UGC12506 has high inclination near 86 deg; the velocity field is a poor rotation-velocity indicator and the PV/envelope method is required. | Strong observer/projection layer from line-of-sight integration through the galaxy's own disk. | SOURCE_SUPPORTED_STRONG | eligible_internal_projection_kernel_component | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_E2_HI_ENVELOPE_SUPPORT | source_native_morphology | UGC12506_HI_SRC1_HIGHMASS_VLA | 652-658, 800-811, 834-839 | The H I disk is traced beyond 60 kpc; UGC12506 is gas-rich, diffuse, stable over most of the disk, and has high spin lambda=0.15. | Strong source-native extended-envelope support component; should not be treated as a small context multiplier only. | SOURCE_SUPPORTED_STRONG | eligible_envelope_support_kernel_component | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_E3_ARM_ASYMMETRY | source_native_asymmetry | UGC12506_HI_SRC1_HIGHMASS_VLA | 676-681 | The approaching and receding sides differ in shape and length; one side is detectable to about 70 kpc and the other to about 50 kpc. | Source-supported lopsided/projection-asymmetry component; radial sign and weighting still need a source-side rule. | SOURCE_SUPPORTED_CAVEATED | eligible_asymmetry_kernel_component_with_caveat | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_E4_IMAGE_INTERLOPERS | image_plane_interloper | UGC12506_HI_SRC1_HIGHMASS_VLA | 659-661 | The optical image contains two interlopers not connected with UGC12506: an eastern star and a southern higher-redshift galaxy intersecting the image. | Photometric/morphology-overlay caveat for K_obs -> K_readout; not by itself a foreground path-gravity component. | SOURCE_SUPPORTED_OVERLAY_CAVEAT | mask_or_caveat_component_not_gravity_kernel | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_E5_FOREGROUND_PATH_OBJECT | foreground_path | UGC12506_HI_SRC1_HIGHMASS_VLA | 659-661 plus source context | The identified galaxy interloper is reported as higher redshift; no foreground massive object along the UGC12506 light path is established. | Do not add a foreground/path lens-like kernel from this evidence. A wider catalogue cone search would be required. | NOT_ESTABLISHED | blocked_foreground_path_kernel_component | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |

## Gates

| galaxy | gate_id | gate_status | evidence | kernel_decision | uses_vobs_or_residual | endpoint_scores_allowed | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | U12506_OPI_G1_INTERNAL_PROJECTION | PASS_STRONG | i=86 deg and PV/envelope method required | include_internal_edgeon_projection_component | False | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_G2_ENVELOPE_SUPPORT | PASS_STRONG | R_HI about 58 kpc, low-density stable H I, high spin lambda=0.15 | include_extended_hi_envelope_support_component | False | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_G3_ARM_ASYMMETRY | PASS_CAVEATED | approaching/receding arms differ in shape and detectable extent | include_asymmetry_component_only_with_source_side_weight_caveat | False | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_G4_IMAGE_INTERLOPER | PASS_CAVEATED | star and higher-redshift galaxy interlopers in optical image | treat_as_photometric_overlay_mask_or_label_caveat | False | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | U12506_OPI_G5_FOREGROUND_PATH | BLOCKED_NOT_ESTABLISHED | known galaxy interloper is higher redshift, not established foreground | do_not_include_foreground_path_kernel_without_new_catalogue_search | False | False | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |

## Component Plan

| galaxy | component_id | component_status | source_basis | allowed_role | blocked_role | claim_boundary |
| --- | --- | --- | --- | --- | --- | --- |
| UGC12506 | K_edgeon_disk_integration | SOURCE_SUPPORTED_NEXT_FORMULA_REQUIRED | high inclination and PV/envelope tracing requirement | principal projection kernel | none | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | K_extended_hi_envelope | SOURCE_SUPPORTED_NEXT_FORMULA_REQUIRED | large H I extent, diffuse stable gas, high spin | principal envelope support kernel | none | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | K_arm_asymmetry_extent | SOURCE_SUPPORTED_CAVEATED_NEXT_FORMULA_REQUIRED | approaching/receding extent difference | secondary asymmetry kernel | residual-selected sign or radial weight | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | M_photometric_interloper_mask | SOURCE_SUPPORTED_CAVEAT_NOT_GRAVITY_KERNEL | star and higher-redshift galaxy image-plane interlopers | K_obs -> K_readout mask/caveat | foreground/path gravity kernel | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |
| UGC12506 | K_foreground_path_object | BLOCKED_NOT_ESTABLISHED | no source-supported foreground object along path | none yet | full observer/path kernel contribution | ugc12506_observer_path_interloper_audit_source_gate_not_endpoint |

## Interpretation

UGC12506 has strong source evidence for internal observer/projection
effects from edge-on disk integration and for a large high-spin H I
envelope. It also has image-plane interlopers, but the source states
that they are not connected with UGC12506, and the identified galaxy is
at higher redshift. Therefore the interloper evidence should be used as
a photometric/morphology mask or caveat, not as a foreground/path gravity
kernel unless a new catalogue cone search establishes a foreground/path
object.
