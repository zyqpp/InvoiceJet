# Ekran: Register

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-02 |
| Trasa | `/register` |
| Komponent | `RegisterComponent` |
| Plik | `src/app/components/register/register.component.ts` |
| AuthGuard | NIE |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Strona rejestracji nowego konta. Dostępna publicznie. Formularz reaktywny Angular.

## Pola formularza

| Pole | Walidacja | Opis |
|---|---|---|
| `firstName` | required | Imię |
| `lastName` | required | Nazwisko |
| `email` | required | Adres email |
| `password` | required | Hasło (min 8 znaków, regex walidowany po stronie API) |
| `passwordConfirmation` | required | Potwierdzenie hasła |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Submit formularza | `POST /api/Auth/register` przez `AuthService.register()` |

## Przepływ po submit

1. Wywołanie `authService.register({firstName, lastName, email, password, passwordConfirmation})`
2. Sukces → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd (400/409) → `errorMessage` wyświetlony na ekranie

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
