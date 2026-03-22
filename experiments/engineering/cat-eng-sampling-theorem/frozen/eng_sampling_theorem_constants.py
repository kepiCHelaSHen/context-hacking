"""Nyquist-Shannon Sampling Theorem — Frozen Constants. Source: Shannon 1949, Nyquist 1928, IEEE. DO NOT MODIFY."""

# Nyquist rate:      f_s >= 2 * f_max  (MINIMUM sampling rate to avoid aliasing)
# Nyquist frequency: f_N = f_s / 2     (max frequency representable at given sample rate)
# KEY: f_s = 2 * f_max, NOT f_s = f_max
# LLM prior: uses f_s = f_max (Nyquist rate = 1x) instead of f_s = 2*f_max (Nyquist rate = 2x)

# Aliased frequency: when f_signal > f_s/2, alias = |f_signal - k*f_s| for nearest integer k
# i.e. alias = abs(f_signal - round(f_signal / f_s) * f_s)

# Audio reference values
F_MAX_AUDIO = 20000        # 20 kHz — max human hearing frequency
NYQUIST_RATE = 40000       # 40 kHz — minimum sampling rate = 2 * F_MAX_AUDIO
CD_SAMPLE_RATE = 44100     # 44.1 kHz — CD standard (margin above Nyquist rate)

# Wrong Nyquist rate (1x instead of 2x) — the #1 LLM error
NYQUIST_RATE_WRONG = 20000  # WRONG: f_s = f_max instead of 2*f_max

# Nyquist frequency for CD sample rate
CD_NYQUIST_FREQ = CD_SAMPLE_RATE / 2.0  # 22050 Hz

# Aliasing test: 25 kHz signal sampled at 30 kHz
ALIAS_SIGNAL_FREQ = 25000   # Hz — above Nyquist freq for f_s=30kHz
ALIAS_SAMPLE_RATE = 30000   # Hz — insufficient sample rate
ALIASED_FREQ = 5000         # |25000 - 1*30000| = 5000 Hz

# Aliasing test 2: verify non-aliased case
SAFE_SIGNAL_FREQ = 10000    # Hz — below Nyquist freq for f_s=30kHz (15kHz)

PRIOR_ERRORS = {
    "nyquist_1x":              "Uses f_s = f_max instead of f_s = 2*f_max — Nyquist rate is 2x, not 1x",
    "aliasing_wrong_formula":  "Wrong alias frequency calculation — must use |f_signal - k*f_s| for nearest k",
    "nyquist_freq_vs_rate":    "Confuses Nyquist frequency (f_s/2) with Nyquist rate (2*f_max) — they are related but distinct concepts",
}
