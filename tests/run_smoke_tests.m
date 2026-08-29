% RUN_SMOKE_TESTS  Deterministic checks for the public numerical core.

original_path = path;
path_cleanup = onCleanup(@() path(original_path)); %#ok<NASGU>
repo_root = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(repo_root, 'tscalar'));
addpath(fullfile(repo_root, 'tmatrix'));

rng(11, 'twister');
tsize = [2, 2];

scalar_value = randn(tsize);
identity_value = E_T(tsize);
product_value = tproduct(scalar_value, identity_value);
identity_error = norm(product_value(:) - scalar_value(:));
assert(identity_error < 1e-10, 'The t-scalar identity check failed.');

one_dimensional_size = 3;
one_dimensional_value = randn(one_dimensional_size, 1);
one_dimensional_identity = E_T(one_dimensional_size);
one_dimensional_product = tproduct( ...
    one_dimensional_value, one_dimensional_identity);
one_dimensional_error = norm( ...
    one_dimensional_product(:) - one_dimensional_value(:));
assert(one_dimensional_error < 1e-10, ...
    'The one-dimensional t-scalar identity check failed.');

matrix_shapes = [3, 2; 2, 3];
reconstruction_error = 0;
for shape_index = 1:size(matrix_shapes, 1)
    rows = matrix_shapes(shape_index, 1);
    columns = matrix_shapes(shape_index, 2);
    A = randn([tsize, rows, columns]);
    [TU, TS, TV] = tsvd(A, tsize);
    A_reconstructed = tmultiplication( ...
        tmultiplication(TU, TS, tsize), ...
        tctranspose(TV, tsize), ...
        tsize);
    current_error = norm(A(:) - A_reconstructed(:)) / ...
        max(norm(A(:)), eps);
    reconstruction_error = max(reconstruction_error, current_error);
end
assert(reconstruction_error < 1e-10, ...
    'A t-SVD reconstruction check failed.');

fprintf(['T-Algebra smoke tests passed. Identity errors: %.3e and %.3e; ', ...
    'maximum reconstruction error: %.3e\n'], identity_error, ...
    one_dimensional_error, reconstruction_error);
