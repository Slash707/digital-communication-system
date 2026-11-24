"""Transparent baseband digital-communication simulation primitives."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np


@dataclass
class BERResult:
    modulation: str
    ebn0_db: np.ndarray
    ber: np.ndarray
    errors: np.ndarray
    tested_bits: int


def constellation(modulation: str) -> tuple[np.ndarray, np.ndarray, int]:
    """Return (points, MSB-first bit labels, bits_per_symbol).

    Points have unit average symbol energy. QPSK and 16-QAM use Gray labels.
    """
    name = modulation.upper()
    if name == "BPSK":
        labels = np.array([[0], [1]], dtype=np.uint8)
        points = np.array([1.0 + 0j, -1.0 + 0j])
        k = 1
    elif name == "QPSK":
        labels = np.array(
            [[(n >> 1) & 1, n & 1] for n in range(4)], dtype=np.uint8
        )
        i_axis = 1 - 2 * labels[:, 0].astype(float)
        q_axis = 1 - 2 * labels[:, 1].astype(float)
        points = (i_axis + 1j * q_axis) / np.sqrt(2.0)
        k = 2
    elif name == "16QAM":
        labels = np.array(
            [[(n >> 3) & 1, (n >> 2) & 1, (n >> 1) & 1, n & 1]
             for n in range(16)],
            dtype=np.uint8,
        )
        gray_levels = np.array([3.0, 1.0, -3.0, -1.0])
        i_index = 2 * labels[:, 0] + labels[:, 1]
        q_index = 2 * labels[:, 2] + labels[:, 3]
        points = (gray_levels[i_index] + 1j * gray_levels[q_index]) / np.sqrt(10.0)
        k = 4
    else:
        raise ValueError("modulation must be BPSK, QPSK, or 16QAM")
    return points.astype(complex), labels, k


def text_to_bits(message: str) -> np.ndarray:
    """Encode ASCII-compatible text as an MSB-first uint8 bit array."""
    try:
        raw = message.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("This starter's text codec supports ordinary ASCII only.") from exc
    if not raw:
        return np.array([], dtype=np.uint8)
    return np.unpackbits(np.frombuffer(raw, dtype=np.uint8), bitorder="big")


def bits_to_text(bits: Iterable[int]) -> str:
    """Decode an MSB-first bit array into ASCII text."""
    arr = np.asarray(list(bits), dtype=np.uint8).reshape(-1)
    if np.any((arr != 0) & (arr != 1)):
        raise ValueError("bits must contain only 0 and 1")
    if arr.size % 8:
        raise ValueError("the number of bits must be a multiple of 8")
    return np.packbits(arr, bitorder="big").tobytes().decode("ascii")


def modulate_bits(bits: Iterable[int], modulation: str) -> tuple[np.ndarray, int]:
    """Group bits and map them to complex symbols; return symbols and pad count."""
    arr = np.asarray(list(bits), dtype=np.uint8).reshape(-1)
    if np.any((arr != 0) & (arr != 1)):
        raise ValueError("bits must contain only 0 and 1")
    points, _, k = constellation(modulation)
    pad_count = (-arr.size) % k
    if pad_count:
        arr = np.concatenate((arr, np.zeros(pad_count, dtype=np.uint8)))
    if arr.size == 0:
        return np.array([], dtype=complex), pad_count
    groups = arr.reshape(-1, k)
    weights = 2 ** np.arange(k - 1, -1, -1)
    indices = groups @ weights
    return points[indices], pad_count


def demodulate_symbols(
    received: Iterable[complex],
    modulation: str,
    original_bit_count: int | None = None,
) -> np.ndarray:
    """Nearest-constellation-point hard decision and bit-label recovery."""
    points, labels, _ = constellation(modulation)
    rx = np.asarray(list(received), dtype=complex).reshape(-1)
    if rx.size == 0:
        return np.array([], dtype=np.uint8)
    distances = np.abs(rx[:, None] - points[None, :]) ** 2
    nearest = np.argmin(distances, axis=1)
    bits = labels[nearest].reshape(-1)
    if original_bit_count is not None:
        if not 0 <= original_bit_count <= bits.size:
            raise ValueError("original_bit_count is outside the recovered bit range")
        bits = bits[:original_bit_count]
    return bits.astype(np.uint8)


def awgn_channel(
    transmitted: Iterable[complex],
    ebn0_db: float,
    bits_per_symbol: int,
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """Add complex AWGN for unit-average-symbol-energy constellations.

    Es = 1, Eb = Es/k, N0 = Eb / 10**(EbN0_dB/10).
    Each real noise dimension has variance N0/2.
    """
    if bits_per_symbol <= 0:
        raise ValueError("bits_per_symbol must be positive")
    if rng is None:
        rng = np.random.default_rng()
    tx = np.asarray(list(transmitted), dtype=complex)
    linear_ebn0 = 10.0 ** (ebn0_db / 10.0)
    n0 = 1.0 / (bits_per_symbol * linear_ebn0)
    sigma = np.sqrt(n0 / 2.0)
    noise = sigma * (
        rng.standard_normal(tx.shape) + 1j * rng.standard_normal(tx.shape)
    )
    return tx + noise


def run_ber_sweep(
    ebn0_db_values: Iterable[float],
    requested_bits: int = 200_000,
    modulations: tuple[str, ...] = ("BPSK", "QPSK", "16QAM"),
    seed: int = 20261124,
) -> list[BERResult]:
    """Run independent Monte Carlo BER sweeps with a reproducible RNG seed."""
    if requested_bits <= 0:
        raise ValueError("requested_bits must be positive")
    ebn0 = np.asarray(list(ebn0_db_values), dtype=float)
    results: list[BERResult] = []
    for mod_index, modulation in enumerate(modulations):
        points, _, k = constellation(modulation)
        del points
        tested_bits = (requested_bits // k) * k
        rng_bits = np.random.default_rng(seed + mod_index)
        tx_bits = rng_bits.integers(0, 2, size=tested_bits, dtype=np.uint8)
        tx_symbols, _ = modulate_bits(tx_bits, modulation)
        errors = np.zeros(ebn0.size, dtype=np.int64)
        for idx, ebn0_value in enumerate(ebn0):
            rng_noise = np.random.default_rng(seed + 1000 * (mod_index + 1) + idx)
            rx_symbols = awgn_channel(tx_symbols, float(ebn0_value), k, rng_noise)
            rx_bits = demodulate_symbols(rx_symbols, modulation, tested_bits)
            errors[idx] = np.count_nonzero(tx_bits != rx_bits)
        results.append(
            BERResult(
                modulation=modulation,
                ebn0_db=ebn0.copy(),
                ber=errors / tested_bits,
                errors=errors,
                tested_bits=tested_bits,
            )
        )
    return results
