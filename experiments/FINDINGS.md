# CHP Multi-Discipline Study — Aggregate Findings

Last updated: 2026-03-22
Experiments complete: 201 (187 catalog, 13 loop, 0 discovery) across 17 domains

## Key Finding: Self-Correcting Verification

The CHP protocol catches errors at every layer of the system, including errors
in the frozen specifications themselves. This has been observed three times:

### Meta-Spec Error 1: sqrt2-newton (Mathematics)
Newton's method computed sqrt(2) to 10,000 digits. The frozen reference file
contained LLM-hallucinated digits after position 50. The computation served as
ground truth to correct the specification.

### Meta-Spec Error 2: Arrhenius A-factor (Chemistry)
Frozen spec gives A = 1.65e13 for H2+I2, but Arrhenius with Ea = 165,000 J/mol
gives k(700K) = 8.04, not the published 1.65e-3. The A-factor is ~4900x too
high — likely an LLM hallucination in the prompt that specified the constants.

### Meta-Spec Error 3: Blood pH constants (Chemistry)
Frozen pKa = 6.352 (thermodynamic) with alpha = 0.0307 gives pH = 7.64, not
the clinical 7.40. The prompt confused thermodynamic and clinical conventions
for the CO2/bicarbonate system.

**The pattern**: The protocol doesn't care *who* made the error — the prompt
author, the implementation LLM, or the frozen spec. When the math doesn't
check out, the protocol catches it.

## Error Taxonomy (201 experiments)

Every LLM prior error falls into one of these categories:

| Category | Count | Example |
|---|---|---|
| Unit errors | 15+ | Ea in kJ not J, mm/yr vs m/yr for plates, radians vs degrees |
| Sign errors | 25+ | van't Hoff, Nernst, Hess, KVL, inverting op-amp, Coriolis |
| Formula errors | 40+ | n² missing in VdW, bh³ not bh², 2GM/c² not GM/c², Darcy vs Fanning (4×) |
| Constant precision | 20+ | Kw=1e-14 vs 1.011e-14, g=10 vs 9.80665, P₅₀=26.6 not 27, H₀=70 not 50 |
| Conceptual errors | 30+ | CLT doesn't apply to Cauchy, S-waves can't traverse liquid, Mohs is ordinal not linear |
| Convention errors | 15+ | Libby vs Godwin, clinical vs thermo pKa, ecology ln vs info theory log₂ |
| Approximation errors | 20+ | 68-95-99.7 is approximate, normal approx invalid for small np, v=cz invalid for z>0.1 |
| **Meta-spec errors** | **3** | **Frozen spec itself wrong** |

## Per-Discipline Summary

### Chemistry (10 cat experiments, 61 tests)
Sprint: chemistry-sprint-2026.
21 prior errors caught. Strongest showing of unit/sign/convention errors.
Two meta-spec errors discovered (A-factor, blood pH).

### Physics (30 cat + 1 loop = 31 experiments, 88+ tests)
Sprint: physics-sprint-2026.
Covers mechanics, E&M, optics, relativity, kinetic theory, thermo, quantum,
nuclear, gravity, fluid dynamics. Prior errors: g rounding, gamma inversion,
Wien peak color, closed pipe harmonics, 3/2kT vs 1/2kT.

### Mathematics (5 cat experiments)
e, pi, sqrt(2) to 10K-1M digits. One meta-spec error: hallucinated reference
digits in sqrt(2) frozen file.

### Statistics (25 cat experiments, 189 tests)
Sprint: statistics-sprint-2026.
Full coverage: distributions (normal, t, chi-squared, F, binomial, Poisson,
exponential), inference (CI, hypothesis testing, power, effect size),
regression (OLS, multiple, logistic), non-parametric (Mann-Whitney,
Kruskal-Wallis, Fisher exact), Bayesian, bootstrap, Markov chains,
Bonferroni/BH correction. Key traps: 68-95-99.7 inexact, df=n-1 not n,
MLE variance divides by n not n-1, Bayes needs normalization.

### Biology (30 cat + 3 loop = 33 experiments, 330+ tests)
Sprint: biology-sprint-2026.
Covers genetics (Hardy-Weinberg, Mendelian, codon table), ecology (logistic,
Gompertz, competition, island biogeography), physiology (Michaelis-Menten,
Hill, HH, Nernst, Goldman), evolution (drift, selection, phylogenetics),
pharmacokinetics (1C, 2C). Key traps: heterozygote is 2pq not pq, Km is
half-max not max, Hill n ≠ binding sites, Goodwin needs n>8, t½=ln2/ke.

### Engineering (25 cat experiments, 351 tests)
Sprint: engineering-sprint-2026.
Covers circuits (RC, RL, RLC, op-amp), controls (PID, Bode, transfer
functions, Routh-Hurwitz), structures (beams, stress-strain, Mohr's circle,
trusses, fatigue), fluids (Reynolds, Darcy-Weisbach, pipe flow, Manning),
thermal (heat exchangers, expansion), signals (sampling, filtering).
Key traps: f_c=1/(2πRC) not 1/(RC), Darcy≠Fanning (4×), I=bh³/12 not bh²/12.

### Economics (20 cat experiments, 224 tests)
Sprint: economics-sprint-2026.
Covers micro (supply-demand, elasticity, surplus, externalities, tax incidence),
macro (IS-LM, Phillips curve, Solow, money multiplier), finance (PV, compound
interest, bonds, Black-Scholes, portfolio), trade (comparative advantage),
game theory (Nash). Key traps: APR≠EAR, money multiplier is 1/rr not 1/(1-rr).

### Earth Science (20 cat experiments, 258 tests)
Sprint: earth-science-sprint-2026.
Covers atmosphere (barometric, lapse rate, Coriolis, geostrophic wind),
geology (seismic waves, Mohs, plate velocity, glacial rebound), climate
(carbon cycle, radiative forcing, greenhouse, Milankovitch), hydrology
(runoff, Manning's equation). Key traps: S-waves can't traverse liquid,
CO₂ forcing is logarithmic, Mohs scale is ordinal not linear.

### Astronomy (20 cat experiments, 291 tests)
Sprint: astronomy-sprint-2026.
Covers orbits (Kepler, vis-viva, escape velocity, Hohmann transfer),
stellar (luminosity, main sequence, spectral types, Chandrasekhar),
cosmology (Hubble, redshift, CMB, Drake equation), gravitational
(Schwarzschild, Roche limit, tidal locking, lensing).
Key traps: Kepler constant depends on mass, v=cz fails for z>0.1,
Einstein deflection is 2× Newtonian.

### Social Science (2 loop + 2 staged)
Schelling segregation, Spatial Prisoner's Dilemma. Prior errors: sequential
vs simultaneous update, tolerance threshold, initial condition sensitivity.

### Computer Science (3 loop experiments)
Grover's search, PBFT consensus, ML hyperparameter search.

### Music (1 loop experiment)
Metal harmony analysis. Classical theory generates 7 "errors" per riff;
metal-aware analysis finds 0.

### Audio DSP (1 loop experiment)
Freeverb: 8 comb filters (not textbook 4), hand-tuned Jezar values.

### Medicine (2 cat experiments)
Anatomy viewers (HTML5 + VTK). Demonstrates protocol is modality-independent.

## How Experiments Map to CHP Layers

| Experiment Type | CHP Layers Validated |
|---|---|
| **cat-** (187) | Layer 1 (Prior-as-Detector), Layer 3 (Frozen Code Forcing) |
| **loop-** (13) | All 9 layers (Builder/Critic/Reviewer, sigma gates, dead ends, mode switching) |
| **disc-** (0) | Layer 1 in the wild (proves errors happen naturally, not just in constructed traps) |

The cat- experiments provide broad coverage of *what* LLMs get wrong across
17 domains. The loop- experiments demonstrate that the *full protocol* catches
and corrects these errors through multi-turn iteration.

## Next Steps

- **Discovery (disc-) experiments**: Capture real LLM errors before correction.
  Requires running LLM without frozen spec, capturing raw output, then comparing.
  These are the strongest evidence that prior errors occur naturally.
- **Additional loop- experiments**: The 13 existing loops cover 7 domains.
  Adding loops for statistics, engineering, economics, earth science, and
  astronomy would demonstrate protocol generality.
- See STUDY_PLAN.md for the full experiment list.
