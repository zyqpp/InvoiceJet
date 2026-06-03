# Jak poruszać się po aplikacji

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## 1. Mapa nawigacji użytkownika

```
[Niezalogowany]
  /login       ← strona startowa / wymagana przed dostępem do dashboardu
  /register    ← rejestracja

[Zalogowany] → AuthGuard chroni WSZYSTKIE poniższe trasy
  /dashboard                        ← statystyki + wykres (DashboardComponent)
  │
  ├── Dokumenty
  │   ├── /dashboard/invoices                 ← lista faktur (InvoicesComponent)
  │   │   ├── /dashboard/add-invoice          ← nowa faktura
  │   │   └── /dashboard/edit-invoice/:id     ← edycja faktury
  │   │
  │   ├── /dashboard/invoice-proformas        ← lista proform (InvoiceProformasComponent)
  │   │   ├── /dashboard/add-invoice-proforma ← nowa proforma
  │   │   └── /dashboard/edit-invoice-proforma/:id
  │   │
  │   └── /dashboard/invoice-stornos          ← lista storn (InvoiceStornosComponent)
  │       └── /dashboard/edit-invoice-storno/:id ← edycja storno
  │           (BRAK /add-storno — tworzone przez TransformToStorno z listy faktur)
  │
  ├── Inwentarz
  │   ├── /dashboard/clients          ← klienci (ClientsComponent)
  │   └── /dashboard/products         ← produkty (ProductsComponent)
  │
  └── Ustawienia
      ├── /dashboard/firm-details     ← dane własnej firmy (FirmDetailsComponent)
      ├── /dashboard/bank-accounts    ← konta bankowe (BankAccountsComponent)
      └── /dashboard/document-series  ← serie dokumentów (DocumentSeriesComponent)
```

---

## 2. Logowanie i sesja

1. Użytkownik wchodzi na `/login`
2. Wprowadza email + hasło → klik "Login"
3. API zwraca JWT → zapisywany w `localStorage["authToken"]`
4. Angular `AuthGuard` i `AuthInterceptor` używają tokenu przy każdym żądaniu
5. **Token wygasa po 10 minutach** — użytkownik zostaje automatycznie wylogowany
6. Przy 401 → `ErrorInterceptor` wylogowuje i przekierowuje na `/login`

**Wylogowanie:** klik w NavbarComponent → `authService.logout()` → usunięcie tokenu z localStorage → redirect `/login`

---

## 3. Typowy przepływ tworzenia faktury

```
1. Dashboard → klik "Invoices" w sidebarze
2. Strona /dashboard/invoices → klik "Add Invoice"
3. Strona /dashboard/add-invoice ← AddOrEditInvoiceComponent
   ↓ ngOnInit: GET /Document/GetDocumentAutofillInfo/1
     (ładuje klientów, serie dokumentów, statusy, produkty)
4. Użytkownik wypełnia formularz:
   - Wybiera klienta (autocomplete z listy klientów)
   - Wybiera serię dokumentów (numer generowany automatycznie)
   - Wybiera datę wystawienia i termin płatności
   - Dodaje produkty (autocomplete lub nowe)
5. Klik "Save" → POST /Document/AddDocument
   ↓ serwis: generuje numer, tworzy dokument, inkrementuje serię
6. Redirect do /dashboard/invoices
7. (Opcjonalnie) Klik PDF → POST /Document/GetInvoicePdfStream
   → otwiera PdfViewerComponent z podglądem PDF
```

---

## 4. Struktura nawigacji w sidebarze

Sidebar (`SidebarComponent`) zawiera drzewo nawigacji zdefiniowane **hardcoded** w `loadData()`:

```
Dashboard
Documents
  ├── Invoices           → /dashboard/invoices
  ├── Invoice Proformas  → /dashboard/invoice-proformas
  └── Invoice Stornos    → /dashboard/invoice-stornos
Inventory
  ├── Clients            → /dashboard/clients
  └── Products           → /dashboard/products
Settings
  ├── Firm Details       → /dashboard/firm-details
  ├── Bank Accounts      → /dashboard/bank-accounts
  └── Document Series    → /dashboard/document-series
```

Sidebar ma wbudowany filtr tekstowy (`filterTree()`). Na ekranach szerszych niż 1500px sidebar jest widoczny na stałe (mode `"side"`), poniżej schowany (tryb `"over"`).

---

## 5. Operacje na listach (pattern)

Wszystkie listy (Clients, Products, BankAccounts, DocumentSeries, Invoices, etc.) mają identyczny wzorzec UX:

| Element | Opis |
|---|---|
| Tabela Material | `MatTableDataSource` z sortowaniem (`MatSort`) i paginacją (`MatPaginator`) |
| Checkboxy | `SelectionModel<T>` — zaznaczanie pojedynczych i wszystkich (`masterToggle()`) |
| Filtr tekstowy | `applyFilter()` — filtruje lokalnie po załadowaniu danych |
| Dodawanie | Dialog (`MatDialog`) lub nawigacja do trasy |
| Edycja | Dialog lub nawigacja — klik na wiersz |
| Usuwanie | Zaznacz → klik "Delete" → `PUT /api/*/Delete*` z tablicą ID |

---

## 6. Gdzie szukać dokumentacji konkretnego tematu

| Temat | Dokument |
|---|---|
| Architektura systemu | [03_architektura_aplikacji.md](03_architektura_aplikacji.md) |
| Stos technologiczny | [02_stos_technologiczny.md](02_stos_technologiczny.md) |
| Lista wszystkich endpointów API | [../_mapowania/inwentaryzacja_api.md](../_mapowania/inwentaryzacja_api.md) |
| Lista ekranów Angular | [../_mapowania/inwentaryzacja_ekranow.md](../_mapowania/inwentaryzacja_ekranow.md) |
| Tabele bazy danych | [../05_model_danych/01_db/spis_schem_i_tabel.md](../05_model_danych/01_db/spis_schem_i_tabel.md) |
| DTO | [../_mapowania/inwentaryzacja_dto.md](../_mapowania/inwentaryzacja_dto.md) |
| Role i uprawnienia | [../_mapowania/inwentaryzacja_rol.md](../_mapowania/inwentaryzacja_rol.md) |
| Procesy techniczne | [../_mapowania/inwentaryzacja_procesow.md](../_mapowania/inwentaryzacja_procesow.md) |
| Algorytmy | [../_mapowania/inwentaryzacja_algorytmow.md](../_mapowania/inwentaryzacja_algorytmow.md) |
| JWT i bezpieczeństwo | [06_globalne_mechanizmy.md](06_globalne_mechanizmy.md) |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Przewodnik po nawigacji aplikacji. |
