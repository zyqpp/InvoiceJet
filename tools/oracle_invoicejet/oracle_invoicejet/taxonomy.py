from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import PurePosixPath
from typing import Iterable


SOURCE_TYPE_BY_SECTION = {
    "01_ekrany": "screen",
    "02_procesy": "process",
    "03_algorytmy": "algorithm",
    "04_api_i_integracje": "api",
    "05_model_danych": "data_model",
    "06_role_i_uprawnienia": "role",
    "07_use_case": "business",
    "08_model_biznesowy": "business",
    "09_procesy_biznesowe": "process",
    "10_testy": "test",
    "_mapowania": "mapping",
}

VALIDATION_MARKERS = {
    "walidacja",
    "walidacje",
    "validation",
    "validator",
    "required",
    "blad",
    "bledy",
    "error",
}

TECHNICAL_STOP_WORDS = {
    "readme",
    "ekran",
    "modal",
    "proces",
    "tc",
    "op",
    "tab",
    "filtr",
    "lista",
    "spis",
    "globalny",
}


@dataclass(frozen=True)
class DocumentTaxonomy:
    source_type: str
    area: str
    entity: str
    screen: str
    process: str
    table: str
    endpoint: str
    knowledge_tags: str

    def as_metadata(self) -> dict[str, str]:
        return {
            "source_type": self.source_type,
            "area": self.area,
            "entity": self.entity,
            "screen": self.screen,
            "process": self.process,
            "table": self.table,
            "endpoint": self.endpoint,
            "knowledge_tags": self.knowledge_tags,
        }


def classify_document(relative_path: str) -> DocumentTaxonomy:
    path = PurePosixPath(relative_path.replace("\\", "/"))
    parts = path.parts
    doc_root_index = _find_doc_root_index(parts)
    section = parts[doc_root_index + 1] if doc_root_index >= 0 and len(parts) > doc_root_index + 1 else ""
    source_type = SOURCE_TYPE_BY_SECTION.get(section, "general")
    if _has_validation_marker(parts):
        source_type = "validation"

    local_parts = parts[doc_root_index + 2 :] if doc_root_index >= 0 else parts
    stem = path.stem
    area = _first_meaningful(local_parts, fallback=section)
    entity = _infer_entity(source_type, local_parts, stem)
    screen = _infer_screen(source_type, section, local_parts, stem)
    process = entity if source_type == "process" else ""
    table = _infer_table(source_type, local_parts, stem)
    endpoint = _infer_endpoint(source_type, stem)
    tags = _build_tags(source_type, section, area, entity, table, endpoint, parts)

    return DocumentTaxonomy(
        source_type=source_type,
        area=area,
        entity=entity,
        screen=screen,
        process=process,
        table=table,
        endpoint=endpoint,
        knowledge_tags=",".join(tags),
    )


def _find_doc_root_index(parts: tuple[str, ...]) -> int:
    for index, part in enumerate(parts):
        if part in {"doc_AI", "doc_user"}:
            return index
    return -1


def _has_validation_marker(parts: Iterable[str]) -> bool:
    normalized = " ".join(_normalize(part) for part in parts)
    return any(marker in normalized for marker in VALIDATION_MARKERS)


def _first_meaningful(parts: tuple[str, ...], fallback: str) -> str:
    for part in parts:
        value = _strip_number_prefix(PurePosixPath(part).stem)
        if value and value.lower() not in TECHNICAL_STOP_WORDS:
            return value
    return _strip_number_prefix(fallback)


def _infer_entity(source_type: str, local_parts: tuple[str, ...], stem: str) -> str:
    if source_type == "api":
        if len(local_parts) >= 2:
            return _strip_number_prefix(local_parts[-2])
        return _strip_number_prefix(stem)
    if source_type == "data_model":
        return _strip_number_prefix(_table_name_from_stem(stem))
    if source_type in {"screen", "validation"}:
        if len(local_parts) >= 2:
            return _strip_number_prefix(local_parts[-2])
        return _strip_number_prefix(stem)
    if source_type == "mapping":
        return _strip_number_prefix(stem)
    return _first_meaningful(local_parts, fallback=stem)


def _infer_screen(source_type: str, section: str, local_parts: tuple[str, ...], stem: str) -> str:
    if source_type not in {"screen", "validation"} or section != "01_ekrany":
        return ""
    if len(local_parts) >= 2:
        return str(local_parts[-2])
    return stem


def _infer_table(source_type: str, local_parts: tuple[str, ...], stem: str) -> str:
    if source_type != "data_model":
        return ""
    if any(part.lower() == "dbo" for part in local_parts):
        return _table_name_from_stem(stem)
    return _strip_number_prefix(_table_name_from_stem(stem))


def _infer_endpoint(source_type: str, stem: str) -> str:
    if source_type != "api":
        return ""
    match = re.match(r"^(GET|POST|PUT|PATCH|DELETE)_(.+)$", stem, flags=re.IGNORECASE)
    if not match:
        return _strip_number_prefix(stem)
    method = match.group(1).upper()
    name = match.group(2).replace("_", "/")
    return f"{method} {name}"


def _build_tags(
    source_type: str,
    section: str,
    area: str,
    entity: str,
    table: str,
    endpoint: str,
    parts: tuple[str, ...],
) -> list[str]:
    tags = [source_type]
    for value in [section, area, entity, table, endpoint]:
        normalized = _normalize(value)
        if normalized:
            tags.append(normalized)
    if _has_validation_marker(parts):
        tags.append("validation")
    return list(dict.fromkeys(tags))


def _table_name_from_stem(stem: str) -> str:
    if stem.startswith("dbo."):
        return stem
    if "." in stem:
        return stem.split(".")[-1]
    return stem


def _strip_number_prefix(value: str) -> str:
    value = re.sub(r"^\d+[_-]+", "", value)
    value = re.sub(r"^[A-Z]-\d+[_-]+", "", value, flags=re.IGNORECASE)
    return value.strip("_- ")


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9_./ -]+", "", value.lower()).strip()
