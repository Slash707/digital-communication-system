function [received, noise] = awgn_channel(transmitted, ebn0dB, bitsPerSymbol)
%AWGN_CHANNEL Add complex AWGN for unit-average-symbol-energy constellations.
% Es = 1, Eb = Es/k, N0 = Eb / 10^(EbN0dB/10).
if bitsPerSymbol <= 0
    error('bitsPerSymbol must be positive.');
end
linearEbN0 = 10.^(ebn0dB/10);
N0 = 1 ./ (bitsPerSymbol .* linearEbN0);
sigma = sqrt(N0/2);
noise = sigma .* (randn(size(transmitted)) + 1i*randn(size(transmitted)));
received = transmitted + noise;
end
