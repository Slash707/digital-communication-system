# Engineering Notes — Advanced AWGN Link Study

## Design question
How does modulation order change reliability and symbol efficiency when links are compared at equal energy per information bit?

## Constellation and energy normalization
BPSK and QPSK are normalized to unit average symbol energy. The 16-QAM square constellation uses I/Q levels ±1 and ±3, then divides complex symbols by sqrt(10), giving unit average symbol energy. This is essential: comparing unnormalized constellations would make the Eb/N0 comparison misleading.

For k=log2(M) bits/symbol and unit Es, Eb=Es/k. The simulation therefore uses N0=1/(k·10^(Eb/N0[dB]/10)); each real noise component has variance N0/2.

## Expected engineering trade-off
BPSK and QPSK have the same uncoded BER at equal Eb/N0 in ideal AWGN, while QPSK carries twice as many bits per symbol. 16-QAM carries four bits per symbol, but its constellation points are closer together after energy normalization, so it needs a higher Eb/N0 for a comparable BER. This is the reliability-versus-spectral-efficiency trade-off that adaptive modulation systems exploit.

## Statistical interpretation
A Monte-Carlo BER is an estimate, not the exact channel BER. The Wilson 95% interval is reported to avoid false certainty, especially when the simulation observes few or no errors. If a point's interval is wide, increase the bit budget. A useful rule for a target BER p is to simulate enough bits to observe many errors; roughly 100/p bits yields about 100 expected errors.

## Scope and limitations
This experiment models uncoded coherent detection over memoryless complex AWGN. It does not model fading, carrier-frequency offset, timing recovery, phase noise, coding, inter-symbol interference, RF impairments, or a real SDR front end. The 16-QAM theory curve is a standard approximation. The reported EVM includes injected AWGN and is not a hardware transmitter/receiver EVM certification.

## Suggested follow-on experiments
1. Rayleigh fading with coherent channel estimation and equalization.
2. Convolutional or LDPC coding and coding gain.
3. Carrier-frequency and phase-offset sensitivity.
4. Packet framing, CRC, and retransmission/throughput under packet errors.
5. SDR over-the-air validation.
