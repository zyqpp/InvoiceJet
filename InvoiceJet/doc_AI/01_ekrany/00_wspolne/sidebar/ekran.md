# SidebarComponent — Boczne menu nawigacyjne

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Sidebar |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Lewe menu nawigacyjne aplikacji wyświetlane po zalogowaniu. Komponent wbudowany w `DashboardLayoutComponent` — widoczny na wszystkich ekranach chronionych przez `AuthGuard`. Zawiera linki do wszystkich sekcji dashboardu. Używa `routerLink` i `routerLinkActive` Angular do podświetlania aktywnej trasy.

## Wizualizacja układu

```
┌──────────────────┐
│ Dashboard        │  ← ikona: dashboard
├──────────────────┤
│ Dane firmy       │  ← ikona: business
├──────────────────┤
│ Klienci          │  ← ikona: people
├──────────────────┤
│ Konta bankowe    │  ← ikona: account_balance
├──────────────────┤
│ Produkty         │  ← ikona: inventory
├──────────────────┤
│ Serie dokumentów │  ← ikona: format_list_numbered
├──────────────────┤
│ Faktury          │  ← ikona: receipt
├──────────────────┤
│ Proformy         │  ← ikona: receipt_long
├──────────────────┤
│ Storna           │  ← ikona: undo
└──────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | Brak — komponent layout (renderowany na każdej trasie `/dashboard/*`) |
| Wymagana rola/uprawnienie | User (przez `DashboardLayoutComponent` → `AuthGuard`) |
| Punkty wejścia | Automatycznie ładowany przez `DashboardLayoutComponent` |
| Powiązany kod komponentu | `src/app/components/sidebar/sidebar.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| `/dashboard` | Klik „Dashboard" | Zawsze | User |
| `/dashboard/firm-details` | Klik „Dane firmy" | Zawsze | User |
| `/dashboard/clients` | Klik „Klienci" | Zawsze | User |
| `/dashboard/bank-accounts` | Klik „Konta bankowe" | Zawsze | User |
| `/dashboard/products` | Klik „Produkty" | Zawsze | User |
| `/dashboard/document-series` | Klik „Serie dokumentów" | Zawsze | User |
| `/dashboard/invoices` | Klik „Faktury" | Zawsze | User |
| `/dashboard/invoice-proformas` | Klik „Proformy" | Zawsze | User |
| `/dashboard/invoice-stornos` | Klik „Storna" | Zawsze | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

Brak.

### Pola

Brak.

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Sidebar-Dashboard | Dashboard | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-DaneFirmy | Dane firmy | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-Klienci | Klienci | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-KontaBankowe | Konta bankowe | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-Produkty | Produkty | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-SerieDokumentow | Serie dokumentów | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-Faktury | Faktury | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-Proformy | Proformy | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |
| OP-Sidebar-Storna | Storna | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) |

### Modale

Brak.

### Powiadomienia

Brak.

## Pozycje menu — szczegóły

| Pozycja | Trasa | Ikona Material |
|---|---|---|
| Dashboard | `/dashboard` | `dashboard` |
| Dane firmy | `/dashboard/firm-details` | `business` |
| Klienci | `/dashboard/clients` | `people` |
| Konta bankowe | `/dashboard/bank-accounts` | `account_balance` |
| Produkty | `/dashboard/products` | `inventory` |
| Serie dokumentów | `/dashboard/document-series` | `format_list_numbered` |
| Faktury | `/dashboard/invoices` | `receipt` |
| Proformy | `/dashboard/invoice-proformas` | `receipt_long` |
| Storna | `/dashboard/invoice-stornos` | `undo` |

## Zachowanie

- Aktywna trasa podświetlona przez `routerLinkActive="active"`
- Menu zawsze widoczne (brak hamburger menu / collapse na mobile)
- Sidebar stały — nie reaguje na szerokość ekranu

## Powiązania

- Powiązane procesy: Brak bezpośrednich
- Powiązane API: Brak bezpośrednich wywołań API
- Powiązane UC: Brak

### Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| Wszystkie pozycje menu (OP-Sidebar-*) | [ALG-IZO Izolacja danych UserFirm](../../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Sidebar nawiguje do sekcji chronionych przez AuthGuard — każda sekcja docelowa prezentuje dane filtrowane per UserFirm zalogowanego użytkownika; sam sidebar nie wywołuje API, ale jest bramą do ekranów stosujących izolację danych |

## Powiązania z kodem

- Komponent: `src/app/components/sidebar/sidebar.component.ts`
- Szablon HTML: `src/app/components/sidebar/sidebar.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- SB-01: Brak responsywności — sidebar zawsze widoczny niezależnie od szerokości ekranu; na urządzeniach mobilnych może zasłaniać treść główną.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `_wspolne/sidebar.md`. |
