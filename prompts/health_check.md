<!-- STATUS: template | USAGE: check CHP loop health -->
# Subagent Health Checks
# Run at the start of every turn to verify agents haven't drifted from their roles.
# Each check is 3 lines max. If the response is wrong, re-invoke with full role prompt.

## Builder Health Check

Prompt: "Confirm active. State the first architecture rule from CHAIN_PROMPT.md."
Expected: cites CHAIN_PROMPT.md content accurately.
Fail: retry once. Still failing → EXIT 2.

## Critic Health Check

Prompt: "Confirm active. You are The Pessimist. What is Gate 1 and its threshold?
         What is your specific mission regarding the frozen specification?"
Expected: "frozen compliance, must = 1.0" +
          "actively look for violations of the frozen spec"
Fail: log "critic role drift" and re-invoke with full role description.

## Reviewer Health Check

Prompt: "Confirm active. You are The Linter. What do you NOT evaluate?"
Expected: "not science, not architecture — only code hygiene"
Fail: log "reviewer role drift" and re-invoke with full role description.
