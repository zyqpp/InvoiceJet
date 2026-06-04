# Markery i weryfikacja backendu

**Obowiązuje:** Dokumentacja AOS backendu InvoiceJetAPI

---

## 1. Markery

| Sytuacja | Marker |
|---|---|
| Informacja nie wynika z plików backendu | `[WYMAGA WERYFIKACJI]` |
| Kod zawiera potencjalną niespójność | `[UWAGA: opis — WYMAGA WERYFIKACJI Z ZESPOŁEM]` |
| Zachowanie wynika tylko z frontendu | `[POZA ZAKRESEM BACKENDU]` |
| Sekcja nie dotyczy procesu | `> Sekcja nie dotyczy tego procesu. [powód]` |
| Wymiar pusty mimo obowiązku | `> Wymiar nie występuje w tym procesie. [powód, np. proces nie zapisuje danych]` |

Marker jest jedyną dozwoloną formą „luki". Pominięcie sekcji bez markera traktuje się jako błąd dokumentu.

---

## 2. Zakazane sformułowania

Nie używać bez markera:

- `prawdopodobnie`, `wydaje się`, `możliwe że`, `powinno`, `należałoby`, `zakładam`, `typowo`, `standardowo`, `itd.`, `itp.`.

Każde takie słowo sygnalizuje interpretację zamiast faktu z kodu.

---

## 3. Definicja ukończenia (Definition of Done) per plik

Plik jest gotowy dopiero, gdy spełnia WSZYSTKIE punkty swojej checklisty. To jest mechanizm wymuszający stałą jakość (zasada ZB.10).

### `00_METADANE.md`
- [ ] Wypełnione: proces, numer `P-XX`, kontroler(y), serwis(y), metody serwisu.
- [ ] Lista wszystkich endpointów procesu (nie tylko głównego).
- [ ] DTO żądania i odpowiedzi, encje, repozytoria, wyjątki, integracje.
- [ ] Autoryzacja (atrybut i rola) lub `N/D` z uzasadnieniem.
- [ ] Status dokumentu, data, autor.

### `01_PRZEGLAD_PROCESU.md`
- [ ] Cel **biznesowy** (dla analityka), nie tylko techniczny.
- [ ] Diagram `mermaid` odzwierciedlający rzeczywisty przepływ (gałęzie błędów też).
- [ ] Tabela warunków wejściowych z kolumną „źródło w kodzie".
- [ ] Tabela wyników (sukces, skutki w bazie, błąd).
- [ ] Sekcja „Reguły biznesowe" — co proces gwarantuje lub wymusza.
- [ ] Sekcja „Uwagi wynikające z kodu" z markerami dla niespójności.

### `02_KONTRAKT_API.md`
- [ ] **Osobny blok dla każdego endpointu** procesu.
- [ ] Metoda HTTP, ścieżka, parametry trasy/zapytania, źródło (`[FromBody]`/`[FromRoute]`).
- [ ] Przykład **konkretnego** JSON żądania (realne wartości, nie placeholdery).
- [ ] Przykład **konkretnego** JSON odpowiedzi.
- [ ] Komplet statusów HTTP z warunkiem każdego.

### `03_LOGIKA_APLIKACYJNA.md`
- [ ] Uporządkowany algorytm: walidacje → logika → zapisy → odpowiedź (zasada ZB.7).
- [ ] Każdy istotny krok ma **cytat kodu** i kotwicę `Plik.cs › Klasa.Metoda` (ZB.6).
- [ ] Tabela `pole encji → źródło` dla tworzonych/aktualizowanych encji.
- [ ] Opis każdego `CompleteAsync()` i granic transakcji.
- [ ] Sekcja „Uwagi techniczne" z markerami (np. brak jawnej transakcji, podwójny zapis).

### `04_DANE_MODELE_MAPOWANIA.md`
- [ ] DTO wejściowe i wyjściowe z listą pól i typów.
- [ ] Encje z tabelą **kolumn**: nazwa, typ SQL, nullability, klucz/indeks (na podstawie snapshotu migracji) (ZB.8).
- [ ] Relacje (FK, kierunek, kaskady) i indeksy unikalne.
- [ ] Profile `AutoMapper` (źródło → cel → profil) z uwagami o nietypowych mapowaniach.
- [ ] Istotne zapytania LINQ/SQL wykonywane przez proces.
- [ ] Użyte enumy i lookupy z odniesieniem do `SLOWNIK_DANYCH`.

### `05_BLEDY_BEZPIECZENSTWO.md` (walidacje + błędy + bezpieczeństwo)
- [ ] **Katalog walidacji**: `WAL-XX` | reguła | podstawa w kodzie | warunek wyzwolenia | wyjątek | status HTTP | komunikat (ZB.9).
- [ ] Tabela błędów: wyjątek → status HTTP → źródło (kontroler lub `ExceptionMiddleware`).
- [ ] Odnotowanie wyjątków **niemapowanych** jawnie (skutkujących `500`).
- [ ] Autoryzacja: atrybut, rola, źródło tożsamości użytkownika.
- [ ] Uwagi bezpieczeństwa (np. własny `try/catch` omijający middleware).

### `06_SCENARIUSZE_TESTOWE.md` (dane testowe — realne wartości)
- [ ] Zestaw **poprawnych** danych wejściowych (realne wartości) z warunkami wstępnymi.
- [ ] Zestawy **niepoprawnych** danych — po jednym na regułę walidacji `WAL-XX`, z oczekiwanym błędem i statusem.
- [ ] Wartości brzegowe (puste, maksymalne, `null`, duplikaty wobec indeksów unikalnych).
- [ ] Warunki wstępne / seed potrzebny, aby dane zadziałały, z odwołaniem do `KATALOG_DANYCH_TESTOWYCH`.
- [ ] Oczekiwany rezultat dla każdego zestawu (status + skutek w bazie/odpowiedzi).

### `HISTORIA_ZMIAN.md`
- [ ] Co najmniej wpis wersji `1.0` z datą, autorem i opisem.

---

## 4. Obowiązkowa weryfikacja procesu (przed oddaniem)

Agent sprawdza:

- czy endpointy istnieją w kontrolerze i zgadzają się metody/ścieżki z atrybutami,
- czy atrybut `Authorize` został opisany,
- czy DTO żądania i odpowiedzi są wskazane,
- czy serwis aplikacyjny i metody serwisu są wskazane z kotwicami,
- czy algorytm w `03` jest uporządkowany i ma cytaty kodu,
- czy `04` schodzi do kolumn na podstawie snapshotu migracji,
- czy każda reguła walidacji ma wyjątek i status,
- czy wyjątki są zgodne z `ExceptionMiddleware` (w tym niemapowane → `500`),
- czy dane testowe są konkretne i wykonalne,
- czy dokument nie opisuje zachowania frontendu,
- czy każdy plik przeszedł swoją Definicję ukończenia z sekcji 3.
