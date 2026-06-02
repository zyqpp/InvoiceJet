# E-11 InvoiceProformasComponent — Lista faktur proforma

| Pole | Wartość |
|---|---|
| ID dokumentu | E-11 |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran listy faktur proforma (`DocumentTypeId = 2`). Identyczna struktura jak `InvoicesComponent` (E-09 lista faktur zwykłych), lecz bez operacji „Przekształć w storno". Prezentuje tabelę proform z filtrowaniem po stronie klienta, sortowaniem kolumn i paginacją. Umożliwia masowe usuwanie zaznaczonych proform oraz nawigację do tworzenia nowej proformy lub edycji istniejącej. Chroniony przez AuthGuard (rola: User).

---

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ Invoice Proformas                          [New Proforma] [⋮ menu]│
├──────────────────────────────────────────────────────────────────┤
│ [Search ____________________________] [×]                        │
├──┬──────────────┬───────────────┬────────────┬─────────┬────────┤
│☐ │ Document Nr  │ Client Name   │ Issue Date │ Due Date│ Total  │
├──┼──────────────┼───────────────┼────────────┼─────────┼────────┤
│☐ │ PRF0012      │ Firma XYZ     │10 May 2026 │24 May 26│5000 RON│
├──┴──────────────┴───────────────┴────────────┴─────────┴────────┤
│ [<< < 1 > >>]   Items per page: [10▼]            1–10 of 20     │
└──────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoice-proformas` |
| Wymagana rola | `User` (AuthGuard JWT) |
| Punkty wejścia | Klik „Invoice Proformas" w [Sidebar](../E-LAYOUT-03_SidebarComponent/E-LAYOUT-03_ekran.md); powrót po zapisaniu proformy |
| Komponent Angular | [`InvoiceProformasComponent`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/invoice-proformas.component.ts) |
| Szablon HTML | [`invoice-proformas.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/invoice-proformas.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| [E-12 Formularz proformy (dodaj)](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) | [OP-E11-01](E-11_OP-01.md) | zawsze | User |
| [E-12 Formularz proformy (edycja)](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) | [OP-E11-02](E-11_OP-02.md) | zawsze | User |

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E11-01 | Search | input, kliencki | [E-11_FILTR-01.md](E-11_FILTR-01.md) |

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E11-01 | Lista proform | [E-11_TAB-01.md](E-11_TAB-01.md) |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis | Algorytm |
|---|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch | — |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer proformy (seria PRF) | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |
| `clientName` | `IDocumentTableRecord.clientName` | Nazwa klienta | — |
| `issueDate` | `IDocumentTableRecord.issueDate` | Data wystawienia | — |
| `dueDate` | `IDocumentTableRecord.dueDate` | Termin płatności | — |
| `totalValue` | `IDocumentTableRecord.totalValue` | Wartość brutto | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) |
| `documentStatus` | `IDocumentTableRecord.documentStatus.status` | Status (Unpaid/Paid) | — |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E11-01 | New Proforma | [E-11_OP-01.md](E-11_OP-01.md) |
| OP-E11-02 | Edytuj (klik wiersza) | [E-11_OP-02.md](E-11_OP-02.md) |
| OP-E11-03 | Delete selected | [E-11_OP-03.md](E-11_OP-03.md) |

> Brak operacji „Transform to storno" — proformy nie podlegają przekształceniu w storno z tego ekranu.

## Modale

Brak — operacje nawigują do osobnych ekranów.

## Scenariusze testowe

→ [E-11_TC.md](E-11_TC.md) — prereq JWT, prereq DB, selektory CSS, 5 scenariuszy e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Załadowanie listy | GET | [/api/Document/GetDocumentTableRecords/2](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) | [DTO-09](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Usuń zaznaczone | PUT | [/api/Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) | `int[]` |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran: formularz proformy | [E-12 AddOrEditInvoiceProformaComponent](../E-12_AddOrEditInvoiceProformaComponent/E-12_ekran.md) |
| Ekran: lista faktur (wzorzec) | [E-09 InvoicesComponent](../E-09_InvoicesComponent/E-09_ekran.md) |
| DTO | [DTO-09 DocumentTableRecordDto](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Kolumna `documentNumber` | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Numer serii PRF nadany przy zapisie proformy; format PRF0001 |
| Kolumna `totalValue` | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | Suma brutto `Document.TotalPrice` z backend |
| Ładowanie listy (ngOnInit) | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | `GetTableRecords` filtruje proformy per UserFirm |
| OP-E11-03 UsunZaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Soft-delete; backend weryfikuje przynależność do UserFirm |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`invoice-proformas.component.ts`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/invoice-proformas.component.ts) |
| Szablon HTML | [`invoice-proformas.component.html`](../../../../InvoiceJetUI/src/app/components/invoice-proformas/invoice-proformas.component.html) |
| Model interfejsu | [`IDocumentTableRecord.ts`](../../../../InvoiceJetUI/src/app/models/IDocumentTableRecord.ts) |
| Serwis | [`document.service.ts`](../../../../InvoiceJetUI/src/app/services/document.service.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | `console.log(this.invoices)` w `loadInvoices()` — aktywny w produkcji (analogia z E-09) |
| IA-02 | `console.log(documentIds)` w `deleteSelected()` — aktywny w produkcji |
| IA-03 | Brak obsługi błędów API w UI — `console.error` bez komunikatu dla użytkownika |
| IA-04 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |
| IA-05 | Brak spinner/skeleton przy ładowaniu tabeli |
| IA-06 | Brak komunikatu „brak wyników" gdy tabela pusta |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — adaptacja z wzorca E-09 i źródła faktury_proforma/lista_faktur_proforma/ekran.md. |
