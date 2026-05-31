# Komponent: Boczne menu (SidebarComponent)

| Atrybut | Wartość |
|---|---|
| ID | LAYOUT-03 |
| Komponent | `SidebarComponent` |
| Plik | `src/app/components/sidebar/sidebar.component.ts` |
| Używany w | `DashboardLayoutComponent` |
| AuthGuard | TAK (przez layout) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lewe menu nawigacyjne aplikacji wyświetlane po zalogowaniu. Zawiera linki do wszystkich sekcji dashboardu. Używa `routerLink` i `routerLinkActive` Angular.

## Pozycje menu

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

## Anomalie

| # | Anomalia |
|---|---|
| SB-01 | Brak responsywności — sidebar zawsze widoczny niezależnie od szerokości ekranu; na mobile może zasłaniać treść |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
