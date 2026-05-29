# Bank Accounts — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy kont bankowych

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje grid kont bankowych.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jedno konto bankowe.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Bank Accounts. | URL `/dashboard/bank-accounts` | N/D | Ekran Bank Accounts jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze kont bankowych. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Bank Name`, `IBAN`, `Currency`, `Active`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie kont bankowych

**Typ:** Functional  
**Cel:** Weryfikacja działania pola Search.  
**Warunek wstępny:** Ekran Bank Accounts zawiera kilka rekordów.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `bank` | Grid wyświetla wiersze pasujące do filtra `bank`. |
| 3 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Dodanie konta bankowego

**Typ:** Happy Path  
**Cel:** Weryfikacja dodania konta przez dialog.  
**Warunek wstępny:** Użytkownik jest zalogowany. API przyjmuje żądanie dodania konta.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk New Account. | `button[mat-raised-button][color="primary"]` w `.app-header` | N/D | Otwiera się dialog `New Bank Account`. |
| 2 | Wypełnij pole Bank Name. | `input[formControlName="bankName"]` | `Banca Test` | Pole zawiera podaną wartość. |
| 3 | Wypełnij pole IBAN. | `input[formControlName="iban"]` | `RO49AAAA1B31007593840000` | Pole zawiera podaną wartość. |
| 4 | Wybierz walutę. | `mat-select[formControlName="currency"]` | `RON` | Pole `currency` zawiera wartość `0`. |
| 5 | Zaznacz Active. | `mat-checkbox[formControlName="isActive"]` | N/D | Pole wyboru jest zaznaczone. |
| 6 | Kliknij Submit. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista kont zostaje odświeżona. |
| 7 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Bank account added`. |

---

## 4. Scenariusz: Edycja konta bankowego

**Typ:** Happy Path  
**Cel:** Weryfikacja edycji konta przez kliknięcie wiersza.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz konta. | `tr[mat-row]` | N/D | Otwiera się dialog `Edit Bank Account`. |
| 2 | Sprawdź dane formularza. | `input[formControlName="bankName"]` | N/D | Formularz zawiera dane klikniętego konta. |
| 3 | Zmień pole Bank Name. | `input[formControlName="bankName"]` | `Banca Test Updated` | Pole zawiera nową wartość. |
| 4 | Kliknij Update. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista kont zostaje odświeżona. |
| 5 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Bank account updated`. |

---

## 5. Scenariusz: Usunięcie zaznaczonych kont

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji Delete selected.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie usunięcia.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest operacja usunięcia zaznaczonych identyfikatorów. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Bank accounts deleted successfully.` |
| 5 | Sprawdź grid. | `table[mat-table]` | N/D | Lista kont zostaje odświeżona. |

---

## 6. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja walidacji `Validators.required`.  
**Warunek wstępny:** Dialog `New Bank Account` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Pozostaw pole Bank Name puste i opuść pole. | `input[formControlName="bankName"]` | Pusty tekst | Widoczny jest komunikat `Bank Name is required`. |
| 2 | Pozostaw pole IBAN puste i opuść pole. | `input[formControlName="iban"]` | Pusty tekst | Widoczny jest komunikat `IBAN is required`. |
| 3 | Nie wybieraj waluty. | `mat-select[formControlName="currency"]` | `null` | Widoczny jest komunikat `Currency is required`. |
| 4 | Kliknij Submit przy niepoprawnym formularzu. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. Widoczny jest tekst `Please fill in all required fields.` |

---

## 7. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Bank Accounts. | URL `/dashboard/bank-accounts` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 8. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid kont bankowych | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Przycisk New Account | `button[mat-raised-button][color="primary"]` w `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Delete selected | `button[mat-menu-item]` |
| Paginator | `mat-paginator` |
| Pole Bank Name | `input[formControlName="bankName"]` |
| Pole IBAN | `input[formControlName="iban"]` |
| Pole Currency | `mat-select[formControlName="currency"]` |
| Pole Active | `mat-checkbox[formControlName="isActive"]` |
| Komunikat walidacji | `mat-error`, `.p-error` |
| Komunikat toast | `.toast-success`, `.toast-error` |

---

## 9. Dane testowe

### 9.1 Dane poprawne

```json
{
  "id": 0,
  "bankName": "Banca Test",
  "iban": "RO49AAAA1B31007593840000",
  "currency": 0,
  "isActive": true
}
```

### 9.2 Dane niepoprawne

```json
{
  "id": 0,
  "bankName": "",
  "iban": "",
  "currency": null,
  "isActive": false
}
```
