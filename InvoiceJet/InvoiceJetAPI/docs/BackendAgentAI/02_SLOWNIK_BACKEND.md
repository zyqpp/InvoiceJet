# Słownik pojęć backendowych

**Obowiązuje:** Dokumentacja AOS backendu InvoiceJetAPI

---

## 1. Terminy techniczne

| Termin obowiązujący | Definicja | Nazwy zakazane bez kontekstu |
|---|---|---|
| **proces backendowy** | Spójna zdolność biznesowa realizowana przez API, od endpointu (lub grupy endpointów) do skutku w warstwie aplikacyjnej lub domenowej. | flow, akcja, funkcja |
| **endpoint** | Metoda HTTP i ścieżka API, na przykład `POST /api/Document/AddDocument`. | adres, route, link |
| **kontroler** | Klasa ASP.NET Core z atrybutem `ApiController`, na przykład `DocumentController`. | controller bez backticków |
| **metoda kontrolera** | Publiczna metoda kontrolera obsługująca endpoint. | akcja kontrolera |
| **DTO** | Klasa transferu danych z przestrzeni `InvoiceJet.Application.DTOs`. | model wejściowy, payload bez opisu |
| **serwis aplikacyjny** | Klasa z `InvoiceJet.Application.Services.Impl`, która wykonuje logikę procesu. | service bez nazwy |
| **algorytm procesu** | Uporządkowana sekwencja kroków wykonywanych przez serwis: walidacje, logika biznesowa, zapisy do bazy, zwrot wyniku. | logika bez kolejności |
| **reguła walidacji** | Warunek sprawdzany w kodzie, którego niespełnienie przerywa proces błędem. Ma podstawę w kodzie, warunek wyzwolenia, wyjątek i status HTTP. | walidacja bez warunku |
| **błąd domenowy** | Wyjątek z `InvoiceJet.Domain.Exceptions` rzucany przez logikę procesu. | error, exception bez nazwy |
| **repozytorium** | Klasa z `InvoiceJet.Infrastructure.Persistence.Repositories`. | repo |
| **encja domenowa** | Klasa z `InvoiceJet.Domain.Models` mapowana do bazy danych. | model bez doprecyzowania |
| **kolumna** | Pole tabeli w bazie, opisane w snapshotcie migracji (typ, nullability, klucze, indeksy). | atrybut bez kontekstu |
| **lookup / tabela słownikowa** | Tabela z wartościami referencyjnymi, na przykład `DocumentType`, `DocumentStatus`. | słownik bez wskazania tabeli |
| **enum** | Typ wyliczeniowy z `InvoiceJet.Domain.Enums`, na przykład `Currency`, `DocumentStatusEnum`, `DocumentTypeEnum`. | stała bez nazwy |
| **seed** | Dane początkowe wstawiane przez `DbSeeder`, na przykład typy dokumentów. | dane startowe bez źródła |
| **jednostka pracy** | `IUnitOfWork`, agreguje repozytoria i wywołuje `CompleteAsync()`. | unit bez kontekstu |
| **middleware błędów** | `ExceptionMiddleware`, zamienia wyjątki na odpowiedzi HTTP JSON. | globalny handler |
| **token JWT** | Token autoryzacyjny obsługiwany przez `JwtBearerDefaults.AuthenticationScheme`. | bearer bez doprecyzowania |
| **aktywny profil firmy** | Relacja `User.ActiveUserFirm` wskazująca firmę używaną przez procesy dokumentów. | aktywna firma bez wskazania relacji |
| **dane testowe** | Konkretne wartości wejściowe i warunki wstępne nadające się do użycia w teście automatycznym lub ręcznym. | przykład bez wartości |
| **wartość brzegowa** | Wartość na granicy reguły walidacji lub typu danych (na przykład pusty ciąg, wartość maksymalna, `null`). | edge case bez wartości |
| **warunek wstępny (precondition)** | Stan bazy lub kontekst użytkownika wymagany, aby scenariusz był wykonalny (na przykład istniejąca firma, aktywne konto bankowe). | założenie bez stanu |
| **kotwica** | Wskazanie źródła twierdzenia w formacie `Plik.cs › Klasa.Metoda`. | odwołanie bez formatu |

---

## 2. Warstwy projektu

| Warstwa | Katalog | Odpowiedzialność |
|---|---|---|
| Presentation | `InvoiceJet.Presentation` | Kontrolery, konfiguracja API, Swagger, CORS, middleware, seeder. |
| Application | `InvoiceJet.Application` | DTO, serwisy aplikacyjne, mapowania AutoMapper. |
| Domain | `InvoiceJet.Domain` | Encje, enumy, wyjątki, interfejsy repozytoriów. |
| Infrastructure | `InvoiceJet.Infrastructure` | EF Core, repozytoria, `InvoiceJetDbContext`, migracje, fabryki i generowanie PDF. |

---

## 3. Metody HTTP

Metody HTTP zapisuje się wersalikami:

- `GET` dla pobrania danych,
- `POST` dla utworzenia zasobu lub operacji generującej zasób,
- `PUT` dla aktualizacji lub operacji modyfikującej istniejące dane,
- `DELETE` tylko gdy endpoint faktycznie używa metody `DELETE`.

Jeżeli kod używa `PUT` do usuwania (na przykład `PUT /api/Document/DeleteDocuments`), dokument opisuje `PUT`, nie zamienia metody na `DELETE`, i odnotowuje rozbieżność markerem.

---

## 4. Identyfikatory w dokumentacji

| Prefiks | Znaczenie | Przykład |
|---|---|---|
| `P-XX` | Numer procesu biznesowego. | `P-01` |
| `API-XX` | Numer endpointu w `KATALOG_API`. | `API-03` |
| `WAL-XX` | Numer reguły walidacji w obrębie procesu (plik `05`). | `WAL-02` |
| `TC-XX` / `TC-NXX` | Identyfikator przypadku/danych testowych (plik `06`). | `TC-01`, `TC-N02` |
| `DT-XX` | Wpis w `KATALOG_DANYCH_TESTOWYCH`. | `DT-05` |
