"""Tests for the telemetry system."""


import pytest

from context_hacking.core.telemetry import TelemetryStore, TurnMetrics, TurnTimer


class TestTurnMetrics:
    def test_defaults(self):
        m = TurnMetrics()
        assert m.turn == 0
        assert m.tokens_total == 0
        assert m.drift_rate == 0.0
        assert m.false_positive_caught is False

    def test_set_values(self):
        m = TurnMetrics(turn=3, tokens_total=5000, gate_3_scientific=0.88)
        assert m.turn == 3
        assert m.tokens_total == 5000
        assert m.gate_3_scientific == 0.88


class TestTurnTimer:
    def test_timer_records_duration(self):
        import time
        m = TurnMetrics()
        with TurnTimer(m):
            time.sleep(0.1)
        assert m.duration_seconds >= 0.09
        assert m.duration_seconds < 1.0


class TestTelemetryStore:
    def test_empty_store(self):
        store = TelemetryStore()
        assert store.total_turns == 0
        assert store.total_tokens == 0

    def test_add_turn(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".chp").mkdir()
        store = TelemetryStore(project_name="test")
        store.add_turn(TurnMetrics(turn=1, tokens_total=1000, lines_written=50))
        store.add_turn(TurnMetrics(turn=2, tokens_total=800, lines_written=30))
        assert store.total_turns == 2
        assert store.total_tokens == 1800
        assert store.total_lines_written == 80

    def test_save_and_load(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / ".chp").mkdir()
        store = TelemetryStore(project_name="roundtrip")
        store.add_turn(TurnMetrics(turn=1, tokens_total=500, false_positive_caught=True))
        store.save()

        loaded = TelemetryStore.load()
        assert loaded.total_turns == 1
        assert loaded.false_positives_caught == 1
        assert loaded.project_name == "roundtrip"

    def test_tokens_per_line(self):
        store = TelemetryStore()
        store.turns = [
            TurnMetrics(tokens_total=1000, lines_written=100),
            TurnMetrics(tokens_total=800, lines_written=80),
        ]
        assert store.tokens_per_line == pytest.approx(10.0)

    def test_mean_drift_rate(self):
        store = TelemetryStore()
        store.turns = [
            TurnMetrics(coefficients_checked=10, coefficients_matched=8, drift_rate=0.2),
            TurnMetrics(coefficients_checked=10, coefficients_matched=10, drift_rate=0.0),
        ]
        assert store.mean_drift_rate == pytest.approx(0.1)

    def test_first_try_pass_rate(self):
        store = TelemetryStore()
        store.turns = [
            TurnMetrics(tests_passed=5, tests_failed=0, tests_passed_first_try=True),
            TurnMetrics(tests_passed=3, tests_failed=2, tests_passed_first_try=False),
            TurnMetrics(tests_passed=5, tests_failed=0, tests_passed_first_try=True),
        ]
        assert store.first_try_pass_rate == pytest.approx(2/3)

    def test_anomaly_rate(self):
        store = TelemetryStore()
        store.turns = [
            TurnMetrics(anomaly=False),
            TurnMetrics(anomaly=True),
            TurnMetrics(anomaly=False),
            TurnMetrics(anomaly=False),
        ]
        assert store.anomaly_rate == pytest.approx(0.25)

    def test_trend(self):
        store = TelemetryStore()
        store.turns = [
            TurnMetrics(tokens_total=1000),
            TurnMetrics(tokens_total=900),
            TurnMetrics(tokens_total=800),
        ]
        t = store.trend("tokens_total", window=3)
        assert t == [1000.0, 900.0, 800.0]

    def test_summary(self):
        store = TelemetryStore()
        store.turns = [TurnMetrics(turn=1, tokens_total=500, lines_written=50)]
        s = store.summary()
        assert s["total_turns"] == 1
        assert s["total_tokens"] == 500
        assert "mean_gates" in s
