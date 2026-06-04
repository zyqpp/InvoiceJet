# Zarządzanie firmami-klientami — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `FirmDto` | DTO odpowiedzi listy klientów. |
| `Firm` | Encja firmy-klienta. |
| `UserFirm` | Relacja użytkownik-firma z flagą `IsClient`. |
| `Document` | Źródło walidacji blokującej usunięcie klienta. |

---

## Mapowanie

| Źródło | Cel | Mechanizm |
|---|---|---|
| `List<Firm>` | `List<FirmDto>` | `FirmProfile` (`ReverseMap`) przez `_mapper.Map<List<FirmDto>>(firms)` |
