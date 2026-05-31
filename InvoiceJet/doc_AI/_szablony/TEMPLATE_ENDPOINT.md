# Endpoint: METHOD /api/Zasób/Akcja

| Atrybut | Wartość |
|---|---|
| ID | API-XX |
| Metoda HTTP | GET / POST / PUT / DELETE |
| Ścieżka | `/api/Zasób/Akcja` |
| Kontroler | `NazwaController` |
| Serwis | `NazwaService` |
| AuthGuard | `[Authorize]` TAK / NIE |
| Ostatnia walidacja | YYYY-MM-DD |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

[Opis endpointu]

## Żądanie (Request)

### Nagłówki

```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

### Parametry URL

| Parametr | Typ | Opis |
|---|---|---|
| `id` | `int` | ... |

### Body

```json
{}
```

## Odpowiedź (Response)

### Sukces — 200 OK / 201 Created

```json
{}
```

### Błędy

| HTTP | Kiedy |
|---|---|
| 400 | Niepoprawne dane |
| 401 | Brak / niepoprawny token |
| 404 | Zasób nie istnieje |
| 500 | Błąd serwera |

## Walidacje backendowe

| ID | Warunek | Wyjątek | HTTP |
|---|---|---|---|
| WAL-01 | ... | `NazwaException` | 4xx |

## Anomalie

| # | Anomalia |
|---|---|
| AX-01 | ... |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
