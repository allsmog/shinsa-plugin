---
name: session-init
description: Initialize compliance assessment session and check for previous state
event: SessionStart
---

# Compliance Assessment Session Initialization

On session start, check for existing assessment state and provide context.

## State Detection

Check for existing assessment state:

```bash
ls shinsa-output/shinsa-state.json shinsa-output/compliance-report.md 2>/dev/null || true
```

### If state file exists:

Read `shinsa-output/shinsa-state.json` and display. Check the `standard` field to determine which standard was assessed:

**If standard is "iso27001":**
```
**Shinsa Compliance Assessment Resumed**

Previous assessment detected:
- **Target**: [From state file]
- **Standard**: ISO 27001:2022 Annex A
- **Agents Completed**: [List of completed agents]
- **Controls Assessed**: [count]
- **Compliance**: [percentage]%
- **Findings**: [total] ([critical] critical, [high] high, [medium] medium, [low] low)
- **Last Updated**: [timestamp]

**Quick Actions:**
- `/shinsa:compliance-scan --resume` - Continue ISO 27001 assessment
- `/shinsa:quick-check A.8.5` - Check a specific ISO control
- `/shinsa:nist-scan` - Start a NIST 800-53 assessment
- Type "reset assessment" to start fresh

**Top Findings:**
[List top 3 findings by severity]
```

**If standard is "nist-800-53":**
```
**Shinsa Compliance Assessment Resumed**

Previous assessment detected:
- **Target**: [From state file]
- **Standard**: NIST SP 800-53 Rev 5
- **Domains Completed**: [List of completed domains]
- **Controls Assessed**: [count]
- **Compliance**: [percentage]%
- **Findings**: [total] ([critical] critical, [high] high, [medium] medium, [low] low)
- **Last Updated**: [timestamp]

**Quick Actions:**
- `/shinsa:nist-scan --resume` - Continue NIST 800-53 assessment
- `/shinsa:nist-quick-check AC-3` - Check a specific NIST control
- `/shinsa:compliance-scan` - Start an ISO 27001 assessment
- Type "reset assessment" to start fresh

**Top Findings:**
[List top 3 findings by severity]
```

### If no state file exists:

Check codebase size:

```bash
find . -type f \( -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.java" -o -name "*.go" -o -name "*.php" -o -name "*.rb" -o -name "*.rs" -o -name "*.cs" \) -not -path "*/node_modules/*" -not -path "*/vendor/*" -not -path "*/dist/*" 2>/dev/null | wc -l
```

Display welcome:

```
**Shinsa Compliance Plugin Ready**

Compliance assessment with evidence-backed findings tied to specific files and line numbers.

**Available Standards:**
- **ISO 27001:2022** — Annex A technological controls (13 controls, 4 domains)
- **NIST SP 800-53 Rev 5** — Federal security controls (53 controls, 6 domains)

**Available Commands:**
- `/shinsa:compliance-scan` - Full ISO 27001 assessment
- `/shinsa:quick-check <control>` - Fast ISO control check (e.g., A.8.5)
- `/shinsa:nist-scan` - Full NIST 800-53 assessment
- `/shinsa:nist-quick-check <control>` - Fast NIST control check (e.g., AC-3)

**Quick Start Examples:**
- `/shinsa:compliance-scan` - Full ISO 27001 assessment
- `/shinsa:nist-scan` - Full NIST 800-53 assessment
- `/shinsa:quick-check A.8.5` - Check ISO secure authentication
- `/shinsa:nist-quick-check AC-3` - Check NIST access enforcement
- `/shinsa:nist-quick-check AU` - Check all NIST audit controls
```
