function [TU, TS, TV] = tsvd(array, tsize)
%TSVD Compute a t-matrix SVD through independent spectral-slice SVDs.

    assert(isa(array, 'double'), ...
        'T-Algebra:Type', 'Input must be a double array.');
    validateattributes(tsize, {'numeric'}, ...
        {'vector', 'integer', 'positive', 'finite', 'real'});
    tsize = double(tsize(:).');

    tdim = numel(tsize);
    array_size = size(array);
    array_size(end + 1:tdim + 2) = 1;
    assert(isequal(array_size(1:tdim), tsize), ...
        'T-Algebra:TShape', ...
        'Leading array dimensions must equal tsize.');
    rows = array_size(tdim + 1);
    columns = array_size(tdim + 2);

    array_hat = reshape(array, [tsize, rows, columns]);
    for dim = 1:tdim
        array_hat = fft(array_hat, [], dim);
    end
    array_hat = reshape(array_hat, prod(tsize), rows, columns);

    for index = 1:prod(tsize)
        slice = reshape(array_hat(index, :, :), rows, columns);
        [U_slice, S_slice, V_slice] = svd(slice, 'econ');
        if index == 1
            U_hat = zeros([prod(tsize), size(U_slice)], 'like', U_slice);
            S_hat = zeros([prod(tsize), size(S_slice)], 'like', S_slice);
            V_hat = zeros([prod(tsize), size(V_slice)], 'like', V_slice);
        end
        U_hat(index, :, :) = U_slice;
        S_hat(index, :, :) = S_slice;
        V_hat(index, :, :) = V_slice;
    end

    TU = reshape(U_hat, [tsize, size(U_hat, 2), size(U_hat, 3)]);
    TS = reshape(S_hat, [tsize, size(S_hat, 2), size(S_hat, 3)]);
    TV = reshape(V_hat, [tsize, size(V_hat, 2), size(V_hat, 3)]);

    for dim = 1:tdim
        TU = ifft(TU, [], dim);
        TS = ifft(TS, [], dim);
        TV = ifft(TV, [], dim);
    end
end
