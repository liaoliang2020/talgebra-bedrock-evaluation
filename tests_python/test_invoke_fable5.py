"""Credential-free tests for the Claude Fable 5 demonstration client."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "aws_bedrock_demo" / "invoke_fable5.py"
)
SPEC = importlib.util.spec_from_file_location("invoke_fable5", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
CLIENT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CLIENT
SPEC.loader.exec_module(CLIENT)


class ResponseAssessmentTests(unittest.TestCase):
    def test_successful_response_collects_text_blocks(self) -> None:
        response = {
            "output": {
                "message": {
                    "content": [
                        {"text": "first"},
                        {"image": {"format": "png"}},
                        {"text": "second"},
                    ]
                }
            },
            "stopReason": "end_turn",
        }

        result = CLIENT.assess_response(response)

        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.text, "first\nsecond")
        self.assertEqual(result.stop_reason, "end_turn")

    def test_refusal_is_not_treated_as_success_or_retried(self) -> None:
        response = {
            "output": {"message": {"content": [{"text": "partial text"}]}},
            "stopReason": "refusal",
        }

        result = CLIENT.assess_response(response)

        self.assertEqual(result.exit_code, 6)
        self.assertEqual(result.text, "")
        self.assertIn("not retried", result.notice)

    def test_truncated_response_is_distinguishable(self) -> None:
        response = {
            "output": {"message": {"content": [{"text": "partial"}]}},
            "stopReason": "max_tokens",
        }

        result = CLIENT.assess_response(response)

        self.assertEqual(result.exit_code, 7)
        self.assertEqual(result.text, "partial")

    def test_missing_text_fails_closed(self) -> None:
        result = CLIENT.assess_response({"stopReason": "end_turn"})

        self.assertEqual(result.exit_code, 5)
        self.assertEqual(result.text, "")

    def test_malformed_envelope_fails_closed(self) -> None:
        result = CLIENT.assess_response(
            {"output": {"message": {"content": "not-a-list"}}}
        )

        self.assertEqual(result.exit_code, 5)


class RequestValidationTests(unittest.TestCase):
    def test_live_request_requires_explicit_acknowledgement(self) -> None:
        error = CLIENT.validate_live_request("synthetic prompt", False)

        self.assertIn("--acknowledge-provider-data-share", error)

    def test_acknowledged_synthetic_prompt_is_accepted(self) -> None:
        error = CLIENT.validate_live_request("synthetic prompt", True)

        self.assertIsNone(error)

    def test_empty_and_oversized_prompts_are_rejected(self) -> None:
        self.assertIsNotNone(CLIENT.validate_live_request("  ", True))
        oversized = "x" * (CLIENT.MAX_PROMPT_CHARACTERS + 1)
        self.assertIsNotNone(CLIENT.validate_live_request(oversized, True))


class InvokeTests(unittest.TestCase):
    def test_invoke_uses_converse_without_unsupported_sampling_fields(self) -> None:
        class FakeRuntimeClient:
            request: dict[str, object] | None = None

            def converse(self, **kwargs: object) -> dict[str, object]:
                self.request = kwargs
                return {
                    "output": {"message": {"content": [{"text": "ok"}]}},
                    "stopReason": "end_turn",
                }

        fake_client = FakeRuntimeClient()
        stdout = StringIO()
        stderr = StringIO()

        with patch("boto3.client", return_value=fake_client) as client_factory:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = CLIENT.invoke(
                    "synthetic prompt", "us-east-1", "anthropic.claude-fable-5"
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue().strip(), "ok")
        client_factory.assert_called_once()
        assert fake_client.request is not None
        self.assertEqual(
            fake_client.request["modelId"], "anthropic.claude-fable-5"
        )
        inference_config = fake_client.request["inferenceConfig"]
        self.assertEqual(inference_config, {"maxTokens": 1024})


if __name__ == "__main__":
    unittest.main()
