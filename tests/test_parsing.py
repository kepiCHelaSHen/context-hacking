"""Comprehensive parse robustness tests for all agent parsers."""


class TestCriticParseRobustness:
    """Critic parse_verdict handles every format the LLM might produce."""

    def test_standard_format(self):
        from context_hacking.agents.critic import parse_verdict
        text = """
        Gate 1 (frozen_compliance): 1.0
        Gate 2 (architecture): 0.90
        Gate 3 (scientific_validity): 0.85
        Gate 4 (drift_check): 0.95
        Verdict: PASS
        blocking_issues:
        NONE
        next_turn_priority: Optimize convergence
        """
        v = parse_verdict(text)
        assert v.gate_1_frozen == 1.0
        assert v.gate_2_architecture == 0.9
        assert v.passed

    def test_fraction_format(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0/1.0\nGate 2: 0.9/1.0\nGate 3: 0.85/1.0\nGate 4: 0.9/1.0\nVerdict: PASS"
        v = parse_verdict(text)
        assert v.gate_1_frozen == 1.0
        assert v.gate_2_architecture == 0.9

    def test_percentage_format(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 100%\nGate 2: 85%\nGate 3: 90%\nGate 4: 80%\nVerdict: PASS"
        v = parse_verdict(text)
        assert v.gate_1_frozen == 1.0
        assert v.gate_2_architecture == 0.85

    def test_empty_string(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict("")
        assert v.verdict == "PARSE_FAILED"
        assert not v.passed

    def test_whitespace_only(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict("   \n\n  \t  ")
        assert v.verdict == "PARSE_FAILED"

    def test_unstructured_garbage(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict(
            "The implementation looks solid."
            " I have no concerns about the architecture."
        )
        assert v.verdict == "PARSE_FAILED"

    def test_partial_gates(self):
        """Some gates present, others missing -- shouldn't PARSE_FAILED."""
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0\nGate 3: 0.85\nVerdict: NEEDS_IMPROVEMENT"
        v = parse_verdict(text)
        assert v.gate_1_frozen == 1.0
        assert v.gate_3_scientific == 0.85
        assert v.verdict != "PARSE_FAILED"

    def test_missing_gates_default_zero(self):
        """Gates not mentioned default to 0.0."""
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0\nGate 3: 0.85\nVerdict: PASS"
        v = parse_verdict(text)
        assert v.gate_2_architecture == 0.0
        assert v.gate_4_drift == 0.0

    def test_all_gates_met_property(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0\nGate 2: 0.90\nGate 3: 0.90\nGate 4: 0.90\nVerdict: PASS"
        v = parse_verdict(text)
        assert v.all_gates_met

    def test_all_gates_not_met_when_below_threshold(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 0.99\nGate 2: 0.90\nGate 3: 0.90\nGate 4: 0.90\nVerdict: PASS"
        v = parse_verdict(text)
        assert not v.all_gates_met  # gate 1 must be exactly 1.0

    def test_blocking_issues_extracted(self):
        from context_hacking.agents.critic import parse_verdict
        text = """
        Gate 1: 1.0
        Gate 2: 0.8
        Gate 3: 0.85
        Gate 4: 0.9
        Verdict: NEEDS_IMPROVEMENT
        blocking_issues:
        - Missing validation step
        - Incorrect coefficient
        """
        v = parse_verdict(text)
        assert v.has_blocking
        assert len(v.blocking_issues) == 2

    def test_blocking_issues_none_keyword(self):
        from context_hacking.agents.critic import parse_verdict
        text = """
        Gate 1: 1.0
        Gate 2: 0.9
        Verdict: PASS
        blocking_issues:
        NONE
        """
        v = parse_verdict(text)
        assert not v.has_blocking

    def test_next_priority_extracted(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0\nGate 2: 0.9\nVerdict: PASS\nnext_turn_priority: Optimize convergence"
        v = parse_verdict(text)
        assert v.next_priority == "Optimize convergence"

    def test_none_input(self):
        from context_hacking.agents.critic import parse_verdict
        v = parse_verdict(None)
        assert v.verdict == "PARSE_FAILED"

    def test_score_clamped_above_100(self):
        """Scores above 100% should clamp to 1.0."""
        from context_hacking.agents.critic import _extract_gate
        assert _extract_gate("Gate 1: 150%", 1) == 1.0

    def test_score_clamped_below_zero(self):
        """Negative scores should clamp to 0.0 (unlikely but defensive)."""
        from context_hacking.agents.critic import _extract_gate
        # Pattern expects [0-9], so negative won't match -- returns 0.0 default
        assert _extract_gate("Gate 1: -0.5", 1) == 0.0

    def test_verdict_pass_case_insensitive(self):
        from context_hacking.agents.critic import parse_verdict
        text = "Gate 1: 1.0\nGate 2: 0.9\nGate 3: 0.9\nGate 4: 0.9\nverdict: pass"
        v = parse_verdict(text)
        assert v.passed

    def test_gate_with_text_label(self):
        """Gate followed by descriptive label, e.g. 'Gate 1 (frozen_compliance): 1.0'."""
        from context_hacking.agents.critic import _extract_gate
        assert _extract_gate("Gate 1 (frozen_compliance): 1.0", 1) == 1.0
        assert _extract_gate("Gate 2 (architecture_quality): 0.9", 2) == 0.9

    def test_gate_underscore_format(self):
        """gate_1_frozen style (used in test_framework.py)."""
        from context_hacking.agents.critic import _extract_gate
        assert _extract_gate("gate_1_frozen: 1.0", 1) == 1.0
        assert _extract_gate("gate_2_arch: 0.95", 2) == 0.95

    def test_decimal_without_leading_zero(self):
        from context_hacking.agents.critic import _extract_gate
        assert _extract_gate("Gate 1: .95", 1) == 0.95


class TestReviewerParseRobustness:
    """Reviewer parse_review handles variant formats."""

    def test_standard_format(self):
        from context_hacking.agents.reviewer import parse_review
        text = """
        CRITICAL: sim.py:42 — Uses print() instead of logging
        WARNING: model.py:10 — Missing type annotation
        MINOR: config.py:1 — Unused import
        Verdict: APPROVE WITH NOTES
        """
        r = parse_review(text)
        assert r.critical_count == 1
        assert r.warning_count == 1
        assert r.verdict == "APPROVE WITH NOTES"

    def test_bold_markers(self):
        from context_hacking.agents.reviewer import parse_review
        text = "**CRITICAL**: `sim.py:42` — Uses print()\nVerdict: NEEDS REVISION"
        r = parse_review(text)
        assert r.critical_count >= 1
        assert r.needs_revision

    def test_empty_string(self):
        from context_hacking.agents.reviewer import parse_review
        r = parse_review("")
        assert r.verdict == "PARSE_FAILED"
        assert r.needs_revision

    def test_no_issues_approve(self):
        from context_hacking.agents.reviewer import parse_review
        text = "No issues found.\nVerdict: APPROVE"
        r = parse_review(text)
        assert r.critical_count == 0
        assert r.verdict == "APPROVE"

    def test_whitespace_only(self):
        from context_hacking.agents.reviewer import parse_review
        r = parse_review("   \n\n   ")
        assert r.verdict == "PARSE_FAILED"

    def test_none_input(self):
        from context_hacking.agents.reviewer import parse_review
        r = parse_review(None)
        assert r.verdict == "PARSE_FAILED"
        assert r.needs_revision

    def test_needs_revision_implies_needs_revision_property(self):
        from context_hacking.agents.reviewer import parse_review
        text = "CRITICAL: file.py:1 — bad\nVerdict: NEEDS REVISION"
        r = parse_review(text)
        assert r.needs_revision

    def test_critical_implies_needs_revision_even_with_approve(self):
        """needs_revision is True if any CRITICAL issue exists, regardless of verdict text."""
        from context_hacking.agents.reviewer import parse_review
        text = "CRITICAL: file.py:1 — bad\nVerdict: APPROVE"
        r = parse_review(text)
        assert r.needs_revision  # critical_count > 0 overrides APPROVE

    def test_warning_only_not_needs_revision(self):
        from context_hacking.agents.reviewer import parse_review
        text = "WARNING: file.py:1 — something\nVerdict: APPROVE WITH NOTES"
        r = parse_review(text)
        assert not r.needs_revision

    def test_file_line_notation(self):
        """'model.py line 10' notation."""
        from context_hacking.agents.reviewer import parse_review
        text = "WARNING: model.py line 10 - Missing type annotation\nVerdict: APPROVE WITH NOTES"
        r = parse_review(text)
        assert len(r.issues) == 1
        assert r.issues[0].line == 10

    def test_bare_severity_no_file(self):
        """MINOR - desc (no file reference)."""
        from context_hacking.agents.reviewer import parse_review
        text = "MINOR - Unused import\nVerdict: APPROVE WITH NOTES"
        r = parse_review(text)
        assert len(r.issues) >= 1
        assert r.issues[0].severity == "MINOR"

    def test_multiple_criticals(self):
        from context_hacking.agents.reviewer import parse_review
        text = """
        CRITICAL: a.py:1 — first
        CRITICAL: b.py:2 — second
        CRITICAL: c.py:3 — third
        Verdict: NEEDS REVISION
        """
        r = parse_review(text)
        assert r.critical_count == 3

    def test_mixed_case_severity(self):
        """Severity keywords are case-insensitive."""
        from context_hacking.agents.reviewer import parse_review
        text = "critical: file.py:1 — bad\nVerdict: NEEDS REVISION"
        r = parse_review(text)
        assert r.critical_count == 1

    def test_verdict_without_prefix(self):
        """Verdict keyword without 'Verdict:' prefix, just on its own line."""
        from context_hacking.agents.reviewer import parse_review
        text = "WARNING: file.py:1 — something\nAPPROVE WITH NOTES"
        r = parse_review(text)
        assert r.verdict == "APPROVE WITH NOTES"

    def test_parse_failed_has_synthetic_critical(self):
        """PARSE_FAILED result contains a synthetic CRITICAL issue."""
        from context_hacking.agents.reviewer import parse_review
        r = parse_review("")
        assert len(r.issues) == 1
        assert r.issues[0].severity == "CRITICAL"
        assert "PARSE_FAILED" in r.issues[0].description


class TestCouncilConsensusRobustness:
    """Council consensus detection edge cases."""

    def test_both_flag_drift_with_json(self):
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["wrong coefficient"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="DRIFT: the coefficient does not match the spec"),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) > 0

    def test_all_models_failed(self):
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o", response="", error="timeout"),
            CouncilReview(provider="xai", model="grok-3", response="", error="rate limit"),
        ]
        result = CouncilResult(reviews=reviews)
        assert result.n_succeeded == 0
        assert len(result.consensus_issues) == 0
        assert not result.any_drift_flagged

    def test_single_model_no_consensus(self):
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["problem"]}'),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0  # Need 2+ for consensus

    def test_negation_not_false_positive(self):
        """'No drift detected' should NOT flag drift."""
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": false, "issues": []}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="No drift detected. Everything matches the spec."),
        ]
        result = CouncilResult(reviews=reviews)
        assert not result.any_drift_flagged

    def test_json_drift_false_not_flagged(self):
        """JSON with drift_detected=false should not flag."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="openai", model="gpt-4o",
                               response='{"drift_detected": false, "issues": []}')
        assert not review.flags_drift

    def test_json_drift_true_flagged(self):
        """JSON with drift_detected=true should flag."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="openai", model="gpt-4o",
                               response='{"drift_detected": true, "issues": ["bad"]}')
        assert review.flags_drift

    def test_json_without_drift_key_not_flagged(self):
        """Valid JSON without drift_detected key should not flag (else branch)."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="openai", model="gpt-4o",
                               response='{"summary": "all good", "score": 10}')
        assert not review.flags_drift

    def test_freetext_drift_keyword(self):
        """Free-text with 'drift' keyword flags drift."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="xai", model="grok-3",
                               response="I found significant drift from the specification.")
        assert review.flags_drift

    def test_freetext_mismatch_keyword(self):
        """Free-text with 'mismatch' keyword flags drift."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="xai", model="grok-3",
                               response="There is a mismatch between spec and implementation.")
        assert review.flags_drift

    def test_freetext_violation_keyword(self):
        """Free-text with 'violat*' keyword flags drift."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="xai", model="grok-3",
                               response="This violates the frozen specification.")
        assert review.flags_drift

    def test_freetext_no_issues_negation(self):
        """'no issues' negation prevents false positive."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="xai", model="grok-3",
                               response="I found no issues with the implementation.")
        assert not review.flags_drift

    def test_negation_with_positive_signal_flags_drift(self):
        """Negation present but also a positive signal like 'incorrect' -- should flag."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="xai", model="grok-3",
                               response="No drift in architecture,"
                                       " but the coefficient is incorrect.")
        assert review.flags_drift

    def test_failed_review_never_flags_drift(self):
        """A review with error should never flag drift."""
        from context_hacking.agents.council import CouncilReview
        review = CouncilReview(provider="openai", model="gpt-4o",
                               response="drift everywhere!", error="timeout")
        assert not review.flags_drift

    def test_empty_reviews_list(self):
        from context_hacking.agents.council import CouncilResult
        result = CouncilResult(reviews=[])
        assert result.n_succeeded == 0
        assert len(result.consensus_issues) == 0
        assert not result.any_drift_flagged

    def test_consensus_requires_two_flaggers(self):
        """One flagger + one non-flagger = no consensus."""
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["bad"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="No drift detected. All good."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 0
        assert result.any_drift_flagged  # at least one flagged

    def test_three_models_two_flag_consensus(self):
        """With 3 models, 2 flagging drift = consensus."""
        from context_hacking.agents.council import CouncilResult, CouncilReview
        reviews = [
            CouncilReview(provider="openai", model="gpt-4o",
                         response='{"drift_detected": true, "issues": ["bad"]}'),
            CouncilReview(provider="xai", model="grok-3",
                         response="I found drift in the implementation."),
            CouncilReview(provider="anthropic", model="claude-3",
                         response="No drift detected."),
        ]
        result = CouncilResult(reviews=reviews)
        assert len(result.consensus_issues) == 1
        assert "openai" in result.consensus_issues[0]
        assert "xai" in result.consensus_issues[0]

    def test_succeeded_property(self):
        from context_hacking.agents.council import CouncilReview
        ok = CouncilReview(provider="openai", model="gpt-4o", response="ok")
        assert ok.succeeded
        fail = CouncilReview(provider="openai", model="gpt-4o", response="", error="timeout")
        assert not fail.succeeded
