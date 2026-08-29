# Security policy

## Supported version

Security and privacy fixes apply to the current `main` branch.

## Private reporting

Use the repository's private vulnerability-reporting or private
security-advisory mechanism. Do not place credentials, personal data, or an
unredacted exploit in a public issue.

If a credential has been committed, revoke or rotate it first. Rewriting Git
history is not a substitute for revocation.

## Public-tree boundary

This repository must not contain:

- passwords, access tokens, private keys, or `.env` files;
- personal names, email addresses, affiliations, or location information;
- unpublished manuscripts or restricted datasets;
- local filesystem paths or machine-specific configuration; or
- binary archives and exported browser pages.

Examples and tests must use deterministic synthetic arrays. No test should
open a network connection or require a secret.

## Local checks

Run:

```bash
python tools/check_public_tree.py
```

Then execute the MATLAB smoke test:

```matlab
run("tests/run_smoke_tests.m")
```
