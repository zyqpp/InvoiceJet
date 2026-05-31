# InvoiceStornosComponent — Lista faktur storno

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-ListaStorn |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran listy faktur storno (DocumentTypeId=3). Storna nie mogą być tworzone bezpośrednio z tego ekranu — brak przycisku „Dodaj storno" i brak trasy `/add-invoice-storno` linkowanej z UI. Storna powstają wyłącznie przez operację „Przekształć w storno" z listy faktur zwykłych. Na tym ekranie możliwa jest edycja istniejącego storna i usunięcie zaznaczonych. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌──────────────────────────────────────────────────────────────┐
│ Storna                                                        │
├──┬──────────────┬───────────────┬───────────┬──────────┬─────┤
│☐ │ Numer        │ Klient        │ Wystawiono│ Termin   │Brutto│
├──┼──────────────┼───────────────┼───────────┼──────────┼─────┤
│☐ │ STORNO0001   │ Firma ABC S.A.│ 2026-05-02│2026-05-16│ -600│
├──┴──────────────┴───────────────┴───────────┴──────────┴─────┤
│ [Usuń zaznaczone]                           [Paginacja]       │
└──────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/invoice-stornos` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Storna" w Sidebar; przekierowanie po operacji TransformToStorno z listy faktur |
| Powiązany kod komponentu | `src/app/components/invoice-stornos/invoice-stornos.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard/edit-invoice-storno/:id` | Klik wiersza (edycja) | Zawsze | User |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-ListaStorn-Szukaj | Filtr wyszukiwania | input (MatTableDataSource filter) | — |

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-ListaStorn-ListaStorn | Lista storn | — |

### Kolumny tabeli

Identyczne jak `lista_faktur/ekran.md` — patrz `IDocumentTableRecord`.

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer storna |
| `clientName` | `IDocumentTableRecord.clientName` | Nazwa klienta |
| `issueDate` | `IDocumentTableRecord.issueDate` | Data wystawienia |
| `dueDate` | `IDocumentTableRecord.dueDate` | Termin płatności |
| `totalValue` | `IDocumentTableRecord.totalValue` | Wartość brutto |
| `documentStatus` | `IDocumentTableRecord.documentStatus.status` | Status |

### Pola

Brak (ekran listowy).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-ListaStorn-EdytujStorno | Edytuj (klik wiersza) | — |
| OP-ListaStorn-UsunZaznaczone | Usuń zaznaczone | — |

### Modale

Brak.

### Powiadomienia

Brak.

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | `GET /api/Document/GetDocumentTableRecords/3` |
| Usunięcie zaznaczonych | `PUT /api/Document/DeleteDocuments` z `[FromBody] int[]` |

## Powiązania

- Powiązane procesy: `../../02_procesy/dokumenty/pobierz_dokumenty/proces.md`, `../../02_procesy/dokumenty/usun_dokumenty/proces.md`, `../../02_procesy/dokumenty/transformuj_na_storno/proces.md`
- Powiązane API: `../../04_api_i_integracje/01_api_frontend/document/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/invoice-stornos/invoice-stornos.component.ts`
- Szablon HTML: `src/app/components/invoice-stornos/invoice-stornos.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- `console.log(this.selection.selected)` i `console.log(documentIds)` aktywne w `deleteSelected()`.
- Brak przycisku „Dodaj storno" w UI — ale trasa `/dashboard/add-invoice-storno` istnieje w konfiguracji routingu. Niespójność: formularz `AddOrEditInvoiceStornosComponent` obsługuje dodawanie, lecz UI go nie eksponuje.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `invoice_stornos/invoice-stornos.md`. |
