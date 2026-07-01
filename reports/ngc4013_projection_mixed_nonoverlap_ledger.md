# NGC4013 Projection/Mixed Non-Overlap Ledger

**Doc class:** source-token non-overlap ledger

**Reader role:** Paper 9 projection/mixed replay maintainer

**Status:** `NGC4013_WVO_MIXED_REPLAY_CAVEATED_ALLOWED_XIT_BLOCKED`

**Canonical parent:** `reports/projection_mixed_source_completion_workplan.md`

Canonical artifacts:

```text
data/derived/ngc4013_projection_mixed_nonoverlap_ledger_v1.csv
data/derived/ngc4013_projection_mixed_nonoverlap_gates_v1.csv
```

## Purpose

This ledger freezes how the source-side NGC4013 evidence may be used before
any additional projection/mixed replay. It does not add a new endpoint score
and does not turn previous diagnostic scores into validation. Its only job is
to prevent the same source facts from being counted twice across
morphology/history, observer/path, vertical-overlay, and clock/readout
channels.

## Source Assignment

The accepted source-side facts are assigned as follows:

| Source token | Allowed role | Blocked reuse |
| --- | --- | --- |
| line-of-sight warp onset and strength | WVO radial window and projection context | independent `Xi_t` clock evidence |
| warp orientation | observer/path orientation caveat | amplitude or clock factor |
| H I scaleheight / flare | vertical-overlay shape | independent time/readout correction |
| radial lag profile | vertical kinematic structure inside WVO | clock route without separate clock proxy |
| extended stellar component | cross-check for vertical-overlay plausibility | second vertical amplitude channel |
| exponential disk carrier | prospective expdisk+WVO protocol context | retroactive endpoint validation |

## Decision

The WVO/mixed projection route is source-supported enough for a caveated replay
reading:

```text
N4013_NONOVERLAP_G2_WVO_MIXED_ROUTE = PASS_CAVEATED_REPLAY_ALLOWED
```

The clock/time-readout route remains blocked:

```text
N4013_NONOVERLAP_G3_XIT_CLOCK_ROUTE = BLOCKED
```

The reason is straightforward: the currently available NGC4013 source facts
are warp, vertical structure, orientation, flare/scaleheight, and lag facts.
Those are exactly the facts needed by the WVO/mixed projection route. They are
not independent evidence for a separate `Xi_t` channel.

## Relation To Existing Scores

The previous score ladder remains:

```text
compact proxy -> WVO -> expdisk+WVO protocol
```

The non-overlap ledger strengthens the interpretation of the WVO route as a
source-supported mixed projection route. It does not retroactively promote the
stronger expdisk+WVO protocol score to endpoint validation. That route remains:

```text
PROSPECTIVE_ONLY
```

## Claim Boundary

Allowed after this ledger:

```text
caveated source-frozen WVO mixed-projection replay/control interpretation
```

Not allowed:

```text
population validation
retroactive validation of expdisk+WVO
independent Xi_t endpoint
new gravitational-law claim
```

## Next Finite Action

The next executable action is to rerun or summarize the NGC4013 WVO replay
under this source-token assignment and compare only against predeclared
wrong-family controls. If a future expdisk+WVO test is wanted, it should be a
prospective replay on a holdout or uninspected analogue, not retroactive
promotion of the existing score.
