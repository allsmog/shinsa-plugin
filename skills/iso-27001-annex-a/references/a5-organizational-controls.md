# A.5 — Organizational Controls (37 Controls)

Most organizational controls require manual evidence (policies, procedures, contracts). However, several can be partially assessed from code.

## Partially Code-Assessable Controls

### A.5.14 — Information Transfer
**Requirement**: Information transfer rules, procedures, or agreements shall exist for all types of transfer facilities within the organization and between the organization and other parties.
**Assessment Mode**: hybrid
**What to check in code**:
- HTTPS enforcement (redirect HTTP to HTTPS, HSTS)
- Webhook signature verification (HMAC validation on incoming webhooks)
- API authentication on data exchange endpoints
- Secure file transfer (SFTP, encrypted channels)
- Email security configuration (SPF, DKIM, DMARC if infra code exists)
**Pass criteria**: Data transfers encrypted, webhooks verified, APIs authenticated

### A.5.17 — Authentication Information (linked to A.8.5)
**Assessment Mode**: hybrid
**What to check in code**:
- Password policy enforcement (minimum length, complexity)
- Password history (prevent reuse)
- Initial password/token generation (temporary, forced change)
**Pass criteria**: Password policy enforced in code

### A.5.23 — Information Security for Use of Cloud Services
**Assessment Mode**: hybrid
**What to check in code**:
- Cloud provider SDK/configuration
- IAM roles and policies (if IaC exists)
- Encryption configuration for cloud storage
- Network security groups / firewall rules
- Cloud audit logging enabled
**Pass criteria**: Cloud resources configured with security best practices

### A.5.34 — Privacy and Protection of PII
**Assessment Mode**: hybrid
**What to check in code**:
- PII identification and classification
- Consent management implementation
- Data subject request handling (GDPR DSARs)
- PII minimization patterns
- Cross-border transfer safeguards
**Pass criteria**: PII handling documented and implemented

## Manual-Only Controls (Not Code-Assessable)

The following controls require policy documents, management records, or operational evidence:

| Control | Name | Evidence Type |
|---------|------|---------------|
| A.5.1 | Policies for information security | Policy documents |
| A.5.2 | Information security roles | Org chart, job descriptions |
| A.5.3 | Segregation of duties | Role matrix |
| A.5.4 | Management responsibilities | Management commitment records |
| A.5.5 | Contact with authorities | Contact list |
| A.5.6 | Contact with special interest groups | Membership records |
| A.5.7 | Threat intelligence | Threat intel feeds, procedures |
| A.5.8 | Information security in project management | Project templates |
| A.5.9 | Inventory of assets | Asset register |
| A.5.10 | Acceptable use | AUP document |
| A.5.11 | Return of assets | Offboarding checklist |
| A.5.12 | Classification of information | Classification scheme |
| A.5.13 | Labelling of information | Labelling procedures |
| A.5.15 | Access control | Access control policy |
| A.5.16 | Identity management | Identity procedures |
| A.5.18 | Access rights | Access provisioning records |
| A.5.19 | Supplier relationships | Supplier assessments |
| A.5.20 | Supplier agreements | Contracts |
| A.5.21 | ICT supply chain | Supply chain procedures |
| A.5.22 | Supplier service monitoring | Review records |
| A.5.24 | Incident management planning | Incident response plan |
| A.5.25 | Assessment of security events | Event classification procedures |
| A.5.26 | Response to incidents | Incident response procedures |
| A.5.27 | Learning from incidents | Post-incident reviews |
| A.5.28 | Collection of evidence | Evidence handling procedures |
| A.5.29 | Information security during disruption | BCP/DRP documents |
| A.5.30 | ICT readiness for business continuity | ICT continuity plan |
| A.5.31 | Legal requirements | Legal register |
| A.5.32 | Intellectual property rights | IP procedures |
| A.5.33 | Protection of records | Records management policy |
| A.5.35 | Independent review | Audit reports |
| A.5.36 | Compliance with policies | Compliance monitoring records |
| A.5.37 | Documented operating procedures | SOPs |

**Note**: When these controls are encountered during assessment, mark them as `not_applicable` with the note: "This control requires manual evidence (policies, procedures, records) that cannot be assessed from source code alone."
