"""Council agent — Layer 4: Multi-model disagreement as signal."""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

_log = logging.getLogger(__name__)

COUNCIL_GPT_PROMPT_PATH = Path("prompts/council_gpt.md")
COUNCIL_GROK_PROMPT_PATH = Path("prompts/council_grok.md")


@dataclass
class CouncilReview:
    """Review from a single council member."""

    provider: str
    model: str
    response: str
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None

    @property
    def flags_drift(self) -> bool:
        """Does this review flag drift/issues?"""
        if not self.succeeded:
            return False
        text = self.response.strip()
        # Try JSON parsing first (OpenAI structured responses)
        try:
            data = json.loads(text)
            if isinstance(data, dict) and "drift_detected" in data:
                return bool(data["drift_detected"])
        except (json.JSONDecodeError, ValueError):
            pass
        else:
            # JSON parsed successfully — don't fall through to keyword matching
            return False
        # Free-text keyword matching with negation handling
        lower = text.lower()
        negation_patterns = ["no drift", "not drift", "no issues", "without drift"]
        if any(neg in lower for neg in negation_patterns):
            # Only negation present — check if there's also a positive signal
            positive_signals = ["mismatch", "incorrect", "wrong",
                               "does not match", "doesn't match", "violat"]
            return any(sig in lower for sig in positive_signals)
        drift_signals = ["drift", "mismatch", "incorrect", "wrong",
                        "does not match", "doesn't match", "violat"]
        return any(sig in lower for sig in drift_signals)


@dataclass
class CouncilResult:
    """Combined result from all council members."""

    reviews: list[CouncilReview] = field(default_factory=list)

    @property
    def n_succeeded(self) -> int:
        return sum(1 for r in self.reviews if r.succeeded)

    @property
    def consensus_issues(self) -> list[str]:
        """Find issues flagged by 2+ council members (true consensus)."""
        if self.n_succeeded < 2:
            return []

        drift_flaggers = [r.provider for r in self.reviews if r.flags_drift]

        if len(drift_flaggers) >= 2:
            return [f"Consensus drift flagged by: {', '.join(drift_flaggers)}"]
        return []

    @property
    def any_drift_flagged(self) -> bool:
        """Did any reviewer flag DRIFT?"""
        return any(r.flags_drift for r in self.reviews)


def _load_prompt(path: Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _call_openai(model: str, prompt: str, api_key: str, **kwargs: Any) -> str:
    """Call OpenAI API (GPT-4o etc)."""
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 600),
            "temperature": kwargs.get("temperature", 0.3),
            "response_format": {"type": "json_object"},
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def _call_xai(model: str, prompt: str, api_key: str, **kwargs: Any) -> str:
    """Call xAI API (Grok etc)."""
    r = requests.post(
        "https://api.x.ai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": kwargs.get("max_tokens", 600),
            "temperature": kwargs.get("temperature", 0.3),
        },
        timeout=60,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


_PROVIDERS = {
    "openai": _call_openai,
    "xai": _call_xai,
}


def run_council(
    innovation_log: str,
    council_config: list[dict[str, Any]],
) -> CouncilResult:
    """Run all council members and return their reviews.

    Parameters
    ----------
    innovation_log:
        The full innovation log text to review.
    council_config:
        List of council member configs from config.yaml, each with:
        provider, model, api_key_env, temperature, max_tokens.
    """
    result = CouncilResult()

    # Load prompt templates
    prompt_templates = {
        "openai": _load_prompt(COUNCIL_GPT_PROMPT_PATH),
        "xai": _load_prompt(COUNCIL_GROK_PROMPT_PATH),
    }

    for member in council_config:
        provider = member["provider"]
        model = member["model"]
        api_key_env = member.get("api_key_env", "")
        api_key = os.environ.get(api_key_env, "")

        if not api_key:
            review = CouncilReview(
                provider=provider,
                model=model,
                response="",
                error=f"API key not found in env var: {api_key_env}",
            )
            result.reviews.append(review)
            _log.warning("Council member %s/%s: no API key (%s)", provider, model, api_key_env)
            continue

        # Build prompt
        template = prompt_templates.get(provider, prompt_templates.get("openai", ""))
        prompt = template.replace("{log}", innovation_log)

        # Call provider
        call_fn = _PROVIDERS.get(provider)
        if call_fn is None:
            review = CouncilReview(
                provider=provider, model=model, response="",
                error=f"Unknown provider: {provider}",
            )
            result.reviews.append(review)
            continue

        try:
            _log.info("Consulting council: %s/%s ...", provider, model)
            response = call_fn(
                model, prompt, api_key,
                temperature=member.get("temperature", 0.3),
                max_tokens=member.get("max_tokens", 600),
            )
            review = CouncilReview(provider=provider, model=model, response=response)
            _log.info("Council %s/%s: received %d chars", provider, model, len(response))
        except Exception as e:
            review = CouncilReview(
                provider=provider, model=model, response="", error=str(e)
            )
            _log.error("Council %s/%s error: %s", provider, model, e)

        result.reviews.append(review)

    # Check for consensus drift flag
    if result.any_drift_flagged:
        _log.warning("COUNCIL: DRIFT flagged — re-read CHAIN_PROMPT.md before continuing")

    return result
