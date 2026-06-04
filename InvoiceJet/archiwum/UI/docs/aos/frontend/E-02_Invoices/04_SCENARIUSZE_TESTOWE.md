# Invoices — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy faktur

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje grid faktur.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jedną fakturę.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Invoices. | URL `/dashboard/invoices` | N/D | Ekran Invoices jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze faktur. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Document Number`, `Client Name`, `Issue Date`, `Due Date`, `Total Value`, `Status`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie faktur

**Typ:** Functional  
**Cel:** Weryfikacja działania pola Search.  
**Warunek wstępny:** Ekran Invoices zawiera kilka rekordów.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `FV` | Grid wyświetla wiersze pasujące do filtra `FV`. |
| 3 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Przejście do nowej faktury

**Typ:** Navigation  
**Cel:** Weryfikacja nawigacji do formularza dodawania faktury.  
**Warunek wstępny:** Użytkownik jest na ekranie Invoices.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk New Invoice. | `button[mat-raised-button][color="primary"]` w `.app-header` | N/D | Router przechodzi do `dashboard/add-invoice`. |
| 2 | Sprawdź komponent docelowy. | URL przeglądarki | N/D | Widoczny jest ekran dodawania faktury. |

---

## 4. Scenariusz: Przejście do edycji faktury

**Typ:** Navigation  
**Cel:** Weryfikacja nawigacji po kliknięciu wiersza.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz faktury. | `tr[mat-row]` | N/D | Wywołana jest metoda `openEditInvoiceDialog(row)`. |
| 2 | Sprawdź trasę. | URL przeglądarki | `row.id` | Router przechodzi do `/dashboard/edit-invoice/{id}`. |

---

## 5. Scenariusz: Usunięcie zaznaczonych faktur

**Typ:** Functional  
**Cel:** Weryfikacja operacji Delete selected.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie usunięcia.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest metoda `deleteSelected()`. |
| 4 | Poczekaj na odpowiedź API. | `table[mat-table]` | N/D | Lista faktur zostaje pobrana ponownie. |

---

## 6. Scenariusz: Transformacja do storna

**Typ:** Functional  
**Cel:** Weryfikacja operacji Transform to storno.  
**Warunek wstępny:** Grid zawiera co najmniej jeden rekord. API przyjmuje żądanie transformacji.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Transform to storno` jest widoczne. |
| 3 | Kliknij Transform to storno. | `button[mat-menu-item]` | N/D | Wywołana jest metoda `transformToStorno()`. |
| 4 | Poczekaj na odpowiedź API. | `table[mat-table]` | N/D | Lista faktur zostaje pobrana ponownie. |

---

## 7. Scenariusz: Operacja bez zaznaczenia

**Typ:** Negative  
**Cel:** Weryfikacja znanej uwagi wynikającej z kodu.  
**Warunek wstępny:** Brak zaznaczonych wierszy.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu jest widoczne. |
| 2 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Komponent wywołuje `DocumentService.deleteDocuments([])`. |
| 3 | Kliknij Transform to storno. | `button[mat-menu-item]` | N/D | Komponent wywołuje `DocumentService.transformToStorno([])`. |

---

## 8. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Invoices. | URL `/dashboard/invoices` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 9. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid faktur | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Przycisk New Invoice | `button[mat-raised-button][color="primary"]` w `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Transform to storno | `button[mat-menu-item]` z ikoną `swap_vert` |
| Przycisk Delete selected | `button[mat-menu-item]` z ikoną `delete` |
| Paginator | `mat-paginator` |
| Status dokumentu | `mat-chip` |
| Checkbox wiersza | `td mat-checkbox` |

---

## 10. Dane testowe

### 10.1 Przykładowy rekord gridu

```json
{
  "id": 1,
  "documentNumber": "FV-0001",
  "clientName": "ACME TEST S.R.L.",
  "issueDate": "2026-05-29",
  "dueDate": "2026-06-12",
  "totalValue": 119,
  "documentStatus": {
    "id": 1,
    "status": "Draft"
  }
}
```

### 10.2 Pusta lista identyfikatorów

```json
[]
```
