# Dodaj konto bankowe — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-AddBankAccount |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces tworzy nowe konto bankowe i przypisuje je do firmy zalogowanego użytkownika przez `UserFirmId`. Konto bankowe będzie wyświetlane na fakturach jako dane do przelewu. Nie ma walidacji formatu IBAN po stronie backendu — odpowiedzialność leży po stronie frontendu.

## Cel procesu

Dodać dane konta bankowego firmy (nazwa banku, IBAN, waluta), aby można je było umieszczać na wystawianych dokumentach.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-AddBankAccount |
| Typ | główny |
| Inicjator | Ekran „Konta bankowe" + dialog „Dodaj konto" + operacja zapisu |
| Warunki startu | Użytkownik zalogowany (JWT); formularz konta bankowego wypełniony |
| Warunki zakończenia (sukces) | Rekord `BankAccount` zapisany w DB; HTTP 201 |
| Warunki zakończenia (błąd) | Błąd DB (nieoczekiwany) |
| Uczestnicy | Frontend (Angular), API (BankAccountController), Service (BankAccountService), Repository (BankAccountRepository), Database (dbo.BankAccount) |

## Diagram sekwencji

```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as BankAccountController
    participant S as BankAccountService
    participant R as BankAccountRepository
    participant D as Database

    F->>A: POST /api/BankAccount/Add (BankAccountRequestDto)
    A->>S: Add(bankAccountRequestDto)
    S->>S: Pobierz userId z JWT claims
    S->>R: GetUserFirmIdByUserId(userId)
    R->>D: SELECT UserFirmId FROM UserFirm WHERE UserId = @userId
    D-->>R: userFirmId
    R-->>S: userFirmId
    S->>S: Mapuj BankAccountRequestDto → BankAccount; ustaw UserFirmId
    S->>R: AddAsync(bankAccount) + CompleteAsync()
    R->>D: INSERT INTO BankAccount (BankName, Iban, Currency, UserFirmId)
    D-->>R: OK
    R-->>S: OK
    S-->>A: 201 Created
    A-->>F: 201 Created
```

## Kroki

1. **Odbiór żądania** — `BankAccountController` odbiera `BankAccountRequestDto` z POST `/api/BankAccount/Add`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pobranie UserFirmId** — zapytanie przez repozytorium.
4. **Mapowanie i przypisanie** — `AutoMapper` mapuje DTO → `BankAccount`; serwis ustawia `UserFirmId`.
5. **Zapis** — `BankAccountRepository.AddAsync(bankAccount)` + `UnitOfWork.CompleteAsync()`.
6. **Odpowiedź** — HTTP 201 Created.

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |
| Błąd DB (nieoczekiwany) | BankAccountRepository | HTTP 500 Internal Server Error (ExceptionMiddleware) |

## Powiązania

- Wywołany z ekranu: `01_ekrany/firma/konta_bankowe/`
- Powiązane API: `POST /api/BankAccount/Add`
- Powiązany algorytm: Nie dotyczy

## Powiązania z kodem

- Kontroler: `InvoiceJetAPI/Controllers/BankAccountController.cs`
- Serwis: `InvoiceJetAPI/Services/BankAccountService.cs`
- Repozytorium: `InvoiceJetAPI/Repositories/BankAccountRepository.cs`

## Wątpliwości i braki

- Brak walidacji formatu IBAN po stronie backendu.
- Brak limitu liczby kont bankowych per firma.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wyodrębniona z P-05_ManageBankAccounts.md (operacja Add). |
