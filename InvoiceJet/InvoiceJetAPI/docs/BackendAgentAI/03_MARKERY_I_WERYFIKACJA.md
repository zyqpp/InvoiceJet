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

---

## 2. Zakazane sformułowania

Nie używać bez markera:

- `prawdopodobnie`,
- `wydaje się`,
- `możliwe że`,
- `powinno`,
- `należałoby`,
- `zakładam`,
- `typowo`,
- `standardowo`,
- `itd.`,
- `itp.`.

---

## 3. Obowiązkowa weryfikacja procesu

Przed oddaniem procesu agent sprawdza:

- czy endpoint istnieje w kontrolerze,
- czy metoda HTTP i ścieżka są zgodne z atrybutami,
- czy atrybut `Authorize` został opisany,
- czy DTO żądania i odpowiedzi są wskazane,
- czy serwis aplikacyjny i metoda serwisu są wskazane,
- czy zapis przez `IUnitOfWork.CompleteAsync()` został opisany,
- czy wyjątki są zgodne z `ExceptionMiddleware`,
- czy dokument nie opisuje zachowania frontendu.
