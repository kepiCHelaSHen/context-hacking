"""cat-earth-volcanic-explosivity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_volcanic_explosivity_constants import *
IMPL = Path(__file__).parent.parent / "earth_volcanic_explosivity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM confusions about VEI."""

    def test_vei_is_logarithmic_not_linear(self):
        """Prior error: vei_linear — VEI is logarithmic (10x volume per step above VEI 2)."""
        m = _i()
        # VEI 5 threshold should be 10x VEI 4 threshold, etc.
        for vei in range(3, 9):
            lower = m.volume_threshold_m3(vei)
            prev = m.volume_threshold_m3(vei - 1)
            ratio = lower / prev
            assert abs(ratio - 10.0) < 1e-6, (
                f"VEI {vei}/{vei-1} threshold ratio should be 10, got {ratio}"
            )

    def test_volume_thresholds_correct(self):
        """Prior error: volume_thresholds_wrong — VEI n (n>=2) starts at 10^(n+4) m³."""
        m = _i()
        for vei in range(2, 9):
            expected = 10.0 ** (vei + VEI_LOG_OFFSET)
            actual = m.volume_threshold_m3(vei)
            assert abs(actual - expected) < 1.0, (
                f"VEI {vei} threshold should be {expected:.0e}, got {actual:.0e}"
            )

    def test_km3_m3_conversion(self):
        """Prior error: km3_m3_confusion — 1 km³ = 10⁹ m³, NOT 10⁶."""
        m = _i()
        result = m.km3_to_m3(1.0)
        assert result == 1e9, f"1 km³ should be 1e9 m³, got {result}"
        assert result != 1e6, "1 km³ = 1e9 m³, NOT 1e6 (that would be 1 million, not 1 billion)"

    def test_50km3_is_vei_6_not_7(self):
        """Prior error: volume_thresholds_wrong — 50 km³ = 5e10 m³ → VEI 6, NOT VEI 7.
        VEI 6: 10^10 to 10^11 m³.  5e10 is between those bounds."""
        m = _i()
        vol_m3 = m.km3_to_m3(50.0)
        vei = m.vei_from_volume_m3(vol_m3)
        assert vei == 6, f"50 km³ (5e10 m³) should be VEI 6, got VEI {vei}"
        assert vei != 7, "50 km³ is VEI 6, NOT VEI 7"

    def test_m3_to_km3_inverse(self):
        """Verify m3_to_km3 divides by 1e9, not 1e6."""
        m = _i()
        assert m.m3_to_km3(1e9) == 1.0, "1e9 m³ should be 1 km³"
        assert m.m3_to_km3(1e6) != 1.0, "1e6 m³ is NOT 1 km³"


class TestVeiFromVolume:
    """Verify VEI classification at boundary values."""

    def test_vei_0(self):
        m = _i()
        assert m.vei_from_volume_m3(1e3) == 0, "1e3 m³ -> VEI 0"
        assert m.vei_from_volume_m3(1.0) == 0, "1 m³ -> VEI 0"

    def test_vei_1(self):
        m = _i()
        assert m.vei_from_volume_m3(1e4) == 1, "1e4 m³ -> VEI 1"
        assert m.vei_from_volume_m3(5e5) == 1, "5e5 m³ -> VEI 1"

    def test_vei_2_lower_boundary(self):
        m = _i()
        assert m.vei_from_volume_m3(1e6) == 2, "1e6 m³ -> VEI 2"

    def test_vei_5_mt_st_helens(self):
        """Mt St Helens 1980: ~1 km³ = 1e9 m³ -> VEI 5."""
        m = _i()
        vol = m.km3_to_m3(1.0)
        assert m.vei_from_volume_m3(vol) == 5

    def test_vei_7_tambora(self):
        """Tambora 1815: ~100 km³ = 1e11 m³ -> VEI 7."""
        m = _i()
        vol = m.km3_to_m3(100.0)
        assert m.vei_from_volume_m3(vol) == 7

    def test_vei_8_yellowstone(self):
        """Yellowstone: ~1000 km³ = 1e12 m³ -> VEI 8."""
        m = _i()
        vol = m.km3_to_m3(1000.0)
        assert m.vei_from_volume_m3(vol) == 8

    def test_vei_8_very_large(self):
        """Extremely large eruption still capped at VEI 8."""
        m = _i()
        assert m.vei_from_volume_m3(1e15) == 8

    def test_invalid_volume_raises(self):
        m = _i()
        with pytest.raises(ValueError):
            m.vei_from_volume_m3(-1)
        with pytest.raises(ValueError):
            m.vei_from_volume_m3(0)

    def test_reference_case(self):
        """Frozen ref: 5e10 m³ (50 km³) -> VEI 6."""
        m = _i()
        assert m.vei_from_volume_m3(REF_VOLUME_M3) == REF_VEI_EXPECTED


class TestVolumeThreshold:
    """Verify volume_threshold_m3 returns correct lower bounds."""

    def test_all_thresholds_match_constants(self):
        m = _i()
        for vei, expected in VEI_THRESHOLDS_M3.items():
            assert m.volume_threshold_m3(vei) == expected, (
                f"VEI {vei} threshold: expected {expected}, got {m.volume_threshold_m3(vei)}"
            )

    def test_invalid_vei_raises(self):
        m = _i()
        with pytest.raises(KeyError):
            m.volume_threshold_m3(-1)
        with pytest.raises(KeyError):
            m.volume_threshold_m3(9)

    def test_monotonically_increasing(self):
        m = _i()
        prev = -1
        for vei in range(9):
            thresh = m.volume_threshold_m3(vei)
            assert thresh > prev, f"VEI {vei} threshold ({thresh}) must exceed VEI {vei-1} ({prev})"
            prev = thresh


class TestUnitConversion:
    """Verify km3<->m3 conversions."""

    def test_km3_to_m3_known_values(self):
        m = _i()
        assert m.km3_to_m3(1.0) == 1e9
        assert m.km3_to_m3(0.001) == 1e6
        assert m.km3_to_m3(1000.0) == 1e12

    def test_m3_to_km3_known_values(self):
        m = _i()
        assert m.m3_to_km3(1e9) == 1.0
        assert m.m3_to_km3(1e12) == 1000.0
        assert m.m3_to_km3(1e6) == 0.001

    def test_round_trip(self):
        m = _i()
        for val in [0.5, 1.0, 50.0, 1000.0]:
            assert abs(m.m3_to_km3(m.km3_to_m3(val)) - val) < 1e-9
