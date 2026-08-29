# Algorithm notes

## 1. T-scalars

Fix a shape

\[
\mathbf n=(n_1,\ldots,n_d).
\]

A t-scalar is stored as a complex or real array of that shape. Addition is
entrywise. Multiplication is multidimensional circular convolution. Writing
\(\widehat a=\mathcal F(a)\) for the discrete Fourier transform over all
\(d\) t-scalar dimensions gives

\[
\widehat{a\circ b}=\widehat a\odot\widehat b.
\]

The identity is the array whose first entry is one and whose remaining entries
are zero. `E_T` constructs this array, and `tproduct` implements the product
with `fftn` and `ifftn`.

## 2. T-matrices and spectral slices

An \(m\)-by-\(n\) t-matrix is stored as an array with size

```text
[n1, ..., nd, m, n].
```

After Fourier transformation over the first \(d\) dimensions, the array can be
viewed as \(n_1\cdots n_d\) ordinary complex matrices. These are the spectral
slices. If \(A\) and \(B\) have compatible matrix dimensions, their product is
computed independently on every slice:

\[
\widehat C_k=\widehat A_k\widehat B_k.
\]

The inverse transform of the collection \(\{\widehat C_k\}\) is the t-matrix
product. No slice communicates with another during the matrix-multiplication
stage.

## 3. T-SVD

For each spectral slice, compute the ordinary economy-size decomposition

\[
\widehat A_k=U_k S_k V_k^*.
\]

Place the factors back into spectral arrays and invert the Fourier transforms.
The result satisfies

\[
A=U\circ S\circ V^*,
\]

up to floating-point error. Singular vectors are not unique when singular
values repeat, so factor arrays may differ between software releases even when
the reconstruction and singular values agree.

## 4. Scope of the implementation

The current core favors direct loops over spectral slices because they make the
algebraic correspondence visible. Future vectorization should preserve:

- the order of the leading t-scalar dimensions;
- the transform normalization used by MATLAB;
- conjugate-transpose behavior in every spectral slice; and
- the reconstruction tolerance exercised by the smoke test.
