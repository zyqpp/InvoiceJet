# Register — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Wyświetlenie formularza rejestracji

**Typ:** Happy Path  
**Cel:** Weryfikacja, że ekran publiczny renderuje formularz Register.  
**Warunek wstępny:** Aplikacja jest uruchomiona.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu Register. | URL `/register` | N/D | Ekran Register jest widoczny. |
| 2 | Sprawdź kartę formularza. | `mat-card` | N/D | Widoczny jest tytuł `Register`. |
| 3 | Sprawdź pola formularza. | `form[formGroup]` | N/D | Widoczne są pola `First Name`, `Last Name`, `Email`, `Password`, `Password Confirmation`. |
| 4 | Sprawdź menu boczne. | `app-sidebar` | N/D | Menu boczne nie jest renderowane. |

---

## 2. Scenariusz: Poprawna rejestracja

**Typ:** Happy Path  
**Cel:** Weryfikacja zapisu tokenu i nawigacji po sukcesie.  
**Warunek wstępny:** API przyjmuje żądanie rejestracji i zwraca `{ "token": "..." }`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wypełnij First Name. | `input[formControlName="firstName"]` | `Jan` | Pole zawiera podaną wartość. |
| 2 | Wypełnij Last Name. | `input[formControlName="lastName"]` | `Kowalski` | Pole zawiera podaną wartość. |
| 3 | Wypełnij Email. | `input[formControlName="email"]` | `jan@example.com` | Pole zawiera podaną wartość. |
| 4 | Wypełnij Password. | `input[formControlName="password"]` | `Test123!` | Pole zawiera podaną wartość. |
| 5 | Wypełnij Password Confirmation. | `input[formControlName="passwordConfirmation"]` | `Test123!` | Pole zawiera podaną wartość. |
| 6 | Kliknij Submit. | `button[type="submit"]` | N/D | Wywołana jest metoda `AuthService.register(user)`. |
| 7 | Sprawdź token. | `localStorage.authToken` | N/D | Token z odpowiedzi jest zapisany. |
| 8 | Sprawdź trasę. | URL przeglądarki | N/D | Aplikacja przechodzi do `dashboard`. |

---

## 3. Scenariusz: Walidacja wymaganych pól

**Typ:** Validation Test  
**Cel:** Weryfikacja komunikatów `Validators.required`.  
**Warunek wstępny:** Ekran Register jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Pozostaw First Name puste i opuść pole. | `input[formControlName="firstName"]` | Pusty tekst | Widoczny jest komunikat `First Name is required`. |
| 2 | Pozostaw Last Name puste i opuść pole. | `input[formControlName="lastName"]` | Pusty tekst | Widoczny jest komunikat `Last Name is required`. |
| 3 | Pozostaw Email puste i opuść pole. | `input[formControlName="email"]` | Pusty tekst | Widoczny jest komunikat `Email Name is required`. |
| 4 | Pozostaw Password puste i opuść pole. | `input[formControlName="password"]` | Pusty tekst | Widoczny jest komunikat `Password Name is required`. |
| 5 | Pozostaw Password Confirmation puste i opuść pole. | `input[formControlName="passwordConfirmation"]` | Pusty tekst | Widoczny jest komunikat `Password confirmation is required`. |
| 6 | Kliknij Submit przy pustym formularzu. | `button[type="submit"]` | N/D | `onSubmit()` kończy działanie przez `return`. Żądanie HTTP nie jest wykonywane. |

---

## 4. Scenariusz: Niepoprawny format email

**Typ:** Validation Test  
**Cel:** Weryfikacja znanej uwagi wynikającej z kodu.  
**Warunek wstępny:** Ekran Register jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wpisz niepoprawny email. | `input[formControlName="email"]` | `jan` | `registerForm.invalid` ma wartość `true`. |
| 2 | Sprawdź komunikat. | `mat-error` przy polu Email | N/D | Brak osobnego komunikatu dla błędu `email`. |
| 3 | Kliknij Submit. | `button[type="submit"]` | N/D | Żądanie HTTP nie jest wykonywane. |

---

## 5. Scenariusz: Różne wartości haseł

**Typ:** Negative  
**Cel:** Weryfikacja braku walidatora zgodności haseł w kodzie frontendu.  
**Warunek wstępny:** Ekran Register jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wypełnij Password. | `input[formControlName="password"]` | `Test123!` | Pole zawiera podaną wartość. |
| 2 | Wypełnij Password Confirmation inną wartością. | `input[formControlName="passwordConfirmation"]` | `Other123!` | Pole zawiera podaną wartość. |
| 3 | Sprawdź formularz. | `registerForm` | N/D | Formularz pozostaje poprawny po stronie frontendu, jeżeli pozostałe pola są poprawne. |

---

## 6. Scenariusz: Przełączenie widoczności hasła

**Typ:** Functional  
**Cel:** Weryfikacja flagi `hide`.  
**Warunek wstępny:** Ekran Register jest widoczny.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Sprawdź typ pola Password. | `input[formControlName="password"]` | N/D | Typ pola to `password`. |
| 2 | Kliknij ikonę widoczności przy Password. | `button[mat-icon-button]` przy polu Password | N/D | Typ pól `password` i `passwordConfirmation` zmienia się na `text`. |
| 3 | Kliknij ikonę ponownie. | `button[mat-icon-button]` | N/D | Typ pól wraca do `password`. |

---

## 7. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Formularz Register | `form[formGroup]` |
| Karta formularza | `mat-card` |
| Pole First Name | `input[formControlName="firstName"]` |
| Pole Last Name | `input[formControlName="lastName"]` |
| Pole Email | `input[formControlName="email"]` |
| Pole Password | `input[formControlName="password"]` |
| Pole Password Confirmation | `input[formControlName="passwordConfirmation"]` |
| Przycisk Submit | `button[type="submit"]` |
| Komunikat walidacji | `mat-error` |
| Stopka błędu | `mat-card-footer.p-error` |

---

## 8. Dane testowe

### 8.1 Dane poprawne

```json
{
  "firstName": "Jan",
  "lastName": "Kowalski",
  "email": "jan@example.com",
  "password": "Test123!",
  "passwordConfirmation": "Test123!"
}
```

### 8.2 Dane niepoprawne

```json
{
  "firstName": "",
  "lastName": "",
  "email": "jan",
  "password": "",
  "passwordConfirmation": ""
}
```
