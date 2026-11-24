function bits = demodulate_symbols(received, modulation, originalBitCount)
%DEMODULATE_SYMBOLS Nearest-point hard-decision demodulation.
[points, labels, ~] = dcsim.constellation(modulation);
received = received(:);
if isempty(received)
    bits = zeros(1,0);
    return;
end
distances = abs(received - points.').^2;
[~, nearestIndex] = min(distances, [], 2);
selectedLabels = labels(nearestIndex, :);
bits = reshape(selectedLabels.', 1, []);
if nargin >= 3 && ~isempty(originalBitCount)
    if originalBitCount < 0 || originalBitCount > numel(bits)
        error('originalBitCount is outside the available demodulated bit range.');
    end
    bits = bits(1:originalBitCount);
end
end
