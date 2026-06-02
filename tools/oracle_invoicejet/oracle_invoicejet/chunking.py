from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import Iterable, List

from .documents import SourceDocument


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class MarkdownChunk:
    chunk_id: str
    text: str
    heading: str
    heading_path: str
    chunk_index: int
    char_start: int
    char_end: int


@dataclass(frozen=True)
class MarkdownSection:
    start: int
    end: int
    heading: str
    heading_path: str


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_sections(text: str) -> List[MarkdownSection]:
    lines = text.splitlines(keepends=True)
    if not lines:
        return [MarkdownSection(0, 0, "ROOT", "ROOT")]

    sections: List[MarkdownSection] = []
    heading_stack: List[str] = []
    current_heading = "ROOT"
    current_path = "ROOT"
    section_start = 0
    cursor = 0

    for line in lines:
        match = HEADING_RE.match(line.strip())
        if match:
            if cursor > section_start:
                sections.append(MarkdownSection(section_start, cursor, current_heading, current_path))
            level = len(match.group(1))
            title = match.group(2).strip()
            heading_stack = heading_stack[: level - 1]
            heading_stack.append(title)
            current_heading = title
            current_path = " > ".join(heading_stack)
            section_start = cursor
        cursor += len(line)

    sections.append(MarkdownSection(section_start, len(text), current_heading, current_path))
    return sections


def chunk_markdown(document: SourceDocument, text: str, chunk_size: int, overlap: int) -> List[MarkdownChunk]:
    chunks: List[MarkdownChunk] = []
    chunk_index = 0
    for section in split_sections(text):
        section_text = text[section.start : section.end]
        for chunk in _split_fixed_size(
            document=document,
            text=section_text,
            base_start=section.start,
            heading=section.heading,
            heading_path=section.heading_path,
            chunk_size=chunk_size,
            overlap=overlap,
            start_index=chunk_index,
        ):
            chunks.append(chunk)
            chunk_index += 1
    return chunks


def _split_fixed_size(
    document: SourceDocument,
    text: str,
    base_start: int,
    heading: str,
    heading_path: str,
    chunk_size: int,
    overlap: int,
    start_index: int,
) -> Iterable[MarkdownChunk]:
    if not text.strip():
        return
    step = max(chunk_size - overlap, 1)
    chunk_index = start_index
    for offset in range(0, len(text), step):
        window = text[offset : offset + chunk_size]
        if not window.strip():
            continue
        char_start = base_start + offset
        char_end = min(base_start + offset + len(window), base_start + len(text))
        yield MarkdownChunk(
            chunk_id=f"{document.relative_path}::{chunk_index:06d}",
            text=window,
            heading=heading or "ROOT",
            heading_path=heading_path or "ROOT",
            chunk_index=chunk_index,
            char_start=char_start,
            char_end=char_end,
        )
        chunk_index += 1
        if offset + chunk_size >= len(text):
            break

