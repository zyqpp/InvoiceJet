# Pobranie aktywnej firmy użytkownika — Dane, modele i mapowania

## Dane źródłowe

| Encja / obiekt | Rola |
|---|---|
| `User` | Zawiera wskaźnik `ActiveUserFirm`. |
| `UserFirm` | Relacja użytkownika i firmy aktywnej. |
| `Firm` | Dane firmy mapowane do DTO. |

---

## Mapowanie

| Źródło | Cel | Mechanizm |
|---|---|---|
| `Firm` | `FirmDto` | `FirmProfile` (`CreateMap<Firm, FirmDto>().ReverseMap()`) |
