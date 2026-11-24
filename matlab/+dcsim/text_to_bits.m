function bits = text_to_bits(message)
%TEXT_TO_BITS Convert ordinary ASCII text to an MSB-first bit row vector.
% This starter intentionally uses 8-bit ASCII-compatible characters.
bytes = uint8(char(message));
bits = zeros(1, 8 * numel(bytes));
for n = 1:numel(bytes)
    for b = 1:8
        bits((n-1)*8 + b) = bitget(bytes(n), 9-b);
    end
end
end
