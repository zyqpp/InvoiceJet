# InvoiceJet — Projekt Figma (wytyczne)

Hub wiedzy o odtworzeniu frontu InvoiceJet w Figmie. To są **wytyczne projektu** —
obowiązują każdego (człowieka i agenta), kto pracuje nad plikiem Figma.

## 1. Cel i zasada naczelna
Odtworzyć istniejącą aplikację **1:1**, na podstawie **kodu + dokumentacji**, podzieloną tak,
by łatwo nią zarządzać.

> **To NIE jest redesign.** Nie wymyślamy układów, kolorów ani etykiet. Każdy element ma
> oparcie w kodzie (`InvoiceJetUI/`) lub dokumentacji (`doc_AI/01_ekrany/`).

## 2. Źródła prawdy (kolejność)
1. `figma/design-tokens.md` — kolory, typografia, odstępy (gotowe, NIE re-skanuj kodu).
2. `figma/screens-index.md` — lista ekranów + ścieżka do dokumentu każdego ekranu.
3. `doc_AI/01_ekrany/<ekran>.md` — kolumny tabel, pola formularzy, akcje, nawigacja.
4. Kod `InvoiceJetUI/src/app/components/...` — tylko gdy dokument nie wystarcza (układ piksel-w-piksel).
5. ❌ **Ignoruj folder `archiwum/`** — to śmieci.

## 3. Decyzje projektowe (ustalone z właścicielem)
| Decyzja | Ustalenie |
|---|---|
| Wierność | Odtworzenie 1:1, bez przeprojektowania |
| Kolejność | Najpierw fundamenty → komponenty → pilot → reszta |
| Motyw | Tylko **jasny** (bazowy). Ciemny pominięty (spisany referencyjnie). |
| Plik Figma | Tworzony przez agenta (MCP) |
| Podział | Strony Figma per obszar (patrz niżej) |

## 4. Struktura pliku Figma (strony)
`00 · Fundamenty` · `01 · Komponenty` · `02 · Auth` · `03 · Layout` · `04 · Dashboard`
· `05 · Faktury` · `06 · Proformy` · `07 · Storna` · `08 · Produkty` · `09 · Klienci`
· `10 · Konta bankowe` · `11 · Serie dokumentów` · `12 · Firma`

## 5. Konwencje nazewnictwa (warstwy/komponenty)
- **Strony:** `NN · Nazwa` (np. `05 · Faktury`).
- **Komponenty Figma:** `Kategoria/Nazwa/Wariant` (np. `Button/Primary`, `Input/Text`, `Table/Row`).
- **Ekrany (frame'y):** `EKRAN-NN — Nazwa` lub `DIALOG-NN — Nazwa` (zgodnie z `screens-index.md`).
- **Tokeny (zmienne Figma):** zgodne z `design-tokens.json` (`surface/page`, `brand/primary`, `space/24` itd.).
- Język UI w makietach: **taki jak w aplikacji** (etykiety z kodu/dokumentacji — w razie wątpliwości EN, bo apka jest po angielsku).

## 6. Workflow i punkty kontrolne
1. **Etap 0 — test uprawnień:** utworzyć pusty plik. Konto bywa „View only" → jeśli edycja zablokowana, zatrzymać się i zgłosić właścicielowi.
2. **Etap 1 — Fundamenty** → ⛔ punkt kontrolny (akceptacja).
3. **Etap 2 — Komponenty** → ⛔ punkt kontrolny.
4. **Etap 3 — Pilot (Lista faktur)** → ⛔ punkt kontrolny (wzorzec jakości).
5. **Etap 4 — reszta ekranów + modale.**
6. **Etap 5 — przegląd końcowy.**

Po każdym ukończonym elemencie: zaktualizuj `figma/progress.md`.

## 7. Higiena tokenów (oszczędność)
- Najpierw `design-tokens.md` + `screens-index.md`; dopiero potem JEDEN dokument ekranu.
- Nie wczytuj całego `doc_AI` ani całego kodu naraz.
- Komponenty buduj raz, potem **reużywaj instancji** — nie powielaj ręcznie.
- Stan trzymaj w `progress.md`, nie w pamięci sesji.

## 8. Zawartość folderu `figma/`
| Plik | Rola |
|---|---|
| `README.md` | ten dokument — wytyczne |
| `AGENT.md` | opis i rola agenta budującego |
| `design-tokens.md` / `.json` | tokeny 1:1 z kodu |
| `screens-index.md` | mapa ekranów → dokumenty |
| `progress.md` | tracker postępu i fileKey |
| `scripts/extract-tokens.ps1` | odświeżanie inwentarza kolorów z SCSS |

## 9. Powiązane
- Skill: `.claude/skills/figma-invoicejet/SKILL.md`
- Agent: `.claude/agents/figma-builder.md`
- Wytyczne dokumentacji projektu: `wytyczne/`
