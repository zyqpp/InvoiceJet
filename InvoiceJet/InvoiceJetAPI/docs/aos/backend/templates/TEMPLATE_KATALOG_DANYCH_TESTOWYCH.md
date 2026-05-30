<!--
SZABLON KATALOG_DANYCH_TESTOWYCH — globalne fixture'y wielokrotnego użytku.
Plik docelowy: docs/aos/backend/KATALOG_DANYCH_TESTOWYCH.md
Procesy odwołują się do tych fixture'ów po ID `DT-XX` (z plików 06).
Nie powtarzaj tu danych specyficznych dla jednego procesu.
-->

# Katalog danych testowych — InvoiceJetAPI

**Data aktualizacji:** RRRR-MM-DD
**Cel:** Wielokrotnie używane fixture'y / seed danych do testów .NET, API, E2E i testów ręcznych.

---

## 1. Spis fixture'ów

| ID | Nazwa | Krótki opis | Wymagane przez |
|---|---|---|---|
| `DT-01` | [np. Użytkownik standardowy + JWT] | [opis] | `P-01`, `P-06`, … |
| `DT-02` | [np. Użytkownik bez aktywnej firmy] | [opis] | `P-01` (negatywne) |
| `DT-03` | [np. Aktywna firma użytkownika] | [opis] | `P-01`, `P-13`, … |
| `DT-04` | [np. Aktywne konto bankowe firmy] | [opis] | `P-01` |
| `DT-05` | [np. Seria dokumentów Invoice] | [opis] | `P-01` |
| `DT-06` | [np. Produkt z UnitPrice=100] | [opis] | `P-01`, `P-09` |

---

## 2. Szczegóły fixture'ów

### `DT-01` — [Nazwa]

Cel: [do czego służy]

Dane:
```json
{
  "email": "tester+01@example.com",
  "firstName": "Test",
  "lastName": "User",
  "password": "Strong!123",
  "role": "User"
}
```

Sposób przygotowania:
- Wariant A (test integracyjny .NET): seed w `WebApplicationFactory` przez `DbContext`.
- Wariant B (API black-box): wywołanie `POST /api/Auth/register` z powyższym body, potem `POST /api/Auth/login` po `token`.
- Wariant C (E2E / manual): zarejestrować ręcznie przez UI Angular.

Zależności: brak.

Sprzątanie: usunięcie rekordu `User` po teście.

---

### `DT-XX` — [...]

[powiel powyższą strukturę dla każdego fixture'u]

---

## 3. Konwencje danych

- E-maile testowe: `tester+<numer>@example.com` (lokalna część `tester+NN` minimalizuje konflikty).
- Hasła testowe: `Strong!123` (spełnia wymagany regex).
- Identyfikatory firm (`CUI`) testowe ANAF: [wpisz konkretne, działające w środowisku testowym].
- Rachunki bankowe (`IBAN`) testowe: [konkretne, walidujące się].

---

## 4. Powiązanie z seedem produkcyjnym (`DbSeeder`)

| Element seedu | Plik | Czy potrzebny w testach? |
|---|---|---|
| Typy dokumentów (Invoice/Proforma/Storno) | `DbSeeder.cs › SeedDocumentTypes` | tak — używany przez `P-01`, `P-13`, … |
