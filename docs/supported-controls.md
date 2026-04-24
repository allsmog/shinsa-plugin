# Supported Controls

Shinsa assesses code-level and repository-level evidence. It does not replace policy, process, or auditor judgment.

## Evidence Modes

| Mode | Meaning | GRC Treatment |
|------|---------|---------------|
| Automated | Repository evidence can directly support the control outcome | Review evidence anchors and remediation guidance |
| Hybrid | Repository evidence supports only part of the control | Attach manual evidence before audit use |
| Manual | Repository evidence is insufficient | Use Shinsa notes only as scoping context |

## ISO 27001 Annex A

| Control | Mode | Notes |
|---------|------|-------|
| A.8.2 Privileged access rights | Hybrid | Code can show RBAC and privileged routes; access review records remain manual |
| A.8.3 Information access restriction | Automated/Hybrid | Route, middleware, object authorization, and API scopes are assessable |
| A.8.5 Secure authentication | Automated/Hybrid | Password hashing, sessions, throttling, MFA hooks, and cookie/JWT settings are assessable |
| A.8.10 Information deletion | Hybrid | Deletion code is assessable; retention approvals and disposal records remain manual |
| A.8.11 Data masking | Automated/Hybrid | Response masking and log redaction are assessable |
| A.8.12 Data leakage prevention | Automated/Hybrid | Validation, output encoding, error handling, CORS, and headers are assessable |
| A.8.15 Logging | Hybrid | Event logging code is assessable; retention and SIEM operations remain manual |
| A.8.16 Monitoring activities | Hybrid | Health checks, metrics, and alert config are assessable; operational response evidence remains manual |
| A.8.17 Clock synchronization | Hybrid | UTC and timestamp handling are assessable; NTP operations remain manual |
| A.8.21 Security of network services | Hybrid | TLS, HSTS, and certificate validation are assessable when config is present |
| A.8.24 Use of cryptography | Automated/Hybrid | Algorithms, key handling patterns, and crypto misuse are assessable |
| A.8.34 Audit testing protection | Hybrid | Test isolation and non-destructive patterns are assessable |
| A.5.14 Information transfer | Hybrid | HTTPS, webhook signatures, transfer filtering, and related code are assessable |

## NIST SP 800-53 Rev 5

| Family | Mode | Notes |
|--------|------|-------|
| AC + IA | Automated/Hybrid | Auth, authorization, account lifecycle, sessions, MFA hooks, and least privilege patterns |
| AU | Hybrid | Audit events, timestamps, log schema, and log protection patterns |
| SC | Automated/Hybrid | TLS, crypto, sessions, transport protection, certificates, and data-at-rest controls |
| SI + MP | Automated/Hybrid | Input validation, error handling, monitoring, malicious-code protections, retention, sanitization |
| CM + RA | Hybrid | Docker, IaC, dependency scanning, CI checks, configuration settings, least functionality |
| SA | Hybrid | SDLC evidence, tests, code review metadata, dependency process hints, toolchain controls |

Manual-only NIST families and organizational ISO controls should be documented in the evidence pack as `manual evidence needed`, not scored as fully implemented from code.
