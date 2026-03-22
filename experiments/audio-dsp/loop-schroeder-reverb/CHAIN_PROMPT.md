# Schroeder/Freeverb Reverb — Design Decisions

## DD01 — Architecture
Jezar's Freeverb: 8 parallel comb filters feeding 4 series allpass filters.
No early reflections. No pre-delay. Pure late reverb tail.

## DD02 — Delay Line Lengths
FROZEN: comb = [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617]
FROZEN: allpass = [556, 441, 341, 225]
Source: Jezar's public domain C++ implementation.
These values are NOT derivable from Schroeder (1962) or any formula.

## DD03 — Signal Flow
Input → gain (0.015) → 8 parallel combs (summed) → 4 series allpasses → output
Each comb: circular buffer + damped feedback (room_size * filtered)
Each allpass: circular buffer + fixed 0.5 feedback

## DD04 — Damping
Low-pass filter in comb feedback loop:
  filtered = output * (1 - damp) + last_filtered * damp
This simulates air absorption (high frequencies decay faster).

## DD05 — Stereo
Right channel delays = left + stereospread (23 samples).
This breaks symmetry and creates spatial width.

## DD06 — Test Methodology
Impulse response analysis:
1. Feed single-sample impulse (1.0 followed by zeros)
2. Capture output for 2-3 seconds
3. Compute FFT → check spectral flatness (no metallic peaks)
4. Estimate RT60 from energy decay curve
5. Compare against "textbook" implementation visually
