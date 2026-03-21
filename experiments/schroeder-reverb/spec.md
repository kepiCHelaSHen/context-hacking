# Schroeder/Freeverb Reverb — CHP Experiment Specification

## Research Question

Does the CHP protocol catch when an LLM generates textbook Schroeder reverb
values instead of the specific Freeverb delay line lengths? Can the difference
be measured audibly and visually via spectrogram analysis?

## What to Build

1. `reverb.py` — The Freeverb implementation
   - CombFilter class (circular delay buffer, damped feedback)
   - AllpassFilter class (circular delay buffer, fixed 0.5 feedback)
   - Freeverb class (8 parallel combs → 4 series allpasses)
   - process(input_samples) → output_samples
   - All delay lengths from frozen/reverb_rules.md EXACTLY
   - Sample rate: 44,100 Hz
   - All parameters from frozen spec (gain=0.015, room_size=0.5, damp=0.5)

2. `run_experiment.py` — Experiment runner
   - Generate test signal: impulse (single sample = 1.0, rest = 0.0)
   - Process through Freeverb → impulse response
   - Compute spectrogram of impulse response
   - Compute comb-filter peak analysis (FFT, find peaks)
   - Optionally: process a short drum hit or click track
   - Output: WAV files, spectrogram PNG, peak analysis CSV

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — CombFilter, AllpassFilter, basic signal flow, smoke test
2. METRICS — Impulse response, spectrogram, comb peak analysis, RT60 estimate
3. COMPARISON — Build a "textbook Schroeder" version with wrong values,
   compare spectrogram/audio against Freeverb spec version
4. CONVERGENCE BATTERY — 3 test signals (impulse, click, noise burst),
   verify spectral flatness, RT60, and absence of metallic coloring

## Frozen Code Compliance

Every delay line length in reverb.py MUST match frozen/reverb_rules.md exactly:
  COMB_DELAYS = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
  ALLPASS_DELAYS = [556, 441, 341, 225]
  ALLPASS_FEEDBACK = 0.5
  GAIN = 0.015
  STEREO_SPREAD = 23

The Critic will verify by diffing the implementation against the frozen spec.

## Expected False Positive (pre-loaded for demo)

The Builder will generate ONE of these wrong implementations:

1. **Schroeder 1962 values** — 4 combs (1557, 1617, 1491, 1422) + 2 allpasses.
   These are the most common textbook values. They'll produce audible metallic
   ringing at 44.1kHz because they were tuned for ~25kHz.

2. **Formula-derived values** — delay_n = round(SR * T / n). These share
   common factors and produce visible comb-filter peaks in the spectrogram.

3. **Correct count but wrong values** — 8 combs, but with different delay
   lengths (e.g., from JC Reverb, MVerb, or another implementation).

In all cases, the spectrogram will show the difference:
- Wrong values → sharp spectral peaks (metallic coloring)
- Correct Freeverb values → smooth spectral decay (natural sound)

## Visual Output

Two spectrograms side by side:
- LEFT: "What the LLM built" (textbook values) — visible comb peaks
- RIGHT: "What the spec says" (Freeverb values) — smooth decay

This is the money shot. The metallic coloring is VISIBLE in the spectrogram
and AUDIBLE in the WAV file. Two senses confirming the same drift.

## Why This Is Ungameable

Even if someone knows "use prime delay lengths" or "use Freeverb," they need
the EXACT values: 1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617.
These are not derivable from any formula. They were hand-tuned by Jezar.
The LLM cannot guess them. It must read the frozen spec or it will drift.
