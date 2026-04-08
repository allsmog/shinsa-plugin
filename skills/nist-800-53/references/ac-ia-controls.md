# AC — Access Control + IA — Identification and Authentication

These controls govern who can access what, and how users prove their identity.

## AC-2 — Account Management

**Requirement**: Manage system accounts including defining account types, establishing conditions for group and role membership, specifying authorized users, and requiring approvals for account creation.
**Assessment Mode**: hybrid
**What to check in code**:
- User account creation with role assignment
- Account deactivation/disabling logic
- Account type definitions (admin, user, service, guest)
- Automated account provisioning/deprovisioning
- Account review or expiry mechanisms
- Inactive account detection and handling
**Pass criteria**: Account lifecycle managed in code with role assignment, deactivation exists
**Common findings**: No account deactivation logic, missing role assignment on creation, no inactive account handling

## AC-3 — Access Enforcement

**Requirement**: Enforce approved authorizations for logical access to information and system resources in accordance with applicable access control policies.
**Assessment Mode**: auto
**What to check in code**:
- Authorization middleware on all routes/endpoints
- Role-based access control (RBAC) enforcement
- Attribute-based access control (ABAC) patterns
- Resource-level access checks (not just route-level)
- Object-level authorization (IDOR prevention)
- Deny-by-default access patterns
**Pass criteria**: All data-accessing endpoints have authorization enforcement
**Common findings**: Missing auth on internal APIs, IDOR via direct object references, allow-by-default patterns

## AC-5 — Separation of Duties

**Requirement**: Separate duties of individuals to reduce the risk of malevolent activity without collusion.
**Assessment Mode**: hybrid
**What to check in code**:
- Role separation (admin cannot also be approver)
- Dual-authorization for sensitive operations
- Maker-checker patterns in workflows
- Distinct role definitions with non-overlapping privileges
- Segregation of development and production access
**Pass criteria**: Distinct roles defined, sensitive ops require multiple parties
**Common findings**: Single superadmin role with all permissions, no dual-authorization on sensitive ops

## AC-6 — Least Privilege

**Requirement**: Employ the principle of least privilege, allowing only authorized accesses for users which are necessary to accomplish assigned tasks.
**Assessment Mode**: auto
**What to check in code**:
- Granular permission definitions (not just admin/user)
- Scoped API keys/tokens (read vs write, per-resource)
- Privilege escalation protections
- Default role has minimal permissions
- Service accounts with limited scope
- Temporary privilege elevation with expiry
**Pass criteria**: Granular permissions enforced, default role is least-privilege
**Common findings**: Overly permissive default roles, all-or-nothing admin access, unscoped API keys

## AC-7 — Unsuccessful Logon Attempts

**Requirement**: Enforce a limit of consecutive invalid logon attempts by a user during a time period, and automatically lock the account or delay next logon when the maximum is exceeded.
**Assessment Mode**: auto
**What to check in code**:
- Failed login attempt tracking
- Account lockout after N failures
- Progressive delay on failures
- Lockout duration and reset mechanism
- Rate limiting on authentication endpoints
- IP-based or account-based throttling
**Pass criteria**: Failed attempt tracking with lockout or rate limiting
**Common findings**: No failed attempt tracking, no rate limiting on auth endpoints, no account lockout

## AC-8 — System Use Notification

**Requirement**: Display a system use notification message before granting access and require acknowledgment before further access.
**Assessment Mode**: hybrid
**What to check in code**:
- Login page or system banner shown before access
- Explicit acknowledgment before further access
- Monitoring, authorized-use, or privacy/security notice content
- Public-system notice content where applicable
**Pass criteria**: Login flow presents a system use banner and requires acknowledgment before access
**Common findings**: No pre-access banner, no explicit acknowledgment, missing monitoring or authorized-use notice

## AC-11 — Device Lock

**Requirement**: Prevent further access to the system by initiating a device or session lock after inactivity until access is re-established.
**Assessment Mode**: hybrid
**What to check in code**:
- Session timeout or lock configuration for interactive clients
- Idle session detection
- Session lock requiring re-authentication
- Configurable inactivity timeout values
- Frontend idle detection (for web apps)
**Pass criteria**: Interactive clients enforce inactivity lock or equivalent re-authentication pattern; mark low confidence if only server-side timeout evidence is visible
**Common findings**: No inactivity lock, excessively long timeout (>30 min), no re-authentication after idle period

## AC-12 — Session Termination

**Requirement**: Automatically terminate a user session after defined conditions.
**Assessment Mode**: auto
**What to check in code**:
- Explicit logout functionality
- Token invalidation on logout
- Session cleanup on server side
- Refresh token revocation
- Maximum session duration enforcement
- Session termination on password change
**Pass criteria**: Logout invalidates tokens/sessions, max session duration enforced
**Common findings**: Logout doesn't invalidate server-side session, tokens remain valid after logout, no max session duration

## AC-14 — Permitted Actions Without Identification or Authentication

**Requirement**: Identify user actions that can be performed without identification or authentication, and document and justify such actions.
**Assessment Mode**: auto
**What to check in code**:
- Unauthenticated endpoints (public routes)
- Auth middleware bypass patterns
- Public API surface documentation
- Health check and status endpoints (acceptable unauthenticated)
- Rate limiting on unauthenticated endpoints
**Pass criteria**: Unauthenticated endpoints are intentional and limited, non-sensitive
**Common findings**: Sensitive endpoints missing authentication, overly broad public API surface

## AC-17 — Remote Access

**Requirement**: Establish usage restrictions, configuration or connection requirements, implementation guidance, and authorization for each type of remote access allowed.
**Assessment Mode**: hybrid
**What to check in code**:
- Documented remote access configuration or connection requirements (if repo or IaC captures them)
- VPN or secure tunnel configuration (if IaC exists)
- Remote API authentication requirements
- SSH key management configuration
- Bastion host or jump server patterns
- IP allowlisting for administrative access
**Pass criteria**: Remote access types are constrained and visible through authentication, configuration, or authorization artifacts
**Common findings**: SSH password auth enabled, no admin access restrictions, missing remote-access configuration guidance in repo artifacts

---

## IA-2 — Identification and Authentication (Organizational Users)

**Requirement**: Uniquely identify and authenticate organizational users, and implement multi-factor authentication.
**Assessment Mode**: auto
**What to check in code**:
- User authentication mechanism (password, SSO, OAuth, SAML)
- Multi-factor authentication (MFA/2FA) implementation
- Unique user identification (no shared accounts in code)
- Authentication for privileged accounts
- Replay-resistant authentication mechanisms
**Pass criteria**: Unique user identification, MFA available for privileged access
**Common findings**: No MFA support, shared service account credentials, no replay protection

## IA-4 — Identifier Management

**Requirement**: Manage system identifiers by receiving authorization to assign identifiers, selecting and assigning individual, group, role, service, or device identifiers, and preventing reuse for a defined period.
**Assessment Mode**: hybrid
**What to check in code**:
- Unique user ID generation (UUID, sequential with gap handling)
- Username uniqueness enforcement
- Account identifier lifecycle (creation, suspension, deletion)
- Service account identifier management
- Prevention of identifier reuse
**Pass criteria**: Unique identifiers enforced, lifecycle managed
**Common findings**: No uniqueness constraint on identifiers, deleted identifiers can be reused immediately

## IA-5 — Authenticator Management

**Requirement**: Manage system authenticators by verifying identity before issuing, establishing initial content, ensuring sufficient strength, and implementing controls for protection and refresh.
**Assessment Mode**: auto
**What to check in code**:
- Password hashing: bcrypt (cost 10+), Argon2id, or scrypt required
- Password complexity requirements (minimum length, character classes)
- Password history (prevent reuse of last N passwords)
- Initial password/token generation (temporary, forced change)
- Credential storage (no plaintext, no reversible encryption)
- API key/token generation (sufficient entropy, CSPRNG)
- Token refresh and rotation mechanisms
**Pass criteria**: Strong password hashing, complexity enforced, no plaintext storage
**Common findings**: SHA-256 for passwords, no complexity requirements, missing password history, hardcoded credentials

## IA-6 — Authentication Feedback

**Requirement**: Obscure feedback of authentication information during the authentication process.
**Assessment Mode**: auto
**What to check in code**:
- Generic error messages on login failure ("invalid credentials" not "invalid password" or "user not found")
- Password fields use masked input (frontend)
- No authentication details in error responses
- Rate limit messages don't reveal account existence
**Pass criteria**: Authentication errors are generic, do not reveal account existence
**Common findings**: Different error messages for invalid username vs invalid password, timing differences that reveal account existence

## IA-8 — Identification and Authentication (Non-organizational Users)

**Requirement**: Uniquely identify and authenticate non-organizational users or processes acting on behalf of non-organizational users.
**Assessment Mode**: hybrid
**What to check in code**:
- External user/API client authentication
- OAuth/OIDC for third-party integration
- API key management for external consumers
- Guest/anonymous access controls
- Third-party identity provider integration
**Pass criteria**: External users authenticated via standard mechanisms
**Common findings**: No authentication for external API consumers, shared API keys for multiple external parties

## IA-11 — Re-authentication

**Requirement**: Require users to re-authenticate when defined circumstances or situations require re-authentication.
**Assessment Mode**: auto
**What to check in code**:
- Step-up authentication for sensitive operations (password change, payment, admin actions)
- Re-authentication before privilege escalation
- Session re-validation on critical operations
- Fresh token requirement for high-risk actions
**Pass criteria**: Sensitive operations require re-authentication
**Common findings**: No re-authentication for password changes, privilege escalation without re-auth, payment without step-up auth
