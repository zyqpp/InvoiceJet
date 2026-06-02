from __future__ import annotations

from dataclasses import replace
import json
from typing import Any, Iterable, Sequence

import streamlit as st

from oracle_invoicejet.agent_profiles import AgentProfile, get_agent_profile, list_agent_profiles
from oracle_invoicejet.agents import OracleOrchestrator, SCOPE_GROUPS
from oracle_invoicejet.config import AppConfig, load_config
from oracle_invoicejet.diagnostics import DoctorService, recommended_models
from oracle_invoicejet.documents import discover_documents
from oracle_invoicejet.embeddings import OllamaClient
from oracle_invoicejet.indexing import IndexManager
from oracle_invoicejet.rag import NO_ANSWER
from oracle_invoicejet.retrieval import RetrievalService


EMBEDDING_HELP = (
    "Embedding to liczbowy odcisk tekstu. Oracle zamienia pytanie i fragmenty dokumentacji "
    "na wektory, a potem szuka najbardziej podobnych fragmentów. Model embeddingów musi być "
    "zgodny z modelem użytym przy budowie indeksu; po zmianie embeddingu zrób rebuild indeksu."
)

SCOPE_LABELS = {
    "full": "Pełny korpus",
    "technical": "Techniczne / doc_AI",
    "user": "Użytkownik / doc_user",
    "backend": "Backend/API z doc_AI",
    "frontend": "Frontend/UI z doc_AI",
    "debt": "Dług techniczny z doc_AI",
}


def main() -> None:
    st.set_page_config(page_title="Oracle InvoiceJet", page_icon="🔎", layout="wide")
    base_config = load_config()
    runtime = render_sidebar(base_config)
    config: AppConfig = runtime["config"]
    profile: AgentProfile = runtime["profile"]
    scope: str = runtime["scope"]
    show_trace: bool = runtime["show_trace"]

    st.title("Oracle InvoiceJet")
    st.caption("Lokalny portal RAG nad dokumentacją InvoiceJet. Modele mają oryginalne nazwy Ollama; agenci są profilami pracy.")

    chat_tab, search_tab, sources_tab, index_tab, agents_tab, diagnostics_tab = st.tabs(
        ["Czat", "Wyszukiwarka", "Źródła", "Indeks", "Agenci i modele", "Diagnostyka"]
    )

    with chat_tab:
        render_chat_tab(config, profile, scope, show_trace)
    with search_tab:
        render_search_tab(config, scope)
    with sources_tab:
        render_sources_tab(config)
    with index_tab:
        render_index_tab(config)
    with agents_tab:
        render_agents_models_tab(config, profile)
    with diagnostics_tab:
        render_diagnostics_tab(config, scope)


def render_sidebar(base_config: AppConfig) -> dict[str, Any]:
    profiles = list_agent_profiles()
    profile_labels = [format_profile_label(profile) for profile in profiles]

    with st.sidebar:
        st.subheader("Profil pracy")
        selected_label = st.selectbox(
            "Agent",
            options=profile_labels,
            index=0,
            help="Agent w portalu to gotowy profil pracy: zakres źródeł, model LLM, embedding i parametry odpowiedzi.",
        )
        profile = get_agent_profile(profiles[profile_labels.index(selected_label)].key)
        st.caption(profile.description)
        if profile.notes:
            st.warning(profile.notes)

        scope_options = list(SCOPE_GROUPS.keys())
        scope = st.selectbox(
            "Zakres źródeł",
            options=scope_options,
            index=scope_options.index(profile.default_scope),
            format_func=lambda value: SCOPE_LABELS.get(value, value),
            help="Zakres decyduje, które grupy dokumentacji są przeszukiwane.",
        )

        st.markdown("**Podstawowe**")
        top_k = st.slider(
            "Liczba źródeł",
            min_value=1,
            max_value=20,
            value=profile.top_k,
            help="Ile najlepiej pasujących fragmentów dokumentacji trafi do odpowiedzi.",
        )
        temperature = st.slider(
            "Kreatywność",
            min_value=0.0,
            max_value=1.0,
            value=float(profile.temperature),
            step=0.05,
            help="Niżej = bardziej konsekwentnie i bezpiecznie. Do dokumentacji zwykle 0.0–0.2.",
        )

        with st.expander("Opcje zaawansowane", expanded=False):
            llm_model = st.selectbox(
                "Model LLM",
                options=llm_model_options(base_config.allowed_models, profiles),
                index=model_option_index(llm_model_options(base_config.allowed_models, profiles), profile.llm_model),
                help="Model Ollama generujący odpowiedź. Nazwa modelu nie jest tłumaczona.",
            )
            embedding_model = st.selectbox(
                "Model embeddingów",
                options=embedding_model_options(base_config.allowed_models, profiles),
                index=model_option_index(embedding_model_options(base_config.allowed_models, profiles), profile.embedding_model),
                help=EMBEDDING_HELP,
            )
            num_ctx = st.number_input("Kontekst modelu", min_value=1024, max_value=32768, value=profile.num_ctx, step=1024)
            num_predict = st.number_input("Maks. tokeny odpowiedzi", min_value=128, max_value=4096, value=profile.num_predict, step=128)
            min_hits = st.number_input("Minimalna liczba trafień", min_value=1, max_value=10, value=profile.min_hits)
            show_trace = st.toggle("Pokaż trace agentów", value=False)

        if embedding_model != base_config.embedding_model:
            st.warning("Zmieniasz embedding względem bieżącej konfiguracji. Po zmianie embeddingu przebuduj indeks.")

        config = replace(
            base_config,
            llm_model=llm_model,
            embedding_model=embedding_model,
            top_k=int(top_k),
            temperature=float(temperature),
            num_ctx=int(num_ctx),
            num_predict=int(num_predict),
            min_hits=int(min_hits),
        )

        st.divider()
        render_sidebar_status(config, profile)

    return {"config": config, "profile": profile, "scope": scope, "show_trace": show_trace}


def render_sidebar_status(config: AppConfig, profile: AgentProfile) -> None:
    st.markdown("**Aktywna konfiguracja**")
    st.write(f"Agent: `{profile.name}`")
    st.write(f"LLM: `{config.llm_model}`")
    st.write(f"Embedding: `{config.embedding_model}`")
    st.write(f"Ollama: `{config.ollama_base_url}`")
    st.write(f"Indeks: `{config.collection_name}`")

    client = OllamaClient(config.ollama_base_url)
    online, message = client.is_online()
    if online:
        st.success(message)
    else:
        st.error(message)


def render_chat_tab(config: AppConfig, profile: AgentProfile, scope: str, show_trace: bool) -> None:
    st.subheader("Czat z dokumentacją")
    st.info(
        f"Aktywny profil: **{profile.name}** — {profile.role}. "
        f"Model: `{config.llm_model}`, embedding: `{config.embedding_model}`, zakres: `{SCOPE_LABELS.get(scope, scope)}`."
    )
    question = st.text_area("Pytanie", height=120, placeholder="Np. Jak wygląda proces rejestracji i logowania?")
    col_ask, col_example = st.columns([1, 1])
    ask_clicked = col_ask.button("Zapytaj Oracle", type="primary")
    if col_example.button("Wstaw pytanie przykładowe"):
        question = "Jak wygląda proces rejestracji i logowania w InvoiceJet?"
        st.session_state["oracle_example_question"] = question
    question = st.session_state.pop("oracle_example_question", question)

    if not ask_clicked:
        return
    if not question.strip():
        st.warning("Wpisz pytanie.")
        return

    with st.spinner("Oracle pracuje: Router → Retriever → Answerer → Verifier..."):
        try:
            result = OracleOrchestrator(config).answer(question.strip(), requested_scope=scope)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Błąd zapytania: {exc}")
            return

    if result.answer.strip() == NO_ANSWER:
        st.warning(result.answer)
    else:
        st.markdown(result.answer)
    st.caption(f"Zakres: {SCOPE_LABELS.get(result.scope, result.scope)} | verified={result.verified}")

    if result.warnings:
        st.warning("\n".join(result.warnings))
    if result.citation_lines:
        with st.expander("Źródła systemowe", expanded=True):
            for citation in result.citation_lines:
                st.code(citation)
    if show_trace:
        with st.expander("Trace agentów", expanded=True):
            for step in result.trace:
                st.write(f"**{step.role}:** {step.message}")


def render_search_tab(config: AppConfig, default_scope: str) -> None:
    st.subheader("Wyszukiwarka semantyczna")
    st.caption("Tu testujesz sam retrieval, bez generowania odpowiedzi przez LLM.")
    question = st.text_input("Zapytanie")
    scope = st.selectbox(
        "Zakres wyszukiwania",
        options=["all"] + list(SCOPE_GROUPS.keys()),
        index=(["all"] + list(SCOPE_GROUPS.keys())).index(default_scope) if default_scope in SCOPE_GROUPS else 0,
        format_func=lambda value: "Wszystko" if value == "all" else SCOPE_LABELS.get(value, value),
    )
    top_k = st.number_input("Top K", min_value=1, max_value=20, value=config.top_k)
    st.caption(f"Embedding: `{config.embedding_model}`")
    if st.button("Szukaj"):
        if not question.strip():
            st.warning("Wpisz zapytanie.")
            return
        groups = None if scope == "all" else SCOPE_GROUPS[scope]
        try:
            hits = RetrievalService(config).search(question.strip(), top_k=int(top_k), source_groups=groups)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Błąd wyszukiwania: {exc}")
            return
        if not hits:
            st.warning("Brak trafień.")
        for hit in hits:
            st.markdown(f"**{hit.source_path}**")
            st.caption(f"{hit.metadata.get('heading_path', 'ROOT')} | distance={hit.distance:.6f}")
            st.code(hit.text[:1500], language="markdown")


def render_sources_tab(config: AppConfig) -> None:
    st.subheader("Źródła dokumentacji")
    documents, skipped = discover_documents(config)
    col_docs, col_skipped = st.columns(2)
    col_docs.metric("Pliki .md w bazie", len(documents))
    col_skipped.metric("Pominięte", skipped)
    st.caption("Baza odpowiedzi obejmuje tylko `InvoiceJet/doc_AI` i `InvoiceJet/doc_user`.")
    rows = [
        {
            "source_group": document.source_group,
            "audience": document.audience,
            "priority": document.priority,
            "relative_path": document.relative_path,
        }
        for document in documents
    ]
    st.dataframe(rows, use_container_width=True, height=520)


def render_index_tab(config: AppConfig) -> None:
    st.subheader("Index Manager")
    render_index_status(config)
    st.caption("Domyślnie użyj odświeżenia incremental. Force rebuild tylko po zmianie embeddingu albo parametrów chunkingu.")
    force = st.checkbox("Force rebuild od zera", value=False)
    if st.button("Odśwież indeks", type="primary"):
        with st.spinner("Indeksuję dokumentację..."):
            try:
                stats = IndexManager(config).run_ingest(force_rebuild=force)
            except Exception as exc:  # noqa: BLE001
                st.error(f"Błąd ingestu: {exc}")
                return
        st.success("Ingest zakończony.")
        st.json(stats.__dict__)


def render_agents_models_tab(config: AppConfig, active_profile: AgentProfile) -> None:
    st.subheader("Agenci i modele")
    st.caption("Agenci to profile pracy. Modele zachowują oryginalne nazwy Ollama.")
    client = OllamaClient(config.ollama_base_url)
    online, message = client.is_online()
    if not online:
        st.error(message)
        return
    st.success(message)

    try:
        models = client.list_models()
    except Exception as exc:  # noqa: BLE001
        st.error(f"Nie można pobrać listy modeli: {exc}")
        return
    available = normalized_model_names(model.get("name", "") for model in models)
    profiles = list_agent_profiles()
    st.dataframe(
        [
            {
                "agent": profile.name,
                "rola": profile.role,
                "scope": SCOPE_LABELS.get(profile.default_scope, profile.default_scope),
                "LLM": profile.llm_model,
                "embedding": profile.embedding_model,
                "dostępny": all(is_model_available(model, available) for model in profile.required_models),
            }
            for profile in profiles
        ],
        use_container_width=True,
    )

    selected_profile_label = st.selectbox(
        "Profil do pobrania/sprawdzenia",
        options=[format_profile_label(profile) for profile in profiles],
        index=[profile.key for profile in profiles].index(active_profile.key),
    )
    selected_profile = profiles[[format_profile_label(profile) for profile in profiles].index(selected_profile_label)]
    missing = [model for model in selected_profile.required_models if not is_model_available(model, available)]
    if missing:
        st.warning(f"Brakuje modeli: {', '.join(missing)}")
    else:
        st.success("Wszystkie modele dla tego profilu są dostępne lokalnie.")

    if st.button("Pobierz wymagane modele profilu", type="primary"):
        pull_models(client, config, selected_profile.required_models)

    with st.expander("Pobierz pojedynczy model z whitelisty"):
        model = st.selectbox("Model", options=recommended_models())
        if st.button("Pobierz wybrany model"):
            pull_models(client, config, [model])

    st.markdown("**Modele lokalne**")
    st.dataframe(
        [
            {
                "name": model.get("name"),
                "size": model.get("size"),
                "modified_at": model.get("modified_at"),
                "quantization": (model.get("details", {}) or {}).get("quantization_level"),
            }
            for model in models
        ],
        use_container_width=True,
    )


def render_diagnostics_tab(config: AppConfig, scope: str) -> None:
    st.subheader("Diagnostyka")
    test_embedding = st.checkbox("Testuj embedding przez Ollama", value=False, help=EMBEDDING_HELP)
    if st.button("Uruchom oracle-doctor"):
        checks = DoctorService(config).run(test_embedding=test_embedding)
        for check in checks:
            if check.ok:
                st.success(f"{check.name}: {check.message}")
            else:
                st.error(f"{check.name}: {check.message}")

    st.divider()
    st.markdown("**Szybkie testy RAG**")
    col_ok, col_fallback = st.columns(2)
    if col_ok.button("Test odpowiedzi z dokumentacji"):
        run_rag_test(config, scope, "Jak wygląda proces rejestracji i logowania w InvoiceJet?", expect_fallback=False)
    if col_fallback.button("Test braku w dokumentacji"):
        run_rag_test(config, scope, "Jaka będzie jutro pogoda w Warszawie?", expect_fallback=True)


def render_index_status(config: AppConfig) -> None:
    manifest_path = config.manifest_path
    if not manifest_path.exists():
        st.warning("Manifest indeksu nie istnieje. Uruchom pierwszy ingest.")
        return
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        st.error(f"Nie można odczytać manifestu: {exc}")
        return
    files = manifest.get("files", {})
    chunk_count = sum(len(file_state.get("chunk_ids", [])) for file_state in files.values() if isinstance(file_state, dict))
    col_files, col_chunks, col_embedding = st.columns(3)
    col_files.metric("Pliki w manifeście", len(files))
    col_chunks.metric("Chunki", chunk_count)
    col_embedding.metric("Embedding indeksu", manifest.get("embedding_model", "-"))


def run_rag_test(config: AppConfig, scope: str, question: str, expect_fallback: bool) -> None:
    with st.spinner("Uruchamiam test RAG..."):
        try:
            result = OracleOrchestrator(config).answer(question, requested_scope=scope)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Test nie powiódł się technicznie: {exc}")
            return
    st.write(result.answer)
    got_fallback = result.answer.strip() == NO_ANSWER
    if got_fallback == expect_fallback:
        st.success("Test przeszedł.")
    else:
        st.error("Test nie przeszedł: wynik nie zgadza się z oczekiwaniem.")
    if result.citation_lines:
        with st.expander("Źródła testu"):
            for citation in result.citation_lines:
                st.code(citation)


def pull_models(client: OllamaClient, config: AppConfig, models: Sequence[str]) -> None:
    for model in models:
        if model not in config.allowed_models:
            st.error(f"Model spoza whitelisty Oracle: {model}")
            return
    for model in models:
        with st.spinner(f"Pobieram {model}..."):
            try:
                st.json(client.pull_model(model))
            except Exception as exc:  # noqa: BLE001
                st.error(f"Błąd pobierania {model}: {exc}")
                return
    st.success("Pobieranie zakończone.")


def format_profile_label(profile: AgentProfile) -> str:
    return f"{profile.name} — {profile.role}"


def llm_model_options(allowed_models: Sequence[str], profiles: Sequence[AgentProfile]) -> list[str]:
    profile_models = [profile.llm_model for profile in profiles]
    allowed_llms = [model for model in allowed_models if model not in {"bge-m3", "nomic-embed-text"}]
    return unique_items([*profile_models, *allowed_llms])


def embedding_model_options(allowed_models: Sequence[str], profiles: Sequence[AgentProfile]) -> list[str]:
    profile_models = [profile.embedding_model for profile in profiles]
    allowed_embeddings = [model for model in allowed_models if model in {"bge-m3", "nomic-embed-text"}]
    return unique_items([*profile_models, *allowed_embeddings])


def model_option_index(options: Sequence[str], selected: str) -> int:
    return list(options).index(selected) if selected in options else 0


def normalized_model_names(model_names: Iterable[str]) -> set[str]:
    names: set[str] = set()
    for raw_name in model_names:
        name = str(raw_name)
        if not name:
            continue
        names.add(name)
        if name.endswith(":latest"):
            names.add(name.removesuffix(":latest"))
    return names


def is_model_available(model: str, available: set[str]) -> bool:
    return model in available or f"{model}:latest" in available


def unique_items(items: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(item for item in items if item))


if __name__ == "__main__":
    main()
