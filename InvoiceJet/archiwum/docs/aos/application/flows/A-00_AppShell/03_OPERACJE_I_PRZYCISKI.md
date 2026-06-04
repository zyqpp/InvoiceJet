# A-00: AppShell — Operacje i Przyciski

## Tabela operacji głównych

| # | Operacja | Element UI | Handler | Serwis Frontend | Endpoint | Kontroler | Serwis Backend | Skutek DB | Reaction UI | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Toggle Sidebar | Przycisk menu (hamburger) w navbar | `NavbarComponent.toggleSidebar()` | `SidebarService.toggleSidebar()` | [TYLKO FRONTEND] | N/D | N/D | N/D | Sidebar schowa/pokaże się (toggle `BehaviorSubject`) | [TYLKO FRONTEND] |
| 2 | Logout | Przycisk "Logout" w menu profilu (navbar) | `NavbarComponent.logout()` | `AuthService.logout()` | [TYLKO FRONTEND] | N/D | N/D | N/D | localStorage.removeItem('authToken') + redirect `/login` | [TYLKO FRONTEND] |
| 3 | Filter Menu | Input "Search" w sidebar + button "Clear" | `SidebarComponent.filterTree()` + `clearFilter()` | `filterTree()` w komponencie | [TYLKO FRONTEND] | N/D | N/D | N/D | Przycina węzły menu pasujące do tekstu / expanduje wszystko | [TYLKO FRONTEND] |
| 4 | Navigate | Klik na węzeł menu (mat-tree-node) | `SidebarComponent` → RouterLink | `Router.navigate()` | [TYLKO FRONTEND] | N/D | N/D | N/D | zmiana router-outlet na nowy ekran | [TYLKO FRONTEND] |
| 5 | Toggle Node (Expand/Collapse) | Klik na ikonę strzałki w drzewie | `SidebarComponent.toggleNode(node)` | `NestedTreeControl.toggle(node)` | [TYLKO FRONTEND] | N/D | N/D | N/D | Węzeł rozszerza/zawija się | [TYLKO FRONTEND] |
| 6 | Toggle Dark Mode | Przycisk w menu profilu (navbar) | `NavbarComponent.toggleTheme()` | `toggleTheme()` lokalnie | [TYLKO FRONTEND] | N/D | N/D | N/D | Klasa `dark-mode` dodana/usunięta na `document.body` | [TYLKO FRONTEND] |
| 7 | Navigate to Login | Link "Login" w navbar (ekrany publiczne) | RouterLink `/login` | `Router.navigate(['/login'])` | [TYLKO FRONTEND] | N/D | N/D | N/D | Redirect na ekran Login | [TYLKO FRONTEND] |
| 8 | Navigate to Register | Link "Register" w navbar (ekrany publiczne) | RouterLink `/register` | `Router.navigate(['/register'])` | [TYLKO FRONTEND] | N/D | N/D | N/D | Redirect na ekran Register | [TYLKO FRONTEND] |

## Szczegóły każdej operacji

### Operacja 1: Toggle Sidebar (menu boczne)

**Cel:** Pokazanie lub ukrycie menu bocznego

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika przycisk menu (hamburger) w navbar
2. **Frontend Handler** → `NavbarComponent.toggleSidebar()` wyzwala się
3. **Frontend Service** → `SidebarService.toggleSidebar()` zmienia wartość w `BehaviorSubject<boolean>`
4. **Walidacja FE** → Sprawdzenie `window.innerWidth`: jeśli < 1500px, auto-zamknięcie po wyborze pozycji menu
5. **API** → [TYLKO FRONTEND] — brak wywołania API
6. **Backend** → N/D
7. **Baza danych** → N/D
8. **Rezultat UI** → Sidebar zmienia widoczność (klasa CSS `mat-sidenav.opened / closed`)

---

### Operacja 2: Logout (wylogowanie)

**Cel:** Usunięcie sesji użytkownika i powrót na ekran logowania

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika "Logout" w menu profilu (navbar)
2. **Frontend Handler** → `NavbarComponent.logout()` wyzwala się
3. **Frontend Service** → `AuthService.logout()` usuwa token z localStorage
   - `localStorage.removeItem('authToken')`
   - Czyści `userInfo`
   - Emituje event `logoutSubject.next()`
4. **Walidacja FE** → Token nie istnieje w localStorage
5. **Router** → `Router.navigate(['/login'])`
6. **API** → [TYLKO FRONTEND] — brak POST `/logout` na backendzie (token po prostu usuwany z przeglądarki)
7. **Backend** → N/D
8. **Baza danych** → N/D
9. **Rezultat UI** → Użytkownik zostaje przekierowany na `/login`, navbar ukrywa przycisk profilu i pokazuje "Login" / "Register"

---

### Operacja 3: Filter Menu (filtrowanie drzewa nawigacji)

**Cel:** Filtrowanie pozycji menu po tekście wyszukiwania

**Kroki:**
1. **UI (Input)** → Użytkownik wpisuje tekst w pole "Search" w sidebar
2. **Frontend Handler** → Trigger `(keyup)` emituje event
3. **Frontend Service** → `SidebarComponent.filterTree(searchQuery: string)`
   - Konwertuje szukany tekst na małe litery
   - Przycina węzły, które NIE zawierają tekstu
   - Reguła: zachowaj węzeł, jeśli nazwa zawiera tekst LUB dziecko pasuje
4. **Walidacja FE** → Jeśli `searchQuery.length > 0`: `expandAll()`, jeśli `searchQuery === ""`: `collapseAll()`
5. **API** → [TYLKO FRONTEND]
6. **Backend** → N/D
7. **Baza danych** → N/D
8. **Rezultat UI** → 
   - Mat-tree odfiltrowana, rozwinięte są węzły zawierające wynik
   - Przycisk "Clear" pojawia się gdy `searchQuery !== ""`
   - Po kliknięciu "Clear": filtr zeruje się, wszystkie węzły zawijają się

---

### Operacja 4: Navigate (nawigacja między ekranami)

**Cel:** Przejście do innego ekranu aplikacji poprzez menu boczne

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika na węzeł menu (np. "Invoices" → `/documents/invoices`)
2. **Frontend Handler** → `mat-tree-node` ma `[routerLink]="[node.route]"`
3. **Frontend Service** → `Router.navigate([node.route])` emituje `NavigationEnd` event
4. **Router** → Router zmienia bieżącą trasę
5. **Guard** → Jeśli nowa trasa to trasa publiczna (`/login`, `/register`), sidebar schowa się
6. **AppComponent** → Nasłuchuje `Router.events.filter(NavigationEnd)` i re-renderuje router-outlet
7. **API** → [TYLKO FRONTEND] — brak przesyłania danych
8. **Backend** → N/D
9. **Baza danych** → N/D
10. **Rezultat UI** → 
    - `router-outlet` zmienia zawartość na nowy komponent
    - Klasa `active-link` przesunie się na nowy węzeł menu
    - Na mobilnych (<1500px) sidebar schowa się automatycznie

---

### Operacja 5: Toggle Node (rozwinięcie/zwinięcie grupy menu)

**Cel:** Pokazanie lub ukrycie podpozycji grupy menu

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika strzałkę rozwijającą grupy (Documents, Inventory, Settings)
2. **Frontend Handler** → `SidebarComponent.toggleNode(node)` wyzwala się
3. **Frontend Service** → `NestedTreeControl.toggle(node)` zmienia stan ekspandowania
4. **Walidacja FE** → Sprawdzenie czy węzeł ma dzieci (`hasChild(node)`)
5. **API** → [TYLKO FRONTEND]
6. **Backend** → N/D
7. **Baza danych** → N/D
8. **Rezultat UI** → Węzeł rozszerza się (pojawiają się dzieci) lub zawija się (chowają się dzieci)

---

### Operacja 6: Toggle Dark Mode (tryb ciemny)

**Cel:** Włączenie/wyłączenie motywu ciemnego

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika toggle "Dark Mode" w menu profilu
2. **Frontend Handler** → `NavbarComponent.toggleTheme()` wyzwala się
3. **Frontend Service** → `toggleTheme()` (lokalnie w komponencie)
   - Sprawdza czy `document.body` ma klasę `dark-mode`
   - Dodaje/usuwa klasę: `document.body.classList.toggle('dark-mode')`
4. **Walidacja FE** → Brak walidacji
5. **API** → [TYLKO FRONTEND]
6. **Backend** → N/D
7. **Baza danych** → N/D
8. **Rezultat UI** → 
   - Klasa `dark-mode` na `body` zmienia style CSS (kolory tła, tekstu)
   - [WYMAGA WERYFIKACJI] Stan nie jest utrwalany w localStorage — po odświeżeniu strony wraca tryb jasny

---

### Operacja 7: Navigate to Login (nawigacja na ekran logowania)

**Cel:** Przejście na ekran logowania z ekranu publicznego

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika link "Login" w navbar (widoczny na `/login` i `/register`)
2. **Frontend Handler** → `[routerLink]="['/login']"` wyzwala się
3. **Frontend Service** → `Router.navigate(['/login'])`
4. **Router** → Zmiana trasy na `/login`
5. **AppComponent** → Nasłuchuje `NavigationEnd`, sprawdza czy trasa zawiera `/login` → ukrywa sidebar
6. **API** → [TYLKO FRONTEND]
7. **Backend** → N/D
8. **Baza danych** → N/D
9. **Rezultat UI** → Wyświetlenie LoginComponent bez navbar i sidebar

---

### Operacja 8: Navigate to Register (nawigacja na ekran rejestracji)

**Cel:** Przejście na ekran rejestracji z ekranu publicznego

**Kroki:**
1. **UI (Klikniecie)** → Użytkownik klika link "Register" w navbar (widoczny na `/login` i `/register`)
2. **Frontend Handler** → `[routerLink]="['/register']"` wyzwala się
3. **Frontend Service** → `Router.navigate(['/register'])`
4. **Router** → Zmiana trasy na `/register`
5. **AppComponent** → Nasłuchuje `NavigationEnd`, sprawdza czy trasa zawiera `/register` → ukrywa sidebar
6. **API** → [TYLKO FRONTEND]
7. **Backend** → N/D
8. **Baza danych** → N/D
9. **Rezultat UI** → Wyświetlenie RegisterComponent bez navbar i sidebar

---

## Operacje bez backendu

Wszystkie operacje w AppShell są `[TYLKO FRONTEND]` — nie ma komunikacji z API dla samego zarządzania powłoką:

| Operacja | Czy ma API | Powód |
|---|---|---|
| Toggle Sidebar | [TYLKO FRONTEND] | Stan przechowywany w `SidebarService` (BehaviorSubject) |
| Logout | [TYLKO FRONTEND] | Token tylko usuwany z localStorage, bez komunikacji z backendem |
| Filter Menu | [TYLKO FRONTEND] | Filtrowanie wykonywane w komponencie Angular |
| Navigate | [TYLKO FRONTEND] | Routing wbudowany w Angular Router |
| Toggle Node | [TYLKO FRONTEND] | NestedTreeControl zarządza stanem w komponencie |
| Toggle Dark Mode | [TYLKO FRONTEND] | Toggle klasy CSS, brak utrwalenia w BD |
| Login / Register | [TYLKO FRONTEND] | Te są linkami do A-11 i A-12 (mają swoje procesy) |
