#!/usr/bin/env python3
"""Reproducible BER/EVM study for BPSK, QPSK and Gray-coded 16-QAM over AWGN."""
from __future__ import annotations
import argparse, csv, math
from pathlib import Path
import numpy as np

MODULATIONS = ("BPSK", "QPSK", "16QAM")
LEVELS = np.array([-3, -1, 3, 1], dtype=float) / math.sqrt(10.0)
GRAY_PAIRS = ((0, 0), (0, 1), (1, 0), (1, 1))
# Index order follows Gray labels 00, 01, 10, 11; physical levels -3,-1,+3,+1.
PAIR_TO_LEVEL = {(0, 0):-3.0, (0, 1):-1.0, (1, 0):3.0, (1, 1):1.0}
LEVEL_TO_PAIR = {-3.0:(0,0), -1.0:(0,1), 3.0:(1,0), 1.0:(1,1)}

def qfunc(x: float) -> float:
    return 0.5 * math.erfc(x / math.sqrt(2.0))

def theory_ber(name: str, ebn0_db: float) -> float:
    gamma = 10.0 ** (ebn0_db / 10.0)
    if name in ("BPSK", "QPSK"):
        return qfunc(math.sqrt(2.0 * gamma))
    # Standard Gray-coded square 16-QAM nearest-neighbour approximation.
    return 0.75 * qfunc(math.sqrt(0.8 * gamma))

def wilson_interval(errors: int, total: int, z: float = 1.959963984540054):
    if total <= 0:
        return (float("nan"), float("nan"))
    p = errors / total
    den = 1.0 + z*z/total
    center = (p + z*z/(2*total)) / den
    half = z * math.sqrt(p*(1-p)/total + z*z/(4*total*total)) / den
    return max(0.0, center-half), min(1.0, center+half)

def bits_to_symbols(bits: np.ndarray, name: str) -> np.ndarray:
    if name == "BPSK":
        return (2*bits.astype(float)-1).astype(complex)
    pairs = bits.reshape(-1, 2)
    if name == "QPSK":
        return ((2*pairs[:,0]-1) + 1j*(2*pairs[:,1]-1)) / math.sqrt(2.0)
    i = np.array([PAIR_TO_LEVEL[tuple(x)] for x in pairs[:,0:2]], dtype=float)
    q = np.array([PAIR_TO_LEVEL[tuple(x)] for x in pairs[:,2:4]], dtype=float)
    return (i + 1j*q) / math.sqrt(10.0)

def symbols_to_bits(rx: np.ndarray, name: str) -> np.ndarray:
    if name == "BPSK":
        return (rx.real >= 0).astype(np.uint8)
    if name == "QPSK":
        return np.column_stack((rx.real >= 0, rx.imag >= 0)).astype(np.uint8).reshape(-1)
    # Nearest normalized 4-PAM level independently on I and Q.
    raw_i = rx.real * math.sqrt(10.0)
    raw_q = rx.imag * math.sqrt(10.0)
    levels = np.array([-3., -1., 1., 3.])
    gray = {-3.0:(0,0), -1.0:(0,1), 1.0:(1,1), 3.0:(1,0)}
    oi = levels[np.abs(raw_i[:,None]-levels[None,:]).argmin(axis=1)]
    oq = levels[np.abs(raw_q[:,None]-levels[None,:]).argmin(axis=1)]
    out = np.empty((len(rx),4), dtype=np.uint8)
    for idx, (a,b) in enumerate(zip(oi,oq)):
        out[idx] = (*gray[float(a)], *gray[float(b)])
    return out.reshape(-1)

def simulate(name: str, ebn0_db: float, nbits: int, rng: np.random.Generator):
    k = {"BPSK":1, "QPSK":2, "16QAM":4}[name]
    nbits = (nbits // k) * k
    bits = rng.integers(0, 2, nbits, dtype=np.uint8)
    tx = bits_to_symbols(bits, name)
    ebn0 = 10.0 ** (ebn0_db / 10.0)
    n0 = 1.0 / (k * ebn0)
    noise_sigma = math.sqrt(n0 / 2.0)
    if name == "BPSK":
        rx = tx + rng.normal(0.0, noise_sigma, len(tx))
    else:
        noise = noise_sigma * (rng.normal(size=len(tx)) + 1j*rng.normal(size=len(tx)))
        rx = tx + noise
    detected = symbols_to_bits(rx, name)
    errors = int(np.count_nonzero(bits != detected))
    evm = float(np.sqrt(np.mean(np.abs(rx-tx)**2) / np.mean(np.abs(tx)**2)))
    lo, hi = wilson_interval(errors, nbits)
    return {"modulation":name, "ebn0_db":ebn0_db, "bits":nbits,
            "bit_errors":errors, "ber":errors/nbits, "ber_ci95_low":lo,
            "ber_ci95_high":hi, "theory_ber":theory_ber(name, ebn0_db),
            "evm_rms":evm, "evm_percent":100*evm,
            "spectral_efficiency_bits_per_symbol":k}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bits", type=int, default=1_000_000, help="bits per modulation/SNR point")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--ebn0", type=float, nargs="+", default=[0,2,4,6,8,10,12])
    ap.add_argument("--out", type=Path, default=Path("results/advanced"))
    args = ap.parse_args()
    if args.bits < 100 or args.bits > 100_000_000:
        ap.error("--bits must be between 100 and 100000000")
    args.out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(args.seed)
    rows=[]
    for name in MODULATIONS:
        for snr in args.ebn0:
            row=simulate(name, float(snr), args.bits, rng)
            rows.append(row)
            print(f"{name:5s} Eb/N0={snr:>5.1f} dB | BER={row['ber']:.6g} "
                  f"[95% {row['ber_ci95_low']:.3g}, {row['ber_ci95_high']:.3g}] "
                  f"| theory≈{row['theory_ber']:.6g} | EVM={row['evm_percent']:.2f}%")
    csv_path=args.out/"link_performance.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer=csv.DictWriter(f, fieldnames=["modulation","ebn0_db","bits","bit_errors","ber",
          "ber_ci95_low","ber_ci95_high","theory_ber","evm_rms","evm_percent",
          "spectral_efficiency_bits_per_symbol","seed"])
        writer.writeheader()
        for row in rows:
            row["seed"]=args.seed
            writer.writerow(row)
    try:
        import matplotlib.pyplot as plt
        fig,ax=plt.subplots(figsize=(9,6))
        for name in MODULATIONS:
            group=[r for r in rows if r["modulation"]==name]
            x=[r["ebn0_db"] for r in group]
            y=[max(r["ber"], 0.5/r["bits"]) for r in group]
            t=[r["theory_ber"] for r in group]
            ax.semilogy(x,y,"o-",label=f"{name} Monte Carlo")
            ax.semilogy(x,t,"--",label=f"{name} analytical")
        ax.set(title="AWGN Link Performance: BER vs Eb/N0",
               xlabel="Eb/N0 (dB)",ylabel="Bit Error Rate")
        ax.grid(True,which="both",alpha=.3); ax.legend(); fig.tight_layout()
        fig.savefig(args.out/"ber_comparison.png",dpi=220); plt.close(fig)
        print(f"Plot: {args.out/'ber_comparison.png'}")
    except ImportError:
        print("Matplotlib not installed; skipped plot (CSV was written).")
    print(f"CSV: {csv_path}")

if __name__ == "__main__":
    main()
