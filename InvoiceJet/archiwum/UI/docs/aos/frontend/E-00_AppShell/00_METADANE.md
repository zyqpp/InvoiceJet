# AppShell — Metadane

**Dokument:** Metadane wspólnej makiety aplikacji  
**Aplikacja:** InvoiceJet  
**Moduł:** Core UI  
**Klasyfikacja:** Wspólny układ aplikacji  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane obszaru

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa obszaru** | AppShell |
| **Zakres URL** | Ekrany publiczne `/login`, `/register`; ekrany chronione pod `/dashboard` |
| **Guard dostępu** | `AuthGuard` dla tras chronionych |
| **Lazy loading** | Nie |
| **Komponent główny** | `src/app/app.component.ts` |
| **Szablon główny** | `src/app/app.component.html` |
| **Komponent paska nawigacyjnego** | `src/app/components/navbar/navbar.component.ts` |
| **Szablon paska nawigacyjnego** | `src/app/components/navbar/navbar.component.html` |
| **Komponent menu bocznego** | `src/app/components/sidebar/sidebar.component.ts` |
| **Szablon menu bocznego** | `src/app/components/sidebar/sidebar.component.html` |
| **Routing** | `src/app/app-routing.module.ts` |
| **Serwis menu bocznego** | `src/app/services/sidebar.service.ts` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

`AppShell` definiuje wspólny układ aplikacji InvoiceJet. Układ zawiera pasek nawigacyjny, menu boczne, wyszukiwarkę pozycji menu i obszar roboczy ładowany przez `router-outlet`.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd obszaru | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Dane i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika frontendowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne komponenty

- `AppComponent` — renderuje `NavbarComponent`, `SidebarComponent` i `router-outlet`.
- `NavbarComponent` — pokazuje tytuł aplikacji, przełącznik menu bocznego, linki logowania i menu profilu.
- `SidebarComponent` — pokazuje drzewo nawigacji i filtruje pozycje menu.

### Główne serwisy

- `AuthService` — udostępnia stan zalogowania, dane użytkownika i wylogowanie.
- `SidebarService` — przechowuje stan widoczności menu bocznego.
- `Router` — steruje aktywną trasą i ładowaniem ekranów do `router-outlet`.

### Guardy i interceptory

- `AuthGuard` — blokuje trasy chronione bez aktywnego tokenu.
- `AuthInterceptor` — dodaje token JWT do żądań HTTP i obsługuje status `401`.
- `ErrorInterceptor` — pokazuje komunikaty błędów HTTP przez `ToastrService`.

---

## Notatki

- Dokument opisuje wyłącznie zachowanie warstwy frontendowej.
- Dokument nie opisuje implementacji backendu ani reguł bazy danych.
- Screen w tym katalogu pokazuje przykładowy ekran chroniony załadowany we wspólnej makiecie aplikacji.
