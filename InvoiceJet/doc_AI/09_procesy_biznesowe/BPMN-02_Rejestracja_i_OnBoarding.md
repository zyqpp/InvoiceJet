# Proces biznesowy: Rejestracja i onboarding (BPMN)

| Atrybut | Wartość |
|---|---|
| ID | BPMN-02 |
| Nazwa | Rejestracja i konfiguracja konta |
| Uczestnicy | Nowy użytkownik, InvoiceJet Frontend, InvoiceJet Backend |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Diagram procesu (Mermaid)

```mermaid
sequenceDiagram
    participant U as Nowy użytkownik
    participant FE as Frontend
    participant BE as Backend
    participant DB as SQL Server

    U->>FE: Otwiera /register
    U->>FE: Wypełnia formularz rejestracji
    FE->>BE: POST /api/Auth/register
    BE->>DB: SELECT User WHERE Email = ?
    DB-->>BE: NULL (email wolny)
    BE->>BE: Walidacja hasła (regex)
    BE->>BE: BCrypt.HashPassword(password)
    BE->>DB: INSERT User
    BE->>DB: INSERT UserFirm (FirmId = NULL)
    DB-->>BE: OK
    BE->>BE: CreateToken(user) → JWT
    BE-->>FE: { token: "..." }

    FE->>FE: localStorage.setItem("authToken", token)
    FE->>FE: router.navigate("/dashboard")

    Note over U,FE: --- ONBOARDING ---

    U->>FE: Otwiera /dashboard/firm-details
    FE->>BE: GET /api/Firm/GetUserActiveFirm
    BE-->>FE: null (brak firmy)
    FE-->>U: Formularz dodania firmy

    opt ANAF autouzupełnienie
        U->>FE: Podaje CUI + klik chmury
        FE->>BE: GET /api/Firm/fromAnaf/{cui}
        BE-->>FE: Dane firmy z ANAF
    end

    U->>FE: Zapisuje dane firmy
    FE->>BE: POST /api/Firm/AddFirm/false
    BE->>DB: INSERT Firm
    BE->>DB: UPDATE UserFirm SET FirmId = newFirmId
    DB-->>BE: OK
    BE-->>FE: 201 Created

    U->>FE: Dodaje konto bankowe (EKRAN-06 + DIALOG-02)
    FE->>BE: POST /api/BankAccount/Add
    BE-->>FE: 201 Created

    U->>FE: Konfiguruje serie numeracji (EKRAN-08 + DIALOG-04)
    FE->>BE: POST /api/DocumentSeries/Add
    BE-->>FE: 201 Created

    Note over U: Gotowy do wystawiania faktur!
```

## Wymagania do pierwszej faktury

Aby wystawić pierwszą fakturę, użytkownik musi kolejno:
1. ✅ Zarejestrować konto
2. ✅ Dodać dane własnej firmy (EKRAN-04)
3. ✅ Dodać konto bankowe (EKRAN-06)
4. ✅ Dodać serię numeracji (EKRAN-08)
5. Opcjonalnie: Dodać klientów (EKRAN-05)
6. Opcjonalnie: Dodać produkty do katalogu (EKRAN-07)

Aplikacja nie wymusza tych kroków w określonej kolejności — użytkownik może próbować wystawić fakturę bez konfiguracji i natrafi na puste selektory.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
