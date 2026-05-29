# Słownik pojęć backendowych

**Obowiązuje:** Dokumentacja AOS backendu InvoiceJetAPI

---

## 1. Terminy techniczne

| Termin obowiązujący | Definicja | Nazwy zakazane bez kontekstu |
|---|---|---|
| **proces backendowy** | Spójny przepływ API od endpointu do skutku w warstwie aplikacyjnej lub domenowej. | flow, akcja, funkcja |
| **endpoint** | Metoda HTTP i ścieżka API, na przykład `POST /api/Document/AddDocument`. | adres, route, link |
| **kontroler** | Klasa ASP.NET Core z atrybutem `ApiController`, na przykład `DocumentController`. | controller bez backticków |
| **metoda kontrolera** | Publiczna metoda kontrolera obsługująca endpoint. | akcja kontrolera |
| **DTO** | Klasa transferu danych z przestrzeni `InvoiceJet.Application.DTOs`. | model wejściowy, payload bez opisu |
| **serwis aplikacyjny** | Klasa z `InvoiceJet.Application.Services.Impl`, która wykonuje logikę procesu. | service bez nazwy |
| **repozytorium** | Klasa z `InvoiceJet.Infrastructure.Persistence.Repositories`. | repo |
| **encja domenowa** | Klasa z `InvoiceJet.Domain.Models` mapowana do bazy danych. | model bez doprecyzowania |
| **jednostka pracy** | `IUnitOfWork`, agreguje repozytoria i wywołuje `CompleteAsync()`. | unit bez kontekstu |
| **middleware błędów** | `ExceptionMiddleware`, zamienia wyjątki na odpowiedzi HTTP JSON. | globalny handler |
| **token JWT** | Token autoryzacyjny obsługiwany przez `JwtBearerDefaults.AuthenticationScheme`. | bearer bez doprecyzowania |
| **aktywny profil firmy** | Relacja `User.ActiveUserFirm` wskazująca firmę używaną przez procesy dokumentów. | aktywna firma bez wskazania relacji |

---

## 2. Warstwy projektu

| Warstwa | Katalog | Odpowiedzialność |
|---|---|---|
| Presentation | `InvoiceJet.Presentation` | Kontrolery, konfiguracja API, Swagger, CORS, middleware. |
| Application | `InvoiceJet.Application` | DTO, serwisy aplikacyjne, mapowania AutoMapper. |
| Domain | `InvoiceJet.Domain` | Encje, enumy, wyjątki, interfejsy repozytoriów. |
| Infrastructure | `InvoiceJet.Infrastructure` | EF Core, repozytoria, `InvoiceJetDbContext`, generowanie PDF. |

---

## 3. Metody HTTP

Metody HTTP zapisuje się wersalikami:

- `GET` dla pobrania danych,
- `POST` dla utworzenia zasobu lub operacji generującej zasób,
- `PUT` dla aktualizacji lub operacji modyfikującej istniejące dane,
- `DELETE` tylko gdy endpoint faktycznie używa metody `DELETE`.

Jeżeli kod używa `PUT` do usuwania, dokument opisuje `PUT`, nie zamienia metody na `DELETE`.
