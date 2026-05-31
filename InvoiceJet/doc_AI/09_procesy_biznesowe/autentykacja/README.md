# autentykacja — Procesy biznesowe uwierzytelniania

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-AUTH-README |
| Typ dokumentu | README grupy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Zakres grupy

Procesy związane z rejestracją nowego konta użytkownika, logowaniem oraz inicjalnym onboardingiem po pierwszym zalogowaniu.

## Pliki

| Plik | ID dokumentu | Opis |
|---|---|---|
| `rejestracja_i_logowanie.md` | BPMN-AUTH-01 | Rejestracja, hashowanie BCrypt, wydanie JWT, onboarding konfiguracji firmy. |

## Technologie

- `POST /api/Auth/register` — rejestracja
- `POST /api/Auth/login` — logowanie
- BCrypt — hashowanie hasła
- JWT — token autoryzacyjny
- `localStorage` — przechowywanie tokenu po stronie frontendu

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
