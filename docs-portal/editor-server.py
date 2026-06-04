#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
from uuid import uuid4


HOST = "127.0.0.1"
DEFAULT_PORT = int(os.environ.get("DOCS_EDITOR_PORT", "8010"))
DOC_STATUSES = ("draft", "review", "accepted", "changed", "deprecated")
COMMENT_STATUSES = ("new", "handled", "rejected")

PORTAL_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PORTAL_ROOT.parent
DOC_AI_ROOT = (REPO_ROOT / "InvoiceJet" / "doc_AI").resolve()
DOC_USER_ROOT = (REPO_ROOT / "InvoiceJet" / "doc_user").resolve()
STORAGE_DIR = REPO_ROOT / ".docreview"
COMMENTS_FILE = STORAGE_DIR / "comments.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def now_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def is_relative_to(path_value: Path, root: Path) -> bool:
    try:
        path_value.relative_to(root)
        return True
    except ValueError:
        return False


def safe_doc_path(raw_path: str) -> Path:
    if not raw_path:
        raise ValueError("Brakuje sciezki dokumentu.")
    candidate = Path(unquote(raw_path)).expanduser().resolve()
    if not candidate.is_file():
        raise FileNotFoundError(f"Plik nie istnieje: {candidate}")
    if not candidate.suffix.lower() == ".md":
        raise ValueError("Edytor obsluguje tylko pliki Markdown.")
    if not (is_relative_to(candidate, DOC_AI_ROOT) or is_relative_to(candidate, DOC_USER_ROOT)):
        raise ValueError("Dostep poza InvoiceJet/doc_AI i InvoiceJet/doc_user jest zablokowany.")
    return candidate


def doc_key(path_value: Path) -> str:
    return path_value.relative_to(REPO_ROOT).as_posix()


def read_text(path_value: Path) -> str:
    return path_value.read_text(encoding="utf-8")


def write_text(path_value: Path, content: str) -> None:
    path_value.write_text(content, encoding="utf-8")


def parse_front_matter(content: str) -> tuple[dict[str, str], str]:
    if not content.startswith("---"):
        return {}, content
    match = re.match(r"^---\r?\n([\s\S]*?)\r?\n---\r?\n?", content)
    if not match:
        return {}, content
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        if key:
            meta[key] = value.strip()
    return meta, content[match.end() :]


def format_front_matter(meta: dict[str, str], body: str) -> str:
    lines = ["---"]
    for key, value in meta.items():
        if value is None or str(value) == "":
            continue
        lines.append(f"{key}: {value}")
    lines.extend(["---", ""])
    return "\n".join(lines) + body.lstrip()


def extract_title(content: str, fallback: str) -> str:
    _, body = parse_front_matter(content)
    match = re.search(r"^\s*#\s+(.+?)\s*$", body, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def ensure_storage() -> None:
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    if not COMMENTS_FILE.exists():
        COMMENTS_FILE.write_text("[]\n", encoding="utf-8")


def load_comments() -> list[dict[str, str]]:
    ensure_storage()
    try:
        data = json.loads(COMMENTS_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def save_comments(comments: list[dict[str, str]]) -> None:
    ensure_storage()
    COMMENTS_FILE.write_text(json.dumps(comments, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def json_response(handler: BaseHTTPRequestHandler, status: int, payload: object) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, PUT, PATCH, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def html_response(handler: BaseHTTPRequestHandler, html: str) -> None:
    body = html.encode("utf-8")
    handler.send_response(200)
    handler.send_header("Cache-Control", "no-store")
    handler.send_header("Content-Type", "text/html; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def read_body(handler: BaseHTTPRequestHandler) -> dict[str, object]:
    length = int(handler.headers.get("Content-Length", "0") or "0")
    if length <= 0:
        return {}
    raw = handler.rfile.read(length).decode("utf-8")
    return json.loads(raw or "{}")


def editor_html(raw_path: str) -> str:
    encoded_path = json.dumps(raw_path, ensure_ascii=False)
    statuses = json.dumps(DOC_STATUSES)
    comment_statuses = json.dumps(COMMENT_STATUSES)
    return f"""<!doctype html>
<html lang="pl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Edytor dokumentu</title>
  <style>
    :root {{
      color-scheme: light dark;
      font-family: Inter, Segoe UI, system-ui, sans-serif;
      --border: #d6d8df;
      --muted: #687080;
      --panel: #f6f7f9;
      --accent: #1f6feb;
    }}
    body {{ margin: 0; color: #172033; background: #fff; }}
    header {{ display: flex; gap: 12px; align-items: center; padding: 12px 16px; border-bottom: 1px solid var(--border); background: var(--panel); }}
    header h1 {{ margin: 0; font-size: 17px; font-weight: 650; flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    main {{ display: grid; grid-template-columns: minmax(0, 1fr) 360px; min-height: calc(100vh - 57px); }}
    .editor {{ display: flex; flex-direction: column; min-width: 0; }}
    .toolbar {{ display: flex; gap: 8px; align-items: center; padding: 10px 12px; border-bottom: 1px solid var(--border); }}
    textarea#content {{ flex: 1; width: 100%; box-sizing: border-box; border: 0; outline: none; resize: none; padding: 18px; font: 14px/1.55 Consolas, "Roboto Mono", monospace; }}
    aside {{ border-left: 1px solid var(--border); background: #fbfbfc; padding: 14px; overflow: auto; }}
    button, select, input, textarea {{ font: inherit; }}
    button, a.button {{ border: 1px solid var(--border); background: #fff; color: #172033; border-radius: 6px; padding: 7px 10px; text-decoration: none; cursor: pointer; }}
    button.primary {{ background: var(--accent); border-color: var(--accent); color: #fff; }}
    select, input, textarea.comment-text {{ border: 1px solid var(--border); border-radius: 6px; padding: 7px 8px; background: #fff; color: #172033; }}
    .path, .hint, .state {{ color: var(--muted); font-size: 12px; }}
    .path {{ padding: 8px 12px; border-bottom: 1px solid var(--border); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .comment {{ border: 1px solid var(--border); border-radius: 8px; background: #fff; padding: 10px; margin: 10px 0; }}
    .comment p {{ margin: 0 0 8px; white-space: pre-wrap; }}
    .comment .meta {{ display: flex; gap: 8px; align-items: center; justify-content: space-between; }}
    .comment-text {{ width: 100%; min-height: 76px; box-sizing: border-box; resize: vertical; }}
    @media (prefers-color-scheme: dark) {{
      body {{ background: #111827; color: #e5e7eb; }}
      header, .toolbar, aside {{ background: #172033; }}
      textarea#content, button, a.button, select, input, textarea.comment-text, .comment {{ background: #111827; color: #e5e7eb; border-color: #374151; }}
      :root {{ --border: #374151; --muted: #9ca3af; --panel: #172033; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1 id="title">Edytor dokumentu</h1>
    <span id="state" class="state">Ladowanie...</span>
    <button id="reload">Odswiez</button>
    <button id="save" class="primary">Zapisz</button>
  </header>
  <main>
    <section class="editor">
      <div class="path" id="path"></div>
      <div class="toolbar">
        <label>Status <select id="status"></select></label>
        <button id="save-status">Zapisz status</button>
        <span class="hint">Zmiany zapisuja plik Markdown. MkDocs odswiezy podglad po zapisie.</span>
      </div>
      <textarea id="content" spellcheck="false"></textarea>
    </section>
    <aside>
      <h2>Komentarze</h2>
      <textarea id="new-comment" class="comment-text" placeholder="Dodaj komentarz do dokumentu"></textarea>
      <div style="display:flex;gap:8px;margin-top:8px;">
        <button id="add-comment" class="primary">Dodaj</button>
      </div>
      <div id="comments"></div>
    </aside>
  </main>
  <script>
    const rawPath = {encoded_path};
    const docStatuses = {statuses};
    const commentStatuses = {comment_statuses};
    let docKey = "";

    const $ = (id) => document.getElementById(id);
    const setState = (text) => $("state").textContent = text;
    const api = async (url, options = {{}}) => {{
      const response = await fetch(url, {{
        ...options,
        headers: {{ "Content-Type": "application/json", ...(options.headers || {{}}) }},
      }});
      const data = await response.json();
      if (!response.ok || data.error) throw new Error(data.error || "Blad API");
      return data;
    }};

    function fillStatus(value) {{
      $("status").innerHTML = "";
      for (const status of docStatuses) {{
        const option = document.createElement("option");
        option.value = status;
        option.textContent = status;
        option.selected = status === value;
        $("status").appendChild(option);
      }}
    }}

    async function loadDoc() {{
      setState("Ladowanie...");
      const data = await api("/api/doc?path=" + encodeURIComponent(rawPath));
      docKey = data.key;
      $("title").textContent = data.title;
      $("path").textContent = data.key;
      $("content").value = data.content;
      fillStatus(data.meta.status || "draft");
      await loadComments();
      setState("Gotowe");
    }}

    async function saveDoc() {{
      setState("Zapisywanie...");
      await api("/api/doc", {{
        method: "PUT",
        body: JSON.stringify({{ path: rawPath, content: $("content").value }}),
      }});
      setState("Zapisano " + new Date().toLocaleTimeString());
    }}

    async function saveStatus() {{
      setState("Zapisywanie statusu...");
      const data = await api("/api/doc/meta", {{
        method: "PATCH",
        body: JSON.stringify({{ path: rawPath, key: "status", value: $("status").value }}),
      }});
      $("content").value = data.content;
      setState("Status zapisany");
    }}

    async function loadComments() {{
      const data = await api("/api/comments?path=" + encodeURIComponent(docKey));
      const box = $("comments");
      box.innerHTML = "";
      if (!data.comments.length) {{
        box.innerHTML = '<p class="hint">Brak komentarzy.</p>';
        return;
      }}
      for (const item of data.comments) {{
        const el = document.createElement("div");
        el.className = "comment";
        const select = commentStatuses.map((status) =>
          `<option value="${{status}}" ${{status === item.status ? "selected" : ""}}>${{status}}</option>`
        ).join("");
        el.innerHTML = `
          <p>${{escapeHtml(item.text)}}</p>
          ${{item.quote ? `<p class="hint">${{escapeHtml(item.quote)}}</p>` : ""}}
          <div class="meta">
            <span class="hint">${{new Date(item.updatedAt || item.createdAt).toLocaleString()}}</span>
            <select data-id="${{item.id}}">${{select}}</select>
          </div>
        `;
        box.appendChild(el);
      }}
      box.querySelectorAll("select[data-id]").forEach((select) => {{
        select.addEventListener("change", async () => {{
          await api("/api/comments/" + encodeURIComponent(select.dataset.id), {{
            method: "PATCH",
            body: JSON.stringify({{ status: select.value }}),
          }});
          await loadComments();
        }});
      }});
    }}

    async function addComment() {{
      const text = $("new-comment").value.trim();
      if (!text) return;
      await api("/api/comments", {{
        method: "POST",
        body: JSON.stringify({{ path: docKey, text }}),
      }});
      $("new-comment").value = "";
      await loadComments();
    }}

    function escapeHtml(value) {{
      return String(value || "").replace(/[&<>"']/g, (ch) => ({{
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;",
      }}[ch]));
    }}

    $("reload").addEventListener("click", loadDoc);
    $("save").addEventListener("click", saveDoc);
    $("save-status").addEventListener("click", saveStatus);
    $("add-comment").addEventListener("click", addComment);
    $("content").addEventListener("keydown", (event) => {{
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "s") {{
        event.preventDefault();
        saveDoc();
      }}
    }});
    loadDoc().catch((error) => setState(error.message));
  </script>
</body>
</html>"""


def open_external(path_value: Path, editor: str | None) -> tuple[bool, str]:
    if not editor:
        return False, "Nie skonfigurowano zewnetrznego edytora."
    try:
        subprocess.Popen([editor, str(path_value)])
        return True, f"Otwarto w {editor}"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


class EditHandler(BaseHTTPRequestHandler):
    external_editor: str | None = None

    def log_message(self, format: str, *args: object) -> None:
        if len(args) > 1 and args[1] == "200":
            return
        super().log_message(format, *args)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, PATCH, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        try:
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            if parsed.path == "/health":
                return json_response(self, 200, {"ok": True, "port": self.server.server_port})
            if parsed.path == "/edit":
                raw_path = params.get("path", [""])[0]
                safe_doc_path(raw_path)
                return html_response(self, editor_html(raw_path))
            if parsed.path == "/api/doc":
                path_value = safe_doc_path(params.get("path", [""])[0])
                content = read_text(path_value)
                meta, _ = parse_front_matter(content)
                return json_response(self, 200, {
                    "path": str(path_value),
                    "key": doc_key(path_value),
                    "title": extract_title(content, path_value.stem),
                    "content": content,
                    "meta": meta,
                })
            if parsed.path == "/api/comments":
                key = params.get("path", [""])[0]
                comments = [item for item in load_comments() if item.get("path") == key]
                comments.sort(key=lambda item: item.get("updatedAt") or item.get("createdAt") or "", reverse=True)
                return json_response(self, 200, {"comments": comments})
            if parsed.path == "/open-external":
                path_value = safe_doc_path(params.get("path", [""])[0])
                ok, message = open_external(path_value, self.external_editor)
                return json_response(self, 200 if ok else 400, {"ok": ok, "message": message})
            return json_response(self, 404, {"error": "Nie znaleziono endpointu."})
        except Exception as exc:  # noqa: BLE001
            return json_response(self, 400, {"error": str(exc)})

    def do_PUT(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path != "/api/doc":
                return json_response(self, 404, {"error": "Nie znaleziono endpointu."})
            payload = read_body(self)
            path_value = safe_doc_path(str(payload.get("path") or ""))
            content = str(payload.get("content") or "")
            write_text(path_value, content)
            return json_response(self, 200, {"ok": True, "key": doc_key(path_value)})
        except Exception as exc:  # noqa: BLE001
            return json_response(self, 400, {"error": str(exc)})

    def do_PATCH(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path == "/api/doc/meta":
                payload = read_body(self)
                path_value = safe_doc_path(str(payload.get("path") or ""))
                key = str(payload.get("key") or "").strip()
                value = str(payload.get("value") or "").strip()
                if key != "status":
                    raise ValueError("Dozwolona jest tylko zmiana pola status.")
                if value not in DOC_STATUSES:
                    raise ValueError("Nieprawidlowy status dokumentu.")
                content = read_text(path_value)
                meta, body = parse_front_matter(content)
                meta["status"] = value
                meta["ostatnia_aktualizacja"] = now_date()
                next_content = format_front_matter(meta, body)
                write_text(path_value, next_content)
                return json_response(self, 200, {"ok": True, "content": next_content, "meta": meta})
            if parsed.path.startswith("/api/comments/"):
                comment_id = unquote(parsed.path[len("/api/comments/") :])
                payload = read_body(self)
                comments = load_comments()
                for item in comments:
                    if item.get("id") == comment_id:
                        if "status" in payload:
                            status = str(payload.get("status") or "").strip()
                            if status not in COMMENT_STATUSES:
                                raise ValueError("Nieprawidlowy status komentarza.")
                            item["status"] = status
                        if "text" in payload:
                            text = str(payload.get("text") or "").strip()
                            if not text:
                                raise ValueError("Komentarz nie moze byc pusty.")
                            item["text"] = text
                        item["updatedAt"] = now_iso()
                        save_comments(comments)
                        return json_response(self, 200, {"comment": item})
                raise FileNotFoundError("Komentarz nie istnieje.")
            return json_response(self, 404, {"error": "Nie znaleziono endpointu."})
        except Exception as exc:  # noqa: BLE001
            return json_response(self, 400, {"error": str(exc)})

    def do_POST(self) -> None:
        try:
            parsed = urlparse(self.path)
            if parsed.path != "/api/comments":
                return json_response(self, 404, {"error": "Nie znaleziono endpointu."})
            payload = read_body(self)
            key = str(payload.get("path") or "").strip()
            text = str(payload.get("text") or "").strip()
            quote = str(payload.get("quote") or "").strip()
            if not key or not text:
                raise ValueError("Komentarz wymaga path i text.")
            now = now_iso()
            record = {
                "id": str(uuid4()),
                "path": key,
                "text": text,
                "quote": quote,
                "status": "new",
                "createdAt": now,
                "updatedAt": now,
            }
            comments = load_comments()
            comments.append(record)
            save_comments(comments)
            return json_response(self, 201, {"comment": record})
        except Exception as exc:  # noqa: BLE001
            return json_response(self, 400, {"error": str(exc)})


def main() -> int:
    parser = argparse.ArgumentParser(description="InvoiceJet MkDocs web editor")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port serwera edycji, domyslnie 8010.")
    parser.add_argument("--editor", default="", help="Opcjonalny zewnetrzny edytor dla /open-external.")
    args = parser.parse_args()

    ensure_storage()
    EditHandler.external_editor = args.editor or None
    server = HTTPServer((HOST, args.port), EditHandler)
    print(f"Docs editor: http://{HOST}:{args.port}")
    print(f"Dozwolone katalogi: {DOC_AI_ROOT} | {DOC_USER_ROOT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Serwer edycji zatrzymany.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
