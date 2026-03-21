# SIMSIV v1 Replication — Dead Ends Log
# Pre-loaded from actual SIMSIV development history (27 sessions)

---

## DEAD END 1 — getattr false defaults in conflict engine

**What was attempted**: Used getattr(config, 'X', False) for optional config
values, which silently disables coalition_defense, leadership, and
third_party_punishment when a partial config is passed.

**Result**: Critical features disabled without warning. The simulation runs
but produces unrealistically low conflict rates.

**Why this is a dead end**: Use direct attribute access on Config dataclass.
Config.__post_init__ validates all fields. No silent defaults.

**Do NOT repeat**: getattr with False default for any behavioral flag.

---

## DEAD END 2 — Simple trait averaging instead of h²-weighted inheritance

**What was attempted**: Child trait = (parent1_trait + parent2_trait) / 2.

**Result**: No heritability weighting. All traits inherited at h²=1.0 effective.
This overestimates genetic contribution for low-h² traits (empathy h²=0.35)
and underestimates for high-h² traits (intelligence h²=0.65).

**Why this is a dead end**: The frozen spec requires h²-weighted midparent:
  child_trait = h² * midparent + (1-h²) * population_mean + mutation
where mutation ~ N(0, 0.05).

**Do NOT repeat**: Any inheritance formula without h² weighting.

---

## DEAD END 3 — Single-phase resource distribution

**What was attempted**: Resources distributed as base_per_agent * intelligence.

**Result**: Missing 7 of the 8 frozen resource phases: cooperation sharing,
tool bonus, prestige allocation, taxation, storage, decay, and Gini computation.
The economy collapses to pure meritocracy without redistribution mechanisms.

**Why this is a dead end**: The frozen spec has an 8-phase pipeline. Each phase
feeds into the next. Skipping phases produces fundamentally different dynamics.

**Do NOT repeat**: Any resource system with fewer than 8 phases.

---

## DEAD END 4 — Fixed institutions instead of emergent drift

**What was attempted**: law_strength as a static config parameter that never changes.

**Result**: In EMERGENT_INSTITUTIONS scenario, law_strength stays at 0 forever.
The frozen spec shows law_strength self-organizing from 0 to 0.83 over 200yr
via the institutional drift mechanism (cooperation_norm drives drift direction).

**Why this is a dead end**: Institutional drift is a core mechanism that makes
cooperation and institutions co-evolve. Without it, the model cannot test the
central research question (Bowles vs North).

**Do NOT repeat**: Any institution engine without a drift rate mechanism.

---

## DEAD END 5 — rng.choice on object lists

**What was attempted**: Passed Agent objects directly to rng.choice() for
random selection.

**Result**: Works in current numpy version but has no cross-version determinism
guarantee. Different numpy versions may iterate object arrays differently.

**Why this is a dead end**: Use index-based sampling: select a random index,
then use it to pick from the list. This is deterministic across numpy versions.

**Do NOT repeat**: rng.choice on lists of non-numeric objects.
