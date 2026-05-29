# Pobranie strumienia PDF faktury — Dane, modele i mapowania

## DTO

| Element | Rola |
|---|---|
| `DocumentRequestDto` | Wejście procesu dla generatora PDF. |
| `DocumentStreamDto` | Nośnik strumienia i numeru dokumentu. |
| `FirmDto` | Uzupełniane pole `Seller`. |
| `BankAccountDto` | Uzupełniane pole `BankAccount`. |

---

## Mapowania

| Źródło | Cel | Profil |
|---|---|---|
| `activeUserFirm.Firm` | `FirmDto` | `FirmProfile` |
| `BankAccount` | `BankAccountDto` | `BankAccountProfile` |
