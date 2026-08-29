function result = tproduct(left, right)
%TPRODUCT Multiply two equally sized t-scalars by circular convolution.

    assert(isa(left, 'double') && isa(right, 'double'), ...
        'T-Algebra:Type', 'Inputs must be double arrays.');
    assert(isequal(size(left), size(right)), ...
        'T-Algebra:Size', 'T-scalar sizes must agree.');

    result = ifftn(fftn(left) .* fftn(right));
end
