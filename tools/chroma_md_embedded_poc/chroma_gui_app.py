from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import subprocess
from typing import Any

from huggingface_hub import hf_hub_download
import requests
import streamlit as st

from chroma_md_poc.config import load_config
from chroma_md_poc.rag import OLLAMA_BASE_URL, query_rows, stream_rag_answer


def _ensure_local_dirs(module_dir: Path) -> tuple[Path, Path]:
    hf_dir = module_dir / "models" / "hf_gguf"
    modelfiles_dir = module_dir / "models" / "modelfiles"
    hf_dir.mkdir(parents=True, exist_ok=True)
    modelfiles_dir.mkdir(parents=True, exist_ok=True)
    return hf_dir, modelfiles_dir


def _load_agent_manual(module_dir: Path) -> str:
    manual_path = module_dir / "AGENT_AI_USER_MANUAL_PL.md"
    if not manual_path.exists():
        return "Brak pliku manuala Agent AI."
    return manual_path.read_text(encoding="utf-8")


def _bytes_to_human(value: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(value)
    unit = units[0]
    for unit in units:
        if size < 1024.0:
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"


def _is_ollama_online() -> tuple[bool, str]:
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=3)
        response.raise_for_status()
        return True, "Ollama API jest dostepne."
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def _ollama_list_models() -> list[dict[str, Any]]:
    response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
    response.raise_for_status()
    payload = response.json()
    return list(payload.get("models", []))


def _ollama_pull(model_name: str) -> dict[str, Any]:
    response = requests.post(
        f"{OLLAMA_BASE_URL}/api/pull",
        json={"model": model_name, "stream": False},
        timeout=7200,
    )
    response.raise_for_status()
    return response.json()


def _sanitize_model_name(name: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_.:-]+", "-", name.strip())
    return sanitized.strip("-").lower()


def _download_gguf_from_hf(hf_dir: Path, repo_id: str, filename: str, hf_token: str) -> Path:
    target_dir = hf_dir / repo_id.replace("/", "__")
    target_dir.mkdir(parents=True, exist_ok=True)
    token: str | None = hf_token.strip() or None
    downloaded_path = hf_hub_download(
        repo_id=repo_id.strip(),
        filename=filename.strip(),
        local_dir=str(target_dir),
        token=token,
    )
    return Path(downloaded_path).resolve()


def _create_ollama_model_from_gguf(
    modelfiles_dir: Path,
    model_name: str,
    gguf_path: Path,
    num_ctx: int,
    temperature: float,
) -> str:
    modelfile_path = modelfiles_dir / f"{model_name.replace(':', '__')}.Modelfile"
    modelfile_text = "\n".join(
        [
            f"FROM {gguf_path}",
            f"PARAMETER num_ctx {num_ctx}",
            f"PARAMETER temperature {temperature}",
            "",
        ]
    )
    modelfile_path.write_text(modelfile_text, encoding="utf-8")

    proc = subprocess.run(
        ["ollama", "create", model_name, "-f", str(modelfile_path)],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip() or "ollama create failed")
    return (proc.stdout or "").strip()


def _render_search_tab(config) -> None:
    col1, col2 = st.columns([2, 1])
    with col1:
        question = st.text_area(
            "Pytanie",
            placeholder="Np. jaki blad dostane przy logowaniu gdy email nie istnieje?",
            height=100,
            key="search_question",
        )
    with col2:
        top_k = st.number_input("Top K", min_value=1, max_value=20, value=int(config.top_k), step=1, key="search_topk")
        source_contains = st.text_input("Filtr source_path zawiera", value="", key="search_filter")

    if not st.button("Szukaj", type="primary", key="search_button"):
        return

    if not question.strip():
        st.warning("Wpisz pytanie.")
        return

    try:
        rows = query_rows(question=question.strip(), top_k=int(top_k), source_contains=source_contains.strip())
    except Exception as exc:  # noqa: BLE001
        st.error(f"Blad zapytania: {exc}")
        return

    st.success(f"Znaleziono {len(rows)} wynikow.")
    for idx, (doc_id, document, metadata, distance) in enumerate(rows, start=1):
        source_path = metadata.get("source_path", "-") if metadata else "-"
        heading = metadata.get("heading", "ROOT") if metadata else "ROOT"
        st.markdown(f"### {idx}. distance={distance:.6f}")
        st.markdown(f"**source**: `{source_path}`")
        st.markdown(f"**heading**: `{heading}`")
        st.markdown(f"**id**: `{doc_id}`")
        st.code((document or "").strip(), language="markdown")
        st.divider()


def _render_model_manager_tab(hf_dir: Path, modelfiles_dir: Path) -> list[dict[str, Any]]:
    st.subheader("Modele lokalne i zarzadzanie")

    ollama_online, ollama_status = _is_ollama_online()
    if ollama_online:
        st.success(ollama_status)
    else:
        st.error("Ollama API jest niedostepne. Uruchom Ollama (`ollama serve`) i odswiez. " f"Szczegoly: {ollama_status}")

    models: list[dict[str, Any]] = []
    if ollama_online:
        try:
            models = _ollama_list_models()
        except Exception as exc:  # noqa: BLE001
            st.warning(f"Nie udalo sie pobrac listy modeli: {exc}")

    with st.expander("1) Pobieranie modeli z biblioteki Ollama", expanded=True):
        pull_name = st.text_input(
            "Nazwa modelu do pobrania (np. qwen2.5:3b-instruct, llama3.2:3b)",
            value="",
            key="pull_model_name",
            help="Podaj nazwe modelu z biblioteki Ollama.",
        )
        if st.button("Pobierz model przez Ollama", key="pull_model_button", help="Pobiera model do lokalnego Ollama."):
            if not pull_name.strip():
                st.warning("Podaj nazwe modelu.")
            elif not ollama_online:
                st.error("Ollama nie jest online.")
            else:
                with st.spinner(f"Pobieram model {pull_name.strip()}..."):
                    try:
                        result = _ollama_pull(pull_name.strip())
                        st.success(f"Pobieranie zakonczone: {result}")
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Blad pobierania: {exc}")

    with st.expander("2) Import GGUF z Hugging Face do Ollama", expanded=False):
        col_a, col_b = st.columns(2)
        with col_a:
            hf_repo = st.text_input(
                "HF repo_id",
                value="bartowski/Llama-3.2-3B-Instruct-GGUF",
                key="hf_repo_id",
                help="Repozytorium modelu GGUF na Hugging Face.",
            )
            hf_filename = st.text_input(
                "Nazwa pliku GGUF",
                value="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
                key="hf_filename",
                help="Dokladna nazwa pliku .gguf.",
            )
        with col_b:
            ollama_model_name = st.text_input(
                "Nazwa modelu w Ollama",
                value="invoicejet-llama3.2-3b-q4",
                key="hf_ollama_model_name",
                help="Lokalna nazwa modelu po imporcie do Ollama.",
            )
            hf_token = st.text_input(
                "Hugging Face token (opcjonalnie, dla prywatnych modeli)",
                value="",
                type="password",
                key="hf_token",
                help="Wymagany dla prywatnych repozytoriow.",
            )

        if st.button(
            "Pobierz GGUF z Hugging Face",
            key="download_gguf_button",
            help="Pobiera GGUF do tools/chroma_md_embedded_poc/models/hf_gguf.",
        ):
            if not hf_repo.strip() or not hf_filename.strip():
                st.warning("Uzupelnij repo_id i nazwe pliku.")
            else:
                with st.spinner("Pobieram plik GGUF z Hugging Face..."):
                    try:
                        gguf_path = _download_gguf_from_hf(hf_dir, hf_repo, hf_filename, hf_token)
                        st.session_state["last_downloaded_gguf"] = str(gguf_path)
                        st.success(f"Pobrano: {gguf_path}")
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"Blad pobierania GGUF: {exc}")

        last_gguf = st.session_state.get("last_downloaded_gguf", "")
        if last_gguf:
            st.info(f"Ostatnio pobrany GGUF: {last_gguf}")

        if st.button(
            "Utworz model Ollama z pobranego GGUF",
            key="create_ollama_model_button",
            help="Tworzy model Ollama na bazie ostatnio pobranego GGUF.",
        ):
            if not ollama_online:
                st.error("Ollama nie jest online.")
            elif not last_gguf:
                st.warning("Najpierw pobierz plik GGUF.")
            else:
                model_name = _sanitize_model_name(ollama_model_name or "")
                if not model_name:
                    st.warning("Podaj poprawna nazwe modelu Ollama.")
                else:
                    with st.spinner(f"Tworze model Ollama: {model_name} ..."):
                        try:
                            output = _create_ollama_model_from_gguf(
                                modelfiles_dir=modelfiles_dir,
                                model_name=model_name,
                                gguf_path=Path(last_gguf),
                                num_ctx=4096,
                                temperature=0.2,
                            )
                            st.success(f"Model utworzony: {model_name}")
                            if output:
                                st.code(output)
                        except Exception as exc:  # noqa: BLE001
                            st.error(f"Blad tworzenia modelu: {exc}")

        gguf_files = sorted(hf_dir.rglob("*.gguf"))
        if gguf_files:
            st.markdown("**Pobrane pliki GGUF:**")
            rows = [
                {
                    "file": str(path),
                    "size": _bytes_to_human(path.stat().st_size),
                    "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                }
                for path in gguf_files
            ]
            st.dataframe(rows, use_container_width=True)
        else:
            st.caption("Brak pobranych plikow GGUF.")

    if models:
        table = [
            {
                "name": model.get("name", "-"),
                "size": _bytes_to_human(int(model.get("size", 0))),
                "modified_at": model.get("modified_at", "-"),
                "quantization": (model.get("details", {}) or {}).get("quantization_level", "-"),
            }
            for model in models
        ]
        st.markdown("**Lokalne modele Ollama:**")
        st.dataframe(table, use_container_width=True)
    else:
        st.caption("Brak modeli w Ollama lub brak polaczenia.")

    return models


def _render_agent_chat_tab(models: list[dict[str, Any]]) -> None:
    st.subheader("Agent AI (RAG + lokalny model)")
    st.caption("Tryb: pytanie -> retrieval z Chroma -> odpowiedz modelu lokalnego (Ollama).")

    if "agent_messages" not in st.session_state:
        st.session_state["agent_messages"] = []

    model_names = [str(m.get("name", "")) for m in models if m.get("name")]
    if not model_names:
        st.warning("Brak dostepnych modeli w Ollama. Najpierw pobierz lub zaimportuj model.")
        return

    col1, col2, col3 = st.columns(3)
    with col1:
        selected_model = st.selectbox(
            "Model",
            options=model_names,
            index=0,
            key="agent_model_name",
            help="Model lokalny Ollama, ktory generuje odpowiedz.",
        )
    with col2:
        top_k = st.number_input(
            "Top K kontekstu",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            key="agent_top_k",
            help="Ile fragmentow dokumentacji trafi do promptu.",
        )
    with col3:
        num_ctx = st.number_input(
            "num_ctx",
            min_value=1024,
            max_value=32768,
            value=8192,
            step=512,
            key="agent_num_ctx",
            help="Maksymalny kontekst modelu (tokeny).",
        )

    col4, col5, col6 = st.columns([2, 1, 1])
    with col4:
        source_contains = st.text_input(
            "Filtr source_path (opcjonalnie)",
            value="",
            key="agent_source_filter",
            help="Zawezenie dokumentow do tych, ktorych source_path zawiera ten tekst.",
        )
    with col5:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.2,
            value=0.2,
            step=0.05,
            key="agent_temperature",
            help="Nizej = stabilniej, wyzej = bardziej kreatywnie.",
        )
    with col6:
        fast_mode = st.checkbox(
            "Tryb szybki",
            value=True,
            key="agent_fast_mode",
            help="Przyspiesza odpowiedzi kosztem szczegolowosci.",
        )

    col7, col8 = st.columns(2)
    with col7:
        max_tokens = st.number_input(
            "Max tokens odpowiedzi (num_predict)",
            min_value=64,
            max_value=4096,
            value=220 if fast_mode else 700,
            step=32,
            key="agent_max_tokens",
            help="Maksymalna dlugosc odpowiedzi modelu.",
        )
    with col8:
        request_timeout = st.number_input(
            "Timeout modelu (sekundy)",
            min_value=20,
            max_value=3600,
            value=180,
            step=10,
            key="agent_timeout_sec",
            help="Po tym czasie zapytanie do modelu zostanie przerwane.",
        )

    if st.button("Wyczysc czat", key="agent_clear_chat", help="Usuwa historie rozmowy."):
        st.session_state["agent_messages"] = []
        st.rerun()

    for message in st.session_state["agent_messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            sources = message.get("sources", [])
            if sources:
                st.markdown("**Zrodla:**")
                for source in sources:
                    st.code(source)

    st.caption("Pole czatu: wpisz pytanie i nacisnij Enter.")
    question = st.chat_input("Zadaj pytanie do dokumentacji")
    if not question:
        return

    st.session_state["agent_messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        output_placeholder = st.empty()
        answer = ""
        used_sources: list[str] = []
        run_stats: dict[str, Any] = {}
        error_details = ""

        with st.status("Przetwarzanie zapytania...", expanded=True) as status_box:
            for event in stream_rag_answer(
                question=question,
                model_name=selected_model,
                top_k=int(top_k),
                source_contains=source_contains.strip(),
                temperature=float(temperature),
                num_ctx=int(num_ctx),
                max_tokens=int(max_tokens),
                timeout_sec=int(request_timeout),
            ):
                event_type = event.get("type")

                if event_type in {"phase_started", "phase_completed"}:
                    status_box.write(str(event.get("message", "")))
                    continue

                if event_type == "token":
                    answer = str(event.get("accumulated_text", ""))
                    output_placeholder.markdown(answer)
                    continue

                if event_type == "completed":
                    answer = str(event.get("answer", ""))
                    used_sources = list(event.get("sources", []))
                    run_stats = dict(event.get("stats", {}))
                    output_placeholder.markdown(answer)
                    status_box.update(label="Zakonczono przetwarzanie zapytania.", state="complete")
                    continue

                if event_type == "error":
                    answer = str(event.get("message", "Blad agenta."))
                    error_details = str(event.get("technical_details", ""))
                    output_placeholder.markdown(answer)
                    status_box.update(label="Blad podczas przetwarzania.", state="error")
                    break

        st.session_state["agent_last_run_stats"] = run_stats

        if used_sources:
            st.markdown("**Zrodla:**")
            for source in used_sources:
                st.code(source)

        if error_details:
            with st.expander("Szczegoly techniczne bledu", expanded=False):
                st.code(error_details)

        stats = st.session_state.get("agent_last_run_stats", {})
        if stats:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Czas retrieval", f"{stats.get('retrieval_sec', 0.0):.2f}s")
            c2.metric("Pierwszy token", f"{stats.get('time_to_first_token_sec', 0.0):.2f}s")
            c3.metric("Czas generowania", f"{stats.get('generation_sec', 0.0):.2f}s")
            c4.metric("Czas calkowity", f"{stats.get('total_sec', 0.0):.2f}s")

            eval_count = int(stats.get("eval_count", 0))
            eval_duration_ns = int(stats.get("eval_duration_ns", 0))
            if eval_count > 0 and eval_duration_ns > 0:
                tok_s = eval_count / (eval_duration_ns / 1_000_000_000)
                st.caption(
                    f"Model throughput: {tok_s:.2f} token/s | "
                    f"prompt_eval_count={int(stats.get('prompt_eval_count', 0))} | "
                    f"eval_count={eval_count}"
                )

    st.session_state["agent_messages"].append({"role": "assistant", "content": answer, "sources": used_sources})


def main() -> None:
    st.set_page_config(page_title="InvoiceJet Chroma + Agent AI", page_icon=":mag:", layout="wide")
    st.title("InvoiceJet - Chroma Search + Agent AI")
    st.caption("Lokalna baza wektorowa (Chroma) + lokalne modele LLM (Ollama).")

    config = load_config()
    module_dir = Path(__file__).resolve().parent
    hf_dir, modelfiles_dir = _ensure_local_dirs(module_dir)
    manual_text = _load_agent_manual(module_dir)

    with st.sidebar:
        st.subheader("Konfiguracja")
        st.write(f"Kolekcja: `{config.collection_name}`")
        st.write(f"Chroma path: `{config.chroma_path}`")
        st.write(f"Project root: `{config.project_root}`")
        st.write(f"HF GGUF dir: `{hf_dir}`")
        st.write(f"Ollama API: `{OLLAMA_BASE_URL}`")

    search_tab, agent_tab = st.tabs(["Wyszukiwarka", "Agent AI"])

    with search_tab:
        _render_search_tab(config)

    with agent_tab:
        if "agent_help_visible" not in st.session_state:
            st.session_state["agent_help_visible"] = False

        help_col_1, help_col_2 = st.columns([1, 3])
        with help_col_1:
            if st.button("Help ?", key="agent_help_button", help="Pokazuje instrukcje uzytkownika Agent AI."):
                st.session_state["agent_help_visible"] = not st.session_state["agent_help_visible"]
        with help_col_2:
            st.download_button(
                "Pobierz manual (.md)",
                data=manual_text,
                file_name="AGENT_AI_USER_MANUAL_PL.md",
                mime="text/markdown",
                key="agent_help_download",
                help="Pobiera instrukcje Agent AI jako plik markdown.",
            )

        if st.session_state["agent_help_visible"]:
            st.info("Manual Agent AI")
            st.markdown(manual_text)
            st.divider()

        models = _render_model_manager_tab(hf_dir=hf_dir, modelfiles_dir=modelfiles_dir)
        st.divider()
        _render_agent_chat_tab(models=models)


if __name__ == "__main__":
    main()
