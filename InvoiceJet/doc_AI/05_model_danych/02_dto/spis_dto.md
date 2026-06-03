# Spis DTO — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | SPIS-DTO-01 |
| Typ dokumentu | Spis zbiorczy |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Opis

Zbiorczy spis wszystkich 14 DTO projektu InvoiceJet. DTO stanowią kontrakt API między frontendem Angular 16 a backendem ASP.NET Core 8. Kierunek "Żądanie" oznacza dane przesyłane przez frontend do backendu; "Odpowiedź" oznacza dane zwracane przez backend; "Oba" — DTO reużywany w obu kierunkach; "Zagnieżdżony" — DTO będący elementem innego DTO.

## Tabela DTO

| ID | Nazwa DTO | Cel | Kierunek | Powiązany endpoint |
|---|---|---|---|---|
| [DTO-01](DTO-01_RegisterUserDto.md) | `RegisterUserDto` | Rejestracja użytkownika | Żądanie | `POST /api/Auth/register` |
| [DTO-02](DTO-02_LoginUserDto.md) | `LoginUserDto` | Logowanie użytkownika | Żądanie | `POST /api/Auth/login` |
| [DTO-03](DTO-03_FirmRequestDto.md) | `FirmRequestDto` | Dane firmy (własna i klienci) | Oba | `POST/PUT /api/Firm`, `GET /api/Firm/GetUserActiveFirm` |
| [DTO-04](DTO-04_BankAccountRequestDto.md) | `BankAccountRequestDto` | Konto bankowe firmy | Oba | `GET/POST/PUT /api/BankAccount` |
| [DTO-05](DTO-05_ProductRequestDto.md) | `ProductRequestDto` | Produkt lub usługa z katalogu | Oba | `GET/POST/PUT /api/Product` |
| [DTO-06](DTO-06_DocumentSeriesRequestDto.md) | `DocumentSeriesRequestDto` | Seria numeracji dokumentów | Oba | `GET/POST/PUT /api/DocumentSeries` |
| [DTO-07](DTO-07_DocumentRequestDto.md) | `DocumentRequestDto` | Dokument (faktura/proforma/storno) | Oba | `POST/PUT /api/Document/Add`, `GET /api/Document/GetDocumentById/{id}` |
| [DTO-08](DTO-08_DocumentProductRequestDto.md) | `DocumentProductRequestDto` | Pozycja dokumentu (linia) | Zagnieżdżony w DTO-07 | — (element `DocumentRequestDto.Products`) |
| [DTO-09](DTO-09_DocumentTableRecordDto.md) | `DocumentTableRecordDto` | Rekord widoku tabelarycznego dokumentów | Odpowiedź | `GET /api/Document/GetTableRecords/{documentTypeId}` |
| [DTO-10](DTO-10_DocumentAutofillInfoDto.md) | `DocumentAutofillInfoDto` | Dane autouzupełnienia formularza dokumentu | Odpowiedź | `GET /api/Document/GetDocumentAutofillInfo/{documentTypeId}` |
| [DTO-11](DTO-11_DocumentStatusDto.md) | `DocumentStatusDto` | Status dokumentu (słownik) | Odpowiedź/Zagnieżdżony | Zagnieżdżony w `DocumentAutofillInfoDto.DocumentStatuses` |
| [DTO-12](DTO-12_DashboardStatsDto.md) | `DashboardStatsDto` | Statystyki dashboardu (liczniki + miesięczne sumy) | Odpowiedź | `GET /api/Document/GetDashboardStats/{year}/{documentType}` |
| [DTO-13](DTO-13_UserDto.md) | `UserDto` | Token JWT po autentykacji | Odpowiedź | `POST /api/Auth/register`, `POST /api/Auth/login` |
| [DTO-14](DTO-14_UserFirmDto.md) | `UserFirmDto` | Powiązanie użytkownika z firmą wystawiającego | Odpowiedź | `GET /api/Firm/GetUserActiveFirm` |

## Legenda kierunków

| Kierunek | Znaczenie |
|---|---|
| Żądanie | Frontend → Backend (ciało żądania HTTP) |
| Odpowiedź | Backend → Frontend (ciało odpowiedzi HTTP) |
| Oba | DTO reużywany w obu kierunkach (request i response) |
| Zagnieżdżony | Element innego DTO — nie przesyłany samodzielnie |

## DTO złożone — zagnieżdżenia

Diagram zagnieżdżeń:

```
DocumentRequestDto (DTO-07)
├── Client: FirmRequestDto (DTO-03)
├── Seller: FirmRequestDto (DTO-03)
├── DocumentSeries: DocumentSeriesRequestDto (DTO-06)
├── BankAccount: BankAccountRequestDto (DTO-04)
└── Products: List<DocumentProductRequestDto> (DTO-08)

DocumentAutofillInfoDto (DTO-10)
├── DocumentSeries: List<DocumentSeriesRequestDto> (DTO-06)
├── Clients: List<FirmRequestDto> (DTO-03)
├── BankAccounts: List<BankAccountRequestDto> (DTO-04)
├── Products: List<ProductRequestDto> (DTO-05)
├── DocumentStatuses: List<DocumentStatusDto> (DTO-11)
└── Seller: FirmRequestDto (DTO-03)
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — spis 14 DTO. |
