# Zarządzanie kontami bankowymi — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `BankAccountDto` | Wejście i wyjście operacji kont bankowych. |
| `BankAccount` | Encja konta bankowego zapisywana i aktualizowana. |
| `Document` | Encja używana do walidacji usuwania kont. |

---

## Mapowanie

| Źródło | Cel | Profil |
|---|---|---|
| `BankAccount` | `BankAccountDto` | `BankAccountProfile` |
| `BankAccountDto` | `BankAccount` | `BankAccountProfile` (`ReverseMap`) |

---

## Reguła aktywnego konta

Jeżeli dodawane lub edytowane konto ma `IsActive = true`, serwis ustawia `IsActive = false` dla pozostałych kont tej samej firmy przez `DeactivateOtherBankAccounts(...)`.
