# Logowanie użytkownika — Przegląd procesu

## Cel

Proces weryfikuje dane logowania użytkownika i zwraca token JWT dla poprawnych poświadczeń.

---

## Diagram przepływu

```mermaid
flowchart TD
  A["POST /api/Auth/login"] --> B["AuthController.Login()"]
  B --> C["AuthService.LoginUser()"]
  C --> D["Pobranie użytkownika po Email"]
  D --> E{"Użytkownik istnieje"}
  E -->|nie| F["UserNotFoundException"]
  E -->|tak| G["BC.Verify(password, passwordHash)"]
  G --> H{"Hasło poprawne"}
  H -->|nie| I["IncorrectPasswordException"]
  H -->|tak| J["CreateToken(user)"]
  J --> K["HTTP 200 OK { token }"]
```

---

## Warunki wejściowe

| Warunek | Źródło | Skutek |
|---|---|---|
| Użytkownik istnieje dla wskazanego `Email` | `_unitOfWork.Users.Query().FirstOrDefaultAsync(...)` | Weryfikacja hasła jest kontynuowana. |
| Hasło zgadza się z hashem | `BC.Verify(userDto.Password, user.PasswordHash)` | Token JWT jest generowany. |

---

## Wynik procesu

| Wynik | Opis |
|---|---|
| Sukces | `200 OK` z obiektem `{ token }`. |
| Błąd użytkownika | `400 Bad Request` dla braku użytkownika lub błędnego hasła. |
