# Frozen Specification: Schroeder/Freeverb Reverb

## Source
Jezar's Freeverb (public domain C++ implementation, ~2000).
Original theory: Schroeder (1962) "Natural Sounding Artificial Reverberation,"
J. Audio Eng. Soc., 10(3), 219-223.

## Critical Insight
Schroeder's 1962 paper specifies delay line lengths for a SPECIFIC sample rate
(NOT specified in paper, assumed ~25kHz era). Modern implementations at 44,100 Hz
require DIFFERENT delay lengths — specifically chosen as mutually prime numbers
to avoid metallic coloring from coincident comb-filter peaks.

## Freeverb Delay Line Lengths (44,100 Hz)

### 8 Parallel Comb Filters (feedback delay lines)
These are the EXACT values from Jezar's Freeverb. They are NOT Schroeder's
original values and NOT derived from any formula in the 1962 paper.

| Comb # | Delay (samples) | Delay (ms @ 44.1kHz) |
|--------|----------------|---------------------|
| 1 | 1116 | 25.31 |
| 2 | 1188 | 26.94 |
| 3 | 1277 | 28.96 |
| 4 | 1356 | 30.75 |
| 5 | 1422 | 32.24 |
| 6 | 1491 | 33.81 |
| 7 | 1557 | 35.31 |
| 8 | 1617 | 36.67 |

### 4 Series Allpass Filters
| Allpass # | Delay (samples) |
|-----------|----------------|
| 1 | 556 |
| 2 | 441 |
| 3 | 341 |
| 4 | 225 |

### Tuning Constants
| Parameter | Value | Description |
|-----------|-------|-------------|
| room_size | 0.5 | feedback coefficient (0.0-1.0) |
| damp | 0.5 | damping coefficient (0.0-1.0) |
| wet | 1/3 | wet signal level |
| dry | 0 | dry signal level (wet-only for testing) |
| width | 1.0 | stereo width |
| mode | 0 | normal (not frozen) |
| gain | 0.015 | fixed input gain |

### Stereo Offset
For stereo processing, RIGHT channel delay lines are offset by +23 samples
from the LEFT channel values. This breaks L/R symmetry and creates width.

stereospread = 23

### Feedback and Damping
Each comb filter applies:
  output = delay_line[read_pos]
  filtered = output * (1 - damp) + last_filtered * damp
  delay_line[write_pos] = input * gain + filtered * room_size

Each allpass filter applies:
  output = -input + delay_line[read_pos]
  delay_line[write_pos] = input + delay_line[read_pos] * 0.5

The allpass feedback coefficient is ALWAYS 0.5. Not configurable.

## What the LLM Prior Will Produce (the trap)

LLMs trained on DSP textbooks will produce one of these WRONG implementations:

### Wrong Answer 1: Schroeder's original values
Schroeder (1962) suggests delay lengths of:
  Combs: 1557, 1617, 1491, 1422 (only 4, not 8)
  Allpasses: 225, 556 (only 2, not 4)
These are for a ~25kHz sample rate and produce metallic coloring at 44.1kHz.

### Wrong Answer 2: Formula-derived values
Some textbooks suggest: delay_n = round(sample_rate * reverb_time / n)
This produces evenly-spaced delays that share common factors, creating
audible comb-filter peaks (metallic ringing).

### Wrong Answer 3: Random prime numbers
Some implementations use arbitrary primes. While avoiding common factors,
these don't produce the tested Freeverb sound. The specific Freeverb values
were hand-tuned by Jezar for 44.1kHz and are the de facto standard.

### Wrong Answer 4: Moorer reverb values
Moorer (1979) used 6 comb filters with different values.
These are a different reverb architecture entirely.

## Detection Method

Check the EXACT delay line values in the implementation:
- Comb 1 must be 1116 (not 1557, not a formula result)
- Must have 8 combs (not 4 or 6)
- Must have 4 allpasses (not 2)
- Allpass feedback must be 0.5 (not configurable)
- Stereo spread must be 23 (not 0 or arbitrary)
- Gain must be 0.015 (not 1.0 or 0.1)

If ANY of these values differ from the frozen spec, it's specification drift.
