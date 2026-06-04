# Katalogi przekrojowe

**Obowiązuje:** Dokumentacja AOS backendu InvoiceJetAPI
**Cel:** Opisać wiedzę, która nie należy do jednego procesu, lecz do całego backendu, i utrzymać ją w jednym miejscu (bez duplikacji w procesach).

---

## 1. Zasada „pojedynczego źródła"

Wiedza przekrojowa (schemat bazy, lista wyjątków, model domeny, zagadnienia techniczne, dane testowe wielokrotnego użytku) żyje w katalogach przekrojowych. Procesy **odwołują się** do nich, zamiast je kopiować.

Przykład: proces `P-09` nie opisuje od nowa, co to enum `Currency` — linkuje do `SLOWNIK_DANYCH.md`.

---

## 2. Lista katalogów przekrojowych

Pliki powstają w `docs/aos/backend/` (poziom nad `processes/`). Szablony są w `docs/aos/backend/templates/`.

| Plik | Zawartość | Główne źródło w kodzie |
|---|---|---|
| `KATALOG_API.md` | Wszystkie endpointy 1:1: metoda, ścieżka, autoryzacja, DTO we/wy, proces. | `Controllers/*` |
| `SLOWNIK_DANYCH.md` | Tabele, kolumny (typ, nullability, klucze, indeksy), relacje, enumy, tabele słownikowe, seed. | snapshot migracji, `Domain/Models`, `Domain/Enums`, `DbSeeder` |
| `KATALOG_WYJATKOW.md` | Każdy wyjątek domenowy → status HTTP → komunikat → czy mapowany jawnie. | `Domain/Exceptions`, `ExceptionMiddleware` |
| `MODEL_DOMENY.md` | Diagram ER i opis relacji między encjami. | `Domain/Models`, `InvoiceJetDbContext`, snapshot |
| `ZAGADNIENIA_PRZEKROJOWE.md` | JWT/uwierzytelnianie, `ExceptionMiddleware`, `IUnitOfWork`/transakcje, AutoMapper, CORS, konfiguracja, integracje ANAF i QuestPDF. | `Program.cs`, `Middleware`, `UnitOfWork`, `appsettings*.json`, `Infrastructure/*` |
| `KATALOG_DANYCH_TESTOWYCH.md` | Wielokrotnie używane fixture'y i seed: użytkownik, firma, konto bankowe, produkt, seria — z wartościami i zależnościami. | `DbSeeder`, snapshot, DTO |
| `MAPA_FULLSTACK.md` | (Odłożone) Mapa proces ↔ funkcja frontu. | — |

---

## 3. Kiedy aktualizować katalogi

| Zdarzenie | Co zaktualizować |
|---|---|
| Nowy/zmieniony endpoint | `KATALOG_API`, proces |
| Zmiana encji/migracja | `SLOWNIK_DANYCH`, `MODEL_DOMENY`, dotknięte procesy |
| Nowy wyjątek / zmiana mapowania | `KATALOG_WYJATKOW`, plik `05` dotkniętych procesów |
| Nowa integracja / zmiana konfiguracji | `ZAGADNIENIA_PRZEKROJOWE` |
| Nowy stały zestaw danych testowych | `KATALOG_DANYCH_TESTOWYCH`, plik `06` procesów |

---

## 4. Relacja katalog ↔ proces

- `KATALOG_API` jest indeksem; szczegóły kontraktu są w pliku `02` procesu.
- `SLOWNIK_DANYCH` jest źródłem prawdy o kolumnach; plik `04` procesu cytuje tylko kolumny, których dotyka, i linkuje do słownika.
- `KATALOG_WYJATKOW` jest źródłem prawdy o mapowaniu wyjątek→HTTP; plik `05` procesu wymienia tylko wyjątki danego procesu i linkuje do katalogu.
- `KATALOG_DANYCH_TESTOWYCH` przechowuje fixture'y współdzielone; plik `06` procesu odwołuje się do nich identyfikatorem `DT-XX` i dokłada dane specyficzne dla procesu.
