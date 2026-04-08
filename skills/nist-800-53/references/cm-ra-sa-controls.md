# CM — Configuration Management + RA — Risk Assessment + SA — System and Services Acquisition

These controls govern system configuration, vulnerability management, and secure development lifecycle.

---

## CM-2 — Baseline Configuration

**Requirement**: Develop, document, and maintain a current baseline configuration of the system under configuration control.
**Assessment Mode**: hybrid
**What to check in code**:
- Infrastructure-as-code (Terraform, CloudFormation, Pulumi, Ansible)
- Docker/container base image configuration (Dockerfile)
- Environment-specific configuration files (dev, staging, production)
- Configuration version control (all config in git)
- Documented configuration defaults
- Environment variable schema/validation
**Pass criteria**: Infrastructure defined as code, configuration version-controlled, environment separation exists
**Common findings**: No IaC, manual server configuration, configuration not in version control, no environment separation

## CM-3 — Configuration Change Control

**Requirement**: Determine types of changes to the system that are configuration-controlled; review proposed changes and approve or disapprove with explicit consideration for security and privacy impact.
**Assessment Mode**: hybrid
**What to check in code**:
- CI/CD pipeline configuration (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
- Branch protection rules (if config in repo)
- Pull request / merge request requirements
- Automated testing before deployment
- Deployment approval gates
- Change tracking in version control
**Pass criteria**: CI/CD pipeline exists with automated testing, branch protection or review requirements
**Common findings**: No CI/CD, direct push to main branch, no automated testing, no deployment gates

## CM-5 — Access Restrictions for Change

**Requirement**: Define, document, approve, and enforce physical and logical access restrictions associated with changes to the system.
**Assessment Mode**: hybrid
**What to check in code**:
- Branch protection configuration
- Deployment credentials management (not hardcoded)
- Role-based access to CI/CD pipelines
- Separate deployment keys/tokens per environment
- Infrastructure change permissions (IaC deployment roles)
**Pass criteria**: Branch protection enabled, deployment credentials managed securely
**Common findings**: No branch protection, deployment secrets in code, same credentials for all environments

## CM-6 — Configuration Settings

**Requirement**: Establish and document configuration settings for components employed within the system using security configuration checklists that reflect the most restrictive mode consistent with operational requirements.
**Assessment Mode**: auto
**What to check in code**:
- Security-hardened default configuration
- Debug mode disabled in production (NODE_ENV=production, DEBUG=false)
- Verbose error reporting disabled in production
- Secure defaults for framework configuration
- Default ports changed or documented
- Unnecessary features disabled
- Security headers configured (Helmet, security middleware)
**Pass criteria**: Production configuration hardened, debug disabled, secure defaults
**Common findings**: Debug mode in production, verbose errors enabled, default credentials, unnecessary features enabled, missing security headers

## CM-7 — Least Functionality

**Requirement**: Configure the system to provide only mission-essential capabilities; prohibit or restrict the use of non-essential functions, ports, protocols, software, and/or services.
**Assessment Mode**: hybrid
**What to check in code**:
- Minimal Docker base images (alpine, distroless, slim)
- Unused dependencies removed from package manifests
- Unnecessary ports not exposed (Docker, K8s, IaC)
- Development dependencies excluded from production builds
- Unnecessary middleware or plugins disabled
- Feature flags for optional functionality
**Pass criteria**: Minimal base images, no unnecessary dependencies in production, minimal port exposure
**Common findings**: Full OS base images, dev dependencies in production, unnecessary ports exposed, unused packages in manifests

## CM-8 — System Component Inventory

**Requirement**: Develop and document an inventory of system components that accurately reflects the system; is at the level of granularity deemed necessary for tracking and reporting; and includes relevant ownership information.
**Assessment Mode**: hybrid
**What to check in code**:
- Package manifest files (package.json, requirements.txt, go.mod, Cargo.toml, pom.xml)
- Lock files for reproducible builds
- SBOM generation capability or configuration
- Docker image manifest
- Service discovery configuration (for microservices)
- Dependency tree documentation
**Pass criteria**: Package manifests and lock files present, dependency tracking in place
**Common findings**: Missing lock files, no SBOM generation, outdated package manifests, undocumented service dependencies

---

## RA-5 — Vulnerability Monitoring and Scanning

**Requirement**: Monitor and scan for vulnerabilities in the system and hosted applications, and remediate discovered vulnerabilities in accordance with an organizational assessment of risk.
**Assessment Mode**: hybrid
**What to check in code**:
- SAST tools in CI/CD (ESLint security rules, Semgrep, CodeQL, SonarQube)
- Dependency vulnerability scanning (npm audit, Snyk, Dependabot, pip-audit)
- Container image scanning (Trivy, Snyk Container, Docker Scout)
- DAST tools integration (if configured)
- Security scanning results as CI gate (fail build on critical findings)
- Vulnerability tracking or suppression with justification
**Pass criteria**: Automated vulnerability scanning in CI/CD, dependency scanning active
**Common findings**: No SAST in CI, no dependency scanning, no container scanning, security findings don't block builds

---

## SA-3 — System Development Life Cycle

**Requirement**: Acquire, develop, and manage the system using a system development life cycle that incorporates information security and privacy considerations.
**Assessment Mode**: hybrid
**What to check in code**:
- Defined development workflow (branching strategy in CI/CD config)
- Code review requirements (PR templates, review rules)
- Testing infrastructure (unit, integration, e2e test directories)
- Security testing as part of development cycle
- Documentation of security-relevant design decisions
**Pass criteria**: Defined development workflow with code review and testing
**Common findings**: No code review process, no testing infrastructure, no security testing, direct deployment without review

## SA-4 — Acquisition Process

**Requirement**: Include security and privacy requirements and criteria in acquisition artifacts for the system or system component.
**Assessment Mode**: hybrid
**What to check in code**:
- Acquisition or supplier requirements captured in repo policy or config artifacts
- Dependency source verification (registry integrity, checksums, approved registries)
- Third-party library evaluation criteria
- License compliance tooling (license-checker, FOSSA)
- Approved or denied dependency or vendor lists
**Pass criteria**: Repository artifacts show acquisition or supplier requirements, or verifiable proxy controls for software component intake
**Common findings**: No license checking, dependencies from unverified sources, no repo-visible acquisition criteria, no approved-source policy artifacts

## SA-11 — Developer Testing and Evaluation

**Requirement**: Require the developer of the system to create and implement a security assessment plan, and perform unit, integration, system, and regression testing/evaluation at a defined depth and coverage.
**Assessment Mode**: auto
**What to check in code**:
- Test directory structure (test/, __tests__/, spec/, *_test.go)
- Test configuration (jest.config, pytest.ini, testing configs)
- Security-specific tests (auth tests, input validation tests, access control tests)
- Test coverage configuration and thresholds
- CI integration for test execution
- Integration and e2e test presence
**Pass criteria**: Test infrastructure exists, security-relevant tests present, CI runs tests
**Common findings**: No test directory, no security-specific tests, no test coverage requirements, tests not in CI

## SA-15 — Development Process, Standards, and Tools

**Requirement**: Require the developer of the system to follow a documented development process; use defined tools, and follow defined development standards.
**Assessment Mode**: hybrid
**What to check in code**:
- Linter configuration (ESLint, Pylint, golangci-lint, Clippy)
- Code formatter configuration (Prettier, Black, gofmt)
- Editor configuration (.editorconfig)
- Pre-commit hooks
- Coding standards documentation (CONTRIBUTING.md, code style guide)
- Static analysis tools beyond linting
**Pass criteria**: Linter and formatter configured, coding standards defined
**Common findings**: No linter, no formatter, no pre-commit hooks, no documented coding standards
