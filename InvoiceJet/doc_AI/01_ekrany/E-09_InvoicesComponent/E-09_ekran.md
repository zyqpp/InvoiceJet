# E-09 InvoicesComponent — Lista faktur

| Pole | Wartość |
|---|---|
| ID dokumentu | E-09 |
| Typ dokumentu | ekran |
| Wersja | 1.1 |
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
| [E-10 Formularz faktury (dodaj)](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) | [OP-E09-01](E-09_OP-01.md) | zawsze | User |
| [E-10 Formularz faktury (edycja)](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) | [OP-E09-02](E-09_OP-02.md) | zawsze | User |
| [E-13 Lista storn](../E-13_InvoiceStornosComponent/E-13_ekran.md) | [OP-E09-04](E-09_OP-04.md) sukces | zaznaczone faktury | User |

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E09-01 | Search | input, kliencki | [E-09_FILTR-01.md](E-09_FILTR-01.md) |

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E09-01 | Lista faktur | [E-09_TAB-01.md](E-09_TAB-01.md) |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E09-01 | New Invoice | [E-09_OP-01.md](E-09_OP-01.md) |
| OP-E09-02 | Edytuj (klik wiersza) | [E-09_OP-02.md](E-09_OP-02.md) |
| OP-E09-03 | Delete selected | [E-09_OP-03.md](E-09_OP-03.md) |
| OP-E09-04 | Transform to storno | [E-09_OP-04.md](E-09_OP-04.md) |

## Modale

Brak — operacje nawigują do osobnych ekranów.

## Scenariusze testowe

→ [E-09_TC.md](E-09_TC.md) — prereq JWT, prereq DB, selektory CSS, 8 scenariuszy e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint | DTO |
|---|---|---|---|
| Załadowanie listy | GET | [/api/Document/GetDocumentTableRecords/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) | [DTO-09](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Usuń zaznaczone | PUT | [/api/Document/DeleteDocuments](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) | `int[]` |
| Przekształć w storno | PUT | [/api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) | `int[]` |

---

## Powiązania

| Typ | Dokument |
|---|---|
| Ekran: formularz faktury | [E-10 AddOrEditInvoiceComponent](../E-10_AddOrEditInvoiceComponent/E-10_ekran.md) |
| Ekran: lista storn | [E-13 InvoiceStornosComponent](../E-13_InvoiceStornosComponent/E-13_ekran.md) |
| DTO | [DTO-09 DocumentTableRecordDto](../../../05_model_danych/02_dto/DTO-09_DocumentTableRecordDto.md) |
| Model DB | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Algorytm | [ALG-08 TransformToStorno](../../../03_algorytmy/ALG-08_TransformToStorno.md) |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`invoices.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.ts) |
| Szablon HTML | [`invoices.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.html) |
| Model interfejsu | [`IDocumentTableRecord.ts`](../../../../InvoiceJetUI/src/app/models/IDocumentTableRecord.ts) |
| Serwis | [`document.service.ts`](../../../../InvoiceJetUI/src/app/services/document.service.ts) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| IA-01 | `console.log(this.invoices)` w `loadInvoices()` — aktywny w produkcji |
| IA-02 | `console.log(documentIds)` dwukrotnie w `deleteSelected()` i `transformToStorno()` |
| IA-03 | Brak obsługi błędów API w UI — `console.error` bez komunikatu dla użytkownika |
| IA-04 | Brak `data-cy` / `data-testid` — selektory nieodporne na zmiany UI |
| IA-05 | Brak spinner/skeleton przy ładowaniu tabeli |
| IA-06 | Brak komunikatu „brak wyników" gdy tabela pusta |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkic. |
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pełna wersja inline. |
| 1.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Podział na pliki — ekran.md jako indeks. |
