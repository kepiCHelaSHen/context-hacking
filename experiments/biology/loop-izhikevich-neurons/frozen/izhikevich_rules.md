# Izhikevich Spiking Neuron Model — Frozen Specification
# Source: Izhikevich (2003) "Simple Model of Spiking Neurons"
#         IEEE Transactions on Neural Networks 14(6):1569-1572
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

The Izhikevich model is a 2-variable spiking neuron model that reproduces 20+
biologically observed firing patterns using only 4 parameters (a, b, c, d).
It is computationally simpler than Hodgkin-Huxley (4 variables, ionic
conductances) while capturing a much wider range of dynamics.

The key scientific point: LLMs commonly generate HODGKIN-HUXLEY equations
when asked for "spiking neuron model" because HH is the most famous model
in computational neuroscience. The Izhikevich model is a DIFFERENT model
with DIFFERENT equations, DIFFERENT variables, and DIFFERENT parameter names.
The Prior-as-Detector catches HH contamination by checking variable count
(2 vs 4) and parameter names (a,b,c,d vs gNa,gK,gL).

================================================================================
EQUATIONS
================================================================================

  v' = 0.04*v^2 + 5*v + 140 - u + I
  u' = a*(b*v - u)

  with after-spike resetting:
    if v >= 30 mV:
      v = c
      u = u + d

VARIABLES:
  v: membrane potential (mV). Represents the neuron's voltage.
  u: recovery variable (dimensionless). Represents membrane recovery
     (activation of K+ currents and inactivation of Na+ currents combined).

  NOTE: ONLY TWO VARIABLES. Hodgkin-Huxley has FOUR (V, m, h, n).
  If the implementation has more than 2 state variables per neuron,
  it's Hodgkin-Huxley contamination.

PARAMETERS:
  a: time scale of recovery variable u. Smaller = slower recovery.
  b: sensitivity of u to subthreshold fluctuations of v.
  c: after-spike reset value of v (mV).
  d: after-spike increment of u.
  I: injected current (external input, mA).

  NOTE: These are the IZHIKEVICH parameter names. Hodgkin-Huxley uses
  gNa, gK, gL, ENa, EK, EL, Cm. If ANY of these HH names appear in
  the code, it's contamination.

================================================================================
FIRING PATTERNS (frozen parameter sets)
================================================================================

Each firing pattern is defined by a specific (a, b, c, d) tuple:

  REGULAR SPIKING (RS):
    a = 0.02, b = 0.2, c = -65, d = 8
    I = 10 (constant current injection)
    Expected: regular, evenly-spaced spikes with slight adaptation.
    Inter-spike-interval (ISI): roughly constant after transient.

  INTRINSICALLY BURSTING (IB):
    a = 0.02, b = 0.2, c = -55, d = 4
    I = 10
    Expected: initial burst of 2-4 rapid spikes, then regular spiking.
    ISI pattern: short-short-long-short-short-long...

  CHATTERING (CH):
    a = 0.02, b = 0.2, c = -50, d = 2
    I = 10
    Expected: rhythmic bursts of 2-4 spikes with pauses between bursts.

  FAST SPIKING (FS):
    a = 0.10, b = 0.2, c = -65, d = 2
    I = 10
    Expected: high-frequency spiking with minimal adaptation.
    ISI: nearly constant, shorter than RS.

  LOW-THRESHOLD SPIKING (LTS):
    a = 0.02, b = 0.25, c = -65, d = 2
    I = 10
    Expected: rebound spike after inhibition, regular spiking under current.

================================================================================
INTEGRATION
================================================================================

METHOD: Forward Euler with dt = 0.5 ms (half-millisecond steps).

  NOTE: Unlike the Lorenz experiment (where Euler is wrong), Euler IS the
  correct method for the Izhikevich model. Izhikevich (2003) explicitly
  uses Euler integration in the paper. The model was DESIGNED for Euler.

  However: the time step must be dt = 0.5, NOT dt = 1.0.
  At dt = 1.0, the v^2 term can cause numerical overflow for v > 30.
  Izhikevich (2003) recommends dt = 0.5 with TWO half-steps for v:

    v = v + 0.5*(0.04*v^2 + 5*v + 140 - u + I)
    v = v + 0.5*(0.04*v^2 + 5*v + 140 - u + I)
    u = u + a*(b*v - u)

  This two-half-step method is in the paper. LLMs that generate a single
  full step (dt=1.0) will produce overflow and incorrect spike timing.

DURATION: 1000 ms (1 second of simulated time).
STEPS: 2000 (at dt = 0.5 ms).

================================================================================
METRICS
================================================================================

  spike_count: number of spikes (v crossing 30 mV from below)
  spike_times: list of times (ms) at which spikes occur
  mean_isi: mean inter-spike interval (ms)
  isi_cv: coefficient of variation of ISI (std/mean)
    RS: CV < 0.15 (regular)
    IB: CV > 0.30 (bursting produces variable ISI)
    FS: CV < 0.10 (very regular, fast)
  v_min: minimum membrane potential (should be >= c for each pattern)
  v_max: maximum membrane potential (should be ~30 mV at spike peak)
  v_bounded: boolean — v stays in [-90, 40] mV

  NOTE: v_max = 30 mV is the SPIKE THRESHOLD, not a biophysical maximum.
  The model resets v to c when v >= 30. If v exceeds 40 mV, integration
  is diverging (wrong dt or missing reset).

================================================================================
HODGKIN-HUXLEY CONTAMINATION WARNING
================================================================================

The Hodgkin-Huxley model equations are:
  C_m * dV/dt = I - gNa*m^3*h*(V-ENa) - gK*n^4*(V-EK) - gL*(V-EL)
  dm/dt = alpha_m(V)*(1-m) - beta_m(V)*m
  dh/dt = alpha_h(V)*(1-h) - beta_h(V)*h
  dn/dt = alpha_n(V)*(1-n) - beta_n(V)*n

Signs of HH contamination:
  - Variables named m, h, n (HH gating variables)
  - Parameters named gNa, gK, gL, ENa, EK, EL, Cm
  - 4 differential equations per neuron (HH has 4, Izhikevich has 2)
  - alpha/beta rate functions for gating
  - Conductance-based current: g * (V - E)

The Izhikevich model has NONE of these. It uses v, u, a, b, c, d.
If the code mentions "conductance," "gating," "sodium," or "potassium,"
it is generating Hodgkin-Huxley from the LLM's neuroscience prior.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  DT: 0.5        # ms, half-millisecond (NOT 1.0)
  DURATION: 1000  # ms
  STEPS: 2000
  SPIKE_THRESHOLD: 30  # mV
  V_EQUATION_COEFFICIENTS: [0.04, 5, 140]  # v' = 0.04*v^2 + 5*v + 140 - u + I
  HALF_STEP: true  # two half-steps for v per Izhikevich (2003)

  RS:  a=0.02, b=0.2,  c=-65, d=8, I=10
  IB:  a=0.02, b=0.2,  c=-55, d=4, I=10
  CH:  a=0.02, b=0.2,  c=-50, d=2, I=10
  FS:  a=0.10, b=0.2,  c=-65, d=2, I=10
  LTS: a=0.02, b=0.25, c=-65, d=2, I=10
