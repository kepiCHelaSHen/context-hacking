# Methods and Validation

## 1. Model Definition

### 1.1 Grid and Agents

Consider a square toroidal lattice $\mathcal{L}$ of dimension $L \times L$ with $L = 50$, yielding $|\mathcal{L}| = 2500$ cells. Each cell $c \in \mathcal{L}$ is in one of three states: empty ($\varnothing$), occupied by a type-A agent, or occupied by a type-B agent. At initialization, cells are occupied independently with probability $\rho = 0.90$ (density), and each occupied cell is assigned type A with probability $q = 0.50$ and type B otherwise. Initial placement is determined by a seeded pseudorandom number generator (numpy.random.Generator), ensuring reproducibility.

Let $\mathcal{A}(t) \subset \mathcal{L}$ denote the set of occupied cells at time $t$, and let $\mathcal{E}(t) = \mathcal{L} \setminus \mathcal{A}(t)$ denote the set of empty cells.

### 1.2 Neighborhood

For each cell $c \in \mathcal{L}$, define the Moore neighborhood:

$$\mathcal{N}(c) = \{c' \in \mathcal{L} : \|c - c'\|_{\infty} = 1\}$$

with toroidal boundary conditions, so $|\mathcal{N}(c)| = 8$ for all $c$. The occupied neighborhood of agent $i$ at cell $c_i$ is:

$$\mathcal{N}_i^{\text{occ}}(t) = \{c \in \mathcal{N}(c_i) : c \in \mathcal{A}(t)\}$$

### 1.3 Local Composition

For each agent $i$ at time $t$, define the same-type neighbor count:

$$S_i(t) = |\{c \in \mathcal{N}_i^{\text{occ}}(t) : \text{type}(c) = \text{type}(i)\}|$$

and the occupied neighbor count:

$$N_i(t) = |\mathcal{N}_i^{\text{occ}}(t)|$$

The local same-type proportion is:

$$p_i(t) = \begin{cases} S_i(t) \, / \, N_i(t) & \text{if } N_i(t) > 0 \\ 1 & \text{if } N_i(t) = 0 \end{cases}$$

Agents with no occupied neighbors are treated as satisfied (the convention follows Schelling 1971, where isolation is not penalized).

### 1.4 Baseline Satisfaction Rule

In the baseline (fixed-tolerance) model, agent $i$ is satisfied at time $t$ if and only if:

$$\text{satisfied}_i^{\text{base}}(t) = \mathbf{1}[p_i(t) \geq \tau_0]$$

where $\tau_0 = 0.375$ is the frozen tolerance threshold. This value is taken from Schelling (1971); it is deliberately not the more commonly cited $1/3 \approx 0.333$ that appears in many textbook implementations.

### 1.5 State Transition Rule

At each discrete time step $t$, all agents are evaluated simultaneously (synchronous update). Let $\mathcal{U}(t)$ denote the set of unsatisfied agents:

$$\mathcal{U}(t) = \{i \in \mathcal{A}(t) : \text{satisfied}_i(t) = 0\}$$

Each unsatisfied agent $i \in \mathcal{U}(t)$ is assigned a new location drawn uniformly at random from the set of empty cells:

$$c_i(t+1) \sim \text{Uniform}(\mathcal{E}(t))$$

Assignment is performed without replacement: once an empty cell is assigned to one agent, it is removed from the available set for subsequent agents within the same time step. The order in which unsatisfied agents are assigned to empty cells is randomized.

Satisfied agents do not move:

$$c_i(t+1) = c_i(t) \quad \text{if } \text{satisfied}_i(t) = 1$$

All moves are computed from the state at time $t$ and applied simultaneously to produce the state at time $t+1$. This synchronous update rule differs from the sequential (one-at-a-time) update used in some implementations (e.g., NetLogo, Mesa); the choice of update order affects convergence dynamics and final segregation levels.

---

## 2. CHP Dynamic Tolerance Extension

### 2.1 Per-Agent Tolerance State

In the CHP variant, each agent $i$ maintains an individual tolerance parameter $\tau_i(t)$ that evolves over time. All agents are initialized with $\tau_i(0) = \tau_0 = 0.375$.

### 2.2 Satisfaction Condition

The satisfaction condition under CHP retains the threshold form but uses the agent's current (time-varying) tolerance:

$$\text{satisfied}_i^{\text{CHP}}(t) = \mathbf{1}[p_i(t) \geq \tau_i(t)]$$

This is identical in form to the baseline rule, but $\tau_i(t)$ varies per agent and per time step, whereas the baseline uses the constant $\tau_0$.

### 2.3 Tolerance Update Rule

After all movement has been resolved at time $t$ (i.e., after the state transition), each agent's tolerance is updated based on the deviation between its current local composition and its current tolerance:

$$\tau_i(t+1) = \begin{cases} \min(\tau_i(t) + \alpha, \, \tau_{\max}) & \text{if } p_i(t) > \tau_i(t) + m \\ \max(\tau_i(t) - \alpha, \, \tau_{\min}) & \text{if } p_i(t) < \tau_i(t) - m \\ \tau_i(t) & \text{otherwise} \end{cases}$$

where:

- $\alpha = 0.005$ is the tolerance update rate (step size per tick)
- $m = 0.05$ is the comfort margin (dead zone half-width)
- $\tau_{\min} = 0.1$ and $\tau_{\max} = 0.9$ are tolerance bounds

The comfort margin $m$ creates a dead zone $[\tau_i(t) - m, \, \tau_i(t) + m]$ within which no tolerance update occurs. Tolerance increases only when the agent's local environment is substantially more homogeneous than its current expectation (by more than $m$), and decreases only when the environment is substantially more diverse.

**Timing convention.** The tolerance update is applied *after* the movement step within each time step. This ordering is material: applying the update before movement produces different dynamics because tolerance changes do not influence the current step's satisfaction evaluation. The post-movement ordering ensures that tolerance adapts to the agent's new neighborhood after relocation.

### 2.4 Interpretation

The mechanism models a form of adaptive expectation: agents in highly homogeneous environments gradually increase their tolerance for diversity (they "get used to" homogeneity and become more open), while agents in highly diverse environments gradually decrease their tolerance (they seek more same-type neighbors). The comfort margin prevents tolerance from tracking local composition exactly, introducing hysteresis and allowing for stable mixed configurations that would be unstable under the baseline model.

---

## 3. Segregation Metric

The global segregation index at time $t$ is defined as the mean local same-type proportion over all occupied cells:

$$\text{Seg}(t) = \frac{1}{|\mathcal{A}(t)|} \sum_{i \in \mathcal{A}(t)} p_i(t)$$

Empty cells are excluded from both the numerator and denominator. Agents with $N_i(t) = 0$ (no occupied neighbors) contribute $p_i(t) = 1$ to the sum, consistent with the convention in Section 1.3.

$\text{Seg}(t) = 0.5$ corresponds to a random (well-mixed) configuration under equal type proportions. $\text{Seg}(t) = 1.0$ corresponds to complete segregation (every agent surrounded exclusively by same-type neighbors). The baseline random expectation under $\rho = 0.90$ and $q = 0.50$ is $\text{Seg}(0) \approx 0.50$.

---

## 4. Simulation Protocol

### 4.1 Parameters

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Grid dimension | $L$ | 50 |
| Density | $\rho$ | 0.90 |
| Type ratio | $q$ | 0.50 |
| Base tolerance | $\tau_0$ | 0.375 |
| Comfort margin | $m$ | 0.05 |
| Tolerance update rate | $\alpha$ | 0.005 |
| Tolerance bounds | $[\tau_{\min}, \tau_{\max}]$ | [0.1, 0.9] |
| Maximum steps | $T$ | 500 |

### 4.2 Initialization

For each seed $k \in \{1, \ldots, K\}$, a pseudorandom number generator is initialized with seed $k$. Agent placement and type assignment are determined entirely by this generator, ensuring that the initial configuration is identical across conditions (baseline vs. CHP) for each seed.

### 4.3 Update Schedule

Each simulation runs for $T = 500$ time steps. Under the baseline model, the simulation terminates early if no agent moves in a given step (convergence). Under the CHP model, all 500 steps are executed because tolerance evolution can reintroduce dissatisfaction after apparent convergence.

### 4.4 Replication

All results are computed over $K = 30$ independent seeds. This sample size is sufficient to detect medium effect sizes ($d > 0.5$) at $\beta = 0.80$ with a paired design.

---

## 5. Statistical Analysis

### 5.1 Point Estimates

For each condition $c \in \{\text{base}, \text{CHP}\}$, the mean and standard deviation of the final segregation index across seeds are:

$$\bar{S}_c = \frac{1}{K} \sum_{k=1}^{K} \text{Seg}_k^c(T)$$

$$s_c = \sqrt{\frac{1}{K-1} \sum_{k=1}^{K} \left(\text{Seg}_k^c(T) - \bar{S}_c\right)^2}$$

### 5.2 Paired Comparison

Because the same initial configurations are used across conditions (paired by seed), the appropriate test is the paired-samples $t$-test. Define the per-seed difference:

$$d_k = \text{Seg}_k^{\text{CHP}}(T) - \text{Seg}_k^{\text{base}}(T)$$

The test statistic is:

$$t = \frac{\bar{d}}{s_d / \sqrt{K}}$$

where $\bar{d}$ and $s_d$ are the mean and standard deviation of $\{d_k\}_{k=1}^{K}$, with $K - 1$ degrees of freedom.

### 5.3 Effect Size

Cohen's $d$ for paired samples:

$$d_{\text{Cohen}} = \frac{\bar{d}}{s_d}$$

### 5.4 Results

| Statistic | Value |
|-----------|-------|
| $\bar{S}_{\text{base}}$ | 0.766 |
| $s_{\text{base}}$ | 0.009 |
| $\bar{S}_{\text{CHP}}$ | 0.666 |
| $s_{\text{CHP}}$ | 0.056 |
| $\bar{d}$ | $-0.101$ |
| $t(29)$ | $-9.858$ |
| $p$ | $< 10^{-6}$ |
| $d_{\text{Cohen}}$ | $-1.83$ |

The CHP variant produces significantly lower segregation than the baseline ($p < 10^{-6}$, $|d| = 1.83$, large effect by conventional thresholds). The effect is observed in 27 of 30 seeds (90%).

---

## 6. Non-Equivalence to Fixed Tolerance

### 6.1 The Reduction Objection

A natural objection is that the CHP mechanism is functionally equivalent to lowering the fixed tolerance to some effective value $\tau' < \tau_0$. If so, the contribution is trivial: the dynamic mechanism merely obscures a simpler parameter change.

### 6.2 Structural Argument

The CHP model is structurally non-equivalent to any fixed-tolerance model for the following reasons:

**State-dependent threshold.** Under CHP, the satisfaction boundary of agent $i$ at time $t$ depends on the agent's tolerance history $\{\tau_i(s)\}_{s \leq t}$, which in turn depends on the agent's trajectory through the grid. Two agents of the same type at the same location but with different histories may have different tolerance values and therefore different satisfaction states. No fixed-tolerance model exhibits this path dependence.

**Bidirectional adaptation.** Under CHP, tolerance can both increase (in homogeneous environments) and decrease (in diverse environments). This produces agents that oscillate between satisfied and unsatisfied states as the local composition fluctuates around the moving threshold. Under a fixed tolerance, an agent's satisfaction state changes only when the neighborhood composition changes, not when the agent's internal state evolves.

**Non-convergence of tolerance.** Under a fixed tolerance, the system converges when no agent is unsatisfied — a static equilibrium. Under CHP, the tolerance field continues to evolve after movement ceases, potentially reintroducing dissatisfaction. The system exhibits a dynamic equilibrium in which agents continue to adjust their tolerances even when no movement occurs, and movement can resume if tolerance drift crosses the satisfaction boundary.

### 6.3 Empirical Test

To verify non-equivalence empirically, we identify the fixed tolerance $\tau'$ that produces the same mean final segregation as the CHP variant ($\bar{S} \approx 0.666$). We then compare the two models on secondary metrics:

| Metric | CHP ($m = 0.05$) | Fixed $\tau'$ (matched Seg) |
|--------|-------------------|----------------------------|
| Steps to first quiescence | $>500$ (never fully quiescent) | $12$–$18$ |
| Proportion of agents that move after step 50 | $> 0$ | $= 0$ |
| Tolerance standard deviation at $t = 500$ | $0.12$–$0.18$ | $0$ (constant) |
| Fraction of agents switching satisfaction state between consecutive steps ($t > 50$) | $0.02$–$0.08$ | $0$ |

The CHP model exhibits persistent low-level dynamics (tolerance drift, occasional relocation) that the matched fixed-tolerance model does not. The two models arrive at similar *levels* of segregation but through qualitatively different *processes*.

---

## 7. Sensitivity Analysis

### 7.1 Comfort Margin Sweep

The comfort margin $m$ is the primary free parameter introduced by CHP. To assess sensitivity, we evaluate final segregation across $m \in \{0.00, 0.02, 0.05, 0.08, 0.10\}$ with all other parameters held at their default values. Each condition is run over $K = 3$ seeds.

| $m$ | $\bar{S}(T)$ | $s(T)$ |
|-----|-------------|--------|
| 0.00 | 0.644 | 0.007 |
| 0.02 | 0.651 | 0.012 |
| 0.05 | 0.665 | 0.019 |
| 0.08 | 0.726 | 0.042 |
| 0.10 | 0.763 | 0.055 |

The relationship between $m$ and final segregation is monotonically increasing: larger comfort margins produce less tolerance adaptation and therefore higher segregation, approaching the baseline as $m \to \infty$. At $m = 0$ (no dead zone), the tolerance tracks local composition directly and produces maximum desegregation. The effect is smooth, not threshold-dependent, consistent with a continuous mechanism rather than a phase transition.

### 7.2 Interpretation

The comfort margin controls the responsiveness of the tolerance update. Small $m$ produces aggressive adaptation (tolerance changes frequently); large $m$ produces conservative adaptation (tolerance changes only under large deviations). The baseline model is recovered in the limit $m \to \infty$ or $\alpha \to 0$.

---

## 8. Null Case

To establish that the CHP mechanism produces a non-trivial effect, we identify a parameter regime in which the mechanism has no impact. When $\tau_0 = 0.10$ (very low baseline tolerance), nearly all agents are satisfied at initialization regardless of local composition. Under both baseline and CHP conditions:

$$\bar{S}_{\text{base}}(\tau_0 = 0.10) \approx \bar{S}_{\text{CHP}}(\tau_0 = 0.10) \approx 0.52$$

$$|\bar{d}| < 0.01, \quad p > 0.50$$

At low tolerance, agents have no incentive to segregate, and the CHP tolerance update has no material effect because $p_i(t) \approx 0.50 > \tau_0 + m$ for most agents — the tolerance increases uniformly toward $\tau_{\max}$ without inducing any movement. This null result is consistent with the mechanism operating only when the tolerance threshold creates meaningful dissatisfaction.

---

## 9. Prior-as-Detector: Specification Drift Measurement

### 9.1 Motivation

A secondary contribution of this work is the measurement of *specification drift* in LLM-assisted code generation. When a large language model is asked to implement the Schelling model without the frozen specification in context, it generates coefficients from its training distribution rather than from the specification.

### 9.2 Drift Metric

Define a set of $J$ frozen coefficients $\{\theta_j^{\text{frozen}}\}_{j=1}^{J}$ (e.g., $\tau_0 = 0.375$, $\rho = 0.90$, update order = synchronous). For a given LLM-generated implementation, let $\hat{\theta}_j$ denote the coefficient produced for parameter $j$. The drift indicator for coefficient $j$ is:

$$\delta_j = \mathbf{1}[\hat{\theta}_j \neq \theta_j^{\text{frozen}}]$$

and the aggregate drift rate is:

$$D = \frac{1}{J} \sum_{j=1}^{J} \delta_j$$

### 9.3 Results

In a controlled experiment with $J = 11$ frozen coefficients measured across three frontier language models (GPT-4o, Grok-3, Claude):

| Condition | Drift rate $D$ |
|-----------|---------------|
| No specification in context | 0.64 (7/11 coefficients incorrect) |
| Frozen specification in prompt | 0.00 (0/11 coefficients incorrect) |

The seven drifted coefficients in the no-specification condition are:

| Coefficient | Frozen value | LLM-generated value | Drift type |
|-------------|-------------|---------------------|-----------|
| Density ($\rho$) | 0.90 | 0.80 | Common tutorial value |
| Tolerance ($\tau_0$) | 0.375 | 0.333 | Textbook approximation ($1/3$) |
| Update order | Synchronous | Sequential | Framework default |
| Max steps ($T$) | 500 | 1000 | Round number prior |
| Update rate ($\alpha$) | 0.005 | 0.01 | Round number prior |
| Tolerance min ($\tau_{\min}$) | 0.1 | 0.0 | Default range |
| Tolerance max ($\tau_{\max}$) | 0.9 | 1.0 | Default range |

Each drifted value corresponds to the most common or "textbook" variant of the parameter, consistent with the hypothesis that LLMs generate from training-data priors rather than from provided specifications when the specification is not in the active context.

### 9.4 Behavioral Drift

Specification drift extends beyond coefficient values. In approximately 40% of implementations generated with the specification in context (but without adversarial review), the tolerance update was applied *before* the movement step rather than after — producing dynamics equivalent to the baseline model despite correct coefficient values. This ordering error is undetectable from coefficient inspection alone and requires behavioral verification (running the simulation and checking the output segregation level).

The adversarial review protocol (the Critic role in CHP) detects this behavioral drift by comparing the output segregation level against the expected range: if dynamic tolerance produces $\text{Seg} > 0.80$, it matches the baseline prior rather than the CHP specification, triggering a correction cycle.

---

## References

Schelling, T. C. (1971). Dynamic models of segregation. *Journal of Mathematical Sociology*, 1(2), 143–186.

Lilja, E. (2009). *Theory and Analysis of Classic Heavy Metal Harmony*. IAML Finland.

Ioannidis, J. P. A. (2005). Why most published research findings are false. *PLoS Medicine*, 2(8), e124.
