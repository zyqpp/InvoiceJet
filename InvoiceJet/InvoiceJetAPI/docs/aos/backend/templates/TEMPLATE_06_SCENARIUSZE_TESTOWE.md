<!--
SZABLON 06 — DANE TESTOWE (uwaga: nazwa pliku zachowana; akcent: REALNE DANE, nie skrypty testów)
Cel: dać testerowi i developerowi materiał, którego MOŻNA UŻYĆ — w testach .NET, API, E2E
lub klikaniu z palca. NIE piszemy tu kodu testów ani struktury frameworka testowego.
Definicja ukończenia: 03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Dane testowe

## 1. Warunki wstępne (preconditions / seed)
<!-- Co musi istnieć w bazie / kontekście, żeby ten proces dało się uruchomić. Linkuj do KATALOG_DANYCH_TESTOWYCH. -->

| Wymóg | Skąd | Identyfikator fixture'u |
|---|---|---|
| [Zalogowany użytkownik z rolą `User`] | seed / rejestracja | `DT-01` |
| [Aktywna firma użytkownika] | seed | `DT-03` |
| [...] | [...] | [...] |

## 2. Dane poprawne (happy path)
<!-- Realne payloady, kompletne, gotowe do wklejenia w Postman/.http/test. -->

### `TC-01` — [opis]
Warunki wstępne: `DT-01`, `DT-03`.

Żądanie:
```json
{
  "pole": "realna wartość"
}
```

Oczekiwany rezultat:
- Status: `200 OK`
- Odpowiedź: [opis / fragment JSON]
- Skutek w bazie: [konkretny zapis, np. „nowy rekord w `Document` z `DocumentStatusId=1`"]

## 3. Dane niepoprawne (po jednej na regułę walidacji)
<!-- Dla każdego WAL-XX z pliku 05 — zestaw danych wymuszający TEN błąd. -->

### `TC-N01` — łamie `WAL-01`: [reguła]
Żądanie:
```json
{ "pole": "[wartość łamiąca regułę]" }
```
Oczekiwany rezultat:
- Status: `400 Bad Request`
- Komunikat: `[treść z exception.Message]`
- Skutek w bazie: brak zmian

## 4. Wartości brzegowe
<!-- Granice typów i ograniczeń DB: puste stringi, null, zero, wartości maksymalne, duplikaty wobec indeksów unikalnych. -->

| ID | Pole | Wartość brzegowa | Oczekiwany rezultat |
|---|---|---|---|
| `TC-B01` | `[Field]` | `""` | [status + uzasadnienie] |
| `TC-B02` | `[Field]` | `null` | [status] |
| `TC-B03` | `[Field]` | [duplikat względem indeksu unikalnego] | [status] |

## 5. Skrót zależności

| Identyfikator | Opis | Wykorzystany w |
|---|---|---|
| `DT-XX` | [opis fixture'u z katalogu globalnego] | `TC-01`, `TC-N01` |

---
<!-- ===== PRZYKŁAD (P-01) — usuń przed oddaniem =====
TC-01 — Wystawienie faktury (happy path). Preconditions: DT-01 (user+JWT), DT-03 (UserFirm), DT-04 (BankAccount active), DT-05 (DocumentSeries).
Żądanie: pełen JSON DocumentRequestDto z 1 pozycją produktu. Oczekiwany rezultat: 200 OK; nowy rekord Document; DocumentSeries.CurrentNumber +1.
TC-N01 — łamie WAL-01: użytkownik bez aktywnej firmy → 400, "User has no associated firm.".
TC-B03 — Product.Name duplikat (indeks unikalny) → wyjątek DB, status zależy od mapowania.
[UWAGA: niespójne sumy gdy lista Products zawiera id=0 dla nowego produktu — WYMAGA WERYFIKACJI Z ZESPOŁEM]
===== KONIEC PRZYKŁADU ===== -->
