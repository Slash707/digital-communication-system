# Digital Communication System Simulation: Technical Report

**Author:** Omar Ahmed  
**Program:** Electrical Engineering  
**Date:** [insert date]

## Abstract

[Summarize the purpose, implementation, experiments, and actual findings after the project is run. Do not fill this with expected outcomes.]

## 1. Introduction

- What digital communication problem is being modeled?
- Why compare BPSK, QPSK, and 16-QAM?
- What are the project objectives?

## 2. System Model

Include a system block diagram and describe:
1. ASCII text source.
2. Bit conversion.
3. Modulator and constellation mapping.
4. Complex baseband AWGN channel.
5. Hard-decision receiver.
6. BER measurement.

## 3. Mathematical Model

Define `M`, `k`, `Es`, `Eb`, `N0`, `Eb/N0`, and BER. Show the noise variance conversion and explain the normalization convention.

## 4. Implementation

Describe the MATLAB, Simulink, Python, and C++ roles. Include software versions and relevant settings. Identify which implementation was used as the reference.

## 5. Verification

Present unit tests, noiseless round-trip checks, constellation energy checks, and cross-language checks.

## 6. Experiments

For every experiment, state:
- Modulation
- Number of information bits
- Eb/N0 sweep
- Random seed
- Number of errors
- Measured BER

Include the actual BER plot and results table.

## 7. Discussion

Answer:
- How did BER change with Eb/N0?
- How did the modulation schemes compare?
- Were any BER points zero because the run was too short?
- Did MATLAB and Python agree within expected statistical variation?
- Which assumptions limit the model?

## 8. Limitations

At minimum discuss ideal AWGN, perfect timing/carrier knowledge, no RF hardware, no multipath/fading in the baseline, and finite Monte Carlo sample size.

## 9. Conclusion and Future Work

Summarize actual findings and select one realistic extension.

## References

[List textbooks, lecture notes, and official software documentation actually consulted.]

## Appendix

Code settings, extra plots, test logs, and Simulink screenshots.
