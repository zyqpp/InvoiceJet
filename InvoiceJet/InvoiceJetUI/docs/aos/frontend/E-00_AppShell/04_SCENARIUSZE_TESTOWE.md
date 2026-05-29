# AppShell — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Render ekranu chronionego w makiecie

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran chroniony jest renderowany z paskiem nawigacyjnym i menu bocznym.  
**Warunek wstępny:** Użytkownik jest zalogowany. Token JWT jest dostępny w `localStorage`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Dashboard. | URL `/dashboard` | N/D | Widoczny jest pasek nawigacyjny `InvoiceJet`. |
| 2 | Sprawdź menu boczne. | `app-sidebar` | N/D | Widoczne jest pole `Search...` i drzewo menu. |
| 3 | Sprawdź obszar roboczy. | `router-outlet` / `.pages` | N/D | Widoczny jest ekran `Dashboard`. |

---

## 2. Scenariusz: Ekran publiczny bez menu bocznego

**Typ:** Functional  
**Cel:** Weryfikacja, że Login i Register nie pokazują menu bocznego.  
**Warunek wstępny:** Użytkownik może być niezalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Login. | URL `/login` | N/D | Widoczny jest formularz Login. |
| 2 | Sprawdź menu boczne. | `app-sidebar` | N/D | Menu boczne nie jest renderowane. |
| 3 | Sprawdź linki publiczne. | `mat-toolbar button` | N/D | Widoczne są przyciski `Login` i `Register`. |

---

## 3. Scenariusz: Przełączenie menu bocznego

**Typ:** Functional  
**Cel:** Weryfikacja działania `SidebarService.toggleSidebar()`.  
**Warunek wstępny:** Użytkownik jest zalogowany i znajduje się na trasie chronionej.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij ikonę menu w pasku nawigacyjnym. | `mat-toolbar button mat-icon` | N/D | Widoczność `mat-sidenav` zmienia stan. |
| 2 | Kliknij ikonę menu ponownie. | `mat-toolbar button mat-icon` | N/D | Widoczność `mat-sidenav` wraca do poprzedniego stanu. |

---

## 4. Scenariusz: Filtrowanie menu bocznego

**Typ:** Functional  
**Cel:** Weryfikacja filtrowania drzewa menu.  
**Warunek wstępny:** Menu boczne jest widoczne.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search w menu bocznym. | `app-sidebar input[placeholder="Search..."]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtra. | `app-sidebar input[placeholder="Search..."]` | `Products` | Drzewo menu pokazuje pozycję `Products` i jej grupę nadrzędną. |
| 3 | Sprawdź przycisk Clear. | `app-sidebar button mat-icon` | N/D | Widoczna jest ikona `close`. |
| 4 | Kliknij przycisk Clear. | `app-sidebar button mat-icon` | N/D | Pole Search jest puste. Drzewo menu wraca do pełnej listy. |

---

## 5. Scenariusz: Aktywna pozycja menu

**Typ:** Functional  
**Cel:** Weryfikacja klasy `active-link`.  
**Warunek wstępny:** Użytkownik jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Products. | URL `/dashboard/products` | N/D | `router-outlet` renderuje `ProductsComponent`. |
| 2 | Sprawdź pozycję menu. | `mat-tree-node.active-link` | N/D | Aktywna jest pozycja `Products`. |

---

## 6. Scenariusz: Wylogowanie

**Typ:** Access Control  
**Cel:** Weryfikacja usunięcia tokenu i przekierowania.  
**Warunek wstępny:** Użytkownik jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz menu profilu. | `.profileButton` | N/D | Widoczne jest menu użytkownika. |
| 2 | Kliknij `Logout`. | `button[mat-menu-item]` | N/D | Wywołana jest metoda `logout()`. |
| 3 | Sprawdź token. | `localStorage.authToken` | N/D | Token `authToken` jest usunięty. |
| 4 | Sprawdź trasę. | URL przeglądarki | N/D | Aplikacja przechodzi do `/login`. |

---

## 7. Scenariusz: Przełączenie trybu ciemnego

**Typ:** Functional  
**Cel:** Weryfikacja klasy `dark-mode`.  
**Warunek wstępny:** Użytkownik jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz menu profilu. | `.profileButton` | N/D | Widoczne jest menu użytkownika. |
| 2 | Kliknij `Toggle Dark Mode`. | `button[mat-menu-item]` | N/D | Element `body` otrzymuje albo traci klasę `dark-mode`. |

---

## 8. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Token `authToken` nie istnieje albo jest nieważny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Products. | URL `/dashboard/products` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przechodzi do `/login`. |

---

## 9. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Pasek nawigacyjny | `app-navbar`, `mat-toolbar` |
| Przycisk menu | `mat-toolbar button[mat-icon-button]` |
| Menu boczne | `app-sidebar`, `mat-sidenav` |
| Pole Search menu bocznego | `app-sidebar input[placeholder="Search..."]` |
| Drzewo menu | `mat-tree` |
| Węzeł menu | `mat-tree-node` |
| Aktywny węzeł menu | `mat-tree-node.active-link` |
| Obszar roboczy | `.pages` |
| Menu profilu | `mat-menu` |
| Przycisk profilu | `.profileButton` |
