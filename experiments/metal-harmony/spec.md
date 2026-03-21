# Metal Harmony Analyzer — CHP Experiment Specification

## Research Question

Can a harmony analyzer correctly identify metal-specific techniques (power chords,
modal harmony, tritone features, parallel fifths as correct) without falling back
to classical music theory rules?

## What to Build

1. `metal_analyzer.py` — Harmony analysis engine
   - Note/interval representation (MIDI numbers, semitone distances)
   - Drop D tuning model (DADGBE)
   - Power chord detector (root + P5, no 3rd)
   - Mode identifier (Aeolian, Phrygian, Dorian, Mixolydian, Locrian)
   - Riff analyzer: classify progression type (chromatic, modal, tritone-based)
   - Voice leading checker: parallel fifths = CORRECT in power chord context
   - All 5 Pantera reference riffs analyzed against frozen spec

2. `run_experiment.py` — Test battery
   - Analyze all 5 Pantera reference riffs
   - Compare metal analyzer output vs classical analyzer output
   - Measure: how many "errors" does classical analysis produce on correct metal?
   - 30-seed test: random metal riff generator + analysis

3. `tests/test_milestone_battery.py` — Sigma-gated verification

## Milestones

1. FOUNDATION — Note representation, interval computation, Drop D tuning
2. POWER CHORDS — Detection, parallel fifth handling (mark as correct)
3. MODE DETECTION — Identify all 5 metal modes from note collections
4. RIFF ANALYSIS — Analyze all 5 Pantera riffs against frozen spec
5. CONVERGENCE — 30 generated riffs, sigma-gates, report

## Expected False Positive

At Milestone 2, the Builder will flag parallel fifths between consecutive
power chords as "voice leading error." This is the CLASSICAL PRIOR — parallel
fifths are forbidden in Bach chorales. In metal, parallel fifths are the
FUNDAMENTAL TECHNIQUE (power chord = root + P5 moved in parallel).

The Critic catches it: "The analyzer is using classical rules on metal.
Parallel fifths in power chord context must be marked CORRECT per the
frozen spec."

At Milestone 3, the Builder will try to assign Roman numeral functional
analysis (I, IV, V) to Pantera riffs. These progressions are MODAL, not
FUNCTIONAL. There is no "tonic-dominant relationship" in "Walk" — it's a
chromatic descent. The Critic catches: "Roman numerals indicate functional
tonality contamination."
