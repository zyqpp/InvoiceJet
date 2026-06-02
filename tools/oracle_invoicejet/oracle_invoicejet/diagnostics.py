from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import sys
from typing import List

from .agent_profiles import list_agent_profiles
from .config import AppConfig, PRESETS
from .documents import discover_documents
from .embeddings import OllamaClient, OllamaEmbeddingProvider


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    message: str


class DoctorService:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.ollama = OllamaClient(config.ollama_base_url)

    def run(self, test_embedding: bool = False) -> List[CheckResult]:
        checks = [
            self._check_python(),
            self._check_repo_root(),
            self._check_tmp_write(),
            self._check_sources(),
            self._check_ollama_cli(),
            self._check_ollama_api(),
            self._check_model_list(),
            self._check_chroma_path(),
        ]
        if test_embedding:
            checks.append(self._check_embedding())
        return checks

    def _check_python(self) -> CheckResult:
        version = sys.version.split()[0]
        return CheckResult("Python", True, f"Python {version}. Zalecane dla zależności: 3.11 albo 3.12.")

    def _check_repo_root(self) -> CheckResult:
        ok = self.config.repo_root.exists()
        return CheckResult("Repo root", ok, str(self.config.repo_root))

    def _check_tmp_write(self) -> CheckResult:
        tmp_dir = self.config.repo_root / ".tmp" / "oracle"
        try:
            tmp_dir.mkdir(parents=True, exist_ok=True)
            test_file = tmp_dir / "write-test.txt"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink(missing_ok=True)
            return CheckResult(".tmp write", True, f"Zapis działa: {tmp_dir}")
        except OSError as exc:
            return CheckResult(".tmp write", False, f"Brak zapisu do {tmp_dir}: {exc}")

    def _check_sources(self) -> CheckResult:
        documents, skipped = discover_documents(self.config)
        ok = len(documents) > 0
        return CheckResult("Źródła dokumentacji", ok, f"Pliki .md: {len(documents)}, pominięte: {skipped}")

    def _check_ollama_cli(self) -> CheckResult:
        path = shutil.which("ollama")
        return CheckResult("Ollama CLI", path is not None, path or "Nie znaleziono `ollama` w PATH.")

    def _check_ollama_api(self) -> CheckResult:
        ok, message = self.ollama.is_online()
        if not ok and "app.log" in message.lower():
            message += " | Możliwy problem uprawnień do logów Ollama na C:\\Users\\kamil\\AppData\\Local\\Ollama."
        return CheckResult("Ollama API", ok, message)

    def _check_model_list(self) -> CheckResult:
        try:
            models = self.ollama.list_models()
        except Exception as exc:  # noqa: BLE001
            return CheckResult("Modele Ollama", False, f"Nie można pobrać listy modeli: {exc}")
        model_names = [str(model.get("name", "")) for model in models]
        available_names = set(model_names)
        for model_name in model_names:
            if model_name.endswith(":latest"):
                available_names.add(model_name.removesuffix(":latest"))
        required = {self.config.llm_model, self.config.embedding_model}
        missing = sorted(required - available_names)
        if missing:
            return CheckResult("Modele Ollama", False, f"Brakuje modeli: {', '.join(missing)}")
        return CheckResult("Modele Ollama", True, f"Dostępne modele: {', '.join(model_names) or 'brak'}")

    def _check_chroma_path(self) -> CheckResult:
        path = self.config.chroma_path
        try:
            path.mkdir(parents=True, exist_ok=True)
            return CheckResult("Chroma path", True, str(path))
        except OSError as exc:
            return CheckResult("Chroma path", False, f"Nie można utworzyć {path}: {exc}")

    def _check_embedding(self) -> CheckResult:
        try:
            dimensions = OllamaEmbeddingProvider(self.config, self.ollama).dimensions()
            return CheckResult("Embedding test", True, f"Model {self.config.embedding_model}, wymiar {dimensions}")
        except Exception as exc:  # noqa: BLE001
            return CheckResult("Embedding test", False, str(exc))


def recommended_models() -> List[str]:
    models: set[str] = set()
    for preset in PRESETS.values():
        models.add(preset.llm_model)
        models.add(preset.embedding_model)
    for profile in list_agent_profiles():
        models.update(profile.required_models)
    return sorted(models)
