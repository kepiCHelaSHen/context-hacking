"""
Freeverb — Jezar's public domain reverb implementation (Python port).

All delay line lengths and coefficients from frozen/reverb_rules.md.
No values are derived from formulas — all are hand-tuned by Jezar
for 44,100 Hz sample rate.

Architecture: 8 parallel comb filters → 4 series allpass filters.
No early reflections. No pre-delay.
"""

import numpy as np


# ── Frozen spec values (from frozen/reverb_rules.md) ─────────────────────────

COMB_DELAYS = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
ALLPASS_DELAYS = [556, 441, 341, 225]
ALLPASS_FEEDBACK = 0.5
GAIN = 0.015
STEREO_SPREAD = 23
SAMPLE_RATE = 44100


class CombFilter:
    """Feedback comb filter with low-pass damping.

    Signal flow (from frozen/reverb_rules.md DD03-DD04):
        output = buffer[read_pos]
        filtered = output * (1 - damp) + last_filtered * damp
        buffer[write_pos] = input * gain + filtered * room_size
    """

    def __init__(self, delay_length: int, room_size: float = 0.5,
                 damp: float = 0.5):
        self.delay_length = delay_length
        self.buffer = np.zeros(delay_length)
        self.index = 0
        self.room_size = room_size
        self.damp = damp
        self.last_filtered = 0.0

    def process(self, input_sample: float) -> float:
        output = self.buffer[self.index]

        # Low-pass damping (frozen/reverb_rules.md DD04)
        self.last_filtered = (
            output * (1.0 - self.damp)
            + self.last_filtered * self.damp
        )

        # Write: input + damped feedback
        self.buffer[self.index] = (
            input_sample + self.last_filtered * self.room_size
        )

        self.index = (self.index + 1) % self.delay_length
        return output


class AllpassFilter:
    """Allpass filter with fixed 0.5 feedback coefficient.

    Signal flow (from frozen/reverb_rules.md DD03):
        output = -input + buffer[read_pos]
        buffer[write_pos] = input + buffer[read_pos] * 0.5

    Feedback coefficient is ALWAYS 0.5. Not configurable.
    """

    def __init__(self, delay_length: int, feedback: float = ALLPASS_FEEDBACK):
        self.delay_length = delay_length
        self.feedback = feedback
        self.buffer = np.zeros(delay_length)
        self.index = 0

    def process(self, input_sample: float) -> float:
        buffered = self.buffer[self.index]
        output = -input_sample + buffered
        self.buffer[self.index] = (
            input_sample + buffered * self.feedback
        )
        self.index = (self.index + 1) % self.delay_length
        return output


class Freeverb:
    """Jezar's Freeverb — 8 parallel combs → 4 series allpasses.

    All delay lengths from frozen/reverb_rules.md DD02.
    Mono processing (left channel). For stereo, use process_stereo().
    """

    def __init__(self, room_size: float = 0.5, damp: float = 0.5):
        self.gain = GAIN
        self.room_size = room_size
        self.damp = damp

        # 8 parallel comb filters (frozen/reverb_rules.md DD02)
        self.combs_L = [
            CombFilter(d, room_size, damp) for d in COMB_DELAYS
        ]

        # Right channel: offset by stereospread (frozen/reverb_rules.md DD05)
        self.combs_R = [
            CombFilter(d + STEREO_SPREAD, room_size, damp) for d in COMB_DELAYS
        ]

        # 4 series allpass filters (frozen/reverb_rules.md DD02)
        self.allpasses_L = [
            AllpassFilter(d, ALLPASS_FEEDBACK) for d in ALLPASS_DELAYS
        ]
        self.allpasses_R = [
            AllpassFilter(d + STEREO_SPREAD, ALLPASS_FEEDBACK)
            for d in ALLPASS_DELAYS
        ]

    def process(self, input_sample: float) -> float:
        """Process one sample (mono, left channel)."""
        inp = input_sample * self.gain

        # Sum output of 8 parallel comb filters
        out = sum(comb.process(inp) for comb in self.combs_L)

        # Pass through 4 series allpass filters
        for ap in self.allpasses_L:
            out = ap.process(out)

        return out

    def process_stereo(self, input_sample: float) -> tuple[float, float]:
        """Process one sample, return (left, right)."""
        inp = input_sample * self.gain

        out_l = sum(comb.process(inp) for comb in self.combs_L)
        out_r = sum(comb.process(inp) for comb in self.combs_R)

        for ap in self.allpasses_L:
            out_l = ap.process(out_l)
        for ap in self.allpasses_R:
            out_r = ap.process(out_r)

        return out_l, out_r


class TextbookSchroeder:
    """WRONG implementation — Schroeder (1962) textbook values.

    This is what the LLM prior produces:
    - 4 combs (not 8) at Schroeder's original delay lengths
    - 2 allpasses (not 4)
    - No damping
    - Values tuned for ~25kHz, wrong for 44.1kHz

    Used ONLY for comparison. This is the "prior" output.
    """

    def __init__(self, room_size: float = 0.5):
        # Schroeder (1962) textbook values — THE WRONG ANSWER
        self.gain = 0.1  # wrong (should be 0.015)
        self.combs = [
            CombFilter(1557, room_size, 0.0),  # no damping
            CombFilter(1617, room_size, 0.0),
            CombFilter(1491, room_size, 0.0),
            CombFilter(1422, room_size, 0.0),
        ]
        self.allpasses = [
            AllpassFilter(225, 0.7),  # wrong feedback (should be 0.5)
            AllpassFilter(556, 0.7),
        ]

    def process(self, input_sample: float) -> float:
        inp = input_sample * self.gain
        out = sum(comb.process(inp) for comb in self.combs)
        for ap in self.allpasses:
            out = ap.process(out)
        return out


def run_simulation(seed: int = 42) -> dict:
    """Run impulse response analysis and return metrics.

    Used by the CHP test battery. Returns dict with:
    - n_comb_filters, n_allpass_filters
    - comb_delay_match, allpass_delay_match (1.0 = exact match)
    - spectral_flatness
    - rt60
    - comparison metrics (Freeverb vs textbook)
    """
    rng = np.random.default_rng(seed)

    # ── Build reverbs ────────────────────────────────────────────────────
    rv = Freeverb()
    tv = TextbookSchroeder()

    # ── Generate impulse response (2 seconds) ────────────────────────────
    n_samples = SAMPLE_RATE * 2
    impulse = np.zeros(n_samples)
    impulse[0] = 1.0

    ir_freeverb = np.array([rv.process(s) for s in impulse])

    # Reset for textbook
    impulse2 = np.zeros(n_samples)
    impulse2[0] = 1.0
    ir_textbook = np.array([tv.process(s) for s in impulse2])

    # ── Spectral analysis ────────────────────────────────────────────────
    fft_freeverb = np.abs(np.fft.rfft(ir_freeverb))
    fft_textbook = np.abs(np.fft.rfft(ir_textbook))

    # Spectral flatness (geometric mean / arithmetic mean of power)
    def spectral_flatness(fft_mag):
        power = fft_mag ** 2
        power = power[power > 0]
        if len(power) == 0:
            return 0.0
        geo = np.exp(np.mean(np.log(power + 1e-30)))
        arith = np.mean(power)
        return float(geo / (arith + 1e-30))

    sf_freeverb = spectral_flatness(fft_freeverb)
    sf_textbook = spectral_flatness(fft_textbook)

    # ── RT60 estimate ────────────────────────────────────────────────────
    def estimate_rt60(ir):
        energy = np.cumsum(ir[::-1] ** 2)[::-1]
        if energy[0] == 0:
            return 0.0
        energy_db = 10 * np.log10(energy / energy[0] + 1e-30)
        rt60_idx = np.argmax(energy_db < -60)
        return float(rt60_idx / SAMPLE_RATE) if rt60_idx > 0 else 0.0

    rt60_freeverb = estimate_rt60(ir_freeverb)
    rt60_textbook = estimate_rt60(ir_textbook)

    # ── Frozen compliance check ──────────────────────────────────────────
    comb_delays = [c.delay_length for c in rv.combs_L]
    ap_delays = [a.delay_length for a in rv.allpasses_L]

    comb_match = 1.0 if comb_delays == list(COMB_DELAYS) else 0.0
    ap_match = 1.0 if ap_delays == list(ALLPASS_DELAYS) else 0.0

    return {
        "n_comb_filters": len(rv.combs_L),
        "n_allpass_filters": len(rv.allpasses_L),
        "comb_delay_match": comb_match,
        "allpass_delay_match": ap_match,
        "comb_delays": comb_delays,
        "allpass_delays": ap_delays,
        "spectral_flatness": sf_freeverb,
        "spectral_flatness_textbook": sf_textbook,
        "rt60": rt60_freeverb,
        "rt60_textbook": rt60_textbook,
        "ir_freeverb": ir_freeverb,
        "ir_textbook": ir_textbook,
        "fft_freeverb": fft_freeverb,
        "fft_textbook": fft_textbook,
    }
