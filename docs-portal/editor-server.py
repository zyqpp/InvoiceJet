#!/usr/bin/env python3
"""
InvoiceJet Docs — Serwer edycji plików (port 8010)

Gdy użytkownik kliknie "Edytuj plik" na portalu MkDocs, przeglądarka
wywołuje http://127.0.0.1:8010/edit?path=<ścieżka_do_pliku>.
Ten serwer otwiera systemowe okno "Otwórz za pomocą..." Windows
lub bezpośrednio edytor (jeśli skonfigurowany).

Uruchomienie:
    python editor-server.py
    python editor-server.py --port 8010 --editor notepad++
"""

import argparse
import subprocess
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote


def open_with_dialog(file_path: str, editor: str = None):
    """Otwiera plik w edytorze lub Windows 'Otwórz za pomocą'."""
    if not os.path.exists(file_path):
        return False, f"Plik nie istnieje: {file_path}"

    if editor:
        # Bezpośrednie otwarcie w skonfigurowanym edytorze
        try:
            subprocess.Popen([editor, file_path])
            return True, f"Otwarto w {editor}"
        except FileNotFoundError:
            # Fallback do dialogu Windows jeśli edytor nie znaleziony
            pass

    # Okno "Otwórz za pomocą..." Windows
    try:
        subprocess.Popen(
            ['rundll32.exe', 'shell32.dll,OpenAs_RunDLL', file_path]
        )
        return True, "Otwarto dialog wyboru edytora"
    except Exception as e:
        # Ostatni fallback - domyślna aplikacja
        try:
            os.startfile(file_path)
            return True, "Otwarto w domyślnej aplikacji"
        except Exception as e2:
            return False, str(e2)


class EditHandler(BaseHTTPRequestHandler):
    editor = None  # ustawiane z argparse

    def log_message(self, format, *args):
        # Tylko błędy w konsoli, nie każde żądanie
        if args[1] != '200':
            super().log_message(format, *args)

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Content-Type', 'application/json; charset=utf-8')

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == '/health':
            self.send_response(200)
            self._cors_headers()
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return

        if parsed.path == '/edit':
            params = parse_qs(parsed.query)
            raw_path = params.get('path', [''])[0]
            file_path = unquote(raw_path).replace('/', os.sep)

            print(f"  📝 Edytuj: {file_path}")
            ok, msg = open_with_dialog(file_path, self.editor)

            status = 200 if ok else 400
            self.send_response(status)
            self._cors_headers()
            self.end_headers()
            response = f'{{"ok":{str(ok).lower()},"msg":"{msg}"}}'
            self.wfile.write(response.encode())
            return

        self.send_response(404)
        self.end_headers()


def main():
    parser = argparse.ArgumentParser(
        description='InvoiceJet Docs — serwer edycji plików'
    )
    parser.add_argument('--port', type=int, default=8010,
                        help='Port serwera (domyślnie: 8010)')
    parser.add_argument('--editor', type=str, default=None,
                        help='Ścieżka do edytora, np. "notepad++" lub "code"')
    args = parser.parse_args()

    EditHandler.editor = args.editor

    server = HTTPServer(('127.0.0.1', args.port), EditHandler)
    editor_info = f"edytor: {args.editor}" if args.editor else "Windows 'Otwórz za pomocą'"
    print(f"✏️  Serwer edycji uruchomiony na http://127.0.0.1:{args.port}")
    print(f"   {editor_info}")
    print(f"   Ctrl+C aby zatrzymać\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSerwer zatrzymany.")


if __name__ == '__main__':
    main()
