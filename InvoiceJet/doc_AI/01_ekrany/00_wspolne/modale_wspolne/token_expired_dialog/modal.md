# TokenExpiredDialogComponent — Dialog wygaśnięcia tokenu

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-Wspolne-TokenExpired |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Globalny dialog informujący użytkownika o wygaśnięciu sesji (JWT). Otwierany automatycznie przez `JwtInterceptor` w momencie gdy odpowiedź API zwróci kod `401 Unauthorized`. Po zamknięciu dialogu użytkownik przekierowywany jest na stronę logowania. Nie ma ekranu nadrzędnego — dostępny globalnie z dowolnego miejsca w aplikacji.

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-Wspolne-TokenExpired |
| Nazwa / tytuł w UI | Sesja wygasła (token expired) |
| Wywołany przez operację | `JwtInterceptor` — automatycznie przy odpowiedzi 401 |
| Ekran nadrzędny | Globalny — każdy ekran chroniony przez AuthGuard |
| Typ modalu | informacyjny |
| Zamknięcie przez Escape | nie (wymaga kliknięcia OK) |
| Zamknięcie przez klik tła | nie |

## Wizualizacja układu

```
┌───────────────────────────────────┐
│ Twoja sesja wygasła           [X] │
├───────────────────────────────────┤
│ Twoja sesja wygasła. Zaloguj się  │
│ ponownie, aby kontynuować.        │
│                                   │
├───────────────────────────────────┤
│                          [  OK  ] │
└───────────────────────────────────┘
```

## Pola modalu

Brak (modal informacyjny, bez pól formularza).

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| OK | Zamknięcie dialogu + przekierowanie do `/login` | Brak wywołania API | tak |

## Mechanizm uruchomienia

```typescript
// JwtInterceptor — fragment
if (error.status === 401) {
    this.dialog.open(TokenExpiredDialogComponent);
    localStorage.removeItem("authToken");
    this.router.navigate(["/login"]);
}
```

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Zamknięcie | Użytkownik klika OK | Brak | Przekierowanie na `/login`; token usunięty z `localStorage` |

## Specyfika tokenów JWT

- JWT wygasa po **10 minutach** (`DateTime.UtcNow.AddMinutes(10)`)
- `ClockSkew = TimeSpan.Zero` — brak marginesu tolerancji
- Brak mechanizmu refresh token — po wygaśnięciu konieczne ponowne logowanie
- Token przechowywany w `localStorage` (nie `sessionStorage`, nie HttpOnly cookie)

## Powiązania z kodem

- Komponent modalu: `src/app/components/token-expired-dialog/token-expired-dialog.component.ts`
- Szablon HTML: `src/app/components/token-expired-dialog/token-expired-dialog.component.html`
- Wywołujący: `src/app/interceptors/jwt.interceptor.ts`

## Wątpliwości i braki

- TED-01: 10-minutowy token JWT to bardzo krótki czas dla aplikacji biznesowej — każda przerwa w pracy (spotkanie, rozmowa telefoniczna) skutkuje wygaśnięciem sesji i koniecznością ponownego logowania.
- TED-02: Token przechowywany w `localStorage` — podatny na atak XSS; bezpieczniejszą alternatywą jest HttpOnly cookie.
- TED-03: Brak mechanizmu refresh token — każde wygaśnięcie wymaga pełnego ponownego logowania.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `_wspolne/token-expired-dialog.md`. |
