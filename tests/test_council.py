"""Tests for council consensus detection."""
from context_hacking.agents.council import CouncilResult, CouncilReview


class TestConsensusDetection:
    def test_consensus_when_both_flag_drift(self):
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["coefficient mismatch"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="DRIFT DETECTED: coefficient values don't match spec"),
        ]
        result = CouncilResult(reviews=reviews)
        assert result.any_drift_flagged
        assert len(result.consensus_issues) > 0

    def test_no_consensus_single_flag(self):
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["coefficient mismatch"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="Code looks correct. No drift detected."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0

    def test_no_consensus_no_flags(self):
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": false, "issues": []}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="Everything looks good."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0
        assert not result.any_drift_flagged

    def test_partial_failure_graceful(self):
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='', error="API timeout"),
            CouncilReview(provider="xai", model="grok-3",
                         response="DRIFT DETECTED: wrong constants"),
        ]
        result = CouncilResult(reviews=reviews)
        assert result.n_succeeded == 1
        assert result.any_drift_flagged
