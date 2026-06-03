# InvoicesComponent — Lista faktur

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-ListaFaktur |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran listy faktur zwykłych (DocumentTypeId=1). Prezentuje tabelę z sortowaniem, paginacją i filtrowaniem. Umożliwia zaznaczenie wielu faktur i wykonanie operacji batch: usunięcie lub przekształcenie w faktury storno. Dostępna nawigacja do tworzenia nowej faktury i edycji istniejącej. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌────────────────────────────────────────────────────────────────┐
│ Faktury                                    [+ Dodaj fakturę]   │
├──┬──────────────┬───────────────┬───────────┬──────────┬───────┤
│☐ │ Numer faktury│ Klient        │ Wystawiono│ Termin   │ Brutto│
│  │              │               │           │ płatności│       │
├──┼──────────────┼───────────────┼───────────┼──────────┼───────┤
│☐ │ FV0005       │ Firma ABC S.A.│ 2026-05-01│2026-05-15│ 1230  │
├──┴──────────────┴───────────────┴───────────┴──────────┴───────┤
│[Usuń zaznaczone] [Przekształć w storno]       [Paginacja]      │
└────────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoices` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Faktury" w Sidebar; przekierowanie po zapisaniu faktury |
| Powiązany kod komponentu | `src/app/components/invoices/invoices.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/add-invoice` | Klik „Dodaj fakturę" | Zawsze | User |
| `/dashboard/edit-invoice/:id` | Klik wiersza (edycja) | Zawsze | User |
| `/dashboard/invoice-stornos` | „Przekształć w storno" (sukces) | Zaznaczone faktury | User |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-ListaFaktur-Szukaj | Filtr wyszukiwania | input (MatTableDataSource filter) | — |

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-ListaFaktur-ListaFaktur | Lista faktur | — |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis | Algorytm |
|---|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch | — |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer faktury | [ALG-02 Generowanie numeru](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — format: SeriesName + CurrentNumber.D4 |
| `clientName` | `IDocumentTableRecord.clientName` | Nazwa klienta | — |
| `issueDate` | `IDocumentTableRecord.issueDate` | Data wystawienia | — |
| `dueDate` | `IDocumentTableRecord.dueDate` | Termin płatności | — |
| `totalValue` | `IDocumentTableRecord.totalValue` | Wartość brutto | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) — suma wszystkich pozycji brutto |
| `documentStatus` | `IDocumentTableRecord.documentStatus.status` | Status (Unpaid/Paid) | — |

### Pola

Brak (ekran listowy).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-ListaFaktur-DodajFakture | Dodaj fakturę | — |
| OP-ListaFaktur-EdytujFakture | Edytuj (klik wiersza) | — |
| OP-ListaFaktur-UsunZaznaczone | Usuń zaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — soft-delete, działa tylko na dokumenty bieżącej firmy |
| OP-ListaFaktur-TransformujNaStorno | Przekształć w storno | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) — zmiana DocumentTypeId=3, wartości ujemne |

### Modale

Brak.

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | [GET /api/Document/GetTableRecords](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) |
| Usunięcie zaznaczonych | [PUT /api/Document/Delete](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) z `[FromBody] int[]` |
| Przekształcenie w storno | [PUT /api/Document/TransformToStorno](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_TransformToStorno.md) z `[FromBody] int[]` |

## Powiązania

- Powiązane procesy: [pobierz_dokumenty](../../../02_procesy/dokumenty/pobierz_dokumenty/proces.md), [usun_dokumenty](../../../02_procesy/dokumenty/usun_dokumenty/proces.md), [transformuj_na_storno](../../../02_procesy/dokumenty/transformuj_na_storno/proces.md)
- Powiązane API: [GET /api/Document/GetTableRecords](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Kolumna `documentNumber` | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Numer wyświetlony w liście jest wynikiem algorytmu nadania numeru przy zapisie faktury |
| Kolumna `totalValue` | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | Suma brutto wyliczona przez backend (`UpdateDocumentProducts`) i przechowana w `Document.TotalPrice` |
| OP-ListaFaktur-TransformujNaStorno | [ALG-08 Transformacja na storno](../../../03_algorytmy/dedykowane/transformacja_na_storno.md) | Zmiana DocumentTypeId → 3, odwrócenie wartości; ⚠️ brak atomowości (race condition) |
| OP-ListaFaktur-UsunZaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Soft-delete (IsDeleted=true); backend weryfikuje przynależność do UserFirm |
| Ładowanie listy (ngOnInit) | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | `GetTableRecords` filtruje dokumenty per UserFirm automatycznie |

## Powiązania z kodem

- Komponent: `src/app/components/invoices/invoices.component.ts`
- Szablon HTML: `src/app/components/invoices/invoices.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- IA-01: `console.log(this.invoices)` aktywny w `loadInvoices()`.
- IA-02: `console.log(documentIds)` aktywny dwukrotnie — w `deleteSelected()` i `transformToStorno()`.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoices/invoices.md`. |
