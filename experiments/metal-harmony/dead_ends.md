# Metal Harmony — Dead Ends Log

---

## DEAD END 1 — Classical voice leading rules on metal

**What was attempted**: Analyzer flagged parallel fifths between consecutive
power chords as "voice leading error (parallel perfect fifths)."

**Result**: Every power chord progression in metal uses parallel fifths.
Flagging them as errors produces 100% false positive rate on metal riffs.

**Why this is a dead end**: Classical rules (Kostka & Payne) forbid parallel
fifths in 4-part chorale writing. Metal is not chorale writing. Power chords
are root + P5 moved in parallel by design. The frozen spec says: parallel
fifths in power chord context = CORRECT.

**Do NOT repeat**: Any voice leading rule from classical theory applied
without checking if the context is metal.

---

## DEAD END 2 — Roman numeral functional analysis on modal riffs

**What was attempted**: Analyzer labeled "Walk" as "I - VII - bVII - VI - V"
using Roman numeral functional tonality.

**Result**: This implies functional relationships (dominant preparation,
tonic resolution) that don't exist. "Walk" is a chromatic descent
harmonized with power chords. There is no "dominant" or "tonic function."

**Why this is a dead end**: Metal harmony is MODAL, not FUNCTIONAL. Roman
numerals imply I-IV-V-I logic. Metal uses riff repetition, chromatic
movement, and tritone emphasis. The frozen spec says: analysis_framework
= "modal", roman_numerals = "not_applicable."

**Do NOT repeat**: Assigning I, IV, V, vi labels to metal progressions.

---

## DEAD END 3 — Standard tuning assumption (EADGBE)

**What was attempted**: Analyzer computed intervals assuming standard guitar
tuning (EADGBE). Fret positions didn't match the expected notes.

**Result**: Pantera uses Drop D (DADGBE). The low string is D2, not E2.
Power chord shapes are different — in Drop D, a power chord is a single-finger
barre across strings 6-5-4. In standard tuning, it requires two fingers.
This changes which progressions are physically playable and idiomatic.

**Do NOT repeat**: Any analysis that doesn't check tuning first. The frozen
spec says tuning = "drop_d" (D2-A2-D3-G3-B3-E4).
