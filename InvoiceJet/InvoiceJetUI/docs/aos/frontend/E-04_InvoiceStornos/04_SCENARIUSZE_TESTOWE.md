# Invoice Stornos — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie listy dokumentów storno

**Typ:** Happy Path
**Cel:** Weryfikacja, że ekran ładuje grid dokumentów storno.
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca co najmniej jeden dokument storno.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Invoice Stornos. | URL `/dashboard/invoice-stornos` | N/D | Ekran Invoice Stornos jest widoczny. |
| 2 | Poczekaj na załadowanie danych. | `table[mat-table]` | N/D | Grid renderuje wiersze dokumentów storno. |
| 3 | Sprawdź nagłówki kolumn. | `th[mat-header-cell]` | N/D | Widoczne są kolumny `Document Number`, `Client Name`, `Issue Date`, `Due Date`, `Total Value`, `Status`. |
| 4 | Sprawdź paginację. | `mat-paginator` | N/D | Widoczny jest paginator z opcjami `10`, `20`, `30`. |

---

## 2. Scenariusz: Filtrowanie dokumentów storno

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Search. | `input[placeholder="Search"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz tekst filtrowania. | `input[placeholder="Search"]` | `ST` | Grid wyświetla wiersze pasujące do filtra `ST`. |
| 3 | Kliknij przycisk Clear. | `button[aria-label="Clear"]` | N/D | Pole Search jest puste. Grid wraca do pełnej listy. |

---

## 3. Scenariusz: Przejście do edycji storna

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij wiersz dokumentu storno. | `tr[mat-row]` | N/D | Wywołana jest metoda `openEditInvoiceStornoDialog(row)`. |
| 2 | Sprawdź trasę. | URL przeglądarki | `row.id` | Router przechodzi do `/dashboard/edit-invoice-storno/{id}`. |

---

## 4. Scenariusz: Usunięcie zaznaczonych dokumentów storno

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaznacz checkbox wiersza. | `td mat-checkbox` | N/D | Wiersz jest zaznaczony. |
| 2 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu z opcją `Delete selected` jest widoczne. |
| 3 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Wywołana jest metoda `deleteSelected()`. |
| 4 | Poczekaj na odpowiedź API. | `table[mat-table]` | N/D | Lista dokumentów storno zostaje pobrana ponownie. |

---

## 5. Scenariusz: Operacja bez zaznaczenia

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz menu kontekstowe. | `button[mat-stroked-button] mat-icon` | N/D | Menu jest widoczne. |
| 2 | Kliknij Delete selected. | `button[mat-menu-item]` | N/D | Komponent wywołuje `DocumentService.deleteDocuments([])`. |

---

## 6. Scenariusz: Brak aktywnego przycisku dodawania

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz ekran Invoice Stornos. | URL `/dashboard/invoice-stornos` | N/D | Widoczny jest nagłówek ekranu. |
| 2 | Sprawdź pasek tytułu. | `.app-header` | N/D | Nie ma aktywnego przycisku `New Storno`. |

---

## 7. Scenariusz: Dostęp bez logowania

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Invoice Stornos. | URL `/dashboard/invoice-stornos` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 8. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Grid dokumentów storno | `table[mat-table]` |
| Wiersz gridu | `tr[mat-row]` |
| Pole Search | `input[placeholder="Search"]` |
| Przycisk Clear | `button[aria-label="Clear"]` |
| Pasek tytułu | `.app-header` |
| Menu kontekstowe | `mat-menu` |
| Przycisk Delete selected | `button[mat-menu-item]` |
| Paginator | `mat-paginator` |
| Status dokumentu | `mat-chip` |
| Checkbox wiersza | `td mat-checkbox` |

---

## 9. Dane testowe

```json
{
  "id": 1,
  "documentNumber": "ST-2026-001",
  "clientName": "ACME TEST S.R.L.",
  "issueDate": "2026-05-29",
  "dueDate": "2026-06-12",
  "totalValue": 1190,
  "documentStatus": {
    "id": 1,
    "status": "Draft"
  }
}
```
