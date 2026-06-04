# A-00: AppShell — Scenariusze Testowe E2E

## Scenariusz 1: Happy Path — Render ekranu chronionego z pełną powłoką (navbar + sidebar)

**Cel:** Weryfikacja, że zalogowany użytkownik widzi navbar, sidebar i zawartość ekranu.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Browser wchodzi na `/dashboard` | AuthService.isLoggedIn() === true (token w localStorage) | — | — | — | — |
| 2 | AuthGuard.canActivate() sprawdza token | Guard zwraca true | — | — | — | AppComponent renderuje |
| 3 | AppComponent nasłuchuje NavigationEnd | Router event fire: type === NavigationEnd | — | — | — | — |
| 4 | Sprawdzenie czy route zawiera `/login` lub `/register` | route.url !== `/login` && !== `/register` → isLoginOrRegister = false | — | — | — | — |
| 5 | Renderowanie powłoki | `<app-navbar>`, `<app-sidebar>`, `<router-outlet>` widoczne | — | — | — | Navbar, Sidebar i zawartość widoczne |
| 6 | Navbar wyświetla menu profilu | NavbarComponent.userInfo.fullName interpr | — | — | — | Imię i email w menu profilu |
| 7 | Sidebar wyświetla drzewo menu | SidebarComponent.dataSource zawiera pozycje | — | — | — | 3 grupy + 9 pozycji widoczne |
| ✓ | **Test zdany** | Wszystkie elementy powłoki renderowane | — | — | — | Ekran chroniony w pełni widoczny |

**Kod kroki:**
- `cy.visit('/dashboard')`
- `cy.get('app-navbar').should('be.visible')`
- `cy.get('app-sidebar').should('be.visible')`
- `cy.get('.pages router-outlet').should('exist')`
- `cy.get('button[matMenuTriggerFor]').should('be.visible')` (profil)

---

## Scenariusz 2: Render ekranu publicznego bez menu bocznego (Login/Register)

**Cel:** Weryfikacja, że na ekranach publicznych sidebar jest ukryty.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Browser wchodzi na `/login` | — | — | — | — | — |
| 2 | AppComponent.router.events nasłuchuje | Router event: NavigationEnd, route.url = `/login` | — | — | — | — |
| 3 | Sprawdzenie warunku: route zawiera `/login`? | route.url.includes('/login') === true | — | — | — | — |
| 4 | isLoginOrRegister = true (zmienna sprawdzająca) | Warunek: `*ngIf="!isLoginOrRegister"` na navbar/sidebar | — | — | — | — |
| 5 | Navbar i Sidebar schowane | `<app-navbar>` i `<app-sidebar>` z `*ngIf="!isLoginOrRegister"` | — | — | — | Navbar i Sidebar nie renderowane |
| 6 | Tylko LoginComponent renderowany | `<router-outlet>` zawiera LoginComponent | — | — | — | Ekran logowania widoczny bez menu |
| ✓ | **Test zdany** | Navbar i Sidebar nie istnieją w DOM | — | — | — | Ekran publiczny bez menu |

**Kod kroki:**
- `cy.visit('/login')`
- `cy.get('app-navbar').should('not.exist')`
- `cy.get('app-sidebar').should('not.exist')`
- `cy.get('app-login').should('be.visible')`

---

## Scenariusz 3: Toggle Sidebar — Pokazanie i ukrycie menu bocznego

**Cel:** Weryfikacja działania przycisku menu (hamburger) w navbar.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Zalogowany użytkownik na `/dashboard` | — | — | — | — | Sidebar widoczny (stan domyślny) |
| 2 | Klik przycisk menu (hamburger) w navbar | NavbarComponent.toggleSidebar() wyzwany | [TYLKO FRONTEND] | — | — | — |
| 3 | SidebarService.toggleSidebar() zmienia BehaviorSubject | `sidebarVisible.next(!sidebarVisible.value)` | — | — | — | — |
| 4 | SidebarComponent nasłuchuje sidebarVisible | Subskrypcja emituje nową wartość | — | — | — | — |
| 5 | Klasa `mat-sidenav.opened` dodana/usunięta | `[opened]="sidebarVisible$ | async"` | — | — | — | Sidebar schowa się (animacja) |
| 6 | Klik przycisk menu ponownie | Toggle state — SidebarService.toggleSidebar() | — | — | — | — |
| 7 | Sidebar otwarty ponownie | `mat-sidenav.opened` = true | — | — | — | Sidebar pokaże się |
| ✓ | **Test zdany** | Toggle działa bidirektunalnie | — | — | — | Sidebar can toggle on/off |

**Kod kroki:**
- `cy.get('app-navbar button[mat-icon-button]').first().click()` (menu toggle)
- `cy.get('mat-sidenav').should('not.have.class', 'mat-drawer-opened')` (na mobilnych)
- `cy.get('app-navbar button[mat-icon-button]').first().click()`
- `cy.get('mat-sidenav').should('have.class', 'mat-drawer-opened')`

---

## Scenariusz 4: Filtrowanie menu bocznego (Search)

**Cel:** Weryfikacja działania wyszukiwania w menu nawigacji.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Zalogowany użytkownik z widocznym Sidebar | Wszystkie pozycje menu widoczne (3 grupy + 9 items) | [TYLKO FRONTEND] | — | — | Pełne drzewo menu |
| 2 | Klik w pole Search i wpisanie "invoice" | Input value: "invoice", trigger (keyup) | — | — | — | — |
| 3 | SidebarComponent.filterTree("invoice") wyzwany | Funkcja przycina węzły, które NIE zawierają "invoice" (case-insensitive) | — | — | — | — |
| 4 | Reguła: zachowaj węzeł jeśli: (a) nazwa zawiera tekst LUB (b) dziecko pasuje | filterNodes() rekursywnie sprawdza | — | — | — | — |
| 5 | Rezultat: tylko "Documents" grupa widoczna (zawiera "Invoices", "Invoice Proformas") | Węzły zawierające "invoice" zaznaczone | — | — | — | Menu odfiltrowane (tylko Invoices-related) |
| 6 | NestedTreeControl.expandAll() wyzwany (expand wszystkie pasujące) | Wszystkie węzły zawierające wynik rozszerzone | — | — | — | — |
| 7 | Przycisk "Clear" pojawia się (bo searchQuery !== "") | `<button *ngIf="searchQuery.length > 0">` | — | — | — | Clear button widoczny |
| 8 | Klik "Clear" button | searchQuery = "", filterTree("") wyzwany | — | — | — | — |
| 9 | NestedTreeControl.collapseAll() wyzwany | Wszystkie węzły zwinięte | — | — | — | Menu wróciło do stanu domyślnego |
| ✓ | **Test zdany** | Filtrowanie działa w obu kierunkach | — | — | — | Szukanie i czyszczenie działa |

**Kod kroki:**
- `cy.get('app-sidebar input[placeholder="Search..."]').type('invoice')`
- `cy.get('mat-tree-node').then(nodes => { expect(nodes.length).to.be.lessThan(12) })` (mniej pozycji)
- `cy.get('button:contains("Clear")').should('be.visible').click()`
- `cy.get('mat-tree-node').then(nodes => { expect(nodes.length).to.equal(12) })` (wróciło 12)

---

## Scenariusz 5: Aktywny element menu — klasa `active-link` na bieżącej trasie

**Cel:** Weryfikacja, że bieżąca trasa jest zaznaczona w menu.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Zalogowany użytkownik na `/documents/invoices` | Router.url = `/documents/invoices` | — | — | — | — |
| 2 | SidebarComponent sprawdza każdy węzeł: czy jest aktywny? | `isActive(node.route)` używa `Router.isActive(node.route, false)` | — | — | — | — |
| 3 | Węzeł "Invoices" pasuje do bieżącej trasy | `node.route === '/documents/invoices'` | — | — | — | — |
| 4 | Klasa `active-link` dodana do węzła | `[ngClass]="{ 'active-link': isActive(node.route) }"` | — | — | — | "Invoices" ma klasę `active-link` (podświetlony) |
| 5 | Klik na inny węzeł: "Clients" (`/inventory/clients`) | Router.navigate(['/inventory/clients']) | — | — | — | — |
| 6 | AppComponent zmienia route, `NavigationEnd` fire | Nowa wartość Router.url | — | — | — | — |
| 7 | SidebarComponent zmienia `active-link` | Węzeł "Invoices" traci klasę, "Clients" ją otrzymuje | — | — | — | Podświetlenie przesunęło się na "Clients" |
| ✓ | **Test zdany** | Active-link śledzą bieżącą trasę | — | — | — | Nagórny menu zawsze pokazuje aktywną stronę |

**Kod kroki:**
- `cy.get('mat-tree-node.active-link').should('contain', 'Invoices')`
- `cy.get('mat-tree-node').contains('Clients').click()`
- `cy.get('mat-tree-node.active-link').should('contain', 'Clients')`

---

## Scenariusz 6: Logout — Usunięcie tokenu i redirect na /login

**Cel:** Weryfikacja działania przycisku wylogowania.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Zalogowany użytkownik ma token w localStorage | `localStorage.getItem('authToken')` !== null | — | — | — | Token istnieje |
| 2 | Klik przycisk profilu w navbar | `(click)="openProfile()"` | — | — | — | Menu profilu otwarty |
| 3 | Klik "Logout" w menu profilu | NavbarComponent.logout() wyzwany | — | — | — | — |
| 4 | AuthService.logout() wyzwany | localStorage.removeItem('authToken') | [TYLKO FRONTEND] | — | — | — |
| 5 | Token usunięty z localStorage | Weryfikacja: `localStorage.getItem('authToken')` === null | — | — | — | — |
| 6 | AuthService emituje logoutSubject event | `logoutSubject.next()` | — | — | — | — |
| 7 | Router.navigate(['/login']) wyzwany | Router zmienia trasę | — | — | — | — |
| 8 | AppComponent nasłuchuje NavigationEnd | NavigationEnd fire, route.url = `/login` | — | — | — | — |
| 9 | Navbar i Sidebar ukryte | `*ngIf="!isLoginOrRegister"` = false | — | — | — | — |
| 10 | LoginComponent renderowany | router-outlet zmienia zawartość | — | — | — | Ekran logowania bez menu |
| ✓ | **Test zdany** | Logout usuwa token i redirectuje | — | — | — | Użytkownik wylogowany i na /login |

**Kod kroki:**
- `cy.visit('/dashboard')`
- `cy.window().then(win => cy.wrap(localStorage.getItem('authToken')).should('not.be.null'))`
- `cy.get('button[matMenuTriggerFor]').click()` (profil)
- `cy.get('button:contains("Logout")').click()`
- `cy.url().should('include', '/login')`
- `cy.window().then(win => cy.wrap(localStorage.getItem('authToken')).should('be.null'))`

---

## Scenariusz 7: Toggle Dark Mode — Przełączenie trybu ciemnego

**Cel:** Weryfikacja działania toggle'a trybu ciemnego.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Zalogowany użytkownik, tryb jasny (domyślny) | Brak klasy `dark-mode` na `body` | [TYLKO FRONTEND] | — | — | Jasne kolory |
| 2 | Klik profil w navbar | Menu profilu otwarty | — | — | — | — |
| 3 | Klik toggle "Dark Mode" | NavbarComponent.toggleTheme() wyzwany | — | — | — | — |
| 4 | Funkcja toggleTheme sprawdza klasy | `document.body.classList.toggle('dark-mode')` | — | — | — | — |
| 5 | Klasa `dark-mode` dodana na `<body>` | Sprawdzenie: `document.body.classList.contains('dark-mode')` === true | — | — | — | — |
| 6 | CSS style zmienia kolory (tło, tekst itp.) | Reguły CSS z `.dark-mode` prefix stosowane | — | — | — | Ciemne kolory, białe tekst (widoczna zmiana) |
| 7 | Klik toggle ponownie | toggleTheme() wyzwany | — | — | — | — |
| 8 | Klasa `dark-mode` usunięta z `<body>` | `document.body.classList.contains('dark-mode')` === false | — | — | — | — |
| 9 | CSS style wróciło do jasnego (domyślne) | Brak klasy dark-mode | — | — | — | Jasne kolory wróciły |
| ⚠️ | **[WYMAGA WERYFIKACJI]** | Stan nie zapisywany w localStorage — po odświeżeniu wraca tryb jasny | — | — | — | Po F5: dark mode resetuje się do jasnego |

**Kod kroki:**
- `cy.get('button[matMenuTriggerFor]').click()`
- `cy.get('button:contains("Dark Mode")').click()`
- `cy.get('body').should('have.class', 'dark-mode')`
- `cy.reload()`
- `cy.get('body').should('not.have.class', 'dark-mode')` (dark mode resetuje się)

---

## Scenariusz 8: Access Control — Blokowanie dostępu bez tokenu (AuthGuard)

**Cel:** Weryfikacja, że niezalogowani użytkownicy nie mogą dostać się do tras chronionych.

| Krok | Akcja UI | Walidacja FE | Walidacja API | Walidacja Backend | Walidacja DB | Rezultat UI |
|---|---|---|---|---|---|---|
| 1 | Nowy браузер sesja (brak tokenu) | localStorage.getItem('authToken') === null | — | — | — | — |
| 2 | Browser wchodzi na `/dashboard` (chroniona trasa) | — | — | — | — | — |
| 3 | AppComponent renderuje, ale AuthGuard sprawdza | AuthGuard.canActivate() wyzwany | — | — | — | — |
| 4 | AuthService.isLoggedIn() zwraca false | Sprawdzenie: `localStorage.getItem('authToken')` === null | — | — | — | — |
| 5 | Guard zwraca false (dostęp ZABLOKOWANY) | `canActivate()` return false | — | — | — | — |
| 6 | Router.navigate(['/login']) wyzwany (wewnątrz guard) | Router zmienia trasę | — | — | — | — |
| 7 | Redirect na `/login` | Browser URL zmienia się na `/login` | — | — | — | — |
| 8 | LoginComponent renderowany | router-outlet zawiera LoginComponent | — | — | — | Ekran logowania widoczny, nie dashboard |
| ✓ | **Test zdany** | Guard blokuje dostęp bez tokenu | — | — | — | Niezalogowani nie mogą wejść |

**Kod kroki:**
- `cy.clearLocalStorage()`
- `cy.visit('/dashboard', { failOnStatusCode: false })`
- `cy.url().should('include', '/login')` (redirect)
- `cy.get('app-login').should('be.visible')`

---

## Podsumowanie scenariuszy

| # | Scenariusz | Typ | Status | Ważny dla |
|---|---|---|---|---|
| 1 | Render powłoki (navbar + sidebar) | Happy Path | ✓ | Weryfikacja struktury UI |
| 2 | Render bez menu (Login/Register) | Functional | ✓ | Weryfikacja warunkowości |
| 3 | Toggle Sidebar | Functional | ✓ | Weryfikacja SidebarService |
| 4 | Filtrowanie menu | Functional | ✓ | Weryfikacja filterTree() |
| 5 | Aktywny element | Functional | ✓ | Weryfikacja active-link |
| 6 | Logout | Functional | ✓ | Weryfikacja AuthService + redirect |
| 7 | Dark Mode | Functional | ⚠️ | Weryfikacja UI, brak utrwalenia |
| 8 | AuthGuard | Access Control | ✓ | Weryfikacja ochrony tras |

**Dane testowe:**
- Token JWT válido: przesyłać przez `localStorage.setItem('authToken', validToken)`
- Niezalogowany: usunąć token z localStorage (`clearLocalStorage()`)
