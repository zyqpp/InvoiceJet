from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys

from .config import load_config
from .diagnostics import DoctorService, recommended_models


def doctor_main() -> None:
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
    for warning in stats.warnings:
        print(f"[WARN] {warning}")


def query_main() -> None:
    from .agents import OracleOrchestrator
    from .rag import NO_ANSWER

    parser = argparse.ArgumentParser(description="Zadaje pytanie do Oracle InvoiceJet.")
    parser.add_argument("question", nargs="+", help="Pytanie do dokumentacji.")
    parser.add_argument("--scope", default=None, help="Zakres: full, technical, user, backend, frontend, debt.")
    args = parser.parse_args()
    result = OracleOrchestrator(load_config()).answer(" ".join(args.question), requested_scope=args.scope)
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
    print(f"\nZakres: {result.scope} | verified={result.verified}")


def evaluate_main() -> None:
    from .retrieval import RetrievalService

    parser = argparse.ArgumentParser(description="Uruchamia podstawowe pytania kontrolne retrievalu.")
    parser.add_argument("--top-k", type=int, default=None)
    args = parser.parse_args()
    config = load_config()
    service = RetrievalService(config)
    questions = [
        "Jak działa logowanie użytkownika?",
        "Jak generowany jest PDF dokumentu?",
        "Jak działa integracja z ANAF?",
        "Jakie są krytyczne elementy długu technicznego?",
        "Jaka jest struktura dokumentacji technicznej?",
    ]
    for question in questions:
        hits = service.search(question, top_k=args.top_k or config.top_k)
        print(f"\n## {question}")
        print(f"Hits: {len(hits)}")
        for hit in hits[:3]:
            print(f"- {hit.source_path} | {hit.metadata.get('heading_path', 'ROOT')} | distance={hit.distance:.6f}")


def serve_main() -> None:
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
