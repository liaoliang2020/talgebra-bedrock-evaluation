# Security policy

## Reporting

Use GitHub private vulnerability reporting when available. Do not put an
unredacted credential, personal data, account identifier, or exploit in a
public issue.

If a credential is exposed, revoke or rotate it before rewriting history.

## Repository boundary

This repository must not contain AWS access keys, Bedrock bearer tokens,
session tokens, `.env` files, private keys, passwords, account IDs, resource
ARNs tied to an account, personal contact details, prompt logs, or customer
data.

Credentials for local evaluation must come from the standard AWS credential
provider chain. Prefer a short-lived IAM role and never configure a live AWS
credential in GitHub Actions.

## Fable 5 data boundary

The example is limited to public documentation, explicitly approved source
excerpts, and synthetic data. Do not submit personal, confidential, regulated,
licensed, export-controlled, or classified material.

The client requires `--acknowledge-provider-data-share` for every live call and
does not configure the AWS account's retention mode. Review the current AWS
terms, model card, regional availability, and retention documentation before
each deployment.

## Local checks

```bash
python -m py_compile aws_bedrock_demo/invoke_fable5.py tools/check_public_tree.py
python aws_bedrock_demo/invoke_fable5.py --dry-run
python -m unittest discover -s tests_python -v
python tools/check_public_tree.py
```
