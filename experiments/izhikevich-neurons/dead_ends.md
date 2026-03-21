# Izhikevich Neurons — Dead Ends Log

---

## DEAD END 1 — Hodgkin-Huxley model instead of Izhikevich

**What was attempted**: Builder generated the Hodgkin-Huxley equations with
4 state variables (V, m, h, n), conductance parameters (gNa=120, gK=36, gL=0.3),
and reversal potentials (ENa=50, EK=-77, EL=-54.4).

**Result**: The model produces spikes but is the WRONG MODEL. Hodgkin-Huxley
has 4 differential equations per neuron; Izhikevich has 2. The parameter sets
(a,b,c,d) from the frozen spec cannot be applied to HH. The firing patterns
(RS, IB, CH, FS, LTS) are defined specifically for the Izhikevich model.

**Why this is a dead end**: "Spiking neuron" triggers the HH prior in LLMs
because HH is the most famous model in neuroscience. The frozen spec explicitly
requires the Izhikevich model: v' = 0.04v^2 + 5v + 140 - u + I, u' = a(bv - u).

**Do NOT repeat**: Any model with variables named m, h, n, or parameters named
gNa, gK, gL. Any model with more than 2 state variables per neuron.

---

## DEAD END 2 — Single full Euler step (dt=1.0) instead of two half-steps (dt=0.5)

**What was attempted**: Builder used standard Euler with dt=1.0 ms:
  v = v + (0.04*v^2 + 5*v + 140 - u + I) * 1.0

**Result**: At high v (near 30 mV), the v^2 term causes numerical overshoot.
Spike timing is shifted by 2-5% compared to the half-step method. For the
fast-spiking (FS) pattern, this timing error accumulates and changes the
spike count over 1000 ms.

**Why this is a dead end**: Izhikevich (2003) explicitly recommends two
half-steps for numerical stability:
  v += 0.5*(0.04*v^2 + 5*v + 140 - u + I)
  v += 0.5*(0.04*v^2 + 5*v + 140 - u + I)
  u += a*(b*v - u)

**Do NOT repeat**: Single-step Euler with dt >= 1.0 on the Izhikevich model.

---

## DEAD END 3 — Wrong v^2 coefficient (0.05 instead of 0.04)

**What was attempted**: Builder generated v' = 0.05*v^2 + 5*v + 140 - u + I
(coefficient 0.05 instead of the frozen 0.04).

**Result**: The 0.05 coefficient changes the spike threshold and resting
potential. The neuron fires at a lower current threshold and the ISI pattern
shifts. This is subtle — the model still "works" but produces different
dynamics than the published Izhikevich (2003) model.

**Why this is a dead end**: LLMs generate similar-but-wrong coefficients
from training priors. The frozen spec says 0.04, 5, 140 exactly. These are
NOT arbitrary — they were fitted by Izhikevich to match cortical neuron
electrophysiology.

**Do NOT repeat**: Any v^2 coefficient other than 0.04. Any v coefficient
other than 5. Any constant other than 140.
