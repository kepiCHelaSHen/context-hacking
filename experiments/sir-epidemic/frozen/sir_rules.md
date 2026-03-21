# Stochastic SIR Epidemic — Frozen Specification
# Grounded in: Kermack & McKendrick (1927), Gillespie (1977), Allen (2008)
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

A stochastic individual-based SIR (Susceptible-Infected-Recovered) model.
Each agent is a discrete individual with an explicit disease state. Transmission
and recovery are STOCHASTIC EVENTS, not deterministic rate equations.

The key scientific point: the deterministic SIR has an exact analytical solution
(the epidemic threshold at R0=1). The stochastic version shows FADEOUT — the
disease can go extinct before reaching endemic equilibrium in small populations.
LLMs that generate from priors will produce deterministic SIR dynamics. The
frozen spec requires stochastic individual-level dynamics with fadeout.

================================================================================
AGENTS
================================================================================

Each agent has one state: S (susceptible), I (infected), or R (recovered).

State transitions (per tick, per agent):
  S → I: infection. Probability per S agent per tick =
         1 - (1 - BETA)^(number of I contacts)
         where contacts are drawn from the agent's interaction set.

  I → R: recovery. Probability per I agent per tick = GAMMA.

  R → R: recovered agents are permanently immune (no waning).

  NOTE: The infection formula uses the COMPLEMENT method:
    p_escape = (1 - BETA)^n_infected_contacts
    p_infect = 1 - p_escape
  This is the correct stochastic per-contact transmission model.
  The DETERMINISTIC approximation is p_infect = BETA * n_infected / N.
  These give DIFFERENT results at small N. The frozen spec uses the
  complement method.

================================================================================
INTERACTION STRUCTURE
================================================================================

MIXING: Each agent contacts K other agents per tick, drawn uniformly at random
  from the full population (homogeneous mixing).

  K = CONTACTS_PER_TICK (default: 10)

  NOTE: This is a FIXED number of contacts per tick, not a rate.
  Deterministic SIR uses a rate (beta * S * I / N per tick).
  The fixed-contact model produces different dynamics at small N.

================================================================================
PARAMETERS (FROZEN)
================================================================================

  N: 500                          # population size
  INITIAL_INFECTED: 5             # I(0)
  BETA: 0.03                      # per-contact transmission probability
  GAMMA: 0.10                     # per-tick recovery probability
  CONTACTS_PER_TICK: 10           # contacts per agent per tick
  MAX_TICKS: 300                  # maximum simulation duration
  SEED: configurable

DERIVED:
  R0 = BETA * CONTACTS_PER_TICK * (1 / GAMMA)
     = 0.03 * 10 * 10
     = 3.0

  NOTE: R0 = 3.0 is well above the epidemic threshold (R0 > 1), so the
  deterministic model predicts a full epidemic affecting ~94% of the
  population (1 - 1/R0 = 0.67 herd immunity threshold, final size ~94%).

  The stochastic model at N=500 with I(0)=5 shows FADEOUT in approximately
  5-15% of runs: the initial infected recover before spreading widely.
  The deterministic model predicts 0% fadeout.

================================================================================
METRICS
================================================================================

  peak_infected: maximum number of simultaneously infected agents
  peak_tick: tick at which peak occurs
  final_recovered: total number recovered at end (= total epidemic size)
  final_size_fraction: final_recovered / N
  fadeout: boolean — did I(t) reach 0 before infecting > 20% of population?
  fadeout_rate: fraction of seeds where fadeout occurred
  epidemic_curve: per-tick I(t) trajectory
  r0_recovered: inferred R0 from early exponential growth phase

================================================================================
EXPECTED DYNAMICS
================================================================================

DETERMINISTIC PREDICTION (what LLMs will generate from priors):
  - Smooth bell-shaped epidemic curve
  - Peak at ~tick 15-25 depending on parameterization
  - Final size: ~94% of population infected (for R0=3.0)
  - Fadeout rate: 0% (the ODE always produces an epidemic for R0 > 1)

STOCHASTIC REALITY (what the frozen spec produces):
  - Noisy epidemic curve with tick-to-tick variation
  - Peak timing varies across seeds
  - Final size: mean ~85-92% (slightly below deterministic due to stochastic effects)
  - FADEOUT RATE: 5-15% at N=500, I(0)=5
  - When fadeout occurs, it happens in the first 10-20 ticks (before exponential growth)

  The key falsifiable prediction: FADEOUT RATE > 0. If the model reports 0%
  fadeout across 30 seeds, it implemented deterministic SIR dynamics.

================================================================================
DETERMINISTIC CONTAMINATION WARNING
================================================================================

The deterministic SIR equations are:
  dS/dt = -beta * S * I / N
  dI/dt = beta * S * I / N - gamma * I
  dR/dt = gamma * I

LLMs WILL generate these equations when asked for "SIR model." The frozen spec
is NOT these equations — it is an individual-based model where each agent has a
discrete state and transitions are stochastic events.

Signs of deterministic contamination:
  - Variables named S, I, R as floats (not integer counts of discrete agents)
  - Infection computed as beta * S * I / N (rate equation, not per-contact)
  - Smooth epidemic curve (no tick-to-tick noise)
  - Fadeout rate = 0%
  - Final size exactly matching 1 - 1/R0 formula

If ANY of these signs appear, the Builder generated from the deterministic prior.
