# Logowanie użytkownika — Dane, modele i mapowania

## DTO wejściowe

| DTO | Rola |
|---|---|
| `UserLoginDto` | Dane wejściowe logowania. |

---

## Encje

| Encja | Operacja |
|---|---|
| `User` | Odczyt użytkownika po `Email`. |

---

## Mapowanie

Proces nie używa `AutoMapper`.

---

## Dane wyjściowe

| Element | Opis |
|---|---|
| `token` | JWT przekazany do klienta. |
