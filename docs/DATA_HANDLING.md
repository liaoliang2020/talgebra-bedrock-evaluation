# Data handling for the Fable 5 evaluation

Last reviewed: 2026-08-29

This project uses a narrow, human-supervised evaluation boundary. It does not
automatically index the repository, upload files, or send a manuscript to
Amazon Bedrock.

## Data flow

1. A maintainer selects a short, non-sensitive prompt.
2. The local client verifies prompt length and requires an explicit
   provider-data-sharing acknowledgement.
3. The standard Amazon Bedrock Runtime `Converse` endpoint sends the prompt to
   Claude Fable 5.
4. The client displays text and a normalized stop reason. It does not write the
   prompt or response to a repository file.
5. A human reviews every mathematical statement and proposed code change.

No repository source file is read automatically. The default prompt is a
synthetic mathematical question embedded in the client.

## Allowed initial inputs

- the built-in synthetic prompt;
- small synthetic matrices, tensors, and error cases;
- short excerpts of project code specifically approved by a maintainer;
- public project documentation.

## Prohibited inputs

- credentials, tokens, passwords, account identifiers, or resource ARNs;
- names, email addresses, locations, affiliations, or contact information;
- unpublished manuscripts or confidential research notes;
- proprietary, licensed, regulated, biometric, medical, financial, legal,
  employment, export-controlled, or classified data;
- third-party material that the project is not authorized to submit.

## Provider sharing and retention

Under the AWS documentation reviewed on the date above, Claude Fable 5 requires
the effective retention mode `provider_data_share`. Prompts and completions may
be shared with Anthropic and retained for up to 30 days for trust and safety.
Cross-region inference can cause retained inputs and outputs to be stored in a
destination region.

The project therefore defaults to the direct model identifier in `us-east-1`
and does not enable cross-region inference automatically. The account owner
must review the current terms and make the retention decision outside this
repository.

## Logging and incident response

The demonstration client does not configure Bedrock model-invocation logging
and does not log prompt bodies. Operational systems should record only the
minimum metadata needed for cost, availability, and incident review.

If restricted data is submitted accidentally, stop further calls, preserve
only the minimum incident metadata, notify the AWS account owner, and follow
the applicable AWS and organizational incident-response process.

## Official references

- [Amazon Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)
- [Claude Fable 5 model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-fable-5.html)
- [Amazon Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
