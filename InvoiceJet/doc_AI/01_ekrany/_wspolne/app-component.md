# Komponent: App Root (AppComponent)

| Atrybut | Wartość |
|---|---|
| ID | LAYOUT-01 |
| Komponent | `AppComponent` |
| Plik | `src/app/app.component.ts` |
| Selektor | `app-root` |
| AuthGuard | NIE |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Główny komponent aplikacji Angular. Zawiera `<router-outlet>` jako punkt wyjścia routera. Nie posiada własnej logiki biznesowej — służy wyłącznie jako kontener routingu.

## Template

```html
<router-outlet></router-outlet>
```

## Struktura routingu

Router renderuje w `<router-outlet>`:
- `/login` → `LoginComponent`
- `/register` → `RegisterComponent`
- `/dashboard` → `DashboardLayoutComponent` (z `NavbarComponent` + `SidebarComponent` + zagnieżdżony `<router-outlet>`)

## Moduł

- `AppModule` z `app.module.ts`
- Router konfiguracja w `app-routing.module.ts`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
