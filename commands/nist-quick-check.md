---
name: nist-quick-check
description: Fast compliance check of a specific NIST SP 800-53 Rev 5 control or control family against the codebase
argument-hint: "<control-id|family> [path] [--verbose]"
allowed-tools:
  - Glob
  - Grep
  - Read
  - TodoWrite
---

# NIST Quick Check

Fast, focused compliance check against a single NIST SP 800-53 Rev 5 control or control family.

## Usage

```
/shinsa:nist-quick-check AC-3              # Check access enforcement
/shinsa:nist-quick-check IA-5              # Check authenticator management
/shinsa:nist-quick-check AC                # Check all Access Control family controls
/shinsa:nist-quick-check SC-13 src/        # Check crypto in specific path
/shinsa:nist-quick-check AU-2 --verbose    # Detailed output with all evidence
```

## Flags

| Flag | Effect |
|------|--------|
| `--verbose` | Show all evidence including passing checks, not just findings |

## Step 1: Parse the control target

Determine what to check:
- **Single control** (e.g., `AC-3`): Look up the control definition from the nist-800-53 skill
- **Control family** (e.g., `AC`): Look up all code-assessable controls in that family

If the control ID is not recognized, suggest the closest match.

**Valid control families**: AC, AU, CM, IA, MP, RA, SA, SC, SI

## Step 2: Quick scope

Identify the target path (default: current directory). Do a fast language detection by checking for package manifests:

Use Glob to check for: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `composer.json`, `Gemfile`. The first match determines the primary language.

## Step 3: Targeted assessment

For the specific control(s), perform a focused search:

### AC-2 — Account Management
Search for user management and check:
- Account creation with role assignment
- Account deactivation/disabling logic
- Inactive account detection
- Automated provisioning/deprovisioning

### AC-3 — Access Enforcement
Search for authorization and check:
- Authorization middleware on routes/endpoints
- RBAC enforcement
- Resource-level access checks (not just route-level)
- Deny-by-default patterns

### AC-5 — Separation of Duties
Search for role separation and check:
- Distinct role definitions
- Dual-authorization for sensitive operations
- Maker-checker patterns

### AC-6 — Least Privilege
Search for privilege patterns and check:
- Granular permission definitions
- Scoped API keys/tokens
- Privilege escalation protections
- Default role has minimal permissions

### AC-7 — Unsuccessful Logon Attempts
Search for auth failure handling and check:
- Failed login attempt tracking
- Account lockout mechanism
- Rate limiting on auth endpoints
- Progressive delay

### AC-8 — System Use Notification
Search for login flow and check:
- System use banner or warning notice before access
- Explicit acknowledgment before further access
- Monitoring, authorized-use, or privacy/security notice content

### AC-11 — Device Lock
Search for session configuration and check:
- Session timeout or lock configuration for interactive clients
- Idle session detection
- Re-authentication or lock-screen pattern after inactivity

### AC-12 — Session Termination
Search for logout and check:
- Explicit logout functionality
- Token invalidation on logout
- Maximum session duration enforcement
- Session cleanup on server side

### AC-14 — Permitted Actions Without Identification or Authentication
Search for unauthenticated routes and check:
- Intentional public endpoints vs accidentally unprotected routes
- Auth middleware bypass patterns
- Rate limiting on unauthenticated endpoints

### AC-17 — Remote Access
Search for remote access config and check:
- Documented remote access configuration or connection requirements in repo/IaC
- VPN/secure tunnel configuration
- SSH or admin-access restrictions
- IP allowlisting or equivalent network restrictions for admin access

### IA-2 — Identification and Authentication (Organizational Users)
Search for auth mechanisms and check:
- User authentication (password, SSO, OAuth, SAML)
- MFA/2FA implementation
- Unique user identification
- Replay-resistant authentication

### IA-4 — Identifier Management
Search for identity management and check:
- Unique user ID generation
- Username uniqueness enforcement
- Identifier lifecycle management
- Prevention of identifier reuse

### IA-5 — Authenticator Management
Search for credential handling and check:
- Password hashing (bcrypt/Argon2/scrypt = pass, MD5/SHA1 = fail)
- Password complexity requirements
- Password history enforcement
- Credential storage (no plaintext)
- Token generation entropy

### IA-6 — Authentication Feedback
Search for login error handling and check:
- Generic error messages on auth failure
- No account existence disclosure
- Masked password input

### IA-8 — Identification and Authentication (Non-organizational Users)
Search for external auth and check:
- External user/API client authentication
- OAuth/OIDC for third-party integration
- API key management for external consumers

### IA-11 — Re-authentication
Search for sensitive operations and check:
- Step-up authentication for sensitive ops
- Re-auth before privilege escalation
- Fresh token requirement for high-risk actions

### AU-2 — Event Logging
Search for logging and check:
- Security event types logged (auth, access, data changes)
- Logging coverage across application layers
- Event type configuration

### AU-3 — Content of Audit Records
Search for log format and check:
- Structured logging (JSON format)
- Log fields: who, what, when, where, outcome
- Correlation IDs

### AU-4 — Audit Log Storage Capacity
Search for log configuration and check:
- Log rotation configuration
- Log file size limits
- External log shipping

### AU-5 — Response to Audit Logging Process Failures
Search for log error handling and check:
- Error handling for logging failures
- Fallback logging mechanism
- Alerting on logging failures

### AU-6 — Audit Record Review, Analysis, and Reporting
Search for log analysis and check:
- Log aggregation configuration
- Alerting rules on log patterns
- Dashboard integration

### AU-7 — Audit Record Reduction and Report Generation
Search for log querying and check:
- Log query/search capability
- Log filtering by severity, user, time
- Structured log format enabling analysis

### AU-8 — Time Stamps
Search for timestamp handling and check:
- UTC usage for all timestamps
- ISO 8601 format
- Consistent timezone handling
- NTP configuration (if IaC exists)

### AU-9 — Protection of Audit Information
Search for log security and check:
- Log file permissions
- Append-only configuration
- Log integrity verification
- Immutable external log shipping

### AU-11 — Audit Record Retention
Search for retention config and check:
- Log retention policy configuration
- TTL or lifecycle policies
- Automated cleanup after retention period

### AU-12 — Audit Record Generation
Search for log generation and check:
- Configurable log levels
- Per-component log level configuration
- Runtime log level adjustment
- Log generation at all application layers

### SC-4 — Information in Shared System Resources
Search for shared resource usage and check:
- Shared cache or session isolation between users/tenants
- Temp file and shared storage cleanup
- Sensitive data not retained in global/shared state
- Memory clearing or equivalent runtime-isolation signals where exposed

### SC-7 — Boundary Protection
Search for boundary controls and check:
- Security headers (CSP, X-Frame-Options)
- CORS configuration
- Rate limiting on external endpoints
- Input validation at boundaries

### SC-8 — Transmission Confidentiality and Integrity
Search for network security and check:
- TLS configuration (TLS 1.2+ required)
- HTTPS enforcement, HSTS
- Certificate validation enabled
- Internal service encryption

### SC-12 — Cryptographic Key Establishment and Management
Search for key management and check:
- Key generation using CSPRNG
- Key storage (env vars or vault, not hardcoded)
- Key rotation mechanisms
- Separate keys for different purposes

### SC-13 — Cryptographic Protection
Search for crypto usage and check:
- Algorithm choices (AES-256 = pass, DES/RC4 = fail)
- Encryption modes (GCM/CTR = pass, ECB = fail)
- IV/nonce generation (CSPRNG required)
- No deprecated algorithms

### SC-17 — Public Key Infrastructure Certificates
Search for certificate config and check:
- TLS certificate configuration
- Auto-renewal (Let's Encrypt, cert-manager)
- Certificate chain validation

### SC-23 — Session Authenticity
Search for session security and check:
- CSRF protection
- Session ID regeneration after authentication
- Cookie security flags (HttpOnly, Secure, SameSite)
- Session fixation prevention

### SC-28 — Protection of Information at Rest
Search for data-at-rest encryption and check:
- Database encryption configuration
- Encrypted storage in IaC
- Sensitive data not in plaintext files

### SI-2 — Flaw Remediation
Search for dependency management and check:
- Lock files present
- Automated dependency updates (Dependabot, Renovate)
- Vulnerability scanning in CI

### SI-3 — Malicious Code Protection
Search for upload handling and check:
- File type validation
- File size limits
- Content-Type validation

### SI-4 — System Monitoring
Search for monitoring and check:
- Health check endpoints
- Metrics collection
- Alerting configuration

### SI-10 — Information Input Validation
Search for validation and check:
- Schema validation on endpoints
- Parameterized queries
- Output encoding
- Command injection prevention

### SI-11 — Error Handling
Search for error handling and check:
- Global error handler
- No stack traces in production
- Generic error messages for clients

### SI-12 — Information Management and Retention
Search for data lifecycle and check:
- Data retention policies
- Deletion mechanisms
- Automated cleanup

### SI-16 — Memory Protection
Search for dynamic execution and check:
- Runtime or build-time memory-execution protections when exposed (for example DEP/NX, ASLR, hardened sandboxing)
- No dynamic code execution with user input
- Safe deserialization practices
- CSP only as supplementary evidence for browser-delivered code

### MP-6 — Media Sanitization
Search for deletion and check:
- Purge, wipe, or decommission hooks for storage or temp media
- Secure temp file cleanup
- Storage lifecycle cleanup in IaC or automation
- Application-level delete helpers only as proxy evidence

### CM-2 — Baseline Configuration
Search for IaC and check:
- Infrastructure-as-code present
- Configuration version-controlled
- Environment separation

### CM-3 — Configuration Change Control
Search for CI/CD and check:
- CI/CD pipeline present
- Automated testing before deploy
- Branch protection or review requirements

### CM-5 — Access Restrictions for Change
Search for deployment access and check:
- Branch protection configuration
- Deployment credentials management
- Separate credentials per environment

### CM-6 — Configuration Settings
Search for config and check:
- Debug mode disabled in production
- Secure framework defaults
- Security headers configured

### CM-7 — Least Functionality
Search for minimization and check:
- Minimal base images
- No unnecessary dependencies in production
- Minimal port exposure

### CM-8 — System Component Inventory
Search for manifests and check:
- Package manifest files present
- Lock files for reproducible builds
- SBOM generation capability

### RA-5 — Vulnerability Monitoring and Scanning
Search for scanning tools and check:
- SAST in CI/CD
- Dependency scanning
- Container image scanning
- Security findings as CI gate

### SA-3 — System Development Life Cycle
Search for development process and check:
- Defined development workflow
- Code review requirements
- Testing infrastructure

### SA-4 — Acquisition Process
Search for dependency evaluation and check:
- Acquisition or supplier requirements captured in repo policy/config artifacts
- Dependency source verification (checksums, pinned registries, approved sources)
- License checking
- Approved/denied dependency or vendor lists

### SA-11 — Developer Testing and Evaluation
Search for tests and check:
- Test directory structure
- Security-specific tests
- Test coverage configuration
- CI integration for tests

### SA-15 — Development Process, Standards, and Tools
Search for tooling and check:
- Linter configuration
- Code formatter configuration
- Pre-commit hooks
- Coding standards documentation

## Step 4: Report

Present a concise assessment:

```
## Quick Check: AC-3 — Access Enforcement

**Status**: partially_implemented
**Maturity**: 3/5 (Defined)
**Confidence**: 0.8

### Findings

**[HIGH] Missing authorization on admin API endpoints**
- `src/routes/admin.ts:23` — Admin endpoints lack authorization middleware
- Recommendation: Add role-based authorization middleware to all admin routes

**[MEDIUM] No object-level authorization**
- `src/routes/users.ts:45` — User profile endpoint accepts any user ID without ownership check
- Recommendation: Add object-level authorization check (req.user.id === params.id)

### Passing Checks
- Route-level authorization middleware exists on main API routes
- RBAC roles defined with distinct permission sets
- API key scoping implemented for service accounts

### Overall: 2 findings (1 high, 1 medium)
```

If `--verbose` is set, include all passing checks with evidence. Otherwise, only show findings and a brief summary of what's passing.
