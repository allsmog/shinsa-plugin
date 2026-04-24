# Limitations and False-Positive Handling

Shinsa produces assessment support evidence. It does not certify compliance.

## Boundaries

- Repository evidence cannot prove production configuration unless that configuration is committed.
- Code cannot prove policies were approved, access reviews were completed, or operational processes happened.
- Framework conventions may hide behavior; Shinsa should mark these as `inferred` unless direct evidence is present.
- Third-party managed services require configuration evidence, screenshots, exports, or attestations outside the repo.

## Evidence Quality

| Quality | Meaning |
|---------|---------|
| strong | Direct file and line evidence supports the outcome |
| partial | Evidence supports part of the control, but gaps or manual evidence remain |
| inferred | Outcome depends on absence-of-evidence or framework convention |
| missing | No reliable evidence was found |

## Handling False Positives

1. Check the evidence path and line number.
2. Confirm whether the finding applies to production code, test code, or dead code.
3. If the code is safe by framework convention, mark evidence quality as `inferred` and request reviewer confirmation.
4. If the finding is wrong, record the reviewer note and update the domain assessor guidance or benchmark.

## Handling False Negatives

1. Use the coverage reviewer to search nearby files and framework entrypoints.
2. Add missed files to the assessment plan or assessor search guidance.
3. Add the case to a benchmark repo when the miss represents a recurring product risk.
4. Keep unresolved reviewer notes visible in the evidence pack.

## Auditor Use

Before using a Shinsa evidence pack in an audit, a human reviewer should sign off on scope, evidence quality, manual-evidence attachments, and unresolved reviewer notes.
