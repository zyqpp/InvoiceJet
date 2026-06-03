# Klasa Bazowa: Formularz dokumentu (BaseInvoiceComponent)

| Atrybut | Wartość |
|---|---|
| ID | BASE-01 |
| Klasa | `BaseInvoiceComponent` (abstract) |
| Plik | `src/app/components/invoices/add-or-edit-invoice/base-invoice.component.ts` |
| Dziedziczą | EKRAN-10, EKRAN-12, EKRAN-14 |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Abstrakcyjna klasa bazowa dla formularzy tworzenia/edycji dokumentów (faktura, proforma, storno). Zawiera całą logikę UI i API wspólną dla wszystkich 3 typów. Klasy pochodne dostarczają wyłącznie `getDocumentTypeId()` i `getNavigationUrl()`.

## Metody abstrakcyjne

```typescript
abstract getDocumentTypeId(): number;    // 1 = Faktura, 2 = Proforma, 3 = Storno
abstract getNavigationUrl(): string;     // trasa powrotu po zapisaniu
```

## Pola formularza

| Pole | Kontrolka | Opis |
|---|---|---|
| `documentSeriesId` | `mat-select` | Seria numeracji |
| `clientId` | `mat-select` + autocomplete | Klient (firma) |
| `bankAccountId` | `mat-select` | Konto bankowe |
| `issueDate` | `mat-datepicker` | Data wystawienia |
| `dueDate` | `mat-datepicker` | Termin płatności |
| `currency` | `mat-select` | Waluta (z konta bankowego) |
| `documentStatus` | `mat-select` | Status (Wysłana, Zapłacona itd.) |
| `products` | tabela dynamiczna | Lista pozycji dokumentu |

## State komponentu

| Pole | Typ | Opis |
|---|---|---|
| `isEditMode` | `boolean` | `true` gdy URL zawiera `:id` |
| `documentId` | `number` | ID edytowanego dokumentu |
| `autofillInfo` | `IDocumentAutofillInfo` | Dane wstępne (serie, klienci, konta) |
| `invoiceForm` | `FormGroup` | Reaktywny formularz dokumentu |
| `products` | `FormArray` | Tablica pozycji dokumentu |
| `totalNetAmount` | `number` | Suma netto (computed) |
| `totalVatAmount` | `number` | Suma VAT (computed) |
| `totalGrossAmount` | `number` | Suma brutto (computed) |

## Lifecycle

### ngOnInit
1. Sprawdzenie czy URL zawiera `:id` → `isEditMode`
2. Wywołanie `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` → wypełnienie selektorów
3. Jeśli `isEditMode` → `GET /api/Document/GetDocumentById/{id}` → wstępne wypełnienie formularza

### onSubmit
1. Walidacja formularza
2. Jeśli `isEditMode` → `PUT /api/Document/Edit`
3. Jeśli `!isEditMode` → `POST /api/Document/Add`
4. Sukces → `router.navigate([getNavigationUrl()])`

## Dynamiczne pozycje dokumentu

- Każda pozycja to `FormGroup` w `FormArray`
- Pola pozycji: `productId`, `quantity`, `price`, `vatRate`, `name`, `measureUnit`
- Wartości `price`, `vatRate`, `name`, `measureUnit` autouzupełniane po wyborze produktu z katalogu
- Sumy przeliczane reaktywnie przy każdej zmianie

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Autouzupełnienie selektorów | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| Załadowanie do edycji | `GET /api/Document/GetDocumentById/{id}` |
| Dodanie dokumentu | `POST /api/Document/Add` |
| Edycja dokumentu | `PUT /api/Document/Edit` |

## Klasy pochodne

| Klasa | EKRAN | `documentTypeId` | `navigationUrl` |
|---|---|---|---|
| `AddOrEditInvoiceComponent` | EKRAN-10 | `1` | `/dashboard/invoices` |
| `AddOrEditInvoiceProformaComponent` | EKRAN-12 | `2` | `/dashboard/invoice-proformas` |
| `AddOrEditInvoiceStornosComponent` | EKRAN-14 | `3` | `/dashboard/invoice-stornos` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
