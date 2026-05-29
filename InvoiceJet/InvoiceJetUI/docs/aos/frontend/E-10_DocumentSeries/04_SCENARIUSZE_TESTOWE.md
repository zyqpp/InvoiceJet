# Document Series — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy serii dokumentów

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje grid serii dokumentów.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jedną serię.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Document Series. | URL `/dashboard/document-series` | N/D | Ekran Document Series jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze serii dokumentów. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Document Type`, `Series Name`, `First Number`, `Current Number`, `Is Default`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie serii dokumentów

**Typ:** Functional  
**Cel:** Weryfikacja działania pola Search.  
**Warunek wstępny:** Ekran Document Series zawiera kilka rekordów.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `Factura` | Grid wyświetla wiersze pasujące do filtra `Factura`. |
| 3 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Dodanie serii dokumentów

**Typ:** Happy Path  
**Cel:** Weryfikacja dodania serii przez dialog.  
**Warunek wstępny:** Użytkownik jest zalogowany. API przyjmuje żądanie dodania serii.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk New Series. | `button[mat-raised-button][color="primary"]` w `.app-header` | N/D | Otwiera się dialog `New Document Series`. |
| 2 | Wybierz Document Type. | `mat-select[formControlName="documentType"]` | `Factura` | Pole zawiera wartość `1`. |
| 3 | Wypełnij Series Name. | `input[formControlName="seriesName"]` | `FV` | Pole zawiera podaną wartość. |
| 4 | Wypełnij First Number. | `input[formControlName="firstNumber"]` | `1` | Pole zawiera podaną wartość. |
| 5 | Wypełnij Current Number. | `input[formControlName="currentNumber"]` | `1` | Pole zawiera podaną wartość. |
| 6 | Zaznacz Default. | `mat-checkbox[formControlName="isDefault"]` | N/D | Pole wyboru jest zaznaczone. |
| 7 | Kliknij Submit. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista serii zostaje odświeżona. |
| 8 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Document series added`. |

---

## 4. Scenariusz: Edycja serii dokumentów

**Typ:** Happy Path  
**Cel:** Weryfikacja edycji serii przez kliknięcie wiersza.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz serii. | `tr[mat-row]` | N/D | Otwiera się dialog `Edit Document Series`. |
| 2 | Sprawdź dane formularza. | `input[formControlName="seriesName"]` | N/D | Formularz zawiera dane klikniętej serii. |
| 3 | Zmień Current Number. | `input[formControlName="currentNumber"]` | `2` | Pole zawiera nową wartość. |
| 4 | Kliknij Update. | `button[type="submit"]` | N/D | Dialog zamyka się po sukcesie. Lista serii zostaje odświeżona. |
| 5 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Document series updated`. |

---

## 5. Scenariusz: Usunięcie zaznaczonych serii

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji Delete selected.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie usunięcia.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest operacja usunięcia zaznaczonych identyfikatorów. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Document series deleted successfully.` |
| 5 | Sprawdź grid. | `table[mat-table]` | N/D | Lista serii zostaje odświeżona. |

---

## 6. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja walidacji `Validators.required`.  
**Warunek wstępny:** Dialog `New Document Series` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Nie wybieraj Document Type. | `mat-select[formControlName="documentType"]` | `null` | Widoczny jest komunikat `Document Type is required`. |
| 2 | Pozostaw Series Name puste. | `input[formControlName="seriesName"]` | Pusty tekst | Widoczny jest komunikat `Series Name is required`. |
| 3 | Pozostaw First Number puste. | `input[formControlName="firstNumber"]` | Pusty tekst | Widoczny jest komunikat `First Number is required`. |
| 4 | Pozostaw Current Number puste. | `input[formControlName="currentNumber"]` | Pusty tekst | Widoczny jest komunikat `Current Number is required`. |
| 5 | Kliknij Submit przy niepoprawnym formularzu. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. Widoczny jest tekst `Please fill in all required fields.` |

---

## 7. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Document Series. | URL `/dashboard/document-series` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 8. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid serii dokumentów | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Przycisk New Series | `button[mat-raised-button][color="primary"]` w `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Delete selected | `button[mat-menu-item]` |
| Paginator | `mat-paginator` |
| Pole Document Type | `mat-select[formControlName="documentType"]` |
| Pole Series Name | `input[formControlName="seriesName"]` |
| Pole First Number | `input[formControlName="firstNumber"]` |
| Pole Current Number | `input[formControlName="currentNumber"]` |
| Pole Default | `mat-checkbox[formControlName="isDefault"]` |
| Komunikat walidacji | `mat-error`, `.p-error` |
| Komunikat toast | `.toast-success`, `.toast-error` |

---

## 9. Dane testowe

### 9.1 Dane poprawne

```json
{
  "id": 0,
  "seriesName": "FV",
  "firstNumber": 1,
  "currentNumber": 1,
  "isDefault": true,
  "documentType": {
    "id": 1,
    "name": "Factura"
  }
}
```

### 9.2 Dane niepoprawne

```json
{
  "id": null,
  "documentType": null,
  "seriesName": "",
  "firstNumber": "",
  "currentNumber": "",
  "isDefault": false
}
```
