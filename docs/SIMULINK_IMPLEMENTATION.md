# Simulink Implementation Plan

## Status

The MATLAB and Python source files are prepared, but a native `.slx` model has **not** yet been created or tested on Omar's computer. This guide defines the model to build after the MATLAB codec tests pass.

## Recommended first model: BPSK link

Build a visible BPSK path first. Do not begin with an all-modulation model; a simple, understood BPSK model is easier to debug.

```text
Bit source
   |
   v
BPSK mapper (0 -> +1, 1 -> -1)
   |
   v
AWGN channel
   |
   v
Hard-decision detector (real(r) >= 0)
   |
   +------> Error Rate Calculation
   |
   v
Recovered bits
```

## Block responsibilities

| Section | Responsibility | Key setting |
|---|---|---|
| Source | Generate a repeatable binary sequence | Fixed seed or supplied test vector |
| Mapper | Convert 0/1 into +1/-1 | Unit symbol energy |
| Channel | Add Gaussian noise | Eb/N0 or equivalent variance |
| Detector | Decide the closest BPSK point | Threshold at zero |
| Metric | Compare transmitted and recovered bits | BER, error count, total bits |
| Scope/Display | Show selected signals | Limit display to a short run |

## Implementation sequence

1. Check whether the installed Simulink library includes the blocks needed for source, random noise, comparison, and error-rate measurement.
2. If a Communications Toolbox block is available, record its exact block name and parameter definition. Confirm whether it expects Eb/N0, Es/N0, or sample SNR.
3. If the Communications Toolbox is not installed, build the BPSK mapper, AWGN, and detector using basic Simulink blocks or MATLAB Function blocks.
4. Verify the model with noise disabled: every input bit must be recovered exactly.
5. Enable noise at a low Eb/N0 and confirm that occasional errors appear.
6. Increase Eb/N0 and confirm that errors generally become less frequent.
7. Save the model as `simulink/digital_link_bpsk.slx` and capture a model screenshot.
8. Only then extend the model to QPSK and 16-QAM.

## Critical parameter check

Different AWGN blocks define signal power, samples per symbol, and SNR differently. Never enter an Eb/N0 number into a field labeled SNR without confirming the conversion. For this project's normalized symbols and `k` bits/symbol:

`N0 = 1 / (k * 10^(EbN0_dB/10))`

Each real component of the complex noise has variance `N0/2`.

Record the block's parameter convention in the engineering log and final report.

## Evidence to save

- Full model screenshot with readable block names.
- Model configuration and solver settings.
- Noise/EbN0 setting used for each run.
- Transmitted and recovered bit sequence for a short test.
- Measured error count, bit count, and BER.
- A note explaining how Simulink's noise parameter maps to the project's Eb/N0 convention.
