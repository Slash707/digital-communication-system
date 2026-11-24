%% Digital Communication System - Simulink BER Sweep
% Tests BPSK performance at different Eb/N0 values.


clc;

modelName = 'digital_communication_system_bpsk';

projectFolder = fileparts(fileparts(mfilename('fullpath')));
modelFile = fullfile(projectFolder, 'simulink', ...
    [modelName '.slx']);

if ~isfile(modelFile)
    error('Simulink model not found: %s', modelFile);
end

load_system(modelFile);

% Add a To Workspace block to record measured BER.
berBlock = [modelName '/BER Sweep Output'];

if isempty(find_system(modelName, 'SearchDepth', 1, ...
        'Name', 'BER Sweep Output'))

    add_block('simulink/Sinks/To Workspace', berBlock, ...
        'VariableName', 'dcsim_ber_log', ...
        'SaveFormat', 'Array', ...
        'Position', [650 250 770 290]);

    add_line(modelName, 'BER Calculator/2', ...
        'BER Sweep Output/1', 'autorouting', 'on');
end

% Eb/N0 test values in dB.
EbN0_values = 0:2:12;

measuredBER = zeros(size(EbN0_values));

fprintf('\nStarting Simulink BER sweep...\n');

for k = 1:length(EbN0_values)

    set_param([modelName '/EbN0'], ...
    'Value', num2str(EbN0_values(k)));
    simOut = sim(modelName, 'ReturnWorkspaceOutputs', 'on');

    berData = simOut.get('dcsim_ber_log');
    measuredBER(k) = berData(end);

    fprintf('Eb/N0 = %2d dB | Measured BER = %.5f\n', ...
        EbN0_values(k), measuredBER(k));
end

% Save results.
resultsFolder = fullfile(projectFolder, 'results', 'simulink');

if ~exist(resultsFolder, 'dir')
    mkdir(resultsFolder);
end

resultsTable = table(EbN0_values(:), measuredBER(:), ...
    'VariableNames', {'EbN0_dB', 'Measured_BER'});

writetable(resultsTable, ...
    fullfile(resultsFolder, 'simulink_ber_results.csv'));

% Plot results.
figure;

semilogy(EbN0_values, measuredBER, '-o', ...
    'LineWidth', 1.5, 'MarkerSize', 7);

grid on;
xlabel('E_b/N_0 (dB)');
ylabel('Bit Error Rate (BER)');
title('Simulink BPSK BER Performance');

fprintf('\nBER sweep completed.\n');
fprintf('Results saved to: %s\n', resultsFolder);
