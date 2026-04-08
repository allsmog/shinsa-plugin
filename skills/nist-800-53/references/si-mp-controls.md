# SI — System and Information Integrity + MP — Media Protection

These controls govern input validation, error handling, flaw remediation, monitoring, and secure data disposal.

## SI-2 — Flaw Remediation

**Requirement**: Identify, report, and correct system flaws; install security-relevant software and firmware updates within the defined time period; and incorporate flaw remediation into the organizational configuration management process.
**Assessment Mode**: hybrid
**What to check in code**:
- Dependency management (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml)
- Known vulnerability scanning (npm audit, pip-audit, govulncheck, cargo-audit)
- Automated dependency updates (Dependabot, Renovate, Snyk)
- Lock file presence and maintenance (package-lock.json, poetry.lock, go.sum)
- CI/CD integration for vulnerability scanning
- Outdated dependency detection
**Pass criteria**: Lock files present, automated dependency updates configured, CI checks for vulnerabilities
**Common findings**: No lock file, no automated dependency updates, known vulnerabilities in dependencies, no CI vulnerability scanning

## SI-3 — Malicious Code Protection

**Requirement**: Implement malicious code protection mechanisms at system entry and exit points to detect and eradicate malicious code.
**Assessment Mode**: auto
**What to check in code**:
- File upload validation (file type checking, magic byte validation)
- File size limits on uploads
- Virus/malware scanning integration (ClamAV, VirusTotal API)
- Content-Type validation
- Executable file blocking
- Archive/zip bomb protection
- User input sanitization (XSS, injection prevention)
**Pass criteria**: File uploads validated for type and size, input sanitized
**Common findings**: No file type validation, missing file size limits, no malware scanning on uploads, user input passed unsanitized

## SI-4 — System Monitoring

**Requirement**: Monitor the system to detect attacks and indicators of potential attacks, unauthorized local, network, and remote connections, and identify unauthorized use.
**Assessment Mode**: hybrid
**What to check in code**:
- Health check endpoints (/health, /healthz, /ready, /livez)
- Metrics collection (Prometheus, Datadog, StatsD, OpenTelemetry)
- APM integration (distributed tracing)
- Error rate monitoring and alerting
- Anomaly detection or threshold-based alerting
- Uptime monitoring configuration
- Security-specific monitoring (auth failure spikes, unusual access patterns)
**Pass criteria**: Health checks exist, metrics collected, alerting configured
**Common findings**: No health check endpoints, no metrics collection, no alerting, no APM

## SI-10 — Information Input Validation

**Requirement**: Check the validity of information inputs to the system.
**Assessment Mode**: auto
**What to check in code**:
- Input validation on all user-facing endpoints
- Schema validation (Zod, Joi, Yup, class-validator, Pydantic, JSON Schema)
- Parameterized queries (no SQL string concatenation)
- Output encoding (HTML entity encoding, URL encoding)
- Command injection prevention (no shell exec with user input)
- Path traversal prevention (no user-controlled file paths)
- Type checking and coercion safety
- Request body size limits
**Pass criteria**: Input validated and sanitized on all user-facing endpoints, parameterized queries used
**Common findings**: Missing input validation, SQL string concatenation, user input in shell commands, path traversal possible, no request size limits

## SI-11 — Error Handling

**Requirement**: Generate error messages that provide information necessary for corrective actions without revealing information that could be exploited.
**Assessment Mode**: auto
**What to check in code**:
- Global error handler that sanitizes responses
- No stack traces in production error responses
- No internal system details in error messages (database names, file paths, internal IPs)
- Generic error messages for clients (HTTP 500 without details)
- Detailed errors logged server-side only
- Different error handling for development vs production
- Custom error pages (not framework defaults)
**Pass criteria**: Error responses sanitized in production, detailed errors server-side only
**Common findings**: Stack traces in production responses, database error messages exposed to clients, framework default error pages revealing technology stack

## SI-12 — Information Management and Retention

**Requirement**: Manage and retain information within the system and information output from the system in accordance with applicable laws, executive orders, directives, regulations, policies, standards, guidelines, and operational requirements.
**Assessment Mode**: hybrid
**What to check in code**:
- Data retention policies implemented (TTL, scheduled cleanup)
- Soft delete vs hard delete mechanisms
- Data archival mechanisms
- GDPR right-to-erasure implementation
- Data lifecycle management
- Automated data purge after retention period
**Pass criteria**: Retention policies defined and enforced, deletion mechanisms exist
**Common findings**: No data retention policies, soft delete only (data never truly removed), no scheduled cleanup, no GDPR erasure endpoint

## SI-16 — Memory Protection

**Requirement**: Implement controls to protect the system memory from unauthorized code execution.
**Assessment Mode**: hybrid
**What to check in code**:
- Runtime or build-time memory-execution protections when exposed by configuration or build artifacts (for example DEP/NX, ASLR, hardened sandboxing)
- No use of dynamic code execution functions with untrusted input
- Template injection prevention (no user-controlled template strings in server-side rendering)
- Deserialization safety (use safe loaders and avoid executing untrusted serialized objects)
- No dynamic code loading from untrusted sources
- CSP only as supplementary evidence for browser-delivered code
**Pass criteria**: Runtime or build artifacts expose memory-execution protections, or the application shows strong compensating controls against unsafe code execution; mark code-only evidence as partial proxy coverage
**Common findings**: No visible runtime hardening signals, dynamic string execution with user-controlled input, unsafe deserialization of untrusted data

---

## MP-6 — Media Sanitization

**Requirement**: Sanitize system media prior to disposal, release, or reuse using defined sanitization techniques and procedures.
**Assessment Mode**: hybrid
**What to check in code**:
- Purge, wipe, or decommission hooks for storage or removable media in code or IaC
- Temp file cleanup and secure disposal workflows
- Database record purging (not just flag-based soft delete)
- Storage volume cleanup or encrypted-media retirement in IaC or automation
- Application-level secure delete helpers only as proxy evidence
**Pass criteria**: Repo artifacts show sanitization support for storage or media lifecycle events; absent platform or operational evidence, keep confidence low
**Common findings**: Only soft delete is visible, temp files with sensitive data are not cleaned up, no storage sanitization or decommission workflow is evident
