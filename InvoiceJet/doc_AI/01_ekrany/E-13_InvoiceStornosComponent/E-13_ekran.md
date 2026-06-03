# E-13 InvoiceStornosComponent — Lista faktur storno

| Pole | Wartość |
|---|---|
| ID dokumentu | E-13 |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran listy faktur storno (`DocumentTypeId = 3`). Storna nie mogą być tworzone bezpośrednio z tego ekranu — brak przycisku „Dodaj storno" i brak odpowiedniej opcji w menu. Storna powstają wyłącznie przez operację „Przekształć w storno" z [listy faktur zwykłych (E-09)](../E-09_InvoicesComponent/E-09_ekran.md). Na tym ekranie możliwa jest edycja istniejącego storna i masowe usunięcie zaznaczonych. Wartości `totalValue` dla storn z operacji TransformToStorno są ujemne. Chroniony przez AuthGuard (rola: User).

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ Invoice Stornos                                       [⋮ menu]   │
├──────────────────────────────────────────────────────────────────┤
│ [Search ____________________________] [×]                        │
├──┬──────────────┬───────────────┬────────────┬─────────┬────────┤
│☐ │ Document Nr  │ Client Name   │ Issue Date │ Due Date│ Total  │
├──┼──────────────┼───────────────┼────────────┼─────────┼────────┤
│☐ │ STORNO0001   │ Firma ABC S.A.│ 2 May 2026 │16 May 26│ -600   │
├──┴──────────────┴───────────────┴────────────┴─────────┴────────┤
│ [<< < 1 > >>]   Items per page: [10▼]            1–5 of 5       │
└──────────────────────────────────────────────────────────────────┘
```

> Brak przycisku „New Storno" — storna tworzone wyłącznie przez TransformToStorno z E-09.

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoice-stornos` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | Klik „Invoice Stornos" w [Sidebar](../E-LAYOUT-03_SidebarComponent/E-LAYOUT-03_ekran.md); przekierowanie po operacji TransformToStorno z [E-09](../E-09_InvoicesComponent/E-09_ekran.md) |
| Komponent Angular | [`InvoiceStornosComponent`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/invoice-stornos.component.ts) |
| Szablon HTML | [`invoice-stornos.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/invoice-stornos.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| [E-14 Formularz storna (edycja)](../E-14_AddOrEditInvoiceStornosComponent/E-14_ekran.md) | [OP-E13-01](E-13_OP-01.md) | zawsze | User |

> Brak przejścia do „dodaj storno" z poziomu UI — trasa `/dashboard/add-invoice-storno` istnieje w routingu, ale nie jest eksponowana w UI (wątpliwość IA-07).

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E13-01 | Search | input, kliencki | [E-13_FILTR-01.md](E-13_FILTR-01.md) |

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E13-01 | Lista storn | [E-13_TAB-01.md](E-13_TAB-01.md) |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis | Algorytm |
|---|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch | — |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer storna (seria STN) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| `clientName` | `IDocumentTableRecord.clientName` | Nazwa klienta | — |
| `issueDate` | `IDocumentTableRecord.issueDate` | Data wystawienia | — |
| `dueDate` | `IDocumentTableRecord.dueDate` | Termin płatności | — |
| `totalValue` | `IDocumentTableRecord.totalValue` | Wartość brutto (ujemna dla storn z TransformToStorno) | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) · [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) |
| `documentStatus` | `IDocumentTableRecord.documentStatus.status` | Status (Unpaid/Paid) | — |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E13-01 | Edytuj (klik wiersza) | [E-13_OP-01.md](E-13_OP-01.md) |
| OP-E13-02 | Delete selected | [E-13_OP-02.md](E-13_OP-02.md) |

## Modale

Brak — operacje nawigują do osobnych ekranów.

## Scenariusze testowe

→ [E-13_TC.md](E-13_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Załadowanie listy | GET | [/api/Document/GetDocumentTableRecords/3](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) | [DTO-09](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Usuń zaznaczone | PUT | [/api/Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) | `int[]` |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran: formularz storna | [E-14 AddOrEditInvoiceStornosComponent](../E-14_AddOrEditInvoiceStornosComponent/E-14_ekran.md) |
| Ekran: lista faktur (źródło storn) | [E-09 InvoicesComponent](../E-09_InvoicesComponent/E-09_ekran.md) |
| Ekran wzorzec listy | [E-11 InvoiceProformasComponent](../E-11_InvoiceProformasComponent/E-11_ekran.md) |
| DTO | [DTO-09 DocumentTableRecordDto](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Kolumna `documentNumber` | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Numer serii STN nadany przy tworzeniu storna |
| Kolumna `totalValue` (ujemna) | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) | Wartości ujemne dla storn stworzonych przez TransformToStorno z E-09 |
| Kolumna `totalValue` | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | Suma brutto `Document.TotalPrice` przechowana w DB |
| Ładowanie listy (ngOnInit) | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | `GetTableRecords` filtruje storna per UserFirm |
| OP-E13-02 UsunZaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Soft-delete; backend weryfikuje przynależność do UserFirm |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`invoice-stornos.component.ts`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/invoice-stornos.component.ts) |
| Szablon HTML | [`invoice-stornos.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-stornos/invoice-stornos.component.html) |
| Model interfejsu | [`IDocumentTableRecord.ts`](../../../../InvoiceJetUI/src/app/models/IDocumentTableRecord.ts) |
| Serwis | [`document.service.ts`](../../../../InvoiceJetUI/src/app/services/document.service.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | `console.log(this.selection.selected)` i `console.log(documentIds)` aktywne w `deleteSelected()` |
| IA-02 | Brak obsługi błędów API w UI — `console.error` bez komunikatu dla użytkownika |
| IA-04 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |
| IA-05 | Brak spinner/skeleton przy ładowaniu tabeli |
| IA-07 | Trasa `/dashboard/add-invoice-storno` istnieje w routingu, ale UI nie eksponuje przycisku „Dodaj storno" — niespójność: celowa decyzja projektowa (storno tylko przez TransformToStorno) czy przeoczenie? |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca E-09/E-11 i źródła faktury_storno/lista_faktur_storno/ekran.md. |
