# Dialog: Token wygasł (Token Expired Dialog)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-06 |
| Komponent | `TokenExpiredDialogComponent` |
| Plik | `src/app/components/token-expired-dialog/token-expired-dialog.component.ts` |
| Otwierany z | `JwtInterceptor` (globalnie) |
| Typ | `MatDialog` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Dialog informujący użytkownika o wygaśnięciu sesji (JWT). Otwierany automatycznie przez `JwtInterceptor` gdy odpowiedź API zwróci kod `401 Unauthorized`.

## Mechanizm uruchomienia

```typescript
// JwtInterceptor — fragment
if (error.status === 401) {
    this.dialog.open(TokenExpiredDialogComponent);
    localStorage.removeItem("authToken");
    this.router.navigate(["/login"]);
}
```

## Zawartość dialogu

- Komunikat informujący o wygaśnięciu sesji
- Przycisk "OK" → zamknięcie dialogu + przekierowanie do `/login`

## Specyfika tokenów JWT

- JWT wygasa po **10 minutach** (`DateTime.UtcNow.AddMinutes(10)`)
- `ClockSkew = TimeSpan.Zero` — brak marginesu tolerancji
- Brak mechanizmu refresh token — po wygaśnięciu konieczne ponowne logowanie
- Token przechowywany w `localStorage` (nie `sessionStorage`, nie HttpOnly cookie)

## Anomalie

| # | Anomalia |
|---|---|
| TED-01 | 10-minutowy token JWT to bardzo krótki czas dla aplikacji biznesowej — każda przerwa w pracy (spotkanie, rozmowa) kończy sesję |
| TED-02 | Token w `localStorage` podatny na XSS |
| TED-03 | Brak refresh token — każde wygaśnięcie wymaga ponownego logowania |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
