function result = tctranspose(array, tsize)
%TCTRANSPOSE Conjugate-transpose each spectral slice of a t-matrix.

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
        transposed_slice = slice';
        if index == 1
            result_hat = zeros([prod(tsize), columns, rows], ...
                'like', transposed_slice);
        end
        result_hat(index, :, :) = transposed_slice;
    end

    result = reshape(result_hat, [tsize, columns, rows]);
    for dim = 1:tdim
        result = ifft(result, [], dim);
    end
end
