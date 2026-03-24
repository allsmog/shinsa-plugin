---
name: quick-check
description: Fast compliance check of a specific ISO 27001 control or control family against the codebase
argument-hint: "<control-id|family> [path] [--verbose]"
allowed-tools:
  - Glob
  - Grep
  - Read
  - TodoWrite
---

# Quick Check

Fast, focused compliance check against a single ISO 27001 control or control family.

## Usage

```
/shinsa:quick-check A.8.5              # Check secure authentication
/shinsa:quick-check A.8.24             # Check cryptography
/shinsa:quick-check A.8                # Check all technological controls
/shinsa:quick-check A.8.15 src/        # Check logging in specific path
/shinsa:quick-check A.8.5 --verbose    # Detailed output with all evidence
```

## Flags

| Flag | Effect |
|------|--------|
| `--verbose` | Show all evidence including passing checks, not just findings |

## Step 1: Parse the control target

Determine what to check:
- **Single control** (e.g., `A.8.5`): Look up the control definition from the iso-27001-annex-a skill
- **Control family** (e.g., `A.8`): Look up all controls in that family

If the control ID is not recognized, suggest the closest match.

## Step 2: Quick scope

Identify the target path (default: current directory). Do a fast language detection:

```bash
ls package.json pyproject.toml go.mod Cargo.toml pom.xml 2>/dev/null | head -1
```

## Step 3: Targeted assessment

For the specific control(s), perform a focused search:

### A.8.5 — Secure Authentication
Search for auth implementations and check:
- Password hashing algorithm (bcrypt/scrypt/Argon2 = pass, MD5/SHA1 = fail)
- MFA implementation
- Session management (token expiry, secure flags)
- Rate limiting on login endpoints
- Account lockout mechanisms

### A.8.24 — Use of Cryptography
Search for crypto usage and check:
- Algorithm choices (AES-256 = pass, DES/RC4 = fail)
- Key management (hardcoded keys = critical finding)
- TLS configuration (TLS 1.2+ required)
- Encryption mode (GCM/CTR = pass, ECB = fail)
- IV/nonce generation (crypto.randomBytes = pass, Math.random = fail)

### A.8.15 — Logging
Search for logging configuration and check:
- Structured logging (JSON format preferred)
- Security event coverage (auth, access control, errors)
- Sensitive data exclusion (passwords, tokens not in logs)
- Log level configuration
- Timestamp format (ISO 8601 with timezone)

### A.8.2 — Privileged Access Rights
Search for authorization and check:
- RBAC or permission system
- Privilege separation (admin vs user roles)
- Principle of least privilege
- Privilege escalation protections

### A.8.3 — Information Access Restriction
Search for access control and check:
- Route/endpoint protection
- Authorization middleware
- Resource-level access checks
- API key/token scoping

### A.8.10 — Information Deletion
Search for data lifecycle and check:
- Soft delete vs hard delete
- Data retention policies
- Secure deletion (overwrite)
- Cascading deletes

### A.8.11 — Data Masking
Search for data display and check:
- PII masking in logs
- Masked fields in API responses
- Redacted data in error messages
- Display truncation of sensitive fields

### A.8.12 — Data Leakage Prevention
Search for data exposure and check:
- Input validation
- Output encoding
- Error message sanitization
- Stack trace suppression in production
- Sensitive headers (X-Powered-By removed)

### A.8.16 — Monitoring Activities
Search for monitoring and check:
- Health check endpoints
- Metrics collection (Prometheus, Datadog, etc.)
- Alerting configuration
- APM integration

### A.8.17 — Clock Synchronization
Search for timestamp handling and check:
- UTC usage
- ISO 8601 format
- NTP configuration (if infrastructure code exists)

### A.8.21 — Security of Network Services
Search for network configuration and check:
- TLS/SSL setup
- Certificate validation
- CORS configuration
- Helmet/security headers

### A.5.14 — Information Transfer
Search for data transfer and check:
- API encryption (HTTPS)
- Webhook signature verification
- File transfer security
- Email security (if applicable)

### A.8.34 — Protection of Information Systems During Audit Testing
Search for test/audit patterns and check:
- Read-only audit endpoints
- Test data isolation
- Audit logging configuration

## Step 4: Report

Present a concise assessment:

```
## Quick Check: A.8.5 — Secure Authentication

**Status**: partially_implemented
**Maturity**: 3/5 (Defined)
**Confidence**: 0.8

### Findings

**[HIGH] Weak password hashing**
- `src/auth/password.ts:23` — Uses SHA-256 instead of bcrypt/Argon2
- Recommendation: Migrate to Argon2id with appropriate parameters

**[MEDIUM] Missing rate limiting on login**
- `src/routes/auth.ts:45` — Login endpoint has no rate limiting
- Recommendation: Add rate limiting (e.g., 5 attempts per 15 minutes)

### Passing Checks
- Session tokens use secure random generation
- HTTP-only and Secure cookie flags are set
- Token expiry is configured (24h access, 7d refresh)

### Overall: 2 findings (1 high, 1 medium)
```

If `--verbose` is set, include all passing checks with evidence. Otherwise, only show findings and a brief summary of what's passing.
