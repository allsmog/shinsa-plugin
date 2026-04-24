---
name: control-plan
description: Maintainer-only planning workflow for new control coverage, prompt refactors, and evaluator changes in the Shinsa plugin
argument-hint: "<slug> [--standard iso27001|nist-800-53] [--area commands|agents|skills|evals]"
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

# Control Plan

Use this command only when evolving the Shinsa plugin itself. Do not use it to assess a third-party codebase.

## Goal

Create a durable maintainer plan artifact for any of these changes:

- new ISO or NIST control coverage
- prompt or orchestration refactors
- reviewer workflow changes
- eval harness changes

## Artifact Rules

Write artifacts under `.plans/`:

- `.plans/<slug>.md`
- `.plans/<slug>/research.md`

The plan file is the contract for `/shinsa:control-implement`.

## Workflow

### Phase 1: Research the existing implementation

Read the relevant commands, agents, skills, references, and validation scripts. Record:

- current command or agent coverage
- contract changes needed
- files likely to change
- backwards-compatibility risks

Persist the result in `.plans/<slug>/research.md`.

### Phase 2: Write the implementation plan

Write `.plans/<slug>.md` with these required sections:

1. `# Title`
2. `## Context`
3. `## Approach`
4. `## Contract Changes`
5. `## Implementation Overview`
6. `## Feature Verification`
7. `## Task List`

The plan must be decision complete. Do not leave `[TBD]` or `[NEEDS CLARIFICATION]`.

### Phase 3: Adversarial review

Run three cold reviews against the plan artifact:

- artifact completeness and contract drift
- control interpretation and standards correctness
- coverage and false-negative risk

Use fresh reviewer agents and provide the plan plus research artifacts, not your hidden reasoning.

### Phase 4: Revise the plan

If any reviewer requests changes:

- update `.plans/<slug>.md`
- persist reviewer outputs under `.plans/<slug>/reviews/round-<n>/`
- re-run all three reviewers
- stop after 3 rounds and annotate unresolved issues in the plan

### Phase 5: Optional maintainer checkpoints

If the user wants git checkpoints, use these commit message prefixes:

- `[plan] AI-reviewed: <slug>`
- `[plan] user-feedback: <slug>`
- `[plan] re-reviewed: <slug>`
- `[plan] approved: <slug>`
