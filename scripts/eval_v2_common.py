#!/usr/bin/env python3
"""Shared helpers for Industrial Agent Benchmark v1.1 evaluation pipeline.

This module intentionally avoids importing application code from sibling
repositories. It provides a tiny OpenAI-compatible HTTP provider used only when
explicitly requested; dry-run and dummy modes do not perform network calls.
"""
from __future__ import annotations

import csv
import json
import math
import os
import re
import statistics
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EVALUATION_SET = ROOT / "evaluation_set_v2.yaml"
DEFAULT_INDEX = ROOT / "benchmark_data" / "index.yaml"
DEFAULT_OUTPUT_ROOT = ROOT / "datasets" / "results"
ANSWER_PROMPT_TEMPLATE_VERSION = "iab_v1_1_answer_prompt_v1"
JUDGE_PROMPT_TEMPLATE_VERSION = "iab_v1_1_judge_v2"

PROMPT_FORBIDDEN_TERMS = [
    "reference_answer",
    "evaluation_rubric",
    "must_have",
    "nice_to_have",
    "critical_failures",
    "score_cap_rules",
    "numeric_checks",
    "disallowed_answers",
    "expected_value",
]

JUDGED_REQUIRED_KEYS = [
    "model_id",
    "question_id",
    "layer",
    "category",
    "difficulty",
    "domain",
    "final_score",
    "must_have_missing_count",
    "numeric_check_failed_ratio",
    "generic_penalty_triggered",
    "critical_failure_triggered",
    "score_cap_applied",
    "judge_summary",
    "evidence_summary",
]

LEADERBOARD_COLUMNS = [
    "model_id",
    "question_id",
    "layer",
    "category",
    "difficulty",
    "domain",
    "final_score",
    "must_have_missing_count",
    "numeric_check_failed_ratio",
    "generic_penalty_triggered",
    "critical_failure_triggered",
    "score_cap_applied",
    "judge_summary",
]

METRIC_COLUMNS = [
    "run_id",
    "model_id",
    "question_count",
    "avg_final_score",
    "score_std",
    "min_score",
    "max_score",
    "critical_failure_count",
    "critical_failure_rate",
    "score_cap_rate",
    "generic_penalty_rate",
    "avg_numeric_check_failed_ratio",
    "structured_output_failure_rate",
]

GROUPED_METRIC_COLUMNS = ["group_type", "group_value", *METRIC_COLUMNS]


@dataclass(frozen=True)
class LLMResponse:
    text: str
    model: str
    provider: str


class ProviderError(RuntimeError):
    """Raised when a provider request or response is invalid."""


class DummyProvider:
    """Deterministic no-network provider for dry-run plumbing checks only."""

    def __init__(self, model: str = "dummy") -> None:
        self.model = model

    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResponse:
        if "## Inputs" in prompt and "Model Answer" in prompt:
            text = json.dumps(
                {
                    "model_id": self.model,
                    "question_id": "DUMMY",
                    "layer": "dry_run",
                    "category": "dry_run",
                    "difficulty": 0,
                    "domain": "dry_run",
                    "final_score": 1,
                    "must_have_missing_count": 0,
                    "numeric_check_failed_ratio": 0.0,
                    "generic_penalty_triggered": False,
                    "critical_failure_triggered": False,
                    "score_cap_applied": False,
                    "structured_output_missing_count": 0,
                    "judge_summary": "Dummy provider output; not a benchmark result.",
                    "evidence_summary": "No evidence evaluated in dummy mode.",
                },
                ensure_ascii=False,
            )
        else:
            text = (
                "This is a dry-run/dummy placeholder answer. "
                "For real evaluation, specify a provider explicitly to generate answers."
            )
        return LLMResponse(text=text, model=self.model, provider="dummy")


# HTTP status codes treated as transient and worth retrying.
_RETRYABLE_HTTP_STATUS = frozenset({408, 409, 425, 429, 500, 502, 503, 504})


class FuguCompatibleProvider:
    """Minimal OpenAI-compatible chat completions provider.

    Environment variables:
      - FUGU_API_KEY
      - FUGU_BASE_URL
      - FUGU_MODEL (optional fallback; get_provider("fugu", model_id) uses model_id by default)
      - FUGU_TIMEOUT_SECONDS (optional, default 300)
      - FUGU_MAX_RETRIES (optional, default 3) - number of *additional* attempts
        after the first request when a transient error or timeout occurs.
      - FUGU_BACKOFF_BASE_SECONDS (optional, default 5.0) - base delay for
        exponential backoff between retries (delay = base * 2**attempt).
      - FUGU_BACKOFF_CAP_SECONDS (optional, default 60.0) - upper bound on the
        backoff delay between any two attempts.

    Constructor arguments override the corresponding environment variables.
    The request always uses temperature 0.0.
    """

    def __init__(
        self,
        model: str | None = None,
        timeout: int | None = None,
        max_retries: int | None = None,
        backoff_base_seconds: float | None = None,
        backoff_cap_seconds: float | None = None,
    ) -> None:
        self.api_key = os.getenv("FUGU_API_KEY")
        self.base_url = os.getenv("FUGU_BASE_URL")
        self.model = model or os.getenv("FUGU_MODEL")
        self.timeout = timeout if timeout is not None else int(os.getenv("FUGU_TIMEOUT_SECONDS", "300"))
        self.max_retries = (
            max_retries
            if max_retries is not None
            else int(os.getenv("FUGU_MAX_RETRIES", "3"))
        )
        if self.max_retries < 0:
            self.max_retries = 0
        self.backoff_base_seconds = (
            backoff_base_seconds
            if backoff_base_seconds is not None
            else float(os.getenv("FUGU_BACKOFF_BASE_SECONDS", "5.0"))
        )
        if self.backoff_base_seconds < 0:
            self.backoff_base_seconds = 0.0
        self.backoff_cap_seconds = (
            backoff_cap_seconds
            if backoff_cap_seconds is not None
            else float(os.getenv("FUGU_BACKOFF_CAP_SECONDS", "60.0"))
        )
        if self.backoff_cap_seconds < self.backoff_base_seconds:
            self.backoff_cap_seconds = self.backoff_base_seconds
        if not self.api_key:
            raise ValueError("FUGU_API_KEY is not set")
        if not self.base_url:
            raise ValueError("FUGU_BASE_URL is not set")
        if not self.model:
            raise ValueError("FUGU_MODEL is not set")

    def _backoff_delay(self, attempt: int) -> float:
        # attempt is 0-indexed (0 for first retry, 1 for second, ...).
        delay = self.backoff_base_seconds * (2 ** attempt)
        return min(delay, self.backoff_cap_seconds)

    def _attempt_once(self, payload: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            return json.loads(response.read().decode("utf-8"))

    def generate(self, prompt: str, system_prompt: str | None = None) -> LLMResponse:
        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        payload = {"model": self.model, "messages": messages, "temperature": 0.0}

        total_attempts = self.max_retries + 1
        last_error: ProviderError | None = None
        data: dict[str, Any] | None = None
        for attempt in range(total_attempts):
            try:
                data = self._attempt_once(payload)
                break
            except urllib.error.HTTPError as error:
                detail = _read_http_error_detail(error)
                err = ProviderError(
                    f"Provider request failed with HTTP {error.code}: {detail}"
                )
                err.__cause__ = error
                retryable = error.code in _RETRYABLE_HTTP_STATUS
                last_error = err
                if not retryable or attempt == total_attempts - 1:
                    raise err from error
            except urllib.error.URLError as error:
                err = ProviderError(f"Provider request failed: {error.reason}")
                err.__cause__ = error
                last_error = err
                if attempt == total_attempts - 1:
                    raise err from error
            except TimeoutError as error:
                err = ProviderError("Provider request timed out")
                err.__cause__ = error
                last_error = err
                if attempt == total_attempts - 1:
                    raise err from error
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                # Invalid JSON is treated as transient (likely truncated body).
                err = ProviderError("Provider returned invalid JSON")
                err.__cause__ = error
                last_error = err
                if attempt == total_attempts - 1:
                    raise err from error
            # Sleep with exponential backoff before the next attempt.
            time.sleep(self._backoff_delay(attempt))

        if data is None:
            # Should be unreachable; raise the last captured error defensively.
            raise last_error or ProviderError("Provider request failed for unknown reason")

        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as error:
            raise ProviderError("Provider response is missing choices[0].message.content") from error
        if not isinstance(text, str):
            raise ProviderError("Provider response content must be a string")
        return LLMResponse(text=text, model=self.model or "unknown", provider="fugu")


def get_provider(
    provider: str,
    model_id: str,
    *,
    timeout: int | None = None,
    max_retries: int | None = None,
    backoff_base_seconds: float | None = None,
) -> DummyProvider | FuguCompatibleProvider:
    if provider == "dummy":
        return DummyProvider(model=model_id)
    if provider == "fugu":
        return FuguCompatibleProvider(
            model=model_id,
            timeout=timeout,
            max_retries=max_retries,
            backoff_base_seconds=backoff_base_seconds,
        )
    raise ValueError(f"Unsupported provider: {provider}")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_evaluation_questions(evaluation_set: Path = DEFAULT_EVALUATION_SET) -> list[dict[str, Any]]:
    data = load_yaml(evaluation_set)
    questions = data.get("questions", [])
    if not isinstance(questions, list):
        raise ValueError(f"{evaluation_set} field 'questions' must be a list")
    return questions


def load_index_by_id(index_path: Path = DEFAULT_INDEX) -> dict[str, dict[str, Any]]:
    index = load_yaml(index_path)
    items = index.get("items", [])
    if not isinstance(items, list):
        raise ValueError(f"{index_path} field 'items' must be a list")
    return {str(item["id"]): item for item in items if isinstance(item, dict) and "id" in item}


def problem_path_from_index(index_by_id: dict[str, dict[str, Any]], question_id: str) -> Path:
    item = index_by_id.get(question_id)
    if not item:
        raise KeyError(f"question_id {question_id} not found in benchmark_data/index.yaml")
    return ROOT / str(item["file_path"])


def load_problem(question_id: str, index_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    return load_yaml(problem_path_from_index(index_by_id, question_id))


def render_answer_prompt(question_meta: dict[str, Any], problem: dict[str, Any]) -> str:
    metadata = {
        "question_id": problem.get("id", question_meta.get("id")),
        "layer": problem.get("layer", question_meta.get("layer")),
        "category": problem.get("category", question_meta.get("category")),
        "domain": problem.get("domain", question_meta.get("domain")),
        "subdomain": problem.get("subdomain", ""),
        "difficulty": problem.get("difficulty", question_meta.get("difficulty")),
        "estimated_time_min": problem.get("estimated_time_min", ""),
        "title": problem.get("title", ""),
    }
    metadata_yaml = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip()
    scenario = str(problem.get("scenario", "")).strip()
    question = str(problem.get("question", "")).strip()
    return (
        "# Industrial Agent Benchmark v1.1.0-pre Answer Prompt\n\n"
        "## Question Metadata\n\n"
        "```yaml\n"
        f"{metadata_yaml}\n"
        "```\n\n"
        "## Scenario\n\n"
        "```text\n"
        f"{scenario}\n"
        "```\n\n"
        "## Question\n\n"
        "```text\n"
        f"{question}\n"
        "```\n"
    )


def check_prompt_leakage(prompt: str) -> list[str]:
    lowered = prompt.lower()
    return [term for term in PROMPT_FORBIDDEN_TERMS if term.lower() in lowered]


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False, sort_keys=False) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8-sig") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSONL at {path}:{line_number}: {error}") from error
            if not isinstance(item, dict):
                raise ValueError(f"JSONL item at {path}:{line_number} must be an object")
            rows.append(item)
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"\s*```$", "", stripped)
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if not match:
            raise
        data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("Judge output must be a JSON object")
    return data


def normalize_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"true", "yes", "1", "y", "triggered", "applied"}
    if isinstance(value, list):
        return bool(value)
    if isinstance(value, dict):
        return bool(value)
    return False


def normalize_float(value: Any, default: float = 0.0) -> float:
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if math.isnan(float(value)):
            return default
        return float(value)
    try:
        return float(str(value).strip())
    except ValueError:
        return default


def normalize_int(value: Any, default: int = 0) -> int:
    try:
        return int(round(normalize_float(value, float(default))))
    except (TypeError, ValueError):
        return default


def normalize_score(value: Any) -> float:
    score = normalize_float(value, 0.0)
    return max(0.0, min(5.0, score))


def normalize_judgement(
    raw: dict[str, Any],
    *,
    run_id: str,
    model_id: str,
    question_meta: dict[str, Any],
) -> dict[str, Any]:
    qid = str(question_meta.get("id") or raw.get("question_id"))
    normalized = {
        "run_id": run_id,
        "model_id": str(raw.get("model_id") or model_id),
        "question_id": qid,
        "layer": str(raw.get("layer") or question_meta.get("layer", "")),
        "category": str(raw.get("category") or question_meta.get("category", "")),
        "difficulty": normalize_int(raw.get("difficulty", question_meta.get("difficulty", 0))),
        "domain": str(raw.get("domain") or question_meta.get("domain", "")),
        "final_score": normalize_score(raw.get("final_score")),
        "must_have_missing_count": normalize_int(raw.get("must_have_missing_count")),
        "numeric_check_failed_ratio": normalize_float(raw.get("numeric_check_failed_ratio")),
        "generic_penalty_triggered": normalize_bool(raw.get("generic_penalty_triggered")),
        "critical_failure_triggered": normalize_bool(raw.get("critical_failure_triggered")),
        "score_cap_applied": normalize_bool(raw.get("score_cap_applied")),
        "structured_output_missing_count": normalize_int(raw.get("structured_output_missing_count")),
        "judge_summary": str(raw.get("judge_summary", "")),
        "evidence_summary": str(raw.get("evidence_summary", "")),
        "raw_judgement": raw,
    }
    return normalized


def compute_metric_row(rows: list[dict[str, Any]], *, run_id: str, model_id: str) -> dict[str, Any]:
    scores = [normalize_score(row.get("final_score")) for row in rows]
    count = len(scores)
    avg = statistics.fmean(scores) if scores else 0.0
    std = statistics.pstdev(scores) if len(scores) > 1 else 0.0
    critical_count = sum(1 for row in rows if normalize_bool(row.get("critical_failure_triggered")))
    cap_count = sum(1 for row in rows if normalize_bool(row.get("score_cap_applied")))
    generic_count = sum(1 for row in rows if normalize_bool(row.get("generic_penalty_triggered")))
    structured_fail_count = sum(1 for row in rows if normalize_int(row.get("structured_output_missing_count")) > 0)
    numeric_avg = statistics.fmean([normalize_float(row.get("numeric_check_failed_ratio")) for row in rows]) if rows else 0.0
    return {
        "run_id": run_id,
        "model_id": model_id,
        "question_count": count,
        "avg_final_score": round(avg, 4),
        "score_std": round(std, 4),
        "min_score": min(scores) if scores else 0.0,
        "max_score": max(scores) if scores else 0.0,
        "critical_failure_count": critical_count,
        "critical_failure_rate": round(critical_count / count, 4) if count else 0.0,
        "score_cap_rate": round(cap_count / count, 4) if count else 0.0,
        "generic_penalty_rate": round(generic_count / count, 4) if count else 0.0,
        "avg_numeric_check_failed_ratio": round(numeric_avg, 4),
        "structured_output_failure_rate": round(structured_fail_count / count, 4) if count else 0.0,
    }


def group_rows(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(str(row.get(key, "")), []).append(row)
    return groups


def _read_http_error_detail(error: urllib.error.HTTPError) -> str:
    try:
        data = json.loads(error.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return str(error.reason)
    if isinstance(data, dict):
        data = data.get("error", data)
    if isinstance(data, dict):
        return str(data.get("message") or data)
    return str(data)


def safe_duration(start: float, end: float) -> float:
    return round(max(0.0, end - start), 4)
