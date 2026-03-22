"""cat-bio-island-biogeography — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from bio_island_biogeography_constants import *
IMPL = Path(__file__).parent.parent / "bio_island_biogeography.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_z_island_is_030_not_05_or_10(self):
        """Canonical island z must be ~0.30, NOT 0.5 or 1.0."""
        m = _i()
        z = m.z_island()
        assert 0.25 <= z <= 0.35, \
            f"Island z={z} outside valid range [0.25, 0.35]; canonical is 0.30"
        assert z < 0.40, \
            f"Island z={z} is too high — z ~ 0.5 is a known LLM error"
        assert z > 0.10, \
            f"Island z={z} is too low — likely using mainland z for islands"

    def test_z_mainland_is_015_not_030(self):
        """Mainland z must be ~0.15, distinctly lower than island z."""
        m = _i()
        z = m.z_mainland()
        assert 0.12 <= z <= 0.17, \
            f"Mainland z={z} outside valid range [0.12, 0.17]; canonical is 0.15"

    def test_doubling_area_does_not_double_species(self):
        """Doubling area should give ~23% more species (z=0.30), NOT 100%."""
        m = _i()
        z = m.z_island()
        ratio = m.doubling_ratio(z)
        # Must be well below 2.0 (which would mean doubling species)
        assert ratio < 1.50, \
            f"Doubling ratio {ratio:.4f} is too high — doubling area must NOT double species"
        # Must be above 1.0 (more area → more species)
        assert ratio > 1.0, \
            f"Doubling ratio {ratio:.4f} must be > 1.0 — more area means more species"

    def test_species_area_is_power_law_not_linear(self):
        """S = c * A^z is a power law. If z were 1.0, S would be linear in A."""
        m = _i()
        S100 = m.species_area(C_TEST, 100, Z_ISLAND)
        S200 = m.species_area(C_TEST, 200, Z_ISLAND)
        S1000 = m.species_area(C_TEST, 1000, Z_ISLAND)
        # If linear (z=1): doubling area doubles species, 10x area → 10x species
        # With z=0.30: doubling → ~1.23x, 10x → ~2x
        ratio_double = S200 / S100
        ratio_tenfold = S1000 / S100
        assert ratio_double < 1.50, \
            f"S(200)/S(100) = {ratio_double:.4f} — too close to 2.0 (linear relationship)"
        assert ratio_tenfold < 3.0, \
            f"S(1000)/S(100) = {ratio_tenfold:.4f} — too close to 10.0 (linear relationship)"


class TestCorrectness:
    def test_species_count_A100(self):
        """S(c=10, A=100, z=0.30) = 39.8107..."""
        m = _i()
        S = m.species_area(C_TEST, A_TEST, Z_ISLAND)
        assert math.isclose(S, S_AT_100, rel_tol=1e-6), \
            f"S={S}, expected {S_AT_100}"

    def test_species_count_A200(self):
        """S(c=10, A=200, z=0.30) = 49.0127..."""
        m = _i()
        S = m.species_area(C_TEST, 200, Z_ISLAND)
        assert math.isclose(S, S_AT_200, rel_tol=1e-6), \
            f"S={S}, expected {S_AT_200}"

    def test_species_count_A1000(self):
        """S(c=10, A=1000, z=0.30) = 79.4328..."""
        m = _i()
        S = m.species_area(C_TEST, 1000, Z_ISLAND)
        assert math.isclose(S, S_AT_1000, rel_tol=1e-6), \
            f"S={S}, expected {S_AT_1000}"

    def test_doubling_ratio_island(self):
        """2^0.30 = 1.2311..."""
        m = _i()
        ratio = m.doubling_ratio(Z_ISLAND)
        assert math.isclose(ratio, DOUBLING_RATIO_ISLAND, rel_tol=1e-6), \
            f"Doubling ratio={ratio}, expected {DOUBLING_RATIO_ISLAND}"

    def test_doubling_ratio_mainland(self):
        """2^0.15 = 1.1096..."""
        m = _i()
        ratio = m.doubling_ratio(Z_MAINLAND)
        assert math.isclose(ratio, DOUBLING_RATIO_MAINLAND, rel_tol=1e-6), \
            f"Doubling ratio={ratio}, expected {DOUBLING_RATIO_MAINLAND}"

    def test_tenfold_area_roughly_doubles_species(self):
        """10x area with z=0.30 gives ~2x species (ratio ~1.995)."""
        m = _i()
        S100 = m.species_area(C_TEST, A_TEST, Z_ISLAND)
        S1000 = m.species_area(C_TEST, 1000, Z_ISLAND)
        ratio = S1000 / S100
        assert math.isclose(ratio, TENFOLD_RATIO_ISLAND, rel_tol=1e-4), \
            f"10x area ratio={ratio}, expected {TENFOLD_RATIO_ISLAND}"

    def test_z_island_value(self):
        m = _i()
        assert m.z_island() == 0.30

    def test_z_mainland_value(self):
        m = _i()
        assert m.z_mainland() == 0.15
