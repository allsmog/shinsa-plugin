# SC — System and Communications Protection

These controls govern cryptographic protection, transmission security, boundary protection, and session management.

## SC-4 — Information in Shared System Resources

**Requirement**: Prevent unauthorized and unintended information transfer via shared system resources.
**Assessment Mode**: hybrid
**What to check in code**:
- No sensitive data retained in global or shared state
- Database, cache, or session isolation between users or tenants
- Temp file or shared storage cleanup after use
- Memory or buffer clearing signals when exposed by the runtime or language
**Pass criteria**: Shared resources are isolated and there is no evidence of unintended cross-user data exposure; treat application-only evidence as partial proxy coverage
**Common findings**: Sensitive data in shared cache without per-user isolation, temp files with secrets not cleaned up, global state reused across users

## SC-7 — Boundary Protection

**Requirement**: Monitor and control communications at the external managed interfaces to the system and at key internal managed interfaces.
**Assessment Mode**: hybrid
**What to check in code**:
- Security headers (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options)
- CORS configuration (not wildcard in production)
- Firewall rules (if IaC exists)
- Network segmentation (if IaC/Docker/K8s exists)
- API gateway or reverse proxy configuration
- Input validation at system boundaries
- Rate limiting on external-facing endpoints
- Server information disclosure prevention (X-Powered-By removed)
**Pass criteria**: Security headers configured, CORS restricted, input validated at boundaries
**Common findings**: Wildcard CORS, missing CSP, missing X-Frame-Options, no rate limiting, server version disclosed

## SC-8 — Transmission Confidentiality and Integrity

**Requirement**: Protect the confidentiality and integrity of transmitted information.
**Assessment Mode**: hybrid
**What to check in code**:
- TLS/SSL configuration (TLS 1.2 minimum, TLS 1.3 preferred)
- HTTPS enforcement (HTTP to HTTPS redirect)
- HSTS header (Strict-Transport-Security)
- Certificate validation enabled (no `rejectUnauthorized: false`)
- Secure cipher suites (forward secrecy required)
- Internal service-to-service encryption (mTLS, TLS)
- Webhook payload signing for integrity
**Pass criteria**: TLS 1.2+, HTTPS enforced, HSTS configured, certificate validation enabled
**Common findings**: TLS 1.0/1.1 accepted, certificate validation disabled, missing HSTS, HTTP allowed

## SC-12 — Cryptographic Key Establishment and Management

**Requirement**: Establish and manage cryptographic keys when cryptography is employed within the system.
**Assessment Mode**: auto
**What to check in code**:
- Key generation using CSPRNG (crypto.randomBytes, secrets module)
- Key storage (environment variables or vault, NOT hardcoded)
- Key rotation mechanisms or versioning
- Key destruction/cleanup
- Separate keys for different purposes (signing vs encryption)
- Key derivation functions (HKDF, PBKDF2)
- Integration with key management services (AWS KMS, HashiCorp Vault, Azure Key Vault)
**Pass criteria**: Keys from CSPRNG, stored securely (not hardcoded), rotation mechanism exists
**Common findings**: Hardcoded encryption keys, no key rotation, same key for all purposes, Math.random for key generation

## SC-13 — Cryptographic Protection

**Requirement**: Determine the cryptographic uses and implement the types of cryptography required for each use.
**Assessment Mode**: auto
**What to check in code**:
- Algorithm strength:
  - Symmetric: AES-128+ (AES-256 preferred), ChaCha20-Poly1305
  - Asymmetric: RSA-2048+ (4096 preferred), ECDSA P-256+, Ed25519
  - Hashing (integrity): SHA-256, SHA-384, SHA-512, BLAKE2
  - Hashing (passwords): Argon2id, bcrypt, scrypt (NOT SHA-family, NOT MD5)
  - MAC: HMAC-SHA256+, Poly1305
- Encryption modes (GCM, CTR preferred; ECB = critical finding)
- IV/nonce generation (CSPRNG required, never reuse)
- Authenticated encryption usage
- No use of deprecated algorithms (DES, 3DES, RC4, Blowfish, MD5, SHA-1)
**Pass criteria**: Strong algorithms, authenticated encryption, proper IV generation
**Common findings**: DES/RC4 in use, ECB mode, MD5 for integrity, static IV/nonce, unauthenticated encryption

## SC-17 — Public Key Infrastructure Certificates

**Requirement**: Issue public key certificates under an appropriate certificate policy or obtain public key certificates from an approved service provider.
**Assessment Mode**: hybrid
**What to check in code**:
- TLS certificate configuration
- Certificate auto-renewal (Let's Encrypt, cert-manager)
- Certificate chain validation
- Certificate expiry monitoring
- Self-signed certificate usage (acceptable in dev, finding in prod)
- Certificate pinning implementation (where appropriate)
**Pass criteria**: Valid certificates from trusted CA, auto-renewal configured
**Common findings**: Self-signed certificates in production config, no certificate monitoring, expired certificate handling missing

## SC-23 — Session Authenticity

**Requirement**: Protect the authenticity of communications sessions.
**Assessment Mode**: auto
**What to check in code**:
- CSRF protection (tokens, SameSite cookies, double-submit)
- Session ID regeneration after authentication
- Session binding to client attributes (IP, user-agent)
- Secure session token generation (CSPRNG, sufficient length)
- Session fixation prevention
- Cookie security flags (HttpOnly, Secure, SameSite)
**Pass criteria**: CSRF protection active, session tokens secure, cookie flags set
**Common findings**: No CSRF protection, session not regenerated on login, missing SameSite cookie flag, session fixation possible

## SC-28 — Protection of Information at Rest

**Requirement**: Protect the confidentiality and integrity of information at rest.
**Assessment Mode**: hybrid
**What to check in code**:
- Database encryption configuration (transparent data encryption, field-level encryption)
- File encryption for sensitive stored data
- Encryption configuration in IaC (EBS encryption, S3 encryption, RDS encryption)
- Sensitive configuration not stored in plaintext files
- Encrypted storage for credentials/secrets
- Backup encryption
**Pass criteria**: Sensitive data encrypted at rest, encryption configured in storage/IaC
**Common findings**: Database without encryption at rest, secrets in plaintext config files, unencrypted backups, S3 buckets without encryption
