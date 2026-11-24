function [symbols, padCount] = modulate_bits(bits, modulation)
%MODULATE_BITS Map MSB-first bits to normalized complex baseband symbols.
bits = double(bits(:).');
if any(bits ~= 0 & bits ~= 1)
    error('Bits must contain only 0 and 1.');
end
[points, ~, k] = dcsim.constellation(modulation);
padCount = mod(-numel(bits), k);
if padCount > 0
    bits = [bits, zeros(1, padCount)];
end
if isempty(bits)
    symbols = complex(zeros(1,0));
    return;
end
groups = reshape(bits, k, []).';
weights = 2.^(k-1:-1:0).';
indices = groups * weights + 1;
symbols = points(indices).';
end
