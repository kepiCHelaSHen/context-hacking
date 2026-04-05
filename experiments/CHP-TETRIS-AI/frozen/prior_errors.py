"""Known LLM error patterns for Tetris heuristic weights."""

KNOWN_TRAPS = [
    {
        "name": "Line-Clear Greed Trap",
        "detect": lambda w: (
            abs(w.get("complete_lines", 0)) > abs(w.get("holes", 0))
            and abs(w.get("holes", 0)) < 2.0
        ),
        "description": (
            "LLMs consistently over-weight complete_lines and under-weight holes. "
            "This creates a greedy player that chases line clears while burying holes, "
            "leading to rapid stack death."
        ),
        "correction_hint": (
            "The hole penalty should be 3-5x stronger than the line clear reward. "
            "Holes are catastrophic; line clears are nice-to-have."
        ),
    },
]
