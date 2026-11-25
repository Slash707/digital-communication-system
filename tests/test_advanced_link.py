import importlib.util
from pathlib import Path
import numpy as np

MODULE_PATH = Path(__file__).parents[1] / "research" / "link_performance.py"
spec = importlib.util.spec_from_file_location("link_performance", MODULE_PATH)
lp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lp)

def test_wilson_interval_contains_observed_rate():
    low, high = lp.wilson_interval(12, 1000)
    assert low <= 0.012 <= high

def test_zero_errors_has_nonzero_uncertainty():
    low, high = lp.wilson_interval(0, 10000)
    assert low == 0
    assert high > 0

def test_bpsk_and_qpsk_theory_match():
    for snr in (0, 2, 6, 10):
        assert lp.theory_ber("BPSK", snr) == lp.theory_ber("QPSK", snr)

def test_all_modulations_have_unit_average_energy():
    rng = np.random.default_rng(7)
    for name, k in (("BPSK",1), ("QPSK",2), ("16QAM",4)):
        bits = rng.integers(0, 2, 40000, dtype=np.uint8)
        symbols = lp.bits_to_symbols(bits, name)
        assert abs(float(np.mean(np.abs(symbols)**2)) - 1.0) < 0.03

def test_noiseless_round_trip_all_modulations():
    rng = np.random.default_rng(9)
    for name, k in (("BPSK",1), ("QPSK",2), ("16QAM",4)):
        bits = rng.integers(0, 2, 4000, dtype=np.uint8)
        recovered = lp.symbols_to_bits(lp.bits_to_symbols(bits, name), name)
        assert np.array_equal(bits, recovered)

def test_simulation_reports_finite_statistics():
    row = lp.simulate("QPSK", 5.0, 20000, np.random.default_rng(11))
    assert 0 <= row["ber"] <= 1
    assert row["ber_ci95_low"] <= row["ber_ci95_high"]
    assert row["evm_rms"] >= 0
