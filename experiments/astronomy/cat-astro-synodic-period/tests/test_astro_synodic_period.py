"""cat-astro-synodic-period — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_synodic_period_constants import *
IMPL = Path(__file__).parent.parent / "astro_synodic_period.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-Error Tests (the mistakes LLMs make) ──────────────────────────

class TestPriorErrors:
    def test_same_formula_all_venus(self):
        """same_formula_all: Using superior formula for Venus gives negative S."""
        m = _i()
        # Correct: inferior formula → positive S ≈ 583.93 days
        S = m.synodic_inferior(P_EARTH, P_VENUS)
        assert S > 0, "Synodic period must be positive"
        assert abs(S - S_VENUS) / S_VENUS < 1e-6, (
            f"Venus synodic period should be {S_VENUS:.2f} d, got {S:.2f} d"
        )
        # Wrong: superior formula would give NEGATIVE S
        assert WRONG_S_VENUS < 0, "Superior formula for Venus must yield negative S"

    def test_same_formula_all_mercury(self):
        """same_formula_all: Using superior formula for Mercury gives negative S."""
        m = _i()
        S = m.synodic_inferior(P_EARTH, P_MERCURY)
        assert S > 0
        assert abs(S - S_MERCURY) / S_MERCURY < 1e-6

    def test_synodic_is_not_sidereal(self):
        """synodic_is_sidereal: Synodic != sidereal period."""
        m = _i()
        S_mars = m.synodic_auto(P_EARTH, P_MARS)
        # Synodic period of Mars (779.88 d) is NOT its sidereal period (687.0 d)
        assert abs(S_mars - P_MARS) > 50, (
            f"Synodic period ({S_mars:.1f} d) must differ from "
            f"sidereal period ({P_MARS} d) — they are not the same concept"
        )

    def test_negative_period_rejected(self):
        """negative_period: synodic_auto must never return negative S."""
        m = _i()
        # All planets must give positive synodic periods
        for P in [P_MARS, P_VENUS, P_MERCURY, P_JUPITER, P_SATURN]:
            S = m.synodic_auto(P_EARTH, P)
            assert S > 0, f"Got negative S for P={P}"

    def test_superior_formula_rejects_inferior_planet(self):
        """same_formula_all: synodic_superior must reject inferior planets."""
        m = _i()
        with pytest.raises(ValueError):
            m.synodic_superior(P_EARTH, P_VENUS)

    def test_inferior_formula_rejects_superior_planet(self):
        """same_formula_all: synodic_inferior must reject superior planets."""
        m = _i()
        with pytest.raises(ValueError):
            m.synodic_inferior(P_EARTH, P_MARS)


# ── Correctness Tests ────────────────────────────────────────────────────

class TestCorrectness:
    def test_mars_synodic_period(self):
        """Mars (superior): S ≈ 779.88 days ≈ 2.135 yr."""
        m = _i()
        S = m.synodic_superior(P_EARTH, P_MARS)
        assert abs(S - S_MARS) / S_MARS < 1e-6

    def test_venus_synodic_period(self):
        """Venus (inferior): S ≈ 583.93 days ≈ 1.599 yr."""
        m = _i()
        S = m.synodic_inferior(P_EARTH, P_VENUS)
        assert abs(S - S_VENUS) / S_VENUS < 1e-6

    def test_mercury_synodic_period(self):
        """Mercury (inferior): S ≈ 115.88 days ≈ 0.317 yr."""
        m = _i()
        S = m.synodic_inferior(P_EARTH, P_MERCURY)
        assert abs(S - S_MERCURY) / S_MERCURY < 1e-6

    def test_jupiter_synodic_period(self):
        """Jupiter (superior): S ≈ 398.88 days ≈ 1.092 yr."""
        m = _i()
        S = m.synodic_superior(P_EARTH, P_JUPITER)
        assert abs(S - S_JUPITER) / S_JUPITER < 1e-6

    def test_saturn_synodic_period(self):
        """Saturn (superior): S ≈ 378.09 days ≈ 1.035 yr."""
        m = _i()
        S = m.synodic_superior(P_EARTH, P_SATURN)
        assert abs(S - S_SATURN) / S_SATURN < 1e-6

    def test_synodic_auto_mars(self):
        """synodic_auto picks superior formula for Mars."""
        m = _i()
        S = m.synodic_auto(P_EARTH, P_MARS)
        assert abs(S - S_MARS) / S_MARS < 1e-6

    def test_synodic_auto_venus(self):
        """synodic_auto picks inferior formula for Venus."""
        m = _i()
        S = m.synodic_auto(P_EARTH, P_VENUS)
        assert abs(S - S_VENUS) / S_VENUS < 1e-6

    def test_synodic_auto_mercury(self):
        """synodic_auto picks inferior formula for Mercury."""
        m = _i()
        S = m.synodic_auto(P_EARTH, P_MERCURY)
        assert abs(S - S_MERCURY) / S_MERCURY < 1e-6

    def test_is_superior_mars(self):
        """Mars is a superior planet (P > P_earth)."""
        m = _i()
        assert m.is_superior(P_MARS, P_EARTH) is True

    def test_is_superior_venus(self):
        """Venus is NOT a superior planet (P < P_earth)."""
        m = _i()
        assert m.is_superior(P_VENUS, P_EARTH) is False

    def test_zero_period_raises(self):
        """Zero sidereal period must raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.synodic_auto(P_EARTH, 0)

    def test_negative_period_raises(self):
        """Negative sidereal period must raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.synodic_auto(P_EARTH, -100)

    def test_equal_period_raises(self):
        """Same period as Earth (S=infinity) must raise ValueError."""
        m = _i()
        with pytest.raises(ValueError):
            m.synodic_auto(P_EARTH, P_EARTH)

    def test_synodic_always_greater_than_sidereal_for_superior(self):
        """For superior planets, synodic period > sidereal period of Earth."""
        m = _i()
        for P in [P_MARS, P_JUPITER, P_SATURN]:
            S = m.synodic_auto(P_EARTH, P)
            assert S > P_EARTH, (
                f"Superior synodic S={S:.1f} should exceed P_earth={P_EARTH}"
            )
