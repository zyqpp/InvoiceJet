# PUT /api/Firm/DeleteFirms — Usunięcie firm

| Atrybut | Wartość |
|---|---|
| ID | API-09 |
| Metoda | PUT |
| URL | `/api/Firm/DeleteFirms` |
| Autoryzacja | `[Authorize(Roles = "User")]` |
| Kontroler | `FirmController.DeleteFirms` |
| Serwis | `FirmService.DeleteFirms` |
| Status doc. | szkic |
| Ostatnia walidacja | 2026-05-31 |

> **Anomalia A-01:** Użycie `PUT` zamiast `DELETE` do usuwania.  
> **Anomalia A-07:** Parametr `int[] firmIds` bez `[FromBody]` — binding z **query string**, nie body.

## Request

### Headers
| Nagłówek | Wartość |
|---|---|
| `Authorization` | `Bearer {token}` |

### Parametr (query string — nie body!)

| Parametr | Typ | Wymagane | Opis |
|---|---|---|---|
| `firmIds` | `int[]` | TAK | Tablica ID firm do usunięcia |

**Przykład URL:**
```
PUT /api/Firm/DeleteFirms?firmIds=10&firmIds=11&firmIds=12
```

> Angular `FirmService.deleteFirms(firmIds: number[])` — musi przekazywać jako query params, nie body.

## Response

### 200 OK

Pusta odpowiedź (HTTP 200 bez body).

### Błędy

| Status HTTP | Wyjątek | Warunek |
|---|---|---|
| 400 Bad Request | `FirmAssociatedWithDocumentException` | Firma powiązana z istniejącym dokumentem (jest klientem) |
| 500 Internal Server Error | `Exception("Product not found.")` | Firma o podanym Id nie istnieje (błędny komunikat w wyjątku!) |
| 401 Unauthorized | — | Brak/wygaśnięty token |

> **Uwaga:** Przy błędzie dla N-tej firmy, wcześniej przetworzone firmy mogą być już usunięte (brak transakcji ogarniającej całą operację — `CompleteAsync()` wywołane raz po pętli).

## Algorytm

```csharp
foreach (var firmId in firmIds)
{
    var firm = await _unitOfWork.Firms.GetByIdAsync(firmId)
               ?? throw new Exception("Product not found."); // błędny komunikat

    bool isAssociatedWithDocuments = await _unitOfWork.Documents.Query()
        .AnyAsync(d => d.ClientId == firmId);
    if (isAssociatedWithDocuments)
        throw new FirmAssociatedWithDocumentException(firm.Name);

    await _unitOfWork.Firms.RemoveAsync(firm);
}
await _unitOfWork.CompleteAsync();
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny z anomaliami. |
