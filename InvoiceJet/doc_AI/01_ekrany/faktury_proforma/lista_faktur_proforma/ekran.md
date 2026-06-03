# InvoiceProformasComponent — Lista faktur proforma

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-ListaProform |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran listy faktur proforma (DocumentTypeId=2). Identyczna struktura jak `InvoicesComponent` (lista faktur zwykłych), lecz bez funkcji „Przekształć w storno". Prezentuje tabelę proform z sortowaniem, paginacją i filtrowaniem. Umożliwia usunięcie zaznaczonych proform (batch) oraz nawigację do tworzenia nowej i edycji istniejącej proformy. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────────┐
│ Proformy                                   [+ Dodaj proformę]    │
├──┬──────────────┬───────────────┬───────────┬──────────┬─────────┤
│☐ │ Numer        │ Klient        │ Wystawiono│ Termin   │ Brutto  │
├──┼──────────────┼───────────────┼───────────┼──────────┼─────────┤
│☐ │ PRF0012      │ Firma XYZ     │ 2026-05-10│2026-05-24│ 5000    │
├──┴──────────────┴───────────────┴───────────┴──────────┴─────────┤
│ [Usuń zaznaczone]                              [Paginacja]        │
└──────────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoice-proformas` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Proformy" w Sidebar; przekierowanie po zapisaniu proformy |
| Powiązany kod komponentu | `src/app/components/invoice-proformas/invoice-proformas.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/add-invoice-proforma` | Klik „Dodaj proformę" | Zawsze | User |
| `/dashboard/edit-invoice-proforma/:id` | Klik wiersza (edycja) | Zawsze | User |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-ListaProform-Szukaj | Filtr wyszukiwania | input (MatTableDataSource filter) | — |

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-ListaProform-ListaProform | Lista proform | — |

### Kolumny tabeli

Identyczne jak `lista_faktur/ekran.md` — patrz `IDocumentTableRecord`.

| Kolumna | Źródło danych | Opis | Algorytm |
|---|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch | — |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer proformy | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) — seria PRF; format PRF0001 |
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
| OP-ListaProform-DodajProferme | Dodaj proformę | — |
| OP-ListaProform-EdytujProferme | Edytuj (klik wiersza) | — |
| OP-ListaProform-UsunZaznaczone | Usuń zaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) — soft-delete, tylko proformy bieżącej firmy |

### Modale

Brak.

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | [GET /api/Document/GetTableRecords](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md) |
| Usunięcie zaznaczonych | [PUT /api/Document/Delete](../../../04_api_i_integracje/01_api_frontend/document/PUT_Document_Delete.md) z `[FromBody] int[]` |

## Powiązania

- Powiązane procesy: [pobierz_dokumenty](../../../02_procesy/dokumenty/pobierz_dokumenty/proces.md), [usun_dokumenty](../../../02_procesy/dokumenty/usun_dokumenty/proces.md)
- Powiązane API: [GET /api/Document/GetTableRecords](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md)
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Kolumna `documentNumber` | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) | Numer serii PRF nadany przy zapisie proformy |
| Kolumna `totalValue` | [ALG-05 Obliczanie wartości dokumentu](../../../03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md) | Suma brutto `Document.TotalPrice` z backend |
| Ładowanie listy (ngOnInit) | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | `GetTableRecords` filtruje proformy per UserFirm |
| OP-ListaProform-UsunZaznaczone | [ALG-10 Izolacja danych](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Soft-delete; backend weryfikuje przynależność |

## Powiązania z kodem

- Komponent: `src/app/components/invoice-proformas/invoice-proformas.component.ts`
- Szablon HTML: `src/app/components/invoice-proformas/invoice-proformas.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoice_proformas/invoice-proformas.md`. |
