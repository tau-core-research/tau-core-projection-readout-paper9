# Paper 9 KernelRecord Status Audit

**Doc class:** paper-level projection-kernel status audit
**Reader role:** reproducibility / claim-boundary reviewer
**Status:** audit map only; not endpoint scoring; not validation
**Canonical theory schema:** `KernelRecord_tau^S`

Paper 9 extends Paper 8 by adding observer/path, history, time/clock, and
envelope/closure projection layers.  Under the current Tau Core kernel
discipline, projection enrichment is allowed only when the added component has
source support that is not already consumed by the base morphology kernel.

## Projection Channels

| channel | Paper 9 role | KernelRecord status | source support rule | endpoint boundary |
| --- | --- | --- | --- | --- |
| present morphology readout | base kernel selection | endpoint-active where source-frozen; otherwise source-proxy | source-selected before scoring | not inferred from residuals |
| observer/path projection | line-of-sight, edge-on, vertical overlay, path visibility | partly endpoint-active in mixed/projection routes | requires explicit source/path support | not every visual coincidence is a path term |
| morphology-history / trajectory phase | disturbance, warp, relaxation, asymmetry | endpoint-active only when source-frozen | history evidence belongs to morphology unless independent clock support exists | future-directed language is phase/readout, not backward causation |
| time / clock readout projection | effective clock/readout mismatch | diagnostic/control in this paper | requires independent clock evidence and non-overlap with morphology/history support | not endpoint-active from warp inputs alone |
| path/environment projection | null-geodesic bundle and metric/matter environment | future full-kernel layer | must affect source-observer bundle | not population-modeled here |
| mass/envelope / closure readout | deeper envelope/closure channel | mostly control/prospective | source-native carrier/amplitude freeze required | not a curve-rescue term |

## Candidate Projection-Enriched Kernels

| galaxy / lane | status | source quotient | source support | overlap decision | result role |
| --- | --- | --- | --- | --- | --- |
| NGC5907 projection / vertical-warp context | accepted mixed endpoint-active single-object kernel | `Q_src^P` projection and edge-on source manifest | line-of-sight/projection support | allowed as projection-enriched route; strict wrong-label margin remains thin | fresh projection-enriched freeze target, not population validation |
| NGC7331 exponential / vertical / outer-warp overlay | caveated accepted mixed endpoint-active kernel | `Q_src^P` mixed source support | outer-warp/vertical support broad-window caveated | allowed but caveated | useful accepted mixed route, not final validation |
| NGC4013 exponential / warp / vertical overlay | caveated mixed-reference kernel | `Q_src^P` mixed support | mixed overlay not fully independent | proof-of-concept / retrospective caveated case | not fresh holdout validation |
| NGC4088 warp/history/asymmetric projection | caveated accepted single-object route | `Q_src^P` warp/history source support | time/clock overlap resolved by setting orthogonal clock residual to zero | visually strong control endpoint | law-level and normalization caveats remain |
| UGC12506 beta-closure / envelope transfer | control-only source-frozen transfer route | `Q_src^P` spin/envelope/closure proxies | source-side spin route and carrier accepted as caveated controls | endpoint validation explicitly false | stress / development route |

## Non-Double-Counting Rule In Paper 9

The NGC4088 double-count resolution is the model example:

```text
warp geometry, radial onset, q_warp, and morphology-history phase
already feed the additive warp/history kernel.

Therefore Xi_eff clock terms built from the same source tokens are not
orthogonal time-projection evidence.
```

The accepted combined endpoint route is:

```text
additive warp/history only, with Xi_eff = 1,
until independent non-overlap clock evidence exists.
```

This is exactly the paper-level version of the theory-side rule:

```text
same source/proxy coordinate cannot support two separately counted
kernel components unless an explicit overlap decision merges, splits,
or demotes the components.
```

## KernelRecord Verdict

Paper 9 currently supports this status:

```text
PAPER9_PROJECTION_READOUT =
    projection-enriched kernel-development evidence
    with several endpoint-active single-object/caveated routes,
    a strict non-double-counting rule,
    and no population validation of a final path-aware Tau Core kernel.
```

The strongest methodological gain is not a new universal correction term.  It
is the source-support discipline saying when a projection/time/path/envelope
component may be counted as a distinct readout channel.
