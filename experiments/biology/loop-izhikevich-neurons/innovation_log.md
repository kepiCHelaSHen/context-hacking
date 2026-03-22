# Izhikevich Neurons — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — neuron class, integration, spike detection (Milestone 1)
  → Watch for: Hodgkin-Huxley equations (Dead End 1), 4 variables instead of 2
  → EXPECTED FALSE POSITIVE: correct spikes but WRONG MODEL (HH not Izhikevich)
Turn 2: Firing patterns — RS, IB, CH, FS, LTS with ISI stats (Milestone 2)
  → Watch for: dt=1.0 instead of dt=0.5 half-step (Dead End 2)
Turn 3: Integration comparison — half-step vs single-step (Milestone 3)
Turn 4: Convergence battery — 30 seeds x 5 patterns (Milestone 4)
