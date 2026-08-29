# IAM and account setup for the Fable 5 evaluation

Last reviewed: 2026-08-29

This checklist targets the standard Amazon Bedrock Runtime endpoint used by the
example. It intentionally separates one-time account setup from daily model
invocation.

## Choose the endpoint deliberately

The example uses `bedrock-runtime` with the `Converse` API. This route supports
Bedrock features such as Guardrails, model evaluation, Knowledge Bases, Flows,
and Agents, but it requires the Anthropic first-time-use form.

AWS currently states that the first-time-use form does not apply to Anthropic
models accessed through `bedrock-mantle`. That endpoint has a different API,
IAM namespace, feature set, and project-level retention option. Do not mix its
credentials or instructions with this example.

## One-time setup principal

An AWS account owner or delegated setup administrator should complete these
steps. Do not grant these capabilities to the runtime client.

1. Verify the AWS account has a valid payment method.
2. Review the applicable AWS and Anthropic terms.
3. Submit accurate Anthropic first-time-use details.
4. Complete or allow the one-time AWS Marketplace subscription.
5. Review and explicitly set the required data-retention mode.
6. Verify model availability before assigning a runtime role.

The first model activation can require these Marketplace actions:

- `aws-marketplace:Subscribe`;
- `aws-marketplace:Unsubscribe`;
- `aws-marketplace:ViewSubscriptions`.

After model activation, remove Marketplace subscription permissions from the
normal runtime identity. Keep `bedrock:PutAccountDataRetention` and
`bedrock:PutUseCaseForModelAccess` restricted to account setup administrators.

AWS CLI version 2.27.42 or later is required by the current programmatic model
access instructions. Read-only checks include:

```bash
aws bedrock get-account-data-retention --region us-east-1
aws bedrock get-foundation-model-availability \
  --model-id anthropic.claude-fable-5 \
  --region us-east-1
```

Changing data retention has legal and privacy consequences. This repository
does not run `put-account-data-retention` automatically.

## Daily runtime principal

The included policy example grants only `bedrock:InvokeModel` for the direct
Fable 5 foundation-model resource in `us-east-1`. The `Converse` API uses that
IAM action. Attach the policy to a short-lived role used solely for this
evaluation.

If the project later uses a geo or global inference profile, create and review
a separate policy for that exact profile. Do not broaden the example to all
Bedrock models merely to avoid an authorization error.

## Credential handling

- Prefer IAM Identity Center, role assumption, or another short-lived provider.
- Keep credentials outside the repository and outside GitHub Actions.
- Do not paste account IDs, ARNs, access keys, or console screenshots into an
  issue or support request.
- Do not use the AWS root user for daily invocation.
- Enable MFA for identities capable of account setup or billing changes.

## Cost controls

Before the first live request, configure a small AWS Budget, cost notifications,
and an appropriate Bedrock service quota. Budget notifications are not an
instant hard spending cap, so keep the evaluation client human-operated and
low-volume.

## Official references

- [Amazon Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html)
- [Identity-based policy examples](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)
- [Amazon Bedrock data retention](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html)
- [Converse API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html)
