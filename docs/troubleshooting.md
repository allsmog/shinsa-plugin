# Troubleshooting

## Install Problems

- Confirm the plugin path points at the repository root.
- Confirm `.claude-plugin/plugin.json` exists.
- Restart Claude Code after adding the plugin.

## Scan Produces No Findings

- Check `shinsa-output/runs/<assessment_id>/scope.md` to confirm source files were counted.
- Check `assessment-plan.md` to confirm the requested controls were in scope.
- Use a quick check for one known control, such as `/shinsa:quick-check A.8.5`.

## Missing Evidence Pack Sections

Run:

```bash
python3 scripts/validate_evals.py evals/benchmark.sample.json
```

The validator fails if canonical evidence packs omit required sections such as `Executive Summary`, `Control Matrix`, `Evidence Index`, `Reviewer Notes`, `Limitations`, or `Human Sign-Off`.

## Resume Problems

Full scans resume only incomplete runs for the matching standard. Candidate state files are filtered by `standard` and `run.phase != "completed"`, then sorted by `last_updated` with file mtime as fallback.

If no matching incomplete run exists, start a new scan instead of using `--resume`.

## Reviewer Disagreements

- `changes_requested`: rerun affected domain assessors and reviewers.
- `unresolved`: finalize the evidence pack with the unresolved risk visible.
- `approved`: evidence is sufficient for the reported outcome, subject to human sign-off.

## Generated Output Cleanup

Generated assessment output lives under `shinsa-output/` and is ignored by git. Golden product examples use `expected-shinsa-output/` so expected evidence packs can be reviewed and versioned.
