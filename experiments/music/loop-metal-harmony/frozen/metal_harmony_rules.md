# Metal Harmony Theory — Frozen Specification
# Sources: Lilja (2009) "Theory and Analysis of Classic Heavy Metal Harmony"
#          Pieslak (2008) "Sound Targets: American Soldiers and Music in Iraq"
#          Walser (1993) "Running with the Devil: Power, Gender, and Madness in Heavy Metal Music"
#          Pantera guitar tablature (official Hal Leonard publications)
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

Metal harmony is a distinct harmonic system that VIOLATES classical tonal harmony
rules deliberately and systematically. It is NOT "classical with distortion."
It has its own theory, its own voice leading rules, and its own aesthetic logic.

The key scientific point: LLMs are trained overwhelmingly on classical music theory
(Bach chorales, Kostka & Payne, Aldwell & Schachter). When asked to analyze
harmony, they generate classical rules. Applying classical rules to metal produces
systematic false errors: every power chord is "wrong" (parallel fifths), every
Phrygian riff is "wrong" (non-functional harmony), every drop-D passage is
"wrong" (non-standard tuning). The Prior-as-Detector catches this: if the
analyzer flags power chords as errors, it's using the classical prior.

================================================================================
TUNING SYSTEM
================================================================================

STANDARD METAL TUNING: Drop D (DADGBE) or lower.

  String 6 (low): D2 (73.42 Hz) — one whole step below standard E2
  String 5: A2 (110.00 Hz) — unchanged
  String 4: D3 (146.83 Hz) — unchanged
  String 3: G3 (196.00 Hz) — unchanged
  String 2: B3 (246.94 Hz) — unchanged
  String 1: E4 (329.63 Hz) — unchanged

  PANTERA SPECIFIC: Dimebag Darrell tuned to Drop D standard on most
  Cowboys From Hell and Vulgar Display of Power tracks. Far Beyond Driven
  uses Drop D tuned down additional quarter-step.

  NOTE: LLMs default to standard tuning (EADGBE) when generating music
  theory. Drop D changes which intervals are playable with a single finger
  barre, which is WHY power chords are the fundamental unit in metal.

================================================================================
POWER CHORD (the fundamental unit)
================================================================================

A power chord consists of: ROOT + PERFECT FIFTH (+ optional OCTAVE)

  In Drop D: playable as a single-finger barre across strings 6-5-4.
  Example: D5 = D2-A2-D3 (frets 0-0-0)
           E5 = E2-B2-E3 (frets 2-2-2)
           F5 = F2-C3-F3 (frets 3-3-3)

  NO THIRD. This is deliberate — the omission of the third makes the chord
  neither major nor minor, creating harmonic ambiguity that distortion
  exploits (the overtone series fills in implied harmonics).

  PARALLEL FIFTHS: Moving a power chord shape up or down the neck produces
  PARALLEL FIFTHS — consecutive perfect fifths moving in the same direction.
  In classical theory, this is FORBIDDEN (Kostka & Payne Rule 1).
  In metal, this is the FUNDAMENTAL TECHNIQUE.

  NOTE: If the analyzer flags power chord progressions as "error: parallel
  fifths," it is applying the classical prior. The frozen spec says:
  parallel fifths in power chord context = CORRECT.

================================================================================
MODAL SYSTEM (not functional tonality)
================================================================================

Metal uses MODES, not major/minor functional harmony.

  PRIMARY MODES IN METAL:
    Aeolian (natural minor):  1 2 b3 4 5 b6 b7 — standard metal minor
    Phrygian:                 1 b2 b3 4 5 b6 b7 — the "evil" sound (Pantera)
    Locrian:                  1 b2 b3 4 b5 b6 b7 — diminished (extreme metal)
    Dorian:                   1 2 b3 4 5 6 b7   — bluesy metal
    Mixolydian:               1 2 3 4 5 6 b7    — rock/power metal

  PANTERA PRIMARY: E Phrygian and D Aeolian/Dorian

  NON-FUNCTIONAL HARMONY: Metal progressions do NOT follow classical
  functional logic (I-IV-V-I). Instead they use:
    - Riff-based repetition (same power chord pattern looped)
    - Chromatic movement (half-step shifts: E5-F5-E5)
    - Tritone relationships (E5 to Bb5 — the "devil's interval")
    - Modal interchange (borrowing chords from parallel modes)

  NOTE: If the analyzer tries to assign Roman numeral functions (I, IV, V, vi)
  to metal progressions, it is applying functional tonality — the classical
  prior. The frozen spec says: metal harmony is MODAL, not FUNCTIONAL.

================================================================================
PANTERA ANALYSIS — 5 REFERENCE RIFFS (frozen)
================================================================================

RIFF 1 — "Walk" (Vulgar Display of Power, 1992)
  Tuning: Drop D
  Progression: D5 — C#5 — C5 — B5 — A5 (descending chromatic power chords)
  Mode: D natural minor / chromatic descent
  Intervals: root, m7, m6 (actual: root, b7, b6 — Aeolian context, chromatic)
  Rhythm: syncopated 16th-note chug on open D string between chords
  Analysis: Chromatic voice leading by half-step. NO functional relationship.
  NOT: "I - VII - bVII - VI - V" (classical would call this "non-functional")
  CORRECT: descending chromatic line harmonized with power chords.

RIFF 2 — "Cowboys From Hell" (Cowboys From Hell, 1990)
  Tuning: Drop D (D standard)
  Key center: E Phrygian
  Progression: E5 — F5 — E5 — G5 — F#5 — E5
  Intervals: root, b2, root, b3, 2, root (Phrygian with chromatic neighbor)
  Analysis: Phrygian mode established by the E-F half-step (b2). The b2
  resolving to root is the Phrygian "tell" — this interval is FORBIDDEN in
  classical voice leading (augmented unison) but DEFINES the Phrygian sound.
  NOT: "i - bII - i" (classical would call bII a "Neapolitan" — wrong context)
  CORRECT: Phrygian modal riff with b2 emphasis.

RIFF 3 — "Domination" (Cowboys From Hell, 1990)
  Tuning: Drop D
  Key center: D minor / Phrygian
  Progression: D5 — Eb5 — D5 — C5 — D5
  Intervals: root, b2, root, b7, root
  Analysis: Phrygian b2 (D-Eb) combined with Aeolian b7 (C). Mixed modal.
  The Eb-D half-step creates maximum tension — resolved by returning to D.

RIFF 4 — "5 Minutes Alone" (Far Beyond Driven, 1994)
  Tuning: Drop D (quarter step down)
  Key center: D
  Progression: D5 (open) — rhythmic muting — F5 — Eb5 — D5
  Intervals: root, b3, b2, root
  Analysis: Minor pentatonic fragment (root-b3) followed by Phrygian b2 descent.
  The muted strings between chord hits are PART of the harmony (percussive).

RIFF 5 — "Mouth for War" (Vulgar Display of Power, 1992)
  Tuning: Drop D
  Key center: E
  Progression: E5 — G5 — A5 — E5 — Bb5 — A5
  Intervals: root, b3, 4, root, b5, 4
  Analysis: The E-Bb TRITONE is the centerpiece — the "devil's interval."
  Classical theory forbids unresolved tritones. Metal FEATURES them.
  NOT: "i - bIII - IV - i - bV - IV" (functional analysis is meaningless here)
  CORRECT: tritone-emphasizing modal riff in E minor/Phrygian context.

================================================================================
METRICS
================================================================================

  power_chord_accuracy: correctly identify power chords (root + P5, no 3rd)
  parallel_fifth_handling: power chord parallel fifths marked CORRECT (not error)
  mode_detection: correctly identify Aeolian, Phrygian, Dorian, etc.
  functional_contamination: Roman numeral analysis should NOT be applied
  interval_accuracy: correctly identify all intervals in the 5 reference riffs
  tritone_handling: tritones marked as FEATURE (not error)
  tuning_awareness: analysis accounts for Drop D (not standard EADGBE)
  riff_classification: correctly classify each of the 5 reference riffs

================================================================================
CLASSICAL CONTAMINATION WARNING
================================================================================

Signs the analyzer is using the classical prior:
  1. Flags parallel fifths as errors
  2. Uses Roman numeral functional analysis (I, IV, V, vi)
  3. Expects resolution of tritones
  4. Assumes standard EADGBE tuning
  5. Calls bII a "Neapolitan sixth" instead of Phrygian b2
  6. Flags non-functional progressions as "non-standard"
  7. Expects smooth voice leading (metal uses LEAPS)
  8. Classifies everything as "major" or "minor" (ignoring modes)

If ANY of these appear, the analyzer is contaminated by classical training data.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  TUNING: "drop_d" (D2-A2-D3-G3-B3-E4)
  POWER_CHORD_INTERVALS: [0, 7] (root + P5 in semitones)
  PARALLEL_FIFTHS: "correct_in_metal"
  TRITONE_STATUS: "feature_not_error"
  ANALYSIS_FRAMEWORK: "modal" (NOT "functional")
  ROMAN_NUMERALS: "not_applicable"
  WALK_INTERVALS: [0, -1, -2, -3, -5] (semitones from D)
  COWBOYS_MODE: "E_phrygian"
  MOUTH_TRITONE: [0, 6] (E to Bb = 6 semitones)
