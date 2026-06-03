from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
from typing import Iterable, List, Tuple

from chroma_md_poc.config import AppConfig


HEADING_RE = re.compile(r"^(#{1,3})\s+(.+?)\s*$")


@dataclass
class MarkdownChunk:
    chunk_id: str
    text: str
    heading: str
    chunk_index: int
    char_start: int
    char_end: int


def normalize_markdown(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalized.startswith("\ufeff"):
        normalized = normalized[1:]
    return normalized


def read_markdown(path: Path) -> str:
    return normalize_markdown(path.read_text(encoding="utf-8"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def discover_markdown_files(config: AppConfig) -> Tuple[List[Path], int]:
    files = set()
    skipped = 0
    for pattern in config.include_globs:
        for candidate in config.project_root.rglob(pattern):
            if not candidate.is_file():
                continue
            lower_parts = [part.lower() for part in candidate.parts]
            if any(excluded in lower_parts for excluded in config.exclude_dirs):
                skipped += 1
                continue
            files.add(candidate.resolve())
    return sorted(files), skipped


def split_sections(text: str) -> List[Tuple[int, int, str]]:
    lines = text.splitlines(keepends=True)
    if not lines:
        return [(0, 0, "ROOT")]

    sections: List[Tuple[int, int, str]] = []
    cursor = 0
    section_start = 0
    current_heading = "ROOT"

    for line in lines:
        match = HEADING_RE.match(line.strip())
        if match and cursor != 0:
            sections.append((section_start, cursor, current_heading))
            section_start = cursor
            current_heading = match.group(2).strip()
        elif match and cursor == 0:
            current_heading = match.group(2).strip()
        cursor += len(line)

    sections.append((section_start, len(text), current_heading))
    return sections


def _split_fixed_size(
    text: str,
    base_start: int,
    heading: str,
    chunk_size: int,
    overlap: int,
    start_index: int,
    rel_path: str,
) -> List[MarkdownChunk]:
    chunks: List[MarkdownChunk] = []
    if not text.strip():
        return chunks

    step = chunk_size - overlap
    if step <= 0:
        step = chunk_size

    chunk_index = start_index
    for offset in range(0, len(text), step):
        window = text[offset : offset + chunk_size]
        if not window.strip():
            continue
        char_start = base_start + offset
        char_end = min(base_start + offset + len(window), base_start + len(text))
        chunk_id = f"{rel_path}::{chunk_index:06d}"
        chunks.append(
            MarkdownChunk(
                chunk_id=chunk_id,
                text=window,
                heading=heading or "ROOT",
                chunk_index=chunk_index,
                char_start=char_start,
                char_end=char_end,
            )
        )
        chunk_index += 1
        if offset + chunk_size >= len(text):
            break
    return chunks


def chunk_markdown(rel_path: str, text: str, chunk_size: int, overlap: int) -> List[MarkdownChunk]:
    sections = split_sections(text)
    chunks: List[MarkdownChunk] = []
    chunk_index = 0

    for start, end, heading in sections:
        section_text = text[start:end]
        section_chunks = _split_fixed_size(
            text=section_text,
            base_start=start,
            heading=heading,
            chunk_size=chunk_size,
            overlap=overlap,
            start_index=chunk_index,
            rel_path=rel_path,
        )
        chunks.extend(section_chunks)
        chunk_index += len(section_chunks)
    return chunks


def batched(items: List[str], batch_size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), batch_size):
        yield items[i : i + batch_size]

