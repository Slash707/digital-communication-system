# Resume Wording — Use Only After Validation

Do not place these bullets on a resume until the corresponding features have actually been run, tested, and understood. Replace bracketed values with measured results.

**Project: Digital Communication System Simulation | MATLAB, Simulink, Python, C++**

- Developed an end-to-end digital baseband communication simulation implementing BPSK, QPSK, and Gray-coded 16-QAM modulation over an AWGN channel.
- Implemented hard-decision receiver logic and evaluated bit-error rate across an Eb/N0 sweep using [number] bits per operating point.
- Cross-validated MATLAB and Python implementations using identical constellation mappings, normalization, and noise conventions.
- Built a Simulink model of a [validated modulation] transmitter/channel/receiver chain and documented its parameter assumptions.
- Implemented a C++17 BPSK Monte Carlo benchmark and compared its BER trend with the Python reference.

## Evidence required before using

- Repository link and reproducible run instructions.
- MATLAB/Simulink screenshots from actual successful runs.
- Final BER plot and CSV generated from actual runs.
- Measured bit counts and error counts.
- Omar's own explanation of the modulation mapping and Eb/N0-to-noise conversion.

Avoid claims like "real-time", "RF", "5G", "hardware transmitter", or "optimized" unless those features are genuinely implemented and measured.
