---
name: chp-dashboard-sync
description: "Fix all drift between dashboard/app.py, context_hacking/figures.py, and tests/"
tools: Read, Write, Edit, Bash
---

# CHP Dashboard Sync — Fix All Drift Between Files

You have one job: find every place where dashboard/app.py, context_hacking/figures.py,
and tests/test_figures.py have drifted out of sync, then fix them all.

No new features. No refactoring. Just sync.

================================================================================
STEP 0 — READ EVERYTHING FIRST
================================================================================

Read ALL of these before touching anything:

  1. dashboard/app.py                     — current dashboard (has drift)
  2. context_hacking/figures.py           — authoritative figure source
  3. tests/test_figures.py                — existing test suite
  4. dashboard/health_patch.py            — dead file (check if imported)

Do not write a single line until you have read all four.

================================================================================
KNOWN DRIFT — FIX ALL OF THESE
================================================================================

These are the confirmed drift problems. Fix every one.

────────────────────────────────────────────────────────────────────────────────
DRIFT 1: FIGURE_DESCRIPTIONS defined twice — must be single source of truth
────────────────────────────────────────────────────────────────────────────────

Current state:
  - context_hacking/figures.py defines FIGURE_DESCRIPTIONS (authoritative)
  - dashboard/app.py ALSO defines its own FIGURE_DESCRIPTIONS (duplicate, already diverged)

Fix:
  In dashboard/app.py, DELETE the hardcoded FIGURE_DESCRIPTIONS dict entirely.
  Replace with a single import at the top of the file:

    from context_hacking.figures import FIGURE_DESCRIPTIONS

  That's it. One source. The dashboard reads from the package.

  Verify: after the fix, grep dashboard/app.py for "FIGURE_DESCRIPTIONS = {" —
  it must not exist.

────────────────────────────────────────────────────────────────────────────────
DRIFT 2: figures.py FIGURE_DESCRIPTIONS is missing entries that exist on disk
────────────────────────────────────────────────────────────────────────────────

Entries that exist as actual .png files in chp-test-run/experiments/*/figures/
but are NOT in context_hacking/figures.py FIGURE_DESCRIPTIONS:

  "lorenz_chp_story"   — CHP Prior-as-Detector: Wrong -> Detected -> Corrected
  "cluster_map"        — Cluster labels: spatially contiguous same-type groups
  "r0_distribution"    — R0 estimate distribution across seeds
  "lyapunov_convergence" — Lyapunov exponent convergence across time
  "phase_portrait"     — Phase space: prey vs predator population trajectory
  "cooperation_rate"   — Cooperation rate per generation

Fix:
  Add all six missing keys to FIGURE_DESCRIPTIONS in context_hacking/figures.py.
  Use em-dash (—) as separator, matching the existing style in that file.

────────────────────────────────────────────────────────────────────────────────
DRIFT 3: figures.py _dark_style() conflicts with white dashboard
────────────────────────────────────────────────────────────────────────────────

Current state:
  _dark_style() sets figure background to #0a0a1a (near-black).
  The dashboard background is #F8F9FC (near-white).
  Dark figures on white cards look broken.

Fix:
  Replace _dark_style() with _white_style() that generates publication-white figures:

    def _white_style():
        import matplotlib.pyplot as plt
        plt.style.use("default")
        plt.rcParams.update({
            "figure.facecolor":  "#FFFFFF",
            "axes.facecolor":    "#FAFBFC",
            "axes.edgecolor":    "#C8CCDB",
            "text.color":        "#374151",
            "axes.labelcolor":   "#374151",
            "xtick.color":       "#6B7280",
            "ytick.color":       "#6B7280",
            "grid.color":        "#E2E5EF",
            "font.family":       "monospace",
        })

  Replace every call to _dark_style() in the file with _white_style().

  Update the inline color choices that were chosen for dark backgrounds:
    "#00ff88" (neon green) -> "#065F46" (dark green, readable on white)
    "#ff4444" (neon red)   -> "#991B1B" (dark red, readable on white)
    "#4488ff" (neon blue)  -> "#1D4ED8" (dark blue, readable on white)
    "#ffaa00" (neon amber) -> "#D97706" (amber, readable on white)
    "#cc44ff" (neon purple)-> "#6D28D9" (purple, readable on white)
    "#0a0a1a" (bg color)   -> "#FFFFFF"
    "#0d0d20" (bg color)   -> "#FAFBFC"

  Check every ax.set_facecolor(), fig.set_facecolor(), ax.set_title() color=
  in the file and apply the mapping above.

  Also update the Schelling figure suptitle:
    color="#00ff88" -> color="#065F46"

  And the Lorenz figure title:
    color="#00ff88" -> color="#065F46"

────────────────────────────────────────────────────────────────────────────────
DRIFT 4: health_patch.py is a dead file
────────────────────────────────────────────────────────────────────────────────

Current state:
  dashboard/health_patch.py exists but dashboard/app.py never imports it.
  The function it defines (_render_protocol_health_contained) is a better
  version of _render_protocol_health in app.py, but it's not being used.

Fix option A (preferred): Delete health_patch.py.
  The contained 2-column layout is already implemented directly in app.py's
  _render_protocol_health function from the last rewrite. The patch file is
  redundant. Delete it.

    import os; os.remove("dashboard/health_patch.py")

  OR use Bash: rm dashboard/health_patch.py

Fix option B (if A fails for any reason): Add the import to app.py.
  Only use this if the file cannot be deleted.

────────────────────────────────────────────────────────────────────────────────
DRIFT 5: EXPERIMENT_CATALOG icons are wrong ASCII characters
────────────────────────────────────────────────────────────────────────────────

Current state in dashboard/app.py:
  The encoding-safe rewrite replaced all emoji with single ASCII letters:
    "schelling-segregation": {"icon": "H", ...}
    "spatial-prisoners-dilemma": {"icon": "D", ...}
    etc.

Fix:
  Restore the correct emoji in EXPERIMENT_CATALOG in dashboard/app.py:

    "schelling-segregation":      "icon": "\U0001F3D8"   # 🏘
    "spatial-prisoners-dilemma":  "icon": "\U0001F3B2"   # 🎲
    "lotka-volterra":             "icon": "\U0001F43A"   # 🐺
    "sir-epidemic":               "icon": "\U0001F9A0"   # 🦠
    "ml-hyperparam-search":       "icon": "\U0001F916"   # 🤖
    "lorenz-attractor":           "icon": "\U0001F98B"   # 🦋
    "quantum-grover":             "icon": "\u269B"       # ⚛
    "izhikevich-neurons":         "icon": "\U0001F9E0"   # 🧠
    "blockchain-consensus":       "icon": "\U0001F517"   # 🔗

  Use Unicode escape sequences (\U000...) rather than literal emoji characters
  to avoid any future encoding issues. Python will render them correctly.

  Also fix the page icon in st.set_page_config:
    page_icon="O"   ->  page_icon="\u2B21"   # ⬡ (hexagon)

────────────────────────────────────────────────────────────────────────────────
DRIFT 6: tests/test_figures.py does not test the new entries
────────────────────────────────────────────────────────────────────────────────

Current state:
  test_figures.py tests for 5 specific keys in FIGURE_DESCRIPTIONS.
  After fixing Drift 2, there will be 6 new keys.
  The tests won't cover them.

Fix:
  Add the six new keys to the test_known_keys test:

    def test_known_keys(self):
        assert "schelling_comparison"  in FIGURE_DESCRIPTIONS
        assert "lorenz_attractor"      in FIGURE_DESCRIPTIONS
        assert "lorenz_chp_story"      in FIGURE_DESCRIPTIONS   # NEW
        assert "grover_amplitude"      in FIGURE_DESCRIPTIONS
        assert "izhikevich_patterns"   in FIGURE_DESCRIPTIONS
        assert "metal_vs_classical"    in FIGURE_DESCRIPTIONS
        assert "cluster_map"           in FIGURE_DESCRIPTIONS   # NEW
        assert "r0_distribution"       in FIGURE_DESCRIPTIONS   # NEW
        assert "lyapunov_convergence"  in FIGURE_DESCRIPTIONS   # NEW
        assert "phase_portrait"        in FIGURE_DESCRIPTIONS   # NEW
        assert "cooperation_rate"      in FIGURE_DESCRIPTIONS   # NEW

  Also add a test that confirms FIGURE_DESCRIPTIONS is NOT defined in app.py
  (enforces the single-source-of-truth fix from Drift 1):

    def test_dashboard_imports_not_defines_figure_descriptions():
        """app.py must import FIGURE_DESCRIPTIONS, not define its own."""
        app_src = (Path(__file__).parent.parent / "dashboard" / "app.py").read_text(encoding="utf-8")
        # Must NOT contain a local dict definition
        assert "FIGURE_DESCRIPTIONS: dict" not in app_src, (
            "dashboard/app.py defines its own FIGURE_DESCRIPTIONS — "
            "it must import from context_hacking.figures instead"
        )
        # Must import from the package
        assert "from context_hacking.figures import" in app_src, (
            "dashboard/app.py must import FIGURE_DESCRIPTIONS from context_hacking.figures"
        )

  And a test that health_patch.py is gone:

    def test_no_dead_patch_file():
        """health_patch.py must not exist as an unimported dead file."""
        patch_path = Path(__file__).parent.parent / "dashboard" / "health_patch.py"
        if patch_path.exists():
            app_src = (Path(__file__).parent.parent / "dashboard" / "app.py").read_text(encoding="utf-8")
            assert "health_patch" in app_src, (
                "dashboard/health_patch.py exists but is never imported in app.py — "
                "either import it or delete it"
            )

================================================================================
ORDER OF OPERATIONS
================================================================================

Do the fixes in this order to avoid breaking intermediate states:

  1. Fix figures.py first (Drifts 2 and 3) — add missing keys, swap color palette
  2. Fix tests/test_figures.py (Drift 6) — add new assertions
  3. Run tests: python -m pytest tests/test_figures.py -v
     All tests must pass before touching the dashboard.
  4. Fix dashboard/app.py (Drifts 1, 4, 5):
     a. Add import from context_hacking.figures
     b. Delete FIGURE_DESCRIPTIONS dict
     c. Delete health_patch.py
     d. Fix EXPERIMENT_CATALOG icons
     e. Fix page_icon
  5. Run tests again: python -m pytest tests/ -v
     All tests must still pass.
  6. Verify dashboard starts: python -c "import dashboard.app" (should not error)

================================================================================
SELF-CHECK BEFORE FINISHING
================================================================================

Run each check. Report PASS or FAIL for each.

  [ ] grep -n "FIGURE_DESCRIPTIONS = {" dashboard/app.py
      Expected: no output (zero matches)
      FAIL if any match found

  [ ] grep -n "from context_hacking.figures import" dashboard/app.py
      Expected: at least one match
      FAIL if no match found

  [ ] python -c "from context_hacking.figures import FIGURE_DESCRIPTIONS; print(len(FIGURE_DESCRIPTIONS), 'keys')"
      Expected: prints a number >= 27 (21 original + 6 new)
      FAIL if import error or count < 27

  [ ] python -c "from context_hacking.figures import FIGURE_DESCRIPTIONS; assert 'lorenz_chp_story' in FIGURE_DESCRIPTIONS"
      Expected: no error
      FAIL if AssertionError

  [ ] python -c "from context_hacking.figures import FIGURE_DESCRIPTIONS; assert 'cluster_map' in FIGURE_DESCRIPTIONS"
      Expected: no error
      FAIL if AssertionError

  [ ] ls dashboard/health_patch.py 2>&1
      Expected: "No such file or directory" (file deleted)
      FAIL if file still exists

  [ ] python -m pytest tests/test_figures.py -v
      Expected: all tests PASS
      FAIL if any test fails

  [ ] python -c "from context_hacking.figures import generate_figures; print('figures import OK')"
      Expected: "figures import OK"
      FAIL if import error

  [ ] grep -n "\"icon\": \"H\"" dashboard/app.py
      Expected: no output (old ASCII icon gone)
      FAIL if match found

  [ ] grep -n "page_icon=\"O\"" dashboard/app.py
      Expected: no output (wrong icon gone)
      FAIL if match found

  [ ] grep -n "#0a0a1a\|#0d0d20\|#00ff88" context_hacking/figures.py
      Expected: no output (dark colors replaced)
      FAIL if match found

  [ ] python -m pytest tests/ -v
      Expected: all tests PASS
      FAIL if any test fails

================================================================================
DONE
================================================================================

When all checks pass, report:

  "Dashboard sync complete.
   6 fixes applied:
   1. FIGURE_DESCRIPTIONS: single source (figures.py), removed from app.py
   2. figures.py: 6 missing keys added
   3. figures.py: dark style replaced with white style
   4. health_patch.py: deleted
   5. EXPERIMENT_CATALOG: emoji icons restored
   6. tests/test_figures.py: 7 new assertions added
   All N tests passing."
