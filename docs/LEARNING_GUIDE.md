# Learning Guide: The Ideas Behind the Simulation

This guide is a compact companion, not a substitute for working through examples.

## 1. Bits, bytes, and symbols

A **bit** is a binary digit: 0 or 1. An 8-bit byte can represent one ordinary ASCII character. A modem does not normally transmit the letters directly; it maps groups of bits to signal symbols.

If a modulation has `M` different symbols, each symbol can represent:

`k = log2(M)` bits.

Examples:
- BPSK: M = 2, so k = 1 bit/symbol.
- QPSK: M = 4, so k = 2 bits/symbol.
- 16-QAM: M = 16, so k = 4 bits/symbol.

## 2. I/Q representation

A complex baseband symbol is written:

`s = I + jQ`

`I` is the in-phase component, `Q` is the quadrature component, and `j` is the imaginary unit. A constellation plot shows each possible symbol as a point in the I-Q plane.

## 3. Modulation

- **BPSK:** two points on the real axis. This project maps bit 0 to +1 and bit 1 to -1.
- **QPSK:** four points. The two bits independently select the sign of I and Q.
- **16-QAM:** sixteen points in a square grid. Each axis has four amplitude levels. The chosen labeling is Gray-coded along each axis so adjacent levels differ by one bit.

The project normalizes the average symbol energy to `Es = 1`. This makes fair energy comparisons easier.

## 4. Noise and AWGN

The received symbol is modeled as:

`r = s + n`

Here `s` is the transmitted symbol and `n` is additive white Gaussian noise. “Additive” means it is added to the signal; “Gaussian” describes its amplitude distribution; “white” means its idealized power spectral density is flat.

This baseline channel does not model reflections, fading, interference, or real RF hardware.

## 5. Eb/N0

`Eb/N0` compares energy per information bit, `Eb`, with the noise power spectral density, `N0`. It is commonly expressed in decibels:

`EbN0_dB = 10 log10(Eb/N0)`

With normalized average symbol energy `Es = 1` and `k` bits per symbol:

`Eb = Es/k = 1/k`

For a selected linear ratio `gamma_b = 10^(EbN0_dB/10)`:

`N0 = 1 / (k * gamma_b)`

The complex AWGN generator uses independent Gaussian noise in I and Q, each with variance `N0/2`.

Do not confuse Eb/N0 with sample SNR. They are related but not interchangeable without accounting for bits per symbol, samples per symbol, and signal scaling.

## 6. Demodulation

The receiver estimates the transmitted symbol. This starter uses **nearest-neighbor hard decisions**:

`estimated symbol = constellation point with the smallest |r - s_i|^2`

Then it maps the selected point back to its bit label. This is simple and appropriate for an introductory simulation, though it is not every receiver's optimal implementation in every setting.

## 7. Bit error rate

`BER = number of incorrect recovered bits / number of transmitted bits`

A lower BER means fewer bit errors in the tested conditions. BER is an estimate from a finite experiment. If no errors occur in a short run, the measured BER is zero; that does **not** prove the true BER is exactly zero.

## 8. What to look for

As Eb/N0 increases, the noise becomes weaker relative to the bit energy, so BER should generally fall.

At the same Eb/N0:
- BPSK and Gray-coded QPSK have very similar theoretical BER in ideal AWGN.
- 16-QAM packs more bits into each symbol, but adjacent points are closer together after energy normalization, making it more sensitive to noise.

## 9. Questions Omar should be able to answer

1. Why do we convert text to bits?
2. What is the difference between a bit and a symbol?
3. What do I and Q represent?
4. Why do QPSK and 16-QAM carry more bits per symbol than BPSK?
5. What does AWGN represent?
6. What is the difference between SNR and Eb/N0?
7. Why does BER usually decrease at higher Eb/N0?
8. Why can a finite simulation report zero errors?
9. What assumptions make this a baseband simulation rather than a real radio?
