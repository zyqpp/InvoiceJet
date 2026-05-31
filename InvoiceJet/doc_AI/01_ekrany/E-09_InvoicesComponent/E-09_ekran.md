# E-09 InvoicesComponent — Lista faktur

| Pole | Wartość |
|---|---|
| ID dokumentu | E-09 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | zweryfikowany |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran listy faktur zwykłych (`DocumentTypeId = 1`). Prezentuje tabelę wystawionych faktur z filtrowaniem po stronie klienta, sortowaniem kolumn i paginacją. Umożliwia masowe usuwanie faktur i ich przekształcanie w faktury korygujące (storno). Z ekranu można przejść do tworzenia nowej faktury lub edycji istniejącej.

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ Invoices                              [New Invoice] [⋮ menu]     │
├──────────────────────────────────────────────────────────────────┤
│ [Search ____________________________] [×]                        │
├──┬──────────────┬───────────────┬────────────┬─────────┬────────┤
│☐ │ Document Nr  │ Client Name   │ Issue Date │ Due Date│ Total  │
├──┼──────────────┼───────────────┼────────────┼─────────┼────────┤
│☐ │ FV0005       │ ABC SRL       │ 1 May 2026 │15 May 26│1230 RON│
├──┴──────────────┴───────────────┴────────────┴─────────┴────────┤
│ [<< < 1 > >>]   Items per page: [10▼]            1–10 of 35     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoices` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | Klik „Invoices" w [Sidebar](../E-LAYOUT-03_SidebarComponent/E-LAYOUT-03_ekran.md); powrót po zapisaniu faktury |
| Komponent Angular | [`InvoicesComponent`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.ts) |
| Szablon HTML | [`invoices.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| `/dashboard/add-invoice` | Klik [OP-E09-01 New Invoice](#op-e09-01-new-invoice) | zawsze | User |
| `/dashboard/edit-invoice/:id` | Klik wiersza tabeli [OP-E09-02 Edytuj fakturę](#op-e09-02-edytuj-fakture) | zawsze | User |
| `/dashboard/invoice-stornos` | [OP-E09-04 Transform to Storno](#op-e09-04-transform-to-storno) sukces | zaznaczone faktury | User |

---

## Filtry

### FILTR-E09-01 Wyszukiwanie (Search)

| Atrybut | Wartość |
|---|---|
| ID | FILTR-E09-01 |
| Etykieta UI | „Search" |
| Nazwa w kodzie | `dataSource.filter` (`MatTableDataSource`) |
| Typ kontrolki | `input[matInput]` z przyciskiem Clear (×) |
| Zawęża | [TAB-E09-01 Lista faktur](#tab-e09-01-lista-faktur) |
| Parametr API | **brak** — filtrowanie po stronie klienta (MatTableDataSource) |
| Pole DTO | nie dotyczy — filtr działa na załadowanej kolekcji |
| Pola filtrowane w rekordzie | wszystkie kolumny tekstowe (`documentNumber`, `clientName`, `documentStatus`) |
| Wartości dopuszczalne | dowolny string; toLowerCase() przed porównaniem |
| Domyślna wartość | puste (brak filtru) |
| Wymagany | nie |

**Zachowanie:**

| Aspekt | Opis |
|---|---|
| Moment zastosowania | na bieżąco przy każdym `(keyup)` — metoda `applyFilter($event)` |
| Efekt na paginację | reset do strony 1 (`paginator.firstPage()`) |
| Przycisk Clear (×) | widoczny gdy `searchInput.value` != "" — czyści filtr i resetuje paginację |
| Łączenie z innymi filtrami | nie dotyczy (jedyny filtr) |

**Dane testowe:**

| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| Filtr po numerze | `"FV0001"` | tabela pokazuje tylko faktury z "FV0001" w dowolnym polu |
| Filtr po kliencie | `"ABC SRL"` | tabela zawęża do faktur klienta ABC SRL |
| Filtr brak wyników | `"NIEISTNIEJACY_NUMER_XYZ"` | tabela pusta |
| Clear filtra | klik ×, gdy wpisano tekst | przywrócenie pełnej listy |
| Rejestracja JWT | nagłówek `Authorization: Bearer <token>` z rolą `User` | wymagane do załadowania ekranu |

---

## Tabele i listy

### TAB-E09-01 Lista faktur

| Atrybut | Wartość |
|---|---|
| ID | TAB-E09-01 |
| Nazwa w UI | brak nagłówka nad tabelą (tytuł strony: „Invoices") |
| Źródło danych | [GET /api/Document/GetDocumentTableRecords/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) |
| DTO odpowiedzi | [DTO-09 DocumentTableRecordDto](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Typ danych Angular | `MatTableDataSource<IDocumentTableRecord>` |
| Paginacja | tak — po stronie klienta (`MatPaginator`) |
| Rozmiar strony domyślny | 10 (opcje: 10, 20, 30) |
| Domyślne sortowanie | brak (zachowana kolejność z API) |
| Sortowanie kolumn | po stronie klienta (`MatSort`) na wszystkich kolumnach z `mat-sort-header` |
| Selekcja wierszy | wielokrotna (`SelectionModel<IDocumentTableRecord>(true, [])`) |
| Zaznaczenie wszystkich | checkbox w nagłówku → `masterToggle()` |

#### Kolumny tabeli

| ID kolumny | Nagłówek UI | Pole DTO | Pole DB | Tabela DB | Typ | Sortowalna | Opis biznesowy |
|---|---|---|---|---|---|---|---|
| KOL-E09-01 | ☐ (checkbox) | — | — | — | bool | nie | Zaznaczanie do operacji batch; nagłówek = select-all |
| KOL-E09-02 | Document Number | `documentNumber` | `Document.DocumentNumber` | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) | string | tak | Numer faktury np. „FV0005"; format: `SeriesName + CurrentNumber.D4` |
| KOL-E09-03 | Client Name | `clientName` | `Firm.Name` (JOIN) | [dbo.Firm](../../../05_model_danych/01_db/dbo/dbo.Firm.md) | string | tak | Nazwa klienta; AutoMapper: `Client.Name → ClientName` |
| KOL-E09-04 | Issue Date | `issueDate` | `Document.IssueDate` | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) | DateTime | tak | Data wystawienia; pipe Angular: `date:'mediumDate'` |
| KOL-E09-05 | Due Date | `dueDate` | `Document.DueDate` | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) | DateTime (nullable) | tak | Termin płatności; pipe Angular: `date:'mediumDate'` |
| KOL-E09-06 | Total Value | `totalValue` | `Document.TotalPrice` (alias) | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) | decimal | tak | Wartość brutto w RON; AutoMapper: `TotalPrice → TotalValue` |
| KOL-E09-07 | Status | `documentStatus.status` | `DocumentStatus.Status` (JOIN) | [dbo.DocumentStatus](../../../05_model_danych/01_db/dbo/dbo.DocumentStatus.md) | string | tak | Status w chip Material; wartości: „Unpaid" / „Paid" |

#### Stany tabeli

| Stan | Warunek | Zachowanie |
|---|---|---|
| Ładowanie | po `ngOnInit()`, przed odpowiedzią API | brak wskaźnika ładowania (anomalia: brak spinnera) |
| Pełna | dane załadowane | wyświetla wiersze |
| Pusta (brak faktur) | API zwraca `[]` | pusta tabela bez komunikatu |
| Pusta (filtr) | filtr nie zwraca wyników | pusta tabela bez komunikatu |
| Błąd API | błąd HTTP | brak obsługi błędu w UI (anomalia IA-03) |

**Dane testowe dla tabeli:**

| Pole | Przykładowa wartość testowa | Źródło |
|---|---|---|
| `id` | `42` | `Document.Id` (autoincrement) |
| `documentNumber` | `"FV0001"` | `SeriesName="FV"` + `CurrentNumber=1` → `"FV0001"` |
| `clientName` | `"FIVE - STAR SOLUTION S.R.L."` | `Firm.Name` z tabeli Firm |
| `issueDate` | `"2026-05-01T00:00:00"` | ISO8601 datetime |
| `dueDate` | `"2026-05-31T00:00:00"` | ISO8601 datetime |
| `totalValue` | `1785.00` | decimal(18,2) |
| `documentStatus.status` | `"Unpaid"` lub `"Paid"` | z tabeli DocumentStatus (seedowane) |

---

## Operacje

### OP-E09-01 New Invoice

| Atrybut | Wartość |
|---|---|
| ID | OP-E09-01 |
| Etykieta UI | „New Invoice" (przycisk `mat-raised-button color="primary"`) |
| Ikona | `add` (Material Icons) |
| Wyzwalacz | `(click)` → `openNewInvoiceDialog()` |
| Wywoływane API | brak (nawigacja) |
| Powiązany proces | brak bezpośredniego (formularz ma własny) |
| Wymagana rola | User |
| Efekt | `router.navigate(["dashboard/add-invoice"])` |

**Pola wejściowe:** brak (tylko nawigacja)

**Możliwe wyniki:**

| Wynik | Warunek | Komunikat | Akcja UI |
|---|---|---|---|
| Sukces | zawsze | brak | przejście do `/dashboard/add-invoice` |

**Dane testowe:**

| Scenariusz | Prereq | Oczekiwany URL |
|---|---|---|
| Klik New Invoice | zalogowany user (JWT User) | `/dashboard/add-invoice` |

---

### OP-E09-02 Edytuj fakturę

| Atrybut | Wartość |
|---|---|
| ID | OP-E09-02 |
| Etykieta UI | klik całego wiersza tabeli (klasa CSS `clickable`) |
| Wyzwalacz | `(click)` na `<tr>` → `openEditInvoiceDialog(row)` |
| Parametr | `row.id` — `IDocumentTableRecord.id` = `Document.Id` |
| Wywoływane API | brak (nawigacja; API ładuje formularz edycji) |
| Efekt | `router.navigate(["/dashboard/edit-invoice", row.id])` |
| Wymagana rola | User |

**Możliwe wyniki:**

| Wynik | Warunek | Akcja UI |
|---|---|---|
| Sukces | zawsze | przejście do `/dashboard/edit-invoice/{id}` |

**Dane testowe:**

| Scenariusz | Prereq | Oczekiwany URL |
|---|---|---|
| Klik wiersza z id=42 | faktura id=42 istnieje | `/dashboard/edit-invoice/42` |

---

### OP-E09-03 Usuń zaznaczone (Delete selected)

| Atrybut | Wartość |
|---|---|
| ID | OP-E09-03 |
| Etykieta UI | „Delete selected" (pozycja menu ⋮) |
| Ikona | `delete` (Material Icons, kolor warn) |
| Wyzwalacz | `(click)` → `deleteSelected()` |
| Wywoływane API | [PUT /api/Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) |
| DTO żądania | `[FromBody] int[]` — tablica `Document.Id` zaznaczonych rekordów |
| Powiązany proces | [usun_dokumenty](../../../02_procesy/dokumenty/usun_dokumenty/proces.md) |
| Wymagana rola | User |

**Pola wejściowe:**

| Pole | Źródło w UI | Pole DTO | Pole DB |
|---|---|---|---|
| `documentIds[]` | `selection.selected.map(doc => doc.id)` | `int[]` body | `Document.Id` |

**Możliwe wyniki:**

| Wynik | Warunek | Komunikat | Akcja UI |
|---|---|---|---|
| Sukces | HTTP 200 | brak | `loadInvoices()` — odświeżenie tabeli |
| Błąd | HTTP 4xx/5xx | `console.error` (anomalia: brak komunikatu w UI) | brak reakcji wizualnej |

**Dane testowe:**

| Scenariusz | Prereq | Body żądania | Oczekiwany efekt |
|---|---|---|---|
| Usuń jedną fakturę | id=42 istnieje, zaznaczony | `[42]` | faktura znika z tabeli |
| Usuń wiele | id=[42,43] zaznaczone | `[42, 43]` | obie znikają |
| Brak zaznaczenia | nic nie zaznaczone | `[]` | PUT z pustą tablicą |
| JWT | nagłówek `Authorization: Bearer <token>` | — | wymagane |

---

### OP-E09-04 Transform to Storno

| Atrybut | Wartość |
|---|---|
| ID | OP-E09-04 |
| Etykieta UI | „Transform to storno" (pozycja menu ⋮) |
| Ikona | `swap_vert` (Material Icons, kolor primary) |
| Wyzwalacz | `(click)` → `transformToStorno()` |
| Wywoływane API | [PUT /api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) |
| DTO żądania | `[FromBody] int[]` — tablica `Document.Id` zaznaczonych rekordów |
| Powiązany proces | [transformuj_na_storno](../../../02_procesy/dokumenty/transformuj_na_storno/proces.md) |
| Algorytm | [ALG-08 TransformToStorno](../../../03_algorytmy/ALG-08_TransformToStorno.md) |
| Wymagana rola | User |

> ⚠️ **Semantyka:** operacja zmienia `DocumentTypeId = 3` na istniejącym rekordzie. Faktura znika z tej listy i pojawia się w [E-13 Lista storn](../E-13_InvoiceStornosComponent/E-13_ekran.md). Nie tworzy nowego dokumentu. → [ALG-08](../../../03_algorytmy/ALG-08_TransformToStorno.md)

**Pola wejściowe:**

| Pole | Źródło w UI | Pole DTO | Pole DB |
|---|---|---|---|
| `documentIds[]` | `selection.selected.map(doc => doc.id)` | `int[]` body | `Document.Id` |

**Możliwe wyniki:**

| Wynik | Warunek | Komunikat | Akcja UI |
|---|---|---|---|
| Sukces | HTTP 200 | brak | `loadInvoices()` — faktura znika z listy |
| Błąd | HTTP 4xx/5xx | `console.error` (brak komunikatu w UI) | brak reakcji wizualnej |

**Dane testowe:**

| Scenariusz | Prereq | Body | Oczekiwany efekt |
|---|---|---|---|
| Storno jednej faktury | id=42 istnieje, `DocumentTypeId=1` | `[42]` | faktura 42 znika, pojawia się w `/invoice-stornos` |
| Storno wielokrotne | id=[42,43] zaznaczone | `[42, 43]` | obie znikają |
| JWT | nagłówek `Authorization: Bearer <token>` rola User | — | wymagane |

---

## Modale

Brak — żadna operacja na tym ekranie nie otwiera dialogu.

> Uwaga: po kliknięciu „New Invoice" lub wiersza następuje nawigacja do osobnego ekranu (nie modal).

---

## Powiadomienia

Brak powiadomień toast/alert zaimplementowanych na tym ekranie.

> Anomalia: błędy operacji (`deleteSelected`, `transformToStorno`) są logowane wyłącznie jako `console.error` — użytkownik nie dostaje żadnego komunikatu o błędzie.

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO | Proces |
|---|---|---|---|---|
| Załadowanie listy (ngOnInit) | GET | [/api/Document/GetDocumentTableRecords/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) | [DTO-09](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) | [pobierz_dokumenty](../../../02_procesy/dokumenty/pobierz_dokumenty/proces.md) |
| Usuń zaznaczone | PUT | [/api/Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) | `int[]` body | [usun_dokumenty](../../../02_procesy/dokumenty/usun_dokumenty/proces.md) |
| Przekształć w storno | PUT | [/api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) | `int[]` body | [transformuj_na_storno](../../../02_procesy/dokumenty/transformuj_na_storno/proces.md) |

---

## Informacje dla testów automatycznych

### Autoryzacja (prereq dla każdego testu)

| Wymaganie | Szczegół |
|---|---|
| Typ autoryzacji | JWT Bearer token |
| Rola wymagana | `"User"` w claims |
| Nagłówek HTTP | `Authorization: Bearer <token>` |
| Uzyskanie tokenu | [POST /api/Auth/login](../../../04_api_i_integracje/01_api_frontend/auth/POST_Auth_login.md) z `{email, password}` |

### Selektory komponentów (brak `data-cy` — anomalia IA-04)

| Element | Selektor CSS / Angular | Uwagi |
|---|---|---|
| Przycisk New Invoice | `button[mat-raised-button]` + tekst „New Invoice" | jedyny raised-button primary |
| Menu ⋮ | `button[mat-stroked-button]` z `mat-icon` `more_vert` | — |
| „Delete selected" | `button[mat-menu-item]` z ikoną `delete` | wewnątrz mat-menu |
| „Transform to storno" | `button[mat-menu-item]` z ikoną `swap_vert` | wewnątrz mat-menu |
| Pole Search | `input[matInput]` z placeholder „Search" | — |
| Wiersze tabeli | `tr.clickable` | klasa CSS `clickable` |
| Checkbox wiersza | `mat-checkbox` wewnątrz `td.select-column` | — |
| Checkbox nagłówka | `mat-checkbox` wewnątrz `th.select-column` | select-all |
| Paginator | `mat-paginator` | — |

### Scenariusze e2e

| ID | Opis | Prereq w DB | Kroki | Oczekiwany wynik |
|---|---|---|---|---|
| TC-E09-01 | Załadowanie listy | ≥1 faktura `DocumentTypeId=1` | 1. Login 2. GET /invoices | tabela z fakturami |
| TC-E09-02 | Wyszukiwanie | faktura z numerem „FV0001" | wpisz „FV0001" w Search | tylko FV0001 w tabeli |
| TC-E09-03 | Clear Search | po TC-E09-02 | klik × | pełna lista powraca |
| TC-E09-04 | Nawigacja New Invoice | — | klik New Invoice | URL = `/dashboard/add-invoice` |
| TC-E09-05 | Nawigacja edycja | faktura id=42 | klik wiersz id=42 | URL = `/dashboard/edit-invoice/42` |
| TC-E09-06 | Usuń fakturę | faktura id=42 | zaznacz → menu ⋮ → Delete selected | id=42 znika z tabeli |
| TC-E09-07 | Transform to Storno | faktura id=42 `TypeId=1` | zaznacz → menu ⋮ → Transform | id=42 znika, pojawia się w /invoice-stornos |
| TC-E09-08 | Brak autoryzacji | brak tokenu | GET /dashboard/invoices | redirect do /login |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran: edycja faktury | [E-10 AddOrEditInvoiceComponent](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) |
| Ekran: lista storn | [E-13 InvoiceStornosComponent](../E-13_InvoiceStornosComponent/E-13_ekran.md) |
| Ekran: sidebar | [E-LAYOUT-03 SidebarComponent](../E-LAYOUT-03_SidebarComponent/E-LAYOUT-03_ekran.md) |
| API: pobierz dokumenty | [GET /Document/GetDocumentTableRecords](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) |
| API: usuń dokumenty | [PUT /Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) |
| API: storno | [PUT /Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) |
| DTO | [DTO-09 DocumentTableRecordDto](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Model DB | [dbo.Firm](../../../05_model_danych/01_db/dbo/dbo.Firm.md) |
| Model DB | [dbo.DocumentStatus](../../../05_model_danych/01_db/dbo/dbo.DocumentStatus.md) |
| Algorytm | [ALG-08 TransformToStorno](../../../03_algorytmy/ALG-08_TransformToStorno.md) |
| Inwentaryzacja | [inwentaryzacja_ekranow](../../../_mapowania/inwentaryzacja_ekranow.md) |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`invoices.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.ts) |
| Szablon HTML | [`invoices.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.html) |
| Style SCSS | [`invoices.component.scss`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.scss) |
| Model interfejsu | [`IDocumentTableRecord.ts`](../../../../InvoiceJetUI/src/app/models/IDocumentTableRecord.ts) |
| Serwis | [`document.service.ts`](../../../../InvoiceJetUI/src/app/services/document.service.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | `console.log(this.invoices)` w `loadInvoices()` — aktywny w produkcji |
| IA-02 | `console.log(documentIds)` dwukrotnie w `deleteSelected()` i `transformToStorno()` |
| IA-03 | Brak obsługi błędów API w UI — `console.error` bez komunikatu dla użytkownika |
| IA-04 | Brak atrybutów `data-cy` / `data-testid` — selektory testów nieodporne na zmiany UI |
| IA-05 | Brak spinner/skeleton przy ładowaniu tabeli |
| IA-06 | Brak komunikatu „brak wyników" gdy tabela pusta |

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkic na podstawie kodu komponentu. |
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wersja pełna — sekcje filtrów, tabeli, operacji z danymi testowymi i linkami. |
