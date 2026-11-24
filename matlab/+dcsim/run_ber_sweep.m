function results = run_ber_sweep(ebn0dBValues, requestedBits, modulations)
%RUN_BER_SWEEP Monte Carlo BER experiment for a set of modulations.
if nargin < 3
    modulations = {'BPSK', 'QPSK', '16QAM'};
end
results = struct('modulation', {}, 'ebn0dB', {}, 'ber', {}, ...
                 'errors', {}, 'testedBits', {});
for m = 1:numel(modulations)
    [~, ~, k] = dcsim.constellation(modulations{m});
    nBits = floor(requestedBits/k)*k;
    txBits = randi([0 1], 1, nBits);
    txSymbols = dcsim.modulate_bits(txBits, modulations{m});
    ber = zeros(size(ebn0dBValues));
    errorCounts = zeros(size(ebn0dBValues));
    for s = 1:numel(ebn0dBValues)
        rxSymbols = dcsim.awgn_channel(txSymbols, ebn0dBValues(s), k);
        rxBits = dcsim.demodulate_symbols(rxSymbols, modulations{m}, nBits);
        errorCounts(s) = sum(txBits ~= rxBits);
        ber(s) = errorCounts(s)/nBits;
    end
    results(m).modulation = modulations{m};
    results(m).ebn0dB = ebn0dBValues(:).';
    results(m).ber = ber;
    results(m).errors = errorCounts;
    results(m).testedBits = nBits;
end
end
