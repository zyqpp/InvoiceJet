from __future__ import annotations

import json
from typing import Any, Iterable, List

import requests

from .config import AppConfig


class OllamaError(RuntimeError):
    pass


class OllamaClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def is_online(self, timeout: int = 3) -> tuple[bool, str]:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=timeout)
            response.raise_for_status()
            return True, "Ollama API jest dostępne."
        except Exception as exc:  # noqa: BLE001
            return False, str(exc)

    def list_models(self) -> List[dict[str, Any]]:
        response = requests.get(f"{self.base_url}/api/tags", timeout=10)
        response.raise_for_status()
        payload = response.json()
        return list(payload.get("models", []))

    def pull_model(self, model: str) -> dict[str, Any]:
        response = requests.post(
            f"{self.base_url}/api/pull",
            json={"model": model, "stream": False},
            timeout=7200,
        )
        response.raise_for_status()
        return response.json()

    def embed(self, model: str, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        try:
            return self._embed_batch(model=model, texts=texts)
        except requests.HTTPError:
            return [self._embed_single(model=model, text=text) for text in texts]

    def _embed_batch(self, model: str, texts: List[str]) -> List[List[float]]:
        response = requests.post(
            f"{self.base_url}/api/embed",
            json={"model": model, "input": texts},
            timeout=600,
        )
        response.raise_for_status()
        payload = response.json()
        embeddings = payload.get("embeddings")
        if not isinstance(embeddings, list):
            raise OllamaError("Ollama /api/embed did not return embeddings.")
        return embeddings

    def _embed_single(self, model: str, text: str) -> List[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=600,
        )
        response.raise_for_status()
        payload = response.json()
        embedding = payload.get("embedding")
        if not isinstance(embedding, list):
            raise OllamaError("Ollama /api/embeddings did not return embedding.")
        return embedding

    def generate(
        self,
        model: str,
        prompt: str,
        num_ctx: int,
        temperature: float,
        num_predict: int,
        top_p: float = 0.9,
        llm_top_k: int = 40,
        repeat_penalty: float = 1.1,
        seed: int | None = None,
        timeout_sec: int = 900,
        think: bool | str | None = None,
    ) -> dict[str, Any]:
        options = _generate_options(
            num_ctx=num_ctx,
            temperature=temperature,
            num_predict=num_predict,
            top_p=top_p,
            llm_top_k=llm_top_k,
            repeat_penalty=repeat_penalty,
            seed=seed,
        )
        request_payload: dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }
        if think is not None:
            request_payload["think"] = think
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=request_payload,
            timeout=timeout_sec,
        )
        response.raise_for_status()
        return response.json()

    def generate_stream(
        self,
        model: str,
        prompt: str,
        num_ctx: int,
        temperature: float,
        num_predict: int,
        top_p: float = 0.9,
        llm_top_k: int = 40,
        repeat_penalty: float = 1.1,
        seed: int | None = None,
        timeout_sec: int = 900,
        think: bool | str | None = None,
    ) -> Iterable[dict[str, Any]]:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": True,
            "options": _generate_options(
                num_ctx=num_ctx,
                temperature=temperature,
                num_predict=num_predict,
                top_p=top_p,
                llm_top_k=llm_top_k,
                repeat_penalty=repeat_penalty,
                seed=seed,
            ),
        }
        if think is not None:
            payload["think"] = think
        with requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            stream=True,
            timeout=(10, timeout_sec),
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                if isinstance(line, bytes):
                    line = line.decode("utf-8", errors="replace")
                try:
                    yield json.loads(line)
                except json.JSONDecodeError:
                    continue


def _generate_options(
    num_ctx: int,
    temperature: float,
    num_predict: int,
    top_p: float,
    llm_top_k: int,
    repeat_penalty: float,
    seed: int | None,
) -> dict[str, Any]:
    options: dict[str, Any] = {
        "num_ctx": num_ctx,
        "temperature": temperature,
        "num_predict": num_predict,
        "top_p": top_p,
        "top_k": llm_top_k,
        "repeat_penalty": repeat_penalty,
    }
    if seed is not None:
        options["seed"] = seed
    return options


class OllamaEmbeddingProvider:
    def __init__(self, config: AppConfig, client: OllamaClient | None = None) -> None:
        self.config = config
        self.client = client or OllamaClient(config.ollama_base_url)

    @property
    def model(self) -> str:
        return self.config.embedding_model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.embed(self.model, texts)

    def embed_query(self, text: str) -> List[float]:
        embeddings = self.client.embed(self.model, [text])
        return embeddings[0]

    def dimensions(self) -> int:
        return len(self.embed_query("test"))
