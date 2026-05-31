# Dodaj firmę — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-AddFirm |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces umożliwia zalogowanemu użytkownikowi dodanie firmy do systemu. Parametr `isClient` decyduje o roli firmy: `false` — własna firma wystawiającego (przypisywana do `UserFirm`), `true` — firma klienta (dodawana do listy klientów `UserFirm.ClientFirms`). Jeden endpoint obsługuje oba przypadki. Po zapisaniu firma jest dostępna w selektorach formularzy dokumentów.

## Cel procesu

Zapisać nową firmę (własną lub klienta) powiązaną z kontem zalogowanego użytkownika, tak aby mogła być używana przy wystawianiu dokumentów.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-AddFirm |
| Typ | główny |
| Inicjator | Ekran danych firmy (`isClient=false`) lub dialog dodania klienta (`isClient=true`) + operacja „Dodaj" |
| Warunki startu | Użytkownik zalogowany (JWT); wypełniony formularz danych firmy |
| Warunki zakończenia (sukces) | Rekord `Firm` zapisany w DB; powiązanie z `UserFirm` zaktualizowane; HTTP 201 |
| Warunki zakończenia (błąd) | Brak — nie ma zdefiniowanych wyjątków dla AddFirm (walidacja po stronie frontu) |
| Uczestnicy | Frontend (Angular), API (FirmController), Service (FirmService), Repository (FirmRepository, UserFirmRepository), Database (dbo.Firm, dbo.UserFirm) |

## Diagram sekwencji

```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as FirmController
    participant S as FirmService
    participant R as FirmRepository / UserFirmRepository
    participant D as Database

    F->>A: POST /api/Firm/AddFirm/{isClient} (FirmRequestDto)
    A->>S: AddFirm(firmRequestDto, isClient)
    S->>S: Pobierz userId z JWT claims
    S->>R: GetUserFirmByUserId(userId)
    R->>D: SELECT UserFirm WHERE UserId = @userId
    D-->>R: UserFirm
    R-->>S: userFirm
    alt isClient = false
        S->>R: AddAsync(firm) — przypisz UserFirm.FirmId
        R->>D: INSERT INTO Firm; UPDATE UserFirm SET FirmId = @firmId
    else isClient = true
        S->>R: AddAsync(firm) — dodaj do UserFirm.ClientFirms
        R->>D: INSERT INTO Firm; INSERT INTO UserFirmClientFirm (powiązanie)
    end
    R-->>S: OK
    S-->>A: 201 Created
    A-->>F: 201 Created
```

## Kroki

1. **Odbiór żądania** — `FirmController` odbiera `FirmRequestDto` i parametr ścieżki `isClient` (bool) z POST `/api/Firm/AddFirm/{isClient}`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pobranie UserFirm** — `UserFirmRepository.GetUserFirmByUserId(userId)` zwraca bieżące powiązanie użytkownika.
4. **Rozgałęzienie logiki wg `isClient`**:
   - `false` — tworzy nowy rekord `Firm` i ustawia go jako własną firmę użytkownika (`UserFirm.FirmId`).
   - `true` — tworzy nowy rekord `Firm` i dodaje go do kolekcji klientów (`UserFirm.ClientFirms`).
5. **Zapis** — `FirmRepository.AddAsync(firm)` + `UnitOfWork.CompleteAsync()`.
6. **Odpowiedź** — HTTP 201 Created.

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |
| Błąd DB (nieoczekiwany) | FirmRepository | HTTP 500 Internal Server Error (ExceptionMiddleware) |

## Powiązania

- Wywołany z ekranu: `01_ekrany/firma/dane_firmy/` (`isClient=false`), `01_ekrany/firma/klienci/` (`isClient=true`)
- Powiązane API: `POST /api/Firm/AddFirm/{isClient}`
- Powiązany algorytm: Nie dotyczy

## Powiązania z kodem

- Kontroler: `InvoiceJetAPI/Controllers/FirmController.cs`
- Serwis: `InvoiceJetAPI/Services/FirmService.cs`
- Repozytorium: `InvoiceJetAPI/Repositories/FirmRepository.cs`, `InvoiceJetAPI/Repositories/UserFirmRepository.cs`

## Wątpliwości i braki

- Brak walidacji unikalności CUI (`cuiValue`) na poziomie backendu — możliwe zduplikowane firmy z tym samym NIP.
- Niejasna logika powiązania `UserFirm` dla pierwszej firmy użytkownika (brak dokumentacji przepływu inicjalnego).

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wyodrębniona z P-03_ManageFirm.md (operacja AddFirm). |
