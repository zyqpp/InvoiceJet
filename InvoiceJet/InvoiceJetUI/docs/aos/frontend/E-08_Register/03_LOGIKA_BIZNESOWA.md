# Register — Logika frontendowa

---

## 1. Zakres dokumentu

Dokument opisuje logikę wykonywaną przez frontend ekranu Register. Dokument nie opisuje implementacji backendu, reguł bazy danych ani wewnętrznego przetwarzania po stronie API.

---

## 2. Inicjalizacja ekranu

### 2.1 Przepływ renderowania

```mermaid
flowchart TD
  A["Wejście na /register"] --> B["AppComponent NavigationEnd"]
  B --> C["isLoginOrRegister = false"]
  C --> D["Menu boczne nie jest renderowane"]
  D --> E["RegisterComponent"]
  E --> F["registerForm z pustymi wartościami"]
```

Trasa `/register` nie ma `AuthGuard`. Ekran jest dostępny publicznie.

---

## 3. Przepływ rejestracji

```mermaid
flowchart TD
  A["Kliknięcie Submit"] --> B["onSubmit()"]
  B --> C{"registerForm.invalid"}
  C -->|true| D["return"]
  C -->|false| E["Budowa IRegisterUser"]
  E --> F["AuthService.register(user)"]
  F --> G["POST /Auth/register"]
  G --> H["response.token"]
  H --> I["localStorage.setItem('authToken', token)"]
  I --> J["router.navigate(['dashboard'])"]
```

`onSubmit()` nie wykonuje żądania HTTP, gdy `registerForm.invalid` ma wartość `true`.

---

## 4. Reguły walidacji frontendowej

| Pole | Walidatory |
|---|---|
| `firstName` | `Validators.required` |
| `lastName` | `Validators.required` |
| `email` | `Validators.required`, `Validators.email` |
| `password` | `Validators.required` |
| `passwordConfirmation` | `Validators.required` |

Walidacja zgodności pól `password` i `passwordConfirmation` nie jest zaimplementowana w pokazanym kodzie.

---

## 5. Przepływ widoczności hasła

Pola `password` i `passwordConfirmation` mają typ zależny od flagi `hide`.

| Wartość `hide` | Typ pól hasła | Ikona |
|---|---|---|
| `true` | `password` | `visibility_off` |
| `false` | `text` | `visibility` |

Kliknięcie przycisku przy dowolnym polu hasła zmienia tę samą flagę `hide`.

---

## 6. Obsługa sukcesu i błędów

Sukces rejestracji jest obsługiwany lokalnie przez zapis tokenu i nawigację do dashboardu.

Błędy HTTP są obsługiwane przez interceptory:

- `AuthInterceptor` obsługuje status `401` przekierowaniem do `/login`.
- `ErrorInterceptor` wyświetla komunikaty błędów przez `ToastrService.error(...)`.

Komponent zawiera pole `errorMessage`, ale pokazany kod nie ustawia go w gałęzi błędu `subscribe`.

---

## 7. Ograniczenia opisu

- Dokument nie opisuje walidacji backendowej.
- Dokument nie opisuje polityki haseł po stronie API.
- Dokument nie opisuje tworzenia użytkownika po stronie API.
- Dokument nie opisuje struktury tokenu poza zapisem wartości `response.token`.
