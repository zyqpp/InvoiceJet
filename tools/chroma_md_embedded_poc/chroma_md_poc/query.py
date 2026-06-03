from __future__ import annotations

import argparse
from typing import Optional

import chromadb

from chroma_md_poc.config import load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run semantic query against embedded Chroma markdown collection.")
    parser.add_argument("--q", required=True, help="Question / search query text.")
    parser.add_argument("--top-k", type=int, default=None, help="Number of top results to return.")
    parser.add_argument(
        "--source-contains",
        default=None,
        help="Optional path substring filter (case-sensitive) for source_path metadata.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config()
    top_k = args.top_k or config.top_k

    client = chromadb.PersistentClient(path=str(config.chroma_path))
    collection = client.get_collection(name=config.collection_name)

    query_limit = top_k * 5 if args.source_contains else top_k
    result = collection.query(
        query_texts=[args.q],
        n_results=query_limit,
    )

    rows = list(
        zip(
            result.get("ids", [[]])[0],
            result.get("documents", [[]])[0],
            result.get("metadatas", [[]])[0],
            result.get("distances", [[]])[0],
        )
    )
    if args.source_contains:
        rows = [
            row
            for row in rows
            if row[2] and args.source_contains in str(row[2].get("source_path", ""))
        ]
    rows = rows[:top_k]

    print("=== Query Results ===")
    print(f"Query          : {args.q}")
    print(f"Collection     : {config.collection_name}")
    print(f"Top K          : {top_k}")
    print(f"Filter         : {args.source_contains or '-'}")
    print(f"Hits returned  : {len(rows)}")
    print()

    for i, (doc_id, document, metadata, distance) in enumerate(rows, start=1):
        source_path = metadata.get("source_path", "-") if metadata else "-"
        heading = metadata.get("heading", "ROOT") if metadata else "ROOT"
        preview = (document or "").replace("\n", " ").strip()
        if len(preview) > 300:
            preview = preview[:300] + "..."

        print(f"[{i}] distance={distance:.6f}")
        print(f"    id         : {doc_id}")
        print(f"    source     : {source_path}")
        print(f"    heading    : {heading}")
        print(f"    excerpt    : {preview}")
        print()


if __name__ == "__main__":
    main()
