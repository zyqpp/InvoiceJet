# [NAZWA_EKRANU] — Scenariusze Testowe

**Przeznaczenie**: Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: [Nazwa scenariusza głównego — golden path]

**Typ**: Happy Path  
**Cel**: [Co powinno zostać osiągnięte]  
**Warunek wstępny**: [Stan systemu przed testem — zalogowany użytkownik, dane w bazie, itp.]

### Kroki testowe

| Lp. | Akcja | Selektor / Element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Nawiguj do ekranu | URL: `/[ścieżka]` | N/A | Ekran załadowany, grid/formularz widoczny |
| 2 | [Opis akcji] | Przycisk [Nazwa] / element `[selektor CSS]` | [Dane] | [Rezultat] |
| 3 | Kliknij przycisk Edycja | Icon button w wierszu / `button[aria-label="edit"]` | N/A | Dialog edycji otwarty z danymi rekordu |
| 4 | Zmień pole [Nazwa] | Input field `[formControlName="fieldName"]` / `input[name="fieldName"]` | "Nowa wartość" | Pole zaktualizowane bez błędów walidacji |
| 5 | Kliknij przycisk Zapis | `button:contains("Zapisz")` / `[data-test="save-btn"]` | N/A | Dialog zamknięty, lista odświeżona, komunikat sukcesu wyświetlony |
| 6 | Verify dane zmieniona | Grid `<mat-table>` / selector `.data-table tr` | N/A | Nowa wartość widoczna w wierszu tabeli |

### Asercje (assertions)

```gherkin
Given użytkownik jest zalogowany i nawiguje do ekranu [nazwa]
When użytkownik kliknie przycisk [Nazwa]
Then dialog powinien otworzyć się z formularzem
And przycisk Zapis powinien być disabled dopóki formularz nie będzie valid
And po wypełnieniu pól i kliknięciu Zapis, dialog zamknie się
And lista powinna być odświeżona z nowymi danymi
And komunikat "[tekst]" powinien się pojawić przez [n] sekund
```

---

## 2. Scenariusz: [Nazwa scenariusza — test walidacji]

**Typ**: Validation Test  
**Cel**: Weryfikacja, że walidacja pól działa poprawnie  
**Warunek wstępny**: [Dialog edycji otwarty]

### Kroki testowe

| Lp. | Akcja | Selektor | Dane | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zostaw pole [Nazwa] puste | Input `[formControlName="[fieldName]"]` | N/A (brak danych) | Komunikat błędu "[tekst]" pojawia się pod polem |
| 2 | Wpisz wartość za krótką | Input | "abc" (jeśli min 5 znaków) | Błąd: "Minimalna długość: 5 znaków" |
| 3 | Wpisz wartość w zły format | Input `[pattern="..."]` | "abc123" (jeśli pattern: `[0-9]+`) | Błąd: "[tekst pattern error]" |
| 4 | Przycisk Zapis | Button | N/A | Przycisk pozostaje disabled |
| 5 | Popraw wartość | Input | "Poprawna wartość" | Błąd znika, przycisk Zapis aktywny |
| 6 | Kliknij Zapis | Button | N/A | Dane zapisane, dialog zamknięty |

---

## 3. Scenariusz: [Nazwa scenariusza — obsługa błędu API]

**Typ**: Error Handling  
**Cel**: Weryfikacja obsługi błędów z serwera  
**Warunek wstępny**: [Symulacja błędu API 400/500]

### Kroki testowe

| Lp. | Akcja | Selektor | Dane | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przygotuj formularz | Form | Dane prowadzące do błędu API (np. email istnieje) | Formularz wypełniony poprawnie |
| 2 | Kliknij Zapis | Button | N/A | Request wysłany do API |
| 3 | Serwer zwraca 400 Bad Request | Mock API | `{ error: "Email already exists" }` | Komunikat błędu wyświetlony |
| 4 | Verify komunikatu | MatSnackBar / `div[role="alert"]` | N/A | Tekst błędu widoczny: "[tekst z API]" |
| 5 | Formularz pozostaje otwarty | Dialog | N/A | Użytkownik może edytować i spróbować ponownie |

---

## 4. Scenariusz: [Nazwa scenariusza — permissioning / access control]

**Typ**: Access Control  
**Cel**: Weryfikacja, że tylko uprawnieni użytkownicy mogą wykonać operacje  
**Warunek wstępny**: [Użytkownik z ograniczoną rolą]

### Kroki testowe

| Lp. | Akcja | Selektor | Dane | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zaloguj się jako [Rola bez uprawnień] | Login form | user: "viewer", pass: "..." | Zalogowanie udane |
| 2 | Nawiguj do `/[ścieżka]` | URL bar | N/A | Ekran załadowany (jeśli dostępny) |
| 3 | Spróbuj kliknąć Edycja | Button (disabled) | N/A | Przycisk jest disabled / niewidoczny |
| 4 | Spróbuj zmienić wartość | Input | "test" | Input jest readonly / disabled |
| 5 | Spróbuj kliknąć Zapis | Button (disabled/hidden) | N/A | Przycisk niedostępny / komunikat "Brak uprawnień" |

---

## 5. Scenariusz: [Edge case — brak danych / pusty stan]

**Typ**: Edge Case  
**Cel**: Weryfikacja zachowania ekranu bez danych  
**Warunek wstępny**: [Baza danych pusta lub żaden rekord nie spełnia filtrów]

### Kroki testowe

| Lp. | Akcja | Selektor | Dane | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Otwórz ekran `[nazwa]` | URL | `/[ścieżka]` | Ekran załadowany |
| 2 | Baza jest pusta | [Brak danych API] | N/A | Komunikat "Brak danych do wyświetlenia" / empty state |
| 3 | Verify UI | [pusta lista] | N/A | Grid pusty, bez zawieszenia się interfejsu |
| 4 | Przycisk Edycja | Button | N/A | Niewidoczny / disabled (bo brak wierszy) |
| 5 | Przycisk Dodaj | Button | N/A | Dostępny, pozwala na dodanie pierwszego rekordu |

---

## 6. Tabela selektorów i lokalizatorów

**Dla automatyzacji QA / E2E tests (Cypress, Protractor, Playwright, itp.)**

| Element | Selektor CSS | Atrybut aria / data-* | XPath |
|---|---|---|---|
| Przycisk [Nazwa] | `button.btn-primary` / `button[class*="primary"]` | `[data-test="btn-save"]` / `[aria-label="Save"]` | `//button[contains(text(), "Zapisz")]` |
| Input pole [Nazwa] | `input[formControlName="fieldName"]` | `[data-test="input-name"]` | `//input[@name="fieldName"]` |
| Grid | `<mat-table>` | `[data-test="firms-grid"]` | `//mat-table` |
| Dialog [Nazwa] | `<mat-dialog-container>` | N/A | `//div[contains(@role, "dialog")]` |
| Komunikat błędu | `<mat-error>` / `<div class="error-message">` | `[data-test="error-msg"]` | `//mat-error` |

---

## 7. Dane testowe (fixtures)

### Zestaw 1: Dane prawidłowe

```json
{
  "name": "Firma Testowa",
  "cui": "1234567890123",
  "regCom": "J40/1234/2023",
  "email": "contact@test.com",
  "phone": "+40123456789"
}
```

### Zestaw 2: Dane z błędami walidacji

```json
{
  "name": "",  // Wymagane
  "cui": "12345",  // Za krótkie (wymagane 13)
  "email": "invalid-email",  // Zły format
  "phone": "abc"  // Powinny być cyfry
}
```

### Zestaw 3: Dane edge case

```json
{
  "name": "Firma z bardzo długą nazwą która zawiera znaki specjalne !@#$%^&*()",
  "cui": "0000000000000",  // Najmniejsza wartość
  "email": "test+alias@domain.co.uk"  // Kompleksowy email
}
```

---

## 8. Performance i Load Testing (opcjonalnie)

- **Liczba rekordów do testowania**: [100 / 1000 / 10000]
- **Czasy ładowania**:
  - Ekran powinien załadować się w < [n]ms
  - Grid powinien renderować w < [n]ms
- **Responsywność**: Kliknięcia przycisku powinny być obsługiwane w < [n]ms

---

## 9. Notatki dla testerów

- Testuj na браuzерach: Chrome, Firefox, Safari, Edge
- Testuj na urządzeniach: Desktop, Tablet (iPad), Mobile (iPhone)
- Testuj Internet Explorer 11 (jeśli wymagane)
- Skopiuj token JWT z Local Storage aby testować offline jeśli potrzeba
- Zrzuć screeny błędów do raportów
- W przypadku znalezienia buga — użyj tego template do raportu
