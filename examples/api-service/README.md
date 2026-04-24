# Golden API Service

Small TypeScript API used to demonstrate Shinsa evidence packs for GRC review.

Known assessment signals:

- Login uses bcrypt, which supports A.8.5 secure authentication.
- Login lacks rate limiting, which is a high-risk A.8.5 gap.
- Admin route checks an admin role but does not audit the privileged action, which is an A.8.15 gap.
- Logger masks authorization headers, which is positive evidence for data leakage prevention.

Run examples:

```text
/shinsa:quick-check A.8.5 examples/api-service
/shinsa:compliance-scan examples/api-service --controls A.8.5,A.8.15
```
