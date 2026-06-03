# InvoiceJet Docs Portal

Lokalny portal dokumentacji dla projektu InvoiceJet oparty na **MkDocs + Material theme**.
Uruchamia dwa niezależne serwery HTTP z pełną nawigacją, wyszukiwarką i możliwością edycji plików.

---

## Idea portalu

Dokumentacja projektu żyje jako pliki `.md` w folderach `doc_AI/` i `doc_user/`.
Portal **nie modyfikuje** tych plików — czyta je i wyświetla jako ładne strony HTML z:

- **Lewym sidebarem** — drzewo nawigacji zwężające się do aktywnej sekcji
- **Górnym paskiem kategorii** — szybkie przeskakiwanie między głównymi sekcjami
- **Prawym spisem treści** — linki do nagłówków bieżącego dokumentu
- **Wyszukiwarką** — full-text po całej dokumentacji
- **Przyciskiem edycji** — otwiera plik w edytorze na dysku

```
doc_AI/        ← pliki źródłowe (niezmieniane)   → Portal Techniczny http://127.0.0.1:8001
doc_user/      ← pliki źródłowe (niezmieniane)   → Portal Użytkownika http://127.0.0.1:8002
docs-portal/   ← konfiguracja portali (ten folder)
```

---

## Wymagania

| Wymaganie | Wersja | Sprawdź |
|---|---|---|
| Python | ≥ 3.8 | `python --version` |
| pip | dowolna | `pip --version` |
| Dostęp do internetu | — | instalacja pakietów (jednorazowo) |

---

## Pierwsze uruchomienie (nowy komputer)

**Jednym poleceniem** — skrypt sam zainstaluje wszystko i uruchomi portale:

```powershell
cd "ścieżka\do\InvoiceJet\docs-portal"
.\setup.ps1
```

Domyślnie uruchamia na portach **8201** (tech) i **8301** (user). Własne porty:

```powershell
.\setup.ps1 -PortAI 9001 -PortUser 9002
```

Skrypt wykonuje kolejno:
1. Sprawdza Python 3.8+
2. Instaluje `mkdocs`, `mkdocs-material`, `mkdocs-awesome-pages-plugin`, `Pygments`
3. Generuje `mkdocs.yml` z ścieżkami pasującymi do tego komputera
4. Sprawdza wolne porty
5. Uruchamia oba serwery
6. Otwiera przeglądarkę

---

## Codzienne uruchomienie

```powershell
cd "ścieżka\do\InvoiceJet\docs-portal"
.\start-docs.ps1
```

Lub uruchom skrót na pulpicie wskazujący na `start-docs.ps1`.

Opcjonalnie — uruchom też serwer edycji:

```powershell
.\start-editor.ps1                          # Windows "Otwórz za pomocą"
.\start-editor.ps1 -Editor "notepad++"      # zawsze Notepad++
.\start-editor.ps1 -Editor "code"           # zawsze VS Code
```

---

## Opis skryptów

### `setup.ps1` — jednorazowy setup
```
Parametry: -PortAI <int>  -PortUser <int>
Domyślnie: 8201 i 8301
```
Używaj na nowym komputerze lub po klonowaniu repo. Instaluje zależności, wykrywa ścieżki i startuje.

---

### `start-docs.ps1` — uruchomienie portali
```
Brak parametrów (porty 8001/8002 hardcoded)
```
Uruchamia dwa okna PowerShell z serwerami MkDocs. Live-reload — zmiany w `.md` są widoczne natychmiast bez restartu.

> ⚠️ Zmiany w `overrides/main.html` (CSS/JS) wymagają restartu skryptu!

---

### `stop-docs.ps1` — zatrzymanie portali
```
Brak parametrów
```
Zatrzymuje procesy na portach 8001 i 8002.

---

### `start-editor.ps1` — serwer edycji plików
```
Parametry: -Port <int>  -Editor <string>
Domyślnie: port 8010, Windows "Otwórz za pomocą"
```
Uruchamia mikro-serwer HTTP który obsługuje żądania edycji plików z przeglądarki.
Gdy klikniesz ✏️ na stronie dokumentu, przeglądarka wywołuje `http://127.0.0.1:8010/edit?path=...`
i serwer otwiera plik w edytorze.

```powershell
.\start-editor.ps1                              # dialog Windows "Otwórz za pomocą"
.\start-editor.ps1 -Editor "notepad++"          # Notepad++ (musi być w PATH)
.\start-editor.ps1 -Editor "code"               # VS Code
.\start-editor.ps1 -Editor "C:\...\nppp.exe"    # pełna ścieżka do edytora
```

---

### `editor-server.py` — serwer edycji (Python)
Bezpośrednio wywoływany przez `start-editor.ps1`. Można uruchomić ręcznie:
```powershell
python editor-server.py --port 8010 --editor notepad++
```

---

## Edycja dokumentów

### Sposób 1 — przycisk ✏️ na portalu (wymaga serwera edycji)
1. Uruchom `.\start-editor.ps1` (raz, w osobnym terminalu)
2. Wejdź na dowolną stronę dokumentacji
3. Kliknij **✏️** w prawym górnym rogu paska
4. Wybierz edytor w oknie Windows lub plik otworzy się bezpośrednio

### Sposób 2 — bezpośrednio w edytorze
Otwórz dowolny plik `.md` z `doc_AI/` lub `doc_user/` w edytorze,
zapisz → portal automatycznie odświeży stronę (live-reload).

### Sposób 3 — VS Code z podglądem
Otwórz folder `InvoiceJet/` w VS Code. Edytuj `.md`, podgląd Markdown w VS Code,
portal odśwież się po zapisie.

---

## Dodawanie nowej dokumentacji

### Nowy plik w istniejącym folderze
Utwórz `doc_AI/XX_folder/nowy-plik.md` → portal wykryje automatycznie.

### Nowy folder (sekcja)
1. Utwórz folder np. `doc_AI/11_nowy_obszar/`
2. Dodaj `README.md` z opisem
3. Dodaj plik `.pages` w folderze (opcjonalnie, kontroluje kolejność):
   ```yaml
   nav:
     - README.md
     - plik1.md
     - podfolder
   ```
4. Dodaj folder do `doc_AI/.pages` w odpowiednim miejscu
5. Dodaj przycisk w `doc-ai/overrides/main.html` (sekcja `var CATS = [...]`)

---

## Konfiguracja

### Zmiana portów
Edytuj `start-docs.ps1`:
```powershell
$PORT_AI   = 8001   # zmień tutaj
$PORT_USER = 8002   # zmień tutaj
```

### Zmiana motywu kolorystycznego
Edytuj `doc-ai/mkdocs.yml` → sekcja `palette`:
```yaml
palette:
  - scheme: default
    primary: indigo   # zmień na: blue, teal, green, red...
```

### Dodanie własnego logo
Dodaj plik `doc-ai/overrides/logo.png` i w `mkdocs.yml`:
```yaml
theme:
  logo: logo.png
```

### Język interfejsu
W `mkdocs.yml` zmień `language: pl` na inny kod ISO (en, de, fr...).

---

## Struktura folderów

```
docs-portal/
├── README.md                    ← ten plik
├── setup.ps1                    ← jednorazowy setup (nowy komputer)
├── start-docs.ps1               ← uruchomienie portali
├── stop-docs.ps1                ← zatrzymanie portali
├── start-editor.ps1             ← uruchomienie serwera edycji
├── editor-server.py             ← mikro-serwer edycji plików (Python)
│
├── doc-ai/                      ← portal Dokumentacji Technicznej
│   ├── mkdocs.yml               ← konfiguracja MkDocs
│   ├── overrides/
│   │   └── main.html            ← custom HTML (pasek kategorii, edytor, portal switch)
│   └── _site/                   ← build HTML (gitignored, generowany automatycznie)
│
└── doc-user/                    ← portal Dokumentacji Użytkownika
    ├── mkdocs.yml
    ├── overrides/
    │   └── main.html
    └── _site/
```

---

## Rozwiązywanie problemów

### Portal nie startuje — "Port X is already in use"
```powershell
.\stop-docs.ps1           # zatrzymaj stare procesy
.\start-docs.ps1          # uruchom ponownie
```

### Zmiany w CSS/JS nie są widoczne
Zmiany w `overrides/main.html` nie są wykrywane przez live-reload.
Wymagają restartu: `.\stop-docs.ps1` → `.\start-docs.ps1`.

### Przycisk ✏️ daje błąd "serwer edycji nie działa"
Uruchom w osobnym terminalu:
```powershell
.\start-editor.ps1
```

### mkdocs nie znaleziony po instalacji
```powershell
# Sprawdź ścieżkę
python -c "import sysconfig; print(sysconfig.get_path('scripts'))"
# Dodaj do PATH lub użyj pełnej ścieżki
```

### Diagramy Mermaid nie renderują się
Sprawdź połączenie z internetem — Mermaid ładuje się z CDN (`unpkg.com`).
Przy braku internetu diagramy pokażą się jako kod źródłowy.

---

## Historia zmian

| Wersja | Data | Opis |
|---|---|---|
| 1.5 | 2026-06-02 | Serwer edycji plików (`editor-server.py`), przycisk ✏️, README |
| 1.4 | 2026-06-02 | Sidebar zwęża się do aktywnej sekcji (`navigation.tabs`) |
| 1.3 | 2026-06-02 | Przyciski kategorii w górnym pasku, portal switch w headerze |
| 1.2 | 2026-06-02 | Naprawiono 404 — absolutne ścieżki, index.html zamiast README.html |
| 1.1 | 2026-06-01 | Drzewo nawigacji, `navigation.prune`, pliki `.pages` |
| 1.0 | 2026-06-01 | Pierwsze wdrożenie — MkDocs Material, dwa serwery, setup.ps1 |

---

## Technologie

| Pakiet | Wersja | Rola |
|---|---|---|
| [MkDocs](https://www.mkdocs.org/) | ≥1.6 | Silnik — buduje HTML z Markdown |
| [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) | ≥9.5 | Motyw — nawigacja, wyszukiwarka, TOC |
| [mkdocs-awesome-pages-plugin](https://github.com/lukasgeiter/mkdocs-awesome-pages-plugin) | ≥2.9 | Kontrola kolejności i filtrowania nawigacji |
| [Pygments](https://pygments.org/) | ≥2.18 | Podświetlanie składni kodu |
| [Mermaid](https://mermaid.js.org/) | 10 (CDN) | Renderowanie diagramów sekwencji, flowchartów |
| Python `http.server` | stdlib | Serwer edycji plików (bez zewnętrznych zależności) |
