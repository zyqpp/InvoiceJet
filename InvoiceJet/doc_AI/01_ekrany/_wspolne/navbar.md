# Komponent: Pasek nawigacji (NavbarComponent)

| Atrybut | Wartość |
|---|---|
| ID | LAYOUT-02 |
| Komponent | `NavbarComponent` |
| Plik | `src/app/components/navbar/navbar.component.ts` |
| Używany w | `DashboardLayoutComponent` |
| AuthGuard | TAK (przez layout) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Górna belka aplikacji wyświetlana po zalogowaniu. Zawiera:
- Logo / nazwa aplikacji
- Imię i nazwisko zalogowanego użytkownika (z JWT claims)
- Przycisk wylogowania

## State komponentu

| Pole | Typ | Źródło | Opis |
|---|---|---|---|
| `userName` | `string` | JWT claim `firstName` + `lastName` | Wyświetlana nazwa użytkownika |

## Wylogowanie

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

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
