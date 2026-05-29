# Dashboard — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie dashboardu

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran ładuje karty statystyk i wykres.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca poprawny obiekt `IDashboardStats`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Dashboard. | URL `/dashboard` | N/D | Ekran Dashboard jest widoczny. |
| 2 | Sprawdź karty statystyk. | `mat-card` | N/D | Widoczne są karty `Clients`, `Bank Accounts`, `Documents`, `Products`. |
| 3 | Sprawdź sekcję Overview. | `.graph-container` | N/D | Widoczny jest nagłówek `Overview`. |
| 4 | Sprawdź wykres. | `canvas[baseChart]` | N/D | Wykres jest renderowany. |

---

## 2. Scenariusz: Zmiana roku

**Typ:** Functional  
**Cel:** Weryfikacja odświeżenia danych po zmianie pola Year.  
**Warunek wstępny:** Ekran Dashboard jest załadowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz listę Year. | `mat-select` z etykietą `Year` | N/D | Lista lat jest widoczna. |
| 2 | Wybierz inny rok. | `mat-option` | Rok z listy | Wywołana jest metoda `onSelectionChange()`. |
| 3 | Poczekaj na odpowiedź API. | Karty i wykres | N/D | Karty i wykres pokazują dane dla wybranego roku. |

---

## 3. Scenariusz: Zmiana typu dokumentu

**Typ:** Functional  
**Cel:** Weryfikacja odświeżenia danych po zmianie pola Document Type.  
**Warunek wstępny:** Ekran Dashboard jest załadowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz listę Document Type. | `mat-select` z etykietą `Document Type` | N/D | Widoczne są opcje `Factura`, `Factura Proforma`, `Factura Storno`. |
| 2 | Wybierz `Factura Proforma`. | `mat-option` | `Factura Proforma` | Wywołana jest metoda `onSelectionChange()`. |
| 3 | Poczekaj na odpowiedź API. | `canvas[baseChart]` | N/D | Wykres pokazuje dane dla typu dokumentu `2`. |

---

## 4. Scenariusz: Dane miesięczne z brakami

**Typ:** Functional  
**Cel:** Weryfikacja, że miesiące bez danych mają wartość `0`.  
**Warunek wstępny:** API zwraca `monthlyTotals` bez części miesięcy.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Załaduj ekran Dashboard. | URL `/dashboard` | Odpowiedź API z niepełną listą miesięcy | `updateChartData(...)` tworzy tablice długości `12`. |
| 2 | Sprawdź wykres. | `canvas[baseChart]` | N/D | Brakujące miesiące mają wartość `0` w seriach wykresu. |

---

## 5. Scenariusz: Brak `monthlyTotals` w odpowiedzi API

**Typ:** Negative  
**Cel:** Weryfikacja znanej uwagi wynikającej z kodu.  
**Warunek wstępny:** API zwraca `IDashboardStats` bez pola `monthlyTotals`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Załaduj ekran Dashboard. | URL `/dashboard` | Odpowiedź bez `monthlyTotals` | `updateChartData(...)` otrzymuje `undefined`. |
| 2 | Obserwuj konsolę przeglądarki. | DevTools Console | N/D | Występuje błąd wykonania przy `monthlyTotals.forEach(...)`. |

---

## 6. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Dashboard. | URL `/dashboard` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 7. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Kontener statystyk | `.stats-container` |
| Pasek tytułu | `.app-header` |
| Karty statystyk | `mat-card` |
| Sekcja wykresu | `.graph-container` |
| Nagłówek Overview | `.overview-text` |
| Lista Year | `mat-select` z etykietą `Year` |
| Lista Document Type | `mat-select` z etykietą `Document Type` |
| Wykres | `canvas[baseChart]` |

---

## 8. Dane testowe

### 8.1 Przykładowa odpowiedź poprawna

```json
{
  "totalDocuments": 10,
  "totalClients": 4,
  "totalProducts": 7,
  "totalBankAccounts": 2,
  "monthlyTotals": [
    { "month": 1, "invoiceAmount": 1000, "incomeAmount": 800 },
    { "month": 2, "invoiceAmount": 2000, "incomeAmount": 1500 }
  ]
}
```

### 8.2 Przykładowa odpowiedź ryzykowna

```json
{
  "totalDocuments": 10,
  "totalClients": 4,
  "totalProducts": 7,
  "totalBankAccounts": 2
}
```
