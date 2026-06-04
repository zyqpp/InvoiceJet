from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .config import load_config
from .diagnostics import DoctorService, recommended_models


def _configure_console_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def doctor_main() -> None:
    _configure_console_encoding()
    parser = argparse.ArgumentParser(description="Sprawdza środowisko Oracle InvoiceJet.")
    parser.add_argument("--test-embedding", action="store_true", help="Wykonaj test embeddingu przez Ollama.")
    args = parser.parse_args()
    config = load_config()
    checks = DoctorService(config).run(test_embedding=args.test_embedding)
    for check in checks:
        status = "OK" if check.ok else "FAIL"
        print(f"[{status}] {check.name}: {check.message}")
    print("Rekomendowane modele:", ", ".join(recommended_models()))


def ingest_main() -> None:
    _configure_console_encoding()
    from .indexing import IndexManager

    parser = argparse.ArgumentParser(description="Indeksuje dokumentację InvoiceJet do lokalnego Chroma.")
    parser.add_argument("--force-rebuild", action="store_true", help="Usuń kolekcję i zbuduj indeks od nowa.")
    args = parser.parse_args()
    stats = IndexManager(load_config()).run_ingest(force_rebuild=args.force_rebuild)
    print("=== Oracle Ingest Report ===")
    print(f"Files discovered   : {stats.files_discovered}")
    print(f"Files skipped      : {stats.files_skipped}")
    print(f"Files changed      : {stats.files_changed}")
    print(f"Files unchanged    : {stats.files_unchanged}")
    print(f"Files deleted      : {stats.files_deleted}")
    print(f"Chunks upserted    : {stats.chunks_upserted}")
    print(f"Chunks deleted     : {stats.chunks_deleted}")
    print(f"Read errors        : {stats.read_errors}")
    print(f"Collection records : {stats.collection_records}")
    print(f"Elapsed seconds    : {stats.elapsed_seconds:.2f}")
    if stats.source_counts:
        print("Source groups      :", ", ".join(f"{key}={value}" for key, value in sorted(stats.source_counts.items())))
    if stats.source_type_counts:
        print("Source types       :", ", ".join(f"{key}={value}" for key, value in sorted(stats.source_type_counts.items())))
    for warning in stats.warnings:
        print(f"[WARN] {warning}")


def query_main() -> None:
    _configure_console_encoding()
    from .agents import OracleOrchestrator
    from .rag import NO_ANSWER

    parser = argparse.ArgumentParser(description="Zadaje pytanie do Oracle InvoiceJet.")
    parser.add_argument("question", nargs="+", help="Pytanie do dokumentacji.")
    parser.add_argument("--scope", default=None, help="Zakres: full, technical, user, backend, frontend, debt.")
    parser.add_argument("--rag-profile", default=None, help="Profil RAG: full_app_qa, cross_reference, technical_deep_dive, database_sql, user_help.")
    parser.add_argument("--prompt-profile", default=None, help="Profil promptu z katalogu profiles.")
    args = parser.parse_args()
    result = OracleOrchestrator(load_config()).answer(
        " ".join(args.question),
        requested_scope=args.scope,
        requested_rag_profile=args.rag_profile,
        prompt_profile_key=args.prompt_profile,
    )
    print(result.answer)
    if result.answer.strip() == NO_ANSWER and not result.citation_lines and not result.warnings:
        return
    if result.warnings:
        print("\nOstrzeżenia:")
        for warning in result.warnings:
            print(f"- {warning}")
    if result.citation_lines:
        print("\nŹródła systemowe:")
        for citation in result.citation_lines:
            print(f"- {citation}")
    print(f"\nZakres: {result.scope} | RAG={result.rag_profile} | prompt={result.prompt_profile} | verified={result.verified}")
    if result.stats:
        print("Metryki:")
        for key, value in result.stats.items():
            print(f"- {key}: {value}")


def evaluate_main() -> None:
    _configure_console_encoding()
    from .evaluation import result_to_row, run_eval_set, summarize_results

    parser = argparse.ArgumentParser(description="Uruchamia golden set Oracle InvoiceJet.")
    parser.add_argument("--mode", choices=["retrieval", "answer"], default="retrieval")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--json", action="store_true", help="Wypisz raport jako JSON.")
    args = parser.parse_args()
    config = load_config()
    results = run_eval_set(config, mode=args.mode, limit=args.limit)
    summary = summarize_results(results)
    rows = [result_to_row(result) for result in results]
    if args.json:
        print(json.dumps({"summary": summary, "results": rows}, ensure_ascii=False, indent=2))
        return
    print("=== Oracle Evaluation Lab ===")
    print(f"Mode      : {args.mode}")
    print(f"Total     : {summary['total']}")
    print(f"Passed    : {summary['passed']}")
    print(f"Failed    : {summary['failed']}")
    print(f"Pass rate : {summary['pass_rate']:.0%}")
    print(f"Elapsed   : {summary['elapsed_sec']:.2f}s")
    for row in rows:
        status = "OK" if row["passed"] else "FAIL"
        print(f"\n[{status}] {row['id']} | {row['rag_profile']} | {row['elapsed_sec']}s")
        print(row["question"])
        if row["missing_sources"]:
            print(f"Missing sources: {row['missing_sources']}")
        if row["missing_source_types"]:
            print(f"Missing source types: {row['missing_source_types']}")
        if row["error"]:
            print(f"Error: {row['error']}")


def serve_main() -> None:
    _configure_console_encoding()
    parser = argparse.ArgumentParser(description="Uruchamia portal Streamlit Oracle InvoiceJet.")
    parser.add_argument("--port", type=int, default=8502)
    args = parser.parse_args()
    app_path = Path(__file__).resolve().parent / "ui.py"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port",
            str(args.port),
            "--server.address",
            "127.0.0.1",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ],
        check=True,
    )


def pull_recommended_main() -> None:
    _configure_console_encoding()
    from .embeddings import OllamaClient

    parser = argparse.ArgumentParser(description="Pobiera wyłącznie rekomendowane modele Oracle.")
    parser.add_argument("models", nargs="*", help="Modele z whitelisty do pobrania. Domyślnie wszystkie.")
    args = parser.parse_args()
    config = load_config()
    allowed = set(config.allowed_models)
    selected = args.models or recommended_models()
    client = OllamaClient(config.ollama_base_url)
    for model in selected:
        if model not in allowed:
            raise SystemExit(f"Model spoza whitelisty Oracle: {model}")
        print(f"Pobieram {model}...")
        print(client.pull_model(model))
