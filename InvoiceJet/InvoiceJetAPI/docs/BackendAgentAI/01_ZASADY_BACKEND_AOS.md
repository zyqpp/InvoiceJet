# Zasady backendowej dokumentacji AOS

**Obowiązuje:** Każda sesja generowania dokumentacji backendowej InvoiceJetAPI
**Priorytet:** Nadrzędny dla dokumentów w `docs/aos/backend`
**Powiązane pliki:** `02_SLOWNIK_BACKEND.md`, `03_MARKERY_I_WERYFIKACJA.md`, `04_REGULY_DEKOMPOZYCJI.md`, `05_KATALOGI_PRZEKROJOWE.md`, `AOS_BACKEND_PROCESS_TEMPLATE.md`

---

## 1. Cel dokumentacji

Dokumentacja backendowa AOS opisuje **zaimplementowane zachowanie API** InvoiceJetAPI. Agent opisuje kod źródłowy, nie projekt docelowy.

Dokumentacja ma trzech odbiorców i każdy fragment musi służyć przynajmniej jednemu z nich:

| Odbiorca | Czego potrzebuje | Co z tego wynika dla dokumentu |
|---|---|---|
| **Analityk** | Kontrola, czy aplikacja działa zgodnie z założeniami biznesu. | Cel biznesowy procesu, reguły, warunki, wynik — opisane po polsku, zrozumiale. |
| **Developer** | Zrozumienie, jak działa kod i logika. | Łańcuch wywołań z cytatami kodu, mapowanie pól, zapisy do bazy, transakcje. |
| **Tester** | Źródło wiedzy do testów automatycznych i ręcznych. | Realne dane wejściowe, warunki wstępne, wartości brzegowe, błędy i statusy HTTP. |

Dokumentacja backendowa jest również **wsadem do dokumentacji Fullstack** (łączonej z AOS frontendu). Dlatego musi pokazywać pełny przepływ: od kontraktu API widzianego przez front, przez logikę aplikacyjną, aż do zapytań bazodanowych, tabel i kolumn.

---

## 2. Dziewięć wymiarów opisu

Każdy proces opisujemy wielowymiarowo. Wymiar bez treści dla danego procesu oznacza się markerem „nie dotyczy" (patrz `03_MARKERY_I_WERYFIKACJA.md`), nie pomija się go w ciszy.

| # | Wymiar | Odpowiada na pytanie | Plik docelowy |
|---|---|---|---|
| 1 | API / kontrakt | Co wchodzi i co wychodzi? | `02_KONTRAKT_API` + `KATALOG_API` |
| 2 | Algorytm / przepływ | Co się dzieje po wywołaniu i w jakiej kolejności? | `03_LOGIKA_APLIKACYJNA` |
| 3 | Walidacje i reguły | Na jakiej podstawie powstają błędy i jakie błędy? | `05_BLEDY_BEZPIECZENSTWO` (sekcja „Katalog walidacji") + `KATALOG_WYJATKOW` |
| 4 | Dane / persystencja | Jakie encje, tabele, kolumny, relacje i transakcje? | `04_DANE_MODELE_MAPOWANIA` + `SLOWNIK_DANYCH` |
| 5 | Słowniki / lookupy | Jakie enumy, tabele słownikowe i seed? | `SLOWNIK_DANYCH` |
| 6 | Bezpieczeństwo | Kto może wywołać i jak działa autoryzacja? | `05_BLEDY_BEZPIECZENSTWO` + `ZAGADNIENIA_PRZEKROJOWE` |
| 7 | Integracje | Jakie zewnętrzne systemy i biblioteki? | `ZAGADNIENIA_PRZEKROJOWE` |
| 8 | Dane testowe | Jakimi danymi wywołać i co sprawdzić? | `06_DANE_TESTOWE` + `KATALOG_DANYCH_TESTOWYCH` |
| 9 | Fullstack (odłożone) | Jak proces wiąże się z funkcją frontu? | `MAPA_FULLSTACK` |

---

## 3. Zakres

Zakres obejmuje:

- endpointy ASP.NET Core, kontrolery, atrybuty routingu,
- autoryzację przez `Authorize` i obsługę tokenu JWT,
- DTO żądania i odpowiedzi oraz ich pola,
- serwisy aplikacyjne i pełny algorytm wykonania procesu,
- walidacje, reguły biznesowe i warunki powstawania błędów,
- mapowanie `AutoMapper`,
- encje domenowe oraz ich odwzorowanie na tabele i kolumny (EF Core, snapshot migracji),
- repozytoria, zapytania LINQ i `IUnitOfWork` (transakcje, `CompleteAsync()`),
- wyjątki domenowe i `ExceptionMiddleware`,
- enumy i tabele słownikowe oraz dane z `DbSeeder`,
- integracje techniczne (ANAF, QuestPDF).

Zakres nie obejmuje:

- układu ekranów frontendu, selektorów CSS, zachowania komponentów Angular,
- założeń biznesowych niewidocznych w kodzie backendu,
- mostu do AOS frontendu (`MAPA_FULLSTACK`) — odłożone do osobnego etapu.

---

## 4. Zasady absolutne

| Kod | Zasada | Opis |
|---|---|---|
| ZB.1 | Kod jest źródłem prawdy | Agent opisuje tylko zachowanie potwierdzone w plikach backendu. |
| ZB.2 | Endpoint jest początkiem procesu | Proces zaczyna się od kontrolera i metody HTTP. |
| ZB.3 | Serwis jest miejscem logiki aplikacyjnej | Reguły wykonania procesu opisuje się na podstawie klasy z `Services/Impl`. |
| ZB.4 | Nie zgadywać kontraktu API | Pola żądania i odpowiedzi opisuje się na podstawie DTO oraz sygnatur kontrolera. |
| ZB.5 | Błędy opisywać przez kod | Status HTTP wynika z kontrolera lub `ExceptionMiddleware`. |
| ZB.6 | Każde twierdzenie ma kotwicę | Każda informacja techniczna wskazuje źródło w formacie `Plik.cs › Klasa.Metoda` i — dla logiki — zawiera krótki cytat kodu. |
| ZB.7 | Algorytm opisujemy po kolei | Plik `03` opisuje uporządkowaną sekwencję: walidacje → logika biznesowa → zapisy do bazy → odpowiedź. Kolejność musi odpowiadać kodowi. |
| ZB.8 | Schodzimy do kolumn | Plik `04` opisuje encje aż do poziomu kolumn (typ, nullability, klucze, indeksy, kaskady) na podstawie snapshotu migracji. |
| ZB.9 | Walidacja jest jawna | Każda reguła walidacji ma: podstawę w kodzie, warunek wyzwolenia, powstający wyjątek i status HTTP. |
| ZB.10 | Nie chudziej niż checklista | Każda sekcja musi spełnić „definicję ukończenia" z `03_MARKERY_I_WERYFIKACJA.md`. Brak danych oznacza się markerem, nie pominięciem. |

---

## 5. Zasada kotwiczenia (ZB.6 w praktyce)

Format kotwicy: `` `Plik.cs › Klasa.Metoda` `` (ścieżka względem korzenia projektu lub sama nazwa pliku, jeśli jednoznaczna).

Dla każdego twierdzenia o logice dołącza się **krótki cytat kodu** w bloku ```` ```csharp ````, ograniczony do fragmentu istotnego dla twierdzenia. Numery linii są opcjonalne (kod się zmienia), symbol jest obowiązkowy.

Przykład poprawnego zakotwiczenia:

> Serwis pobiera aktywną firmę użytkownika. Źródło: `DocumentService.cs › DocumentService.AddDocument`.
>
> ```csharp
> var userFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
> if (userFirmId is null)
>     throw new UserHasNoAssociatedFirmException();
> ```

---

## 6. Ton i styl

Dokument jest formalny, rzeczowy i bezosobowy. Nazwy klas, metod, endpointów, DTO, pól, tabel i kolumn zapisuje się w oryginalnym brzmieniu w backtickach.

Opis biznesowy jest po polsku. Opis techniczny zachowuje nazwy z kodu.

---

## 7. Reguła braku interpretacji

Jeżeli kod zawiera niespójność, agent oznacza ją markerem `[UWAGA: ... — WYMAGA WERYFIKACJI Z ZESPOŁEM]` (pełna lista markerów w `03_MARKERY_I_WERYFIKACJA.md`).

Agent nie zapisuje, że kod działa inaczej niż wynika z implementacji.

- Źle: `Endpoint waliduje wymagane pola dokumentu, mimo że nie wynika to z kodu.`
- Dobrze: `DTO nie zawiera atrybutów walidacyjnych. [UWAGA: walidacja pól wejściowych nie jest widoczna w DTO — WYMAGA WERYFIKACJI Z ZESPOŁEM]`

---

## 8. Wzorzec jakości

W tej wersji frameworka **nie istnieje wzorcowy proces referencyjny**. Stare procesy `P-01`..`P-19` zostały zarchiwizowane (`docs/aos/backend/_archive/`) — powstały na poprzedniej, chudej wersji szablonów i **nie spełniają** nowego kontraktu wyjścia.

Źródłem prawdy o jakości są:

- **Szablony** z `docs/aos/backend/templates/` — instrukcje w komentarzach `<!-- ... -->` i pola obowiązkowe.
- **Definicja Ukończenia per plik** w `03_MARKERY_I_WERYFIKACJA.md` (sekcja 3) — checklista, którą każdy plik musi spełnić.
- **Zasady absolutne `ZB.1`–`ZB.10`** z sekcji 4 niniejszego dokumentu.

Pierwszy proces dokumentowany wg nowych szablonów staje się **roboczym wzorcem** dla kolejnych — pod warunkiem, że przeszedł review zespołu. Do tego czasu agent nie odwołuje się do żadnego procesu jako wzorca; opiera się wyłącznie na szablonach i Definicjach Ukończenia.
