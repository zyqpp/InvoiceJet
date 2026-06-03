# Logowanie użytkownika — Scenariusze testowe

## Scenariusze pozytywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-01 | Logowanie poprawne | Użytkownik istnieje i hasło jest poprawne. | `200 OK`, odpowiedź zawiera `token`. |

---

## Scenariusze negatywne

| ID | Scenariusz | Warunek | Oczekiwany rezultat |
|---|---|---|---|
| TC-N01 | Nieistniejący użytkownik | `email` nie istnieje w bazie. | `400 Bad Request`, komunikat z `UserNotFoundException`. |
| TC-N02 | Błędne hasło | `password` nie pasuje do hasha. | `400 Bad Request`, komunikat z `IncorrectPasswordException`. |

---

## Dane testowe przykładowe

```json
{
  "email": "jan.kowalski@example.com",
  "password": "Strong!123"
}
```
