# Analityczny Opis Systemu — Frontend
## [NAZWA APLIKACJI] — [NAZWA EKRANU]

---

<!-- 
  ╔══════════════════════════════════════════════════════════════════════╗
  ║  INSTRUKCJA DLA AGENTA                                              ║
  ║  Ten blok komentarza usuń przed oddaniem dokumentu.                 ║
  ║  Każda sekcja zawiera [PLACEHOLDER] — zastąp je danymi z kodu.      ║
  ║  Sekcje oznaczone N/D zachowaj z wpisem "Nie dotyczy tego ekranu."  ║
  ╚══════════════════════════════════════════════════════════════════════╝
-->

---

## 1. Metadane dokumentu

| Atrybut | Wartość |
|---|---|
| **Aplikacja** | [NAZWA_APLIKACJI] |
| **Moduł** | [NAZWA_MODUŁU, np. Inventory / Documents / Settings] |
| **Ekran** | [BIZNESOWA_NAZWA_EKRANU] |
| **Wersja dokumentu** | 1.0 |
| **Data utworzenia** | [YYYY-MM-DD] |
| **Autor dokumentu** | Agent AI / [IMIĘ_NAZWISKO_WERYFIKUJĄCEGO] |
| **Status** | Roboczy / Do weryfikacji / Zatwierdzony |
| **Plik komponentu** | `src/app/components/[ścieżka]/[nazwa].component.ts` |
| **Plik szablonu** | `src/app/components/[ścieżka]/[nazwa].component.html` |
| **Ścieżka URL** | `/[ścieżka-routingu]` |
| **Lazy loading** | Tak / Nie |
| **Wersja aplikacji** | [WERSJA] |

---

## 2. Makieta / Wizualizacja ekranu

### 2.1 Opis ogólny ekranu

[Jeden akapit opisujący cel biznesowy ekranu — co użytkownik może na nim zrobić, jaki problem rozwiązuje.]

### 2.2 Struktura layoutu

```
┌─────────────────────────────────────────────────────────┐
│  [NAGŁÓWEK APLIKACJI — Navbar]                          │
├──────────────┬──────────────────────────────────────────┤
│              │  [TYTUŁ EKRANU]          [PRZYCISKI TOP] │
│  [SIDEBAR]   ├──────────────────────────────────────────┤
│              │  [SEKCJA FILTRÓW — jeśli istnieje]       │
│  - Link 1    ├──────────────────────────────────────────┤
│  - Link 2    │  [GRID / TABELA DANYCH]                  │
│  - ...       │                                          │
│              │  [PAGINACJA]                             │
└──────────────┴──────────────────────────────────────────┘
```

> Dostosuj diagram do rzeczywistej struktury ekranu. Dodaj lub usuń sekcje.

### 2.3 Nawigacja i dostęp

| Atrybut | Wartość |
|---|---|
| **Pozycja w menu bocznym** | [np. Inventory > Clients] |
| **Ścieżka routingu** | `[ścieżka]` |
| **Guard dostępu** | `[nazwa guarda, np. AuthGuard]` — [opis warunku, np. "wymagane zalogowanie"] |
| **Lazy loading modułu** | Tak (`[nazwa-chunk].chunk.js`) / Nie |
| **Przycisk Wstecz** | Tak (`[opis działania]`) / Nie |

### 2.4 Screen aplikacji

> Wstaw zrzut ekranu lub odwołanie do pliku graficznego:
> `![Ekran [NAZWA]](./screenshots/[nazwa-pliku].png)`

---

## 3. Sekcja filtrów

<!-- Jeśli ekran nie zawiera dedykowanej sekcji filtrów, wpisz poniżej: -->
<!-- > Ekran nie zawiera dedykowanej sekcji filtrów. -->

### 3.1 Opis sekcji filtrów

[Krótki opis — gdzie filtr się znajduje, czy jest stale widoczny, czy rozwijany, jak wpływa na dane.]

### 3.2 Pola filtrujące

| # | Nazwa wyświetlana | Typ pola | Binding / formControlName | Placeholder | Dozwolone wartości | Domyślna wartość | Wyzwalacz wyszukiwania | Selektor CSS / data-testid |
|---|---|---|---|---|---|---|---|---|
| 1 | [Nazwa] | [input/select/datepicker/checkbox] | `[formControlName lub ngModel]` | [tekst] | [opis wartości] | [wartość lub brak] | [onChange/onEnter/przycisk] | `[selektor]` |

### 3.3 Operacje sekcji filtrów

| Przycisk / Akcja | Typ | Event handler | Opis działania | Selektor CSS |
|---|---|---|---|---|
| [Szukaj / Filtruj] | `mat-raised-button` | `(click)="[metoda]()"` | [co wywołuje] | `[selektor]` |
| [Wyczyść] | `mat-button` | `(click)="[metoda]()"` | [co resetuje] | `[selektor]` |

---

## 4. Pola ekranu

<!-- Dotyczy pól formularza które nie są filtrami i nie są kolumnami gridu. -->
<!-- Typowe: formularze edycji, szczegóły rekordu, pola konfiguracyjne. -->
<!-- Jeśli ekran nie zawiera takich pól (np. jest tylko listą), wpisz: -->
<!-- > Ekran nie zawiera samodzielnych pól formularza poza gridem. -->

### 4.1 Formularz: [NAZWA FORMULARZA / SEKCJI]

> Podaj nazwę `FormGroup` z kodu, np. `clientForm`, `invoiceForm`.

#### Pole: [NAZWA_POLA_1]

| Atrybut | Wartość |
|---|---|
| **Nazwa wyświetlana** | [etykieta visible dla użytkownika] |
| **Nazwa biznesowa** | [nazwa w domenie biznesowej, np. "Numer identyfikacji podatkowej"] |
| **Tooltip** | [tekst tooltipa lub "Brak"] |
| **Typ pola** | [input text / input number / select / datepicker / checkbox / textarea / radio] |
| **Format / Maska** | [np. "YYYY-MM-DD", "tylko cyfry", "max 255 znaków", "brak"] |
| **Dozwolone wartości** | [słownik: nazwa_słownika / regex: wzorzec / zakres: min-max / dowolny tekst] |
| **Domyślna wartość** | [wartość lub "Brak"] |
| **Wypełnienie obowiązkowe** | Tak / Nie |
| **Widoczne** | Zawsze / Warunkowo: `[warunek ngIf/hidden]` |
| **Edytowalne** | Zawsze / Warunkowo: `[warunek disabled]` / Tylko do odczytu |
| **Walidatory** | `Validators.required`, `Validators.minLength(n)`, `Validators.pattern(regex)`, ... |
| **Komunikat walidacji** | `[tekst mat-error z HTML]` |
| **Logika specjalna** | [np. "Po wpisaniu CUI wywołuje ANAF API", "Blokuje zapis jeśli puste" — lub "Brak"] |
| **Pole w modelu TS** | `I[Interfejs].[pole]` |
| **formControlName** | `[wartość]` |
| **Dane techniczne** | Selektor: `[selektor CSS lub mat-form-field id]`; Serwis: `[serwis].[metoda]()` jeśli pole wywołuje API |

---

#### Pole: [NAZWA_POLA_2]

| Atrybut | Wartość |
|---|---|
| **Nazwa wyświetlana** | |
| **Nazwa biznesowa** | |
| **Tooltip** | |
| **Typ pola** | |
| **Format / Maska** | |
| **Dozwolone wartości** | |
| **Domyślna wartość** | |
| **Wypełnienie obowiązkowe** | |
| **Widoczne** | |
| **Edytowalne** | |
| **Walidatory** | |
| **Komunikat walidacji** | |
| **Logika specjalna** | |
| **Pole w modelu TS** | |
| **formControlName** | |
| **Dane techniczne** | |

<!-- Powiel blok powyżej dla każdego kolejnego pola formularza -->

---

## 5. Kolumny gridu / tabeli danych

<!-- Jeśli ekran nie zawiera gridu, wpisz: -->
<!-- > Ekran nie zawiera komponentu gridu / tabeli danych. -->

### 5.1 Opis gridu

| Atrybut | Wartość |
|---|---|
| **Komponent Angular** | `<mat-table>` / `<table mat-table>` |
| **Zmienna źródła danych** | `[dataSource]` — typ: `MatTableDataSource<I[Interfejs]>` / `[Interfejs][]` |
| **Paginacja** | Tak (po stronie serwera / klienta) / Nie |
| **Sortowanie** | Tak (kolumny: [lista]) / Nie |
| **Zaznaczanie wierszy** | Tak (checkbox `SelectionModel`) / Nie |
| **Ładowanie inicjalne** | `ngOnInit()` → `[serwis].[metoda]()` |
| **Selektor CSS tabeli** | `[selektor]` |
| **Parametry paginacji API** | `pageIndex`, `pageSize` / N/D |
| **Parametry sortowania API** | `sortField`, `sortDirection` / N/D |

### 5.2 Definicja kolumn

| # | matColumnDef | Nagłówek (wyświetlany) | Zawartość komórki | Typ | Sortowalna | Uwagi |
|---|---|---|---|---|---|---|
| 1 | `[matColumnDef]` | [Nagłówek] | `{{element.[pole]}}` | tekst / data / liczba / status-badge / akcje | Tak / Nie | [np. pipe: date, currency, custom] |
| 2 | | | | | | |
| 3 | | | | | | |
| ... | | | | | | |
| N | `actions` | Akcje | Przyciski: [lista przycisków] | akcje | Nie | |

### 5.3 Dane techniczne gridu

| Atrybut | Wartość |
|---|---|
| **Metoda ładowania danych** | `[serwis].[metoda](params)` |
| **Endpoint HTTP** | `[METODA] [URL]` |
| **Parametry żądania** | [lista query params lub body] |
| **Typ odpowiedzi API** | `I[Interfejs][]` / `{ data: I[Interfejs][], total: number }` |
| **Nagłówki HTTP** | `Authorization: Bearer JWT` (AuthInterceptor) |

---

## 6. Operacje

### 6.1 Tabela operacji ekranu

| # | Nazwa operacji | Typ elementu | Lokalizacja | Event | Handler w komponencie | Opis działania | Warunek aktywności | Selektor CSS |
|---|---|---|---|---|---|---|---|---|
| 1 | [Nazwa] | `mat-raised-button` / `mat-icon-button` / link | Pasek tytułu / Wiersz gridu / Formularz | `(click)` | `[nazwaMetody]()` | [opis biznesowy] | Zawsze / `[disabled]=[warunek]` | `[selektor]` |
| 2 | | | | | | | | |

### 6.2 Szczegóły operacji

#### Operacja: [NAZWA_OPERACJI_1]

| Atrybut | Wartość |
|---|---|
| **Typ operacji** | Nawigacja / Otwarcie dialogu / Wywołanie API / Walidacja + Wywołanie API / Eksport |
| **Handler** | `[nazwaMetody]()` w `[NazwaKomponentu].component.ts` linia ~[nr] |
| **Pre-walidacja** | Tak (`[formularz].valid`) / Nie |
| **Wywołanie serwisu** | `this.[serwis].[metoda](params)` |
| **Endpoint** | `[HTTP_METHOD] /api/[ścieżka]` |
| **Parametry żądania** | [opis body/params] |
| **Obsługa sukcesu** | [co dzieje się po sukcesie: odświeżenie listy / komunikat / nawigacja] |
| **Obsługa błędu** | [co dzieje się przy błędzie: snackbar / log / modal] |
| **Komunikat sukcesu** | `"[tekst]"` (MatSnackBar) / Brak |
| **Komunikat błędu** | `"[tekst]"` (MatSnackBar / error.interceptor) / Brak |

---

## 7. Okna modalne i dialogi

<!-- Jeśli ekran nie wywołuje żadnych dialogów, wpisz: -->
<!-- > Ekran nie wywołuje okien modalnych. -->

### 7.1 Dialog: [NAZWA_DIALOGU]

#### 7.1.1 Metadane dialogu

| Atrybut | Wartość |
|---|---|
| **Komponent dialogu** | `[NazwaDialogu]Component` |
| **Plik** | `src/app/components/[ścieżka]/[nazwa]-dialog.component.ts` |
| **Wywołanie** | `this.dialog.open([NazwaDialogu]Component, { data: [opis danych] })` |
| **Dane wejściowe (data)** | `{ [pole]: [typ] }` — [opis przekazywanych danych] |
| **Wynik (afterClosed)** | `[typ zwracanego obiektu]` / `undefined` jeśli anulowano |
| **Tytuł dialogu** | "[tekst]" |
| **Szerokość** | `[np. 400px, auto]` |

#### 7.1.2 Pola dialogu

| # | Nazwa wyświetlana | formControlName | Typ pola | Obowiązkowe | Walidatory | Komunikat walidacji | Domyślna wartość | Selektor CSS |
|---|---|---|---|---|---|---|---|---|
| 1 | [Nazwa] | `[formControlName]` | [typ] | Tak/Nie | [walidatory] | [tekst błędu] | [wartość] | `[selektor]` |

#### 7.1.3 Operacje dialogu

| Przycisk | Typ | Handler | Opis działania | Warunek aktywności | Endpoint API |
|---|---|---|---|---|---|
| [Zapisz/Dodaj/Aktualizuj] | `mat-raised-button` [color="primary"] | `[metoda]()` | [opis] | `[formularz].valid` | `[HTTP] /api/[ścieżka]` |
| Anuluj / Zamknij | `mat-button` | `dialogRef.close()` | Zamknięcie bez zapisu | Zawsze | N/D |

#### 7.1.4 Walidacje w dialogu

| Pole | Walidator | Komunikat | Kiedy wyświetlany |
|---|---|---|---|
| [Pole] | `Validators.required` | "[tekst]" | Po dotknięciu pola i opuszczeniu bez wartości |
| [Pole] | `Validators.pattern(...)` | "[tekst]" | Gdy wartość nie pasuje do wzorca |

---

## 8. Powiadomienia i obsługa błędów

### 8.1 Komunikaty sukcesu

| Operacja | Komunikat | Sposób wyświetlenia | Czas trwania |
|---|---|---|---|
| [Nazwa operacji] | `"[tekst]"` | MatSnackBar | [ms] |

### 8.2 Komunikaty błędów

| Źródło błędu | Kod HTTP / warunek | Komunikat | Sposób wyświetlenia |
|---|---|---|---|
| [Endpoint/operacja] | `[400/401/403/404/500]` | `"[tekst]"` | MatSnackBar / error.interceptor |
| Walidacja formularza | Frontend (przed API) | [per pole — patrz sekcja 4] | `mat-error` inline |

### 8.3 Walidacje inline formularzy

| Pole | Warunek błędu | Tekst komunikatu | Selektor mat-error |
|---|---|---|---|
| [Pole] | Pole puste (required) | `"[tekst]"` | `mat-error` w `mat-form-field` `formControlName="[nazwa]"` |
| [Pole] | Nieprawidłowy format | `"[tekst]"` | |

---

## 9. Zależności techniczne ekranu

### 9.1 Serwisy Angular

| Serwis | Plik | Metody używane przez ekran | Cel |
|---|---|---|---|
| `[NazwaSerwisu]Service` | `[plik].service.ts` | `[metoda1]()`, `[metoda2]()` | [opis] |

### 9.2 Modele danych (interfejsy TypeScript)

| Interfejs | Plik | Używany do |
|---|---|---|
| `I[Nazwa]` | `models/I[Nazwa].ts` | [cel: dane gridu / formularz / żądanie API / odpowiedź API] |

### 9.3 Interceptory HTTP

| Interceptor | Plik | Wpływ na ekran |
|---|---|---|
| `AuthInterceptor` | `interceptor/auth.interceptor.ts` | Dodaje nagłówek `Authorization: Bearer JWT` do każdego żądania |
| `ErrorInterceptor` | `interceptor/error.interceptor.ts` | Globalnie obsługuje błędy HTTP — [opis zachowania] |

### 9.4 Guards

| Guard | Plik | Warunek dostępu |
|---|---|---|
| `AuthGuard` | `guards/auth.guard.ts` | [opis — np. "Sprawdza obecność tokenu JWT w localStorage. Redirect do /login jeśli brak."] |

### 9.5 Routing

```
{
  path: '[ścieżka]',
  component: [NazwaKomponentu]Component,
  canActivate: [[Guard]]
}
```

---

## 10. Mapowanie danych: Frontend ↔ API ↔ Baza

| Pole na ekranie | formControlName | Pole w DTO (API) | Interfejs TS | Endpoint |
|---|---|---|---|---|
| [Nazwa pola] | `[formControlName]` | `[pole w JSON]` | `I[Interfejs].[pole]` | `[HTTP] /api/[ścieżka]` |

---

## 11. Scenariusze testowe (dla testerów)

### 11.1 Scenariusze pozytywne

| # | Scenariusz | Kroki | Oczekiwany rezultat | Selektor kluczowy |
|---|---|---|---|---|
| TC-01 | [Opis] | 1. [Krok] 2. [Krok] | [Oczekiwany wynik] | `[selektor]` |

### 11.2 Scenariusze negatywne / walidacje

| # | Scenariusz | Warunek | Oczekiwany błąd | Selektor weryfikacji |
|---|---|---|---|---|
| TC-N01 | [Opis] | [Warunek wejściowy] | [Komunikat/zachowanie] | `mat-error` / snackbar |

---

## 12. Historia zmian dokumentu

| Wersja | Data | Autor | Opis zmian |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | Agent AI | Dokument inicjalny |

---

---
---

# PRZYKŁAD WYPEŁNIENIA: Ekran „Clients" — InvoiceJet

> Poniżej kompletny przykład dokumentu AOS dla ekranu Clients aplikacji InvoiceJet.
> Służy jako wzorzec dla agenta — pokazuje oczekiwany poziom szczegółowości.

---

## 1. Metadane dokumentu

| Atrybut | Wartość |
|---|---|
| **Aplikacja** | InvoiceJet |
| **Moduł** | Inventory |
| **Ekran** | Klienci (Clients) |
| **Wersja dokumentu** | 1.0 |
| **Data utworzenia** | 2025-05-29 |
| **Autor dokumentu** | Agent AI / [Do weryfikacji] |
| **Status** | Do weryfikacji |
| **Plik komponentu** | `src/app/components/firm/clients/clients.component.ts` |
| **Plik szablonu** | `src/app/components/firm/clients/clients.component.html` |
| **Ścieżka URL** | `/clients` |
| **Lazy loading** | Do potwierdzenia (brak `loadChildren` w widocznym routingu — wymaga weryfikacji) |
| **Wersja aplikacji** | 1.0 |

---

## 2. Makieta / Wizualizacja ekranu

### 2.1 Opis ogólny ekranu

Ekran Klienci umożliwia przeglądanie listy firm-klientów przypisanych do zalogowanego użytkownika oraz zarządzanie nimi (dodawanie, edycja, usuwanie). Każdy klient reprezentuje firmę, dla której wystawiać będą się dokumenty finansowe (faktury, proformy, storna). Dane klientów są reużywane na ekranie tworzenia dokumentów.

### 2.2 Struktura layoutu

```
┌─────────────────────────────────────────────────────────────┐
│  InvoiceJet                              [Avatar użytkownika] │
├──────────────────┬──────────────────────────────────────────┤
│                  │  Clients              [+ New Client] [⋮]  │
│  Dashboard       ├──────────────────────────────────────────┤
│  Documents ▾     │  ☐  Name  │ CUI  │ RegCom │ Address │... │
│    Invoices      │  ☐  [row] │ ...  │ ...    │ ...     │... │
│    Proformas     │  ☐  [row] │ ...  │ ...    │ ...     │... │
│    Stornos       │  ...                                      │
│  Inventory ▾     │                                           │
│    Clients  ←    │                                           │
│    Products      │                                           │
│  Settings ▾      │                                           │
│    Firm Details  │                                           │
│    Bank Accounts │                                           │
│    Doc. Series   │                                           │
└──────────────────┴───────────────────────────────────────────┘
```

### 2.3 Nawigacja i dostęp

| Atrybut | Wartość |
|---|---|
| **Pozycja w menu bocznym** | Inventory > Clients |
| **Ścieżka routingu** | `/clients` |
| **Guard dostępu** | `AuthGuard` — wymagane zalogowanie (obecność ważnego tokenu JWT) |
| **Lazy loading modułu** | Do potwierdzenia w `app-routing.module.ts` |
| **Przycisk Wstecz** | Nie dotyczy (ekran poziomy w menu) |

### 2.4 Screen aplikacji

> `![Ekran Clients](./screenshots/clients-list.png)`
> *(Zrzut dostępny w dokumentacji projektu — Picture8.png)*

---

## 3. Sekcja filtrów

> Ekran nie zawiera dedykowanej sekcji filtrów (brak oddzielnego formularza filtrów w widocznym HTML komponentu `clients.component.html`).
> Funkcja wyszukiwania może być realizowana przez globalny komponent Search w Navbar — wymaga weryfikacji z zespołem.

---

## 4. Pola ekranu

> Ekran Clients w trybie listy nie zawiera samodzielnych pól formularza — dane są wyświetlane wyłącznie w gridzie.
> Pola formularzy edycji/dodawania klienta są dokumentowane w sekcji 7 (Okna modalne — Add/Edit Client Dialog).

---

## 5. Kolumny gridu / tabeli danych

### 5.1 Opis gridu

| Atrybut | Wartość |
|---|---|
| **Komponent Angular** | `<mat-table>` (Angular Material) |
| **Zmienna źródła danych** | `clients` — typ: `IFirm[]` (na podstawie modelu `IFirm.ts`) |
| **Paginacja** | Do weryfikacji (brak `mat-paginator` widocznego na screenie; możliwe że dane są ładowane w całości) |
| **Sortowanie** | Do weryfikacji w kodzie komponentu |
| **Zaznaczanie wierszy** | Tak — checkbox w pierwszej kolumnie (`SelectionModel` lub `mat-checkbox`) |
| **Ładowanie inicjalne** | `ngOnInit()` → `firmService.getClients()` lub `firmService.getFirms()` |
| **Selektor CSS tabeli** | `[WYMAGA WERYFIKACJI z kodu HTML]` |
| **Parametry paginacji API** | Do weryfikacji |
| **Parametry sortowania API** | Do weryfikacji |

### 5.2 Definicja kolumn

Na podstawie widocznego screenu (Picture8.png):

| # | matColumnDef | Nagłówek (wyświetlany) | Zawartość komórki | Typ | Sortowalna | Uwagi |
|---|---|---|---|---|---|---|
| 0 | `select` | ☐ (checkbox) | `<mat-checkbox>` zaznaczenia wiersza | checkbox | Nie | Nagłówek: checkbox "Zaznacz wszystkie" |
| 1 | `name` | Name | `{{element.name}}` | tekst | Do weryfikacji | Nazwa firmy klienta |
| 2 | `cui` | CUI | `{{element.cui}}` | tekst | Do weryfikacji | Numer identyfikacji podatkowej (RO: CUI) |
| 3 | `regCom` | RegCom | `{{element.regCom}}` | tekst | Do weryfikacji | Numer rejestracji w rejestrze handlowym |
| 4 | `address` | Address | `{{element.address}}` | tekst | Do weryfikacji | Pełny adres siedziby klienta |
| 5 | `actions` | (brak nagłówka) | Przyciski: [Edytuj] | akcje | Nie | Przycisk wywołujący dialog edycji |

> **Uwaga:** Dokładne wartości `matColumnDef` wymagają potwierdzenia z pliku `clients.component.html`.
> Kolumna County i City mogą być oddzielnymi kolumnami lub częścią Address — do weryfikacji.

### 5.3 Dane techniczne gridu

| Atrybut | Wartość |
|---|---|
| **Metoda ładowania danych** | `firmService.getClients()` (szacowane — do weryfikacji z `.ts`) |
| **Endpoint HTTP** | `GET /api/firms/clients` lub `GET /api/firms` — [WYMAGA WERYFIKACJI z `firm.service.ts`] |
| **Parametry żądania** | Brak (pełna lista) lub `{ isClient: true }` — do weryfikacji |
| **Typ odpowiedzi API** | `IFirm[]` |
| **Nagłówki HTTP** | `Authorization: Bearer JWT` (dodawany przez `AuthInterceptor`) |

---

## 6. Operacje

### 6.1 Tabela operacji ekranu

| # | Nazwa operacji | Typ elementu | Lokalizacja | Event | Handler | Opis działania | Warunek aktywności | Selektor CSS |
|---|---|---|---|---|---|---|---|---|
| 1 | Nowy klient | `mat-raised-button` color="primary" | Pasek tytułu, prawy górny róg | `(click)` | `openAddClientDialog()` lub `openDialog()` | Otwiera dialog dodawania nowego klienta | Zawsze | `[WYMAGA WERYFIKACJI]` |
| 2 | Menu kontekstowe (⋮) | `mat-icon-button` | Pasek tytułu, obok "New Client" | `(click)` | `[metoda]` | Rozwija menu z opcją "Delete selected" | Zawsze | `[WYMAGA WERYFIKACJI]` |
| 3 | Usuń zaznaczone | `mat-menu-item` (w menu ⋮) | Menu kontekstowe | `(click)` | `deleteSelected()` lub `deleteClients()` | Usuwa zaznaczone wiersze (z potwierdzeniem lub bez) | Min. 1 wiersz zaznaczony | `[WYMAGA WERYFIKACJI]` |
| 4 | Edytuj klienta | Ikona/przycisk w wierszu gridu | Kolumna Actions w gridzie | `(click)` | `openEditDialog(client)` lub `editClient(client)` | Otwiera dialog edycji wybranego klienta | Zawsze (dla każdego wiersza) | `[WYMAGA WERYFIKACJI]` |

### 6.2 Szczegóły operacji

#### Operacja: Nowy klient (New Client)

| Atrybut | Wartość |
|---|---|
| **Typ operacji** | Otwarcie dialogu modalnego |
| **Handler** | `openAddClientDialog()` / `openDialog()` w `ClientsComponent` |
| **Pre-walidacja** | Nie |
| **Wywołanie serwisu** | Po zamknięciu dialogu z wynikiem: `firmService.addClient(newClient)` [do weryfikacji] |
| **Endpoint** | `POST /api/firms` lub `POST /api/firms/clients` — [WYMAGA WERYFIKACJI] |
| **Parametry żądania** | `IFirm` (dane nowego klienta z formularza dialogu) |
| **Obsługa sukcesu** | Odświeżenie listy klientów, zamknięcie dialogu |
| **Obsługa błędu** | MatSnackBar z komunikatem błędu |
| **Komunikat sukcesu** | `"Client added successfully"` [WYMAGA WERYFIKACJI] |
| **Komunikat błędu** | Obsługiwany przez `ErrorInterceptor` |

#### Operacja: Usuń zaznaczone (Delete selected)

| Atrybut | Wartość |
|---|---|
| **Typ operacji** | Wywołanie API (DELETE) |
| **Handler** | `deleteSelected()` lub `deleteClients()` w `ClientsComponent` |
| **Pre-walidacja** | Sprawdzenie czy zaznaczono min. 1 wiersz |
| **Wywołanie serwisu** | `firmService.deleteClient(id)` lub batch delete — [WYMAGA WERYFIKACJI] |
| **Endpoint** | `DELETE /api/firms/{id}` lub `DELETE /api/firms` z body — [WYMAGA WERYFIKACJI] |
| **Parametry żądania** | ID lub tablica ID zaznaczonych klientów |
| **Obsługa sukcesu** | Usunięcie wierszy z listy, opcjonalny komunikat sukcesu |
| **Obsługa błędu** | MatSnackBar z komunikatem błędu |
| **Komunikat sukcesu** | [WYMAGA WERYFIKACJI] |
| **Komunikat błędu** | Obsługiwany przez `ErrorInterceptor` |

---

## 7. Okna modalne i dialogi

### 7.1 Dialog: Add/Edit Client (AddEditClientDialogComponent)

#### 7.1.1 Metadane dialogu

| Atrybut | Wartość |
|---|---|
| **Komponent dialogu** | `AddEditClientDialogComponent` |
| **Plik** | `src/app/components/firm/add-edit-client-dialog/add-edit-client-dialog.component.ts` |
| **Wywołanie (Add)** | `this.dialog.open(AddEditClientDialogComponent, { data: null })` [szacowane] |
| **Wywołanie (Edit)** | `this.dialog.open(AddEditClientDialogComponent, { data: { client: selectedClient } })` [szacowane] |
| **Dane wejściowe (data)** | `null` dla trybu Dodaj; `{ client: IFirm }` dla trybu Edytuj |
| **Wynik (afterClosed)** | `IFirm` (nowy/zaktualizowany klient) lub `undefined` jeśli Anulowano |
| **Tytuł dialogu** | "Add Client" / "Edit Client" (dynamiczny na podstawie trybu) |
| **Szerokość** | ~940px (full-screen panel po prawej stronie — patrz screen) |

#### 7.1.2 Pola dialogu

Na podstawie screenu (Picture8.png — panel "Edit Client"):

| # | Nazwa wyświetlana | formControlName | Typ pola | Obowiązkowe | Walidatory | Komunikat walidacji | Domyślna wartość | Selektor CSS |
|---|---|---|---|---|---|---|---|---|
| 1 | Firm Name | `firmName` | `mat-input` (text) | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak (tryb Add) / Aktualna wartość (Edit) | `[formControlName="firmName"]` |
| 2 | CUI Value | `cuiValue` | `mat-input` (text) + button "Pobierz z ANAF" | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak / Aktualna wartość | `[formControlName="cuiValue"]` |
| 3 | Registration Number (RegCom) | `regCom` | `mat-input` (text) | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak / Aktualna wartość | `[formControlName="regCom"]` |
| 4 | Address | `address` | `mat-input` (text) | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak / Aktualna wartość | `[formControlName="address"]` |
| 5 | County | `county` | `mat-input` (text) | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak / Aktualna wartość | `[formControlName="county"]` |
| 6 | City | `city` | `mat-input` (text) | Tak (`*`) | `Validators.required` | [WYMAGA WERYFIKACJI] | Brak / Aktualna wartość | `[formControlName="city"]` |

> **Pole specjalne — CUI Value:** Przycisk ikony (upload/cloud) obok pola CUI wywołuje ANAF API.
> Po wpisaniu CUI i kliknięciu przycisku — autouzupełnia pola: Firm Name, RegCom, Address, County, City danymi z zewnętrznego rejestru firm.
> Serwis: `firmService.getFirmDataByCui(cui)` lub podobny → `GET [ANAF_ENDPOINT]?cui=[wartość]`

#### 7.1.3 Operacje dialogu

| Przycisk | Typ | Handler | Opis działania | Warunek aktywności | Endpoint API |
|---|---|---|---|---|---|
| Update / Add | `mat-raised-button` color="primary" | `saveClient()` lub `updateClient()` / `addClient()` | Waliduje formularz i wysyła dane do API. Zamyka dialog z wynikiem po sukcesie. | `clientForm.valid` | `POST /api/firms` (Add) lub `PUT /api/firms/{id}` (Edit) — [WYMAGA WERYFIKACJI] |
| Cancel | `mat-button` | `dialogRef.close()` lub `cancel()` | Zamyka dialog bez zapisu. Dane nie są zapisywane. | Zawsze | N/D |

#### 7.1.4 Walidacje w dialogu

| Pole | Walidator | Komunikat | Kiedy wyświetlany |
|---|---|---|---|
| Firm Name | `Validators.required` | [WYMAGA WERYFIKACJI z `mat-error` w HTML] | Po dotknięciu pola i opuszczeniu bez wartości |
| CUI Value | `Validators.required` | [WYMAGA WERYFIKACJI] | j.w. |
| Registration Number | `Validators.required` | [WYMAGA WERYFIKACJI] | j.w. |
| Address | `Validators.required` | [WYMAGA WERYFIKACJI] | j.w. |
| County | `Validators.required` | [WYMAGA WERYFIKACJI] | j.w. |
| City | `Validators.required` | [WYMAGA WERYFIKACJI] | j.w. |

> **Logika specjalna CUI — integracja ANAF API:**
> Przycisk "cloud/upload" przy polu CUI wywołuje zewnętrzne API ANAF (rumuński rejestr podatkowy).
> Rezultat autouzupełnia pozostałe pola formularza. Jest to kluczowa funkcjonalność biznesowa wymagająca osobnego testu integracyjnego.

---

## 8. Powiadomienia i obsługa błędów

### 8.1 Komunikaty sukcesu

| Operacja | Komunikat | Sposób wyświetlenia | Czas trwania |
|---|---|---|---|
| Dodanie klienta | [WYMAGA WERYFIKACJI z kodu] | MatSnackBar | [ms — WYMAGA WERYFIKACJI] |
| Edycja klienta | [WYMAGA WERYFIKACJI] | MatSnackBar | |
| Usunięcie klienta | [WYMAGA WERYFIKACJI] | MatSnackBar | |

### 8.2 Komunikaty błędów

| Źródło błędu | Kod HTTP | Komunikat | Sposób wyświetlenia |
|---|---|---|---|
| GET lista klientów | 401 | Redirect do /login (AuthGuard/Interceptor) | Nawigacja |
| GET lista klientów | 500 | [WYMAGA WERYFIKACJI] | MatSnackBar / ErrorInterceptor |
| POST/PUT klient | 400 | [WYMAGA WERYFIKACJI — walidacja backend] | MatSnackBar |
| POST/PUT klient | 500 | [WYMAGA WERYFIKACJI] | MatSnackBar |
| ANAF API | Timeout/Błąd | [WYMAGA WERYFIKACJI] | MatSnackBar |
| Walidacja formularza | Frontend | Per-pole (patrz 7.1.4) | `mat-error` inline |

---

## 9. Zależności techniczne ekranu

### 9.1 Serwisy Angular

| Serwis | Plik | Metody używane przez ekran | Cel |
|---|---|---|---|
| `FirmService` | `services/firm.service.ts` | `getClients()` / `getFirms()`, `addClient()`, `updateClient()`, `deleteClient()` | CRUD klientów; integracja ANAF API po CUI |
| `MatDialog` | Angular Material | `open(AddEditClientDialogComponent, ...)` | Otwieranie dialogów dodaj/edytuj |
| `MatSnackBar` | Angular Material | `open(message, action, config)` | Komunikaty sukcesu/błędu |

### 9.2 Modele danych (interfejsy TypeScript)

| Interfejs | Plik | Używany do |
|---|---|---|
| `IFirm` | `models/IFirm.ts` | Typ danych klienta (wiersze gridu, dane formularza dialogu, żądania API) |

Pola interfejsu `IFirm` (szacowane na podstawie screenu i schematu bazy):

| Pole | Typ TS | Obowiązkowe | Odpowiednik w bazie (tabela Firm) |
|---|---|---|---|
| `id` | `number` | Tak | `Firm.Id` |
| `name` | `string` | Tak | `Firm.Name` |
| `cui` | `string` | Tak | `Firm.CUI` |
| `regCom` | `string` | Tak | `Firm.RegCom` |
| `address` | `string` | Tak | `Firm.Address` |
| `county` | `string` | Tak | `Firm.County` |
| `city` | `string` | Tak | `Firm.City` |

> Dokładna lista pól wymaga weryfikacji z `models/IFirm.ts`.

### 9.3 Interceptory HTTP

| Interceptor | Plik | Wpływ na ekran |
|---|---|---|
| `AuthInterceptor` | `interceptor/auth.interceptor.ts` | Dodaje `Authorization: Bearer JWT` do każdego żądania HTTP wykonanego przez `FirmService` |
| `ErrorInterceptor` | `interceptor/error.interceptor.ts` | Globalnie obsługuje błędy HTTP — przechwytuje odpowiedzi z kodem 4xx/5xx i wyświetla komunikat lub wykonuje redirect |

### 9.4 Guards

| Guard | Plik | Warunek dostępu |
|---|---|---|
| `AuthGuard` | `guards/auth.guard.ts` | Sprawdza obecność i ważność tokenu JWT. Jeśli brak — redirect do `/login`. |

### 9.5 Routing

```typescript
// app-routing.module.ts (szacowane — WYMAGA WERYFIKACJI)
{
  path: 'clients',
  component: ClientsComponent,
  canActivate: [AuthGuard]
}
```

---

## 10. Mapowanie danych: Frontend ↔ API ↔ Baza

| Pole na ekranie (Dialog) | formControlName | Pole w DTO (API JSON) | Interfejs TS | Tabela.Kolumna (DB) | Endpoint |
|---|---|---|---|---|---|
| Firm Name | `firmName` | `name` | `IFirm.name` | `Firm.Name` | `POST/PUT /api/firms` |
| CUI Value | `cuiValue` | `cui` | `IFirm.cui` | `Firm.CUI` | `POST/PUT /api/firms` |
| Registration Number | `regCom` | `regCom` | `IFirm.regCom` | `Firm.RegCom` | `POST/PUT /api/firms` |
| Address | `address` | `address` | `IFirm.address` | `Firm.Address` | `POST/PUT /api/firms` |
| County | `county` | `county` | `IFirm.county` | `Firm.County` | `POST/PUT /api/firms` |
| City | `city` | `city` | `IFirm.city` | `Firm.City` | `POST/PUT /api/firms` |

> Mapowanie oparte na screenie i schemacie bazy. Dokładne nazwy pól JSON wymagają weryfikacji z `firm.service.ts` i DTO po stronie backendu.

---

## 11. Scenariusze testowe (dla testerów)

### 11.1 Scenariusze pozytywne

| # | Scenariusz | Kroki | Oczekiwany rezultat | Selektor kluczowy |
|---|---|---|---|---|
| TC-01 | Wyświetlenie listy klientów | 1. Zaloguj się. 2. Kliknij "Clients" w menu. | Lista klientów zalogowanego użytkownika wyświetlona w gridzie. | `mat-table` / `[data-testid="clients-table"]` |
| TC-02 | Dodanie nowego klienta | 1. Kliknij "+ New Client". 2. Wypełnij wszystkie pola. 3. Kliknij "Add/Update". | Dialog zamknięty. Nowy klient widoczny w gridzie. | `[formControlName="firmName"]`, `button[color="primary"]` |
| TC-03 | Edycja klienta | 1. Kliknij ikonę edycji przy kliencie. 2. Zmień pole "City". 3. Kliknij "Update". | Dialog zamknięty. Zmieniona wartość widoczna w gridzie. | `[formControlName="city"]` |
| TC-04 | Autouzupełnianie z ANAF | 1. Otwórz dialog Add. 2. Wpisz CUI. 3. Kliknij ikonę "cloud". | Pola Firm Name, RegCom, Address, County, City wypełnione automatycznie. | `[formControlName="cuiValue"]`, ikona ANAF |
| TC-05 | Usunięcie klienta | 1. Zaznacz checkbox przy kliencie. 2. Kliknij "⋮". 3. Kliknij "Delete selected". | Klient usunięty z listy. | `mat-checkbox`, `mat-menu-item` |

### 11.2 Scenariusze negatywne / walidacje

| # | Scenariusz | Warunek | Oczekiwany błąd | Selektor weryfikacji |
|---|---|---|---|---|
| TC-N01 | Próba zapisu bez nazwy firmy | Pole "Firm Name" puste, kliknięcie "Add" | Komunikat walidacji inline pod polem. Przycisk dezaktywowany lub zapis zablokowany. | `mat-error` przy `[formControlName="firmName"]` |
| TC-N02 | Próba zapisu bez CUI | Pole "CUI Value" puste | Komunikat walidacji inline. Zapis zablokowany. | `mat-error` przy `[formControlName="cuiValue"]` |
| TC-N03 | Dostęp bez logowania | Próba wejścia na `/clients` bez tokenu | Redirect do `/login` | URL: `/login` |
| TC-N04 | ANAF API niedostępne | CUI wpisany, kliknięcie "cloud", API zwraca błąd | Komunikat błędu (snackbar). Pola pozostają puste lub zachowują poprzednie wartości. | MatSnackBar |

---

## 12. Historia zmian dokumentu

| Wersja | Data | Autor | Opis zmian |
|---|---|---|---|
| 1.0 | 2025-05-29 | Agent AI (Claude Sonnet 4.6) | Dokument inicjalny — wygenerowany na podstawie screenshotów, struktury katalogów i modeli danych. Sekcje oznaczone [WYMAGA WERYFIKACJI] wymagają potwierdzenia z kodem źródłowym. |
