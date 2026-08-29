function result = E_T(tsize)
%E_T Multiplicative identity for a t-scalar circular-convolution algebra.

    validateattributes(tsize, {'numeric'}, ...
        {'vector', 'integer', 'positive', 'finite', 'real'});
    tsize = double(tsize(:).');

    if isscalar(tsize)
        result = zeros(tsize, 1);
    else
        result = zeros(tsize);
    end
    result(1) = 1;
end
