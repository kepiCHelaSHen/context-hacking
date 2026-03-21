---
name: chp-init
description: "Initialize a new CHP project in the current directory. Creates all template files, frozen/ folder, and config.yaml."
tools: Write, Bash
---

Create the following CHP project structure in the current directory:

## Files to create

1. **CHAIN_PROMPT.md** — Ask the user what their project is about, then write
   the master design doc with: project identity, purpose, confirmed design
   decisions (empty — user fills in), architecture rules, frozen code section.

2. **config.yaml** — CHP configuration with the user's project name and
   sensible defaults for all 9 layers.

3. **innovation_log.md** — Empty template with header.

4. **dead_ends.md** — Empty template with format instructions.

5. **state_vector.md** — Initial state (Turn 0, VALIDATION, not started).

6. **frozen/** — Empty directory. Tell user to put their immutable spec here.

7. **tests/** — Empty directory with __init__.py.

## After creating

Tell the user:
- "Edit CHAIN_PROMPT.md with your design decisions"
- "Put your frozen specification in frozen/"
- "Type /chp-run to start the first build turn"
