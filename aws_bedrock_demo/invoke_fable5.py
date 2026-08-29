#!/usr/bin/env python3
"""Minimal, privacy-conscious Claude Fable 5 call through Amazon Bedrock."""

from __future__ import annotations

import argparse
import os
import sys
from dataclasses import dataclass
from typing import Any


DEFAULT_MODEL_ID = "anthropic.claude-fable-5"
DEFAULT_REGION = "us-east-1"
MAX_PROMPT_CHARACTERS = 20_000
DEFAULT_PROMPT = (
    "Using only the definition supplied here, explain how Fourier-domain "
    "slice computations can reduce a t-matrix multiplication to independent "
    "ordinary matrix multiplications. State any assumptions and do not infer "
    "facts about people or organizations."
)


@dataclass(frozen=True)
class ResponseAssessment:
    """A normalized result that keeps refusal handling easy to test."""

    exit_code: int
    text: str
    stop_reason: str
    notice: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Invoke Claude Fable 5 for a public-code research example."
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Public, non-sensitive prompt to send to the model.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without loading credentials or calling AWS.",
    )
    parser.add_argument(
        "--acknowledge-provider-data-share",
        action="store_true",
        help=(
            "Confirm that this live request may be shared with Anthropic and "
            "retained for up to 30 days. Required for every live call."
        ),
    )
    return parser.parse_args()


def runtime_configuration() -> tuple[str, str]:
    region = os.environ.get("AWS_REGION") or os.environ.get(
        "AWS_DEFAULT_REGION", DEFAULT_REGION
    )
    model_id = os.environ.get("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)
    return region, model_id


def extract_text(response: dict[str, Any]) -> str:
    output = response.get("output")
    if not isinstance(output, dict):
        return ""
    message = output.get("message")
    if not isinstance(message, dict):
        return ""
    content = message.get("content")
    if not isinstance(content, list):
        return ""
    return "\n".join(
        block["text"]
        for block in content
        if isinstance(block, dict) and isinstance(block.get("text"), str)
    ).strip()


def assess_response(response: dict[str, Any]) -> ResponseAssessment:
    """Classify normal, refused, truncated, and malformed Converse responses."""

    stop_reason = str(response.get("stopReason", "unknown"))
    text = extract_text(response)

    if stop_reason in {"refusal", "content_filtered", "guardrail_intervened"}:
        return ResponseAssessment(
            exit_code=6,
            text="",
            stop_reason=stop_reason,
            notice=(
                "The request was declined by a model safety classifier or "
                "Bedrock Guardrail. It was not retried."
            ),
        )

    if stop_reason == "tool_use":
        return ResponseAssessment(
            exit_code=8,
            text="",
            stop_reason=stop_reason,
            notice="The model requested a tool, but this example executes no tools.",
        )

    if not text:
        return ResponseAssessment(
            exit_code=5,
            text="",
            stop_reason=stop_reason,
            notice="No text was returned by the model.",
        )

    if stop_reason in {"max_tokens", "model_context_window_exceeded"}:
        return ResponseAssessment(
            exit_code=7,
            text=text,
            stop_reason=stop_reason,
            notice="The response is incomplete because a model limit was reached.",
        )

    return ResponseAssessment(
        exit_code=0,
        text=text,
        stop_reason=stop_reason,
        notice="",
    )


def validate_live_request(prompt: str, acknowledged: bool) -> str | None:
    """Return a user-facing validation error, or ``None`` when safe to proceed."""

    if not prompt.strip():
        return "The prompt must not be empty."
    if len(prompt) > MAX_PROMPT_CHARACTERS:
        return f"The prompt exceeds the {MAX_PROMPT_CHARACTERS:,}-character demo limit."
    if not acknowledged:
        return (
            "Live invocation requires --acknowledge-provider-data-share. "
            "Review the AWS retention terms before continuing."
        )
    return None


def guidance_for_client_error(code: str) -> str:
    """Return guidance without echoing potentially identifying AWS error text."""

    guidance = {
        "AccessDeniedException": (
            "Check the Anthropic first-time-use form, Marketplace activation, "
            "provider_data_share mode, and bedrock:InvokeModel permission."
        ),
        "ValidationException": (
            "Check the selected region, model ID, and Fable 5 parameters."
        ),
        "ThrottlingException": "Check the service quota and retry later.",
    }
    return guidance.get(
        code, "Review the AWS console and CloudTrail with an account owner."
    )


def invoke(prompt: str, region: str, model_id: str) -> int:
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
        from botocore.config import Config
    except ImportError:
        print(
            "boto3 is not installed; install aws_bedrock_demo/requirements.txt.",
            file=sys.stderr,
        )
        return 2

    try:
        client = boto3.client(
            "bedrock-runtime",
            region_name=region,
            config=Config(
                connect_timeout=10,
                read_timeout=120,
                retries={"max_attempts": 2, "mode": "standard"},
                user_agent_extra="talgebra-fable5-evaluation/0.1",
            ),
        )
        response = client.converse(
            modelId=model_id,
            system=[
                {
                    "text": (
                        "You are a human-supervised research-software assistant. "
                        "Analyze only the information supplied in the request, "
                        "state uncertainty, and do not infer personal information."
                    )
                }
            ],
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"maxTokens": 1024},
        )
    except NoCredentialsError:
        print("No AWS credentials were available from the provider chain.", file=sys.stderr)
        return 3
    except (BotoCoreError, ClientError) as error:
        if isinstance(error, ClientError):
            details = error.response.get("Error", {})
            code = details.get("Code", "ClientError")
            print(
                f"AWS request failed ({code}). {guidance_for_client_error(code)}",
                file=sys.stderr,
            )
        else:
            print(f"AWS request failed: {type(error).__name__}", file=sys.stderr)
        return 4

    assessment = assess_response(response)
    if assessment.text:
        print(assessment.text)
    if assessment.notice:
        print(assessment.notice, file=sys.stderr)
    print(f"[stop reason: {assessment.stop_reason}]", file=sys.stderr)
    return assessment.exit_code


def main() -> int:
    args = parse_args()
    region, model_id = runtime_configuration()

    if args.dry_run:
        print("Dry run passed.")
        print(f"Region: {region}")
        print(f"Model ID: {model_id}")
        print(f"Prompt characters: {len(args.prompt)}")
        print("A provider-data-sharing acknowledgement is required for a live call.")
        print("No credentials were loaded and no network request was made.")
        return 0

    validation_error = validate_live_request(
        args.prompt, args.acknowledge_provider_data_share
    )
    if validation_error:
        print(validation_error, file=sys.stderr)
        return 2

    return invoke(args.prompt, region, model_id)


if __name__ == "__main__":
    raise SystemExit(main())
