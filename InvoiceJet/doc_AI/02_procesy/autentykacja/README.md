# autentykacja

Procesy techniczne związane z uwierzytelnianiem i rejestracją użytkowników w systemie InvoiceJet.

## Drzewo zawartości

```
autentykacja/
├── README.md                  # ten plik
├── rejestracja/
│   └── proces.md              # PROC-RegisterUser — zakładanie nowego konta
└── logowanie/
    └── proces.md              # PROC-LoginUser — logowanie i wydanie tokenu JWT
```

## Kluczowe dokumenty

- `rejestracja/proces.md` — rejestracja nowego użytkownika (POST /api/Auth/register)
- `logowanie/proces.md` — logowanie użytkownika (POST /api/Auth/login)

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/auth/` — dokumentacja endpointów API autoryzacji
- `../../03_algorytmy/autoryzacyjne/` — algorytmy JWT (tworzenie i weryfikacja tokenu)
- `../../01_ekrany/login/` — ekran logowania
- `../../01_ekrany/register/` — ekran rejestracji

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów autentykacji. |
