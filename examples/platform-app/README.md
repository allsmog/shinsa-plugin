# Golden Platform App

Small app with application code, Docker configuration, and CI metadata used to demonstrate NIST-oriented evidence packs.

Known assessment signals:

- Docker image uses a fixed runtime family but does not pin a digest.
- CI runs dependency audit and tests.
- Application health endpoint supports monitoring evidence.
- Container lacks an explicit non-root runtime user.

Run examples:

```text
/shinsa:nist-quick-check CM examples/platform-app
/shinsa:nist-scan examples/platform-app --family CM,RA,SI
```
