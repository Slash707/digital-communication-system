# Digital Communication System Simulation

Multi-language digital communications simulation framework implementing **BPSK**, **QPSK**, and **16-QAM** over an **AWGN** channel across **MATLAB/Simulink**, **Python**, and **C++**, with automated testing, documentation, and Bit Error Rate (BER) sweep results.

## Tools & Environment
- **MATLAB R2026b Update 1 & Simulink R2026b**: Modulation/demodulation package (`+dcsim`), Simulink BPSK model, and automated BER sweep
- **Python 3.14**: Reference implementation, demo runner, and automated unit tests (`pytest`)
- **C++**: BPSK AWGN BER simulation (`cpp/ber_bpsk.cpp`)
- **Git & GitHub**: Version control and CI workflow (`.github/workflows/python-tests.yml`)

## Repository Structure
- `matlab/` - MATLAB `+dcsim` package (BPSK, QPSK, 16-QAM, AWGN, text/bit codec, BER sweep) and sweep/test scripts
- `simulink/` - Simulink BPSK model (`digital_communication_system_bpsk.slx`), builder script, and 80-bit backup
- `src/python/` & `tests/` - Python digital communications modules and automated test suite
- `cpp/` - C++ BPSK simulation source code
- `research/` - Reproducible multi-modulation link-performance study, analytical BER references, confidence intervals, EVM, and engineering notes
- `results/` - Simulation outputs including Simulink BER CSV (`results/simulink/simulink_ber_results.csv`), Python reference CSV/plot, and C++ reference CSV
- `docs/` - Engineering logs, project/test plans, Simulink implementation notes, report template, and resume/viva notes

## How to Run
1. **Simulink BPSK BER Sweep (MATLAB/Simulink)**: Open `matlab/` and `simulink/` in MATLAB R2026b and run `run_simulink_ber_sweep.m` (or open `simulink/digital_communication_system_bpsk.slx` directly).
2. **MATLAB Package & Tests**: Add `matlab/` to your MATLAB path and run `test_codec.m` or call `+dcsim` functions.
3. **Python Demo & Tests**: Install dependencies from `requirements.txt`, run `python src/python/run_demo.py`, and run `pytest` from the project root.
4. **C++ BPSK Simulation**: Compile and run `cpp/ber_bpsk.cpp` with a standard C++ compiler (such as `g++` or MSVC).
5. **Advanced link study**: Install NumPy and Matplotlib, then run `python research/link_performance.py --bits 1000000 --seed 42 --out results/advanced`. See [research/README.md](research/README.md).

## Simulink BPSK Simulation Results (100,000 Random Bits)
Upgraded from an initial 80-bit test model to **100,000 random bits** over an AWGN channel, saved in `results/simulink/simulink_ber_results.csv`:

| Eb/N0 (dB) | Measured BER |
| ---: | ---: |
| 0 | 0.07923 |
| 2 | 0.03792 |
| 4 | 0.01281 |
| 6 | 0.00258 |
| 8 | 0.00016 |
| 10 | 0 |
| 12 | 0 |

> A measured zero means no errors were observed in that finite run; it does not mean the true BER is zero.

## Advanced Link-Performance Study
The new `research/` laboratory compares BPSK, QPSK, and Gray-coded 16-QAM at equal Eb/N0. It produces Monte-Carlo BER, analytical reference curves, Wilson 95% confidence intervals, RMS EVM, and bits-per-symbol efficiency. Constellations are unit-average-energy normalized and the noise variance is derived from Eb/N0, making the comparison physically meaningful. The 16-QAM analytical curve is explicitly identified as a nearest-neighbour approximation. See [engineering notes](research/ENGINEERING_NOTES.md) for assumptions, interpretation, limitations, and next experiments.
