# CHP Multi-Discipline Study — Master Plan

## Decisions Log

- **2026-03-22**: Decided on three evidence standards (catalog, discovery, loop)
- **2026-03-22**: Prefix naming: `cat-`, `disc-`, `loop-` before experiment name
- **2026-03-22**: Organize by discipline, not by standard
- **2026-03-22**: Don't rerun existing experiments — rename with prefix, keep results
- **2026-03-22**: Target ~500 experiments: ~300 catalog, ~150 discovery, ~50 loop
- **2026-03-22**: Sprint prompts per discipline (like chemistry_sprint.md) are the execution unit

## Evidence Standards

| Prefix | Standard | What It Proves | How It Works |
|--------|----------|----------------|--------------|
| `cat-` | Catalog | "LLMs get this wrong" | Pre-specified errors in frozen spec. Single-pass implementation + tests. Proves the error exists and is catchable. |
| `disc-` | Discovery | "We proved it happens in the wild" | Run LLM *without* frozen spec first. Capture raw output. Compare to authoritative values. Then implement with spec. Two outputs: the error and the fix. |
| `loop-` | Loop | "The protocol finds and fixes it autonomously" | Full Builder/Critic multi-turn cycle. Gate scores. Statistical validation (multi-seed where applicable). Errors discovered, not pre-specified. |

## What Makes Each Standard Valuable

**Catalog** is breadth. 300 experiments across 14 disciplines builds the error
taxonomy. Each one is a data point: "given this formula, LLMs make this specific
mistake." Fast to produce. The claim: systematic coverage.

**Discovery** is proof. You can't just say "LLMs confuse kJ and J." You have to
show it. Discovery experiments capture the raw LLM output (the wrong answer),
then the corrected output. The evidence is the before/after pair.

**Loop** is the mechanism. The protocol doesn't just detect — it corrects
autonomously across multiple turns. Gate scores track quality. Statistical
batteries prove the fix is real. This is the novel contribution.

**Meta-spec errors** can occur at any standard level. When the frozen spec itself
is wrong (written by an LLM), and the computation catches it, that's tracked as
a separate error category regardless of experiment type.

---

## Existing Experiments (28 complete, 3 staged/superseded)

### Chemistry — 10 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| chem-equilibrium | cat-chem-equilibrium | cat | Kp=Kc (ignores Δn) |
| chem-kinetics | cat-chem-kinetics | cat | Ea in kJ not J |
| chem-buffers | cat-chem-buffers | cat | H-H inverted, blood pKa wrong |
| chem-radioactive-decay | cat-chem-radioactive-decay | cat | Libby 5568 not Godwin 5730 |
| chem-vdw-gas | cat-chem-vdw-gas | cat | Missing n² in VdW |
| chem-electrochemistry | cat-chem-electrochemistry | cat | Nernst sign, ΔG sign |
| chem-spectrophotometry | cat-chem-spectrophotometry | cat | ln not log10 |
| chem-thermochemistry | cat-chem-thermochemistry | cat | C₂H₄/NO sign, Hess reversed |
| chem-stoichiometry | cat-chem-stoichiometry | cat | Integer atomic weights |
| chem-crystal-packing | cat-chem-crystal-packing | cat | FCC=8 atoms (should be 4) |

### Mathematics — 5 complete + 1 superseded
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| euler-e | cat-euler-e | cat | Uses math.e (15 digits) not Taylor series |
| pi-machin | cat-pi-machin | cat | Leibniz/Monte Carlo instead of Machin |
| sqrt2-newton | cat-sqrt2-newton | cat | **META-SPEC**: frozen digits hallucinated |
| time_sprint | cat-time-sprint | cat | Naive algorithms at scale |
| omega_sentinel_1M | cat-omega-sentinel-1M | cat | Decimal bottleneck at 1M digits |
| pi-calculator | *(superseded by pi-machin)* | — | — |

### Biology — 3 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| sir-epidemic | loop-sir-epidemic | loop | Deterministic model contamination |
| lotka-volterra | loop-lotka-volterra | loop | ODE contamination (no extinction) |
| izhikevich-neurons | loop-izhikevich-neurons | loop | Hodgkin-Huxley contamination |

### Physics — 1 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| lorenz-attractor | loop-lorenz-attractor | loop | Euler integration, wrong IC |

### Social Science — 2 complete + 2 staged
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| schelling-segregation | loop-schelling-segregation | loop | Sequential update, wrong tolerance |
| spatial-prisoners-dilemma | loop-spatial-prisoners-dilemma | loop | Single-defector IC, deterministic |
| simsiv-v1-replication | *(staged)* | loop | — |
| simsiv-v2-replication | *(staged)* | loop | — |

### Computer Science — 3 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| quantum-grover | loop-quantum-grover | loop | Boolean oracle not phase-flip |
| blockchain-consensus | loop-blockchain-consensus | loop | Raft contamination in PBFT |
| ml-hyperparam-search | loop-ml-hyperparam-search | loop | Data leakage |

### Music — 1 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| metal-harmony | loop-metal-harmony | loop | Classical theory as wrong prior |

### Audio DSP — 1 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| schroeder-reverb | loop-schroeder-reverb | loop | 4 comb filters (should be 8) |

### Medicine — 2 complete
| Current Name | New Name | Type | Key Prior Error |
|---|---|---|---|
| anatomy-viewer | cat-anatomy-viewer | cat | Anatomical position errors |
| anatomy-viewer-vtk | cat-anatomy-viewer-vtk | cat | Same spec, different renderer |

---

## Planned New Experiments (472 to reach 500)

### Chemistry — 40 new (→ 50 total)

**Catalog (30):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-chem-solubility-product | Ksp, common ion effect, precipitation | Ksp units wrong, ignores activity coefficients |
| 2 | cat-chem-colligative | Boiling point elevation, freezing depression | Uses wrong Kb/Kf, ignores van't Hoff factor i |
| 3 | cat-chem-oxidation-states | Assign oxidation numbers, balance redox | Peroxide O = -1 not -2, Cr₂O₇²⁻ wrong |
| 4 | cat-chem-gas-laws | Combined/Dalton's/Graham's law | Graham's uses sqrt(M) not M, wrong STP values |
| 5 | cat-chem-henry-law | Gas solubility vs pressure | Confuses Henry's law forms (Kh vs 1/Kh) |
| 6 | cat-chem-raoult-law | Vapor pressure of mixtures | Assumes ideal for non-ideal mixtures |
| 7 | cat-chem-clausius-clapeyron | Vapor pressure vs temperature | Wrong sign or wrong R value |
| 8 | cat-chem-born-haber | Lattice energy cycles | Wrong sign convention for electron affinity |
| 9 | cat-chem-molecular-orbital | Bond order calculations | Fills orbitals in wrong order for O₂ |
| 10 | cat-chem-vsepr | Molecular geometry prediction | Confuses electron pair vs molecular geometry |
| 11 | cat-chem-phase-diagrams | Phase boundaries, triple point | Wrong Clausius-Clapeyron slope for water |
| 12 | cat-chem-ionic-strength | Activity coefficients, Debye-Hückel | Uses concentration not activity |
| 13 | cat-chem-combustion-analysis | Empirical formula from combustion data | Forgets to subtract O from CO₂ and H₂O |
| 14 | cat-chem-dilution | Serial dilution, concentration | C1V1=C2V2 applied to non-dilution problems |
| 15 | cat-chem-osmotic-pressure | π = iMRT calculations | Forgets van't Hoff factor for electrolytes |
| 16 | cat-chem-coordination | Crystal field splitting, spectrochemical series | Wrong d-electron count, high/low spin confusion |
| 17 | cat-chem-organic-naming | IUPAC nomenclature, functional groups | Wrong parent chain, wrong numbering |
| 18 | cat-chem-chirality | R/S assignment, optical activity | Cahn-Ingold-Prelog priority errors |
| 19 | cat-chem-reaction-rates | Rate law determination from data | Confuses order with stoichiometric coefficient |
| 20 | cat-chem-le-chatelier | Equilibrium shift predictions | Volume change: wrong direction for gases |
| 21 | cat-chem-galvanic-electrolytic | Cell type identification, reactions | Confuses anode/cathode for electrolytic cells |
| 22 | cat-chem-polyprotic | Diprotic/triprotic acid calculations | Uses Ka1 for all steps, ignores Ka2 |
| 23 | cat-chem-indicators | pH indicator selection, color changes | Wrong pH range for phenolphthalein |
| 24 | cat-chem-calorimetry | q=mcΔT, bomb calorimetry | Specific heat of water = 4.184 not 4.2 |
| 25 | cat-chem-faraday-electrolysis | Mass deposited in electrolysis | Wrong n (electrons transferred) |
| 26 | cat-chem-nuclear-reactions | Binding energy, mass defect | Uses atomic mass not nuclear mass |
| 27 | cat-chem-ideal-solution | Raoult's law deviations | Doesn't distinguish positive/negative deviations |
| 28 | cat-chem-rate-temperature | Q₁₀ rule, Arrhenius at multiple temps | "Rate doubles per 10°C" is only approximate |
| 29 | cat-chem-electron-config | Ground state configurations, exceptions | Cr is [Ar]3d⁵4s¹ not 3d⁴4s², Cu is 3d¹⁰4s¹ |
| 30 | cat-chem-lattice-energy | Born-Landé, Madelung constants | Wrong Madelung constant for structure type |

**Discovery (8):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 31 | disc-chem-acid-base-titration | Strong/weak acid-base titration | Wrong equivalence point pH for weak acid |
| 32 | disc-chem-electrochemical-series | Predicting reactions from E⁰ | Reversed spontaneity prediction |
| 33 | disc-chem-thermodynamic-spontaneity | ΔG = ΔH - TΔS at various T | Temperature-dependent spontaneity missed |
| 34 | disc-chem-kinetic-molecular | Maxwell-Boltzmann distribution | Wrong most probable vs mean vs RMS speed |
| 35 | disc-chem-hybridization | sp/sp2/sp3 assignment | Wrong hybridization for common molecules |
| 36 | disc-chem-entropy-calculations | ΔS for reactions, phase changes | Sign error, forgets ΔS_surr |
| 37 | disc-chem-transition-metals | d-orbital splitting, magnetism | Paramagnetic/diamagnetic prediction wrong |
| 38 | disc-chem-polymer-chemistry | Degree of polymerization, MW distributions | Mn vs Mw confusion |

**Loop (2):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 39 | loop-chem-multi-equilibrium | Coupled equilibria (dissolving + acid-base) | Treats equilibria independently |
| 40 | loop-chem-electrochemical-cell-design | Full galvanic cell simulation | Multiple sign/direction errors compound |

### Physics — 49 new (→ 50 total)

**Catalog (30):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-phys-projectile | Range, max height with drag | Uses g=10 not 9.80665, ignores drag |
| 2 | cat-phys-pendulum | Period (simple + large angle) | Small-angle approximation for large angles |
| 3 | cat-phys-shm | Spring-mass oscillator | Confuses ω and f (factor of 2π) |
| 4 | cat-phys-coulomb | Electric force and field | Uses k vs ε₀ inconsistently, unit errors |
| 5 | cat-phys-circuits | Series/parallel R, Kirchhoff's laws | Inverts parallel resistance formula |
| 6 | cat-phys-blackbody | Wien's law, Stefan-Boltzmann | Wrong Wien constant, confuses peak λ vs ν |
| 7 | cat-phys-doppler | Frequency shift (sound + light) | Wrong sign convention approach vs recede |
| 8 | cat-phys-snell | Refraction, total internal reflection | sin/cos confusion, wrong critical angle |
| 9 | cat-phys-relativity | Lorentz factor, time dilation | γ vs 1/γ confusion |
| 10 | cat-phys-kinetic-theory | Molecular speeds, energy | 3/2 kT vs 1/2 kT, mean vs RMS |
| 11 | cat-phys-thermodynamic-processes | Isothermal, adiabatic work | Wrong sign on work, Cv vs Cp confusion |
| 12 | cat-phys-carnot | Efficiency, COP for heat pumps | Uses T in °C not K |
| 13 | cat-phys-entropy | Entropy change calculations | Forgets irreversibility contribution |
| 14 | cat-phys-waves | Standing waves, harmonics | Open vs closed pipe: even harmonics |
| 15 | cat-phys-photoelectric | Threshold frequency, stopping potential | Uses wavelength where frequency needed |
| 16 | cat-phys-compton | Wavelength shift | Wrong formula (missing 1-cosθ) |
| 17 | cat-phys-de-broglie | Wavelength of particles | Uses classical KE for relativistic particles |
| 18 | cat-phys-bohr-model | Hydrogen energy levels | Wrong sign or wrong n² dependence |
| 19 | cat-phys-nuclear-binding | Binding energy per nucleon | Confuses mass defect direction |
| 20 | cat-phys-gravity | Orbits, escape velocity, Kepler | Uses r not r² in gravitational force |
| 21 | cat-phys-moment-inertia | I for various shapes | Wrong formula for hollow sphere vs solid |
| 22 | cat-phys-angular-momentum | Conservation, precession | L=Iω vs L=mvr confusion |
| 23 | cat-phys-bernoulli | Fluid flow, lift | Forgets height term, wrong ½ρv² |
| 24 | cat-phys-viscosity | Stokes drag, Reynolds number | Uses diameter not radius in Stokes |
| 25 | cat-phys-heat-transfer | Conduction, radiation, convection | Wrong Stefan-Boltzmann (T⁴ not T) |
| 26 | cat-phys-diffraction | Single/double slit patterns | Confuses minima and maxima conditions |
| 27 | cat-phys-interference | Thin film, Newton's rings | Forgets phase change at reflection |
| 28 | cat-phys-magnetic-force | Lorentz force, cyclotron radius | Wrong cross product direction |
| 29 | cat-phys-faraday-induction | EMF, Lenz's law | Wrong sign (forgets Lenz's law) |
| 30 | cat-phys-capacitors | Series/parallel, energy stored | Series/parallel formulas swapped vs resistors |

**Discovery (14):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 31 | disc-phys-rc-transient | RC circuit charge/discharge curves | Wrong time constant τ, exponential direction |
| 32 | disc-phys-rlc-resonance | Resonance frequency, Q factor | Wrong formula for bandwidth |
| 33 | disc-phys-op-amp | Inverting/non-inverting gain | Sign error on inverting amp |
| 34 | disc-phys-planck-radiation | Spectral radiance curve | Rayleigh-Jeans used where Planck needed |
| 35 | disc-phys-hydrogen-spectrum | Balmer, Lyman, Paschen series | Wrong n₁/n₂ assignment |
| 36 | disc-phys-particle-in-box | Quantum energy levels | Missing factor of 2 in denominator |
| 37 | disc-phys-tunneling | Barrier penetration probability | Wrong decay constant formula |
| 38 | disc-phys-stefan-boltzmann-stars | Stellar luminosity from T and R | Forgets 4πR² factor |
| 39 | disc-phys-rocket-equation | Tsiolkovsky rocket equation | Uses wrong log base or wrong mass ratio |
| 40 | disc-phys-satellite-orbits | Orbital period, velocity | Confuses orbital radius with altitude |
| 41 | disc-phys-gyroscope | Precession rate | Wrong direction or missing I factor |
| 42 | disc-phys-lens-equation | Thin lens, magnification | Sign convention errors (real/virtual) |
| 43 | disc-phys-polarization | Malus's law, Brewster's angle | Confuses cos²θ with cos θ |
| 44 | disc-phys-debye-model | Specific heat at low T | Classical Dulong-Petit at low T (wrong) |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 45 | loop-phys-three-body | Restricted three-body problem | Oversimplified to two-body |
| 46 | loop-phys-double-pendulum | Chaotic motion | Linearized equations for chaotic regime |
| 47 | loop-phys-ising-model | 2D Ising, phase transition | Wrong critical temperature |
| 48 | loop-phys-fluid-turbulence | Navier-Stokes simplified | Laminar assumptions in turbulent regime |
| 49 | loop-phys-quantum-harmonic | Quantum vs classical oscillator | Classical energy spacing (wrong) |

### Mathematics — 45 new (→ 50 total)

**Catalog (30):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-math-golden-ratio | φ to high precision | Uses 1.618 (3dp) not computed value |
| 2 | cat-math-fibonacci | Large Fibonacci numbers, Binet | Float overflow, Binet rounding at large n |
| 3 | cat-math-prime-sieve | Sieve of Eratosthenes, prime counting | Off-by-one in sieve boundary |
| 4 | cat-math-zeta-values | ζ(2)=π²/6, ζ(4)=π⁴/90 | Wrong coefficient or wrong π power |
| 5 | cat-math-euler-mascheroni | γ constant to high precision | Uses 0.5772 (4dp), slow convergence |
| 6 | cat-math-catalan | Catalan constant G | Low precision, wrong series |
| 7 | cat-math-stirling | Stirling's approximation accuracy | Forgets √(2πn) term |
| 8 | cat-math-binomial | Binomial coefficients, Pascal's triangle | Integer overflow for large n |
| 9 | cat-math-taylor-convergence | Radius of convergence for common series | Wrong radius for ln(1+x), arctan(x) |
| 10 | cat-math-fourier | Fourier coefficients of standard functions | Wrong normalization factor |
| 11 | cat-math-matrix-eigenvalues | Eigenvalue computation | Characteristic polynomial errors |
| 12 | cat-math-determinant | Determinant algorithms | Cofactor expansion errors for n>3 |
| 13 | cat-math-numerical-integration | Simpson's rule, Gauss quadrature | Wrong weights for Gauss-Legendre |
| 14 | cat-math-root-finding | Newton's, bisection, secant | Newton divergence cases missed |
| 15 | cat-math-ode-comparison | Euler vs RK4 accuracy | Euler error order (1st not 2nd) |
| 16 | cat-math-interpolation | Lagrange, Newton interpolation | Runge phenomenon ignored |
| 17 | cat-math-fft | FFT implementation | Wrong twiddle factor, bit-reversal |
| 18 | cat-math-svd | Singular value decomposition | Wrong matrix dimensions in result |
| 19 | cat-math-graph-shortest-path | Dijkstra's algorithm | Negative weight handling (need Bellman-Ford) |
| 20 | cat-math-combinatorics | Derangements, partitions | Wrong derangement formula |
| 21 | cat-math-modular-arithmetic | Modular exponentiation, CRT | CRT coprimality assumption missed |
| 22 | cat-math-continued-fractions | CF representation of irrationals | Convergent computation errors |
| 23 | cat-math-gamma-function | Γ(n) for non-integer values | Γ(n) = (n-1)! only for integers |
| 24 | cat-math-bernoulli-numbers | Bernoulli number computation | Wrong sign convention (B₁ = +1/2 vs -1/2) |
| 25 | cat-math-riemann-hypothesis | Zero distribution on critical strip | Claiming proof or disproof |
| 26 | cat-math-elliptic-integrals | Complete elliptic integrals K, E | Wrong argument convention (k vs m=k²) |
| 27 | cat-math-bessel-functions | J₀, J₁ computation | Wrong series coefficients |
| 28 | cat-math-pi-digits-distribution | Digit frequency analysis | Assuming uniform without verification |
| 29 | cat-math-primality-testing | Miller-Rabin, deterministic bases | Wrong witness set for deterministic test |
| 30 | cat-math-numerical-differentiation | Finite differences, Richardson | Wrong step size, numerical instability |

**Discovery (10):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 31 | disc-math-floating-point | IEEE 754 edge cases | Associativity assumed, catastrophic cancellation |
| 32 | disc-math-chaos-logistic | Logistic map bifurcation | Wrong critical r values |
| 33 | disc-math-random-walk | 1D/2D random walk statistics | Wrong return probability for 3D (Pólya) |
| 34 | disc-math-birthday-problem | Collision probability | Approximation vs exact disagreement |
| 35 | disc-math-monty-hall | Simulation vs analytical | Uniform prior assumption wrong |
| 36 | disc-math-pi-leibniz-vs-machin | Convergence rate comparison | Overstates Leibniz convergence |
| 37 | disc-math-matrix-condition | Condition number and stability | Ignores conditioning in matrix inversion |
| 38 | disc-math-p-vs-np | Reduction examples | Wrong reduction direction |
| 39 | disc-math-halting-problem | Undecidability demonstration | Claims decidable for "simple" cases |
| 40 | disc-math-godel-numbering | Gödel encoding | Wrong prime factorization scheme |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 41 | loop-math-mandelbrot | Mandelbrot set boundary | Iteration count insufficient, wrong escape |
| 42 | loop-math-cellular-automata | Rule 110 universal computation | Wrong rule table |
| 43 | loop-math-game-of-life | Conway's GoL pattern classification | Misidentified still lifes/oscillators |
| 44 | loop-math-fractal-dimension | Box-counting dimension | Wrong scaling exponent |
| 45 | loop-math-langtons-ant | Emergent highway behavior | Wrong step count to highway |

### Biology — 47 new (→ 50 total)

**Catalog (30):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-bio-hardy-weinberg | Allele/genotype frequencies | Forgets 2pq for heterozygotes |
| 2 | cat-bio-mendelian-ratios | Punnett square, dihybrid crosses | Wrong ratio for dihybrid (9:3:3:1) |
| 3 | cat-bio-codon-table | Translation, reading frames | Wrong start codon frequency |
| 4 | cat-bio-michaelis-menten | Enzyme kinetics, Km, Vmax | Confuses Km with substrate concentration |
| 5 | cat-bio-hill-equation | Cooperativity coefficient | Hill coefficient interpretation wrong |
| 6 | cat-bio-logistic-growth | Carrying capacity, growth rate | Confuses r and K effects |
| 7 | cat-bio-gompertz | Tumor growth modeling | Wrong asymptotic behavior |
| 8 | cat-bio-competition | Lotka-Volterra competition | Wrong coexistence criteria (α < K/K') |
| 9 | cat-bio-seir | SEIR epidemic model | Wrong R₀ formula for SEIR vs SIR |
| 10 | cat-bio-pharmacokinetics-1c | One-compartment PK model | Half-life vs elimination rate confusion |
| 11 | cat-bio-pharmacokinetics-2c | Two-compartment PK model | Distribution vs elimination phase |
| 12 | cat-bio-hodgkin-huxley | Simplified HH equations | Wrong gating variable kinetics |
| 13 | cat-bio-fitzhugh-nagumo | Excitable dynamics | Wrong nullcline shape |
| 14 | cat-bio-circadian | Goodwin oscillator | Wrong Hill coefficient for oscillation |
| 15 | cat-bio-genetic-drift | Wright-Fisher model | Fixation probability wrong for small N |
| 16 | cat-bio-natural-selection | Fitness landscapes | Confuses additive and multiplicative fitness |
| 17 | cat-bio-shannon-diversity | Diversity indices | Uses ln vs log₂ inconsistently |
| 18 | cat-bio-simpson-diversity | Simpson's index | D vs 1-D vs 1/D confusion |
| 19 | cat-bio-population-age | Leslie matrix, stable age distribution | Wrong eigenvalue interpretation |
| 20 | cat-bio-dna-melting | Tm calculation (nearest-neighbor) | Uses old %GC method instead of NN |
| 21 | cat-bio-pcr-amplification | PCR yield vs cycle number | Assumes 100% efficiency |
| 22 | cat-bio-protein-pI | Isoelectric point calculation | Wrong pKa values for amino acids |
| 23 | cat-bio-enzyme-inhibition | Competitive vs uncompetitive Ki | Wrong Lineweaver-Burk intercept changes |
| 24 | cat-bio-oxygen-dissociation | Hemoglobin O₂ saturation curve | Ignores Bohr effect, wrong P₅₀ |
| 25 | cat-bio-membrane-potential | Nernst equation for ions | Wrong sign or wrong z value |
| 26 | cat-bio-goldman-equation | Resting potential, Goldman-Hodgkin-Katz | Wrong permeability ratio handling |
| 27 | cat-bio-allometric-scaling | Kleiber's law, metabolic scaling | Uses 2/3 not 3/4 exponent |
| 28 | cat-bio-island-biogeography | Species-area relationship | Wrong z exponent |
| 29 | cat-bio-predator-functional-response | Holling Type I/II/III | Wrong curve shape for Type III |
| 30 | cat-bio-phylogenetic-distance | Jukes-Cantor correction | Uses raw distance instead of corrected |

**Discovery (12):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 31 | disc-bio-sis-epidemic | SIS endemic equilibrium | Wrong endemic equilibrium formula |
| 32 | disc-bio-metapopulation | Levins model, patch occupancy | Ignores rescue effect |
| 33 | disc-bio-neutral-theory | Hubbell's neutral model | Assumes niche differentiation |
| 34 | disc-bio-kin-selection | Hamilton's rule (rB > C) | Wrong relatedness coefficient |
| 35 | disc-bio-sex-ratio | Fisher's principle | Frequency-dependent selection missed |
| 36 | disc-bio-ecological-niche | Hutchinson's n-dimensional niche | Fundamental vs realized niche |
| 37 | disc-bio-replication-fork | DNA replication speed | Wrong Okazaki fragment direction |
| 38 | disc-bio-central-dogma | Information flow exceptions | Forgets reverse transcriptase |
| 39 | disc-bio-krebs-cycle | ATP yield per glucose | Uses 38 ATP (old) not 30-32 (modern) |
| 40 | disc-bio-photosynthesis | Light reaction energetics | Wrong photosystem order (II before I) |
| 41 | disc-bio-action-potential | AP phases and ion channels | Na⁺/K⁺ channel timing wrong |
| 42 | disc-bio-synaptic-transmission | EPSP/IPSP calculations | Wrong reversal potential |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 43 | loop-bio-evolution-simulation | Selection + drift + mutation | Mutation rate orders of magnitude wrong |
| 44 | loop-bio-ecosystem | Multi-species food web dynamics | Unrealistic parameter combinations |
| 45 | loop-bio-neural-network | Biological neural network simulation | ANN contamination in bio model |
| 46 | loop-bio-epidemiological-forecast | SIR with interventions | Herd immunity threshold wrong |
| 47 | loop-bio-protein-folding | HP lattice model | Energy function wrong |

### Engineering — 40 new

**Catalog (25):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-eng-ohm-kirchhoff | Kirchhoff's circuit analysis | Wrong sign convention for KVL |
| 2 | cat-eng-rc-circuit | RC time constant, frequency response | Wrong cutoff frequency formula |
| 3 | cat-eng-rl-circuit | RL transient, time constant | Wrong τ = L/R (not R/L) |
| 4 | cat-eng-rlc-resonance | Resonance frequency, bandwidth | Wrong Q factor formula |
| 5 | cat-eng-op-amp-ideal | Inverting/non-inverting/diff amp | Virtual ground not applied correctly |
| 6 | cat-eng-digital-logic | Boolean simplification, Karnaugh maps | Wrong don't-care handling |
| 7 | cat-eng-sampling-theorem | Nyquist rate, aliasing | Nyquist is 2× not 1× signal frequency |
| 8 | cat-eng-pid-controller | PID tuning, step response | Wrong integral/derivative term signs |
| 9 | cat-eng-bode-plot | Gain/phase margins | Wrong phase contribution from poles/zeros |
| 10 | cat-eng-transfer-function | Pole-zero analysis | Confuses poles and zeros |
| 11 | cat-eng-beam-bending | Euler-Bernoulli beam equations | Wrong moment of inertia for cross-section |
| 12 | cat-eng-stress-strain | Young's modulus, yield strength | Confuses engineering and true stress |
| 13 | cat-eng-mohr-circle | Principal stresses, max shear | Wrong center or radius calculation |
| 14 | cat-eng-reynolds-number | Flow regime classification | Wrong characteristic length |
| 15 | cat-eng-darcy-weisbach | Pipe friction losses | Wrong friction factor (Darcy vs Fanning, 4×) |
| 16 | cat-eng-heat-exchanger | LMTD method | Wrong ΔT for counter-flow |
| 17 | cat-eng-gear-ratios | Gear train analysis | Wrong direction of rotation |
| 18 | cat-eng-truss-analysis | Method of joints/sections | Wrong force direction at pin joints |
| 19 | cat-eng-fatigue | S-N curve, Miner's rule | Wrong endurance limit |
| 20 | cat-eng-thermal-expansion | Linear/volumetric expansion | Uses linear α for volumetric (need 3α) |
| 21 | cat-eng-pipe-flow | Hagen-Poiseuille, Bernoulli | Confuses laminar/turbulent flow regimes |
| 22 | cat-eng-power-transmission | Belt drives, chain drives | Wrong tension ratio formula |
| 23 | cat-eng-spring-design | Wahl correction factor | Ignores curvature correction for helical springs |
| 24 | cat-eng-signal-filtering | Low-pass, high-pass filter design | Wrong component values for cutoff frequency |
| 25 | cat-eng-feedback-stability | Routh-Hurwitz, Nyquist criterion | Wrong number of RHP poles |

**Discovery (10):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 26 | disc-eng-bridge-design | Load distribution, safety factor | Wrong load combination (missing partial factors) |
| 27 | disc-eng-motor-selection | Torque-speed curves | Confused starting vs running torque |
| 28 | disc-eng-compressor-work | Isentropic vs polytropic | Wrong polytropic exponent |
| 29 | disc-eng-antenna-gain | Directivity, aperture efficiency | Wrong 4π factor |
| 30 | disc-eng-welding-heat | Heat input, HAZ size | Wrong preheat temperature |
| 31 | disc-eng-concrete-mix | Water/cement ratio, strength | Wrong Abrams' law application |
| 32 | disc-eng-buckling | Euler buckling load | Wrong effective length factor K |
| 33 | disc-eng-vibration-isolation | Transmissibility, natural frequency | Wrong damping ratio effect |
| 34 | disc-eng-corrosion-rate | Tafel extrapolation | Wrong exchange current density |
| 35 | disc-eng-semiconductor | pn junction, diode equation | Wrong thermal voltage at non-standard T |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 36 | loop-eng-control-system | Multi-loop control design | Inner/outer loop interaction |
| 37 | loop-eng-power-grid | Load flow analysis | Slack bus handling wrong |
| 38 | loop-eng-robot-kinematics | Forward/inverse kinematics | DH parameter convention errors |
| 39 | loop-eng-fluid-simulation | CFD simplified (lid-driven cavity) | Boundary condition errors |
| 40 | loop-eng-structural-optimization | Topology optimization | Checkerboard pattern (no filter) |

### Statistics — 40 new

**Catalog (25):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-stat-normal-dist | z-scores, percentiles, CDF | 68-95-99.7 rule precision (99.7 is approximate) |
| 2 | cat-stat-t-dist | t-values, confidence intervals | Wrong df (n-1 not n) |
| 3 | cat-stat-chi-squared | Goodness of fit, independence | Wrong df for contingency tables |
| 4 | cat-stat-f-dist | ANOVA, variance ratio | Wrong df numerator/denominator |
| 5 | cat-stat-binomial | Probability calculations | Normal approximation where invalid (small n) |
| 6 | cat-stat-poisson | Event rate modeling | Uses Poisson where negative binomial needed |
| 7 | cat-stat-exponential | Memoryless property, hazard rate | Mean = 1/λ not λ |
| 8 | cat-stat-bayes-theorem | Posterior calculation | Prior × likelihood without normalizing |
| 9 | cat-stat-mle | Maximum likelihood estimation | Wrong log-likelihood for common distributions |
| 10 | cat-stat-ols-regression | Least squares, R², residuals | R² interpretation for multiple regression |
| 11 | cat-stat-multiple-regression | Multicollinearity, VIF | Ignores VIF, interprets partial coefficients as total |
| 12 | cat-stat-logistic-regression | Odds ratio, log-odds | Odds ratio vs probability confusion |
| 13 | cat-stat-confidence-interval | CI construction and interpretation | "95% chance parameter is in CI" (wrong) |
| 14 | cat-stat-hypothesis-testing | Type I/II error, power | Confuses α and β |
| 15 | cat-stat-power-analysis | Sample size determination | Wrong effect size standardization |
| 16 | cat-stat-effect-size | Cohen's d, η², r | Wrong pooled SD formula |
| 17 | cat-stat-correlation | Pearson, Spearman, Kendall | Correlation implies causation |
| 18 | cat-stat-clt | Central limit theorem demo | CLT applies to any distribution (wrong for Cauchy) |
| 19 | cat-stat-bootstrap | Confidence intervals via resampling | Wrong resampling scheme (without replacement) |
| 20 | cat-stat-markov-chain | Transition matrices, steady state | Wrong steady-state equation |
| 21 | cat-stat-survival-analysis | Kaplan-Meier estimator | Wrong censoring handling |
| 22 | cat-stat-mann-whitney | Non-parametric test | Wrong U statistic formula |
| 23 | cat-stat-kruskal-wallis | Non-parametric ANOVA | Wrong tie correction |
| 24 | cat-stat-fisher-exact | Exact test for 2×2 tables | Wrong hypergeometric calculation |
| 25 | cat-stat-bonferroni | Multiple comparisons correction | Too conservative, ignores FDR alternative |

**Discovery (10):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 26 | disc-stat-p-value | p-value calculation and interpretation | p-value = P(H₀ true | data) — WRONG |
| 27 | disc-stat-bayesian-updating | Sequential Bayesian inference | Wrong conjugate prior |
| 28 | disc-stat-ab-testing | Sample size, significance, power | Peeking problem, early stopping |
| 29 | disc-stat-regression-diagnostics | Leverage, Cook's distance | Wrong influence threshold |
| 30 | disc-stat-time-series | ARIMA modeling, stationarity | Differencing order wrong |
| 31 | disc-stat-pca | Principal component analysis | Wrong variance explained calculation |
| 32 | disc-stat-clustering | k-means, silhouette score | Wrong distance metric |
| 33 | disc-stat-propensity-score | Matching, causal inference | Ignores positivity assumption |
| 34 | disc-stat-meta-analysis | Fixed vs random effects | Wrong heterogeneity test (I²) |
| 35 | disc-stat-sample-bias | Selection bias, survivorship bias | Doesn't recognize survivorship bias in data |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 36 | loop-stat-mcmc | Metropolis-Hastings sampling | Wrong acceptance ratio |
| 37 | loop-stat-em-algorithm | Expectation-maximization for GMM | Local optima, wrong initialization |
| 38 | loop-stat-causal-inference | DAG-based causal analysis | Confuses mediators and confounders |
| 39 | loop-stat-anomaly-detection | Statistical process control | Wrong control limit calculation |
| 40 | loop-stat-experimental-design | Factorial design, blocking | Confounding with block effects |

### Economics — 30 new

**Catalog (20):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-econ-supply-demand | Equilibrium price/quantity | Wrong direction for shift effects |
| 2 | cat-econ-elasticity | Price, income, cross elasticity | Elasticity sign confusion |
| 3 | cat-econ-consumer-surplus | CS/PS from supply-demand curves | Wrong integration bounds |
| 4 | cat-econ-cobb-douglas | Returns to scale, factor shares | Exponents must sum to 1 (only for CRS) |
| 5 | cat-econ-present-value | NPV, IRR, annuities | Wrong compounding (continuous vs discrete) |
| 6 | cat-econ-compound-interest | Effective annual rate | APR vs EAR confusion |
| 7 | cat-econ-bond-pricing | YTM, duration, convexity | Wrong coupon timing convention |
| 8 | cat-econ-black-scholes | Option pricing | Wrong volatility (historical vs implied) |
| 9 | cat-econ-portfolio | Markowitz optimization | Wrong covariance matrix handling |
| 10 | cat-econ-nash-equilibrium | 2×2 game solutions | Mixed strategy calculation errors |
| 11 | cat-econ-is-lm | IS-LM equilibrium | Wrong slope signs |
| 12 | cat-econ-phillips-curve | Inflation-unemployment tradeoff | Assumes stable long-run tradeoff |
| 13 | cat-econ-solow-model | Steady-state capital per worker | Wrong depreciation handling |
| 14 | cat-econ-comparative-advantage | Ricardo model, terms of trade | Confuses absolute and comparative advantage |
| 15 | cat-econ-gini | Gini coefficient from data | Wrong Lorenz curve calculation |
| 16 | cat-econ-gdp-deflator | Real vs nominal GDP | Wrong base year handling |
| 17 | cat-econ-exchange-rate | PPP, interest rate parity | Wrong direction for appreciation/depreciation |
| 18 | cat-econ-tax-incidence | Deadweight loss, who bears tax | Assumes seller always bears tax |
| 19 | cat-econ-externality | Pigouvian tax, social optimum | Wrong marginal social cost |
| 20 | cat-econ-money-multiplier | Fractional reserve banking | Wrong reserve ratio application |

**Discovery (7):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 21 | disc-econ-auction-theory | Vickrey, English, Dutch auctions | Revenue equivalence conditions wrong |
| 22 | disc-econ-moral-hazard | Principal-agent problem | Wrong incentive compatibility constraint |
| 23 | disc-econ-adverse-selection | Akerlof lemons model | Wrong pooling/separating equilibrium |
| 24 | disc-econ-oligopoly | Cournot vs Bertrand | Wrong equilibrium for differentiated products |
| 25 | disc-econ-behavioral-finance | Prospect theory, loss aversion | Wrong value function shape parameters |
| 26 | disc-econ-real-options | Option value of waiting | Wrong discount rate for real options |
| 27 | disc-econ-cryptocurrency | Mining difficulty, halving schedule | Wrong block reward calculation |

**Loop (3):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 28 | loop-econ-market-simulation | Multi-agent market dynamics | No convergence to equilibrium |
| 29 | loop-econ-macro-model | DSGE simplified model | Wrong Euler equation |
| 30 | loop-econ-financial-crisis | Systemic risk contagion | Wrong network topology effects |

### Earth Science — 30 new

**Catalog (20):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-earth-atmospheric-pressure | Barometric formula | Wrong scale height |
| 2 | cat-earth-lapse-rate | Temperature vs altitude | Dry vs moist lapse rate confusion |
| 3 | cat-earth-coriolis | Coriolis parameter vs latitude | Wrong at equator (zero not maximum) |
| 4 | cat-earth-geostrophic-wind | Wind from pressure gradient | Wrong direction (NH vs SH) |
| 5 | cat-earth-richter-scale | Magnitude from seismogram | Richter vs moment magnitude confusion |
| 6 | cat-earth-plate-velocity | Plate motion calculations | Wrong reference frame |
| 7 | cat-earth-ocean-density | Salinity, temperature, pressure effects | Wrong equation of state |
| 8 | cat-earth-tidal-forces | Tidal bulge calculation | Only considers moon, forgets sun |
| 9 | cat-earth-seismic-waves | P-wave, S-wave velocities | S-waves through liquid (wrong) |
| 10 | cat-earth-mohs-hardness | Mineral identification | Wrong relative hardness values |
| 11 | cat-earth-soil-classification | USDA soil texture triangle | Wrong clay/silt/sand boundaries |
| 12 | cat-earth-runoff | Rational method, curve number | Wrong runoff coefficient |
| 13 | cat-earth-glacial-rebound | Isostatic adjustment rate | Wrong viscosity estimate |
| 14 | cat-earth-carbon-cycle | Reservoir sizes, fluxes | Ocean vs atmosphere flux direction |
| 15 | cat-earth-radiative-forcing | CO₂ forcing formula | Wrong logarithmic relationship |
| 16 | cat-earth-greenhouse-simple | Single-layer atmosphere model | Wrong emissivity assumption |
| 17 | cat-earth-milankovitch | Orbital parameters, periodicity | Wrong precession period (26K not 23K) |
| 18 | cat-earth-continental-drift | Plate velocity from hotspot tracks | Wrong age-distance calculation |
| 19 | cat-earth-volcanic-explosivity | VEI scale, tephra volume | Wrong volume thresholds |
| 20 | cat-earth-stream-discharge | Manning's equation | Wrong hydraulic radius |

**Discovery (7):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 21 | disc-earth-climate-sensitivity | ECS from energy balance | Wrong feedback factor |
| 22 | disc-earth-ocean-circulation | Thermohaline circulation | Wrong density-driven flow direction |
| 23 | disc-earth-weathering | Chemical weathering rates | Wrong Arrhenius dependence |
| 24 | disc-earth-magnetic-reversal | Polarity timescale | Wrong frequency of reversals |
| 25 | disc-earth-tsunami-speed | Shallow water wave speed | Uses deep water formula |
| 26 | disc-earth-groundwater | Darcy's law, aquifer properties | Wrong hydraulic conductivity units |
| 27 | disc-earth-erosion | USLE soil loss equation | Wrong rainfall erosivity |

**Loop (3):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 28 | loop-earth-climate-model | Energy balance model with feedbacks | Wrong ice-albedo feedback sign |
| 29 | loop-earth-earthquake-sequence | Gutenberg-Richter + Omori's law | Wrong b-value or p-value |
| 30 | loop-earth-ocean-acidification | pH change from CO₂ absorption | Wrong carbonate system equilibrium |

### Astronomy — 30 new

**Catalog (20):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-astro-kepler-laws | Orbital period, semi-major axis | Wrong T²/a³ constant for non-solar |
| 2 | cat-astro-vis-viva | Orbital velocity at any point | Wrong sign or missing μ/r term |
| 3 | cat-astro-escape-velocity | Escape speed from surface | Uses wrong radius (equatorial vs mean) |
| 4 | cat-astro-schwarzschild | Black hole radius | Wrong factor (2GM/c² not GM/c²) |
| 5 | cat-astro-stellar-luminosity | L = 4πR²σT⁴ | Wrong units for R (forgets solar conversion) |
| 6 | cat-astro-main-sequence | Lifetime from mass-luminosity | Wrong M-L exponent (3.5 vs 4) |
| 7 | cat-astro-hubble-law | Distance from redshift | Wrong H₀ value (uses outdated) |
| 8 | cat-astro-redshift | Cosmological vs Doppler | Uses v=cz for large z (wrong) |
| 9 | cat-astro-parallax | Distance from parallax angle | Wrong parsec definition |
| 10 | cat-astro-magnitude | Apparent vs absolute magnitude | Wrong distance modulus formula |
| 11 | cat-astro-stefan-boltzmann-stars | Spectral type from temperature | Wrong spectral class boundaries |
| 12 | cat-astro-chandrasekhar | White dwarf mass limit | Uses 1.4 when 1.44 M☉ more precise |
| 13 | cat-astro-roche-limit | Tidal disruption distance | Wrong density ratio handling |
| 14 | cat-astro-tidal-locking | Locking timescale | Wrong Q (tidal dissipation factor) |
| 15 | cat-astro-drake-equation | Factor estimates | Orders of magnitude disagreement |
| 16 | cat-astro-cmb-temperature | 2.725 K, Wien peak wavelength | Uses 3K (rounded), wrong peak |
| 17 | cat-astro-synodic-period | Synodic from sidereal periods | Wrong formula for inferior planets |
| 18 | cat-astro-equilibrium-temp | Planetary temperature from albedo | Forgets greenhouse correction |
| 19 | cat-astro-orbital-mechanics | Hohmann transfer orbit | Wrong Δv calculation |
| 20 | cat-astro-gravitational-lensing | Einstein ring radius | Wrong angular diameter distance |

**Discovery (7):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 21 | disc-astro-hr-diagram | Stellar classification plotting | Wrong luminosity class boundaries |
| 22 | disc-astro-nucleosynthesis | Stellar fusion energy yield | Wrong binding energy curve peak |
| 23 | disc-astro-exoplanet-transit | Transit depth, period | Wrong limb darkening correction |
| 24 | disc-astro-dark-matter | Rotation curve, virial theorem | Wrong NFW profile parameters |
| 25 | disc-astro-cosmic-expansion | Friedmann equations simplified | Wrong matter/radiation/dark energy era |
| 26 | disc-astro-neutron-star | Density, rotation, magnetic field | Wrong moment of inertia |
| 27 | disc-astro-binary-stars | Mass from orbital parameters | Wrong mass function |

**Loop (3):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 28 | loop-astro-n-body | N-body gravitational simulation | Energy not conserved (wrong integrator) |
| 29 | loop-astro-galaxy-rotation | Simulated rotation curve | Newtonian without DM |
| 30 | loop-astro-stellar-evolution | HR diagram evolution track | Wrong transition timescales |

### Computer Science — 37 new (→ 40 total)

**Catalog (22):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-cs-sorting-complexity | Comparison of sort algorithms | Wrong best/worst case for quicksort |
| 2 | cat-cs-hash-collision | Birthday paradox in hashing | Wrong collision probability formula |
| 3 | cat-cs-bst-operations | BST insert, delete, search | Wrong delete for node with two children |
| 4 | cat-cs-bfs-dfs | Graph traversal, shortest path | BFS not shortest for weighted graphs |
| 5 | cat-cs-dijkstra | Shortest path algorithm | Fails with negative weights (need Bellman-Ford) |
| 6 | cat-cs-a-star | Heuristic pathfinding | Inadmissible heuristic not flagged |
| 7 | cat-cs-dynamic-programming | Knapsack, LCS, edit distance | Wrong recurrence relation |
| 8 | cat-cs-information-entropy | Shannon entropy calculation | Wrong log base (bits vs nats) |
| 9 | cat-cs-huffman | Huffman coding tree | Non-optimal tree from wrong algorithm |
| 10 | cat-cs-hamming | Error detection/correction | Wrong syndrome calculation |
| 11 | cat-cs-rsa | Key generation, encryption | Wrong totient (Euler's vs Carmichael's) |
| 12 | cat-cs-diffie-hellman | Key exchange | Wrong generator selection |
| 13 | cat-cs-backpropagation | Neural network gradient computation | Vanishing gradient not addressed |
| 14 | cat-cs-gradient-descent | Convergence, learning rate | Wrong learning rate bounds |
| 15 | cat-cs-pagerank | Link analysis, eigenvector | Wrong damping factor effect |
| 16 | cat-cs-mapreduce | Word count, distributed patterns | Wrong combiner vs reducer |
| 17 | cat-cs-database-normalization | 1NF through BCNF | Confuses 3NF and BCNF |
| 18 | cat-cs-queuing-theory | M/M/1 queue, Little's law | Wrong utilization formula |
| 19 | cat-cs-turing-machine | State machine simulation | Wrong transition function |
| 20 | cat-cs-regex | Regular expression matching | Backreference not regular (requires PDA) |
| 21 | cat-cs-cache-performance | Hit rate, miss penalty | Wrong AMAT formula |
| 22 | cat-cs-big-o | Complexity analysis | Wrong amortized analysis |

**Discovery (10):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 23 | disc-cs-floating-point | IEEE 754 arithmetic edge cases | NaN propagation rules wrong |
| 24 | disc-cs-concurrency | Race conditions, deadlock detection | Wrong Coffman conditions |
| 25 | disc-cs-consensus | Paxos/Raft correctness | Wrong quorum size |
| 26 | disc-cs-bloom-filter | False positive rate | Wrong formula for optimal k |
| 27 | disc-cs-lru-cache | Cache eviction simulation | Wrong eviction order |
| 28 | disc-cs-tcp-congestion | AIMD, slow start | Wrong window size calculation |
| 29 | disc-cs-garbage-collection | Mark-sweep, reference counting | Cycle detection missed |
| 30 | disc-cs-type-inference | Hindley-Milner algorithm | Wrong unification |
| 31 | disc-cs-lambda-calculus | Beta reduction, Church encoding | Wrong evaluation order |
| 32 | disc-cs-automata-theory | DFA/NFA equivalence | Wrong subset construction |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 33 | loop-cs-distributed-clock | Lamport/vector clocks | Wrong causality detection |
| 34 | loop-cs-genetic-algorithm | Optimization via GA | Premature convergence (wrong selection) |
| 35 | loop-cs-compiler-optimization | Constant folding, dead code | Wrong liveness analysis |
| 36 | loop-cs-network-routing | Distance vector, link state | Count-to-infinity problem |
| 37 | loop-cs-database-transactions | ACID, isolation levels | Phantom reads at wrong isolation level |

### Social Science — 28 new (→ 30 total)

**Catalog (15):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-soc-voter-model | Opinion dynamics, consensus time | Wrong consensus time scaling |
| 2 | cat-soc-bounded-confidence | Deffuant/HK opinion model | Wrong convergence threshold |
| 3 | cat-soc-axelrod-culture | Cultural dissemination | Wrong interaction probability |
| 4 | cat-soc-ultimatum-game | Fair offer predictions | Assumes rational homo economicus |
| 5 | cat-soc-public-goods | Contribution dynamics | Free rider equilibrium wrong |
| 6 | cat-soc-tragedy-commons | Resource depletion | Wrong Nash equilibrium |
| 7 | cat-soc-small-world | Watts-Strogatz network | Wrong clustering coefficient formula |
| 8 | cat-soc-scale-free | Barabási-Albert model | Wrong degree distribution exponent |
| 9 | cat-soc-epidemic-network | SIS/SIR on networks | Wrong epidemic threshold on networks |
| 10 | cat-soc-social-influence | DeGroot learning model | Wrong convergence conditions |
| 11 | cat-soc-cooperation-evolution | Reciprocity, punishment | Wrong Nowak rule for cooperation |
| 12 | cat-soc-demographic-transition | Birth/death rate modeling | Wrong stage transitions |
| 13 | cat-soc-voting-systems | Arrow's impossibility | Wrong Condorcet conditions |
| 14 | cat-soc-gerrymandering | Efficiency gap, compactness | Wrong metric calculation |
| 15 | cat-soc-income-inequality | Pareto distribution, power law | Wrong tail exponent |

**Discovery (8):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 16 | disc-soc-segregation-dynamics | Extended Schelling with mobility | Wrong equilibrium prediction |
| 17 | disc-soc-information-cascade | Herding behavior | Wrong Bayesian updating |
| 18 | disc-soc-network-formation | Strategic network formation | Wrong pairwise stability |
| 19 | disc-soc-trust-game | Trust and reciprocity | Wrong subgame perfect equilibrium |
| 20 | disc-soc-matching-markets | Gale-Shapley algorithm | Wrong stability definition |
| 21 | disc-soc-social-learning | Observational learning | Wrong information aggregation |
| 22 | disc-soc-polarization | Opinion polarization dynamics | Wrong homophily effect |
| 23 | disc-soc-collective-action | Olson's logic | Wrong group size effect |

**Loop (5):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 24 | loop-soc-civil-violence | Epstein rebellion model | Wrong threshold function |
| 25 | loop-soc-urban-growth | Cellular automata city model | Wrong growth rules |
| 26 | loop-soc-language-evolution | Naming game dynamics | Wrong convergence mechanism |
| 27 | loop-soc-market-emergence | Sugarscape trading | Wrong trade protocol |
| 28 | loop-soc-norm-emergence | Axelrod norm game | Wrong metanorm calculation |

### Medicine — 18 new (→ 20 total)

**Catalog (12):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-med-drug-half-life | Elimination kinetics, steady state | t½ = 0.693/ke, uses wrong ke |
| 2 | cat-med-dosing-regimen | Loading dose, maintenance dose | Wrong Vd or wrong bioavailability |
| 3 | cat-med-creatinine-clearance | Cockcroft-Gault, MDRD eGFR | Wrong weight (lean vs total) |
| 4 | cat-med-bmi | BMI calculation, classification | Wrong category boundaries |
| 5 | cat-med-corrected-qt | Bazett, Fridericia correction | Bazett overcorrects at high HR |
| 6 | cat-med-anion-gap | AG = Na - (Cl + HCO3) | Forgets albumin correction |
| 7 | cat-med-alveolar-gas | PAO₂ = FiO₂(PB-PH₂O) - PaCO₂/R | Wrong R value (0.8 not 1.0) |
| 8 | cat-med-osmolality | 2Na + Glucose/18 + BUN/2.8 | Wrong conversion factors |
| 9 | cat-med-dose-response | EC₅₀, Hill coefficient | Wrong sigmoid curve parameters |
| 10 | cat-med-cardiac-output | Fick principle: CO = VO₂/(CaO₂-CvO₂) | Wrong O₂ content calculation |
| 11 | cat-med-ventilation-perfusion | V/Q ratio, shunt fraction | Wrong dead space calculation |
| 12 | cat-med-sensitivity-specificity | PPV, NPV, ROC | PPV depends on prevalence (often ignored) |

**Discovery (4):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 13 | disc-med-pharmacogenomics | CYP450 metabolism rates | Wrong enzyme classification |
| 14 | disc-med-acid-base-physiology | ABG interpretation, Winter's formula | Wrong compensation formula |
| 15 | disc-med-fluid-balance | IV fluid distribution (0.9% NaCl vs D5W) | Wrong distribution volumes |
| 16 | disc-med-oxygen-hemoglobin | O₂-Hb dissociation curve shifts | Wrong Bohr effect direction |

**Loop (2):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 17 | loop-med-drug-interaction | Multi-drug PK/PD simulation | Wrong CYP inhibition model |
| 18 | loop-med-disease-progression | Markov model for chronic disease | Wrong transition probabilities |

### Audio DSP — 9 new (→ 10 total)

**Catalog (6):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-dsp-fir-filter | FIR filter design, impulse response | Wrong coefficient calculation |
| 2 | cat-dsp-iir-filter | IIR butterworth, Chebyshev | Wrong bilinear transform |
| 3 | cat-dsp-fft-spectrum | FFT, spectral analysis | Wrong frequency resolution (fs/N) |
| 4 | cat-dsp-windowing | Hann, Hamming, Blackman windows | Wrong window function coefficients |
| 5 | cat-dsp-sample-rate | Resampling, interpolation | Wrong anti-aliasing filter |
| 6 | cat-dsp-compression | Dynamic range compression | Wrong attack/release time constants |

**Discovery (2):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 7 | disc-dsp-chorus-flanger | Delay modulation effects | Wrong LFO rate/depth |
| 8 | disc-dsp-parametric-eq | Peaking/shelving EQ design | Wrong Q factor to bandwidth conversion |

**Loop (1):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 9 | loop-dsp-synthesizer | Subtractive synthesis chain | Wrong filter resonance behavior |

### Music — 9 new (→ 10 total)

**Catalog (6):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 1 | cat-mus-interval-ratios | Just intonation vs 12-TET | Wrong cent values |
| 2 | cat-mus-circle-of-fifths | Key signatures, enharmonics | Wrong number of sharps/flats |
| 3 | cat-mus-scale-construction | Major, minor, modal scales | Wrong interval pattern for modes |
| 4 | cat-mus-chord-voicing | Voice leading rules | Parallel fifths detection wrong |
| 5 | cat-mus-rhythm-quantization | Beat division, time signatures | Wrong subdivision for compound time |
| 6 | cat-mus-tuning-systems | Pythagorean, meantone, well-tempered | Pythagorean comma value wrong |

**Discovery (2):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 7 | disc-mus-harmonic-series | Overtone frequencies, timbre | Wrong partial numbering |
| 8 | disc-mus-key-detection | Key estimation from note frequencies | Wrong profile correlation method |

**Loop (1):**
| # | Name | What It Computes | Expected LLM Error |
|---|------|-----------------|-------------------|
| 9 | loop-mus-counterpoint | Species counterpoint generation | Wrong consonance/dissonance rules |

---

## Totals

| Discipline | Cat | Disc | Loop | Total |
|---|---|---|---|---|
| Chemistry | 40 | 8 | 2 | 50 |
| Physics | 30 | 14 | 5+1 | 50 |
| Mathematics | 30 | 10 | 5+5 | 50 |
| Biology | 30 | 12 | 5+3 | 50 |
| Engineering | 25 | 10 | 5 | 40 |
| Statistics | 25 | 10 | 5 | 40 |
| Computer Science | 22 | 10 | 5+3 | 40 |
| Social Science | 15 | 8 | 5+2 | 30 |
| Economics | 20 | 7 | 3 | 30 |
| Earth Science | 20 | 7 | 3 | 30 |
| Astronomy | 20 | 7 | 3 | 30 |
| Medicine | 12 | 4 | 2+2 | 20 |
| Audio DSP | 6 | 2 | 1+1 | 10 |
| Music | 6 | 2 | 1+1 | 10 |
| **Total** | **301** | **111** | **50+18** | **~500** |

("+N" means N already exist from prior work)

## Execution Plan

Each discipline gets a sprint prompt (like `prompts/chemistry_sprint.md`) that specifies:
1. Frozen constants with authoritative sources
2. Named prior errors (PRIOR_ERRORS dict)
3. Function signatures
4. Test specifications

Sprint prompts are the execution unit. Each covers 10 experiments.
Estimated: ~47 sprint prompts to reach 500 experiments.

## Sprint Prompt Priority Order

1. Physics (highest value — fundamental science, rich errors)
2. Statistics (high value — methodology errors affect all fields)
3. Biology (high value — many quantitative errors)
4. Engineering (high value — practical impact)
5. Earth Science (timely — climate/geology)
6. Astronomy (compelling — space science)
7. Economics (useful — quantitative finance)
8. Computer Science (remaining 37)
9. Social Science (remaining 28)
10. Chemistry (remaining 40)
11. Medicine (remaining 18)
12. Audio DSP (remaining 9)
13. Music (remaining 9)
