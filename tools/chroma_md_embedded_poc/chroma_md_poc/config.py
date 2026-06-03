from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from typing import Dict, List


ENV_PREFIX = "CHROMA_POC_"


def _load_dotenv(dotenv_path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not dotenv_path.exists():
        return values

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            values[key] = value
    return values


def _as_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class AppConfig:
    project_root: Path
    chroma_path: Path
    collection_name: str
    include_globs: List[str]
    exclude_dirs: List[str]
    chunk_size: int
    chunk_overlap: int
    top_k: int
    batch_size: int
    manifest_path: Path
    module_root: Path


def load_config() -> AppConfig:
    module_root = Path(__file__).resolve().parents[1]
    dotenv_values = _load_dotenv(module_root / ".env")

    def read_var(name: str, default: str) -> str:
        env_name = f"{ENV_PREFIX}{name}"
        if env_name in os.environ:
            return os.environ[env_name]
        if env_name in dotenv_values:
            return dotenv_values[env_name]
        return default

    project_root = (module_root / read_var("PROJECT_ROOT", "../../")).resolve()
    chroma_path = (module_root / read_var("CHROMA_PATH", "./chroma_data")).resolve()
    collection_name = read_var("COLLECTION_NAME", "invoicejet_md_docs")
    include_globs = _as_list(read_var("INCLUDE_GLOBS", "*.md,*.MD"))
    exclude_dirs = [item.lower() for item in _as_list(read_var("EXCLUDE_DIRS", ".git,node_modules,bin,obj,.venv,venv,chroma_data,.tmp"))]
    chunk_size = int(read_var("CHUNK_SIZE", "1800"))
    chunk_overlap = int(read_var("CHUNK_OVERLAP", "250"))
    top_k = int(read_var("TOP_K", "5"))
    batch_size = int(read_var("BATCH_SIZE", "64"))
    manifest_path = module_root / "index_manifest.json"

    if chunk_size <= 0:
        raise ValueError("CHROMA_POC_CHUNK_SIZE must be > 0.")
    if chunk_overlap < 0:
        raise ValueError("CHROMA_POC_CHUNK_OVERLAP must be >= 0.")
    if chunk_overlap >= chunk_size:
        raise ValueError("CHROMA_POC_CHUNK_OVERLAP must be < CHROMA_POC_CHUNK_SIZE.")
    if top_k <= 0:
        raise ValueError("CHROMA_POC_TOP_K must be > 0.")
    if batch_size <= 0:
        raise ValueError("CHROMA_POC_BATCH_SIZE must be > 0.")
    if not project_root.exists():
        raise ValueError(f"Project root does not exist: {project_root}")

    return AppConfig(
        project_root=project_root,
        chroma_path=chroma_path,
        collection_name=collection_name,
        include_globs=include_globs,
        exclude_dirs=exclude_dirs,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        top_k=top_k,
        batch_size=batch_size,
        manifest_path=manifest_path,
        module_root=module_root,
    )
