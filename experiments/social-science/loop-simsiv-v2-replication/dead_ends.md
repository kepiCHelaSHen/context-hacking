# SIMSIV v2 Replication — Dead Ends Log
# Pre-loaded from actual SIMSIV v2 build (11 turns + post-review fixes)
# These are REAL dead ends from REAL development. Do NOT repeat any.

---

## DEAD END 1 — n <= 4 bands for between-group selection detection

**What was attempted**: Exp 2 factorial with 4 bands per condition (2 Free + 2 State).

**Result**: At n=3 seeds, interaction effect +0.039 (appeared to support Bowles).
At n=10 seeds: +0.0004, p=0.954. FALSE POSITIVE. All conditions converge to ~0.505.

**Why this is a dead end**: Pearson r on 4 data points has inherent std ~0.2-0.4.
Between-group selection is undetectable at this scale. Need n=20+ bands.

**Do NOT repeat**: Any experiment with n<=4 bands expecting to detect selection effects.

---

## DEAD END 2 — Blended fitness proxy (0.6/0.4 demographic + raid)

**What was attempted**: band_fitness = 0.6 * demographic + 0.4 * raid_win_rate.

**Result**: Not comparable to Bowles (2006) eq. 1 which uses pure demographic fitness.
The blended coefficient is apples-to-oranges with the literature.

**Why this is a dead end**: Split into demographic_selection_coeff and raid_selection_coeff.
Each is independently interpretable against the Price equation.

**Do NOT repeat**: Blending fitness components without citation.

---

## DEAD END 3 — Migration routing: all migrants to one destination

**What was attempted**: Per origin band, pick ONE random destination, send ALL
migrants there.

**Result**: Pulsed directional gene flow instead of Wright island-model uniform flow.
Fst INCREASES with migration rate (opposite of theoretical prediction).

**Why this is a dead end**: Each agent must independently choose a destination
weighted by trust*(1-distance). Per-agent choice, not per-band.

**Do NOT repeat**: Any migration where destination is chosen per-band instead of per-agent.

---

## DEAD END 4 — fighter.die("raid", 0) — wrong death year

**What was attempted**: Passing year=0 as placeholder in kill_fighters.

**Result**: All raid casualties recorded as dying in year 0. Corrupts mortality data.

**Do NOT repeat**: Always thread the actual simulation year through the call chain.

---

## DEAD END 5 — law_strength read from society instead of society.config

**What was attempted**: getattr(band.society, "law_strength", 0.0)

**Result**: Society doesn't have law_strength — it's on society.config. Returns 0.0
for all bands. Silent data corruption.

**Do NOT repeat**: Always read config attributes from band.society.config, not band.society.

---

## DEAD END 6 — Default trust 0.5 (too high for raids to fire)

**What was attempted**: Initial inter-band trust defaults to 0.5.

**Result**: raid_trust_suppression_threshold=0.4, so trust_deficit = 0 when trust >= 0.4.
Raids never fire because trust starts above the threshold.

**Why this is a dead end**: Bowles (2009): forager bands treat unmet groups with moderate
distrust. Default 0.3 enables the raid mechanism from early ticks.

**Do NOT repeat**: Default trust above 0.3 for inter-band relationships.

---

## DEAD END 7 — n=3 seeds gives false positives (Ioannidis 2005)

**What was attempted**: Reporting results from n=3 seeds as findings.

**Result**: Exp 2 interaction +0.039 at n=3 → +0.0004 at n=10 → dead.
Minimum detectable effect at 80% power with n=3 requires d=2.9.
Observed d~0.45. Statistical power: ~10%. False discovery rate: >50%.

**Do NOT repeat**: Any directional claim from n<6 seeds. Replicate at n=10 minimum.

---

## DEAD END 8 — Raid scarcity threshold too low for default resources

**What was attempted**: raid_scarcity_threshold=3.0 with default resources ~10/agent.

**Result**: scarcity = max(0, 1 - 10/3) = 0. Raids never trigger because
resources always exceed the threshold.

**Do NOT repeat**: Scarcity threshold must be ABOVE mean resources (~15-20) for
raids to have nonzero trigger probability.
