# Schroeder/Freeverb Reverb — CHP Experiment Report

## Result: PASS (4/4 milestones)

## Frozen Compliance
- Comb delays: [1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617] — EXACT MATCH
- Allpass delays: [556, 441, 341, 225] — EXACT MATCH
- Allpass feedback: 0.5 — MATCH
- Gain: 0.015 — MATCH
- 8 comb filters — MATCH (not 4)
- 4 allpass filters — MATCH (not 2)

## Metrics
| Metric | Freeverb (Spec) | Textbook (Prior) |
|--------|----------------|-----------------|
| Spectral flatness | 0.5001 | 0.5579 |
| RT60 | 0.33s | 0.41s |
| Comb filters | 8 | 4 |
| Allpass filters | 4 | 2 |
| Damping | Yes (LP filter) | No |
| Metallic coloring | None visible | Visible comb peaks |

## Prior-as-Detector Confirmation

The TextbookSchroeder implementation produces:
- 4 combs instead of 8 (Schroeder 1962 original)
- 2 allpasses instead of 4
- No damping (undamped feedback)
- Higher gain (0.1 vs 0.015)
- Wrong allpass feedback (0.7 vs 0.5)

These are EXACTLY the values an LLM would produce when asked to
"implement a Schroeder reverb." They come from the 1962 paper,
which is in every DSP textbook and therefore in every LLM's training data.

The visual difference (see figures/reverb_comparison.png):
- Freeverb: dense, smooth impulse response → natural-sounding reverb
- Textbook: sparse, spiky impulse response → metallic, ringing reverb

## Gate Scores
- Frozen compliance: 1.00 (all values match exactly)
- Architecture: 0.95
- Scientific validity: 0.95
- Drift check: 1.00

## Why This Experiment Is Ungameable

Even knowing "use Freeverb" or "use 8 comb filters" does not help.
The SPECIFIC delay values (1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617)
are not derivable from any formula. They were hand-tuned by Jezar for
44,100 Hz. The LLM must read the frozen spec to produce them.
