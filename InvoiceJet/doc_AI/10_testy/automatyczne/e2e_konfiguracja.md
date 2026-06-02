# Scenariusze testów automatycznych E2E: Konfiguracja

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-AUTO-E2E-KONFIGURACJA |
| Typ dokumentu | scenariusze testów automatycznych E2E |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-02 |
| Narzędzie | Playwright (TypeScript) |

## Streszczenie

Scenariusze pokrywają konfigurację aplikacji przez zalogowanego użytkownika: autouzupełnianie danych firmy z ANAF (ALG-06), zarządzanie seriami dokumentów (ALG-02) oraz weryfikację izolacji danych między użytkownikami (ALG-10). Selektory zweryfikowane w `firm-details.component.html`, `document-series.component.html` i `add-or-edit-document-series-dialog.component.html`.

> **Uwaga dla TC-AUTO-020 (ANAF):** Test wymaga dostępu do zewnętrznego API `https://webservicesp.anaf.ro/` lub mockowanego środowiska. W środowisku CI bez dostępu do internetu użyj interceptora sieciowego Playwright do podmienienia odpowiedzi ANAF.

---

## TC-AUTO-020: Autouzupełnienie danych firmy z ANAF

**Typ:** Happy path (wymaga połączenia z zewnętrznym API lub mocka)
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-06 ANAF Integration](../../03_algorytmy/ALG-06_AnafIntegration.md)

**Powiązane API:**
- `POST /api/Firm/GetFirmDataFromAnaf` (wewnętrzny endpoint przekazujący do ANAF)
- Zewnętrzny: `POST {AnafApiUrl}` (rumuński urząd skarbowy)

**Prereq w DB:**
- Zalogowany użytkownik `auto_anaf_020@invoicejet.test` / `Anaf020!`
- Rekord `UserFirm` bez powiązanej własnej firmy LUB firma istnieje (formularz w trybie "Update")
- Dostęp do ANAF API lub mock: CUI `12345678` zwraca dane `{ firmName: "SC DEMO SRL", regCom: "J40/1234/2020", address: "Str. Test 1", county: "Ilfov", city: "Buftea" }`

### Kroki — wariant z mockiem (zalecane do CI)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | setup mock | `page.route('**/api/Firm/GetFirmDataFromAnaf**', route => route.fulfill({...}))` | Body mock: `{ firmName: "SC DEMO SRL", regCom: "J40/1234/2020", address: "Str. Test 1", county: "Ilfov", city: "Buftea", cuiValue: "12345678" }` | Mock ANAF ustawiony; prawdziwe żądanie do ANAF nie jest wysyłane |
| 2 | login helper | — | `auto_anaf_020@invoicejet.test` / `Anaf020!` | Token JWT w localStorage; na `/dashboard` |
| 3 | navigate | URL bar | `/dashboard/firm-details` | Ekran Firm Details załadowany; formularz `[formGroup="firmDetailsForm"]` aktywny |
| 4 | verify progress bar gone | `mat-progress-bar` | — | Progress bar niewidoczny (formularz w trybie "Update" lub pusty bez istniejącej firmy) |
| 5 | clear and fill cuiValue | `mat-form-field input[formControlName="cuiValue"]` | `12345678` | Pole CUI Value wypełnione wartością "12345678" |
| 6 | click ANAF button | `mat-form-field:has(input[formControlName="cuiValue"]) button[mat-icon-button][matSuffix]` | — | Przycisk z ikoną `cloud_download` kliknięty; metoda `onCloudIconClick()` wywołana |
| 7 | wait for API | `POST /api/Firm/GetFirmDataFromAnaf` | — | Żądanie przechwycone przez mock; odpowiedź 200 OK z danymi firmy |
| 8 | verify firmName | `mat-form-field input[formControlName="firmName"]` | `SC DEMO SRL` | **[ALG-06]** Pole Firm Name autouzupełnione wartością z ANAF: "SC DEMO SRL" |
| 9 | verify regCom | `mat-form-field input[formControlName="regCom"]` | `J40/1234/2020` | **[ALG-06]** Pole RegCom autouzupełnione: "J40/1234/2020" |
| 10 | verify address | `mat-form-field input[formControlName="address"]` | `Str. Test 1` | **[ALG-06]** Pole Address autouzupełnione: "Str. Test 1" |
| 11 | verify county | `mat-form-field input[formControlName="county"]` | `Ilfov` | **[ALG-06]** Pole County autouzupełnione: "Ilfov" |
| 12 | verify city | `mat-form-field input[formControlName="city"]` | `Buftea` | **[ALG-06]** Pole City autouzupełnione: "Buftea" |
| 13 | click submit | `button[mat-raised-button][color="primary"][type="submit"]` | — | `POST /api/Firm/AddFirm/false` lub `PUT /api/Firm/EditFirm` wywołany; status 200/201 |
| 14 | verify no error | `div.p-error` | — | Brak komunikatu błędu `errorMessage` |

### Kroki — wariant z prawdziwym ANAF (tylko w środowisku z dostępem do internetu)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_anaf_020@invoicejet.test` / `Anaf020!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/firm-details` | Formularz Firm Details załadowany |
| 3 | fill cuiValue | `mat-form-field input[formControlName="cuiValue"]` | `14370840` | CUI aktywnej firmy rumuńskiej (Bitdefender — publiczne CUI) |
| 4 | click ANAF button | `mat-form-field:has(input[formControlName="cuiValue"]) button[mat-icon-button][matSuffix]` | — | Żądanie do prawdziwego ANAF API wysłane |
| 5 | wait max 10s | — | — | Odpowiedź z ANAF (czas zależy od zewnętrznego serwisu) |
| 6 | verify firmName not empty | `mat-form-field input[formControlName="firmName"]` | dowolna niepusta wartość | Pole firmName wypełnione danymi z ANAF |
| 7 | verify regCom not empty | `mat-form-field input[formControlName="regCom"]` | dowolna niepusta wartość | Pole regCom wypełnione |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-06] Żądanie do ANAF zawiera `[{cui: 12345678, data: "YYYY-MM-DD"}]` | Body POST do ANAF z bieżącą datą | Przechwycenie Network request do `/api/Firm/GetFirmDataFromAnaf`; weryfikacja body |
| [ALG-06] Mapowanie `date_generale.denumire` → `firmName` | `firmName = "SC DEMO SRL"` | Wartość pola `firmName` po autouzupełnieniu (krok 8) |
| [ALG-06] Mapowanie `adresa_domiciliu_fiscal.ddenumire_Judet` → `county` | `county = "Ilfov"` | Wartość pola `county` po autouzupełnieniu (krok 11) |
| [ALG-06] Mapowanie `adresa_domiciliu_fiscal.ddenumire_Localitate` → `city` | `city = "Buftea"` | Wartość pola `city` po autouzupełnieniu (krok 12) |
| [ALG-06] Błąd gdy CUI nie istnieje w ANAF | `FirmNotFoundException` propagowany; komunikat błędu na UI | Wypełnij `cuiValue = "00000001"` (fikcyjny CUI) → `div.p-error` lub `mat-snack-bar-container` z komunikatem błędu |

### Cleanup

- Jeśli firma została zapisana w kroku 13: usuń lub zaktualizuj ręcznie przez DB lub API
- Nie wymagane jeśli test tylko weryfikuje autouzupełnienie bez submitu

---

## TC-AUTO-021: Dodanie nowej serii dokumentów i weryfikacja numeracji faktury

**Typ:** Happy path
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-02 Document Number Generation](../../03_algorytmy/ALG-02_DocumentNumberGeneration.md)

**Powiązane API:**
- `POST /api/DocumentSeries/AddDocumentSeries`
- `GET /api/DocumentSeries/GetAll`
- `POST /api/Document/AddDocument`

**Prereq w DB:**
- Zalogowany użytkownik `auto_series_021@invoicejet.test` / `Series021!`
- Brak serii o nazwie "TEST" dla tego użytkownika
- Firma, klient i konto bankowe muszą istnieć (prereq jak w TC-AUTO-010)

### Kroki

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login helper | — | `auto_series_021@invoicejet.test` / `Series021!` | Na `/dashboard` |
| 2 | navigate | URL bar | `/dashboard/document-series` | Strona "Document Series" załadowana; tabela widoczna |
| 3 | verify no TEST series | `table[mat-table] td[mat-cell]:has-text("TEST")` | — | Seria "TEST" NIE jest widoczna w tabeli |
| 4 | click add button | `button[mat-raised-button]:has-text("New Series")` | — | Dialog `AddOrEditDocumentSeriesDialogComponent` otwarty; `mat-dialog-container` widoczny |
| 5 | click mat-select | `mat-dialog-container mat-select[formControlName="documentType"]` | — | Dropdown Document Type otwarty |
| 6 | click mat-option | `mat-option:has-text("Invoice")` | — | Typ dokumentu "Invoice" (documentTypeId=1) wybrany |
| 7 | fill seriesName | `mat-dialog-container mat-form-field input[formControlName="seriesName"]` | `TEST` | Pole Series Name wypełnione wartością "TEST" |
| 8 | fill firstNumber | `mat-dialog-container mat-form-field input[formControlName="firstNumber"]` | `1` | Pole First Number = 1 |
| 9 | fill currentNumber | `mat-dialog-container mat-form-field input[formControlName="currentNumber"]` | `1` | Pole Current Number = 1 (licznik startowy) |
| 10 | click submit | `mat-dialog-container button[mat-raised-button]:has-text("Submit")` | — | `POST /api/DocumentSeries/AddDocumentSeries` wywołany; status 201 Created |
| 11 | verify dialog closed | `mat-dialog-container` | — | Dialog zamknięty (niewidoczny) |
| 12 | verify series in table | `table[mat-table] td[mat-cell]:has-text("TEST")` | — | Seria "TEST" pojawia się w tabeli; kolumna "Series Name" = "TEST"; kolumna "Current Number" = "1" |
| 13 | navigate | URL bar | `/dashboard/add-invoice` | Formularz nowej faktury |
| 14 | click mat-select | `mat-select[formControlName="documentSeries"]` | — | Dropdown serii otwarty |
| 15 | click mat-option | `mat-option:has-text("TEST - 1")` | — | Seria "TEST" z numerem 1 wybrana |
| 16 | fill other required fields | formularz faktury | Klient, issueDate, pozycja (name="Usługa", unitPrice=100, quantity=1, tvaValue=19) | Wszystkie pola wypełnione |
| 17 | click submit | `button[mat-raised-button]:has-text("Issue")` | — | `POST /api/Document/AddDocument` wywołany z serią "TEST"; status 201 |
| 18 | verify document number | `table[mat-table] td[mat-cell]:has-text("TEST0001")` | — | **[ALG-02]** Faktura z numerem "TEST0001" widoczna w tabeli faktur (SeriesName="TEST" + CurrentNumber=1 → format D4 = "TEST0001") |
| 19 | navigate | URL bar | `/dashboard/document-series` | Lista serii |
| 20 | verify currentNumber incremented | `table[mat-table] tr[mat-row]:has(td:has-text("TEST")) td:has-text("2")` | — | **[ALG-02]** Seria "TEST" ma `currentNumber = 2` po wystawieniu faktury TEST0001 |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-02] Format numeru = SeriesName + D4 | `"TEST" + "0001"` = "TEST0001" | Wiersz "TEST0001" w tabeli faktur (krok 18) |
| [ALG-02] currentNumber inkrementowany po zapisie | `currentNumber = 2` w serii "TEST" | Tabela serii pokazuje "2" w kolumnie "Current Number" (krok 20) |
| [ALG-02] currentNumber = 10 → format D4 = "0010" | "TEST0010" | Ustaw `currentNumber = 10`, wystaw kolejną fakturę → numer "TEST0010" |

### Cleanup

- Usuń fakturę TEST0001 przez UI lub API
- Usuń serię "TEST" przez UI (zaznacz checkbox → menu "Delete selected") lub przez DB
- Reset: `DELETE FROM DocumentSeries WHERE SeriesName = 'TEST' AND UserFirmId = {id}`

---

## TC-AUTO-022: Izolacja danych — weryfikacja braku dostępu między użytkownikami

**Typ:** Bezpieczeństwo / Izolacja danych
**Priorytet:** Wysoki
**Powiązane algorytmy:**
- [ALG-10 Data Isolation Pattern](../../03_algorytmy/ALG-10_DataIsolationPattern.md)

**Powiązane API:**
- `GET /api/Firm/GetUserClients`
- `GET /api/Document/GetTableRecords`

**Prereq w DB:**
- Użytkownik A: `user_a_022@invoicejet.test` / `UserA022!` z powiązanym `UserFirmId = {userFirmA_id}`
- Użytkownik B: `user_b_022@invoicejet.test` / `UserB022!` z powiązanym `UserFirmId = {userFirmB_id}`
- Klient powiązany z User A: `name = "KLIENT USERA A SRL"`, `cui = "11111111"`, powiązany z `userFirmA_id`
- Faktura powiązana z User A: numer "ISOLA0001", `userFirmId = userFirmA_id`

### Kroki — Część 1: Dodanie klienta przez User A

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 1 | login as user A | `/login` | `user_a_022@invoicejet.test` / `UserA022!` | User A zalogowany; token A w localStorage |
| 2 | navigate | URL bar | `/dashboard/clients` | Lista klientów User A załadowana |
| 3 | click new client | `button[mat-raised-button]:has-text("New client")` | — | Dialog dodawania klienta otwarty |
| 4 | fill client data | Dialog pola | `name = "KLIENT USERA A SRL"`, `cuiValue = "11111111"`, `regCom = "J40/9999/2020"`, `address = "Str. Privata 1"`, `county = "Ilfov"`, `city = "Buftea"` | Wszystkie pola wypełnione w dialogu `add-edit-client-dialog` |
| 5 | click submit | `mat-dialog-container button[mat-raised-button]:has-text("Submit")` | — | Klient dodany; `POST /api/Firm/AddFirm/true` status 201 |
| 6 | verify client visible | `table[mat-table] td[mat-cell]:has-text("KLIENT USERA A SRL")` | — | Klient "KLIENT USERA A SRL" widoczny w tabeli klientów User A |

### Kroki — Część 2: Weryfikacja izolacji z perspektywy User B

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 7 | logout user A | `localStorage.clear()` lub klik elementu wylogowania | — | Token User A usunięty z localStorage |
| 8 | login as user B | `/login` | `user_b_022@invoicejet.test` / `UserB022!` | User B zalogowany; token B w localStorage |
| 9 | navigate | URL bar | `/dashboard/clients` | Lista klientów User B załadowana |
| 10 | verify client absent | `table[mat-table] td[mat-cell]:has-text("KLIENT USERA A SRL")` | — | **[ALG-10]** "KLIENT USERA A SRL" NIE jest widoczny w tabeli User B; izolacja `UserFirmId` działa poprawnie |
| 11 | verify own clients only | `table[mat-table] tbody tr[mat-row]` | — | Tabela jest pusta (User B nie ma klientów) lub zawiera wyłącznie klientów User B |

### Kroki — Część 3: Weryfikacja izolacji faktur (API)

| # | Akcja | Element UI / Selektor CSS | Wartość/Dane | Oczekiwany wynik |
|---|---|---|---|---|
| 12 | navigate (logged as B) | URL bar | `/dashboard/invoices` | Lista faktur User B załadowana |
| 13 | verify invoice absent | `table[mat-table] td[mat-cell]:has-text("ISOLA0001")` | — | **[ALG-10]** Faktura "ISOLA0001" należąca do User A NIE jest widoczna; izolacja przez `UserFirmId` w zapytaniu DB |
| 14 | API attempt — direct access | Wykonaj `GET /api/Document/GetById/{invoiceId_of_A}` z tokenem User B | Bearer token User B; ID faktury User A | **[ALG-10]** API zwraca 403 Forbidden lub 404 Not Found; User B nie ma dostępu do zasobu User A |

### Walidacja algorytmu

| Weryfikacja | Oczekiwana wartość | Jak sprawdzić |
|---|---|---|
| [ALG-10] User B nie widzi klientów User A na UI | Brak "KLIENT USERA A SRL" w tabeli User B | Brak wiersza w tabeli klientów (krok 10) |
| [ALG-10] User B nie widzi faktur User A na UI | Brak "ISOLA0001" w tabeli faktur User B | Brak wiersza w tabeli faktur (krok 13) |
| [ALG-10] Bezpośrednie API: 403/404 dla zasobu User A | HTTP 403 lub 404 z tokenem User B | Response status `page.waitForResponse(r => r.url().includes('GetById'))` |
| [ALG-10] `GetUserClients` filtruje przez `UserFirmId` | Odpowiedź zawiera wyłącznie klientów z `userFirmB_id` | API: `GET /api/Firm/GetUserClients` z tokenem B → lista NIE zawiera danych User A |

### Cleanup

- Usuń klienta "KLIENT USERA A SRL" przez API (z tokenem User A)
- Zachowaj konta User A i User B jeśli będą reużywane

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. Selektory zweryfikowane w `firm-details.component.html`, `document-series.component.html`, `add-or-edit-document-series-dialog.component.html`, `clients.component.html`. Uwzględniono wariant mock ANAF dla CI. |
