# Prompts Index — Context Hacking Protocol

All prompts live in `prompts/`. Run any prompt with:
```
claude --dangerously-skip-permissions < prompts/<name>.md
```

---

## Run (Executed)

These prompts have been executed and produced output.

| Prompt | Description | Command |
|--------|-------------|---------|
| math_sprint.md | One-hour sprint: e, pi, sqrt(2) arbitrary-precision | `claude --dangerously-skip-permissions < prompts/math_sprint.md` |
| euler_e.md | Compute Euler's e past the LLM float ceiling | `claude --dangerously-skip-permissions < prompts/euler_e.md` |
| dashboard_sync.md | Fix drift between dashboard, figures, and tests | `claude --dangerously-skip-permissions < prompts/dashboard_sync.md` |
| dashboard_redesign.md | White clinical theme + control panel for dashboard | `claude --dangerously-skip-permissions < prompts/dashboard_redesign.md` |
| consolidate.md | Consolidate experiments into single index | `claude --dangerously-skip-permissions < prompts/consolidate.md` |
| anatomy_viewer.md | Verified anatomical viewer (Gray's Anatomy data) | `claude --dangerously-skip-permissions < prompts/anatomy_viewer.md` |
| anatomy_viewer_vtk.md | 3D anatomical viewer using VTK | `claude --dangerously-skip-permissions < prompts/anatomy_viewer_vtk.md` |
| overnight_fix.md | Full overnight consolidation pass | `claude --dangerously-skip-permissions < prompts/overnight_fix.md` |
| chemistry_sprint.md | 10 verified chemistry experiments | `claude --dangerously-skip-permissions < prompts/chemistry_sprint.md` |

## Ready to Run (Staged)

No prompts currently staged. Move prompts here when they are written but not yet executed.

## Agent Roles

These prompts define agent personas for the CHP loop. They are not run standalone.

| Prompt | Role | Command |
|--------|------|---------|
| builder.md | The Implementer — builds exactly what is specified | `claude --dangerously-skip-permissions < prompts/builder.md` |
| critic.md | The Pessimist — proves the science is wrong | `claude --dangerously-skip-permissions < prompts/critic.md` |
| reviewer.md | The Linter — code hygiene only | `claude --dangerously-skip-permissions < prompts/reviewer.md` |
| council_gpt.md | Council reviewer sent to GPT-4o | `claude --dangerously-skip-permissions < prompts/council_gpt.md` |
| council_grok.md | Council reviewer sent to Grok | `claude --dangerously-skip-permissions < prompts/council_grok.md` |

## Templates

Reusable templates for creating new prompts or checking loop health.

| Prompt | Purpose | Command |
|--------|---------|---------|
| loop_template.md | Starting point for new experiment prompts | `claude --dangerously-skip-permissions < prompts/loop_template.md` |
| health_check.md | Verify CHP loop agents haven't drifted | `claude --dangerously-skip-permissions < prompts/health_check.md` |
