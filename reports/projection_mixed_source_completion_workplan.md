# Projection/Mixed Source-Completion Workplan

**Doc class:** source-completion workplan

**Reader role:** Paper 9 endpoint/replay maintainer

**Status:** `PROJECTION_MIXED_SOURCE_COMPLETION_REQUIRED`

**Canonical parent:** `reports/projection_enriched_candidate_kernel_audit.md`

Canonical data artifact:

```text
data/derived/projection_mixed_source_completion_targets_v1.csv
```

## Purpose

This workplan turns the common kernel ledger into a Paper 9-specific next
action. It does not add endpoint scores. It identifies which source-side
tokens must be frozen before projection-enriched mixed kernels can be replayed
without leakage or double counting.

## Current Priority

The first runnable route is `K_projection_mixed`:

```text
present morphology handle
    + observer/path projection
    + source-frozen morphology-history phase
    -> mixed readout kernel
```

This is the most direct Paper 9 test of the central operational claim:
improving the source-side morphology/projection description should improve the
readout prediction without using the rotation residual to choose the kernel.

## Non-Overlap Discipline

Every active source token must be assigned to exactly one channel:

```text
morphology/history: Theta_morph
observer/path:      O_path or projection weights
clock/readout:      Xi_t
mass/closure:       beta_cl or envelope closure
```

If one source fact would support two channels, the route must either merge the
channels into one shared quotient contribution, add an independent
residual-blind source split, or keep the second channel diagnostic/control
only.

## Run Decision

Allowed next action:

```text
freeze source-token ledger
    -> choose one already-studied mixed/projection candidate
    -> replay with the predeclared mixed kernel
    -> compare against wrong-family controls
```

Blocked actions:

```text
do not promote Xi_t from warp/history evidence alone
do not alter amplitude from rotation residuals
do not choose radial windows from RMSE shape
```

## Claim Boundary

If the route passes after this source completion, the allowed claim is still:

```text
caveated endpoint candidate / source-frozen replay support
```

It is not population validation and not proof of a new gravitational law.

## First Case Ledger

The first concrete source-token ledger under this workplan is:

```text
reports/ngc4013_projection_mixed_nonoverlap_ledger.md
data/derived/ngc4013_projection_mixed_nonoverlap_ledger_v1.csv
data/derived/ngc4013_projection_mixed_nonoverlap_gates_v1.csv
```

It assigns NGC4013 warp, orientation, flare/scaleheight, lag, and extended
component evidence to a caveated WVO/mixed projection route and explicitly
blocks an independent `Xi_t` endpoint because no separate clock/readout source
token is currently available.

The corresponding replay-classification audit is:

```text
reports/ngc4013_projection_mixed_replay_classification.md
data/derived/ngc4013_projection_mixed_replay_classification_v1.csv
data/derived/ngc4013_projection_mixed_replay_classification_summary_v1.csv
```

It does not add a new score. It reclassifies the existing NGC4013 score ladder
under the non-overlap ledger: WVO/mixed replay is caveated-allowed, the
independent `Xi_t` route is blocked, and the expdisk+WVO score remains
prospective-only.

The follow-up morphology-completion audit is:

```text
reports/ngc4013_morphology_completion_pressure.md
data/derived/ngc4013_morphology_completion_pressure_summary_v1.csv
data/derived/ngc4013_morphology_completion_pressure_components_v1.csv
```

It records why the best wrong-family control (`K_exponential_disk`) should be
read as completion pressure for a mixed disk-carrier plus WVO readout, not as a
true negative against the Tau Core framework. The mixed expdisk+WVO route
remains prospective-only for NGC4013.
