from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
from typing import Dict, List


ENV_PREFIX = "ORACLE_"
MANIFEST_SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ModelPreset:
    name: str
    label: str
    llm_model: str
    embedding_model: str
    top_k: int
    num_ctx: int
    temperature: float
    num_predict: int


@dataclass(frozen=True)
class SourceConfig:
    source_group: str
    audience: str
    priority: int
    relative_path: str


@dataclass(frozen=True)
class AppConfig:
    tool_root: Path
    repo_root: Path
    chroma_path: Path
    manifest_path: Path
    collection_name: str
    ollama_base_url: str
    llm_model: str
    embedding_model: str
    top_k: int
    num_ctx: int
    temperature: float
    num_predict: int
    chunk_size: int
    chunk_overlap: int
    batch_size: int
    min_hits: int
    sources: List[SourceConfig]
    exclude_dirs: List[str]
    allowed_models: List[str]


PRESETS: Dict[str, ModelPreset] = {
    "rtx2060": ModelPreset(
        name="rtx2060",
        label="RTX 2060 6GB",
        llm_model="gemma3:4b",
        embedding_model="bge-m3",
        top_k=5,
        num_ctx=8192,
        temperature=0.1,
        num_predict=512,
    ),
    "light": ModelPreset(
        name="light",
        label="Tryb lekki",
        llm_model="gemma3:1b",
        embedding_model="bge-m3",
        top_k=4,
        num_ctx=4096,
        temperature=0.1,
        num_predict=384,
    ),
}


DEFAULT_SOURCES: List[SourceConfig] = [
    SourceConfig("doc_ai", "technical", 100, "InvoiceJet/doc_AI"),
    SourceConfig("doc_user", "user", 70, "InvoiceJet/doc_user"),
]


def _load_dotenv(dotenv_path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not dotenv_path.exists():
        return values
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'").strip('"')
    return values


def _as_list(value: str) -> List[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _read_var(name: str, default: str, dotenv_values: Dict[str, str]) -> str:
    env_name = f"{ENV_PREFIX}{name}"
    if env_name in os.environ:
        return os.environ[env_name]
    if env_name in dotenv_values:
        return dotenv_values[env_name]
    return default


def load_config() -> AppConfig:
    tool_root = Path(__file__).resolve().parents[1]
    repo_root_default = tool_root.parents[1]
    dotenv_values = _load_dotenv(tool_root / ".env")
    preset_name = _read_var("MODEL_PRESET", "rtx2060", dotenv_values).lower()
    preset = PRESETS.get(preset_name, PRESETS["rtx2060"])

    repo_root_value = Path(_read_var("REPO_ROOT", str(repo_root_default), dotenv_values))
    repo_root = (repo_root_value if repo_root_value.is_absolute() else tool_root / repo_root_value).resolve()
    chroma_path = (tool_root / _read_var("CHROMA_PATH", "./chroma_data", dotenv_values)).resolve()
    manifest_path = (tool_root / _read_var("MANIFEST_PATH", "./index_manifest.json", dotenv_values)).resolve()
    collection_name = _read_var("COLLECTION_NAME", "oracle_invoicejet_docs", dotenv_values)
    ollama_base_url = _read_var("OLLAMA_BASE_URL", "http://127.0.0.1:11434", dotenv_values).rstrip("/")

    llm_model = _read_var("LLM_MODEL", preset.llm_model, dotenv_values)
    embedding_model = _read_var("EMBEDDING_MODEL", preset.embedding_model, dotenv_values)
    top_k = int(_read_var("TOP_K", str(preset.top_k), dotenv_values))
    num_ctx = int(_read_var("NUM_CTX", str(preset.num_ctx), dotenv_values))
    temperature = float(_read_var("TEMPERATURE", str(preset.temperature), dotenv_values))
    num_predict = int(_read_var("NUM_PREDICT", str(preset.num_predict), dotenv_values))

    chunk_size = int(_read_var("CHUNK_SIZE", "1800", dotenv_values))
    chunk_overlap = int(_read_var("CHUNK_OVERLAP", "250", dotenv_values))
    batch_size = int(_read_var("BATCH_SIZE", "24", dotenv_values))
    min_hits = int(_read_var("MIN_HITS", "1", dotenv_values))
    exclude_dirs = [item.lower() for item in _as_list(_read_var(
        "EXCLUDE_DIRS",
        ".git,node_modules,bin,obj,.venv,venv,chroma_data,.tmp,archiwum,_site,models,__pycache__",
        dotenv_values,
    ))]
    allowed_models = _as_list(_read_var(
        "ALLOWED_MODELS",
        "gemma3:4b,gemma3:1b,qwen3:4b,qwen3:1.7b,bge-m3,nomic-embed-text",
        dotenv_values,
    ))

    if chunk_overlap >= chunk_size:
        raise ValueError("ORACLE_CHUNK_OVERLAP must be smaller than ORACLE_CHUNK_SIZE.")
    if not repo_root.exists():
        raise ValueError(f"Repo root does not exist: {repo_root}")
    if top_k <= 0 or batch_size <= 0 or min_hits <= 0:
        raise ValueError("ORACLE_TOP_K, ORACLE_BATCH_SIZE and ORACLE_MIN_HITS must be positive.")

    return AppConfig(
        tool_root=tool_root,
        repo_root=repo_root,
        chroma_path=chroma_path,
        manifest_path=manifest_path,
        collection_name=collection_name,
        ollama_base_url=ollama_base_url,
        llm_model=llm_model,
        embedding_model=embedding_model,
        top_k=top_k,
        num_ctx=num_ctx,
        temperature=temperature,
        num_predict=num_predict,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        batch_size=batch_size,
        min_hits=min_hits,
        sources=DEFAULT_SOURCES,
        exclude_dirs=exclude_dirs,
        allowed_models=allowed_models,
    )
