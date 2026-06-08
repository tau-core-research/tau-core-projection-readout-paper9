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

## arXiv Source Package

`arxiv_submission_source.zip` is generated from `paper9_submission_source/` and
excludes the rendered PDF and build byproducts.

## Scope

This is a candidate/control audit paper.  The next validation step is an
independent, predeclared projection-enriched catalogue test.
