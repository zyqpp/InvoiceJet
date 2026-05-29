# Clients — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy klientów

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje grid klientów.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jeden rekord klienta.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Clients. | URL `/dashboard/clients` | N/D | Ekran Clients jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze klientów. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Name`, `CUI`, `RegCom`, `Address`, `County`, `City`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie klientów

**Typ:** Functional  
**Cel:** Weryfikacja działania pola Search.  
**Warunek wstępny:** Ekran Clients zawiera kilka rekordów.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `job` | Grid wyświetla wiersze pasujące do filtra `job`. |
| 3 | Sprawdź przycisk Clear. | `button[aria-label="Clear"]` | N/D | Przycisk Clear jest widoczny. |
| 4 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Sortowanie gridu

**Typ:** Functional  
**Cel:** Weryfikacja sortowania przez `mat-sort-header`.  
**Warunek wstępny:** Grid zawiera co najmniej dwa rekordy.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij nagłówek kolumny Name. | `th[mat-sort-header][sortActionDescription="Sort by name"]` | N/D | Grid sortuje wiersze po kolumnie `name`. |
| 2 | Kliknij nagłówek kolumny CUI. | `th[mat-sort-header][sortActionDescription="Sort by CUI"]` | N/D | Grid sortuje wiersze po kolumnie `cui`. |
| 3 | Kliknij nagłówek kolumny City. | `th[mat-sort-header][sortActionDescription="Sort by city"]` | N/D | Grid sortuje wiersze po kolumnie `city`. |

---

## 4. Scenariusz: Dodanie klienta

**Typ:** Happy Path  
**Cel:** Weryfikacja dodania klienta przez dialog.  
**Warunek wstępny:** Użytkownik jest zalogowany. API przyjmuje żądanie dodania klienta.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk New client. | `button[mat-raised-button][color="primary"]` w `.app-header` | N/D | Otwiera się dialog `New Client`. |
| 2 | Wypełnij pole Firm Name. | `input[formControlName="firmName"]` | `ACME TEST S.R.L.` | Pole zawiera podaną wartość. |
| 3 | Wypełnij pole CUI Value. | `input[formControlName="cuiValue"]` | `12345678` | Pole zawiera podaną wartość. |
| 4 | Wypełnij pole Registration Number. | `input[formControlName="regCom"]` | `J40/123/2026` | Pole zawiera podaną wartość. |
| 5 | Wypełnij pole Address. | `input[formControlName="address"]` | `Str. Test 1` | Pole zawiera podaną wartość. |
| 6 | Wypełnij pole County. | `input[formControlName="county"]` | `Bucuresti` | Pole zawiera podaną wartość. |
| 7 | Wypełnij pole City. | `input[formControlName="city"]` | `Bucuresti` | Pole zawiera podaną wartość. |
| 8 | Kliknij Submit. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista klientów zostaje odświeżona. |
| 9 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Firm added successfully`. |

---

## 5. Scenariusz: Edycja klienta

**Typ:** Happy Path  
**Cel:** Weryfikacja edycji klienta przez kliknięcie wiersza.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz klienta. | `tr[mat-row]` | N/D | Otwiera się dialog `Edit Client`. |
| 2 | Sprawdź dane formularza. | `input[formControlName="firmName"]` | N/D | Formularz zawiera dane klikniętego klienta. |
| 3 | Zmień pole City. | `input[formControlName="city"]` | `Cluj-Napoca` | Pole zawiera nową wartość. |
| 4 | Kliknij Update. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista klientów zostaje odświeżona. |
| 5 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Firm details updated successfully`. |

---

## 6. Scenariusz: Anulowanie edycji klienta

**Typ:** Functional  
**Cel:** Weryfikacja zamknięcia dialogu edycji bez zapisu.  
**Warunek wstępny:** Dialog `Edit Client` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zmień wartość pola Firm Name. | `input[formControlName="firmName"]` | `Nazwa tymczasowa` | Pole zawiera wartość tymczasową. |
| 2 | Kliknij Cancel. | `button mat-stroked-button` | N/D | Dialog zamyka się z wynikiem `false`. |
| 3 | Sprawdź grid. | `table[mat-table]` | N/D | Lista nie jest odświeżana przez `afterClosed()` dla wyniku `false`. |

---

## 7. Scenariusz: Usunięcie zaznaczonych klientów

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji Delete selected.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie usunięcia.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest operacja usunięcia zaznaczonych identyfikatorów. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Firms deleted successfully`. |
| 5 | Sprawdź grid. | `table[mat-table]` | N/D | Lista klientów zostaje odświeżona. |

---

## 8. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja walidacji `Validators.required`.  
**Warunek wstępny:** Dialog `New Client` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Pozostaw pole Firm Name puste i opuść pole. | `input[formControlName="firmName"]` | Pusty tekst | Widoczny jest komunikat `Firm Name is required`. |
| 2 | Pozostaw pole CUI Value puste i opuść pole. | `input[formControlName="cuiValue"]` | Pusty tekst | Widoczny jest komunikat `CUI Value is required`. |
| 3 | Pozostaw pole RegCom puste i opuść pole. | `input[formControlName="regCom"]` | Pusty tekst | Widoczny jest komunikat `Registration Number is required`. |
| 4 | Pozostaw pole Address puste i opuść pole. | `input[formControlName="address"]` | Pusty tekst | Widoczny jest komunikat `Address is required`. |
| 5 | Pozostaw pole County puste i opuść pole. | `input[formControlName="county"]` | Pusty tekst | Widoczny jest komunikat `County is required`. |
| 6 | Pozostaw pole City puste i opuść pole. | `input[formControlName="city"]` | Pusty tekst | Widoczny jest komunikat `City is required`. |
| 7 | Kliknij Submit przy pustym formularzu. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane, ponieważ `firmDetailsForm.invalid` kończy `onSubmit()` przez `return`. |

---

## 9. Scenariusz: Pobranie danych z ANAF

**Typ:** Functional  
**Cel:** Weryfikacja autouzupełniania pól dialogu.  
**Warunek wstępny:** Dialog `New Client` lub `Edit Client` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wpisz wartość w pole CUI Value. | `input[formControlName="cuiValue"]` | `47362945` | Pole zawiera wartość CUI. |
| 2 | Kliknij ikonę cloud_download. | `button[matSuffix] mat-icon` | N/D | Wywołana jest metoda `onCloudIconClick()`. |
| 3 | Poczekaj na odpowiedź. | Formularz dialogu | N/D | Pola `firmName`, `regCom`, `address`, `county`, `city` są uzupełnione z odpowiedzi. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Firm details fetched from ANAF`. |

---

## 10. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Clients. | URL `/dashboard/clients` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 11. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid klientów | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Nagłówek gridu | `tr[mat-header-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Przycisk New client | `button[mat-raised-button][color="primary"]` w `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Delete selected | `button[mat-menu-item]` |
| Paginator | `mat-paginator` |
| Pole Firm Name | `input[formControlName="firmName"]` |
| Pole CUI Value | `input[formControlName="cuiValue"]` |
| Pole RegCom | `input[formControlName="regCom"]` |
| Pole Address | `input[formControlName="address"]` |
| Pole County | `input[formControlName="county"]` |
| Pole City | `input[formControlName="city"]` |
| Komunikat walidacji | `mat-error` |
| Komunikat toast | `.toast-success`, `.toast-error` |

---

## 12. Dane testowe

### 12.1 Dane poprawne

```json
{
  "id": 0,
  "name": "ACME TEST S.R.L.",
  "cui": "12345678",
  "regCom": "J40/123/2026",
  "address": "Str. Test 1",
  "county": "Bucuresti",
  "city": "Bucuresti"
}
```

### 12.2 Dane niepoprawne

```json
{
  "id": 0,
  "name": "",
  "cui": "",
  "regCom": "",
  "address": "",
  "county": "",
  "city": ""
}
```
