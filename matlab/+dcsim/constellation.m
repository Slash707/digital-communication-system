function [points, labels, k] = constellation(modulation)
%CONSTELLATION Return unit-average-energy Gray-labelled constellation.
% Rows of labels correspond to points. Bit labels are MSB-first.
name = upper(char(modulation));
switch name
    case 'BPSK'
        k = 1;
        labels = [0; 1];
        points = [1; -1];
    case 'QPSK'
        k = 2;
        labels = zeros(4, 2);
        for n = 0:3
            labels(n+1, :) = [bitget(uint32(n), 2), bitget(uint32(n), 1)];
        end
        iAxis = 1 - 2*labels(:,1);
        qAxis = 1 - 2*labels(:,2);
        points = (iAxis + 1i*qAxis) / sqrt(2);
    case '16QAM'
        k = 4;
        labels = zeros(16, 4);
        for n = 0:15
            labels(n+1, :) = [bitget(uint32(n),4), bitget(uint32(n),3), ...
                              bitget(uint32(n),2), bitget(uint32(n),1)];
        end
        % Gray sequence along increasing amplitude: 10, 11, 01, 00.
        grayLevels = [3, 1, -3, -1]; % indexed by binary pair 00,01,10,11
        iIndex = 2*labels(:,1) + labels(:,2) + 1;
        qIndex = 2*labels(:,3) + labels(:,4) + 1;
        iAxis = grayLevels(iIndex).';
        qAxis = grayLevels(qIndex).';
        points = (iAxis + 1i*qAxis) / sqrt(10);
    otherwise
        error('Unsupported modulation. Choose BPSK, QPSK, or 16QAM.');
end
points = points(:);
end
