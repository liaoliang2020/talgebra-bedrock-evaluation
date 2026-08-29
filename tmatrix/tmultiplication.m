function result = tmultiplication(left, right, tsize)
%TMULTIPLICATION Multiply compatible t-matrices through spectral slices.

    assert(isa(left, 'double') && isa(right, 'double'), ...
        'T-Algebra:Type', 'Inputs must be double arrays.');
    tsize = validate_tmatrix_shape(left, tsize);
    validate_tmatrix_shape(right, tsize);

    tdim = numel(tsize);
    left_size = padded_size(left, tdim + 2);
    right_size = padded_size(right, tdim + 2);
    rows = left_size(tdim + 1);
    inner = left_size(tdim + 2);
    assert(inner == right_size(tdim + 1), ...
        'T-Algebra:InnerDimension', 'Inner matrix dimensions must agree.');
    columns = right_size(tdim + 2);

    left_hat = left;
    right_hat = right;
    for dim = 1:tdim
        left_hat = fft(left_hat, [], dim);
        right_hat = fft(right_hat, [], dim);
    end

    slice_count = prod(tsize);
    left_hat = reshape(left_hat, slice_count, rows, inner);
    right_hat = reshape(right_hat, slice_count, inner, columns);

    for index = 1:slice_count
        left_slice = reshape(left_hat(index, :, :), rows, inner);
        right_slice = reshape(right_hat(index, :, :), inner, columns);
        product_slice = left_slice * right_slice;
        if index == 1
            result_hat = zeros([slice_count, rows, columns], ...
                'like', product_slice);
        end
        result_hat(index, :, :) = product_slice;
    end

    result = reshape(result_hat, [tsize, rows, columns]);
    for dim = 1:tdim
        result = ifft(result, [], dim);
    end
end

function tsize = validate_tmatrix_shape(array, tsize)
    validateattributes(tsize, {'numeric'}, ...
        {'vector', 'integer', 'positive', 'finite', 'real'});
    tsize = double(tsize(:).');
    array_size = padded_size(array, numel(tsize) + 2);
    assert(isequal(array_size(1:numel(tsize)), tsize), ...
        'T-Algebra:TShape', ...
        'Leading array dimensions must equal tsize.');
end

function result = padded_size(array, count)
    result = size(array);
    result(end + 1:count) = 1;
end
