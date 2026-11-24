function message = bits_to_text(bits)
%BITS_TO_TEXT Convert an MSB-first bit vector back to 8-bit characters.
bits = double(bits(:).');
if any(bits ~= 0 & bits ~= 1)
    error('Bits must contain only 0 and 1.');
end
if mod(numel(bits), 8) ~= 0
    error('The number of bits must be a multiple of 8.');
end
if isempty(bits)
    message = '';
    return;
end
bitRows = reshape(bits, 8, []).';
weights = 2.^(7:-1:0).';
bytes = uint8(bitRows * weights);
message = char(bytes.');
end
