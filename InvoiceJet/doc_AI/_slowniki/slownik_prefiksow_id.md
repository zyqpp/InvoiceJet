# S-05. Słownik prefiksów identyfikatorów — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| ID | S-05 |
| Nazwa | Słownik prefiksów identyfikatorów |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Data | 2026-05-31 |
| Status | Szkic |
| Plik | `doc_AI/_slowniki/slownik_prefiksow_id.md` |

## Streszczenie

Słownik definiuje zamkniętą listę prefiksów identyfikatorów używanych w całej dokumentacji AOS projektu InvoiceJet. Format identyfikatora: `<PREFIKS>-<RodzicNazwa>-<Nazwa>` lub `<PREFIKS>-<Nazwa>` dla artefaktów bez rodzica. Spójna konwencja prefiksów umożliwia jednoznaczne linkowanie między dokumentami i mapami krzyżowymi bez ryzyka kolizji nazw.

---

## Format identyfikatora

```
<PREFIKS>-<RodzicNazwa>-<Nazwa>
```

- `PREFIKS` — typ artefaktu (z poniższej tabeli, zawsze WIELKIE LITERY lub z łącznikiem)
- `RodzicNazwa` — nazwa kontekstu nadrzędnego (ekran, encja, proces) — PascalCase, bez spacji
- `Nazwa` — nazwa konkretnego artefaktu — PascalCase, bez spacji, bez polskich znaków diakrytycznych

Przykład: `POLE-Login-Email` = pole o nazwie Email, należące do ekranu Login.

---

## Tabela prefiksów

| Prefiks | Typ dokumentu / artefaktu | Przykład ID | Powiązany typ artefaktu |
|---|---|---|---|
| `EKRAN` | Ekran Angular (komponent z trasą routingową) | `EKRAN-Login` | Komponent `.ts` + szablon `.html` |
| `POLE` | Pole formularza lub kolumna tabeli w UI | `POLE-Login-Email` | Formant Angular Material |
| `OP` | Operacja użytkownika (przycisk, link, skrót) | `OP-Login-Zaloguj` | Metoda w komponencie Angular |
| `FILTR` | Filtr listy / tabeli w UI | `FILTR-Faktury-TypDokumentu` | Pole formularza filtrów |
| `TAB` | Tabela / lista danych w UI (grid) | `TAB-Faktury-Lista` | `MatTable` lub podobny komponent |
| `MODAL` | Modal / dialog nakładkowy | `MODAL-Klienci-DodajKlienta` | `MatDialog` Angular Material |
| `POW` | Powiadomienie (toast, snackbar, alert) | `POW-Faktury-ZapisanoFakture` | `MatSnackBar` Angular Material |
| `PROC` | Proces techniczny (backend: kontroler → serwis → repo → DB) | `PROC-Rejestracja` | Metoda serwisu + ścieżka wywołań |
| `ALG` | Algorytm (procedura obliczeniowa lub decyzyjna) | `ALG-WalidacjaHasla` | Metoda lub blok logiki w kodzie |
| `API` | Endpoint API (metoda HTTP + URL + DTO żądania + DTO odpowiedzi) | `API-PostAuthRegister` | Metoda kontrolera ASP.NET Core |
| `INT` | Integracja zewnętrzna (serwis trzeci) | `INT-ANAF` | HttpClient + zewnętrzny serwis |
| `TAB-DB` | Tabela bazy danych (encja EF Core) | `TAB-DB-Document` | Klasa encji + migracja EF Core |
| `DTO` | Data Transfer Object | `DTO-RegisterUserDto` | Klasa C# `*Dto.cs` |
| `LINQ` | Zapytanie LINQ / EF Core | `LINQ-GetDocumentById` | Wyrażenie LINQ w repozytorium |
| `SKRYPT` | Skrypt bazodanowy lub seeder danych | `SKRYPT-DbSeeder` | Plik `.sql` lub klasa seeder C# |
| `ROLA` | Rola użytkownika systemu | `ROLA-User` | Claim `role` w JWT |
| `UPR` | Uprawnienie (granularne prawo dostępu) | `UPR-ZarzadzajFakturami` | Atrybut `[Authorize]` lub polityka |
| `UC` | Przypadek użycia (scenariusz interakcji aktora z systemem) | `UC-WystawienieFaktury` | Dokument UC |
| `KLASA-BIZ` | Klasa biznesowa (encja domenowa lub serwis domenowy) | `KLASA-BIZ-Dokument` | Klasa C# w warstwie Domain |
| `BPMN` | Proces biznesowy w notacji BPMN | `BPMN-WystawienieFaktury` | Diagram BPMN |
| `TEST` | Scenariusz testowy | `TEST-Rejestracja-SzczesliwaSciezka` | Dokument scenariusza testowego |

---

## Reguły konwencji

1. **Wielkie litery prefiksu** — prefiks zawsze pisany wielkimi literami: `EKRAN`, `PROC`, `ALG`. Wyjątek: złożone prefiksy z łącznikiem: `TAB-DB`, `KLASA-BIZ`.
2. **PascalCase bez spacji** — `RodzicNazwa` i `Nazwa` pisane PascalCase, bez spacji, bez polskich znaków diakrytycznych (`Faktura` nie `Faktura`; `SzczesliwaSciezka` nie `Szczęśliwa ścieżka`).
3. **Unikalność w obrębie prefiksu** — identyfikator musi być unikalny w obrębie swojego prefiksu. Kolizje rozwiązywane przez uszczegółowienie `Nazwy`.
4. **Stabilność po nadaniu** — raz nadany identyfikator nie zmienia się. Zmiana niszczy linki w dokumentacji.
5. **Lista zamknięta** — nowe prefiksy dodawane wyłącznie przez aktualizację tego słownika i pliku `wytyczne/04_jezyk_styl_i_konwencje.md`.

---

## Prefiksy z poprzedniej konwencji (do ujednolicenia)

Poniższe prefiksy używane są w `slownik_pojec.md` i mogą wymagać migracji do konwencji powyżej:

| Stary prefiks | Nowy prefiks | Uwaga |
|---|---|---|
| `DIALOG-XX` | `MODAL-` | Ujednolicić — oba oznaczają modalne okno dialogowe |
| `LAYOUT-XX` | Brak odpowiednika | Do_zdefiniowania — czy layout to ekran bez trasy? |
| `BASE-XX` | `KLASA-BIZ-` | Klasa abstrakcyjna / bazowa komponentu Angular |
| `AM-XX` | Brak odpowiednika | AutoMapper Profile — rozważyć nowy prefiks `MAPPER-` |
| `WAL-XX` | Brak odpowiednika | Walidacja / reguła biznesowa — rozważyć prefiks `WAL-` |
| `LT-XX` | Brak odpowiednika | Dług techniczny — rozważyć prefiks `LT-` |
| `FA-XX` | Brak odpowiednika | Anomalia funkcjonalna — rozważyć prefiks `ANO-F-` |
| `DA-XX` | Brak odpowiednika | Anomalia danych — rozważyć prefiks `ANO-D-` |
| `DT-XX` | Brak odpowiednika | Dane testowe (fixture) — rozważyć prefiks `FIXTURE-` |
| `P-XX` | `PROC-` | Stary prefiks procesów technicznych w dokumentacji backendowej |

---

## Wątpliwości i braki

| ID | Wątpliwość | Status |
|---|---|---|
| W-01 | Brak prefiksu dla AutoMapper Profile (`AM-XX`) w nowej konwencji. Wymaga decyzji: dodać `MAPPER-` czy zlikwidować osobny prefiks. | Do_zdefiniowania |
| W-02 | `LAYOUT-XX` (Navbar, Sidebar) — czy traktować jako osobny prefiks, czy scalić z `EKRAN-`? | Do_zdefiniowania |
| W-03 | `WAL-XX` (walidacje/reguły biznesowe) — brak odpowiednika w nowej konwencji. Wytyczne nie wymieniają tego prefiksu jawnie. | Do_zdefiniowania |
| W-04 | Migracja starych identyfikatorów (`P-08`, `ALG-04` itp.) z istniejącej dokumentacji backendowej do nowej konwencji — zakres pracy niezdefiniowany. | Do_zdefiniowania |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 21 prefiksów w tabeli głównej + 10 starych do ujednolicenia. |
