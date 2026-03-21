---
name: chp-status
description: "Show current CHP project status: turn, mode, gates, dead ends, next focus."
tools: Read, Glob
---

Read these files and present a concise status report:

1. **state_vector.md** — current turn, mode, milestone, flags
2. **dead_ends.md** — count and list dead end titles
3. **innovation_log.md** — last turn's "what next" section
4. **config.yaml** — project name and gate definitions

## Output format

```
CHP Status: [project name]
  Turn:       [N]
  Mode:       [VALIDATION / EXPLORATION / DONE]
  Milestone:  [current]
  Gates:      [last result or "not run yet"]
  Dead ends:  [count] — [list titles]
  Flags:      [any open flags or "none"]
  Next focus: [from last innovation log entry]
```

Then suggest: "Type /chp-run to execute the next turn."
