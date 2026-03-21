"""
Metal Harmony Analyzer — CHP Implementation
Frozen spec: frozen/metal_harmony_rules.md

Analyzes metal riffs using METAL theory, NOT classical theory.
Power chords are correct. Parallel fifths are correct. Tritones are features.
Modal analysis, NOT functional (no Roman numerals).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum

import numpy as np

_log = logging.getLogger(__name__)

# ── Note representation ──────────────────────────────────────────────────────

NOTE_NAMES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]

# Drop D tuning: D2-A2-D3-G3-B3-E4 (MIDI numbers)
DROP_D_OPEN = [38, 45, 50, 55, 59, 64]  # D2, A2, D3, G3, B3, E4
STANDARD_OPEN = [40, 45, 50, 55, 59, 64]  # E2, A2, D3, G3, B3, E4


class Tuning(Enum):
    DROP_D = "drop_d"
    STANDARD = "standard"


def note_name(midi: int) -> str:
    return NOTE_NAMES[midi % 12]


def interval_semitones(note1: int, note2: int) -> int:
    return (note2 - note1) % 12


# ── Modes ────────────────────────────────────────────────────────────────────

MODES = {
    "ionian":     [0, 2, 4, 5, 7, 9, 11],
    "dorian":     [0, 2, 3, 5, 7, 9, 10],
    "phrygian":   [0, 1, 3, 5, 7, 8, 10],
    "lydian":     [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "aeolian":    [0, 2, 3, 5, 7, 8, 10],
    "locrian":    [0, 1, 3, 5, 6, 8, 10],
}


def detect_mode(notes: list[int], root: int) -> tuple[str, float]:
    """Detect the most likely mode given a set of notes and a root.

    Returns (mode_name, confidence) where confidence is the fraction
    of notes that fit the mode's scale.
    """
    pitch_classes = set((n - root) % 12 for n in notes)
    best_mode = "chromatic"
    best_score = 0.0

    for mode_name, intervals in MODES.items():
        mode_set = set(intervals)
        if not pitch_classes:
            continue
        overlap = len(pitch_classes & mode_set)
        score = overlap / len(pitch_classes)
        if score > best_score:
            best_score = score
            best_mode = mode_name

    return best_mode, best_score


# ── Power Chord Detection ────────────────────────────────────────────────────

@dataclass
class Chord:
    notes: list[int]  # MIDI numbers
    root: int = 0
    name: str = ""
    is_power_chord: bool = False

    def __post_init__(self):
        if self.notes:
            self.root = min(self.notes)
            intervals = sorted(set((n - self.root) % 12 for n in self.notes))
            # Power chord: root + P5 (+ optional octave). NO third.
            if set(intervals) <= {0, 7}:
                self.is_power_chord = True
                self.name = f"{note_name(self.root)}5"
            elif 3 in intervals or 4 in intervals:
                # Has a third — not a power chord
                self.is_power_chord = False
                if 4 in intervals:
                    self.name = f"{note_name(self.root)}maj"
                elif 3 in intervals:
                    self.name = f"{note_name(self.root)}min"
            else:
                self.name = f"{note_name(self.root)}(?)"


# ── Riff Analysis ────────────────────────────────────────────────────────────

@dataclass
class RiffAnalysis:
    name: str
    chords: list[Chord]
    key_center: int  # MIDI root
    mode: str
    mode_confidence: float
    intervals_from_root: list[int]  # semitones from key center
    has_parallel_fifths: bool
    parallel_fifths_correct: bool  # True in metal context
    has_tritone: bool
    tritone_is_feature: bool  # True in metal context
    is_functional: bool  # False for metal (modal, not functional)
    classical_errors: list[str]  # "errors" that classical theory would flag
    metal_assessment: str  # correct analysis under metal theory


def analyze_riff(
    name: str,
    chord_notes: list[list[int]],
    key_center: int,
    tuning: Tuning = Tuning.DROP_D,
) -> RiffAnalysis:
    """Analyze a riff using METAL theory (not classical)."""

    chords = [Chord(notes=n) for n in chord_notes]

    # Intervals from key center
    intervals = [(c.root - key_center) % 12 for c in chords]

    # Mode detection
    all_notes = [n for c in chords for n in c.notes]
    mode, mode_conf = detect_mode(all_notes, key_center)

    # Parallel fifths: consecutive power chords moving in same direction
    has_parallel_fifths = False
    if len(chords) >= 2:
        for i in range(len(chords) - 1):
            if chords[i].is_power_chord and chords[i + 1].is_power_chord:
                if chords[i].root != chords[i + 1].root:
                    has_parallel_fifths = True
                    break

    # Tritone detection (6 semitones)
    has_tritone = False
    for i in range(len(chords)):
        for j in range(i + 1, len(chords)):
            if interval_semitones(chords[i].root, chords[j].root) == 6:
                has_tritone = True
                break

    # Classical errors (things classical theory would flag as wrong)
    classical_errors = []
    if has_parallel_fifths:
        classical_errors.append("parallel fifths (forbidden in classical voice leading)")
    if has_tritone:
        classical_errors.append("unresolved tritone (should resolve in classical)")
    if mode in ("phrygian", "locrian"):
        classical_errors.append(f"{mode} mode (rare/avoided in common practice)")
    for c in chords:
        if c.is_power_chord:
            classical_errors.append(f"incomplete chord {c.name} (missing third)")

    # Metal assessment (correct analysis)
    metal_parts = []
    if all(c.is_power_chord for c in chords):
        metal_parts.append("power chord progression")
    if has_parallel_fifths:
        metal_parts.append("parallel fifths (idiomatic metal technique)")
    if has_tritone:
        metal_parts.append("tritone emphasis (feature, not error)")
    metal_parts.append(f"{mode} mode (key center: {note_name(key_center)})")

    return RiffAnalysis(
        name=name,
        chords=chords,
        key_center=key_center,
        mode=mode,
        mode_confidence=mode_conf,
        intervals_from_root=intervals,
        has_parallel_fifths=has_parallel_fifths,
        parallel_fifths_correct=has_parallel_fifths,  # CORRECT in metal
        has_tritone=has_tritone,
        tritone_is_feature=has_tritone,  # FEATURE in metal
        is_functional=False,  # metal is MODAL, not functional
        classical_errors=classical_errors,
        metal_assessment="; ".join(metal_parts),
    )


# ── The 5 Pantera Reference Riffs ────────────────────────────────────────────

D2 = 38; Eb2 = 39; E2 = 40; F2 = 41; Gb2 = 42; G2 = 43; Ab2 = 44
A2 = 45; Bb2 = 46; B2 = 47; C3 = 48; Db3 = 49; D3 = 50

def pantera_walk() -> RiffAnalysis:
    """Walk (Vulgar Display of Power, 1992) — chromatic descent in D."""
    return analyze_riff(
        "Walk",
        [[D2, A2, D3], [Db3-12, Ab2, Db3], [C3-12, G2, C3],
         [B2-12, Gb2, B2], [A2-12, E2, A2]],  # D5-Db5-C5-B5-A5
        key_center=D2,
    )

def pantera_cowboys() -> RiffAnalysis:
    """Cowboys From Hell (1990) — E Phrygian."""
    return analyze_riff(
        "Cowboys From Hell",
        [[E2, B2, E2+12], [F2, C3, F2+12], [E2, B2, E2+12],
         [G2, D3, G2+12], [Gb2, Db3, Gb2+12], [E2, B2, E2+12]],
        key_center=E2,
    )

def pantera_domination() -> RiffAnalysis:
    """Domination (Cowboys From Hell, 1990) — D Phrygian."""
    return analyze_riff(
        "Domination",
        [[D2, A2, D3], [Eb2, Bb2, Eb2+12], [D2, A2, D3],
         [C3-12, G2, C3], [D2, A2, D3]],
        key_center=D2,
    )

def pantera_five_minutes() -> RiffAnalysis:
    """5 Minutes Alone (Far Beyond Driven, 1994) — D minor/Phrygian."""
    return analyze_riff(
        "5 Minutes Alone",
        [[D2, A2, D3], [F2, C3, F2+12], [Eb2, Bb2, Eb2+12], [D2, A2, D3]],
        key_center=D2,
    )

def pantera_mouth_for_war() -> RiffAnalysis:
    """Mouth for War (Vulgar Display of Power, 1992) — E with tritone."""
    return analyze_riff(
        "Mouth for War",
        [[E2, B2, E2+12], [G2, D3, G2+12], [A2, E2+12, A2+12],
         [E2, B2, E2+12], [Bb2, F2+12, Bb2+12], [A2, E2+12, A2+12]],
        key_center=E2,
    )

REFERENCE_RIFFS = {
    "walk": pantera_walk,
    "cowboys": pantera_cowboys,
    "domination": pantera_domination,
    "five_minutes": pantera_five_minutes,
    "mouth_for_war": pantera_mouth_for_war,
}


def run_simulation(seed: int = 42) -> dict:
    """Analyze all 5 Pantera reference riffs and return metrics."""
    rng = np.random.default_rng(seed)
    results = {}

    power_chord_correct = 0
    parallel_fifth_correct = 0
    mode_correct = 0
    tritone_correct = 0
    functional_contamination = 0
    total_riffs = 0

    expected_modes = {
        "walk": "aeolian",
        "cowboys": "phrygian",
        "domination": "phrygian",
        "five_minutes": "phrygian",
        "mouth_for_war": "aeolian",
    }

    for riff_name, riff_fn in REFERENCE_RIFFS.items():
        analysis = riff_fn()
        total_riffs += 1

        # Power chord detection
        n_power = sum(1 for c in analysis.chords if c.is_power_chord)
        if n_power == len(analysis.chords):
            power_chord_correct += 1

        # Parallel fifths handled correctly (marked as correct, not error)
        if analysis.has_parallel_fifths and analysis.parallel_fifths_correct:
            parallel_fifth_correct += 1

        # Mode detection
        expected = expected_modes.get(riff_name, "")
        if analysis.mode == expected:
            mode_correct += 1

        # Tritone as feature
        if analysis.has_tritone and analysis.tritone_is_feature:
            tritone_correct += 1

        # Functional contamination check
        if analysis.is_functional:
            functional_contamination += 1

        results[riff_name] = {
            "name": analysis.name,
            "mode": analysis.mode,
            "mode_confidence": analysis.mode_confidence,
            "parallel_fifths": analysis.has_parallel_fifths,
            "parallel_fifths_correct": analysis.parallel_fifths_correct,
            "has_tritone": analysis.has_tritone,
            "tritone_feature": analysis.tritone_is_feature,
            "is_functional": analysis.is_functional,
            "classical_errors_count": len(analysis.classical_errors),
            "metal_assessment": analysis.metal_assessment,
        }

    return {
        "riff_results": results,
        "power_chord_accuracy": power_chord_correct / max(total_riffs, 1),
        "parallel_fifth_handling": parallel_fifth_correct / max(total_riffs, 1),
        "mode_accuracy": mode_correct / max(total_riffs, 1),
        "tritone_handling": tritone_correct / max(total_riffs, 1),
        "functional_contamination": functional_contamination / max(total_riffs, 1),
        "total_riffs_analyzed": total_riffs,
    }
