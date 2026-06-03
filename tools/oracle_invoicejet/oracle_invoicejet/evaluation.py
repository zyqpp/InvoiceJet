from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import time
from typing import Any, List

from .agents import OracleOrchestrator
from .config import AppConfig
from .rag import NO_ANSWER
from .rag_profiles import get_rag_profile
from .retrieval import RetrievalService


@dataclass(frozen=True)
class EvalCase:
    id: str
    question: str
    rag_profile: str = "full_app_qa"
    expected_sources: List[str] = field(default_factory=list)
    expected_source_types: List[str] = field(default_factory=list)
    expect_fallback: bool = False
    notes: str = ""


@dataclass(frozen=True)
class EvalResult:
    case_id: str
    question: str
    mode: str
    passed: bool
    answer: str
    sources: List[str]
    source_types: List[str]
    missing_sources: List[str]
    missing_source_types: List[str]
    expected_fallback: bool
    got_fallback: bool
    elapsed_sec: float
    answer_length: int
    citations_present: bool
    rag_profile: str
    error: str = ""


def load_eval_cases(tool_root: Path) -> List[EvalCase]:
    path = tool_root / "eval" / "golden_set.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError(f"Eval file must contain a list: {path}")
    return [
        EvalCase(
            id=str(row["id"]),
            question=str(row["question"]),
            rag_profile=str(row.get("rag_profile", "full_app_qa")),
            expected_sources=[str(item) for item in row.get("expected_sources", [])],
            expected_source_types=[str(item) for item in row.get("expected_source_types", [])],
            expect_fallback=bool(row.get("expect_fallback", False)),
            notes=str(row.get("notes", "")),
        )
        for row in payload
    ]


def run_eval_set(config: AppConfig, mode: str = "retrieval", limit: int | None = None) -> List[EvalResult]:
    cases = load_eval_cases(config.tool_root)
    if limit is not None:
        cases = cases[:limit]
    if mode not in {"retrieval", "answer"}:
        raise ValueError("mode must be `retrieval` or `answer`.")
    if mode == "answer":
        return [_run_answer_case(config, case) for case in cases]
    return [_run_retrieval_case(config, case) for case in cases]


def summarize_results(results: List[EvalResult]) -> dict[str, Any]:
    passed = sum(1 for result in results if result.passed)
    failed = len(results) - passed
    elapsed = sum(result.elapsed_sec for result in results)
    return {
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / len(results) if results else 0.0,
        "elapsed_sec": elapsed,
    }


def result_to_row(result: EvalResult) -> dict[str, Any]:
    return {
        "id": result.case_id,
        "mode": result.mode,
        "passed": result.passed,
        "rag_profile": result.rag_profile,
        "expected_fallback": result.expected_fallback,
        "got_fallback": result.got_fallback,
        "missing_sources": ", ".join(result.missing_sources),
        "missing_source_types": ", ".join(result.missing_source_types),
        "sources": ", ".join(result.sources[:5]),
        "source_types": ", ".join(result.source_types),
        "answer_length": result.answer_length,
        "citations_present": result.citations_present,
        "elapsed_sec": round(result.elapsed_sec, 3),
        "question": result.question,
        "error": result.error,
    }


def _run_retrieval_case(config: AppConfig, case: EvalCase) -> EvalResult:
    start = time.perf_counter()
    try:
        profile = get_rag_profile(case.rag_profile)
        hits = RetrievalService(config).search_with_profile(case.question, profile=profile, top_k=config.top_k)
        sources = [hit.source_path for hit in hits]
        source_types = sorted({str(hit.metadata.get("source_type", "")) for hit in hits if hit.metadata})
        missing_sources = _missing_expected(sources, case.expected_sources)
        missing_types = _missing_expected(source_types, case.expected_source_types)
        got_fallback = len(hits) < max(config.min_hits, profile.min_hits)
        passed = _is_passed(case, got_fallback, missing_sources, missing_types, mode="retrieval")
        return EvalResult(
            case_id=case.id,
            question=case.question,
            mode="retrieval",
            passed=passed,
            answer="",
            sources=sources,
            source_types=source_types,
            missing_sources=missing_sources,
            missing_source_types=missing_types,
            expected_fallback=case.expect_fallback,
            got_fallback=got_fallback,
            elapsed_sec=time.perf_counter() - start,
            answer_length=0,
            citations_present=bool(sources),
            rag_profile=profile.key,
        )
    except Exception as exc:  # noqa: BLE001
        return _error_result(case, "retrieval", time.perf_counter() - start, str(exc))


def _run_answer_case(config: AppConfig, case: EvalCase) -> EvalResult:
    start = time.perf_counter()
    try:
        result = OracleOrchestrator(config).answer(case.question, requested_rag_profile=case.rag_profile)
        sources = [citation.source_path for citation in result.citations]
        source_types = sorted({citation.source_type for citation in result.citations})
        missing_sources = _missing_expected(sources, case.expected_sources)
        missing_types = _missing_expected(source_types, case.expected_source_types)
        got_fallback = result.answer.strip() == NO_ANSWER
        passed = _is_passed(case, got_fallback, missing_sources, missing_types, mode="answer")
        return EvalResult(
            case_id=case.id,
            question=case.question,
            mode="answer",
            passed=passed,
            answer=result.answer,
            sources=sources,
            source_types=source_types,
            missing_sources=missing_sources,
            missing_source_types=missing_types,
            expected_fallback=case.expect_fallback,
            got_fallback=got_fallback,
            elapsed_sec=time.perf_counter() - start,
            answer_length=len(result.answer),
            citations_present=bool(result.citations),
            rag_profile=result.rag_profile,
        )
    except Exception as exc:  # noqa: BLE001
        return _error_result(case, "answer", time.perf_counter() - start, str(exc))


def _missing_expected(actual_values: List[str], expected_values: List[str]) -> List[str]:
    normalized_actual = [value.lower() for value in actual_values]
    missing: List[str] = []
    for expected in expected_values:
        expected_lower = expected.lower()
        if not any(expected_lower in actual for actual in normalized_actual):
            missing.append(expected)
    return missing


def _is_passed(case: EvalCase, got_fallback: bool, missing_sources: List[str], missing_types: List[str], mode: str) -> bool:
    if case.expect_fallback:
        if mode == "retrieval":
            return True
        return got_fallback
    return not got_fallback and not missing_sources and not missing_types


def _error_result(case: EvalCase, mode: str, elapsed_sec: float, error: str) -> EvalResult:
    return EvalResult(
        case_id=case.id,
        question=case.question,
        mode=mode,
        passed=False,
        answer="",
        sources=[],
        source_types=[],
        missing_sources=case.expected_sources,
        missing_source_types=case.expected_source_types,
        expected_fallback=case.expect_fallback,
        got_fallback=False,
        elapsed_sec=elapsed_sec,
        answer_length=0,
        citations_present=False,
        rag_profile=case.rag_profile,
        error=error,
    )
