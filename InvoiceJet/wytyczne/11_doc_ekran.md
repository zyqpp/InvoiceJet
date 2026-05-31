---
name: doc-ekran
description: >-
  Dokumentuj ekran aplikacji Angular InvoiceJet zgodnie ze standardem AOS.
  Rola: Agent-Dokumentalista-Ekranów (B.7 z wytycznych). Trigger: "udokumentuj
  ekran X", "stwórz dokumentację ekranu", "opisz komponent X", "napisz ekran.md
  dla X". Produkuje plik E-NN_ekran.md z pełnymi sekcjami: filtry (z danymi
  testowymi i DB), tabela/kolumny (z mapowaniem DB), operacje (z API/DTO/procesem),
  modale, testy automatyczne, powiązania z kodem.
---

# Skill: doc-ekran — Agent-Dokumentalista-Ekranów

Produkuje plik `E-NN_ekran.md` dla ekranu Angular zgodnie ze standardem AOS InvoiceJet.
Wzorzec: [`E-09_InvoicesComponent/E-09_ekran.md`](../../../InvoiceJet/doc_AI/01_ekrany/E-09_InvoicesComponent/E-09_ekran.md)

---

## Krok 0 — Określ ID ekranu

Sprawdź w [`_mapowania/inwentaryzacja_ekranow.md`](../../../InvoiceJet/doc_AI/_mapowania/inwentaryzacja_ekranow.md):

| Typ | Format ID | Przykłady |
|---|---|---|
| Ekran z trasą | `E-NN` (numer z inwentaryzacji) | `E-09`, `E-10` |
| Dialog/modal | `E-DIALOG-NN` | `E-DIALOG-01` |
| Layout (navbar/sidebar) | `E-LAYOUT-NN` | `E-LAYOUT-02` |

Folder: `doc_AI/01_ekrany/E-NN_NazwaKomponentu/`
Plik: `E-NN_ekran.md`

---

## Krok 1 — Zbierz dane źródłowe

Przeczytaj w tej kolejności (nie więcej niż potrzeba):

1. **Kod komponentu** `.component.ts` — metody, konstruktor, `displayedColumns`, `dataSource`, serwisy
2. **Szablon HTML** `.component.html` — etykiety UI, bindowania, zdarzenia `(click)`, selektory
3. **Model interfejsu** (`IXxx.ts`) — pola dostępne w tabeli/formularzu
4. **Dokument DTO** — mapowanie backend → frontend
5. **Dokument API** — endpointy wywoływane przez komponent

Używaj [`doc-linking`](../doc-linking/SKILL.md) do wszystkich ścieżek linków.

---

## Krok 2 — Struktura dokumentu (kolejność sekcji — niezmienna per ZZ-08)

```
# E-NN NazwaKomponentu — Tytuł biznesowy

Metryka (ID, typ, wersja, status, autor, data)

## Streszczenie (2-4 zdania biznesowe)

## Wizualizacja układu (ASCII box)

## Wywołanie ekranu (URL, rola, punkty wejścia, kod)

## Przejścia z ekranu (tabela: cel | wywołanie | warunek | uprawnienie)

## Filtry (sekcja per filtr)

## Tabele i listy (sekcja per tabela + kolumny)

## Operacje (sekcja per operacja)

## Modale (tabela lub "Brak")

## Powiadomienia (tabela lub "Brak")

## Wywołania API — podsumowanie (tabela)

## Informacje dla testów automatycznych

## Powiązania (tabela linków)

## Powiązania z kodem (tabela linków)

## Wątpliwości i braki

## Rejestr zmian
```

---

## Krok 3 — Sekcja: Filtry

Jeden blok per filtr. Zawiera:

```markdown
### FILTR-ENN-NN Nazwa filtru

| Atrybut | Wartość |
|---|---|
| ID | FILTR-E09-01 |
| Etykieta UI | „..." (dokładna etykieta z HTML) |
| Nazwa w kodzie | nazwa zmiennej/właściwości w .ts lub dataSource.filter |
| Typ kontrolki | input / select / date-range / checkbox |
| Zawęża | [TAB-ENN-NN nazwa tabeli](#tab-enn-nn) |
| Parametr API | nazwa query param LUB "brak — filtr kliencki (MatTableDataSource)" |
| Pole DTO | link do DTO LUB "nie dotyczy" |
| Pola filtrowane | pola rekordu porównywane przez filtr |
| Wartości dopuszczalne | opis |
| Domyślna wartość | puste / wartość / brak filtru |
| Wymagany | tak / nie |

**Zachowanie:**
| Aspekt | Opis |
|---|---|
| Moment zastosowania | na_biezaco przy (keyup) / po kliknięciu / po wyborze |
| Efekt na paginację | reset do strony 1 / nie dotyczy |
| Łączenie z innymi | AND / OR / jedyny filtr |

**Dane testowe:**
| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| filtr trafia | ... | ... |
| filtr nie trafia | ... | pusta tabela |
| clear | klik × | pełna lista |
```

**Uwaga kluczowa:** rozróżnij:
- Filtr **kliencki** (MatTableDataSource.filter) — brak parametru API, działa na załadowanych danych
- Filtr **serwerowy** — parametr query string, nowe wywołanie API

---

## Krok 4 — Sekcja: Tabele i kolumny

```markdown
### TAB-ENN-NN Nazwa tabeli

| Atrybut | Wartość |
|---|---|
| ID | TAB-E09-01 |
| Źródło danych | [link do endpointu API] |
| DTO odpowiedzi | [link do DTO] |
| Typ Angular | MatTableDataSource<IXxx> / zwykła tablica |
| Paginacja | tak kliencka (MatPaginator) / tak serwerowa / nie |
| Rozmiar strony domyślny | liczba lub N/D |
| Domyślne sortowanie | kolumna + ASC/DESC / brak |
| Selekcja | wielokrotna / pojedyncza / brak |

#### Kolumny tabeli

| ID kolumny | Nagłówek UI | Pole DTO | Pole DB | Tabela DB | Typ | Sortowalna | Opis |
|---|---|---|---|---|---|---|---|
| KOL-ENN-NN | "Document Number" | `documentNumber` | `Document.DocumentNumber` | [dbo.Document](link) | string | tak | ... |
```

**Zasada:** każda kolumna musi mieć `Pole DB` + link do tabeli DB lub „obliczane w szablonie" / „brak w DB".

---

## Krok 5 — Sekcja: Operacje

Jeden blok per operacja (przycisk, link, klik wiersza):

> **REGUŁA TWARDA: każde odwołanie do innego ekranu, API, procesu, algorytmu lub DTO MUSI być klikalnym linkiem. Nigdy nie wpisuj tekstu tam gdzie istnieje dokument docelowy.**

```markdown
### OP-ENN-NN Nazwa operacji

| Atrybut | Wartość |
|---|---|
| ID | OP-E09-01 |
| Etykieta UI | „..." (dokładna etykieta z HTML) |
| Wyzwalacz | (click) → metoda() / (keyup.enter) / etc. |
| Wywoływane API | [link do endpointu](ścieżka) LUB "brak — czysta nawigacja" |
| DTO żądania | [link do DTO](ścieżka) LUB "int[] body" LUB "nie dotyczy" |
| Powiązany proces | [link do 02_procesy](ścieżka) LUB "brak" (z uzasadnieniem) |
| Algorytm | [link do 03_algorytmy](ścieżka) LUB "brak" |
| Ekran docelowy | [E-NN Nazwa](ścieżka) ← WYMAGANE gdy operacja nawiguje do ekranu |
| Wymagana rola | User / brak |

**Pola wejściowe:**
| Pole | Źródło w UI | Pole DTO | Pole DB |
|---|---|---|---|

**Możliwe wyniki:**
| Wynik | Warunek | Komunikat | Akcja UI |
|---|---|---|---|
| Sukces | HTTP 200 | brak / toast | przeładowanie tabeli / redirect → [E-NN Ekran docelowy](link) |
| Błąd | HTTP 4xx/5xx | komunikat błędu | zachowanie UI |

> Akcja UI po sukcesie MUSI linkować do ekranu docelowego jeśli jest nawigacja.

**Dane testowe:**
| Scenariusz | Prereq | Dane wejściowe | Oczekiwany wynik |
|---|---|---|---|
```

---

## Krok 6 — Sekcja: Testy automatyczne

Zawsze zawiera:

1. **Blok Autoryzacja** — JWT prereq
2. **Selektory** — CSS/Angular dla każdego elementu interaktywnego
3. **Scenariusze e2e** — tabela z prereq w DB, krokami i oczekiwanym wynikiem

```markdown
## Informacje dla testów automatycznych

### Autoryzacja (prereq dla każdego testu)
| Wymaganie | Szczegół |
|---|---|
| Typ autoryzacji | JWT Bearer token |
| Rola wymagana | "User" |
| Nagłówek HTTP | Authorization: Bearer <token> |
| Uzyskanie tokenu | [POST /api/Auth/login](link) |

### Selektory
| Element | Selektor CSS | Uwagi |
|---|---|---|

### Scenariusze e2e
| ID | Opis | Prereq w DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-ENN-01 | ... | ... | 1. Login 2. ... | ... |
```

---

## Krok 7 — Identyfikatory

Konwencja ID (stabilne, nie zmieniają się po edycji per RO-09):

| Element | Format | Przykład |
|---|---|---|
| Ekran | `E-NN` | `E-09` |
| Filtr | `FILTR-E{NN}-{NN}` | `FILTR-E09-01` |
| Tabela | `TAB-E{NN}-{NN}` | `TAB-E09-01` |
| Kolumna | `KOL-E{NN}-{NN}` | `KOL-E09-02` |
| Operacja | `OP-E{NN}-{NN}` | `OP-E09-03` |
| Modal | `MODAL-E{NN}-{NN}` | `MODAL-E10-01` |
| Scenariusz testu | `TC-E{NN}-{NN}` | `TC-E09-06` |
| Dialog (osobny ekran) | `E-DIALOG-{NN}` | `E-DIALOG-01` |

---

## Krok 8 — Konwencja folderów i podział plików

**Zasada:** `E-NN_ekran.md` to **indeks** — zawiera tylko metrykę, streszczenie, układ, wywołanie, przejścia i tabele linków do sub-plików. Szczegóły w osobnych plikach.

```
doc_AI/01_ekrany/
  E-NN_NazwaKomponentu/
    E-NN_ekran.md              ← indeks (~60–80 linii)
    E-NN_FILTR-01.md           ← jeden filtr
    E-NN_FILTR-02.md           ← drugi filtr (jeśli jest)
    E-NN_POLA.md               ← wszystkie pola formularza (grupowo)
    E-NN_TAB-01.md             ← tabela + kolumny
    E-NN_OP-01.md              ← operacja 1
    E-NN_OP-02.md              ← operacja 2 ...
    E-NN_MODAL-01.md           ← modal (jeśli jest)
    E-NN_TC.md                 ← scenariusze testowe
```

**Kiedy grupować, kiedy dzielić:**
- Filtry: **jeden plik per filtr** (mają własną logikę zachowania)
- Pola formularza: **jeden plik dla wszystkich** (są mniejsze, podobna struktura)
- Tabele: **jeden plik per tabela** (ma kolumny i stany)
- Operacje: **jeden plik per operacja** (mają API/DTO/proces/testy — są wartościowe osobno)
- Modale: **jeden plik per modal**
- Testy: **jeden wspólny plik** dla całego ekranu

Wzorzec: `E-09_InvoicesComponent/` i `E-10_AddOrEditInvoiceComponent/`

---

## Krok 9 — Złote zasady (z wytycznych)

- **ZZ-01** język polski (poza cytatami kodu)
- **ZZ-02** nazwy z kodu 1:1 (nie tłumacz nazw metod, pól, endpointów)
- **ZZ-04** brak nadinterpretacji — czego nie wiesz, wpisz w Wątpliwości i braki
- **ZZ-05** wszystko podlinkowane — żaden element nie jest wyspą
- **ZZ-08** metryka na górze, rejestr zmian na dole
- **RO-09** ID stabilne i jednoznaczne

---

## Krok 10 — Walidacja przed zapisem

- [ ] Każda kolumna tabeli ma `Pole DB` + link do tabeli DB
- [ ] Każda operacja ma link do API lub „brak — czysta nawigacja"
- [ ] Każda operacja **nawigująca do ekranu** ma `Ekran docelowy` z linkiem
- [ ] Każda operacja z API ma link do DTO
- [ ] Każda operacja z API ma link do procesu (lub „brak" z uzasadnieniem)
- [ ] Każda operacja z API ma link do algorytmu jeśli wywołuje logikę biznesową
- [ ] Każde `Akcja UI: redirect/nawigacja` w sekcji wyników linkuje do ekranu
- [ ] NIGDY plain text tam gdzie istnieje dokument docelowy
- [ ] Sekcja testów ma prereq autoryzacji (JWT)
- [ ] Sekcja testów ma selektory CSS/Angular
- [ ] Sekcja testów ma scenariusze e2e z prereq w DB
- [ ] Wątpliwości i braki wypełnione (nawet jeśli „Brak")
- [ ] Rejestr zmian wypełniony
- [ ] Linki względne (nie absolutne)
- [ ] Mermaid diagrams (jeśli są) przeszły checklist z `mermaid-diagrams`
