# Rejestracja użytkownika — Przegląd procesu

## Cel

Proces tworzy nowego użytkownika w bazie danych, zapisuje hasło jako hash `BCrypt` i zwraca token JWT.

---

## Diagram przepływu

```mermaid
flowchart TD
  A["POST /api/Auth/register"] --> B["AuthController.Register()"]
  B --> C["AuthService.RegisterUser()"]
  C --> D["Sprawdzenie unikalności email"]
  D --> E["Walidacja regex hasła"]
  E --> F["Sprawdzenie zgodności password i confirmation"]
  F --> G["Utworzenie encji User"]
  G --> H["Users.AddAsync(user)"]
  H --> I["CompleteAsync()"]
  I --> J["CreateToken(user)"]
  J --> K["HTTP 200 OK { token }"]
```

---

## Warunki wejściowe

| Warunek | Źródło | Skutek |
|---|---|---|
| Brak istniejącego użytkownika z danym adresem e-mail | `_unitOfWork.Users.Query().FirstOrDefaultAsync(u => u.Email == userDto.Email)` | Tworzenie użytkownika jest kontynuowane. |
| Hasło spełnia wzorzec regex | `passwordRules.IsMatch(userDto.Password)` | Tworzenie użytkownika jest kontynuowane. |
| `Password` i `PasswordConfirmation` mają taką samą wartość | `userDto.Password == userDto.PasswordConfirmation` | Tworzenie użytkownika jest kontynuowane. |

---

## Wynik procesu

| Wynik | Opis |
|---|---|
| Sukces | API zwraca `200 OK` i obiekt `{ token }`. |
| Zapis danych | W bazie powstaje rekord `User` z hashem hasła i rolą `User`. |
| Token | JWT zawiera claimy `userId`, `firstName`, `lastName`, `email`, rolę `User` i czas wygaśnięcia 10 minut. |
