# Propozycje testów API — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-AUTO-API |
| Typ dokumentu | propozycje testów API (nie zaimplementowane) |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Projekt InvoiceJet nie zawiera zaimplementowanych testów API. Poniżej przedstawiono propozycje testów dla 31 endpointów REST API, z uwzględnieniem priorytetów i scenariuszy krytycznych. Implementacja rekomendowana jest z użyciem `WebApplicationFactory` (ASP.NET Core 8) z bazą danych EF Core InMemory.

## Propozycje testów API

| ID | Endpoint | Metoda | Scenariusz testowy | Priorytet | Anomalia |
|---|---|---|---|---|---|
| T-API-01 | `/api/Auth/register` | POST | Rejestracja z poprawnymi danymi — 200 OK + JWT | KRYTYCZNY | — |
| T-API-02 | `/api/Auth/register` | POST | Rejestracja — e-mail już zajęty — błąd | KRYTYCZNY | — |
| T-API-03 | `/api/Auth/register` | POST | Rejestracja — hasło bez znaku specjalnego — 400 | WYSOKI | — |
| T-API-04 | `/api/Auth/register` | POST | Rejestracja — hasło < 8 znaków — 400 | WYSOKI | — |
| T-API-05 | `/api/Auth/register` | POST | Rejestracja — brak wielkiej litery — 400 | WYSOKI | — |
| T-API-06 | `/api/Auth/login` | POST | Logowanie z poprawnymi danymi — 200 OK + JWT | KRYTYCZNY | — |
| T-API-07 | `/api/Auth/login` | POST | Logowanie — błędne hasło — 401 | KRYTYCZNY | — |
| T-API-08 | `/api/Auth/login` | POST | Logowanie — nieistniejący e-mail — 401 | WYSOKI | — |
| T-API-09 | `/api/Firm/AddFirm/false` | POST | Dodanie własnej firmy — 201 Created | WYSOKI | — |
| T-API-10 | `/api/Firm/AddFirm/true` | POST | Dodanie klienta — 201 Created | WYSOKI | — |
| T-API-11 | `/api/Firm/GetUserActiveFirm` | GET | Brak firmy — odpowiedź null | WYSOKI | — |
| T-API-12 | `/api/Firm/GetUserActiveFirm` | GET | Brak tokenu — 401 | WYSOKI | — |
| T-API-13 | `/api/Product/AddProduct` | POST | Dodanie produktu — 201 Created | WYSOKI | — |
| T-API-14 | `/api/Product/AddProduct` | POST | Dwie konta, ta sama nazwa produktu — błąd UNIQUE | KRYTYCZNY | A-03 |
| T-API-15 | `/api/Product/GetAll` | GET | Brak tokenu — 401 | WYSOKI | — |
| T-API-16 | `/api/BankAccount/AddBankAccount` | POST | Dodanie konta — 201 Created | WYSOKI | — |
| T-API-17 | `/api/BankAccount/DeleteBankAccounts` | PUT | Usunięcie konta z powiązaną fakturą — CASCADE DELETE | KRYTYCZNY | A-KRIT-01 |
| T-API-18 | `/api/DocumentSeries/AddDocumentSeries` | POST | Dodanie serii FV — 201 Created | WYSOKI | — |
| T-API-19 | `/api/Document/AddDocument` | POST | Wystawienie faktury — 201 + numer FV0001 | KRYTYCZNY | — |
| T-API-20 | `/api/Document/AddDocument` | POST | Wystawienie proformy (documentTypeId=2) — 201 + PRF0001 | KRYTYCZNY | — |
| T-API-21 | `/api/Document/AddDocument` | POST | Równoczesne 2 żądania — numery unikalne | KRYTYCZNY | A-02 race condition |
| T-API-22 | `/api/Document/AddDocument` | POST | Brak serii dokumentów — błąd walidacji | WYSOKI | — |
| T-API-23 | `/api/Document/AddDocument` | POST | Brak tokenu — 401 | WYSOKI | — |
| T-API-24 | `/api/Document/GetTableRecords` | GET | Pobranie listy faktur — 200 + lista | WYSOKI | — |
| T-API-25 | `/api/Document/GetById/{id}` | GET | Pobranie faktury po ID — 200 + obiekt | WYSOKI | — |
| T-API-26 | `/api/Document/GetById/{id}` | GET | Dostęp do dokumentu innego użytkownika | KRYTYCZNY | izolacja danych |
| T-API-27 | `/api/Document/GenerateInvoicePdf` | POST | PDF faktury — typ `InvoiceDocument` | WYSOKI | — |
| T-API-28 | `/api/Document/GenerateInvoicePdf` | POST | PDF proformy — weryfikacja błędu hardcoded szablonu | KRYTYCZNY | A-KRIT-04 |
| T-API-29 | `/api/Document/GetPdfStream` | POST | Strumień PDF faktury — 200 + stream | WYSOKI | — |
| T-API-30 | `/api/Document/TransformToStorno` | PUT | Konwersja faktury na storno — 200 + typ storno | WYSOKI | — |
| T-API-31 | `/api/Document/GetDashboardStats` | GET | Statystyki roku — 200 + dane zagregowane | ŚREDNI | — |

## Priorytety implementacji

### Faza 1 — Krytyczne (zalecane przed pierwszym wdrożeniem produkcyjnym)

1. T-API-17: Weryfikacja anomalii CASCADE DELETE kont bankowych
2. T-API-21: Test race condition numeracji dokumentów
3. T-API-28: Weryfikacja błędnego szablonu PDF dla proformy
4. T-API-14: Weryfikacja globalnego UNIQUE INDEX na nazwie produktu
5. T-API-26: Izolacja danych między użytkownikami (autoryzacja)

### Faza 2 — Wysokie (testy podstawowych przepływów)

Endpointy: T-API-01 do T-API-13, T-API-18 do T-API-20, T-API-22 do T-API-25

### Faza 3 — Średnie (pokrycie uzupełniające)

Endpointy: T-API-31, testy walidacji formularzy, testy paginacji

## Przykładowa implementacja (szkielet)

```csharp
// Przykład: WebApplicationFactory test dla API-01
public class AuthControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public AuthControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task Register_WithValidData_Returns200WithToken()
    {
        var request = new { email = "test@example.com", password = "Test@123",
                            firstName = "Jan", lastName = "Kowalski" };
        var response = await _client.PostAsJsonAsync("/api/Auth/register", request);
        response.EnsureSuccessStatusCode();
        var body = await response.Content.ReadFromJsonAsync<dynamic>();
        Assert.NotNull(body?.token);
    }
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
