# A-00: AppShell — Metadane

## Informacje podstawowe

| Właściwość | Wartość |
|---|---|
| **ID przepływu** | A-00 |
| **Nazwa** | AppShell |
| **Cel biznesowy** | Powłoka aplikacji definiująca strukturę interfejsu (navbar, sidebar, routing), zarządzanie logowaniem, nawigacją i wylogowaniem |
| **Sekcja menu** | Globalna (00_GLOBAL) — wszystkie ekrany chronione |
| **Typ dokumentu** | Przepływ aplikacyjny (Application Flow) |
| **Wersja dokumentu** | 1.0 |
| **Data ostatniej aktualizacji** | 2026-05-29 |
| **Status** | Stworzony |

## Powiązania techniczne

### Komponenty frontend
| Komponenta | Plik | Cel |
|---|---|---|
| `AppComponent` | `app.component.ts` | Główny komponent renderujący makietę powłoki (navbar, sidebar, router-outlet) |
| `NavbarComponent` | `navbar.component.ts` | Pasek nawigacyjny z logowaniem/rejestracją i menu profilu |
| `SidebarComponent` | `sidebar.component.ts` | Menu boczne z drzewem nawigacji i filtrowaniem |

### Serwisy frontend
| Serwis | Cel |
|---|---|
| `AuthService` | Zarządzanie stanem logowania, dekodowanie tokenu JWT, dane użytkownika |
| `SidebarService` | Kontrola widoczności menu bocznego (toggle, stan) |
| `Router` (Angular) | Zarządzanie routingiem, nawigacja między ekranami |

### Guardy
| Guard | Cel |
|---|---|
| `AuthGuard` | Blokowanie dostępu do tras chronionych bez tokenu, redirekcja na `/login` |

### Interceptory
| Interceptor | Cel |
|---|---|
| `AuthInterceptor` | Dodawanie tokenu JWT do nagłówków HTTP, obsługa błędu 401 (token wygasł) |
| `ErrorInterceptor` | Wyświetlanie błędów HTTP (400, 401, 404, 500) przez ToastrService |

## Elementy danych

### Encje (backend)
N/D — AppShell nie ma dedykowanego backendu, operuje na UI i serwisach frontend

### DTO (frontend → backend)
N/D — AppShell nie komunikuje się z API

### Tabele bazy danych
N/D — AppShell nie mapuje do tabel bazy

## Trasy i ekrany
| Trasa | Typ | Ekran | Guard | Sidebar |
|---|---|---|---|---|
| `/login` | Publiczna | Login | — | Ukryty |
| `/register` | Publiczna | Register | — | Ukryty |
| `/dashboard/*` | Chroniona | Dashboard + poddokumenty | AuthGuard | Widoczny |
| Inne trasy `/...` | Chronione | Ekrany aplikacyjne | AuthGuard | Widoczny |

## Powiązane dokumenty

| # | Dokument | Cel |
|---|---|---|
| 01 | [01_PRZEGLAD_END_TO_END.md](01_PRZEGLAD_END_TO_END.md) | Widok całego przepływu od UI do bazy (diagram, warunki, wyniki) |
| 02 | [02_MAPA_POL_UI_DO_DANYCH.md](02_MAPA_POL_UI_DO_DANYCH.md) | Mapowanie elementów UI, danych, bindingów |
| 03 | [03_OPERACJE_I_PRZYCISKI.md](03_OPERACJE_I_PRZYCISKI.md) | Opis każdej operacji (toggle menu, logout, filtrowanie, nawigacja) |
| 04 | [04_GRIDY_LISTY_ZAPYTANIA.md](04_GRIDY_LISTY_ZAPYTANIA.md) | Źródła danych tabelarycznych (nie dotyczy AppShell) |
| 05 | [05_WALIDACJE_BLEDY_BEZPIECZENSTWO.md](05_WALIDACJE_BLEDY_BEZPIECZENSTWO.md) | Guardy, interceptory, bezpieczeństwo dostępu |
| 06 | [06_SCENARIUSZE_TESTOWE_E2E.md](06_SCENARIUSZE_TESTOWE_E2E.md) | Plany testów (scenariusze Happy Path i negatywne) |
| 07 | [07_SLEDZENIE_ZRODEL.md](07_SLEDZENIE_ZRODEL.md) | Śledzenie źródeł (linki do E-00, brak P-XX) |
| H | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) | Historia wersji dokumentu |

## Reguły markerów

| Sytuacja | Marker | Przykład |
|---|---|---|
| Informacja nie potwierdzona w dostępnych dokumentach | `[WYMAGA WERYFIKACJI]` | `Nazwa: [WYMAGA WERYFIKACJI]` |
| Element UI bez potwierdzenia w kodzie/dokumentacji | `[BRAK POTWIERDZENIA W DOKUMENTACJI]` | `Pole: [BRAK POTWIERDZENIA W DOKUMENTACJI]` |
| Ślad UI→DB urywnie się | `[BRAK MAPOWANIA DO BAZY]` | `Baza danych: [BRAK MAPOWANIA DO BAZY]` |
| Brak danych | `N/D` | `DTO: N/D` |
| Operacja bez backendu | `[TYLKO FRONTEND]` | `Endpoint: [TYLKO FRONTEND]` |

## Źródła dokumentacji

- **Frontend AOS:** [`InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/`](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/)
  - E-00 zawiera 5 dokumentów: Metadane, Przegląd, Dane i operacje, Logika biznesowa, Scenariusze testowe
- **Backend AOS:** N/D — brak dedykowanego procesu backend dla AppShell
- **Szablony:** [`docs/aos/application/templates/TEMPLATE_*.md`](../../templates/)
