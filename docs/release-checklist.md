# Release Checklist

Use this checklist before publishing a Shinsa plugin release.

## Validation

```bash
python3 scripts/quick_validate.py
python3 scripts/validate_evals.py evals/benchmark.sample.json
python3 -m py_compile scripts/quick_validate.py scripts/validate_evals.py
```

## Product Proof

- Golden API evidence pack exists and validates.
- Golden platform evidence pack exists and validates.
- At least one benchmark includes reviewer-requested changes or unresolved reviewer notes.
- README first-run path matches current command names and artifact paths.

## Contract Review

- `references/assessment.schema.json` version and README state contract match.
- Evidence pack sections match `references/orchestration-contract.md`.
- Schema compatibility notes are captured in the changelog.

## GRC Review

- Supported controls page distinguishes automated, hybrid, and manual evidence.
- Limitations page states that Shinsa does not certify compliance.
- Evidence packs include human sign-off placeholders.
- Manual evidence needs are visible for hybrid controls.
