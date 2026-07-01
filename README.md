# Tau Core Projection Readout Paper 9

This public repository contains Paper 9 in the Tau Core SPARC morphology/readout
sequence.

## Main Claim

The paper defines a source-frozen candidate/control audit for projection,
time-readout, and closure-control kernels in SPARC galaxies.  It asks whether
projection-enriched readout layers can be specified before endpoint residuals
are inspected.

## Does Not Claim

- It does not validate a new population-level gravitational law.
- It does not count UGC12506 as a validation case.
- It does not treat the post-diagnostic \(\beta_{\rm cl}\) expression as
  evidence on UGC12506.
- It does not claim that the path/environment term is modeled or scored.
- It does not claim that every source-frozen projection kernel is already a
  Tau-side derived source.

## Source-Grounding Boundary

Paper 9 uses source-frozen projection, morphology-history, time-readout, and
closure-control kernels. A source-frozen kernel is allowed into the audit only
because its inputs are fixed before endpoint residuals are inspected. That is a
leakage-prevention condition, not a full Tau Core derivation.

The stronger source-grounding gate is projection induction: a channel can be
promoted from operational proxy to Tau-side induced source only if a Tau-side
mode is activated, survives the null/gauge quotient, remains stable under the
closure test, and survives the 4D readout map. Schematically:

```text
O_i^4D = R_i^4D( Pi_stab([A_tau(u)]) )
```

This paper treats that gate as a claim boundary. Its candidate/control results
motivate which channels should be grounded next; they do not by themselves
prove the source-grounding derivation.

The current theory update also adds a source-factored non-double-counting
discipline. Operationally:

```text
K_i(s0) = Ktilde_i(M_tau^stab)
t_obs^gal = R_time^{obs,gal}(M_tau^stab, OI_gal, o_path^gal)
one protected source coordinate -> one quotient contribution
```

Every projection, morphology-history, and time-readout component must declare
`SourceSupp(Delta K_a)`. If two components reuse the same source/proxy
coordinate, they must be merged into one shared quotient term, separated by an
independent residual-blind source split, or retained only as diagnostic/control
curves. This is why some lower-RMSE time/projection replays remain blocked.

## Included Data

The repository currently includes the manuscript source, rendered PDF, figures
embedded in the paper source tree, and minimal reproducibility scripts.  Larger
shared source-review ledgers and reusable morphology/readout infrastructure are
kept in the common repository:

`tau-core-morphology-readout-common`

## Reproduce

```bash
python scripts/reproduce.py
```

This compiles the manuscript, builds the arXiv source package, and runs the
smoke tests.

The reproduction script fixes `SOURCE_DATE_EPOCH` for the TeX build, and the
arXiv ZIP builder writes deterministic archive timestamps.  The package is
still a source-level reproducibility target: rendered PDFs can vary slightly
across TeX engines or local font stacks, but the smoke tests and generated
source package should remain stable for the committed inputs.

### Online Data Dependencies

The one-command reproduction path:

```bash
python scripts/reproduce.py
```

does not perform live online data acquisition.  It compiles the manuscript,
builds the arXiv ZIP, and runs smoke tests against committed inputs.

Several optional source-acquisition/provenance scripts do reference external
resources and may require network access when run manually, for example:

- `scripts/acquire_ugc12506_beta_closure_transfer_halo_fit_fields.py`
  reads/caches the Li et al. SPARC halo-model table from VizieR.
- `scripts/acquire_ugc12506_highmass_fast_source_context.py` expects the
  cached UGC12506 HIghMass context PDF derived from arXiv source context.
- `scripts/acquire_ugc12506_beta_closure_direct_lambda_spin_sources.py` and
  `scripts/acquire_ugc12506_beta_closure_ngc0891_spin_source_hunt_update.py`
  record external source-review routes rather than endpoint scores.

Those optional scripts are provenance/source-review helpers.  They are not
called by `scripts/reproduce.py`, and a failure to reach an external service
does not affect the committed Paper 9 smoke-test reproduction.

## Current Source-Completion Workplan

The current replay-facing source-completion workplan is:

```text
reports/projection_mixed_source_completion_workplan.md
data/derived/projection_mixed_source_completion_targets_v1.csv
```

It ranks the projection/mixed routes that can be advanced next and records the
source-token non-overlap requirements that must be satisfied before additional
endpoint-style replay is allowed.

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper9_submission_source/` and
excludes the rendered PDF and build byproducts.

## Zenodo Publication Status

This public repository is Zenodo-ready for version `v0.1.1`:

```text
.zenodo.json
CITATION.cff
LICENSE
arxiv_submission_source.zip
paper9_submission_source/main.pdf
```

The repository is public and carries `.zenodo.json` plus `CITATION.cff`.
Automatic DOI minting still requires enabling the repository in the Zenodo
GitHub integration before creating or reprocessing a GitHub release. If the
integration is not enabled, the same release package can be uploaded manually
or through the Zenodo API with this metadata.

## Scope

This is a candidate/control audit paper.  The next validation step is an
independent, predeclared projection-enriched catalogue test.
