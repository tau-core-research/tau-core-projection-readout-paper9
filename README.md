# Tau Core Projection Readout Paper 9

This private repository contains Paper 9 in the Tau Core SPARC morphology/readout
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

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper9_submission_source/` and
excludes the rendered PDF and build byproducts.

## Scope

This is a candidate/control audit paper.  The next validation step is an
independent, predeclared projection-enriched catalogue test.
