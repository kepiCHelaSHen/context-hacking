# Dead Ends — Schroeder/Freeverb Reverb

## DEAD END 1 — Schroeder (1962) original delay values
**What was attempted**: Used 4 comb filters at 1557, 1617, 1491, 1422 samples
**Result**: Metallic coloring at 44.1kHz — audible ringing, visible spectral peaks
**Why this is a dead end**: These values were tuned for ~25kHz era equipment.
At 44.1kHz they produce coincident harmonics that create comb-filter artifacts.
**Do NOT repeat**: Always use Freeverb's 8 comb values: 1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617

## DEAD END 2 — Formula-derived delay lengths
**What was attempted**: Computed delays as round(SR * T60 / n) for n=1..8
**Result**: Evenly-spaced delays share common factors (GCD > 1), producing
periodic spectral peaks that sound metallic
**Why this is a dead end**: The Freeverb values are hand-tuned, not formula-derived.
No mathematical formula reproduces them.
**Do NOT repeat**: Do not derive delay lengths from formulas. Use the exact frozen values.

## DEAD END 3 — Moorer (1979) reverb architecture
**What was attempted**: Used 6 comb filters with Moorer's delay values + early reflections
**Result**: Different reverb character (Moorer adds early reflection taps).
Not wrong per se, but a DIFFERENT algorithm than Freeverb.
**Why this is a dead end**: The spec requires Jezar's Freeverb, not Moorer reverb.
**Do NOT repeat**: Do not add early reflection taps. Freeverb has no early reflections.
