# AppShell — Przegląd

---

## 1. Układ aplikacji

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]                                    │
│  [menu] InvoiceJet                                      [Profil/Login]   │
├──────────────────┬───────────────────────────────────────────────────────┤
│ [Menu boczne]    │ [Obszar roboczy — router-outlet]                      │
│                  │                                                       │
│ Search... [x]    │  Ekran ładowany na podstawie aktywnej trasy           │
│                  │                                                       │
│ Dashboard        │  Przykłady: Dashboard, Clients, Products, Invoices    │
│ Documents        │                                                       │
│  - Invoices      │                                                       │
│  - Proformas     │                                                       │
│  - Stornos       │                                                       │
│ Inventory        │                                                       │
│  - Clients       │                                                       │
│  - Products      │                                                       │
│ Settings         │                                                       │
│  - Firm Details  │                                                       │
│  - Bank Accounts │                                                       │
│  - Doc. Series   │                                                       │
└──────────────────┴───────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

`AppComponent` renderuje pasek nawigacyjny na górze aplikacji. Dla ekranów innych niż `/login` i `/register` renderuje także menu boczne oraz obszar `.pages` z `router-outlet`.

`router-outlet` ładuje komponent ekranu zgodny z aktywną trasą Angular Router. Przykładami są `DashboardComponent`, `ProductsComponent`, `InvoicesComponent` i ekrany ustawień.

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek nawigacyjny | `NavbarComponent` | Wyświetla tytuł `InvoiceJet`, przycisk menu, linki publiczne lub menu profilu. |
| Menu boczne | `SidebarComponent` | Wyświetla wyszukiwarkę i drzewo pozycji nawigacyjnych. |
| Obszar roboczy | `router-outlet` | Renderuje aktywny ekran aplikacji. |
| Menu profilu | `mat-menu` | Wyświetla imię, nazwisko, email, przełącznik trybu ciemnego i operację `Logout`. |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk menu | `button mat-icon-button` | Wywołuje `toggleSidebar()` w `NavbarComponent`. |
| Link Login | `button mat-button` | Nawiguje do `/login`. |
| Link Register | `button mat-button` | Nawiguje do `/register`. |
| Przycisk profilu | `button mat-button` | Otwiera `mat-menu` użytkownika. |
| Toggle Dark Mode | `button mat-menu-item` | Przełącza klasę `dark-mode` na elemencie `body`. |
| Logout | `button mat-menu-item` | Wywołuje `AuthService.logout()` i przechodzi do `/login`. |
| Pole Search w menu bocznym | `input matInput` | Filtruje drzewo pozycji menu. |
| Przycisk Clear w menu bocznym | `button mat-icon-button` | Czyści filtr menu bocznego. |

---

## 3. Nawigacja główna

| Grupa | Pozycja | Trasa | Komponent |
|---|---|---|---|
| N/D | Dashboard | `/dashboard` | `DashboardComponent` |
| Documents | Invoices | `/dashboard/invoices` | `InvoicesComponent` |
| Documents | Invoice Proformas | `/dashboard/invoice-proformas` | `InvoiceProformasComponent` |
| Documents | Invoice Stornos | `/dashboard/invoice-stornos` | `InvoiceStornosComponent` |
| Inventory | Clients | `/dashboard/clients` | `ClientsComponent` |
| Inventory | Products | `/dashboard/products` | `ProductsComponent` |
| Settings | Firm Details | `/dashboard/firm-details` | `FirmDetailsComponent` |
| Settings | Bank Accounts | `/dashboard/bank-accounts` | `BankAccountsComponent` |
| Settings | Document Series | `/dashboard/document-series` | `DocumentSeriesComponent` |

---

## 4. Scenariusz główny

1. Użytkownik wchodzi na trasę chronioną, na przykład `/dashboard/products`.
2. `AuthGuard` sprawdza `AuthService.isLoggedIn()`.
3. Po pozytywnej weryfikacji `AppComponent` ustawia `isLoginOrRegister = true`.
4. Szablon `app.component.html` renderuje `NavbarComponent`, `SidebarComponent` i `router-outlet`.
5. `router-outlet` renderuje komponent przypisany do trasy.
6. `SidebarComponent` zaznacza aktywną pozycję menu przez `isActiveRoute(node.route)`.

---

## 5. Stany obszaru

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Ekran publiczny | Widoczny jest pasek nawigacyjny z linkami `Login` i `Register`. Menu boczne nie jest renderowane. | Trasa zawiera `login` albo `register`. |
| Ekran chroniony | Widoczny jest pasek nawigacyjny, menu boczne i obszar roboczy. | Trasa nie zawiera `login` ani `register`. |
| Menu boczne otwarte | `SidebarService.sidebarVisible` emituje `true`. | Start na szerokim ekranie lub kliknięcie przycisku menu. |
| Menu boczne zamknięte | `SidebarService.sidebarVisible` emituje `false`. | Kliknięcie przycisku menu albo wybór pozycji na ekranie poniżej `1500px`. |
| Filtrowanie menu | `dataSource.data` zawiera tylko pasujące węzły drzewa. | Zdarzenie `(keyup)` w polu Search. |
| Tryb ciemny | Element `body` posiada klasę `dark-mode`. | Kliknięcie `Toggle Dark Mode`. |

---

## 6. Dostęp i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | `AuthGuard` dopuszcza trasę chronioną. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}`. |
| Odpowiedź HTTP ma status `401` | `AuthInterceptor` przekierowuje do `/login` i wywołuje `AuthService.logout()`. |

---

## 7. Notatki techniczne

- `AppComponent.isLoginOrRegister` ma wartość `true` dla tras innych niż `/login` i `/register`. [UWAGA: nazwa zmiennej sugeruje odwrotne znaczenie niż faktyczna wartość]
- `SidebarService` ustala początkową widoczność menu na podstawie `window.innerWidth > 1500`.
- `SidebarComponent.sidebarMode` ma stałą wartość `side`.
- `SidebarComponent.closeSidebar()` zwija menu boczne po wyborze pozycji tylko gdy `window.innerWidth < 1500`.
- `SidebarComponent.clearSearch()` czyści filtr i rozwija wszystkie węzły drzewa.

---

## Następne sekcje

- Szczegółowe dane o elementach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
