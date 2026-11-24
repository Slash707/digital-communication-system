# Test and Verification Plan

## Unit tests

| ID | Test | Expected result |
|---|---|---|
| T01 | Convert `A` to bits | `01000001` using MSB-first byte order |
| T02 | Convert ASCII text to bits and back | Original message recovered exactly |
| T03 | Modulate/demodulate BPSK with no noise | Exact bit recovery |
| T04 | Modulate/demodulate QPSK with no noise | Exact bit recovery |
| T05 | Modulate/demodulate 16-QAM with no noise | Exact bit recovery |
| T06 | Average constellation energy | Approximately 1 for all schemes |
| T07 | AWGN output shape | Same number of samples as input |
| T08 | BER sweep output | BER lies between 0 and 1 |
| T09 | C++ BPSK smoke test | Valid CSV output; BER estimates trend downward over enough bits |

## Cross-language verification

Use the same short bit sequence, modulation, and Eb/N0 in MATLAB and Python. First compare:
1. The constellation symbol selected for every bit group.
2. The computed noise variance.
3. The noiseless demodulated bits.

Random noise samples will not be identical across languages unless the same generator algorithm and state are deliberately matched. Compare statistical behavior rather than expecting identical error counts from independent random trials.

## Sanity checks

- Every constellation point is unique.
- Average energy is approximately 1.
- Modulation and demodulation preserve bit order.
- Padding bits are removed by the demodulator.
- BER is calculated only over the original information bits.
- A finite run with zero bit errors is not represented as proof of zero true BER.
- Eb/N0 is defined consistently across modulation schemes.

## Record every experiment

For each run, record date, software version, modulation, number of bits, Eb/N0 values, random seed, errors, BER, and any warnings or unusual observations.
