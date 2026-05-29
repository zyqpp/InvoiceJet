# Rejestracja użytkownika — Dane, modele i mapowania

## DTO wejściowe

| DTO | Rola |
|---|---|
| `UserRegisterDto` | Dane wejściowe rejestracji użytkownika. |

---

## Encje

| Encja | Operacja |
|---|---|
| `User` | Dodanie nowego rekordu użytkownika. |

---

## Mapowanie

Proces nie korzysta z `AutoMapper`. Pola encji `User` są przypisywane ręcznie.

---

## Dane wyjściowe

| Element | Opis |
|---|---|
| `token` | JWT zwrócony jako obiekt anonimowy z jednym polem. |
