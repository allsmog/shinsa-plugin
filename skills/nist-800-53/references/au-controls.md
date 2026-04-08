# AU — Audit and Accountability

These controls govern event logging, audit record content, storage, analysis, and protection.

## AU-2 — Event Logging

**Requirement**: Identify the types of events that the system is capable of logging in support of the audit function, and coordinate the event logging function with other organizational entities.
**Assessment Mode**: auto
**What to check in code**:
- Security event types logged:
  - Authentication events (login, logout, failed login)
  - Authorization events (access granted, access denied, privilege changes)
  - Data modification events (create, update, delete on sensitive resources)
  - System events (startup, shutdown, configuration changes)
  - Administrative actions (user management, role changes)
  - Error and exception events
- Logging coverage across application layers (routes, middleware, services)
- Logging at system boundaries (API endpoints, external integrations)
**Pass criteria**: Authentication, authorization, and data modification events all logged
**Common findings**: Only error logging exists, no auth event logging, missing data modification audit trail

## AU-3 — Content of Audit Records

**Requirement**: Ensure that audit records contain information that establishes what type of event occurred, when it occurred, where it occurred, the source of the event, the outcome, and the identity of individuals or subjects associated with the event.
**Assessment Mode**: auto
**What to check in code**:
- Log entries include: who (user ID/session), what (action/event type), when (timestamp), where (source IP/component), outcome (success/failure)
- Structured logging format (JSON preferred)
- Correlation IDs or request IDs for tracing
- Consistent log schema across components
**Pass criteria**: Structured logging with who/what/when/where/outcome fields
**Common findings**: Unstructured text logging, missing user identity in logs, no correlation IDs, inconsistent log format

## AU-4 — Audit Log Storage Capacity

**Requirement**: Allocate audit log storage capacity and configure auditing to reduce the likelihood of such capacity being exceeded.
**Assessment Mode**: hybrid
**What to check in code**:
- Log rotation configuration
- Log file size limits
- Log retention policies
- External log shipping (to aggregator like ELK, Datadog, CloudWatch)
- Disk space monitoring for log volumes
**Pass criteria**: Log rotation configured, external shipping or retention policy exists
**Common findings**: No log rotation, logs written to local disk with no size limit, no external log shipping

## AU-5 — Response to Audit Logging Process Failures

**Requirement**: Alert personnel or roles in the event of an audit logging process failure and take defined additional actions.
**Assessment Mode**: hybrid
**What to check in code**:
- Error handling for logging failures (try/catch around log writes)
- Fallback logging mechanism (stderr, secondary transport)
- Alerting on logging failures
- Graceful degradation when logging is unavailable
- Application behavior when audit log is full or unavailable
**Pass criteria**: Logging failures are caught and handled, fallback exists
**Common findings**: Logging failures silently swallowed, no fallback logging, application crashes on log write failure

## AU-6 — Audit Record Review, Analysis, and Reporting

**Requirement**: Review and analyze system audit records for indications of inappropriate or unusual activity, and report findings.
**Assessment Mode**: hybrid
**What to check in code**:
- Log aggregation configuration (ELK, Splunk, Datadog, CloudWatch Logs)
- Search and filter capabilities on logs
- Alerting rules based on log patterns (failed auth spikes, error rate thresholds)
- Dashboard or monitoring integration
- Anomaly detection on audit data
**Pass criteria**: Logs shipped to aggregation platform, alerting on suspicious patterns configured
**Common findings**: Logs only on local disk, no alerting on auth failures, no log analysis capability

## AU-7 — Audit Record Reduction and Report Generation

**Requirement**: Provide and implement an audit record reduction and report generation capability that supports on-demand audit review, analysis, and reporting requirements.
**Assessment Mode**: hybrid
**What to check in code**:
- Log query/search API or interface
- Log filtering by severity, user, time range, event type
- Report generation from log data
- Log export capabilities
- Structured log format enabling automated analysis
**Pass criteria**: Structured logs that can be queried and filtered
**Common findings**: Unstructured logs that cannot be machine-parsed, no query capability

## AU-8 — Time Stamps

**Requirement**: Use internal system clocks to generate time stamps for audit records, and record time stamps that can be mapped to UTC.
**Assessment Mode**: auto
**What to check in code**:
- UTC usage for all log timestamps
- ISO 8601 format in log output
- Consistent timezone handling across services
- NTP configuration (if infrastructure code exists)
- Log timestamp precision (milliseconds or better)
- No use of local timezone in audit records
**Pass criteria**: UTC timestamps in ISO 8601 format across all logs
**Common findings**: Local timezone used, inconsistent timestamp formats, missing timezone in log entries

## AU-9 — Protection of Audit Information

**Requirement**: Protect audit information and audit logging tools from unauthorized access, modification, and deletion.
**Assessment Mode**: hybrid
**What to check in code**:
- Log file permissions (not world-readable)
- Append-only log configuration
- Log integrity verification (checksums, signing)
- Separate log storage from application data
- Access control on log management endpoints
- Immutable log shipping to external system
**Pass criteria**: Logs written with restricted permissions, shipped to external immutable storage
**Common findings**: Log files world-readable, logs modifiable by application user, no integrity protection

## AU-11 — Audit Record Retention

**Requirement**: Retain audit records for a defined period to provide support for after-the-fact investigations of incidents and meet regulatory and organizational information retention requirements.
**Assessment Mode**: hybrid
**What to check in code**:
- Log retention policy configuration
- Log archival mechanisms
- TTL or lifecycle policies on log storage
- Retention period settings (typically 90 days to 1 year)
- Automated log cleanup after retention period
**Pass criteria**: Retention policy defined and enforced
**Common findings**: No retention policy, logs retained indefinitely or deleted too quickly, no archival

## AU-12 — Audit Record Generation

**Requirement**: Provide audit record generation capability for the event types the system is capable of auditing, allow designated personnel to select which events require auditing, and generate audit records for selected events.
**Assessment Mode**: auto
**What to check in code**:
- Configurable log levels (DEBUG, INFO, WARN, ERROR)
- Per-component or per-module log level configuration
- Runtime log level adjustment capability
- Event type filtering in logging configuration
- Log generation at all application layers (not just one layer)
**Pass criteria**: Configurable logging with adjustable levels and event type selection
**Common findings**: Hardcoded log levels, only one log level across entire application, no runtime adjustment capability
