# Ekran: Login

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-01 |
| Trasa | `/login` |
| Komponent | `LoginComponent` |
| Plik | `src/app/components/login/login.component.ts` |
| AuthGuard | NIE |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Strona logowania. Dostępna publicznie (bez AuthGuard). Formularz reaktywny Angular.

## Pola formularza

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `email` | `mat-form-field` + `input[type=email]` | required | Adres email |
| `password` | `mat-form-field` + `input[type=password]` | required | Hasło; toggle widoczności przez `hide` |

## State komponentu

| Pole | Typ | Opis |
|---|---|---|
| `errorMessage` | `string \| null` | Komunikat błędu z API |
| `hide` | `boolean` | Ukrycie/pokazanie hasła (domyślnie `true`) |
| `loginForm` | `FormGroup` | Reaktywny formularz (email, password) |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Submit formularza | `POST /api/Auth/login` przez `AuthService.login()` |

## Przepływ po submit

1. `loginForm.valid` → wywołanie `authService.login({email, password})`
2. Sukces → `localStorage.setItem("authToken", response.token)` → `router.navigate(["/dashboard"])`
3. Błąd → `errorMessage = error.error` (wyświetlony na ekranie)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
