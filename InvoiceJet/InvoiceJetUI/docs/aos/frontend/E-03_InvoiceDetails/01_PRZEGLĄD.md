# Invoice Details — Przegląd

---

## 1. Layout ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ [NAGŁÓWEK APLIKACJI — NavbarComponent]                                      │
├──────────────────┬───────────────────────────────────────────────────────────┤
│                  │  [←] Invoice Details - 20240007 [Unpaid]                 │
│  [SIDEBAR]       ├───────────────────────────────────────────────────────────┤
│  Documents       │  Formularz dokumentu                                     │
│   - Invoices     │  [Client Name or CUI] [Issue Date] [Due Date] [Status]   │
│   - Proformas    ├───────────────────────────────────────────────────────────┤
│   - Stornos      │  Grid pozycji dokumentu                                  │
│                  │  ┌──────────────┬──────┬────┬────┬─────┬─────┬───────┐ │
│                  │  │ Product Name │ Unit │ Qt │ UM │ TVA │ Yes │ Total │ │
│                  │  ├──────────────┼──────┼────┼────┼─────┼─────┼───────┤ │
│                  │  │ [pole]       │ [#]  │[#] │buc │ 19  │ ☑   │ [#]   │ │
│                  │  │ [pole]       │ [#]  │[#] │buc │ 19  │ ☐   │ [#]   │ │
│                  │  └──────────────┴──────┴────┴────┴─────┴─────┴───────┘ │
│                  │  [Update / Issue] [Preview]                             │
└──────────────────┴───────────────────────────────────────────────────────────┘
```

### 1.2 Opis layoutu

Ekran zawiera pasek tytułu z przyciskiem Wstecz, tytułem `Invoice Details`, numerem dokumentu w trybie edycji i chipem statusu dokumentu. Pod paskiem tytułu znajduje się formularz dokumentu.

Pierwsza część formularza zawiera dane nagłówkowe dokumentu: klienta, datę wystawienia, termin płatności oraz serię dokumentu albo status dokumentu. Druga część formularza zawiera grid pozycji dokumentu. Każdy wiersz gridu jest grupą formularza z polami produktu, ceny, ilości, jednostki miary, TVA, flagi `Contains TVA`, ceny całkowitej i akcji.

---

## 2. Tryby ekranu

| Tryb | Warunek | Widoczne elementy | Główna operacja |
|---|---|---|---|
| Dodawanie faktury | Brak parametru `id` w URL `/dashboard/add-invoice` | Pole `Document Series`, przycisk `Issue`, brak przycisku `Preview`. | Dodanie dokumentu przez `addDocument()`. |
| Edycja faktury | Parametr `id` w URL `/dashboard/edit-invoice/:id` | Numer dokumentu w tytule, chip statusu, pole `Status`, przyciski `Update` i `Preview`. | Edycja dokumentu przez `updateDocument()`. |

---

## 3. Komponenty główne

### 3.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek ładowania | `mat-progress-bar` | Widoczny, gdy `loading` ma wartość `true`. |
| Pasek tytułu | `div.title-container` | Zawiera przycisk Wstecz, tytuł, numer dokumentu i chip statusu. |
| Formularz nagłówka | `form [formGroup]="invoiceForm"` | Zawiera pola klienta, dat, serii albo statusu. |
| Grid pozycji dokumentu | `table mat-table` | Zawiera dynamiczny `FormArray` pozycji dokumentu. |
| Kontrolki formularza | `div.controls` | Zawiera przycisk `Issue` albo `Update` oraz `Preview` w trybie edycji. |
| Dialog PDF | `PdfViewerComponent` | Wyświetla wygenerowany PDF w `iframe`. |

### 3.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk Wstecz | `button mat-icon-button` | Wywołuje `goBack()` i nawiguje do `/dashboard/invoices`. |
| Pole Client Name or CUI | `input matInput` z `mat-autocomplete` | Pozwala wybrać klienta po nazwie lub CUI. |
| Pole Issue Date | `mat-datepicker` | Ustawia datę wystawienia. |
| Pole Due Date | `mat-datepicker` | Ustawia termin płatności. |
| Pole Document Series | `mat-select` | Wybiera serię dokumentu w trybie dodawania. |
| Pole Status | `mat-select` | Wybiera status dokumentu w trybie edycji. |
| Pole Product Name | `input matInput` z `mat-autocomplete` | Pozwala wybrać produkt i autouzupełnia dane pozycji. |
| Przycisk Add | `button mat-icon-button` | Dodaje nowy wiersz pozycji dokumentu. |
| Przycisk Remove | `button mat-icon-button` | Usuwa wiersz pozycji dokumentu, jeżeli istnieje więcej niż jeden wiersz. |
| Przycisk Issue | `button mat-raised-button` | Zapisuje nową fakturę. |
| Przycisk Update | `button mat-raised-button` | Zapisuje zmiany edytowanej faktury. |
| Przycisk Preview | `button mat-raised-button` | Otwiera dialog podglądu PDF. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do `/dashboard/add-invoice` albo `/dashboard/edit-invoice/:id`.
2. `AuthGuard` dopuszcza dostęp, jeżeli `AuthService.isLoggedIn()` zwraca `true`.
3. Komponent inicjalizuje `invoiceForm`.
4. Komponent pobiera dane autouzupełniania przez `DocumentService.getDocumentAutofillInfo(1)`.
5. W trybie edycji komponent pobiera dokument przez `DocumentService.getDocumentById(id)` i wypełnia formularz.
6. Użytkownik wybiera klienta, daty, serię albo status oraz pozycje dokumentu.
7. Użytkownik klika `Issue` albo `Update`.
8. Jeżeli formularz jest poprawny, frontend wysyła model `IDocumentRequest`.
9. Po sukcesie wyświetlany jest komunikat i następuje nawigacja do `/dashboard/invoices`.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Ładowanie | Widoczny `mat-progress-bar`; formularz jest ukryty. | `loading = true`. |
| Dodawanie | Formularz ma pusty dokument i jeden domyślny wiersz produktu. | Wejście na `/dashboard/add-invoice`. |
| Edycja | Formularz jest wypełniony danymi dokumentu. | Wejście na `/dashboard/edit-invoice/:id`. |
| Autouzupełnianie klienta | Lista klientów jest filtrowana po nazwie albo CUI. | Zmiana wartości pola `client`. |
| Autouzupełnianie produktu | Lista produktów jest filtrowana po nazwie produktu. | Zmiana wartości pola `name` w pozycji dokumentu. |
| Przeliczanie pozycji | Pole `totalPrice` jest aktualizowane. | Zmiana ceny, ilości, TVA albo flagi `containsTva`. |
| Podgląd PDF | Otwarty dialog `PdfViewerComponent`. | Kliknięcie `Preview` w trybie edycji. |
| Błąd HTTP | Błąd obsługiwany przez interceptory lub lokalny `console.error`. | Odpowiedź HTTP z błędem. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| `AuthService.isLoggedIn()` zwraca `true` | Dostęp do ekranu jest dozwolony. |
| `AuthService.isLoggedIn()` zwraca `false` | `AuthGuard` wywołuje `AuthService.logout()` i przekierowuje do `/login`. |
| Token JWT istnieje w `localStorage` pod kluczem `authToken` | `AuthInterceptor` dodaje nagłówek `Authorization: Bearer {token}` do żądań HTTP. |
| Odpowiedź HTTP ma status `401` | `AuthInterceptor` przekierowuje do `/login` i wywołuje `AuthService.logout()`. |

---

## 7. Notatki techniczne

- Komponent ekranu: `AddOrEditInvoiceComponent`.
- Klasa bazowa: `BaseInvoiceComponent`.
- Typ dokumentu: `getDocumentTypeId()` zwraca `1`.
- URL powrotu: `getNavigationUrl()` zwraca `/dashboard/invoices`.
- Źródło danych gridu: `MatTableDataSource`.
- Formularz: `invoiceForm`.
- Pozycje dokumentu: `products: FormArray`.
- Dialog PDF: `PdfViewerComponent`.

---

## Następne sekcje

- Szczegółowe dane o polach, kolumnach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
