# NavbarComponent — Pasek nawigacji

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Navbar |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Górna belka aplikacji wyświetlana po zalogowaniu użytkownika. Komponent wbudowany w `DashboardLayoutComponent` — widoczny na wszystkich ekranach chronionych przez `AuthGuard`. Wyświetla imię i nazwisko zalogowanego użytkownika (pobrane z claims JWT) oraz przycisk wylogowania.

## Wizualizacja układu

```
┌─────────────────────────────────────────────────────────────┐
│  [Logo/Nazwa aplikacji]       Jan Kowalski  [Wyloguj] (ikona)│
└─────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | Brak — komponent layout (renderowany na każdej trasie `/dashboard/*`) |
| Wymagana rola/uprawnienie | User (przez `DashboardLayoutComponent` → `AuthGuard`) |
| Punkty wejścia | Automatycznie ładowany przez `DashboardLayoutComponent` |
| Powiązany kod komponentu | `src/app/components/navbar/navbar.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/login` | Klik przycisku „Wyloguj" | Zawsze | Brak (akcja publiczna) |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

Brak.

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-Navbar-userName | Imię i nazwisko użytkownika (wyświetlane) | — (tylko odczyt) | [ALG-JWT Weryfikacja tokenu JWT](../../../../03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md) |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Navbar-Wyloguj | Wyloguj (ikona / przycisk) | [ALG-JWT Weryfikacja tokenu JWT](../../../../03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md) |

### Modale

Brak.

### Powiadomienia

Brak.

## Stan komponentu

| Pole | Typ | Źródło | Opis |
|---|---|---|---|
| `userName` | `string` | JWT claim `firstName` + `lastName` | Wyświetlana nazwa użytkownika |

## Logika wylogowania

```typescript
logout() {
    localStorage.removeItem("authToken");
    this.router.navigate(["/login"]);
}
```

Brak wywołania API przy wylogowaniu — token usuwany tylko lokalnie. Server-side invalidation nie istnieje (JWT bezstanowy).

## Odczyt danych z JWT

Komponent odczytuje dane użytkownika przez `JwtHelperService` z `@auth0/angular-jwt`:

```typescript
const token = localStorage.getItem("authToken");
const decoded = this.jwtHelper.decodeToken(token);
this.userName = decoded.firstName + " " + decoded.lastName;
```

## Powiązania

- Powiązane procesy: `../../02_procesy/autentykacja/logowanie/proces.md`
- Powiązane API: Brak bezpośrednich wywołań API
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-Navbar-userName | [ALG-JWT Weryfikacja tokenu JWT](../../../../03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md) | Imię i nazwisko użytkownika odczytywane z claims tokenu JWT (firstName + lastName) przez JwtHelperService — token musi być ważny, aby dane były dostępne |
| OP-Navbar-Wyloguj | [ALG-JWT Weryfikacja tokenu JWT](../../../../03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md) | Wylogowanie usuwa token z localStorage; AuthInterceptor i TokenExpiredDialog powiązane z cyklem życia tokenu JWT (token bezstanowy — wygasa po 10 minutach od wystawienia) |

## Powiązania z kodem

- Komponent: `src/app/components/navbar/navbar.component.ts`
- Szablon HTML: `src/app/components/navbar/navbar.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- Brak server-side invalidation tokenu przy wylogowaniu — token wygasa dopiero po 10 minutach od wystawienia, nawet po lokalnym usunięciu.
- Brak `data-cy` / `data-testid` dla przycisku wylogowania.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `_wspolne/navbar.md`. |
