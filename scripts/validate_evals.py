#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

import quick_validate

ROOT = Path(__file__).resolve().parents[1]

EVIDENCE_PACK_SECTIONS = [
    "## Assessment Metadata",
    "## Executive Summary",
    "## Control Matrix",
    "## Findings",
    "## Evidence Index",
    "## Reviewer Notes",
    "## Unresolved Risks",
    "## Limitations",
    "## What To Do Next",
    "## Human Sign-Off",
]

EVIDENCE_PACK_METADATA_MARKERS = [
    "Plugin Version:",
    "Target Path:",
    "Target Commit:",
    "Assessment Mode:",
    "Standards:",
    "Scope Exclusions:",
    "Methodology:",
    "Raw Artifact References:",
]

CONTROL_TRUST_FIELDS = [
    "control_id",
    "status",
    "confidence",
    "confidence_rationale",
    "evidence_quality",
    "evidence_quality_rationale",
    "manual_evidence_needed",
    "manual_evidence_items",
    "reviewer_disposition",
    "grc_action",
]

DOMAIN_CONTROL_REQUIRED_FIELDS = [
    "title",
    "maturity",
    "agent",
    *CONTROL_TRUST_FIELDS,
]

CONTROL_MATRIX_REQUIRED_FIELDS = [
    *CONTROL_TRUST_FIELDS,
    "remediation_priority",
    "ticket_ready_action",
]

EVIDENCE_QUALITY_VALUES = {"strong", "partial", "inferred", "missing"}
REVIEWER_DISPOSITION_VALUES = {"approved", "changes_requested", "unresolved", "not_reviewed"}
GRC_ACTION_VALUES = {"accept", "reject", "request_evidence", "create_remediation_ticket"}


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_trigger_cases(data: object, errors: list[str]) -> dict[str, dict[str, object]]:
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        errors.append("trigger_evals.json must contain a top-level 'cases' list")
        return {}

    cases_by_id: dict[str, dict[str, object]] = {}
    for case in data["cases"]:
        if not isinstance(case, dict):
            errors.append("trigger_evals.json cases must be objects")
            continue
        case_id = case.get("id")
        target = case.get("target")
        if not case_id or not isinstance(case_id, str):
            errors.append("trigger_evals.json case missing string id")
            continue
        if not isinstance(case.get("query"), str):
            errors.append(f"trigger eval '{case_id}' missing query")
        if not isinstance(case.get("should_trigger"), bool):
            errors.append(f"trigger eval '{case_id}' missing should_trigger boolean")
        if not isinstance(target, str):
            errors.append(f"trigger eval '{case_id}' missing target")
        cases_by_id[case_id] = case
    return cases_by_id


def validate_eval_cases(data: object, errors: list[str]) -> dict[str, dict[str, object]]:
    if not isinstance(data, dict) or not isinstance(data.get("cases"), list):
        errors.append("evals.json must contain a top-level 'cases' list")
        return {}

    cases_by_id: dict[str, dict[str, object]] = {}
    for case in data["cases"]:
        if not isinstance(case, dict):
            errors.append("evals.json cases must be objects")
            continue
        case_id = case.get("id")
        if not case_id or not isinstance(case_id, str):
            errors.append("evals.json case missing string id")
            continue
        if case.get("command") not in quick_validate.REQUIRED_COMMANDS:
            errors.append(f"eval case '{case_id}' references unknown command '{case.get('command')}'")
        required_artifacts = case.get("required_artifacts")
        if not isinstance(required_artifacts, list) or not required_artifacts:
            errors.append(f"eval case '{case_id}' must define required_artifacts")
        cases_by_id[case_id] = case
    return cases_by_id


def resolve_root(value: object, field: str, case_id: str, errors: list[str]) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        errors.append(f"Benchmark case '{case_id}' missing {field}")
        return None

    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    path = path.resolve()

    if not path.exists():
        errors.append(f"Benchmark case '{case_id}' {field} does not exist: {path}")
        return None
    if not path.is_dir():
        errors.append(f"Benchmark case '{case_id}' {field} is not a directory: {path}")
        return None
    return path


def validate_required_artifacts(
    case_id: str,
    artifact_root: Path,
    required_artifacts: object,
    slug: object,
    errors: list[str],
) -> None:
    if not isinstance(required_artifacts, list):
        errors.append(f"Eval case '{case_id}' required_artifacts must be a list")
        return

    for pattern_value in required_artifacts:
        if not isinstance(pattern_value, str) or not pattern_value.strip():
            errors.append(f"Eval case '{case_id}' has an invalid required artifact pattern")
            continue

        pattern = pattern_value
        if "<slug>" in pattern:
            if not isinstance(slug, str) or not slug.strip():
                errors.append(f"Benchmark case '{case_id}' must define slug for pattern '{pattern_value}'")
                continue
            pattern = pattern.replace("<slug>", slug.strip())

        matches = [path for path in artifact_root.glob(pattern) if path.is_file()]
        if not matches:
            errors.append(
                f"Benchmark case '{case_id}' missing required artifact '{pattern}' under {artifact_root}"
            )
            continue

        for match in matches:
            if match.name == "compliance-report.md" and match.parent.name == "synthesis":
                validate_evidence_pack_sections(case_id, match, errors)
            if match.name == "control-matrix.json" and match.parent.name == "synthesis":
                validate_control_matrix(case_id, match, errors)
            if match.suffix == ".json" and match.parent.name == "domains":
                validate_domain_result(case_id, match, errors)

    validate_evidence_pack_bundle(case_id, artifact_root, errors)


def validate_evidence_pack_sections(case_id: str, report_path: Path, errors: list[str]) -> None:
    text = report_path.read_text(encoding="utf-8")
    missing = [section for section in EVIDENCE_PACK_SECTIONS if section not in text]
    for section in missing:
        errors.append(f"Benchmark case '{case_id}' evidence pack missing section {section}: {report_path}")
    for marker in EVIDENCE_PACK_METADATA_MARKERS:
        if marker not in text:
            errors.append(f"Benchmark case '{case_id}' evidence pack missing metadata marker {marker}: {report_path}")

    raw_refs_index = text.find("Raw Artifact References:")
    if raw_refs_index == -1:
        errors.append(f"Benchmark case '{case_id}' evidence pack missing raw artifact references: {report_path}")
    else:
        raw_refs = text[raw_refs_index : raw_refs_index + 500]
        if ".json" not in raw_refs and ".md" not in raw_refs:
            errors.append(f"Benchmark case '{case_id}' evidence pack raw artifact references are empty: {report_path}")


def section_text(report_text: str, section: str) -> str:
    start = report_text.find(section)
    if start == -1:
        return ""
    next_section = report_text.find("\n## ", start + len(section))
    if next_section == -1:
        return report_text[start:]
    return report_text[start:next_section]


def validate_control_trust_fields(
    case_id: str,
    control: object,
    source: str,
    required_fields: list[str],
    errors: list[str],
) -> None:
    if not isinstance(control, dict):
        errors.append(f"Benchmark case '{case_id}' {source} control must be an object")
        return

    control_id = control.get("control_id", "<missing>")
    for field in required_fields:
        if field not in control:
            errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing {field}")

    status = control.get("status")
    if not isinstance(status, str) or not status.strip():
        errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing valid status")

    confidence = control.get("confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing valid confidence")

    for field in ("confidence_rationale", "evidence_quality_rationale"):
        value = control.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing {field}")

    evidence_quality = control.get("evidence_quality")
    if evidence_quality not in EVIDENCE_QUALITY_VALUES:
        errors.append(
            f"Benchmark case '{case_id}' {source} control {control_id} has invalid evidence_quality: {evidence_quality}"
        )

    manual_needed = control.get("manual_evidence_needed")
    if not isinstance(manual_needed, bool):
        errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing boolean manual_evidence_needed")

    manual_items = control.get("manual_evidence_items")
    if not isinstance(manual_items, list):
        errors.append(f"Benchmark case '{case_id}' {source} control {control_id} missing manual_evidence_items list")
    else:
        for item in manual_items:
            if not isinstance(item, str) or not item.strip():
                errors.append(f"Benchmark case '{case_id}' {source} control {control_id} has invalid manual_evidence_items entry")
        if manual_needed is True and not manual_items:
            errors.append(
                f"Benchmark case '{case_id}' {source} control {control_id} needs manual evidence but manual_evidence_items is empty"
            )

    if manual_needed is True and status == "implemented":
        errors.append(
            f"Benchmark case '{case_id}' {source} control {control_id} cannot be implemented while manual_evidence_needed is true"
        )

    reviewer_disposition = control.get("reviewer_disposition")
    if reviewer_disposition not in REVIEWER_DISPOSITION_VALUES:
        errors.append(
            f"Benchmark case '{case_id}' {source} control {control_id} has invalid reviewer_disposition: {reviewer_disposition}"
        )

    grc_action = control.get("grc_action")
    if grc_action not in GRC_ACTION_VALUES:
        errors.append(f"Benchmark case '{case_id}' {source} control {control_id} has invalid grc_action: {grc_action}")


def extract_control_rows(data: object, path: Path, case_id: str, errors: list[str]) -> list[object]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("controls"), list):
        return data["controls"]
    errors.append(f"Benchmark case '{case_id}' control artifact must be a list or contain controls[]: {path}")
    return []


def validate_control_matrix(case_id: str, matrix_path: Path, errors: list[str]) -> None:
    try:
        data = load_json(matrix_path)
    except Exception as exc:
        errors.append(f"Benchmark case '{case_id}' unable to parse control matrix {matrix_path}: {exc}")
        return
    rows = extract_control_rows(data, matrix_path, case_id, errors)
    if not rows:
        errors.append(f"Benchmark case '{case_id}' control matrix is empty: {matrix_path}")
    for row in rows:
        validate_control_trust_fields(case_id, row, f"control matrix {matrix_path}", CONTROL_MATRIX_REQUIRED_FIELDS, errors)


def validate_domain_result(case_id: str, domain_path: Path, errors: list[str]) -> None:
    try:
        data = load_json(domain_path)
    except Exception as exc:
        errors.append(f"Benchmark case '{case_id}' unable to parse domain result {domain_path}: {exc}")
        return
    if not isinstance(data, dict):
        errors.append(f"Benchmark case '{case_id}' domain result must be an object: {domain_path}")
        return
    controls = data.get("controls")
    if not isinstance(controls, list) or not controls:
        errors.append(f"Benchmark case '{case_id}' domain result missing controls[]: {domain_path}")
        return
    for control in controls:
        validate_control_trust_fields(case_id, control, f"domain result {domain_path}", DOMAIN_CONTROL_REQUIRED_FIELDS, errors)
        if isinstance(control, dict) and control.get("reviewer_disposition") != "not_reviewed":
            errors.append(
                f"Benchmark case '{case_id}' domain result {domain_path} control "
                f"{control.get('control_id', '<missing>')} must use reviewer_disposition not_reviewed"
            )


def unresolved_controls_from_reviews(artifact_root: Path) -> set[str]:
    controls: set[str] = set()
    for review_path in artifact_root.glob("reviews/round-*/*.json"):
        try:
            data = load_json(review_path)
        except Exception:
            continue
        if not isinstance(data, dict) or data.get("status") != "unresolved":
            continue
        affected = data.get("affected_controls")
        if isinstance(affected, list):
            for control_id in affected:
                if isinstance(control_id, str) and control_id.strip():
                    controls.add(control_id.strip())
    return controls


def unresolved_controls_from_matrix(matrix_path: Path) -> set[str]:
    try:
        data = load_json(matrix_path)
    except Exception:
        return set()
    controls: set[str] = set()
    for row in extract_control_rows(data, matrix_path, "bundle", []):
        if isinstance(row, dict) and row.get("reviewer_disposition") == "unresolved":
            control_id = row.get("control_id")
            if isinstance(control_id, str) and control_id.strip():
                controls.add(control_id.strip())
    return controls


def validate_evidence_pack_bundle(case_id: str, artifact_root: Path, errors: list[str]) -> None:
    report_path = artifact_root / "synthesis" / "compliance-report.md"
    matrix_path = artifact_root / "synthesis" / "control-matrix.json"
    if not report_path.is_file() or not matrix_path.is_file():
        return

    report_text = report_path.read_text(encoding="utf-8")
    reviewer_notes = section_text(report_text, "## Reviewer Notes")
    unresolved_risks = section_text(report_text, "## Unresolved Risks")
    control_matrix = section_text(report_text, "## Control Matrix")

    unresolved_controls = unresolved_controls_from_reviews(artifact_root)
    unresolved_controls.update(unresolved_controls_from_matrix(matrix_path))

    for control_id in sorted(unresolved_controls):
        if control_id not in control_matrix or "unresolved" not in control_matrix.lower():
            errors.append(
                f"Benchmark case '{case_id}' unresolved control {control_id} missing from report Control Matrix"
            )
        if control_id not in reviewer_notes or "unresolved" not in reviewer_notes.lower():
            errors.append(
                f"Benchmark case '{case_id}' unresolved control {control_id} missing from report Reviewer Notes"
            )
        if control_id not in unresolved_risks or "unresolved" not in unresolved_risks.lower():
            errors.append(
                f"Benchmark case '{case_id}' unresolved control {control_id} missing from report Unresolved Risks"
            )


def count_lines(path: Path) -> int:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return sum(1 for _ in handle)


def validate_finding_anchor(
    case_id: str,
    finding: dict[str, object],
    source_root: Path,
    errors: list[str],
) -> None:
    file_path = finding.get("file_path")
    if not isinstance(file_path, str) or not file_path:
        errors.append(f"Benchmark case '{case_id}' has finding without file_path")
        return

    relative_path = Path(file_path)
    if relative_path.is_absolute():
        errors.append(f"Benchmark case '{case_id}' finding file_path must be relative: {file_path}")
        return

    source_path = (source_root / relative_path).resolve()
    try:
        source_path.relative_to(source_root)
    except ValueError:
        errors.append(f"Benchmark case '{case_id}' finding escapes source_root: {file_path}")
        return

    start_line = finding.get("start_line")
    if not isinstance(start_line, int) or start_line < 1:
        errors.append(f"Benchmark case '{case_id}' has finding without valid start_line")
        return

    if not source_path.is_file():
        errors.append(f"Benchmark case '{case_id}' finding file does not exist: {source_path}")
        return

    line_count = count_lines(source_path)
    if start_line > line_count:
        errors.append(
            f"Benchmark case '{case_id}' finding start_line {start_line} exceeds "
            f"{source_path} line count {line_count}"
        )


def validate_quality_notes(case_id: str, result: dict[str, object], errors: list[str]) -> None:
    notes = result.get("quality_notes")
    if not isinstance(notes, dict):
        errors.append(f"Benchmark case '{case_id}' missing quality_notes")
        return
    for field in ("false_positive_notes", "false_negative_notes"):
        value = notes.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Benchmark case '{case_id}' missing quality_notes.{field}")


def validate_benchmark(
    data: object,
    trigger_cases: dict[str, dict[str, object]],
    eval_cases: dict[str, dict[str, object]],
    errors: list[str],
) -> None:
    if not isinstance(data, dict):
        errors.append("Benchmark file must be a JSON object")
        return

    reviewer_threshold = data.get("reviewer_min_pass_rate", 0.0)
    if not isinstance(reviewer_threshold, (int, float)):
        errors.append("Benchmark reviewer_min_pass_rate must be numeric")
        reviewer_threshold = 0.0

    trigger_results = data.get("trigger_results")
    if not isinstance(trigger_results, list):
        errors.append("Benchmark missing trigger_results list")
        trigger_results = []

    seen_trigger_ids: set[str] = set()
    for result in trigger_results:
        if not isinstance(result, dict):
            errors.append("Benchmark trigger result must be an object")
            continue
        case_id = result.get("case_id")
        if case_id not in trigger_cases:
            errors.append(f"Benchmark references unknown trigger case '{case_id}'")
            continue
        seen_trigger_ids.add(case_id)
        rate = result.get("observed_trigger_rate")
        if not isinstance(rate, (int, float)) or not 0.0 <= rate <= 1.0:
            errors.append(f"Trigger case '{case_id}' has invalid observed_trigger_rate")
            continue
        should_trigger = bool(trigger_cases[case_id]["should_trigger"])
        if should_trigger and rate <= 0.0:
            errors.append(f"Trigger case '{case_id}' should trigger but observed_trigger_rate is {rate}")
        if not should_trigger and rate > 0.0:
            errors.append(f"Trigger case '{case_id}' should not trigger but observed_trigger_rate is {rate}")

    missing_triggers = set(trigger_cases) - seen_trigger_ids
    for case_id in sorted(missing_triggers):
        errors.append(f"Benchmark missing trigger result for '{case_id}'")

    run_results = data.get("run_results")
    if not isinstance(run_results, list):
        errors.append("Benchmark missing run_results list")
        run_results = []

    seen_eval_ids: set[str] = set()
    for result in run_results:
        if not isinstance(result, dict):
            errors.append("Benchmark run result must be an object")
            continue

        case_id = result.get("case_id")
        if case_id not in eval_cases:
            errors.append(f"Benchmark references unknown eval case '{case_id}'")
            continue
        seen_eval_ids.add(case_id)
        eval_case = eval_cases[case_id]

        if result.get("command") != eval_case["command"]:
            errors.append(f"Benchmark case '{case_id}' used unexpected command '{result.get('command')}'")

        artifact_root = resolve_root(result.get("artifact_root"), "artifact_root", case_id, errors)
        source_root = resolve_root(result.get("source_root"), "source_root", case_id, errors)
        if artifact_root is not None:
            validate_required_artifacts(
                case_id,
                artifact_root,
                eval_case.get("required_artifacts"),
                result.get("slug"),
                errors,
            )

        review_rounds = result.get("review_rounds")
        if not isinstance(review_rounds, list) or not review_rounds:
            errors.append(f"Benchmark case '{case_id}' missing review_rounds")
            continue

        approvals = 0
        for round_result in review_rounds:
            if not isinstance(round_result, dict):
                errors.append(f"Benchmark case '{case_id}' has non-object review round")
                continue
            status = round_result.get("status")
            if status == "approved":
                approvals += 1
        pass_rate = approvals / len(review_rounds)
        minimum = float(eval_cases[case_id].get("minimum_reviewer_pass_rate", reviewer_threshold))
        if pass_rate < minimum:
            errors.append(
                f"Benchmark case '{case_id}' reviewer pass rate {pass_rate:.2f} is below required {minimum:.2f}"
            )

        findings = result.get("findings")
        if not isinstance(findings, list):
            errors.append(f"Benchmark case '{case_id}' missing findings list")
            continue
        expected_findings_total = result.get("expected_findings_total")
        if isinstance(expected_findings_total, int) and len(findings) != expected_findings_total:
            errors.append(
                f"Benchmark case '{case_id}' expected {expected_findings_total} findings "
                f"but benchmark listed {len(findings)}"
            )
        if eval_case.get("kind") == "enterprise_benchmark":
            validate_quality_notes(case_id, result, errors)
        for finding in findings:
            if not isinstance(finding, dict):
                errors.append(f"Benchmark case '{case_id}' has non-object finding")
                continue
            if source_root is not None:
                validate_finding_anchor(case_id, finding, source_root, errors)

    missing_evals = set(eval_cases) - seen_eval_ids
    for case_id in sorted(missing_evals):
        errors.append(f"Benchmark missing run result for '{case_id}'")


def main() -> int:
    errors = quick_validate.collect_errors(ROOT)

    trigger_cases = validate_trigger_cases(load_json(ROOT / "evals" / "trigger_evals.json"), errors)
    eval_cases = validate_eval_cases(load_json(ROOT / "evals" / "evals.json"), errors)

    benchmark_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "evals" / "benchmark.sample.json"
    if not benchmark_path.is_absolute():
        benchmark_path = (ROOT / benchmark_path).resolve()

    try:
        benchmark_data = load_json(benchmark_path)
    except Exception as exc:
        errors.append(f"Unable to parse benchmark file '{benchmark_path}': {exc}")
        benchmark_data = {}

    validate_benchmark(benchmark_data, trigger_cases, eval_cases, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"Shinsa eval validation passed for {benchmark_path}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
