import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src" / "python"))

from dcsim import (  # noqa: E402
    bits_to_text,
    constellation,
    demodulate_symbols,
    modulate_bits,
    text_to_bits,
)


class DigitalCommunicationTests(unittest.TestCase):
    def test_ascii_msb_first(self):
        self.assertEqual(text_to_bits("A").tolist(), [0, 1, 0, 0, 0, 0, 0, 1])
        self.assertEqual(bits_to_text(text_to_bits("HELLO OMAR")), "HELLO OMAR")

    def test_noiseless_round_trip_all_modulations(self):
        bits = np.array([0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1], dtype=np.uint8)
        for modulation in ("BPSK", "QPSK", "16QAM"):
            symbols, _ = modulate_bits(bits, modulation)
            recovered = demodulate_symbols(symbols, modulation, len(bits))
            np.testing.assert_array_equal(recovered, bits)

    def test_constellations_have_unit_average_energy(self):
        for modulation in ("BPSK", "QPSK", "16QAM"):
            points, labels, k = constellation(modulation)
            self.assertEqual(len(points), 2**k)
            self.assertAlmostEqual(float(np.mean(np.abs(points) ** 2)), 1.0, places=12)
            self.assertEqual(labels.shape, (2**k, k))

    def test_padding_is_removed(self):
        bits = np.array([1, 0, 1], dtype=np.uint8)
        symbols, pad_count = modulate_bits(bits, "QPSK")
        self.assertEqual(pad_count, 1)
        recovered = demodulate_symbols(symbols, "QPSK", len(bits))
        np.testing.assert_array_equal(recovered, bits)

    def test_invalid_modulation_raises(self):
        with self.assertRaises(ValueError):
            constellation("8PSK")


if __name__ == "__main__":
    unittest.main()
