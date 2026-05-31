# PUT /api/Product/DeleteProducts — Usunięcie produktów

| Atrybut | Wartość |
|---|---|
| ID | API-13 |
| Metoda | PUT |
| URL | `/api/Product/DeleteProducts` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `ProductController.DeleteProducts` |
| Serwis | `IProductService.DeleteProducts` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Anomalia A-07:** `int[] productIds` bez `[FromBody]` → binding z query string, nie body.

## Request

### Parametr (query string — nie body!)

**Przykład URL:**
```
PUT /api/Product/DeleteProducts?productIds=1&productIds=2
```

## Response

### 200 OK — pusta odpowiedź

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
