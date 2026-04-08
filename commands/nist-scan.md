---
name: nist-scan
description: Run a full NIST SP 800-53 Rev 5 compliance assessment against the codebase with all 6 assessment domains
argument-hint: "[path] [--controls AC-3,IA-5] [--family AC,AU] [--severity critical,high] [--format json|md] [--output file] [--resume]"
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

# NIST SP 800-53 Rev 5 Compliance Scan

Run a full NIST SP 800-53 Rev 5 compliance assessment with evidence-backed findings.

**Persistence rule**: Write artifacts to disk incrementally. Use the Write tool to save `shinsa-output/shinsa-state.json` after each domain completes (not only at the end). Write `shinsa-output/compliance-report.md` as the final step. This ensures partial runs still produce usable output.

## Flags

| Flag | Effect |
|------|--------|
| `--controls` | Assess specific controls only (comma-separated IDs, e.g., `AC-3,IA-5`) |
| `--family` | Assess specific control families (comma-separated, e.g., `AC,AU,SC`) |
| `--severity` | Only report findings at or above severity (e.g., `--severity high`) |
| `--format` | Output format: `json` or `md` (default: both) |
| `--output` | Save report to a specific file path |
| `--resume` | Resume from a previous incomplete assessment |

## Step 1: Check for prior state

Check if a previous assessment exists:

```bash
ls shinsa-output/shinsa-state.json 2>/dev/null || true
```

If `--resume` is passed and state exists with `"standard": "nist-800-53"`, load it and skip completed domains. Otherwise start fresh.

## Step 2: Scope the codebase

Identify the repository structure, languages, and frameworks:

1. **Language detection** — Check file extensions and package manifests:
   ```bash
   ls package.json pyproject.toml requirements.txt go.mod Cargo.toml pom.xml composer.json Gemfile 2>/dev/null || true
   ```

2. **Framework detection** — Identify web frameworks, ORMs, auth libraries:
   - Read the primary package manifest
   - Note frameworks that affect control assessment (e.g., Express implies Node.js auth patterns)

3. **Architecture detection** — Check for infrastructure-as-code, CI/CD, Docker:
   ```bash
   ls Dockerfile docker-compose.yml .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile terraform/*.tf k8s/*.yaml 2>/dev/null || true
   ```

4. **Size check** — Count source files:
   ```bash
   find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
   ```

Record the scope in a brief summary for assessment context.

## Step 3: Determine applicable controls

Based on scope, determine which NIST SP 800-53 Rev 5 controls are assessable from code:

**Always applicable** (code-assessable):
- **AC**: AC-2, AC-3, AC-5, AC-6, AC-7, AC-8, AC-11, AC-12, AC-14, AC-17
- **IA**: IA-2, IA-4, IA-5, IA-6, IA-8, IA-11
- **AU**: AU-2, AU-3, AU-4, AU-5, AU-6, AU-7, AU-8, AU-9, AU-11, AU-12
- **SC**: SC-4, SC-7, SC-8, SC-12, SC-13, SC-17, SC-23, SC-28
- **SI**: SI-2, SI-3, SI-4, SI-10, SI-11, SI-12, SI-16
- **MP**: MP-6

**Conditionally applicable** (based on detected infrastructure):
- **CM**: CM-2, CM-3, CM-5, CM-6, CM-7, CM-8 — if IaC or CI/CD detected
- **RA**: RA-5 — if CI/CD detected
- **SA**: SA-3, SA-4, SA-11, SA-15 — if CI/CD or test infrastructure detected

If `--controls` or `--family` is specified, filter to those only.

## Step 4: Assess controls and persist incrementally

**CRITICAL: Do NOT dispatch subagents for assessment. Perform the assessment INLINE to avoid subagent startup overhead. Assess each control domain in order, and IMMEDIATELY write the updated state file to `shinsa-output/shinsa-state.json` after each domain before proceeding to the next.**

**For each domain, do the assessment yourself (do not use the Agent tool):**

### Domain 1: Access Control + Identification/Authentication (AC + IA)

Assess AC-2, AC-3, AC-5, AC-6, AC-7, AC-8, AC-11, AC-12, AC-14, AC-17, IA-2, IA-4, IA-5, IA-6, IA-8, IA-11.

Search for access control and auth implementations using Grep/Glob, read the relevant files, assess against control requirements. Look for:
- Authorization middleware, RBAC, role definitions, permission enforcement
- Account management (creation, deactivation, provisioning)
- Separation of duties, least privilege patterns
- Failed logon handling, account lockout, rate limiting
- Session management (timeout, termination, lock)
- Authentication mechanisms (password hashing, MFA, JWT/session tokens)
- Generic auth error messages (IA-6), re-authentication for sensitive ops (IA-11)

```bash
# Auth middleware and handlers
grep -rniE "(passport|authenticate|login|signIn|sign_in|auth_middleware|requireAuth|isAuthenticated|verify_token|jwt\.verify|bcrypt|argon2|scrypt)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java" --include="*.rb" --include="*.php" --include="*.cs"

# Session management
grep -rniE "(session|cookie|Set-Cookie|express-session|connect-redis|iron-session|timeout|idle|lock)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go"

# RBAC and permissions
grep -rniE "(role|permission|authorize|isAdmin|hasRole|canAccess|guard|policy|ability|casl|casbin|least.?privilege)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Rate limiting and lockout
grep -rniE "(rate.?limit|throttle|lockout|brute.?force|failed.?attempt|max.?attempts)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# MFA
grep -rniE "(mfa|2fa|two.?factor|totp|otp|authenticator|multi.?factor)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"
```

**After assessing, IMMEDIATELY use Write tool to save `shinsa-output/shinsa-state.json` with Domain 1 results.**

### Domain 2: Audit and Accountability (AU)

Assess AU-2, AU-3, AU-4, AU-5, AU-6, AU-7, AU-8, AU-9, AU-11, AU-12.

Search for logging and audit implementations. Look for:
- Security event logging (auth events, access changes, data modifications)
- Audit record content (who, what, when, where, outcome)
- Structured logging (JSON format)
- Log rotation, retention, storage capacity
- Log failure handling and fallback
- Log aggregation and analysis tools (ELK, Datadog, CloudWatch)
- UTC timestamps in ISO 8601 format
- Log protection (permissions, integrity, immutability)
- Configurable log levels

```bash
# Logging libraries
grep -rniE "(winston|pino|bunyan|morgan|log4j|logback|slf4j|slog|zerolog|zap|logrus|logging\.getLogger|structlog|NLog|Serilog)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java" --include="*.cs"

# Security event logging
grep -rniE "(log.*(login|logout|auth|failed|denied|unauthorized|forbidden|access|permission))" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Audit trail
grep -rniE "(audit.?log|audit.?trail|log.*(create|update|delete|modify))" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Timestamp handling
grep -rniE "(new Date|Date\.now|datetime\.utcnow|datetime\.now\(timezone\.utc\)|time\.Now|Instant\.now|UTC|toISOString|isoformat)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Log configuration
grep -rniE "(log.?level|LOG_LEVEL|log.?rotation|log.?retention|max.?size|max.?files)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.yaml" --include="*.yml" --include="*.env"
```

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with Domain 2 results added.**

### Domain 3: System and Communications Protection (SC)

Assess SC-4, SC-7, SC-8, SC-12, SC-13, SC-17, SC-23, SC-28.

Search for crypto, TLS, network protection, and session security. Look for:
- Shared resource isolation, memory clearing after sensitive ops
- Security headers (CSP, X-Frame-Options, CORS), boundary protection
- TLS/SSL configuration (TLS 1.2+), HTTPS enforcement, HSTS
- Key management (generation, storage, rotation — no hardcoded keys)
- Cryptographic algorithm choices (AES, RSA, SHA — not DES, MD5, ECB)
- Certificate management, PKI configuration
- CSRF protection, session authenticity, cookie flags
- Encryption at rest (database, file, IaC config)

```bash
# Crypto imports and algorithms
grep -rniE "(require\(['\"]crypto['\"]|import.*crypto|from crypto|hashlib|ssl|OpenSSL|javax\.crypto)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

grep -rniE "(AES|DES|RC4|Blowfish|RSA|ECDSA|Ed25519|SHA-?1|SHA-?256|SHA-?512|MD5|HMAC|GCM|CBC|ECB|CTR|chacha20)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Keys and secrets
grep -rniE "(secret|private.?key|api.?key|encryption.?key|ENCRYPTION_KEY|SECRET_KEY|JWT_SECRET|signing.?key)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java" --include="*.env" --include="*.env.*"

# TLS and network security
grep -rniE "(tls|ssl|https|cert|certificate|secureProtocol|minVersion|TLSv1|SSLv3|ciphers)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.conf" --include="*.yaml" --include="*.yml"

# Security headers and CSRF
grep -rniE "(helmet|Content-Security-Policy|X-Frame-Options|X-Content-Type-Options|Strict-Transport-Security|cors|csrf|csurf|SameSite)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.conf" --include="*.yaml"
```

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with Domain 3 results added.**

### Domain 4: System and Information Integrity + Media Protection (SI + MP)

Assess SI-2, SI-3, SI-4, SI-10, SI-11, SI-12, SI-16, MP-6.

Search for input validation, error handling, monitoring, and data lifecycle. Look for:
- Dependency management and vulnerability scanning (SI-2)
- File upload validation, malware protection (SI-3)
- Health checks, metrics, alerting, APM (SI-4)
- Input validation, parameterized queries, output encoding (SI-10)
- Error sanitization, no stack traces in production (SI-11)
- Data retention, deletion policies (SI-12)
- No dynamic code execution with user input, safe deserialization (SI-16)
- Secure deletion, media sanitization (MP-6)

```bash
# Input validation
grep -rniE "(validate|sanitize|escape|encode|zod|joi|yup|class-validator|pydantic|validator)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Error handling
grep -rniE "(catch|except|rescue|recover|error.?handler|onError|500|InternalServerError|stack.?trace)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Health and monitoring
grep -rniE "(health|healthz|readyz|livez|prometheus|prom-client|datadog|opentelemetry|otel|metrics|counter|histogram|gauge)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java" --include="*.yaml"

# File upload handling
grep -rniE "(multer|upload|multipart|formidable|busboy|file.?type|mime.?type|content.?type)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Data lifecycle
grep -rniE "(delete|remove|destroy|purge|cleanup|retain|retention|ttl|expire|softDelete|hardDelete|gdpr|erasure)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.java"

# Dependency management
grep -rniE "(dependabot|renovate|snyk|npm.?audit|pip.?audit)" --include="*.yml" --include="*.yaml" --include="*.json" --include="*.toml"
```

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with Domain 4 results added.**

### Domain 5: Configuration Management + Risk Assessment (CM + RA)

Assess CM-2, CM-3, CM-5, CM-6, CM-7, CM-8, RA-5. **Skip this domain if no IaC or CI/CD was detected in Step 2.**

Search for configuration management and vulnerability scanning. Look for:
- IaC baseline configuration (Terraform, Docker, CloudFormation)
- CI/CD pipelines with change control
- Branch protection, deployment access restrictions
- Security-hardened defaults, debug mode disabled in production
- Minimal base images, unnecessary dependencies removed
- Package manifests, lock files, SBOM
- SAST/DAST/dependency scanning in CI

```bash
# IaC and configuration
grep -rniE "(terraform|cloudformation|pulumi|ansible)" --include="*.tf" --include="*.yaml" --include="*.yml" --include="*.json"

# CI/CD
ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile bitbucket-pipelines.yml .circleci/config.yml 2>/dev/null || true

# Docker configuration
grep -rniE "(FROM|EXPOSE|ENV|RUN)" Dockerfile* 2>/dev/null || true

# Debug/production mode
grep -rniE "(NODE_ENV|RAILS_ENV|FLASK_ENV|DEBUG|debug.?mode|production)" --include="*.ts" --include="*.js" --include="*.py" --include="*.go" --include="*.env" --include="*.yaml"

# Security scanning in CI
grep -rniE "(semgrep|codeql|sonarqube|snyk|trivy|docker.?scout|npm.?audit|safety|bandit|gosec)" --include="*.yml" --include="*.yaml"

# Branch protection
cat .github/CODEOWNERS 2>/dev/null || true
```

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with Domain 5 results added.**

### Domain 6: System Acquisition (SA)

Assess SA-3, SA-4, SA-11, SA-15. **Skip this domain if no CI/CD or test infrastructure was detected in Step 2.**

Search for development lifecycle and testing. Look for:
- SDLC process (branching, code review, PR templates)
- Dependency evaluation (license checking, source verification)
- Test infrastructure (test directories, frameworks, coverage)
- Security-specific tests
- Linter and formatter configuration, pre-commit hooks, coding standards

```bash
# Test infrastructure
ls -d test/ tests/ __tests__/ spec/ *_test.go cypress/ e2e/ 2>/dev/null || true

# Test configuration
ls jest.config* pytest.ini setup.cfg vitest.config* .mocharc* karma.conf* 2>/dev/null || true

# Linting and formatting
ls .eslintrc* .pylintrc .golangci.yml .prettierrc* .editorconfig rustfmt.toml 2>/dev/null || true

# Pre-commit hooks
ls .husky/ .pre-commit-config.yaml 2>/dev/null || true
cat .husky/pre-commit 2>/dev/null || true

# PR templates and code review
ls .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE/ CONTRIBUTING.md 2>/dev/null || true

# License checking
grep -rniE "(license-checker|fossa|licensee|license.?compliance)" --include="*.json" --include="*.yml" --include="*.yaml"
```

**After assessing, IMMEDIATELY use Write tool to update `shinsa-output/shinsa-state.json` with Domain 6 results added.**

## Step 5: Final state update

After all domains are assessed, read `shinsa-output/shinsa-state.json` from disk, compute final summary, and write the completed state. The state file should already contain all control assessments from incremental writes — just update `completed_at` and the final summary totals.

**How to write**: Use `mkdir -p shinsa-output && cat > shinsa-output/shinsa-state.json << 'JSONEOF'` via Bash.

## State file schema

`shinsa-output/shinsa-state.json`:

```json
{
  "schema_version": "1.1.0",
  "assessment_id": "<unique-id>",
  "target": "<project-path>",
  "standard": "nist-800-53",
  "started_at": "<ISO-8601>",
  "last_updated": "<ISO-8601>",
  "completed_at": "<ISO-8601 or null>",
  "scope": {
    "languages": ["typescript"],
    "frameworks": ["express"],
    "infrastructure": ["docker", "github-actions"],
    "source_file_count": 150
  },
  "domains_completed": ["ac-ia", "au", "sc", "si-mp", "cm-ra", "sa"],
  "summary": {
    "controls_assessed": 53,
    "implemented": 30,
    "partially_implemented": 12,
    "not_implemented": 8,
    "not_applicable": 3,
    "compliance_percentage": 75,
    "average_maturity": 3.2,
    "findings": {
      "total": 15,
      "critical": 2,
      "high": 5,
      "medium": 4,
      "low": 3,
      "info": 1
    }
  },
  "controls": [
    {
      "control_id": "AC-3",
      "control_family": "AC",
      "title": "Access Enforcement",
      "status": "partially_implemented",
      "maturity": 3,
      "confidence": 0.85,
      "agent": "nist-access-control-assessor",
      "finding_count": 2
    }
  ]
}
```

## Step 6: Generate report (from state file only)

**IMPORTANT: Generate the report by reading `shinsa-output/shinsa-state.json` from disk. Do NOT re-read or re-analyze the codebase.** The state file already contains all control assessments, findings, maturity scores, and evidence. Just format it as markdown.

Write human-readable report to `shinsa-output/compliance-report.md` using `cat > shinsa-output/compliance-report.md << 'REPORTEOF'` via Bash:

```markdown
# NIST SP 800-53 Rev 5 Compliance Assessment

**Target**: <project-path>
**Date**: <ISO-8601>
**Standard**: NIST SP 800-53 Rev 5

## Executive Summary

<2-3 sentences summarizing compliance posture>

## Compliance Overview

| Metric | Value |
|--------|-------|
| Controls Assessed | X |
| Implemented | X (Y%) |
| Partially Implemented | X (Y%) |
| Not Implemented | X (Y%) |
| Average Maturity | X.X / 5 |

## Critical & High Findings

### [FINDING-001] <title>
- **Control**: XX-N — <control name>
- **Family**: <family name>
- **Severity**: critical/high
- **Status**: not_implemented / partially_implemented
- **Evidence**:
  - `<file>:<line>` — <code snippet>
  - <assessment rationale>
- **Gap**: <what's missing>
- **Recommendation**: <how to fix>

## Assessment by Control Family

### Access Control (AC)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| AC-2 | Account Management | implemented | 4/5 | 0 |
| AC-3 | Access Enforcement | partial | 3/5 | 2 |
| ... | ... | ... | ... | ... |

### Identification and Authentication (IA)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| IA-2 | Identification and Authentication | partial | 3/5 | 1 |
| ... | ... | ... | ... | ... |

### Audit and Accountability (AU)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| AU-2 | Event Logging | partial | 2/5 | 3 |
| ... | ... | ... | ... | ... |

### System and Communications Protection (SC)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| SC-13 | Cryptographic Protection | implemented | 4/5 | 0 |
| ... | ... | ... | ... | ... |

### System and Information Integrity (SI) / Media Protection (MP)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| SI-10 | Information Input Validation | partial | 3/5 | 1 |
| ... | ... | ... | ... | ... |

### Configuration Management (CM) / Risk Assessment (RA)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| CM-6 | Configuration Settings | partial | 2/5 | 2 |
| ... | ... | ... | ... | ... |

### System Acquisition (SA)

| Control | Name | Status | Maturity | Findings |
|---------|------|--------|----------|----------|
| SA-11 | Developer Testing | partial | 3/5 | 1 |
| ... | ... | ... | ... | ... |

## Recommendations (Prioritized)

1. <Most critical recommendation>
2. <Next priority>
3. ...

## Cross-Standard Mapping

Where NIST 800-53 controls map to ISO 27001 Annex A, findings apply to both. See the control-mapping skill for details.
```

## Step 7: Emit requested format

### `--format json`
Output the full assessment as structured JSON (all control assessments with findings and evidence).

### `--format md` (default)
Display the compliance report summary in the conversation. Reference `shinsa-output/compliance-report.md` for the full report.

## Notes

- Every finding MUST include file path, line numbers, and code snippet as evidence
- Confidence below 0.5 should be flagged as "low confidence — manual review recommended"
- Controls from non-code-assessable families (PE, PS, PL, PM, AT, MA, PT, SR, CP, IR) are marked `not_applicable` with a note explaining they require manual evidence
- The assessment is advisory — it does not replace a formal NIST 800-53 authorization assessment
- Controls are assessed without regard to impact baseline (Low/Moderate/High) — all code-assessable controls are checked
