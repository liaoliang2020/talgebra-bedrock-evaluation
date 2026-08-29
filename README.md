# T-Algebra Bedrock Evaluation

[![Public readiness](https://github.com/liaoliang2020/talgebra-bedrock-evaluation/actions/workflows/public-readiness.yml/badge.svg)](https://github.com/liaoliang2020/talgebra-bedrock-evaluation/actions/workflows/public-readiness.yml)

This is the public project page for a proposed, low-volume evaluation of
Anthropic Claude Fable 5 through Amazon Bedrock. The intended use is a
human-supervised mathematical research and coding assistant for generalized
linear algebra, tensor computation, and MATLAB research software.

This repository is deliberately small. It contains the public use-case
statement, data boundary, least-privilege IAM example, credential-free client
tests, and a minimal Python client. It does not contain a manuscript, private
research notes, personal data, AWS credentials, customer data, or the complete
MATLAB research codebase.

## Intended evaluation

The model may be asked to:

- explain approved, non-sensitive algorithm excerpts;
- propose synthetic numerical tests;
- check dimensions and assumptions in small MATLAB functions;
- help prepare reproducible experiments with synthetic inputs; and
- summarize results for a human researcher.

The model will not make medical, legal, financial, employment, or other
high-impact decisions. A human remains responsible for every mathematical
claim and software change.

See the [complete use-case statement](docs/USE_CASE.md),
[data-handling boundary](docs/DATA_HANDLING.md), and
[IAM and account checklist](docs/IAM_AND_ACCOUNT_SETUP.md).

## Privacy boundary

Claude Fable 5 currently requires the Amazon Bedrock retention mode
`provider_data_share`. AWS documents that prompts and completions may be shared
with Anthropic and retained for up to 30 days for trust and safety. Initial
inputs are therefore restricted to public documentation, explicitly approved
source excerpts, and synthetic data.

The example never changes an AWS account's retention setting. A live call also
requires the explicit local option `--acknowledge-provider-data-share`.

## Credential-free verification

Python 3.10 or later is required.

```bash
python -m pip install -r aws_bedrock_demo/requirements.txt
python aws_bedrock_demo/invoke_fable5.py --dry-run
python -m unittest discover -s tests_python -v
python tools/check_public_tree.py
```

The dry run and tests neither load AWS credentials nor contact AWS. Do not add
AWS keys or a live Bedrock call to GitHub Actions.

## Live evaluation

Only an AWS account owner or an authorized operator should complete the
first-time-use form, review the applicable terms, configure retention, and
assign a short-lived runtime role. After that account-side work, the built-in
synthetic prompt can be invoked manually:

```bash
export AWS_REGION=us-east-1
export BEDROCK_MODEL_ID=anthropic.claude-fable-5
python aws_bedrock_demo/invoke_fable5.py \
  --acknowledge-provider-data-share
```

No prompt text or model output is written to the repository by the client.

## Status

This is an evaluation scaffold, not a production service. It is not affiliated
with or endorsed by Amazon Web Services, Anthropic, MathWorks, or GitHub.
