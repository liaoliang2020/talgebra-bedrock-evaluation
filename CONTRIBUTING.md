# Contributing

Contributions should keep this repository small, reproducible, and suitable
for public mathematical-software review.

## Before opening a change

1. Use original source or dependencies whose redistribution terms are clear.
2. Use deterministic synthetic data in examples and tests.
3. Do not add papers, webpage archives, third-party toolboxes, private data,
   credentials, local paths, or compressed binary bundles.
4. Document array dimensions, mathematical assumptions, and numerical
   tolerances.
5. Add a regression case when correcting an algorithm.
6. Run the repository checker and MATLAB smoke tests.

## Coding guidance

- Keep one public function per `.m` file and match the file name to the
  function name.
- Avoid silently changing transform normalization or dimension ordering.
- Prefer small, explicit spectral-slice loops until a vectorized version has
  an equivalent regression test.
- State any add-on toolbox requirement in both the function header and README.

## Local checks

```bash
python tools/check_public_tree.py
```

```matlab
run("tests/run_smoke_tests.m")
```

By contributing original material, you agree that it may be distributed under
the repository's MIT License. Do not submit material that you do not have the
right to redistribute.
