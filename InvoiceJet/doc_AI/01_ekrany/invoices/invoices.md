# Ekran: Lista faktur (Invoices)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-09 |
| Trasa | `/dashboard/invoices` |
| Komponent | `InvoicesComponent` |
| Plik | `src/app/components/invoices/invoices.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista faktur zwykłych (DocumentTypeId=1). Tabela z sortowaniem, paginacją, filtrowaniem. Możliwość zaznaczenia wielu, usunięcia, nawigacji do edycji, przekształcenia w storno.

## Kolumny tabeli

| Kolumna | Źródło | Opis |
|---|---|---|
| Checkbox | `selection` | Zaznaczanie |
| `documentNumber` | `IDocumentTableRecord.documentNumber` | Numer faktury |
| `clientName` | `IDocumentTableRecord.clientName` | Nazwa klienta |
| `issueDate` | `IDocumentTableRecord.issueDate` | Data wystawienia |
| `dueDate` | `IDocumentTableRecord.dueDate` | Termin płatności |
| `totalValue` | `IDocumentTableRecord.totalValue` | Wartość brutto |
| `documentStatus` | `IDocumentTableRecord.documentStatus.status` | Status (Unpaid/Paid) |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | `GET /api/Document/GetDocumentTableRecords/1` |
| Usunięcie zaznaczonych | `PUT /api/Document/DeleteDocuments` z `[FromBody] int[]` |
| Przekształcenie w storno | `PUT /api/Document/TransformToStorno` z `[FromBody] int[]` |

## Nawigacja

| Akcja | Cel |
|---|---|
| Klik "Add Invoice" | `router.navigate(["/dashboard/add-invoice"])` |
| Klik wiersz (edycja) | `router.navigate(["/dashboard/edit-invoice", id])` |

## Anomalie

| # | Anomalia |
|---|---|
| IA-01 | `console.log(this.invoices)` w `loadInvoices()` |
| IA-02 | `console.log(documentIds)` dwukrotnie — w `deleteSelected()` i `transformToStorno()` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
