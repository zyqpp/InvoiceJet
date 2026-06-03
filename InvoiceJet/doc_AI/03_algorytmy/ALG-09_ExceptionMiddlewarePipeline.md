# Algorytm: Pipeline obsługi wyjątków (ExceptionMiddleware)

| Atrybut | Wartość |
|---|---|
| ID | ALG-09 |
| Nazwa | Exception Handling Middleware Pipeline |
| Kategoria | Obsługa błędów / Middleware |
| Pliki | `ExceptionMiddleware.cs`, `Program.cs` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Globalna obsługa wyjątków na poziomie middleware — przechwytuje wszystkie wyjątki z serwisów aplikacyjnych i mapuje je na odpowiednie kody HTTP z komunikatem JSON.

## Diagram przepływu

```mermaid
flowchart TD
    A[HTTP Request] --> B[ExceptionMiddleware]
    B --> C[try: next middleware]
    C --> D{Wyjątek?}
    D -- NIE --> E[Normalny response]
    D -- TAK --> F{Typ wyjątku}
    F --> G[UserAlreadyExistsException → 409]
    F --> H[UserNotFoundException → 401]
    F --> I[InvalidCredentialsException → 401]
    F --> J[InvalidPasswordException → 400]
    F --> K[FirmNotFoundException → 404]
    F --> L[BankAccountNotFoundException → 404]
    F --> M[ProductNotFoundException → 404]
    F --> N[DocumentNotFoundException → 404]
    F --> O[DocumentSeriesNotFoundException → 404]
    F --> P[Inny wyjątek → 500 Internal Server Error]
    G & H & I & J & K & L & M & N & O & P --> Q[Response: JSON {message}]
```

## Mapa wyjątków → HTTP

| Wyjątek domenowy | Kod HTTP | Komunikat |
|---|---|---|
| `UserAlreadyExistsException` | 409 Conflict | "User already exists" |
| `UserNotFoundException` | 401 Unauthorized | "User not found" |
| `InvalidCredentialsException` | 401 Unauthorized | "Invalid credentials" |
| `InvalidPasswordException` | 400 Bad Request | "Invalid password" |
| `FirmNotFoundException` | 404 Not Found | "Firm not found" |
| `BankAccountNotFoundException` | 404 Not Found | "Bank account not found" |
| `ProductNotFoundException` | 404 Not Found | "Product not found" |
| `DocumentNotFoundException` | 404 Not Found | "Document not found" |
| `DocumentSeriesNotFoundException` | 404 Not Found | "Document series not found" |
| `Exception` (catch-all) | 500 Internal Server Error | Stack trace / message |

## Format odpowiedzi błędu

```json
{
  "message": "User not found"
}
```

## Struktura middleware

```csharp
// ExceptionMiddleware.cs
public class ExceptionMiddleware
{
    private readonly RequestDelegate _next;

    public async Task InvokeAsync(HttpContext context)
    {
        try {
            await _next(context);
        }
        catch (UserAlreadyExistsException ex) {
            context.Response.StatusCode = 409;
            await context.Response.WriteAsJsonAsync(new { message = ex.Message });
        }
        catch (UserNotFoundException ex) {
            context.Response.StatusCode = 401;
            await context.Response.WriteAsJsonAsync(new { message = ex.Message });
        }
        // ... pozostałe wyjątki ...
        catch (Exception ex) {
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new { message = ex.Message });
        }
    }
}
```

## Anomalie

| # | Anomalia |
|---|---|
| EXC-01 | Wyjątek UniqueConstraint (duplikat nazwy produktu) trafia do catch-all → 500; brak własnego wyjątku domenowego |
| EXC-02 | Catch-all 500 zwraca `ex.Message` — może ujawniać szczegóły stack trace w produkcji |
| EXC-03 | Kontroler `DocumentController` i `BankAccountController` mają własne try/catch obok middleware — podwójna obsługa błędów |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
