# Products — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy produktów

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje grid produktów.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jeden rekord produktu.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Products. | URL `/dashboard/products` | N/D | Ekran Products jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze produktów. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Name`, `Price`, `Unit of Measurement`, `TVA Value`, `TVA Included`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie produktów

**Typ:** Functional  
**Cel:** Weryfikacja działania pola Search.  
**Warunek wstępny:** Ekran Products zawiera kilka rekordów.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `service` | Grid wyświetla wiersze pasujące do filtra `service`. |
| 3 | Sprawdź przycisk Clear. | `button[aria-label="Clear"]` | N/D | Przycisk Clear jest widoczny. |
| 4 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Sortowanie gridu

**Typ:** Functional  
**Cel:** Weryfikacja sortowania przez `mat-sort-header`.  
**Warunek wstępny:** Grid zawiera co najmniej dwa rekordy.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij nagłówek kolumny Name. | `th[mat-sort-header]` | N/D | Grid sortuje wiersze po kolumnie `name`. |
| 2 | Kliknij nagłówek kolumny Price. | `th[mat-sort-header]` | N/D | Grid sortuje wiersze po kolumnie `price`. |
| 3 | Kliknij nagłówek kolumny TVA Value. | `th[mat-sort-header]` | N/D | Grid sortuje wiersze po kolumnie `tvaValue`. |

---

## 4. Scenariusz: Dodanie produktu

**Typ:** Happy Path  
**Cel:** Weryfikacja dodania produktu przez dialog.  
**Warunek wstępny:** Użytkownik jest zalogowany. API przyjmuje żądanie dodania produktu.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk New Product. | `button[mat-raised-button][color="primary"]` w `.app-header` | N/D | Otwiera się dialog `New Product`. |
| 2 | Wypełnij pole Name. | `input[formControlName="name"]` | `Consulting service` | Pole zawiera podaną wartość. |
| 3 | Wypełnij pole Price. | `input[formControlName="price"]` | `100` | Pole zawiera podaną wartość. |
| 4 | Wypełnij pole Unit of Measurement. | `input[formControlName="unitOfMeasurement"]` | `hour` | Pole zawiera podaną wartość. |
| 5 | Wypełnij pole TVA Value. | `input[formControlName="tvaValue"]` | `19` | Pole zawiera podaną wartość. |
| 6 | Zaznacz Contains TVA. | `mat-checkbox[formControlName="containsTva"]` | N/D | Pole wyboru jest zaznaczone. |
| 7 | Kliknij Submit. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista produktów zostaje odświeżona. |
| 8 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Product added successfully!`. |

---

## 5. Scenariusz: Edycja produktu

**Typ:** Happy Path  
**Cel:** Weryfikacja edycji produktu przez kliknięcie wiersza.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz produktu. | `tr[mat-row]` | N/D | Otwiera się dialog `Edit Product`. |
| 2 | Sprawdź dane formularza. | `input[formControlName="name"]` | N/D | Formularz zawiera dane klikniętego produktu. |
| 3 | Zmień pole Price. | `input[formControlName="price"]` | `120` | Pole zawiera nową wartość. |
| 4 | Kliknij Update. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista produktów zostaje odświeżona. |
| 5 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Product updated successfully!`. |

---

## 6. Scenariusz: Anulowanie edycji produktu

**Typ:** Functional  
**Cel:** Weryfikacja zamknięcia dialogu edycji bez zapisu.  
**Warunek wstępny:** Dialog `Edit Product` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zmień wartość pola Name. | `input[formControlName="name"]` | `Nazwa tymczasowa` | Pole zawiera wartość tymczasową. |
| 2 | Kliknij Cancel. | `button[mat-stroked-button]` | N/D | Dialog zamyka się z wynikiem `false`. |
| 3 | Sprawdź grid. | `table[mat-table]` | N/D | Lista nie jest odświeżana przez `afterClosed()` dla wyniku `false`. |

---

## 7. Scenariusz: Usunięcie zaznaczonych produktów

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji Delete selected.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie usunięcia.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest operacja usunięcia zaznaczonych identyfikatorów. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Products deleted successfully!`. |
| 5 | Sprawdź grid. | `table[mat-table]` | N/D | Lista produktów zostaje odświeżona. |

---

## 8. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja walidacji `Validators.required`.  
**Warunek wstępny:** Dialog `New Product` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Pozostaw pole Name puste i opuść pole. | `input[formControlName="name"]` | Pusty tekst | Widoczny jest komunikat `Name is required`. |
| 2 | Pozostaw pole Price puste i opuść pole. | `input[formControlName="price"]` | Pusty tekst | Widoczny jest komunikat `Price is required`. |
| 3 | Usuń wartość pola TVA Value. | `input[formControlName="tvaValue"]` | Pusty tekst | Formularz jest niepoprawny. |
| 4 | Kliknij Submit przy niepoprawnym formularzu. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. Widoczny jest tekst `Please fill in all required fields.` |

---

## 9. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Products. | URL `/dashboard/products` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 10. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid produktów | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Nagłówek gridu | `tr[mat-header-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Przycisk New Product | `button[mat-raised-button][color="primary"]` w `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Delete selected | `button[mat-menu-item]` |
| Paginator | `mat-paginator` |
| Pole Name | `input[formControlName="name"]` |
| Pole Price | `input[formControlName="price"]` |
| Pole Unit of Measurement | `input[formControlName="unitOfMeasurement"]` |
| Pole TVA Value | `input[formControlName="tvaValue"]` |
| Pole Contains TVA | `mat-checkbox[formControlName="containsTva"]` |
| Komunikat walidacji | `mat-error`, `.p-error` |
| Komunikat toast | `.toast-success`, `.toast-error` |

---

## 11. Dane testowe

### 11.1 Dane poprawne

```json
{
  "id": 0,
  "name": "Consulting service",
  "price": 100,
  "containsTva": true,
  "unitOfMeasurement": "hour",
  "tvaValue": 19
}
```

### 11.2 Dane niepoprawne

```json
{
  "id": 0,
  "name": "",
  "price": "",
  "containsTva": false,
  "unitOfMeasurement": "",
  "tvaValue": ""
}
```
