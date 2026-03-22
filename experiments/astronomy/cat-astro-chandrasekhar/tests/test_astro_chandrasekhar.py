"""cat-astro-chandrasekhar — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_chandrasekhar_constants import *
IMPL = Path(__file__).parent.parent / "astro_chandrasekhar.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three documented LLM failure modes."""

    def test_not_rounded_to_1_point_4(self):
        """CRITICAL: M_Ch must be ≈1.44, NOT 1.4 — the 0.04 matters."""
        m = _i(); mch = m.chandrasekhar_mass(mu_e=2.0)
        # Must be closer to 1.44 than to 1.4
        assert mch > 1.42, f"Got {mch}, too low — should be ≈1.44-1.46, not 1.4"
        assert abs(mch - M_CH_WRONG_ROUNDED) > 0.02, (
            f"Got {mch}, suspiciously close to 1.4 — rounding error?"
        )

    def test_more_massive_wd_is_smaller(self):
        """R ∝ M^(-1/3): more massive WD must have SMALLER radius."""
        m = _i()
        r_low = m.wd_radius_relative(0.6)
        r_high = m.wd_radius_relative(1.2)
        assert r_high < r_low, (
            f"R(1.2M)={r_high} >= R(0.6M)={r_low} — more massive WD must be SMALLER!"
        )

    def test_not_tov_limit(self):
        """Chandrasekhar limit ≈1.44 M_sun, NOT TOV limit ≈2-3 M_sun."""
        m = _i(); mch = m.chandrasekhar_mass(mu_e=2.0)
        assert mch < 2.0, (
            f"Got {mch} M_sun — this is TOV territory, not Chandrasekhar!"
        )
        assert abs(mch - M_TOV_MSUN) > 0.5, (
            f"Got {mch} M_sun — suspiciously close to TOV limit {M_TOV_MSUN}"
        )


class TestCorrectness:
    """Verify numerical accuracy against precomputed constants."""

    def test_chandrasekhar_mass_co_wd(self):
        """M_Ch for C/O white dwarf (μ_e=2) matches frozen constant."""
        m = _i(); mch = m.chandrasekhar_mass(mu_e=2.0)
        assert abs(mch - M_CH_MSUN) / M_CH_MSUN < 1e-6

    def test_chandrasekhar_mass_kg(self):
        """M_Ch in kg matches frozen constant."""
        m = _i(); mch_kg = m.chandrasekhar_mass_kg(mu_e=2.0)
        assert abs(mch_kg - M_CH_KG) / M_CH_KG < 1e-6

    def test_chandrasekhar_mass_fe_wd(self):
        """M_Ch for iron-core WD (μ_e=2.154) matches frozen constant."""
        m = _i(); mch = m.chandrasekhar_mass(mu_e=MU_E_FE)
        assert abs(mch - M_CH_FE_MSUN) / M_CH_FE_MSUN < 1e-6

    def test_formula_5_83_over_mu_e_squared(self):
        """M_Ch = 5.83 / μ_e² — verify formula directly."""
        m = _i()
        for mu_e in [1.0, 1.5, 2.0, 2.154, 3.0]:
            expected = 5.83 / mu_e ** 2
            got = m.chandrasekhar_mass(mu_e=mu_e)
            assert abs(got - expected) / expected < 1e-10, (
                f"μ_e={mu_e}: got {got}, expected {expected}"
            )

    def test_wd_radius_inverse_cube_root(self):
        """R ∝ M^(-1/3) — verify exponent."""
        m = _i()
        r1 = m.wd_radius_relative(1.0)
        r8 = m.wd_radius_relative(8.0)
        # 8^(-1/3) = 0.5, so r8/r1 should be 0.5
        ratio = r8 / r1
        assert abs(ratio - 0.5) < 1e-10, f"R(8)/R(1) = {ratio}, expected 0.5"

    def test_wd_radius_unit_mass(self):
        """R(1.0) = 1.0 (reference point)."""
        m = _i()
        assert abs(m.wd_radius_relative(1.0) - 1.0) < 1e-10

    def test_wd_radius_rejects_nonpositive(self):
        """Mass ratio must be positive."""
        m = _i()
        with pytest.raises(ValueError):
            m.wd_radius_relative(0.0)
        with pytest.raises(ValueError):
            m.wd_radius_relative(-1.0)

    def test_is_above_limit_true(self):
        """1.5 M_sun exceeds the Chandrasekhar limit."""
        m = _i(); assert m.is_above_limit(1.5)

    def test_is_above_limit_false(self):
        """1.0 M_sun is below the Chandrasekhar limit."""
        m = _i(); assert not m.is_above_limit(1.0)

    def test_is_above_limit_boundary(self):
        """Exactly at 1.44 is NOT above (must strictly exceed)."""
        m = _i(); assert not m.is_above_limit(1.44)

    def test_kg_and_msun_consistent(self):
        """kg result = M_sun result × M_SUN constant."""
        m = _i()
        mch_msun = m.chandrasekhar_mass(mu_e=2.0)
        mch_kg = m.chandrasekhar_mass_kg(mu_e=2.0)
        assert abs(mch_kg - mch_msun * M_SUN) / (mch_msun * M_SUN) < 1e-10
