% TEST_CODEC Basic noiseless tests for text and modulation functions.
clear; clc;
projectRoot = fileparts(mfilename('fullpath'));
addpath(projectRoot);

message = 'A';
bits = dcsim.text_to_bits(message);
assert(isequal(bits, [0 1 0 0 0 0 0 1]));
assert(strcmp(dcsim.bits_to_text(bits), message));

testBits = [0 1 1 0 1 0 0 1 1 1 0 0 0 1 0 1];
modulations = {'BPSK', 'QPSK', '16QAM'};
for m = 1:numel(modulations)
    name = modulations{m};
    [points, ~, ~] = dcsim.constellation(name);
    assert(abs(mean(abs(points).^2) - 1) < 1e-12);
    [tx, ~] = dcsim.modulate_bits(testBits, name);
    rxBits = dcsim.demodulate_symbols(tx, name, numel(testBits));
    assert(isequal(testBits, rxBits));
    fprintf('%s noiseless round-trip: PASS\n', name);
end
fprintf('Text codec: PASS\nAll basic MATLAB tests passed.\n');
