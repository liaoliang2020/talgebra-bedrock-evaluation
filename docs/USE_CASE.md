# Claude Fable 5 use-case statement

Last reviewed: 2026-08-29

This statement can be adapted to the Anthropic first-time-use form for the
standard Amazon Bedrock Runtime route. The actual submission must match the
applicant's AWS account, users, region, and deployment plan.

## Project identity

- Project name: T-Algebra Project
- Project type: independent, non-company research-software project
- Public URL:
  <https://github.com/liaoliang2020/talgebra-bedrock-evaluation>
- Field: mathematical research software, education, and numerical computing

The project must not be presented as a registered company unless that is
independently true for the applicant.

## Proposed use

Claude Fable 5 will be evaluated as a human-supervised mathematical research
and coding assistant. It may explain generalized-linear-algebra and
tensor-computation algorithms, propose synthetic tests, review approved MATLAB
excerpts for dimensional consistency, and help design reproducible numerical
experiments.

Initial use is internal, low-volume research and development by project
maintainers. No external-facing service is included. A human reviews every
mathematical claim and proposed code change.

## Suggested concise form text

> We are evaluating Anthropic Claude Fable 5 on Amazon Bedrock as a
> human-supervised research and coding assistant for a privacy-reviewed MATLAB
> toolkit in generalized linear algebra and tensor computation. The model will
> analyze approved source excerpts, explain algorithms, propose synthetic tests,
> and help prepare reproducible numerical experiments. Initial use is internal
> and low volume. Inputs will be limited to public project documentation,
> approved non-sensitive source excerpts, and synthetic numerical examples. We
> will not use the system for high-impact decisions or submit credentials,
> personal data, confidential manuscripts, regulated records, or proprietary
> customer data. A human will review all generated mathematics and code.

## Form mapping

| Form field | Project answer |
| --- | --- |
| Company or project name | `T-Algebra Project`, explicitly described as an independent research project |
| Website | `https://github.com/liaoliang2020/talgebra-bedrock-evaluation` |
| Intended users | Internal (`0`) |
| Industry | Select the closest available research, education, software, or technology option in the current console |
| Other industry | Complete only if the selected option is Other |
| Use cases | Use the concise text above |

If AWS requests a legal person or billing identity, the account owner must
answer truthfully in AWS. Private account information must not be added here.

## Safety controls

- prompts are short, deliberately selected, and non-sensitive;
- the client reads no repository file automatically;
- every live call requires a provider-data-sharing acknowledgement;
- refusal and Guardrail stop reasons are handled without bypass retries;
- the client does not log prompt bodies;
- the runtime role is restricted to the selected model;
- a human reviews all outputs; and
- spending alerts and low request volume are required before live use.

## Excluded uses and data

The project excludes high-impact decisions, unattended external services,
credentials, account identifiers, personal information, confidential or
unpublished manuscripts, proprietary customer data, regulated records,
unauthorized third-party content, and export-controlled or classified material.

## Official references

- [Amazon Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [Claude Fable 5 model card](https://docs.aws.amazon.com/bedrock/latest/userguide/model-card-anthropic-claude-fable-5.html)
- [Amazon Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)
