# Wystawienie nowej faktury - Przeglad end-to-end

## 1. Cel

Przeplyw opisuje utworzenie faktury z ekranu `Invoice Details`. Formularz pobiera dane pomocnicze z API, przyjmuje klienta, serie dokumentu, daty i pozycje dokumentu, a nastepnie zapisuje dokument w bazie.

## 2. Diagram

```mermaid
sequenceDiagram
  actor Tester
  participant UI as AddOrEditInvoiceComponent
  participant FS as DocumentService Angular
  participant API as DocumentController
  participant BS as DocumentService backend
  participant DB as SQL Server

  Tester->>UI: otwarcie /dashboard/add-invoice
  UI->>FS: getDocumentAutofillInfo(1)
  FS->>API: GET /api/Document/GetDocumentAutofillInfo/1
  API->>BS: GetDocumentAutofillInfo(1)
  BS->>DB: odczyt Firm, DocumentSeries, DocumentStatus, Product
  DB-->>BS: dane pomocnicze
  BS-->>API: DocumentAutofillDto
  API-->>FS: 200 OK
  FS-->>UI: dane do formularza
  Tester->>UI: wypelnienie formularza i klikniecie Issue
  UI->>FS: addDocument(documentData)
  FS->>API: POST /api/Document/AddDocument
  API->>BS: AddDocument(DocumentRequestDto)
  BS->>DB: zapis Document
  BS->>DB: zapis DocumentProduct i Product dla nowych pozycji
  BS->>DB: aktualizacja DocumentSeries.CurrentNumber
  API-->>FS: 200 OK
  FS-->>UI: sukces
  UI-->>Tester: toastr i powrot do /dashboard/invoices
```

## 3. Warunki wejscia

| Warunek | Zrodlo |
|---|---|
| Uzytkownik jest zalogowany | `AuthGuard`, `[Authorize(Roles = "User")]` |
| Uzytkownik ma aktywna firme | `Users.GetUserFirmIdAsync()` |
| Aktywna firma ma aktywne konto bankowe | `BankAccounts.Query().Where(ba => ba.UserFirmId == userFirmId && ba.IsActive)` |
| Istnieje seria dokumentu dla typu `1` | `DocumentSeries` filtrowane po `DocumentTypeId == 1` |

## 4. Wynik

| Warstwa | Skutek |
|---|---|
| UI | Komunikat `Document added successfully` i przejscie do `/dashboard/invoices`. |
| API | `POST /api/Document/AddDocument` zwraca `200 OK`. |
| Backend | `DocumentService.AddDocument()` tworzy dokument i pozycje. |
| Baza | Zapisy w `Document`, `DocumentProduct`, opcjonalnie `Product`; aktualizacja `DocumentSeries.CurrentNumber`. |
