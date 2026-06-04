# A-00: AppShell — Mapa pól UI do danych

## A. Elementy Navbar (pasek nawigacyjny)

| Element UI | Typ | formControlName | Warstwa TS | Binding | Funkcja | Serwis | Endpoint | DTO | Backend | Encja | Tabela | Dowód |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Przycisk menu (toggle) | `button` | N/D | `NavbarComponent` | `(click)="toggleSidebar()"` | Pokazanie/ukrycie menu bocznego | `SidebarService.toggleSidebar()` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Logo "InvoiceJet" | `h1` | N/D | `NavbarComponent` | `Text: "InvoiceJet"` | Nazwa aplikacji | — | — | N/D | N/D | N/D | N/D | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Link "Login" | `button mat-button` | N/D | `NavbarComponent` | `[routerLink]="['/login']"` | Nawigacja na ekran logowania | `Router` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Link "Register" | `button mat-button` | N/D | `NavbarComponent` | `[routerLink]="['/register']"` | Nawigacja na ekran rejestracji | `Router` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Przycisk profilu (avatar) | `button mat-button` | N/D | `NavbarComponent` | `(click)="openProfile()"` → `[matMenuTriggerFor]="profileMenu"` | Otwarcie menu profilu | — | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Menu profilu — Imię i nazwisko | `mat-menu-item` | N/D | `NavbarComponent.userInfo.fullName` | Interpolacja: `{{ userInfo.fullName }}` | Wyświetlenie imienia z tokenu JWT | `AuthService.userInfo.fullName` | [TYLKO FRONTEND] | `UserInfo { fullName, email, initials }` | N/D | N/D | N/D | [E-00 03_LOGIKA_BIZNESOWA.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/03_LOGIKA_BIZNESOWA.md) |
| Menu profilu — Email | `mat-menu-item` | N/D | `NavbarComponent.userInfo.email` | Interpolacja: `{{ userInfo.email }}` | Wyświetlenie emailu z tokenu JWT | `AuthService.userInfo.email` | [TYLKO FRONTEND] | `UserInfo { fullName, email, initials }` | N/D | N/D | N/D | [E-00 03_LOGIKA_BIZNESOWA.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/03_LOGIKA_BIZNESOWA.md) |
| Menu profilu — Toggle Dark Mode | `mat-menu-item button` | N/D | `NavbarComponent` | `(click)="toggleTheme()"` | Przełączenie trybu ciemnego | `toggleTheme()` (lokalnie) | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Menu profilu — Logout | `mat-menu-item button` | N/D | `NavbarComponent` | `(click)="logout()"` | Wylogowanie użytkownika | `AuthService.logout()` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |

## B. Elementy Sidebar (menu boczne)

| Element UI | Typ | Binding | Warstwa TS | Funkcja | Serwis | Endpoint | DTO | Backend | Encja | Tabela | Dowód |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Pole Search (filtr menu) | `input[placeholder="Search..."]` | `[(ngModel)]="searchQuery"` → `(keyup)="filterTree()"` | `SidebarComponent` | Filtrowanie drzewa nawigacji po tekście | `filterTree()` w komponencie | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Przycisk Clear (czyszczenie filtra) | `button mat-button` | `(click)="clearFilter()"` | `SidebarComponent` | Wyczyszczenie filtra i zawinięcie menu | `clearFilter()` w komponencie | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Drzewo nawigacji (mat-tree) | `mat-tree` | `[dataSource]="dataSource"` | `SidebarComponent` | Wyświetlenie hierarchii menu: 3 główne grupy (Documents, Inventory, Settings) + 9 podpozycji | `MatTreeDataSource` + `NestedTreeControl` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Węzły menu (mat-tree-node) | `mat-tree-node` | `[routerLink]="[node.route]"` + `(click)="toggleNode(node)"` | `SidebarComponent` | Nawigacja do ekranu, toggle ekspandowania grupy | `Router` + `NestedTreeControl.toggle()` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Aktywna pozycja menu | `mat-tree-node.active-link` | `[ngClass]="{ 'active-link': isActive(node.route) }"` | `SidebarComponent` | Zaznaczenie aktywnego elementu menu | `Router.isActive()` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 02_DANE_I_OPERACJE.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/02_DANE_I_OPERACJE.md) |
| Auto-zamykanie menu (mobile) | N/D (logika) | `if (window.innerWidth < 1500) SidebarService.closeSidebar()` | `SidebarComponent` | Automatyczne zamknięcie menu po wyborze na urządzeniach mobilnych | `SidebarService.closeSidebar()` | [TYLKO FRONTEND] | N/D | N/D | N/D | N/D | [E-00 03_LOGIKA_BIZNESOWA.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/03_LOGIKA_BIZNESOWA.md) |

## C. Dane pomocnicze — Struktura Menu (dane statyczne)

| Grupa | Pozycja | Route | Typ | Źródło danych | Komponent docelowy | Dowód |
|---|---|---|---|---|---|---|
| Dashboard | Dashboard | `/dashboard` | Ekran | Statyczne | DashboardComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Documents | Invoices | `/documents/invoices` | Ekran | Statyczne | InvoicesComponent (lista) | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Documents | Invoice Proformas | `/documents/proformas` | Ekran | Statyczne | InvoiceProformasComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Documents | Invoice Stornos | `/documents/stornos` | Ekran | Statyczne | InvoiceStornosComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Inventory | Clients | `/inventory/clients` | Ekran | Statyczne | ClientsComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Inventory | Products | `/inventory/products` | Ekran | Statyczne | ProductsComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Settings | Firm Details | `/settings/firm-details` | Ekran | Statyczne | FirmDetailsComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Settings | Bank Accounts | `/settings/bank-accounts` | Ekran | Statyczne | BankAccountsComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |
| Settings | Document Series | `/settings/document-series` | Ekran | Statyczne | DocumentSeriesComponent | [E-00 01_PRZEGLĄD.md](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/01_PRZEGLĄD.md) |

## Uwagi

- **[TYLKO FRONTEND]**: Wszystkie operacje AppShell (toggle menu, logout, filtrowanie, nawigacja) są wykonywane bez API. Nie ma komunikacji z backendem dla samej powłoki.
- **[BRAK MAPOWANIA DO BAZY]**: AppShell nie mapuje do żadnych tabel bazy danych. Dane wyświetlane w navbar (imię, email) pochodzą z dekodowanego tokenu JWT, nie z bazy.
- **Tryb ciemny**: Stan nie jest utrwalany w `localStorage` — po odświeżeniu strony wraca do jasnego trybu. [WYMAGA WERYFIKACJI] czy to jest zamierzone.
- **Token JWT**: Dane użytkownika (fullName, email, initials) są dekodowane z tokenu bez weryfikacji na backendzie. Bezpieczeństwo zależy od poprawności tokenu wydanego przez serwer.
