% QUICKSTART_TSVD  Synthetic t-SVD reconstruction example.

original_path = path;
path_cleanup = onCleanup(@() path(original_path)); %#ok<NASGU>
repo_root = fileparts(fileparts(mfilename('fullpath')));
addpath(fullfile(repo_root, 'tscalar'));
addpath(fullfile(repo_root, 'tmatrix'));

rng(7, 'twister');
tsize = [2, 2];
A = randn([tsize, 3, 2]);

[TU, TS, TV] = tsvd(A, tsize);
A_reconstructed = tmultiplication( ...
    tmultiplication(TU, TS, tsize), ...
    tctranspose(TV, tsize), ...
    tsize);

relative_error = norm(A(:) - A_reconstructed(:)) / max(norm(A(:)), eps);
fprintf('Relative t-SVD reconstruction error: %.3e\n', relative_error);
assert(relative_error < 1e-10, 'Unexpected t-SVD reconstruction error.');
