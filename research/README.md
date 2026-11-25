# Advanced Link-Performance Laboratory

A reproducible, cross-modulation link study for BPSK, QPSK and Gray-coded 16-QAM over an AWGN channel.

## What this adds
- Monte-Carlo bit-error measurements with a fixed seed and configurable bit budget.
- Analytical reference curves (exact BPSK/QPSK; standard Gray-coded square-QAM approximation for 16-QAM).
- Wilson 95% confidence intervals for measured BER, including a meaningful upper bound when zero errors are observed.
- EVM/RMS error-vector magnitude, spectral efficiency, and uncoded bit throughput calculations.
- Machine-readable CSV output and publication-quality BER plot.

## Run
From the repository root:

```bash
python research/link_performance.py --bits 1000000 --seed 42 --out results/advanced
```

Requires NumPy and Matplotlib (Matplotlib is only needed for the plot). If Matplotlib is unavailable, CSV generation still succeeds.

## Method and assumptions
- Unit-average-energy constellations: BPSK/QPSK have Es=1; 16-QAM is normalized by sqrt(10).
- Eb/N0 is the independent variable. Complex AWGN uses variance N0/2 per real dimension.
- Gray-coded QPSK and 16-QAM are used. The 16-QAM analytical curve is the common nearest-neighbour BER approximation, not an exact finite-SNR expression.
- BER is errors / transmitted bits. Wilson intervals communicate finite-sample uncertainty. Zero observed errors is never reported as a true BER of zero.
- EVM is measured at the receiver against the transmitted symbols before hard decisions; RMS EVM is dimensionless and is also reported as a percentage.

## Interpreting zero errors
With N tested bits and zero observed errors, the approximate 95% "rule of three" upper bound is 3/N. The script reports the more accurate Wilson interval. This is why a measured BER of 0 must not be interpreted as a perfect channel.

## Reproducibility
The random generator, seed, bit count, Eb/N0 grid, and assumptions are recorded in the CSV metadata columns. Re-run with the same arguments to reproduce the same measurements.
