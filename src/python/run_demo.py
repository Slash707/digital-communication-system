"""Run the message-recovery demonstration and BER sweep."""
from __future__ import annotations

import csv
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dcsim import (  # noqa: E402
    awgn_channel,
    bits_to_text,
    constellation,
    demodulate_symbols,
    modulate_bits,
    run_ber_sweep,
    text_to_bits,
)


def main() -> None:
    message = "HELLO OMAR"
    tx_bits = text_to_bits(message)
    demo_ebn0_db = 10.0
    print("Digital Communication System Demo")
    print(f"Original message: {message}")
    print(f"Information bits: {tx_bits.size}\n")

    for modulation in ("BPSK", "QPSK", "16QAM"):
        _, _, k = constellation(modulation)
        tx_symbols, pad_count = modulate_bits(tx_bits, modulation)
        rng = np.random.default_rng(4400 + k)
        rx_symbols = awgn_channel(tx_symbols, demo_ebn0_db, k, rng)
        rx_bits = demodulate_symbols(rx_symbols, modulation, tx_bits.size)
        recovered = bits_to_text(rx_bits)
        errors = int(np.count_nonzero(tx_bits != rx_bits))
        print(
            f"{modulation}: recovered={recovered!r}, "
            f"bit errors={errors}/{tx_bits.size}, padding={pad_count}"
        )

    print("\nRunning BER sweep...")
    ebn0_db = np.arange(0, 15, 2, dtype=float)
    results = run_ber_sweep(ebn0_db, requested_bits=200_000)

    out_dir = PROJECT_ROOT / "results" / "python_reference"
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "ber_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["modulation", "ebn0_db", "errors", "tested_bits", "ber"])
        for result in results:
            for snr, error_count, ber in zip(
                result.ebn0_db, result.errors, result.ber
            ):
                writer.writerow(
                    [result.modulation, snr, int(error_count), result.tested_bits, ber]
                )

    plt.figure(figsize=(8.2, 5.2))
    for result in results:
        plotted = result.ber.astype(float).copy()
        plotted[plotted == 0] = np.nan
        plt.semilogy(
            result.ebn0_db, plotted, marker="o", linewidth=1.6,
            label=result.modulation
        )
    plt.grid(True, which="both", alpha=0.3)
    plt.xlabel(r"$E_b/N_0$ (dB)")
    plt.ylabel("Measured bit error rate")
    plt.title("Digital modulation over an AWGN channel")
    plt.legend()
    plt.tight_layout()
    plot_path = out_dir / "ber_vs_ebn0.png"
    plt.savefig(plot_path, dpi=180)
    plt.close()

    print(f"\nSaved CSV:  {csv_path}")
    print(f"Saved plot: {plot_path}")
    print("Zero-error points are omitted from the logarithmic plot; they are not proof")
    print("that the true BER is zero. Interpret the finite bit count carefully.")


if __name__ == "__main__":
    main()
