# Reproducibility guide

## Deterministic examples

The example and smoke test set the random-number generator explicitly before
constructing arrays. They use no downloaded dataset, cached result, or local
configuration file.

## What the smoke test establishes

The test checks two invariants:

1. multiplying a t-scalar by `E_T(tsize)` returns the original t-scalar; and
2. multiplying the three t-SVD factors reconstructs a synthetic t-matrix to a
   relative error below `1e-10`.

These checks are intentionally small. They establish a reproducible baseline,
not a full numerical-validation campaign.

## What a larger study should record

For a report or benchmark, record at least:

- the exact repository commit;
- MATLAB release and operating system;
- t-scalar shape and matrix dimensions;
- random seed or dataset provenance;
- transform and normalization conventions;
- error metric and tolerance; and
- elapsed time together with hardware details when reporting performance.

## Numerical cautions

- Relative errors depend on conditioning and floating-point precision.
- Singular vectors may change sign or complex phase without changing the
  represented factorization.
- Repeated or tightly clustered singular values make individual singular
  vectors especially non-unique.
- A result suitable for exploratory research is not automatically suitable for
  safety-critical or high-impact use.
