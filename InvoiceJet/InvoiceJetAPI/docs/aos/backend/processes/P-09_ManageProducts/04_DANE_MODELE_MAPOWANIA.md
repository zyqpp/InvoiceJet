# Zarządzanie produktami — Dane, modele i mapowania

## DTO i encje

| Element | Rola |
|---|---|
| `ProductDto` | Wejście i wyjście operacji produktu. |
| `Product` | Encja produktu zapisywana i aktualizowana w bazie. |
| `DocumentProduct` | Encja używana do walidacji usuwania produktu. |

---

## Mapowanie

| Źródło | Cel | Profil |
|---|---|---|
| `Product` | `ProductDto` | `ProductProfile` |
| `ProductDto` | `Product` | `ProductProfile` (`ReverseMap`) |
