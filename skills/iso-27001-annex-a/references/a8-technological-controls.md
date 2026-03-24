# A.8 — Technological Controls (34 Controls)

These are the primary controls assessable from source code.

## Core Controls (Fully Code-Assessable)

### A.8.2 — Privileged Access Rights
**Requirement**: The allocation and use of privileged access rights shall be restricted and managed.
**Assessment Mode**: auto
**What to check in code**:
- RBAC or permission system implementation
- Admin/superuser role definitions and separation
- Middleware enforcing role checks on privileged endpoints
- Privilege escalation protections
- Least privilege patterns (scoped permissions)
**Pass criteria**: Roles defined, middleware enforces access, admin endpoints protected
**Common findings**: Missing role checks on admin routes, overly permissive default roles

### A.8.3 — Information Access Restriction
**Requirement**: Access to information and other associated assets shall be restricted in accordance with the established topic-specific policy on access control.
**Assessment Mode**: auto
**What to check in code**:
- Authorization middleware on routes/endpoints
- Resource-level access checks (not just route-level)
- Object-level authorization (IDOR prevention)
- Field-level access control
- API scoping (read vs write permissions)
**Pass criteria**: All data-accessing endpoints have authorization checks
**Common findings**: Missing auth on internal APIs, IDOR via direct object references

### A.8.5 — Secure Authentication
**Requirement**: Secure authentication technologies and procedures shall be established and implemented based on information access restrictions and the topic-specific policy on access control.
**Assessment Mode**: auto
**What to check in code**:
- Password hashing: bcrypt (cost 10+), Argon2id, or scrypt required
- Session tokens: cryptographically random, sufficient length (32+ bytes)
- JWT: algorithm validation (RS256/ES256 preferred), expiry enforced, secret strength
- Cookie security: HttpOnly, Secure, SameSite flags
- Rate limiting on auth endpoints
- Account lockout after failed attempts
- MFA support
**Pass criteria**: Strong password hashing, secure session management, rate limiting
**Common findings**: SHA-256 for passwords, missing rate limiting, JWT with HS256 and weak secret

### A.8.9 — Configuration Management
**Requirement**: Configurations, including security configurations, of hardware, software, services and networks shall be established, documented, maintained and regularly reviewed.
**Assessment Mode**: hybrid
**What to check in code**:
- Infrastructure-as-code (Terraform, CloudFormation, Pulumi)
- Docker/container configuration
- Environment-specific configs (dev vs staging vs prod)
- Security-relevant defaults
- Config validation on startup
**Pass criteria**: IaC exists, security configs documented, environment separation

### A.8.10 — Information Deletion
**Requirement**: Information stored in information systems, devices or in any other storage media shall be deleted when no longer required.
**Assessment Mode**: auto
**What to check in code**:
- Data deletion endpoints (user account deletion, data purge)
- Soft delete vs hard delete implementation
- Data retention TTL mechanisms (database TTL, scheduled jobs)
- Cascading deletes for related records
- GDPR right-to-erasure implementation
**Pass criteria**: Deletion mechanisms exist, retention policies implemented
**Common findings**: Soft delete only (data persists), no scheduled cleanup, missing cascade

### A.8.11 — Data Masking
**Requirement**: Data masking shall be used in accordance with the organization's topic-specific policy on access control and other related topic-specific policies, and business requirements, taking applicable legislation into consideration.
**Assessment Mode**: auto
**What to check in code**:
- PII masking in API responses (emails, phone numbers, SSN)
- Masking in log output
- Redaction in error messages
- Data masking in non-production environments
- Partial display patterns (last 4 digits, masked email)
**Pass criteria**: Sensitive fields masked in responses and logs
**Common findings**: Full email in API responses, PII in log messages

### A.8.12 — Data Leakage Prevention
**Requirement**: Data leakage prevention measures shall be applied to systems, networks and any other devices that process, store or transmit sensitive information.
**Assessment Mode**: auto
**What to check in code**:
- Input validation (injection prevention)
- Output encoding (XSS prevention)
- Error sanitization (no stack traces in production)
- Security headers (CSP, X-Frame-Options, X-Content-Type-Options)
- CORS configuration (not wildcard in production)
- Sensitive data in URL parameters
- Server information disclosure (X-Powered-By, Server headers)
**Pass criteria**: Input validated, output encoded, errors sanitized, headers configured
**Common findings**: Missing CSP, stack traces in production, wildcard CORS

### A.8.15 — Logging
**Requirement**: Logs that record activities, exceptions, faults and other relevant events shall be produced, stored, protected and analysed.
**Assessment Mode**: auto
**What to check in code**:
- Structured logging (JSON format)
- Security event logging (auth events, access changes, errors)
- Log content: who (user ID), what (action), when (timestamp), where (source), result (success/failure)
- Sensitive data exclusion from logs
- Log injection prevention (user input sanitized)
- Log level configuration (not DEBUG in production)
**Pass criteria**: Structured logging configured, security events logged, PII excluded
**Common findings**: Unstructured logging, missing auth event logging, PII in logs

### A.8.16 — Monitoring Activities
**Requirement**: Networks, systems and applications shall be monitored for anomalous behaviour and appropriate actions taken to evaluate potential information security incidents.
**Assessment Mode**: hybrid
**What to check in code**:
- Health check endpoints (/health, /healthz, /ready)
- Metrics collection (Prometheus, Datadog, OpenTelemetry)
- Alerting configuration
- APM integration (distributed tracing)
- Error rate monitoring
**Pass criteria**: Health checks exist, metrics collected, alerting configured
**Common findings**: No health checks, no metrics, no alerting

### A.8.17 — Clock Synchronization
**Requirement**: The clocks of information processing systems used by the organization shall be synchronized to approved time sources.
**Assessment Mode**: auto
**What to check in code**:
- UTC usage for all timestamps
- ISO 8601 format
- Consistent timezone handling
- NTP configuration (if IaC exists)
**Pass criteria**: UTC used consistently, ISO 8601 format
**Common findings**: Local timezone used, inconsistent timestamp formats

### A.8.21 — Security of Network Services
**Requirement**: Security mechanisms, service levels and service requirements of network services shall be identified, implemented and monitored.
**Assessment Mode**: hybrid
**What to check in code**:
- TLS/SSL configuration (TLS 1.2+ required)
- Certificate validation enabled
- HSTS header
- Secure cipher suites (forward secrecy)
- Internal service communication security
**Pass criteria**: TLS 1.2+, certificate validation, HSTS configured
**Common findings**: TLS 1.0/1.1 accepted, certificate validation disabled

### A.8.24 — Use of Cryptography
**Requirement**: Rules for the effective use of cryptography, including cryptographic key management, shall be defined and implemented.
**Assessment Mode**: auto
**What to check in code**:
- Algorithm strength (AES-256, RSA-2048+, SHA-256+)
- Key management (no hardcoded keys, env vars or vault)
- Encryption modes (GCM, CTR preferred; ECB = finding)
- IV/nonce generation (CSPRNG required)
- Key rotation mechanisms
- Deprecated algorithm usage (MD5, DES, RC4)
**Pass criteria**: Strong algorithms, proper key management, authenticated encryption
**Common findings**: Hardcoded keys, weak algorithms, ECB mode

### A.8.25 — Secure Development Life Cycle
**Requirement**: Rules for the secure development of software and systems shall be established and applied.
**Assessment Mode**: hybrid
**What to check in code**:
- CI/CD pipeline configuration
- Security scanning in pipeline (SAST, dependency scanning)
- Code review requirements (branch protection)
- Test coverage for security-relevant code
- Dependency update automation (Dependabot, Renovate)
**Pass criteria**: CI/CD exists with security checks, branch protection enabled

### A.8.28 — Secure Coding
**Requirement**: Secure coding principles shall be applied to software development.
**Assessment Mode**: auto
**What to check in code**:
- Input validation on all user-facing endpoints
- Parameterized queries (no string concatenation in SQL)
- Output encoding
- Error handling (no information leakage)
- Secure defaults
- Dependency management (no known vulnerabilities)
**Pass criteria**: Input validated, queries parameterized, errors handled safely

### A.8.31 — Separation of Development, Test and Production Environments
**Requirement**: Development, testing and production environments shall be separated and secured.
**Assessment Mode**: hybrid
**What to check in code**:
- Environment-specific configuration (NODE_ENV, RAILS_ENV, etc.)
- Different database connections per environment
- Feature flags or environment guards
- Docker Compose vs production deployment differences
- CI/CD environment separation
**Pass criteria**: Environment configs exist, separation enforced

### A.8.34 — Protection of Information Systems During Audit Testing
**Requirement**: Audit tests and other assurance activities involving assessment of operational systems shall be planned and agreed between the tester and appropriate management.
**Assessment Mode**: hybrid
**What to check in code**:
- Read-only audit/reporting endpoints
- Non-destructive query patterns
- Audit-specific logging
- Test data isolation
**Pass criteria**: Audit endpoints are read-only, logging covers audit activities

## Conditional Controls (Depends on Infrastructure)

### A.8.7 — Protection Against Malware
Relevant if: File upload handling exists
Check: File type validation, virus scanning integration, upload size limits

### A.8.13 — Information Backup
Relevant if: Database or persistent storage exists
Check: Backup configuration in IaC, backup schedule, restoration testing

### A.8.20 — Networks Security
Relevant if: Network configuration in IaC
Check: Network segmentation, firewall rules, VPC configuration

### A.8.22 — Segregation of Networks
Relevant if: Multi-tier architecture in IaC
Check: Network boundaries, DMZ configuration, internal/external separation

## Controls Not Assessable from Code

The following A.8 controls require manual evidence:
- A.8.1 (User endpoint devices) — policy-level
- A.8.4 (Access to source code) — process-level
- A.8.6 (Capacity management) — infrastructure-level
- A.8.8 (Management of technical vulnerabilities) — process-level
- A.8.14 (Redundancy) — infrastructure-level
- A.8.18 (Privileged utility programs) — operational
- A.8.19 (Installation of software) — operational
- A.8.23 (Web filtering) — network-level
- A.8.26 (Application security requirements) — requirements-level
- A.8.27 (Secure system architecture) — design-level
- A.8.29 (Security testing in dev/acceptance) — process-level
- A.8.30 (Outsourced development) — contract-level
- A.8.32 (Change management) — process-level
- A.8.33 (Test information) — data management
