# Zasady backendowej dokumentacji AOS

**Obowiązuje:** Każda sesja generowania dokumentacji backendowej InvoiceJetAPI
**Priorytet:** Nadrzędny dla dokumentów w `docs/aos/backend`

---

## 1. Zakres dokumentacji backendowej

Dokumentacja backendowa opisuje zaimplementowane zachowanie API. Agent opisuje kod źródłowy, nie projekt docelowy.

Zakres obejmuje:

- endpointy ASP.NET Core,
- kontrolery i atrybuty routingu,
- autoryzację przez `Authorize`,
- DTO żądania i odpowiedzi,
- serwisy aplikacyjne,
- mapowanie `AutoMapper`,
- encje domenowe,
- repozytoria i `IUnitOfWork`,
- zapis przez EF Core,
- wyjątki i `ExceptionMiddleware`,
- integracje techniczne, na przykład ANAF i QuestPDF.

Zakres nie obejmuje:

- układu ekranów frontendu,
- selektorów CSS,
- zachowania komponentów Angular,
- założeń biznesowych niewidocznych w kodzie backendu.

---

## 2. Zasady absolutne

| Kod | Zasada | Opis |
|---|---|---|
| ZB.1 | Kod jest źródłem prawdy | Agent opisuje tylko zachowanie potwierdzone w plikach backendu. |
| ZB.2 | Endpoint jest początkiem procesu | Proces zaczyna się od kontrolera i metody HTTP. |
| ZB.3 | Serwis jest miejscem logiki aplikacyjnej | Reguły wykonania procesu opisuje się na podstawie klasy z `Services/Impl`. |
| ZB.4 | Nie zgadywać kontraktu API | Pola żądania i odpowiedzi opisuje się na podstawie DTO oraz sygnatur kontrolera. |
| ZB.5 | Błędy opisywać przez kod | Status HTTP wynika z kontrolera lub `ExceptionMiddleware`. |

---

## 3. Ton i styl

Dokument jest formalny, rzeczowy i bezosobowy. Nazwy klas, metod, endpointów, DTO i pól są zapisywane w oryginalnym brzmieniu w backtickach.

Opis biznesowy jest po polsku. Opis techniczny zachowuje nazwy z kodu.

---

## 4. Reguła braku interpretacji

Jeżeli kod zawiera niespójność, agent oznacza ją markerem `[UWAGA: ... — WYMAGA WERYFIKACJI Z ZESPOŁEM]`.

Agent nie zapisuje, że kod działa inaczej niż wynika z implementacji.

Przykład:

- Źle: `Endpoint waliduje wymagane pola dokumentu, mimo że nie wynika to z kodu.`
- Dobrze: `DTO nie zawiera atrybutów walidacyjnych. [UWAGA: walidacja pól wejściowych nie jest widoczna w DTO — WYMAGA WERYFIKACJI Z ZESPOŁEM]`
