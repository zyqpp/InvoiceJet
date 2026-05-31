# Dodaj produkt — proces techniczny

| Pole | Wartość |
|---|---|
| ID dokumentu | PROC-AddProduct |
| Typ dokumentu | proces |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces tworzy nowy produkt lub usługę w katalogu firmy zalogowanego użytkownika. Produkt przypisywany jest do `UserFirm` przez `UserFirmId`. Backend waliduje unikalność nazwy produktu — jednak unikalność jest egzekwowana globalnie (nie per firma), co stanowi anomalię projektową powodującą nieoczekiwane błędy 500.

## Cel procesu

Dodać nową pozycję (produkt lub usługę) do katalogu firmy, aby można ją było wybierać przy wystawianiu dokumentów.

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| ID procesu | PROC-AddProduct |
| Typ | główny |
| Inicjator | Ekran „Produkty" + dialog „Dodaj produkt" + operacja zapisu |
| Warunki startu | Użytkownik zalogowany (JWT); formularz produktu wypełniony |
| Warunki zakończenia (sukces) | Rekord `Product` zapisany w DB; HTTP 201 |
| Warunki zakończenia (błąd) | Nazwa produktu zajęta globalnie (500 zamiast 409 — anomalia) |
| Uczestnicy | Frontend (Angular), API (ProductController), Service (ProductService), Repository (ProductRepository), Database (dbo.Product) |

## Diagram sekwencji

```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as ProductController
    participant S as ProductService
    participant R as ProductRepository
    participant D as Database

    F->>A: POST /api/Product/Add (ProductRequestDto)
    A->>S: AddProduct(productRequestDto)
    S->>S: Pobierz userId z JWT claims
    S->>R: GetUserFirmIdByUserId(userId)
    R->>D: SELECT UserFirmId FROM UserFirm WHERE UserId = @userId
    D-->>R: userFirmId
    R-->>S: userFirmId
    S->>S: Mapuj ProductRequestDto → Product; ustaw UserFirmId
    S->>R: AddAsync(product) + CompleteAsync()
    R->>D: INSERT INTO Product (Name, MeasureUnit, Price, VatRate, UserFirmId)
    alt Nazwa unikalna — OK
        D-->>R: OK
        R-->>S: OK
        S-->>A: 201 Created
        A-->>F: 201 Created
    else Naruszenie UNIQUE INDEX na Name
        D-->>R: SqlException (UniqueConstraint)
        R-->>S: Exception
        S-->>A: Exception nieobsłużony → ExceptionMiddleware
        A-->>F: 500 Internal Server Error
    end
```

## Kroki

1. **Odbiór żądania** — `ProductController` odbiera `ProductRequestDto` z POST `/api/Product/Add`.
2. **Ekstrakcja userId** — serwis pobiera `userId` z claims JWT.
3. **Pobranie UserFirmId** — zapytanie do bazy przez repozytorium lub z claims.
4. **Mapowanie i przypisanie** — `AutoMapper` mapuje DTO → `Product`; serwis ustawia `UserFirmId`.
5. **Zapis** — `ProductRepository.AddAsync(product)` + `UnitOfWork.CompleteAsync()`.
6. **Odpowiedź** — HTTP 201 Created; lub 500 przy naruszeniu UNIQUE INDEX (anomalia PD-02).

## Obsługa błędów

| Błąd | Miejsce wystąpienia | Reakcja |
|---|---|---|
| UNIQUE INDEX violation (`Product.Name`) | Database | HTTP 500 — niezrozumiały błąd zamiast 409 Conflict (anomalia PD-02) |
| Nieautoryzowany dostęp | AuthMiddleware | HTTP 401 Unauthorized |
| Błąd DB (nieoczekiwany) | ProductRepository | HTTP 500 Internal Server Error (ExceptionMiddleware) |

## Powiązania

- Wywołany z ekranu: `01_ekrany/produkty/`
- Powiązane API: `POST /api/Product/Add`
- Powiązany algorytm: Nie dotyczy

## Powiązania z kodem

- Kontroler: `InvoiceJetAPI/Controllers/ProductController.cs`
- Serwis: `InvoiceJetAPI/Services/ProductService.cs`
- Repozytorium: `InvoiceJetAPI/Repositories/ProductRepository.cs`

## Wątpliwości i braki

- `Product.Name` ma UNIQUE INDEX **globalny** (nie per UserFirm) — dwóch różnych użytkowników nie może mieć produktu o tej samej nazwie. To błąd projektowy (anomalia PD-01).
- Naruszenie UNIQUE zwraca niezrozumiały 500 zamiast 409 Conflict z komunikatem dla użytkownika (anomalia PD-02).

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wyodrębniona z P-06_ManageProducts.md (operacja AddProduct). |
