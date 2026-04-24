# Changelog

## 3.2.0 - Enterprise Trust Fields

- Upgraded assessor prompts to emit evidence quality rationale, confidence rationale, manual evidence checklists, reviewer disposition, and GRC action for every control.
- Upgraded cold-review prompts to challenge evidence quality, manual evidence needs, overclaiming, and false-negative risk.
- Rewrote the evidence-generation skill around ISO/NIST enterprise evidence packs.
- Expanded golden evidence packs with assessment metadata, raw artifact references, richer control rows, and unresolved-risk propagation.
- Strengthened eval validation for domain JSON trust fields, control matrix completeness, report metadata, and unresolved reviewer propagation.

Compatibility note: assessment state schema is now `1.4.0`. Consumers of `controls[]` should expect `manual_evidence_items`, `confidence_rationale`, `evidence_quality_rationale`, and `grc_action` in addition to the 1.3.0 trust fields.

## 3.1.0 - Enterprise Evidence Packs

- Added canonical enterprise evidence-pack sections for final reports.
- Added schema fields for evidence quality, manual-evidence need, and reviewer disposition.
- Added golden API and platform benchmark examples with expected evidence packs.
- Added validation for evidence-pack report sections and benchmark quality notes.
- Added Security/GRC docs for supported controls, limitations, troubleshooting, and release readiness.

Compatibility note: assessment state schema is now `1.3.0`. Consumers of `controls[]` should expect `evidence_quality`, `manual_evidence_needed`, and `reviewer_disposition`.
