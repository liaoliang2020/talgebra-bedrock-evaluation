# T-Algebra MATLAB Toolkit

[![Repository checks](https://github.com/liaoliang2020/talgebra-matlab-toolkit/actions/workflows/repository-checks.yml/badge.svg)](https://github.com/liaoliang2020/talgebra-matlab-toolkit/actions/workflows/repository-checks.yml)

T-Algebra MATLAB Toolkit is a compact research-software project for numerical
experiments with t-scalars, t-matrices, multidimensional Fourier transforms,
and spectral-slice matrix computations. The public tree deliberately starts
with a small, testable core so that the definitions and numerical assumptions
remain easy to inspect.

## Mathematical idea

A t-scalar is represented by an array whose leading dimensions have shape
`tsize`. Its product is multidimensional circular convolution. If
\(\mathcal F\) denotes the Fourier transform over the t-scalar dimensions,
then

\[
a \circ b = \mathcal F^{-1}\!\left(\mathcal F(a)\odot\mathcal F(b)\right).
\]

A t-matrix stores one t-scalar in each matrix entry. Fourier transformation
turns t-matrix multiplication and decomposition into independent ordinary
matrix operations on spectral slices. The included t-SVD follows exactly this
pattern: transform, compute an economy-size SVD on each slice, and transform
the factors back.

More detail is available in [the algorithm notes](docs/ALGORITHM_NOTES.md).

## Included core

- `tscalar/E_T.m`: multiplicative identity for the t-scalar convolution;
- `tscalar/tproduct.m`: t-scalar product;
- `tmatrix/tmultiplication.m`: t-matrix multiplication;
- `tmatrix/tctranspose.m`: conjugate transpose of a t-matrix;
- `tmatrix/tsvd.m`: spectral-slice t-SVD;
- `examples/quickstart_tsvd.m`: deterministic reconstruction example; and
- `tests/run_smoke_tests.m`: identity and reconstruction checks.

## Quick start

Clone the repository and start MATLAB in the project directory:

```bash
git clone https://github.com/liaoliang2020/talgebra-matlab-toolkit.git
cd talgebra-matlab-toolkit
```

Then run:

```matlab
run("examples/quickstart_tsvd.m")
run("tests/run_smoke_tests.m")
```

Both scripts generate deterministic synthetic arrays. They do not download a
dataset or require a bundled data file.

## Requirements

- MATLAB R2021a or later is recommended;
- base functions including `fftn`, `ifftn`, `fft`, `ifft`, and `svd`; and
- Python 3.10 or later only for the repository-content safety check.

No add-on toolbox is required by the included core.

## Reproducibility and scope

The smoke test verifies the t-scalar identity and checks that a synthetic
t-matrix is reconstructed from its t-SVD to a relative error below
\(10^{-10}\). Continuous integration runs the same test on a hosted MATLAB
environment and scans the public tree for credential-like or identifying
material.

This repository is a research prototype, not a production numerical library.
It currently focuses on correctness and inspectability rather than exhaustive
input handling, performance benchmarking, or safety-critical use. See
[the reproducibility guide](docs/REPRODUCIBILITY.md) before interpreting
experimental results.

## Privacy and security

The public tree contains only source code, documentation, and synthetic tests.
Do not commit credentials, personal contact details, unpublished manuscripts,
restricted datasets, local paths, or binary archives. Run the following before
publishing a change:

```bash
python tools/check_public_tree.py
```

See [SECURITY.md](SECURITY.md) for private vulnerability reporting and
credential-response guidance.

## License and citation

Project source is released under the [MIT License](LICENSE). Cite the exact
revision used in a numerical experiment; a neutral software citation is
provided in [CITATION.cff](CITATION.cff).
