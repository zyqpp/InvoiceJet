# Login — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie formularza logowania

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran publiczny renderuje formularz Login.  
**Warunek wstępny:** Aplikacja jest uruchomiona.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Login. | URL `/login` | N/D | Ekran Login jest widoczny. |
| 2 | Sprawdź kartę formularza. | `mat-card` | N/D | Widoczny jest tytuł `Login`. |
| 3 | Sprawdź pola formularza. | `form[formGroup]` | N/D | Widoczne są pola `Email` i `Password`. |
| 4 | Sprawdź menu boczne. | `app-sidebar` | N/D | Menu boczne nie jest renderowane. |

---

## 2. Scenariusz: Poprawne logowanie

**Typ:** Happy Path  
**Cel:** Weryfikacja zapisu tokenu i nawigacji po sukcesie.  
**Warunek wstępny:** API przyjmuje żądanie logowania i zwraca `{ "token": "..." }`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wypełnij Email. | `input[formControlName="email"]` | `jan@example.com` | Pole zawiera podaną wartość. |
| 2 | Wypełnij Password. | `input[formControlName="password"]` | `Test123!` | Pole zawiera podaną wartość. |
| 3 | Kliknij Submit. | `button[type="submit"]` | N/D | Wywołana jest metoda `AuthService.login(user)`. |
| 4 | Sprawdź token. | `localStorage.authToken` | N/D | Token z odpowiedzi jest zapisany. |
| 5 | Sprawdź trasę. | URL przeglądarki | N/D | Aplikacja przechodzi do `dashboard`. |

---

## 3. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja komunikatów `Validators.required`.  
**Warunek wstępny:** Ekran Login jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Pozostaw Email puste i opuść pole. | `input[formControlName="email"]` | Pusty tekst | Widoczny jest komunikat `Email is required`. |
| 2 | Pozostaw Password puste i opuść pole. | `input[formControlName="password"]` | Pusty tekst | Widoczny jest komunikat `Password is required`. |
| 3 | Kliknij Submit przy pustym formularzu. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. |

---

## 4. Scenariusz: Niepoprawny format email

**Typ:** Validation Test  
**Cel:** Weryfikacja znanej uwagi wynikającej z kodu.  
**Warunek wstępny:** Ekran Login jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wpisz niepoprawny email. | `input[formControlName="email"]` | `jan` | `loginForm.valid` ma wartość `false`. |
| 2 | Sprawdź komunikat. | `mat-error` przy polu Email | N/D | Brak osobnego komunikatu dla błędu `email`. |
| 3 | Kliknij Submit. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. |

---

## 5. Scenariusz: Przełączenie widoczności hasła

**Typ:** Functional  
**Cel:** Weryfikacja flagi `hide`.  
**Warunek wstępny:** Ekran Login jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Sprawdź typ pola Password. | `input[formControlName="password"]` | N/D | Typ pola to `password`. |
| 2 | Kliknij ikonę widoczności. | `button[mat-icon-button]` przy polu Password | N/D | Typ pola zmienia się na `text`. |
| 3 | Kliknij ikonę ponownie. | `button[mat-icon-button]` | N/D | Typ pola wraca do `password`. |

---

## 6. Scenariusz: Dostęp do Login z istniejącym tokenem

**Typ:** Functional  
**Cel:** Weryfikacja zachowania trasy publicznej.  
**Warunek wstępny:** `localStorage.authToken` zawiera token.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Login. | URL `/login` | N/D | Ekran Login jest renderowany. |
| 2 | Sprawdź przekierowanie automatyczne. | URL przeglądarki | N/D | Kod komponentu nie wykonuje przekierowania do dashboardu. |

---

## 7. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Formularz Login | `form[formGroup]` |
| Karta formularza | `mat-card` |
| Pole Email | `input[formControlName="email"]` |
| Pole Password | `input[formControlName="password"]` |
| Przycisk Submit | `button[type="submit"]` |
| Przycisk widoczności hasła | `button[mat-icon-button]` przy polu Password |
| Komunikat walidacji | `mat-error` |
| Komunikat błędu | `.p-error` |

---

## 8. Dane testowe

### 8.1 Dane poprawne

```json
{
  "email": "jan@example.com",
  "password": "Test123!"
}
```

### 8.2 Dane niepoprawne

```json
{
  "email": "jan",
  "password": ""
}
```
