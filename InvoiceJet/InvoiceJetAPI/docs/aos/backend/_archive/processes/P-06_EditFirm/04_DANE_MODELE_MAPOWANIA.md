# Edycja firmy — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `FirmDto` | Dane wejściowe i wyjściowe procesu. |
| `Firm` | Encja firmy aktualizowana w bazie. |
| `UserFirm` | Relacja użytkownika i firmy aktualizowana dla flagi `IsClient`. |

---

## Mapowanie

| Źródło | Cel | Mechanizm |
|---|---|---|
| `FirmDto` | `Firm` | `FirmProfile` (`ReverseMap`) i `_mapper.Map(firmDto, firm)` |
| `isClient` | `UserFirm.IsClient` | Przypisanie bezpośrednie w `ManageUserFirmRelation` |
