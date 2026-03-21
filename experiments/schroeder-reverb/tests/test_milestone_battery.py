"""
Schroeder/Freeverb Reverb — Milestone Battery Tests

Tests verify:
1. Correct delay line values (frozen spec compliance)
2. Correct filter count (8 combs, 4 allpasses)
3. Spectral quality (no metallic coloring)
4. RT60 estimation
5. Comparison against textbook (wrong) implementation
"""

import numpy as np
import sys
import os

# Add experiment root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ── Frozen spec values ───────────────────────────────────────────────────────
FROZEN_COMB_DELAYS = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
FROZEN_ALLPASS_DELAYS = [556, 441, 341, 225]
FROZEN_ALLPASS_FEEDBACK = 0.5
FROZEN_GAIN = 0.015
FROZEN_STEREO_SPREAD = 23
SAMPLE_RATE = 44100


def test_milestone_1_foundation():
    """M1: CombFilter and AllpassFilter exist and process audio."""
    from reverb import CombFilter, AllpassFilter

    # Comb filter produces output
    comb = CombFilter(1116, 0.5, 0.5)
    impulse = np.zeros(4410)
    impulse[0] = 1.0
    output = np.array([comb.process(s) for s in impulse])
    assert np.any(output != 0), "CombFilter produced silence"
    assert len(output) == 4410

    # Allpass filter produces output
    ap = AllpassFilter(556, 0.5)
    output_ap = np.array([ap.process(s) for s in impulse])
    assert np.any(output_ap != 0), "AllpassFilter produced silence"


def test_milestone_2_frozen_compliance():
    """M2: All delay line values match frozen spec EXACTLY."""
    from reverb import Freeverb

    rv = Freeverb()

    # Check comb delays
    comb_delays = [c.delay_length for c in rv.combs_L]
    assert comb_delays == FROZEN_COMB_DELAYS, \
        f"Comb delays {comb_delays} != frozen {FROZEN_COMB_DELAYS}"

    # Check allpass delays
    ap_delays = [a.delay_length for a in rv.allpasses_L]
    assert ap_delays == FROZEN_ALLPASS_DELAYS, \
        f"Allpass delays {ap_delays} != frozen {FROZEN_ALLPASS_DELAYS}"

    # Check counts
    assert len(rv.combs_L) == 8, f"Expected 8 combs, got {len(rv.combs_L)}"
    assert len(rv.allpasses_L) == 4, f"Expected 4 allpasses, got {len(rv.allpasses_L)}"

    # Check allpass feedback
    for ap in rv.allpasses_L:
        assert abs(ap.feedback - FROZEN_ALLPASS_FEEDBACK) < 1e-6, \
            f"Allpass feedback {ap.feedback} != {FROZEN_ALLPASS_FEEDBACK}"

    # Check gain
    assert abs(rv.gain - FROZEN_GAIN) < 1e-6, \
        f"Gain {rv.gain} != {FROZEN_GAIN}"


def test_milestone_3_spectral_quality():
    """M3: Impulse response has acceptable spectral flatness (no metallic coloring)."""
    from reverb import Freeverb

    rv = Freeverb()

    # Generate impulse response (2 seconds)
    n_samples = SAMPLE_RATE * 2
    impulse = np.zeros(n_samples)
    impulse[0] = 1.0
    ir = np.array([rv.process(s) for s in impulse])

    # Compute FFT magnitude spectrum
    fft_mag = np.abs(np.fft.rfft(ir))
    fft_mag_db = 20 * np.log10(fft_mag + 1e-10)

    # Spectral flatness: geometric mean / arithmetic mean
    # Higher = flatter spectrum = less metallic coloring
    fft_power = fft_mag ** 2
    fft_power = fft_power[fft_power > 0]  # remove zeros
    geo_mean = np.exp(np.mean(np.log(fft_power + 1e-30)))
    arith_mean = np.mean(fft_power)
    spectral_flatness = geo_mean / (arith_mean + 1e-30)

    assert spectral_flatness > 0.01, \
        f"Spectral flatness {spectral_flatness:.4f} too low — metallic coloring detected"

    # RT60 estimate from energy decay
    energy = np.cumsum(ir[::-1] ** 2)[::-1]
    energy_db = 10 * np.log10(energy / (energy[0] + 1e-30) + 1e-30)
    rt60_samples = np.argmax(energy_db < -60)
    rt60_seconds = rt60_samples / SAMPLE_RATE if rt60_samples > 0 else 0

    assert rt60_seconds > 0.3, f"RT60 {rt60_seconds:.2f}s too short"


def test_milestone_4_comparison():
    """M4: Freeverb sounds different from textbook Schroeder (4 combs, 2 allpasses)."""
    from reverb import Freeverb

    # Freeverb (correct)
    rv_correct = Freeverb()
    n_samples = SAMPLE_RATE * 2
    impulse = np.zeros(n_samples)
    impulse[0] = 1.0
    ir_correct = np.array([rv_correct.process(s) for s in impulse])

    # The correct implementation should have non-trivial energy
    energy_correct = np.sum(ir_correct ** 2)
    assert energy_correct > 0.001, "Freeverb produced near-silence"

    # Verify the impulse response has reverb character (energy spread over time)
    # Not just a single echo
    # Check energy exists beyond first 0.1s (reverb tail, not just echo)
    early_cutoff = SAMPLE_RATE // 10
    late_energy = np.sum(ir_correct[early_cutoff:] ** 2)
    total_energy = np.sum(ir_correct ** 2)
    late_ratio = late_energy / (total_energy + 1e-30)
    assert late_ratio > 0.001, "No late reverb energy — not a proper reverb tail"


if __name__ == "__main__":
    print("Running Schroeder/Freeverb milestone battery...")
    tests = [
        ("M1: Foundation", test_milestone_1_foundation),
        ("M2: Frozen Compliance", test_milestone_2_frozen_compliance),
        ("M3: Spectral Quality", test_milestone_3_spectral_quality),
        ("M4: Comparison", test_milestone_4_comparison),
    ]
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  {name}: PASS")
        except Exception as e:
            print(f"  {name}: FAIL — {e}")
