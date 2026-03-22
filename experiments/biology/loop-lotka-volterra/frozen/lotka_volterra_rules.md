# Agent-Based Lotka-Volterra — Frozen Specification
# Grounded in: Lotka (1925), Volterra (1926), Gillespie (1977)
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

An agent-based (individual-level) predator-prey model. Each animal is a discrete
agent with position, energy, and age. The dynamics approximate the classic
Lotka-Volterra ODEs but with DEMOGRAPHIC STOCHASTICITY: individual birth/death
events produce noise, extinction risk, and deviations from ODE predictions.

The key scientific point: the ODE version predicts eternal neutral oscillations.
The agent-based version shows EXTINCTIONS at small population sizes that the ODE
cannot predict. LLMs that generate from priors will produce ODE dynamics. The
frozen spec requires agent-based dynamics with stochastic extinction.

================================================================================
AGENTS
================================================================================

PREY:
  - energy: float, starts at 1.0
  - Each tick: energy += PREY_ENERGY_GAIN (grazing)
  - If energy >= PREY_REPRODUCE_THRESHOLD: split into two prey, each with
    energy = parent_energy / 2. No sexual reproduction — asexual fission.
  - Prey do NOT die of starvation (unlimited grass).
  - Prey die only when eaten by a predator.

PREDATOR:
  - energy: float, starts at 1.0
  - Each tick: energy -= PREDATOR_ENERGY_COST (metabolic cost)
  - If a prey is in the same cell: eat it. energy += PREDATOR_ENERGY_GAIN.
  - If energy >= PREDATOR_REPRODUCE_THRESHOLD: split into two predators,
    each with energy = parent_energy / 2.
  - If energy <= 0: die (starvation).

================================================================================
SPATIAL STRUCTURE
================================================================================

GRID: W x H toroidal grid (default 50 x 50).
MOVEMENT: Each agent moves to a random adjacent cell (4-connected: up/down/left/right)
  each tick. Movement is random, not directed.

ENCOUNTER: A predator in the same cell as a prey eats ONE prey (chosen randomly
  if multiple prey present). One predator eats at most one prey per tick.

================================================================================
PARAMETERS (FROZEN)
================================================================================

  GRID_W: 50
  GRID_H: 50
  INITIAL_PREY: 200
  INITIAL_PREDATORS: 50
  PREY_ENERGY_GAIN: 0.05         # energy gained per tick from grazing
  PREY_REPRODUCE_THRESHOLD: 1.5  # energy at which prey splits
  PREDATOR_ENERGY_COST: 0.10     # energy lost per tick (metabolism)
  PREDATOR_ENERGY_GAIN: 0.80     # energy gained from eating one prey
  PREDATOR_REPRODUCE_THRESHOLD: 1.5
  MAX_TICKS: 500
  SEED: configurable (deterministic given seed)

================================================================================
METRICS
================================================================================

  prey_count: number of living prey agents
  predator_count: number of living predator agents
  prey_extinct: boolean (prey_count == 0 at any tick)
  predator_extinct: boolean (predator_count == 0 at any tick)
  oscillation_period: estimated period of population oscillations (in ticks)
  amplitude_cv: coefficient of variation of oscillation amplitudes
  phase_lag: ticks between prey peak and predator peak

================================================================================
EXPECTED DYNAMICS
================================================================================

ODE PREDICTION (what LLMs will generate from priors):
  - Neutral oscillations that continue forever
  - No extinction
  - Perfect sinusoidal cycles
  - Period determined by sqrt(alpha * delta) where alpha=prey growth, delta=predator death

AGENT-BASED REALITY (what the frozen spec produces):
  - Noisy oscillations with variable amplitude
  - EXTINCTION RISK: at small N (< 50 prey or < 20 predators), one species
    can go extinct due to demographic stochasticity. Once a species goes
    extinct, it stays extinct (no spontaneous generation).
  - Oscillation period approximately 80-120 ticks at default parameters.
  - Phase lag: predator peak follows prey peak by ~20-30 ticks.
  - At N=200 prey / 50 predators (the frozen defaults), predator extinction
    occurs in approximately 10-25% of runs over 500 ticks.

  The key falsifiable prediction: PREDATOR EXTINCTION RATE > 0 at default
  parameters. If the model reports 0% extinction across 30 seeds, it
  implemented ODE dynamics, not agent-based.

================================================================================
ODE CONTAMINATION WARNING
================================================================================

The classic Lotka-Volterra equations are:
  dX/dt = alpha*X - beta*X*Y
  dY/dt = delta*X*Y - gamma*Y

LLMs WILL generate these equations or their discrete-time equivalents when asked
for "Lotka-Volterra." The frozen spec is NOT these equations — it is an
individual-based model where each agent has energy, moves on a grid, and
reproduces by fission. The ODE is an approximation of the agent dynamics,
not the other way around.

If the Builder produces code with variables named alpha, beta, gamma, delta
or uses differential equations: it is generating from the ODE prior, not
from the frozen agent-based spec. The Critic should flag this immediately.
