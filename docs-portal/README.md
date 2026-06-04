# InvoiceJet Docs Portal

Lokalny portal dokumentacji InvoiceJet oparty na **MkDocs + Material theme**.
Uruchamia dwa serwery HTTP z nawigacją, wyszukiwarką i webowym edytorem plików Markdown.

```
InvoiceJet/doc_AI/     -> Portal techniczny   http://127.0.0.1:8001
InvoiceJet/doc_user/   -> Portal użytkownika  http://127.0.0.1:8002
docs-portal/           -> konfiguracja MkDocs i edytor
```

Edytor działa jako osobny lokalny serwer na `http://127.0.0.1:8010`. Przycisk **Edytuj** w portalu MkDocs otwiera właściwy plik `.md` w przeglądarce, z możliwością zapisu treści, zmiany statusu i dodania komentarzy.

---

## Wymagania

| Wymaganie | Wersja | Sprawdzenie |
|---|---:|---|
| Python | 3.8+ | `python --version` |
| pip | dowolna | `pip --version` |
| Internet | jednorazowo | instalacja pakietów MkDocs |

---

## Pierwsze uruchomienie

```powershell
cd "ścieżka\do\InvoiceJet\docs-portal"
.\setup.ps1
```

Domyślnie skrypt uruchamia:

| Usługa | Port |
|---|---:|
| Dokumentacja techniczna `doc_AI` | 8001 |
| Dokumentacja użytkownika `doc_user` | 8002 |
| Webowy edytor dokumentów | 8010 |

Własne porty:

```powershell
.\setup.ps1 -PortAI 9001 -PortUser 9002 -EditorPort 9010
.\setup.ps1 -Host 192.168.1.10 -PortAI 9001 -PortUser 9002
```

`setup.ps1` instaluje zależności, generuje lokalne `mkdocs.yml`, synchronizuje `tools/oracle_invoicejet/.env` i uruchamia portale.

---

## Codzienne uruchomienie

```powershell
cd "ścieżka\do\InvoiceJet\docs-portal"
.\start-docs.ps1
```

Jeśli Windows blokuje `.ps1` jako niepodpisany skrypt, uruchom:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\start-docs.ps1
```

`start-docs.ps1` uruchamia oba portale oraz edytor. Przed startem aktualizuje:

- `site_url` w obu plikach `mkdocs.yml`,
- `extra.editor_url` i `extra.source_dir` dla przycisku **Edytuj**,
- `extra.portal.doc_ai_url` i `extra.portal.doc_user_url` dla przełącznika portali,
- `ORACLE_DOCS_PORTAL_DOC_AI` i `ORACLE_DOCS_PORTAL_DOC_USER` w lokalnym `.env` Oracle.

Opcje:

```powershell
.\start-docs.ps1 -Host 192.168.1.10 -PortAI 9001 -PortUser 9002 -EditorPort 9010
.\start-docs.ps1 -OracleEnvPath "..\tools\oracle_invoicejet\.env"
.\start-docs.ps1 -NoEditor
.\start-docs.ps1 -EnableKroki
```

Zmiany w plikach `.md` są widoczne po zapisie dzięki live-reload MkDocs. Zmiany w `overrides/main.html` wymagają restartu `start-docs.ps1`.

Plugin `kroki` dla diagramów PlantUML jest domyślnie wyłączony, żeby portal techniczny startował także bez internetu. Włącz go parametrem `-EnableKroki`, jeśli masz dostęp do `https://kroki.io`.

---

## Zatrzymanie

```powershell
.\stop-docs.ps1
.\stop-docs.ps1 -PortAI 9001 -PortUser 9002 -EditorPort 9010
.\stop-docs.ps1 -NoEditor
```

Skrypt zatrzymuje procesy nasłuchujące na portach portali i edytora.

---

## Edycja dokumentów

1. Uruchom `.\start-docs.ps1`.
2. Wejdź do portalu MkDocs na `8001` albo `8002`.
3. Otwórz dokument.
4. Kliknij **Edytuj** w górnym pasku.
5. W nowej karcie edytuj Markdown, status lub komentarze.
6. Kliknij **Zapisz**.

Komentarze są zapisywane lokalnie w `.docreview/comments.json`. Ten folder jest ignorowany przez git i nie trafia do indeksu RAG.

Edytor dopuszcza zapis tylko w:

- `InvoiceJet/doc_AI`
- `InvoiceJet/doc_user`

Ścieżki spoza tych katalogów są blokowane.

---

## Skrypty

### `setup.ps1`

Jednorazowy setup na nowym komputerze.

```text
-Host <string>
-PortAI <int>
-PortUser <int>
-EditorPort <int>
-NoEditor
-EnableKroki
-OracleEnvPath <path>
```

### `start-docs.ps1`

Codzienne uruchomienie portali. Automatycznie synchronizuje linki portali, ścieżki źródłowe i lokalny `.env` Oracle.

```text
-Host <string>
-PortAI <int>
-PortUser <int>
-EditorPort <int>
-NoEditor
-OracleEnvPath <path>
```

### `start-editor.ps1`

Uruchamia tylko webowy edytor Markdown.

```powershell
.\start-editor.ps1
.\start-editor.ps1 -Port 8011
```

Parametr `-Editor` zostaje jako opcjonalny fallback dla endpointu `/open-external`, ale standardowa edycja odbywa się w przeglądarce.

### `editor-server.py`

Serwer edycji bez zależności zewnętrznych.

```powershell
python editor-server.py --port 8010
```

Najważniejsze endpointy:

| Endpoint | Rola |
|---|---|
| `GET /edit?path=...` | strona edytora |
| `GET /api/doc?path=...` | pobranie treści dokumentu |
| `PUT /api/doc` | zapis dokumentu |
| `PATCH /api/doc/meta` | zmiana statusu dokumentu |
| `GET /api/comments?path=...` | komentarze dokumentu |
| `POST /api/comments` | dodanie komentarza |
| `PATCH /api/comments/<id>` | zmiana komentarza |

---

## Konfiguracja linkowania

Przycisk **Edytuj** w `doc-ai/overrides/main.html` i `doc-user/overrides/main.html` buduje link z dwóch wartości MkDocs:

```yaml
extra:
  editor_url: "http://127.0.0.1:8010"
  source_dir: "G:/.../InvoiceJet/InvoiceJet/doc_AI"
```

Dla portalu użytkownika `source_dir` wskazuje na `InvoiceJet/doc_user`.

Przykłady mapowania:

| URL w MkDocs | Plik źródłowy |
|---|---|
| `/` | `README.md` |
| `/index.html` | `README.md` |
| `/01_ekrany/index.html` | `01_ekrany/README.md` |
| `/01_ekrany/faktury.html` | `01_ekrany/faktury.md` |

Jeśli zmieniasz port edytora, użyj `-EditorPort`. Jeśli dokumentacja ma być dostępna w sieci lokalnej, użyj `-Host` dla portali MkDocs.

---

## Dodawanie dokumentacji

Nowy plik w istniejącym folderze:

```text
InvoiceJet/doc_AI/XX_folder/nowy-plik.md
InvoiceJet/doc_user/XX_folder/nowy-plik.md
```

Nowa sekcja:

1. Dodaj folder, np. `InvoiceJet/doc_AI/11_nowy_obszar`.
2. Dodaj `README.md`.
3. Opcjonalnie dodaj `.pages`, jeśli chcesz kontrolować kolejność nawigacji.
4. Po zapisie MkDocs odświeży portal.

---

## Rozwiązywanie problemów

### Port jest zajęty

```powershell
.\stop-docs.ps1
.\start-docs.ps1
```

Albo wybierz inne porty:

```powershell
.\start-docs.ps1 -PortAI 9001 -PortUser 9002 -EditorPort 9010
```

### Nie widać przycisku Edytuj

Zrestartuj portale, bo zmiany w `overrides/main.html` nie są przeładowywane automatycznie:

```powershell
.\stop-docs.ps1
.\start-docs.ps1
```

### Kliknięcie Edytuj nie otwiera edytora

Sprawdź, czy działa serwer edycji:

```powershell
Invoke-RestMethod http://127.0.0.1:8010/health
```

Jeśli nie działa:

```powershell
.\start-editor.ps1
```

### Edytor pokazuje błąd ścieżki

Sprawdź `extra.source_dir` w odpowiednim `mkdocs.yml`. Powinien wskazywać fizyczny katalog `InvoiceJet/doc_AI` albo `InvoiceJet/doc_user`.

---

## Struktura

```text
docs-portal/
├── README.md
├── setup.ps1
├── start-docs.ps1
├── stop-docs.ps1
├── start-editor.ps1
├── editor-server.py
├── doc-ai/
│   ├── mkdocs.yml
│   └── overrides/main.html
└── doc-user/
    ├── mkdocs.yml
    └── overrides/main.html
```

---

## Technologie

| Pakiet | Rola |
|---|---|
| MkDocs | budowanie HTML z Markdown |
| MkDocs Material | motyw, nawigacja, wyszukiwarka |
| mkdocs-awesome-pages-plugin | kolejność i filtrowanie nawigacji |
| Python `http.server` | lokalny webowy edytor dokumentów |
