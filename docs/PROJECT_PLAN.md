# Project Plan and Milestones

## Project title

**End-to-End Digital Communication System Simulation and Modulation Performance Comparison**

## Level and scope

This plan is designed for a sophomore Electrical Engineering student who is beginning formal communications and signal-processing study. The target is a strong, explainable simulation project—not an industrial modem or a real radio.

## Research question

How do BPSK, QPSK, and Gray-coded 16-QAM compare in bit-error performance when transmitted through an ideal AWGN channel at the same Eb/N0?

A second practical question is: can the same digital link be implemented independently in MATLAB and Python and produce consistent results within Monte Carlo variation?

## Work packages

### WP0 — Understand the foundations
Learn bit streams, symbols, I/Q representation, modulation, noise, SNR, Eb/N0, and BER. Complete small exercises before interpreting the full simulation.

**Exit check:** Explain why BPSK carries one bit per symbol, QPSK carries two, and 16-QAM carries four.

### WP1 — Establish a transparent reference implementation
Run the Python implementation and tests. Trace a short text message through bytes, bits, symbols, noisy samples, hard decisions, and recovered bytes.

**Deliverables:** passing unit tests, command-line demo, one BER CSV, one plot.

### WP2 — Reproduce the system in MATLAB
Run `matlab/test_codec.m` and `matlab/run_demo.m`. Compare its outputs with the Python reference using the same input bits and Eb/N0 settings where possible.

**Deliverables:** MATLAB scripts, screenshots, MATLAB results file, cross-check notes.

### WP3 — Build the Simulink model
Construct a block-level baseband model that visibly represents the source, modulator, channel, demodulator, and measurement path. Start with BPSK, then parameterize the modulation choice only after the BPSK path is understood.

**Deliverables:** `.slx` model created and run on Omar's installation, annotated block diagram, model settings and screenshots.

### WP4 — Analyze and explain results
Run repeated trials with enough bits to make conclusions meaningful. Explain finite-sample effects, especially why a measured BER can be zero when no errors happen in a finite test.

**Deliverables:** final BER graph, result table, discussion of trade-offs and limitations.

### WP5 — C++ implementation
Compile and run the BPSK Monte Carlo program. Explain how the code maps to the BPSK/AWGN equations. Compare the C++ and Python BPSK results statistically, not by expecting identical random sequences.

**Deliverables:** source, compiler command, captured CSV output, comparison notes.

### WP6 — Final engineering package
Complete the report, engineering log, README, figures, and short demo recording. Add only validated project claims to the portfolio and resume.

**Deliverables:** concise technical report, final repository, 2–4 minute demo, resume bullets supported by evidence.

## Suggested 7-week sequence

| Week | Focus | Practical output |
|---|---|---|
| 1 | Bits, bytes, vectors, complex numbers, MATLAB/Python refresh | Explain and run text-to-bits |
| 2 | Constellations and modulation | Plot and identify BPSK/QPSK/16-QAM points |
| 3 | AWGN, Eb/N0, hard decisions | Recover short messages at several noise levels |
| 4 | BER experiments and statistics | Reproducible BER sweep and graph |
| 5 | MATLAB/Simulink implementation | MATLAB run + first Simulink BPSK model |
| 6 | Cross-check and C++ benchmark | Compare independent implementations |
| 7 | Report, results, presentation, portfolio | Evidence-backed final package |

The schedule is a guide. If a concept is unclear, extend that stage rather than rushing forward.

## Performance and quality targets

These are acceptance checks, not promised numerical outcomes:

1. Noiseless modulation/demodulation must recover every supported bit pattern.
2. All constellations must have average symbol energy equal to approximately one.
3. The empirical BER should generally trend downward as Eb/N0 rises.
4. QPSK with Gray mapping should have a BER trend similar to BPSK in AWGN when Eb/N0 is defined consistently, though finite-run samples can differ.
5. At the same Eb/N0, 16-QAM normally has a higher BER than QPSK/BPSK because its constellation points are more closely spaced.
6. MATLAB and Python should use identical bit labeling and noise definitions before comparing results.

Do not force a graph to match a textbook curve. Investigate unexpected results and report what the simulation actually shows.

## Optional extensions — only after baseline completion

1. Theoretical BER curves for BPSK and QPSK.
2. Pulse shaping and matched filtering (requires careful sampling and symbol timing).
3. Carrier-frequency and phase offset.
4. Simple timing synchronization.
5. Rayleigh flat-fading channel.
6. A basic repetition code or Hamming (7,4) code and coding-gain comparison.

Choose one or two extensions. A smaller project with sound analysis is stronger than many unfinished features.

## Weekly evidence checklist

- Commit code changes with descriptive messages.
- Save terminal output and plots generated by actual runs.
- Add dated notes to the engineering log.
- Record unexpected behavior and how it was diagnosed.
- Keep a list of concepts Omar can explain confidently and concepts that still need study.
