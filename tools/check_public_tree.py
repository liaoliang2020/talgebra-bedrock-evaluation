#!/usr/bin/env python3
"""Fail safely when public-release hazards are found in the working tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
MAX_FILE_SIZE = 2 * 1024 * 1024
SKIP_DIRECTORIES = {".git", ".venv", "venv", "__pycache__"}
FORBIDDEN_SUFFIXES = {
    ".7z",
    ".docx",
    ".key",
    ".mhtml",
    ".p12",
    ".pem",
    ".pfx",
    ".pdf",
    ".rar",
    ".zip",
}
FORBIDDEN_NAMES = {
    ".env",
    "credentials",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}
SENSITIVE_PATTERNS = {
    "cloud access key ID": re.compile(rb"(?:AKIA|ASIA)[A-Z0-9]{16}"),
    "repository access token": re.compile(
        rb"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})"
    ),
    "private key": re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----"),
    "12-digit account identifier": re.compile(rb"(?<!\d)\d{12}(?!\d)"),
    "email address": re.compile(
        rb"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.IGNORECASE
    ),
}


def tracked_candidates() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*")
        if path.is_file() and not any(part in SKIP_DIRECTORIES for part in path.parts)
    )


def main() -> int:
    problems: list[str] = []

    for path in tracked_candidates():
        relative_path = path.relative_to(ROOT)
        suffix = path.suffix.lower()

        if suffix in FORBIDDEN_SUFFIXES:
            problems.append(f"forbidden public artifact: {relative_path}")
        if path.name.lower() in FORBIDDEN_NAMES or path.name.lower().startswith(
            ".env."
        ):
            problems.append(f"forbidden credential filename: {relative_path}")

        size = path.stat().st_size
        if size > MAX_FILE_SIZE:
            problems.append(f"file exceeds 2 MiB: {relative_path}")

        if path == SELF:
            continue

        data = path.read_bytes()
        for label, pattern in SENSITIVE_PATTERNS.items():
            if pattern.search(data):
                problems.append(f"{label} pattern: {relative_path}")

    if problems:
        print("Public-readiness check failed:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1

    print("Public-readiness check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
