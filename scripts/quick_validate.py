#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_COMMANDS = [
    "compliance-scan",
    "quick-check",
    "nist-scan",
    "nist-quick-check",
    "control-plan",
    "control-implement",
]

REQUIRED_AGENTS = [
    "auth-assessor",
    "crypto-assessor",
    "data-protection-assessor",
    "logging-assessor",
    "nist-access-control-assessor",
    "nist-audit-assessor",
    "nist-sc-assessor",
    "nist-si-assessor",
    "nist-cm-assessor",
    "nist-sa-assessor",
    "evidence-completeness-reviewer",
    "control-interpretation-reviewer",
    "coverage-reviewer",
]

DOCS = ["README.md", "AGENTS.md", "CLAUDE.md"]


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def collect_errors(root: Path = ROOT) -> list[str]:
    errors: list[str] = []

    for command in REQUIRED_COMMANDS:
        path = root / "commands" / f"{command}.md"
        if not path.exists():
            errors.append(f"Missing command file: {path}")

    for agent in REQUIRED_AGENTS:
        path = root / "agents" / f"{agent}.md"
        if not path.exists():
            errors.append(f"Missing agent file: {path}")

    schema_path = root / "references" / "assessment.schema.json"
    try:
        schema = load_json(schema_path)
    except Exception as exc:
        errors.append(f"Unable to parse assessment schema: {exc}")
        schema = {}

    if isinstance(schema, dict):
        schema_version = schema.get("properties", {}).get("schema_version", {}).get("const")
        if schema_version != "1.4.0":
            errors.append("Assessment schema version must be 1.4.0")

        required = set(schema.get("required", []))
        for field in ("run", "review", "artifacts"):
            if field not in required:
                errors.append(f"Assessment schema missing required field: {field}")

        properties = schema.get("properties", {})
        run_props = properties.get("run", {}).get("properties", {})
        review_props = properties.get("review", {}).get("properties", {})
        artifact_props = properties.get("artifacts", {}).get("properties", {})

        for field in ("id", "standard", "phase", "round"):
            if field not in run_props:
                errors.append(f"Assessment schema missing run.{field}")

        if "rounds" not in review_props:
            errors.append("Assessment schema missing review.rounds")

        for field in ("plan_path", "domain_results", "review_paths", "report_path"):
            if field not in artifact_props:
                errors.append(f"Assessment schema missing artifacts.{field}")

        controls_items = properties.get("controls", {}).get("items", {})
        finding_items = (
            controls_items.get("properties", {})
            .get("findings", {})
            .get("items", {})
        )
        finding_required = set(finding_items.get("required", []))
        if "evidence" not in finding_required:
            errors.append("Assessment schema findings must require evidence")

        evidence_schema = finding_items.get("properties", {}).get("evidence", {})
        if evidence_schema.get("minItems", 0) < 1:
            errors.append("Assessment schema findings.evidence must require at least one item")

        evidence_items = evidence_schema.get("items", {})
        evidence_required = set(evidence_items.get("required", []))
        for field in ("file_path", "start_line", "assessment"):
            if field not in evidence_required:
                errors.append(f"Assessment schema evidence missing required field: {field}")

        evidence_props = evidence_items.get("properties", {})
        if evidence_props.get("file_path", {}).get("minLength", 0) < 1:
            errors.append("Assessment schema evidence.file_path must be non-empty")
        if evidence_props.get("start_line", {}).get("minimum", 0) < 1:
            errors.append("Assessment schema evidence.start_line must be at least 1")
        if evidence_props.get("assessment", {}).get("minLength", 0) < 1:
            errors.append("Assessment schema evidence.assessment must be non-empty")

        control_required = set(controls_items.get("required", []))
        for field in (
            "evidence_quality",
            "manual_evidence_needed",
            "manual_evidence_items",
            "reviewer_disposition",
            "confidence_rationale",
            "evidence_quality_rationale",
            "grc_action",
        ):
            if field not in control_required:
                errors.append(f"Assessment schema controls must require {field}")

        control_props = controls_items.get("properties", {})
        evidence_quality_values = set(control_props.get("evidence_quality", {}).get("enum", []))
        for value in ("strong", "partial", "inferred", "missing"):
            if value not in evidence_quality_values:
                errors.append(f"Assessment schema evidence_quality missing enum value: {value}")

        reviewer_values = set(control_props.get("reviewer_disposition", {}).get("enum", []))
        for value in ("approved", "changes_requested", "unresolved", "not_reviewed"):
            if value not in reviewer_values:
                errors.append(f"Assessment schema reviewer_disposition missing enum value: {value}")

        grc_action_values = set(control_props.get("grc_action", {}).get("enum", []))
        for value in ("accept", "reject", "request_evidence", "create_remediation_ticket"):
            if value not in grc_action_values:
                errors.append(f"Assessment schema grc_action missing enum value: {value}")

        if control_props.get("manual_evidence_items", {}).get("type") != "array":
            errors.append("Assessment schema manual_evidence_items must be an array")

    required_docs = [
        root / "docs" / "supported-controls.md",
        root / "docs" / "limitations-and-false-positives.md",
        root / "docs" / "troubleshooting.md",
        root / "docs" / "release-checklist.md",
    ]
    for path in required_docs:
        if not path.exists():
            errors.append(f"Missing enterprise product doc: {path}")

    contract_text = (root / "references" / "orchestration-contract.md").read_text(encoding="utf-8")
    for phrase in (
        "Evidence Pack",
        "Evidence Quality",
        "Human Sign-Off",
        "manual_evidence_items",
        "confidence_rationale",
        "evidence_quality_rationale",
        "grc_action",
    ):
        if phrase not in contract_text:
            errors.append(f"orchestration contract missing enterprise section phrase: {phrase}")

    for doc_name in DOCS:
        doc_path = root / doc_name
        text = doc_path.read_text(encoding="utf-8")
        for command in REQUIRED_COMMANDS:
            if f"/shinsa:{command}" not in text:
                errors.append(f"{doc_name} does not mention /shinsa:{command}")
        for reviewer in (
            "evidence-completeness-reviewer",
            "control-interpretation-reviewer",
            "coverage-reviewer",
        ):
            if reviewer not in text:
                errors.append(f"{doc_name} does not mention {reviewer}")

    hook_text = (root / "hooks" / "session-start.md").read_text(encoding="utf-8")
    if "shinsa-output/runs/" not in hook_text:
        errors.append("hooks/session-start.md does not mention run directories")

    return errors


def main() -> int:
    errors = collect_errors()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Shinsa quick validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
