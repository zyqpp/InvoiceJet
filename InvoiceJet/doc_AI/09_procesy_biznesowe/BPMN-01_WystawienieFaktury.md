# Proces biznesowy: Wystawienie faktury (BPMN)

| Atrybut | Wartość |
|---|---|
| ID | BPMN-01 |
| Nazwa | Wystawienie faktury |
| Uczestnicy | Użytkownik, InvoiceJet Frontend, InvoiceJet Backend, ANAF API |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Diagram procesu (Mermaid)

```mermaid
sequenceDiagram
    participant U as Użytkownik
    participant FE as Frontend (Angular)
    participant BE as Backend (API)
    participant DB as SQL Server
    participant ANAF as ANAF API

    U->>FE: Klik "Nowa faktura"
    FE->>BE: GET /api/Document/GetDocumentAutofillInfo/1
    BE->>DB: SELECT DocumentSeries, Clients, BankAccounts, Products, Statuses
    DB-->>BE: Dane autouzupełnienia
    BE-->>FE: DocumentAutofillInfoDto

    FE-->>U: Formularz z selektorami

    alt Autouzupełnienie klienta z ANAF
        U->>FE: Wpisuje CUI + klika ikonę chmury
        FE->>BE: GET /api/Firm/fromAnaf/{cui}
        BE->>ANAF: POST [{cui, data}]
        ANAF-->>BE: Dane firmy
        BE-->>FE: FirmRequestDto
        FE-->>U: Autouzupełnienie pól klienta
    end

    U->>FE: Wypełnia formularz i dodaje pozycje
    FE-->>U: Sumy obliczane na żywo (netto/VAT/brutto)
    U->>FE: Klik "Zapisz"

    FE->>BE: POST /api/Document/Add (DocumentRequestDto)
    BE->>DB: INSERT Document
    BE->>DB: INSERT DocumentProducts[]
    BE->>DB: UPDATE DocumentSeries (CurrentNumber++)
    DB-->>BE: OK
    BE-->>FE: 201 Created + documentId

    FE->>FE: router.navigate('/dashboard/invoices')
    FE-->>U: Lista faktur z nową fakturą

    opt Generuj PDF
        U->>FE: Klik "PDF"
        FE->>BE: POST /api/Document/GetPdfStream {documentId}
        BE->>DB: SELECT Document z wszystkimi JOIN
        DB-->>BE: Document data
        BE->>BE: InvoiceDocumentFactory.Create(typeId)
        BE->>BE: QuestPDF GeneratePdf()
        BE-->>FE: FileStreamResult (application/pdf)
        FE-->>U: PDF otwarty w przeglądarce
    end
```

## Ścieżki alternatywne

### Błąd walidacji
- Brak wymaganego pola → frontend pokazuje błąd walidacji; żądanie nie wysyłane
- DocumentSeries nie istnieje → Backend 404 → Frontend toastr error

### Wygaśnięcie sesji w trakcie
- JWT wygasa → JwtInterceptor łapie 401 → TokenExpiredDialog → redirect do /login
- Dane niezapisanego formularza przepadają

### ANAF niedostępny
- Timeout lub błąd → Frontend toastr error → Użytkownik wpisuje dane ręcznie

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
