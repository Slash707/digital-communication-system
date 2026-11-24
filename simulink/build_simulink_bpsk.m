%% Build a BPSK digital communication system in Simulink
% This script creates and runs a complete, basic BPSK link using only
% standard Simulink blocks and MATLAB Function blocks.
%
% Run this script from MATLAB. The model is saved beside this script.

clearvars;
clc;

scriptFolder = fileparts(mfilename('fullpath'));
modelName = 'digital_communication_system_bpsk';
modelFile = fullfile(scriptFolder, [modelName '.slx']);

% A short, fixed message represented as bits.
message = 'HELLO OMAR';
messageBytes = uint8(message);
bitMatrix = dec2bin(messageBytes, 8) - '0';
txBits = reshape(bitMatrix.', 1, []);
assignin('base', 'dcsim_txBits', double(txBits));

% Close an older copy of this model, if it is already open.
if bdIsLoaded(modelName)
    close_system(modelName, 0);
end

% Create a new model.
new_system(modelName);
open_system(modelName);
set_param(modelName, 'StopTime', '1');

% Add the source.
add_block('simulink/Sources/Constant', [modelName '/Transmitted Bits'], ...
    'Value', 'dcsim_txBits', ...
    'Position', [40 115 150 155]);

% Add MATLAB Function blocks.
modPath = [modelName '/BPSK Modulator'];
add_block('simulink/User-Defined Functions/MATLAB Function', modPath, ...
    'Position', [220 105 355 165]);

noisePath = [modelName '/AWGN Channel'];
add_block('simulink/User-Defined Functions/MATLAB Function', noisePath, ...
    'Position', [425 105 560 165]);

demodPath = [modelName '/BPSK Demodulator'];
add_block('simulink/User-Defined Functions/MATLAB Function', demodPath, ...
    'Position', [630 105 765 165]);

berPath = [modelName '/BER Calculator'];
add_block('simulink/User-Defined Functions/MATLAB Function', berPath, ...
    'Position', [835 105 985 165]);

% Add displays for the error count and BER.
add_block('simulink/Sinks/Display', [modelName '/Bit Errors'], ...
    'Position', [1050 90 1150 125]);
add_block('simulink/Sinks/Display', [modelName '/Measured BER'], ...
    'Position', [1050 155 1150 190]);

% Set the MATLAB Function block code.
setMatlabFunctionScript(modPath, sprintf([ ...
    'function symbols = fcn(bits)\n' ...
    '%% Map binary 0 to +1 and binary 1 to -1.\n' ...
    'symbols = 1 - 2*double(bits);\n' ...
    'end\n']));

setMatlabFunctionScript(noisePath, sprintf([ ...
    'function received = fcn(transmitted)\n' ...
    '%% Real AWGN channel for BPSK at Eb/N0 = 8 dB.\n' ...
    'EbN0dB = 8;\n' ...
    'EbN0 = 10^(EbN0dB/10);\n' ...
    'noiseStd = sqrt(1/(2*EbN0));\n' ...
    'received = transmitted + noiseStd*randn(size(transmitted));\n' ...
    'end\n']));

setMatlabFunctionScript(demodPath, sprintf([ ...
    'function bits = fcn(received)\n' ...
    '%% Decide 0 for nonnegative samples and 1 for negative samples.\n' ...
    'bits = double(received < 0);\n' ...
    'end\n']));

setMatlabFunctionScript(berPath, sprintf([ ...
    'function [errorCount, ber] = fcn(transmittedBits, receivedBits)\n' ...
    '%% Compare transmitted and received bits.\n' ...
    'errors = transmittedBits ~= receivedBits;\n' ...
    'errorCount = sum(errors);\n' ...
    'ber = errorCount / numel(transmittedBits);\n' ...
    'end\n']));

% Connect the blocks.
add_line(modelName, 'Transmitted Bits/1', 'BPSK Modulator/1', 'autorouting', 'on');
add_line(modelName, 'BPSK Modulator/1', 'AWGN Channel/1', 'autorouting', 'on');
add_line(modelName, 'AWGN Channel/1', 'BPSK Demodulator/1', 'autorouting', 'on');
add_line(modelName, 'Transmitted Bits/1', 'BER Calculator/1', 'autorouting', 'on');
add_line(modelName, 'BPSK Demodulator/1', 'BER Calculator/2', 'autorouting', 'on');
add_line(modelName, 'BER Calculator/1', 'Bit Errors/1', 'autorouting', 'on');
add_line(modelName, 'BER Calculator/2', 'Measured BER/1', 'autorouting', 'on');

% Save and simulate.
save_system(modelName, modelFile);
fprintf('Created Simulink model: %s\n', modelFile);
fprintf('Message: %s\n', message);
fprintf('Number of transmitted bits: %d\n', numel(txBits));
fprintf('Channel setting: BPSK, AWGN, Eb/N0 = 8 dB\n');
fprintf('Running simulation...\n');

simOut = sim(modelName);
disp('Simulation finished. Check the Bit Errors and Measured BER displays in the model.');

%% Local helper: write code into a MATLAB Function block.
function setMatlabFunctionScript(blockPath, codeText)
    rt = sfroot;
    chart = rt.find('-isa', 'Stateflow.EMChart', 'Path', blockPath);
    if isempty(chart)
        error(['Could not find the MATLAB Function chart for block: ' blockPath]);
    end
    chart.Script = codeText;
end
