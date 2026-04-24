---
name: control-implement
description: Maintainer-only implementation workflow that executes a Shinsa plan artifact with review and eval gates
argument-hint: "<slug> [--auto] [--review] [--no-pr]"
allowed-tools:
  - Bash
  - Glob
  - Grep
  - Read
  - Write
  - Agent
  - TodoWrite
  - AskUserQuestion
---

# Control Implement

Use this command only when implementing a Shinsa maintainer plan. Do not use it against an assessed target repository.

## Goal

Read `.plans/<slug>.md`, implement it in the plugin repo, review the changes cold, benchmark the result, and validate the benchmark before shipping.

## Preconditions

Fail fast if any of these are missing:

- `.plans/<slug>.md`
- required plan sections from `/shinsa:control-plan`
- no unresolved `[TBD]` or `[NEEDS CLARIFICATION]` markers

If the plan is incomplete, stop and direct the maintainer back to `/shinsa:control-plan`.

## Workflow

### Phase 1: Parse the plan

Extract:

- contract changes
- implementation tasks
- verification scenarios
- required commands, agents, skills, references, and scripts

Write `.plans/<slug>/implementation-notes.md` before editing.

### Phase 2: Execute tasks with cold review

For each logical task:

1. Implement the task
2. Run a fresh cold review against the diff and the plan
3. If review requests changes, revise and re-review
4. Stop after 3 rounds and annotate unresolved issues

Cold review must not rely on the implementer reasoning. Use the plan artifact plus current diff only.

### Phase 3: Benchmark and eval

Write benchmark output to `.plans/<slug>/benchmark.json`.

The benchmark must cover:

- trigger behavior
- schema contract validity
- evidence anchoring
- doc/command/agent inventory consistency
- reviewer pass rate

Run:

```bash
python3 scripts/validate_evals.py .plans/<slug>/benchmark.json
```

Do not treat the work as complete if this validation fails.

### Phase 4: Optional git checkpoints

If the maintainer wants checkpoint commits, use one commit per approved task. Suggested prefixes:

- `[implement] task: <slug>`
- `[implement] review-fixes: <slug>`
- `[implement] benchmarked: <slug>`
