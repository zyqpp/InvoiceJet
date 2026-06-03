from __future__ import annotations

from dataclasses import replace
import json
import re
from typing import Any, Iterable, Sequence

import streamlit as st

from oracle_invoicejet.agent_profiles import AgentProfile, get_agent_profile, list_agent_profiles
from oracle_invoicejet.agents import OracleOrchestrator, SCOPE_GROUPS
from oracle_invoicejet.config import AppConfig, load_config
from oracle_invoicejet.diagnostics import DoctorService, recommended_models
from oracle_invoicejet.documents import discover_documents
from oracle_invoicejet.embeddings import OllamaClient
from oracle_invoicejet.evaluation import result_to_row, run_eval_set, summarize_results
from oracle_invoicejet.indexing import IndexManager
from oracle_invoicejet.profiles import get_model_profile, list_model_profiles, list_prompt_profiles
from oracle_invoicejet.rag import NO_ANSWER, source_path_to_portal_url
from oracle_invoicejet.rag_profiles import get_rag_profile, list_rag_profiles
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

MISSING_MODEL_SOURCES_WARNING = "Model nie dodał sekcji źródeł; cytowania pokazano osobno przez system."


def main() -> None:
    st.set_page_config(page_title="Oracle InvoiceJet", page_icon="🔎", layout="wide")
    base_config = load_config()
    runtime = render_sidebar(base_config)
    config: AppConfig = runtime["config"]
    profile: AgentProfile = runtime["profile"]
    scope: str = runtime["scope"]
    rag_profile_key: str = runtime["rag_profile"]
    prompt_profile_key: str = runtime["prompt_profile"]
    show_trace: bool = runtime["show_trace"]

    st.title("Oracle InvoiceJet")
    st.caption("Lokalny portal RAG nad dokumentacją InvoiceJet. Jeden portal, Chroma + Ollama, profile RAG/modeli/promptów.")

    chat_tab, search_tab, sources_tab, index_tab, eval_tab, agents_tab, diagnostics_tab = st.tabs(
        ["Czat", "Wyszukiwarka", "Źródła", "Indeks", "Ewaluacja", "Agenci i modele", "Diagnostyka"]
    )

    with chat_tab:
        render_chat_tab(config, profile, scope, rag_profile_key, prompt_profile_key, show_trace)
    with search_tab:
        render_search_tab(config, rag_profile_key)
    with sources_tab:
        render_sources_tab(config)
    with index_tab:
        render_index_tab(config)
    with eval_tab:
        render_evaluation_tab(config)
    with agents_tab:
        render_agents_models_tab(config, profile)
    with diagnostics_tab:
        render_diagnostics_tab(config, scope, rag_profile_key, prompt_profile_key)


def render_sidebar(base_config: AppConfig) -> dict[str, Any]:
    profiles = list_agent_profiles()
    profile_labels = [format_profile_label(profile) for profile in profiles]

    with st.sidebar:
        st.subheader("Profil pracy")
        selected_label = st.selectbox(
            "Agent",
            options=profile_labels,
            index=0,
            help="Agent to profil pracy: model, prompt, RAG profile, zakres źródeł i limity.",
        )
        profile = get_agent_profile(profiles[profile_labels.index(selected_label)].key)
        st.caption(profile.description)
        if profile.tooltip:
            st.caption(f"Instrukcja: {profile.tooltip}")
        render_agent_guidance(profile)
        if profile.notes:
            st.warning(profile.notes)

        scope_options = list(SCOPE_GROUPS.keys())
        scope = st.selectbox(
            "Zakres źródeł",
            options=scope_options,
            index=scope_options.index(profile.default_scope),
            format_func=lambda value: SCOPE_LABELS.get(value, value),
        )

        model_profiles = list_model_profiles(base_config.tool_root)
        model_keys = [item.key for item in model_profiles]
        selected_model_key = st.selectbox(
            "Profil modelu",
            options=model_keys,
            index=model_option_index(model_keys, profile.model_profile),
            format_func=lambda key: get_model_profile(base_config.tool_root, key).name,
        )
        model_profile = get_model_profile(base_config.tool_root, selected_model_key)
        use_agent_overrides = selected_model_key == profile.model_profile
        default_llm_model = profile.llm_model if use_agent_overrides else model_profile.llm_model
        default_embedding_model = profile.embedding_model if use_agent_overrides else model_profile.embedding_model
        default_top_k = profile.top_k if use_agent_overrides else model_profile.top_k
        default_num_ctx = profile.num_ctx if use_agent_overrides else model_profile.num_ctx
        default_temperature = profile.temperature if use_agent_overrides else model_profile.temperature
        default_num_predict = profile.num_predict if use_agent_overrides else model_profile.num_predict
        default_top_p = profile.top_p if use_agent_overrides else model_profile.top_p
        default_llm_top_k = profile.llm_top_k if use_agent_overrides else model_profile.llm_top_k
        default_repeat_penalty = profile.repeat_penalty if use_agent_overrides else model_profile.repeat_penalty
        default_seed = profile.seed if use_agent_overrides else model_profile.seed
        default_timeout_sec = profile.timeout_sec if use_agent_overrides else model_profile.timeout_sec
        default_think = profile.think if use_agent_overrides else model_profile.think
        default_strip_thinking = profile.strip_thinking if use_agent_overrides else model_profile.strip_thinking

        rag_profiles = list_rag_profiles()
        rag_keys = [item.key for item in rag_profiles]
        rag_profile_key = st.selectbox(
            "Profil RAG",
            options=rag_keys,
            index=model_option_index(rag_keys, profile.rag_profile),
            format_func=lambda key: get_rag_profile(key).label,
            help="Profil RAG decyduje, jakie typy źródeł mają dostać priorytet.",
        )

        prompt_profiles = list_prompt_profiles(base_config.tool_root)
        prompt_keys = [item.key for item in prompt_profiles]
        prompt_profile_key = st.selectbox(
            "Master prompt",
            options=prompt_keys,
            index=model_option_index(prompt_keys, profile.prompt_profile),
            format_func=lambda key: next(item.name for item in prompt_profiles if item.key == key),
        )

        st.markdown("**Podstawowe**")
        top_k = st.slider("Liczba źródeł", min_value=1, max_value=24, value=default_top_k)
        temperature = st.slider(
            "Kreatywność",
            min_value=0.0,
            max_value=1.0,
            value=float(default_temperature),
            step=0.05,
            help="Niżej = bardziej konsekwentnie i bezpiecznie. Do dokumentacji zwykle 0.0-0.2.",
        )

        with st.expander("Opcje zaawansowane", expanded=False):
            llm_model = st.selectbox(
                "Model LLM",
                options=llm_model_options(base_config.allowed_models, profiles, model_profiles),
                index=model_option_index(llm_model_options(base_config.allowed_models, profiles, model_profiles), default_llm_model),
            )
            embedding_model = st.selectbox(
                "Model embeddingów",
                options=embedding_model_options(base_config.allowed_models, profiles, model_profiles),
                index=model_option_index(embedding_model_options(base_config.allowed_models, profiles, model_profiles), default_embedding_model),
                help=EMBEDDING_HELP,
            )
            num_ctx = st.number_input("Kontekst modelu", min_value=1024, max_value=32768, value=default_num_ctx, step=1024)
            num_predict = st.number_input("Maks. tokeny odpowiedzi", min_value=128, max_value=4096, value=default_num_predict, step=128)
            top_p = st.slider("top_p", min_value=0.05, max_value=1.0, value=float(default_top_p), step=0.05)
            llm_top_k = st.number_input("top_k modelu", min_value=1, max_value=200, value=default_llm_top_k, step=1)
            repeat_penalty = st.slider("repeat_penalty", min_value=0.8, max_value=2.0, value=float(default_repeat_penalty), step=0.05)
            seed_raw = st.text_input("seed", value="" if default_seed is None else str(default_seed))
            timeout_sec = st.number_input("Timeout generacji [s]", min_value=30, max_value=3600, value=default_timeout_sec, step=30)
            think_option = st.selectbox(
                "Thinking Ollama",
                options=["auto", "off", "on", "low", "medium", "high"],
                index=model_option_index(["auto", "off", "on", "low", "medium", "high"], think_to_option(default_think)),
                help="Dla modeli typu Qwen/DeepSeek. Qwen w Oracle powinien zwykle pracowac z off.",
            )
            strip_thinking = st.toggle(
                "Ukryj sekcje thinking",
                value=bool(default_strip_thinking),
                help="Usuwa bloki <think>...</think> z odpowiedzi, gdy model zwroci je mimo konfiguracji.",
            )
            min_hits = st.number_input("Minimalna liczba trafień", min_value=1, max_value=10, value=profile.min_hits)
            show_trace = st.toggle("Pokaż trace agentów", value=False)

        seed = int(seed_raw) if seed_raw.strip() else None
        think = option_to_think(think_option)
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
            top_p=float(top_p),
            llm_top_k=int(llm_top_k),
            repeat_penalty=float(repeat_penalty),
            seed=seed,
            timeout_sec=int(timeout_sec),
            min_hits=int(min_hits),
            think=think,
            strip_thinking=bool(strip_thinking),
        )

        st.divider()
        render_sidebar_status(config, profile, selected_model_key, rag_profile_key, prompt_profile_key)

    return {
        "config": config,
        "profile": profile,
        "scope": scope,
        "rag_profile": rag_profile_key,
        "prompt_profile": prompt_profile_key,
        "show_trace": show_trace,
    }


def render_sidebar_status(
    config: AppConfig,
    profile: AgentProfile,
    model_profile: str,
    rag_profile: str,
    prompt_profile: str,
) -> None:
    st.markdown("**Aktywna konfiguracja**")
    st.write(f"Agent: `{profile.name}`")
    st.write(f"Model profile: `{model_profile}`")
    st.write(f"RAG profile: `{rag_profile}`")
    st.write(f"Prompt: `{prompt_profile}`")
    st.write(f"LLM: `{config.llm_model}`")
    st.write(f"Embedding: `{config.embedding_model}`")
    st.write(f"Thinking: `{think_to_option(config.think)}`")
    st.write(f"Strip thinking: `{config.strip_thinking}`")
    st.write(f"Ollama: `{config.ollama_base_url}`")
    st.write(f"Indeks: `{config.collection_name}`")
    st.markdown("**Portale dokumentacji**")
    st.markdown(f"- [doc_user]({config.docs_portal_doc_user})")
    st.markdown(f"- [doc_AI]({config.docs_portal_doc_ai})")
    st.markdown("**Pipeline v2 — agenty**")
    st.caption(f"Light LLM: `{config.light_llm_model}`")
    with st.expander("Status agentów v2"):
        st.caption(f"Klasyfikator: {'✅ włączony' if config.enable_query_classifier else '❌ wyłączony'}")
        st.caption(f"Dekompozycja: {'✅ włączona' if config.enable_query_decomposer else '❌ wyłączona'}")
        st.caption(f"Hygiene: {'✅ włączony' if config.enable_context_hygiene else '❌ wyłączony'}")
        st.caption(f"MissingLink: {'✅ włączony' if config.enable_missing_link else '❌ wyłączony'}")
        st.caption(f"FactChecker: {'✅ włączony' if config.enable_fact_checker else '❌ wyłączony (domyślnie)'}")

    client = OllamaClient(config.ollama_base_url)
    online, message = client.is_online()
    if online:
        st.success(message)
    else:
        st.error(message)


def render_agent_guidance(profile: AgentProfile) -> None:
    capabilities = list(profile.capabilities or [])
    limitations = list(profile.limitations or [])
    examples = list(profile.examples or [])
    if not capabilities and not limitations and not examples:
        return
    with st.expander("Co potrafi ten agent?", expanded=False):
        if capabilities:
            st.markdown("**Potrafi**")
            for item in capabilities:
                st.write(f"- {item}")
        if limitations:
            st.markdown("**Ograniczenia**")
            for item in limitations:
                st.write(f"- {item}")
        if examples:
            st.markdown("**Przykladowe pytania**")
            for item in examples:
                st.code(item, language="text")


def render_chat_tab(
    config: AppConfig,
    profile: AgentProfile,
    scope: str,
    rag_profile: str,
    prompt_profile: str,
    show_trace: bool,
) -> None:
    st.subheader("Czat z dokumentacją")
    st.info(
        f"Aktywny profil: **{profile.name}** - {profile.role}. "
        f"Model: `{config.llm_model}`, embedding: `{config.embedding_model}`, "
        f"RAG: `{rag_profile}`, prompt: `{prompt_profile}`."
    )
    if profile.tooltip:
        st.caption(f"Instrukcja agenta: {profile.tooltip}")
    question = st.text_area(
        "Pytanie",
        height=120,
        placeholder="Np. Na ekranie serii dokumentów skąd pobierane są informacje i jaka tabela je przechowuje?",
    )
    col_ask, col_example = st.columns([1, 1])
    ask_clicked = col_ask.button("Zapytaj Oracle", type="primary")
    if col_example.button("Wstaw pytanie przekrojowe"):
        question = "Na ekranie serii dokumentów skąd pobierane są informacje i jaka tabela je przechowuje?"
        st.session_state["oracle_example_question"] = question
    question = st.session_state.pop("oracle_example_question", question)

    if not ask_clicked:
        return
    if not question.strip():
        st.warning("Wpisz pytanie.")
        return

    answer_placeholder = st.empty()
    final_event: dict[str, Any] | None = None
    with st.status("Oracle pracuje...", expanded=True) as status:
        for event in OracleOrchestrator(config).stream_answer(
            question.strip(),
            requested_scope=scope,
            requested_rag_profile=rag_profile,
            prompt_profile_key=prompt_profile,
        ):
            event_type = event.get("type")
            if event_type == "phase_started":
                status.update(label=str(event.get("message", "")), state="running")
                st.write(f"Start: {event.get('phase')}")
            elif event_type == "phase_completed":
                status.update(label=str(event.get("message", "")), state="running")
                st.write(f"OK: {event.get('phase')}")
            elif event_type == "token":
                answer_placeholder.markdown(str(event.get("accumulated_text", "")))
            elif event_type == "completed":
                final_event = event
                status.update(label="Gotowe.", state="complete")
            elif event_type == "error":
                status.update(label="Błąd generowania.", state="error")
                st.error(str(event.get("message", "Błąd.")))
                with st.expander("Szczegóły techniczne"):
                    st.code(str(event.get("technical_details", "")))
                return

    if not final_event:
        st.error("Generator zakończył się bez eventu completed.")
        return
    render_completed_answer(final_event, answer_placeholder, show_trace, config)


_MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+?\.md)\)")


def _rewrite_md_links(
    answer: str,
    sources: list[dict[str, Any]],
    doc_user_base: str,
    doc_ai_base: str,
) -> str:
    """Przepisuje [text](*.md) na pełne URL portalu MkDocs na podstawie cytowań."""
    filename_map: dict[str, str] = {}
    for src in sources:
        sp = _source_path_from_row(src)
        url = source_path_to_portal_url(sp, doc_user_base, doc_ai_base)
        if url:
            filename_map[sp.replace("\\", "/").rsplit("/", 1)[-1]] = url

    def _replace(m: re.Match) -> str:
        text, href = m.group(1), m.group(2)
        direct = source_path_to_portal_url(href, doc_user_base, doc_ai_base)
        if direct:
            return f"[{text}]({direct})"
        filename = href.replace("\\", "/").rsplit("/", 1)[-1]
        if filename in filename_map:
            return f"[{text}]({filename_map[filename]})"
        return m.group(0)

    return _MD_LINK_RE.sub(_replace, answer)


def build_enriched_source_rows(
    sources: Sequence[dict[str, Any]],
    doc_user_base: str,
    doc_ai_base: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in sources:
        source_path = _source_path_from_row(source)
        row = dict(source)
        row.pop("portal_url", None)
        rows.append(
            {
                "portal_url": source_path_to_portal_url(source_path, doc_user_base, doc_ai_base) or "",
                **row,
            }
        )
    return rows


def build_source_links_markdown(
    sources: Sequence[dict[str, Any]],
    doc_user_base: str,
    doc_ai_base: str,
) -> str:
    links: list[str] = []
    for source in sources:
        source_path = _source_path_from_row(source)
        url = source_path_to_portal_url(source_path, doc_user_base, doc_ai_base)
        if url:
            links.append(f"- [{source_path}]({url})")
    return "\n".join(links)


def _portal_markdown_link(source_path: str, doc_user_base: str, doc_ai_base: str, label: str = "Otwórz w portalu") -> str:
    url = source_path_to_portal_url(source_path, doc_user_base, doc_ai_base)
    return f"[{label}]({url})" if url else ""


def _source_path_from_row(source: dict[str, Any]) -> str:
    return str(source.get("source_path") or source.get("relative_path") or "")


def render_completed_answer(event: dict[str, Any], answer_placeholder, show_trace: bool, config: AppConfig) -> None:
    answer = str(event.get("answer", "")).strip()
    sources = list(event.get("sources", []))
    if answer == NO_ANSWER:
        answer_placeholder.warning(answer)
    else:
        answer = _rewrite_md_links(
            answer, sources,
            config.docs_portal_doc_user,
            config.docs_portal_doc_ai,
        )
        answer_placeholder.markdown(answer)
    st.caption(
        f"Zakres: {event.get('scope')} | RAG={event.get('rag_profile')} | "
        f"prompt={event.get('prompt_profile')} | verified={event.get('verified')}"
    )
    warnings = list(event.get("warnings", []))
    if warnings:
        info_warnings = [str(item) for item in warnings if str(item) == MISSING_MODEL_SOURCES_WARNING]
        warning_warnings = [str(item) for item in warnings if str(item) != MISSING_MODEL_SOURCES_WARNING]
        if info_warnings:
            st.info("\n".join(info_warnings))
        if warning_warnings:
            st.warning("\n".join(warning_warnings))
    render_metrics(event.get("stats", {}))
    if sources:
        st.markdown("**Źródła systemowe**")
        source_links = build_source_links_markdown(
            sources,
            config.docs_portal_doc_user,
            config.docs_portal_doc_ai,
        )
        if source_links:
            st.markdown(source_links)
        enriched = build_enriched_source_rows(
            sources,
            config.docs_portal_doc_user,
            config.docs_portal_doc_ai,
        )
        st.dataframe(
            enriched,
            column_config={
                "portal_url": st.column_config.LinkColumn("Portal", display_text="Otwórz ↗")
            },
            width="stretch",
            height=min(360, 80 + 36 * len(enriched)),
        )
    if show_trace:
        with st.expander("Trace agentów", expanded=True):
            for step in event.get("trace", []):
                st.write(f"**{step.get('role')}:** {step.get('message')}")


def render_metrics(stats: dict[str, Any]) -> None:
    if not stats:
        return
    col_total, col_retrieval, col_generation, col_ttft = st.columns(4)
    col_total.metric("Total", _format_seconds(stats.get("total_sec")))
    col_retrieval.metric("Retrieval", _format_seconds(stats.get("retrieval_sec")))
    col_generation.metric("Generacja", _format_seconds(stats.get("generation_sec")))
    col_ttft.metric("TTFT", _format_seconds(stats.get("time_to_first_token_sec")))
    with st.expander("Metryki techniczne"):
        st.json(stats)


def render_search_tab(config: AppConfig, default_rag_profile: str) -> None:
    st.subheader("Wyszukiwarka semantyczna")
    st.caption("Tu testujesz retrieval, bez generowania odpowiedzi przez LLM.")
    question = st.text_input("Zapytanie")
    rag_keys = [profile.key for profile in list_rag_profiles()]
    rag_profile = st.selectbox(
        "Profil RAG",
        options=rag_keys,
        index=model_option_index(rag_keys, default_rag_profile),
        format_func=lambda key: get_rag_profile(key).label,
    )
    top_k = st.number_input("Top K", min_value=1, max_value=30, value=config.top_k)
    st.caption(f"Embedding: `{config.embedding_model}`")
    if st.button("Szukaj"):
        if not question.strip():
            st.warning("Wpisz zapytanie.")
            return
        try:
            hits = RetrievalService(config).search_with_profile(question.strip(), profile=get_rag_profile(rag_profile), top_k=int(top_k))
        except Exception as exc:  # noqa: BLE001
            st.error(f"Błąd wyszukiwania: {exc}")
            return
        if not hits:
            st.warning("Brak trafień.")
        for hit in hits:
            st.markdown(f"**{hit.source_path}**")
            portal_link = _portal_markdown_link(
                hit.source_path,
                config.docs_portal_doc_user,
                config.docs_portal_doc_ai,
            )
            if portal_link:
                st.markdown(portal_link)
            st.caption(
                f"{hit.metadata.get('heading_path', 'ROOT')} | {hit.metadata.get('source_type', '-')} | "
                f"entity={hit.metadata.get('entity', '-')} | table={hit.metadata.get('table', '-')} | "
                f"endpoint={hit.metadata.get('endpoint', '-')} | distance={hit.distance:.6f}"
            )
            st.code(hit.text[:1500], language="markdown")


def render_sources_tab(config: AppConfig) -> None:
    st.subheader("Źródła dokumentacji")
    documents, skipped = discover_documents(config)
    col_docs, col_skipped = st.columns(2)
    col_docs.metric("Pliki .md w bazie", len(documents))
    col_skipped.metric("Pominięte", skipped)
    st.caption("Baza odpowiedzi obejmuje `InvoiceJet/doc_AI` i `InvoiceJet/doc_user`; metadane są wyprowadzane ze ścieżek.")
    rows = [
        {
            "source_group": document.source_group,
            "source_type": document.source_type,
            "area": document.area,
            "entity": document.entity,
            "screen": document.screen,
            "process": document.process,
            "table": document.table,
            "endpoint": document.endpoint,
            "priority": document.priority,
            "relative_path": document.relative_path,
        }
        for document in documents
    ]
    enriched_rows = build_enriched_source_rows(
        rows,
        config.docs_portal_doc_user,
        config.docs_portal_doc_ai,
    )
    st.dataframe(
        enriched_rows,
        column_config={
            "portal_url": st.column_config.LinkColumn("Portal", display_text="Otwórz ↗")
        },
        width="stretch",
        height=560,
    )


def render_index_tab(config: AppConfig) -> None:
    st.subheader("Index Manager")
    render_index_status(config)
    st.caption("Po tej zmianie wykonaj Force rebuild, bo manifest v2 dodaje metadane typów źródeł.")
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


def render_evaluation_tab(config: AppConfig) -> None:
    st.subheader("Evaluation Lab")
    st.caption("Golden set mierzy, czy profile RAG znajdują oczekiwane źródła dla pytań przekrojowych.")
    mode = st.radio("Tryb", options=["retrieval", "answer"], horizontal=True, help="answer uruchamia pełne LLM i będzie wolniejsze.")
    limit = st.number_input("Limit przypadków", min_value=1, max_value=50, value=12)
    if st.button("Uruchom ewaluację", type="primary"):
        with st.spinner("Uruchamiam evaluation lab..."):
            results = run_eval_set(config, mode=mode, limit=int(limit))
        summary = summarize_results(results)
        col_total, col_ok, col_fail, col_rate = st.columns(4)
        col_total.metric("Total", summary["total"])
        col_ok.metric("Passed", summary["passed"])
        col_fail.metric("Failed", summary["failed"])
        col_rate.metric("Pass rate", f"{summary['pass_rate']:.0%}")
        rows = [result_to_row(result) for result in results]
        st.dataframe(rows, width="stretch", height=520)


def render_agents_models_tab(config: AppConfig, active_profile: AgentProfile) -> None:
    st.subheader("Agenci i modele")
    st.caption("Agenci, modele i prompty są profilami konfiguracyjnymi w katalogu `profiles`.")
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
                "model_profile": profile.model_profile,
                "prompt_profile": profile.prompt_profile,
                "rag_profile": profile.rag_profile,
                "LLM": profile.llm_model,
                "embedding": profile.embedding_model,
                "dostępny": all(is_model_available(model, available) for model in profile.required_models),
            }
            for profile in profiles
        ],
        width="stretch",
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

    with st.expander("Profile modeli"):
        st.dataframe([profile.__dict__ for profile in list_model_profiles(config.tool_root)], width="stretch")
    with st.expander("Prompt Studio - podgląd profili"):
        st.dataframe([profile.__dict__ for profile in list_prompt_profiles(config.tool_root)], width="stretch")
    with st.expander("Profile RAG"):
        st.dataframe([profile.__dict__ for profile in list_rag_profiles()], width="stretch")
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
        width="stretch",
    )


def render_diagnostics_tab(config: AppConfig, scope: str, rag_profile: str, prompt_profile: str) -> None:
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
        run_rag_test(config, scope, rag_profile, prompt_profile, "Jak wygląda proces rejestracji i logowania w InvoiceJet?", False)
    if col_fallback.button("Test braku w dokumentacji"):
        run_rag_test(config, scope, rag_profile, prompt_profile, "Jaka będzie jutro pogoda w Warszawie?", True)


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
    col_files, col_chunks, col_embedding, col_schema = st.columns(4)
    col_files.metric("Pliki w manifeście", len(files))
    col_chunks.metric("Chunki", chunk_count)
    col_embedding.metric("Embedding indeksu", manifest.get("embedding_model", "-"))
    col_schema.metric("Schema", manifest.get("schema_version", "-"))
    if int(manifest.get("schema_version", 0) or 0) < 2:
        st.warning("Manifest jest starszy niż v2. Wykonaj Force rebuild, aby dodać metadane typów źródeł.")


def run_rag_test(config: AppConfig, scope: str, rag_profile: str, prompt_profile: str, question: str, expect_fallback: bool) -> None:
    with st.spinner("Uruchamiam test RAG..."):
        try:
            result = OracleOrchestrator(config).answer(
                question,
                requested_scope=scope,
                requested_rag_profile=rag_profile,
                prompt_profile_key=prompt_profile,
            )
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
    return f"{profile.name} - {profile.role}"


def llm_model_options(allowed_models: Sequence[str], profiles: Sequence[AgentProfile], model_profiles) -> list[str]:
    profile_models = [profile.llm_model for profile in profiles]
    configured = [profile.llm_model for profile in model_profiles]
    allowed_llms = [model for model in allowed_models if model not in {"bge-m3", "nomic-embed-text"}]
    return unique_items([*profile_models, *configured, *allowed_llms])


def embedding_model_options(allowed_models: Sequence[str], profiles: Sequence[AgentProfile], model_profiles) -> list[str]:
    profile_models = [profile.embedding_model for profile in profiles]
    configured = [profile.embedding_model for profile in model_profiles]
    allowed_embeddings = [model for model in allowed_models if model in {"bge-m3", "nomic-embed-text"}]
    return unique_items([*profile_models, *configured, *allowed_embeddings])


def model_option_index(options: Sequence[str], selected: str) -> int:
    return list(options).index(selected) if selected in options else 0


def think_to_option(value: bool | str | None) -> str:
    if value is None:
        return "auto"
    if isinstance(value, bool):
        return "on" if value else "off"
    return value if value in {"low", "medium", "high"} else "auto"


def option_to_think(value: str) -> bool | str | None:
    if value == "auto":
        return None
    if value == "on":
        return True
    if value == "off":
        return False
    return value


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


def _format_seconds(value: Any) -> str:
    if value is None:
        return "-"
    try:
        return f"{float(value):.2f}s"
    except (TypeError, ValueError):
        return "-"


if __name__ == "__main__":
    main()
