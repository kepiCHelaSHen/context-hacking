"""cat-astro-tidal-locking — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_tidal_locking_constants import *
IMPL = Path(__file__).parent.parent / "astro_tidal_locking.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod


# ── Prior-Error Tests (the mistakes LLMs make) ──────────────────────────

class TestPriorErrors:
    def test_a_sixth_not_cubed(self):
        """a_cubed_not_sixth: timescale ratio must use a⁶, not a³.
        Doubling distance → 2⁶ = 64×, NOT 2³ = 8×."""
        mod = _import_impl()
        ratio = mod.locking_timescale_ratio(A_MOON, A_MOON_HALF)
        # Must be 64, not 8
        assert abs(ratio - 64.0) < 0.01, (
            f"Ratio = {ratio:.2f}, expected 64.0 (a⁶). Got ~8? That's a³ — WRONG."
        )

    def test_q_wrong_order(self):
        """q_wrong_order: Q values must be correct order of magnitude.
        Earth Q≈12, Jupiter Q≈10⁵ — off by ~4 orders of magnitude."""
        mod = _import_impl()
        q_earth = mod.q_factor("Earth")
        q_jupiter = mod.q_factor("Jupiter")
        # Earth Q should be ~12 (order 10¹)
        assert 5 < q_earth < 50, f"Earth Q = {q_earth}, expected ~12"
        # Jupiter Q should be ~10⁵ (order 10⁵)
        assert 1e4 < q_jupiter < 1e7, f"Jupiter Q = {q_jupiter}, expected ~10⁵"
        # The ratio should be huge — at least 1000×
        assert q_jupiter / q_earth > 1000, (
            f"Jupiter Q / Earth Q = {q_jupiter / q_earth:.0f}, "
            f"should be >1000 (different by orders of magnitude)"
        )

    def test_mercury_not_locked(self):
        """mercury_is_locked: Mercury is NOT tidally locked — it's in 3:2 resonance."""
        mod = _import_impl()
        locked = mod.is_tidally_locked(T_SPIN_MERCURY, T_ORBIT_MERCURY)
        assert locked is False, (
            "Mercury should NOT be tidally locked (1:1). "
            "It is in a 3:2 spin-orbit resonance."
        )
        resonance = mod.spin_orbit_resonance(T_SPIN_MERCURY, T_ORBIT_MERCURY)
        assert resonance == "3:2", (
            f"Mercury resonance = '{resonance}', expected '3:2'"
        )


# ── Correctness Tests ────────────────────────────────────────────────────

class TestCorrectness:
    def test_locking_ratio_identity(self):
        """Same distance → ratio = 1."""
        mod = _import_impl()
        ratio = mod.locking_timescale_ratio(A_MOON, A_MOON)
        assert abs(ratio - 1.0) < 1e-10

    def test_locking_ratio_triple_distance(self):
        """Triple distance → 3⁶ = 729× longer."""
        mod = _import_impl()
        ratio = mod.locking_timescale_ratio(3 * A_MOON, A_MOON)
        assert abs(ratio - 729.0) < 0.01

    def test_moon_is_locked(self):
        """Moon is tidally locked to Earth (spin = orbital period)."""
        mod = _import_impl()
        locked = mod.is_tidally_locked(T_SPIN_MOON, T_ORBIT_MOON)
        assert locked is True, "Moon should be tidally locked"

    def test_pluto_charon_locked(self):
        """Pluto-Charon: mutually tidally locked."""
        mod = _import_impl()
        locked_pluto = mod.is_tidally_locked(T_SPIN_PLUTO, T_ORBIT_PLUTO_CHARON)
        locked_charon = mod.is_tidally_locked(T_SPIN_CHARON, T_ORBIT_PLUTO_CHARON)
        assert locked_pluto is True, "Pluto should be locked to Charon"
        assert locked_charon is True, "Charon should be locked to Pluto"

    def test_resonance_moon_1to1(self):
        """Moon resonance should be '1:1'."""
        mod = _import_impl()
        res = mod.spin_orbit_resonance(T_SPIN_MOON, T_ORBIT_MOON)
        assert res == "1:1", f"Moon resonance = '{res}', expected '1:1'"

    def test_q_factor_moon(self):
        """Moon Q should be ~27."""
        mod = _import_impl()
        q = mod.q_factor("Moon")
        assert abs(q - Q_MOON) < 0.01

    def test_q_factor_case_insensitive(self):
        """Q lookup should be case-insensitive."""
        mod = _import_impl()
        assert mod.q_factor("earth") == mod.q_factor("EARTH") == mod.q_factor("Earth")

    def test_q_factor_unknown_raises(self):
        """Unknown body should raise ValueError."""
        mod = _import_impl()
        with pytest.raises(ValueError):
            mod.q_factor("Pluto")

    def test_locking_ratio_scaling(self):
        """Verify a⁶ scaling: ratio(k*a, a) = k⁶ for several k values."""
        mod = _import_impl()
        for k in [0.5, 1.5, 2.0, 4.0, 10.0]:
            ratio = mod.locking_timescale_ratio(k * A_MOON, A_MOON)
            expected = k ** 6
            assert abs(ratio - expected) / expected < 1e-9, (
                f"k={k}: ratio={ratio:.4f}, expected {expected:.4f}"
            )
