# Słownik anomalii — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Skonsolidowana lista wszystkich zidentyfikowanych anomalii w systemie InvoiceJet, pogrupowana według kategorii i ważności.

---

## KRYTYCZNE (mogą powodować utratę danych lub naruszenie integralności)

| ID | Opis | Plik | Dotyczy |
|---|---|---|---|
| A-KRIT-01 | **CASCADE DELETE konta bankowego usuwa wszystkie powiązane dokumenty** — brak ostrzeżenia w UI | `BankAccountController`, `BankAccountService` | P-05, EKRAN-06 |
| A-KRIT-02 | **`TransformToStorno` — `CompleteAsync()` wewnątrz pętli** — brak atomowości; możliwa częściowa konwersja | `DocumentService.TransformToStorno()` | P-15, ALG-08 |
| A-KRIT-03 | **Race condition na `DocumentSeries.CurrentNumber`** — możliwe duplikaty numerów dokumentów przy równoległych żądaniach | `DocumentService.AddDocument()` | P-08, ALG-02 |
| A-KRIT-04 | **`GenerateInvoicePdf` hardkoduje `new InvoiceDocument()`** — proformy i storna generują PDF jako zwykła faktura | `DocumentService.GenerateInvoicePdf()` | P-12, ALG-07 |

---

## WYSOKIE (błędy logiczne lub bezpieczeństwo)

| ID | Opis | Plik | Dotyczy |
|---|---|---|---|
| A-WYS-01 | **JWT wygasa po 10 minutach** — brak refresh token; każda przerwa kończy sesję | `AuthService.CreateToken()` | ALG-04 |
| A-WYS-02 | **Token w localStorage** — podatny na XSS | `JwtInterceptor` | ALG-01 |
| A-WYS-03 | **`ValidateIssuer=false`, `ValidateAudience=false`** — słabsza weryfikacja JWT | `Program.cs` | ALG-01 |
| A-WYS-04 | **Brak weryfikacji własności zasobów** — wystarczy znać ID by edytować cudzy zasób | `BankAccountService`, `ProductService` | P-05, P-06 |
| A-WYS-05 | **`Product.Name` UNIQUE INDEX globalny** — dwóch użytkowników nie może mieć produktu o tej samej nazwie | DB Snapshot | P-06, DTO-05 |
| A-WYS-06 | **Catch-all 500 zwraca `ex.Message`** — ujawnia szczegóły błędów w produkcji | `ExceptionMiddleware` | ALG-09 |
| A-WYS-07 | **CORS tylko dla localhost:4200** — brak produkcyjnego origina frontendu | `Program.cs` | 00_meta |
| A-WYS-08 | **Brak server-side invalidation tokenu** — wylogowanie tylko lokalne | `NavbarComponent` | ALG-01 |

---

## ŚREDNIE (błędy funkcjonalne lub degradacja UX)

| ID | Opis | Plik | Dotyczy |
|---|---|---|---|
| A-SR-01 | **`isFormChanged()` w FirmDetailsComponent zawsze zwraca `false`** — przycisk Save zawsze aktywny | `firm-details.component.ts` | EKRAN-04 |
| A-SR-02 | **`console.log()` aktywne w produkcji** (invoiceAmounts, incomeAmounts) | `dashboard.component.ts` | EKRAN-03 |
| A-SR-03 | **Brak paginacji na listach** — GetTableRecords zwraca wszystkie rekordy | `DocumentService` | P-10 |
| A-SR-04 | **`monthlyTotals` bez pustych miesięcy** — wykres liniowy nie pokazuje 12 punktów | `DocumentService` | P-14 |
| A-SR-05 | **`addNewClient()` niezaimplementowana** — tylko `console.log` | `firm-details.component.ts` | EKRAN-04 |
| A-SR-06 | **Brak timeout HttpClient dla ANAF** — możliwe blokowanie wątków | `FirmService.GetFirmDataFromAnaf()` | ALG-06 |
| A-SR-07 | **Dokumenty bez własnego `DocumentSeriesId`** — frontend przekazuje `CurrentNumber` z pamięci | `DocumentService.AddDocument()` | P-08 |
| A-SR-08 | **Dwa osobne `CompleteAsync()` przy AddDocument** — niespójna transakcja | `DocumentService.AddDocument()` | P-08 |

---

## NISKIE (stylistyczne, jakość kodu, UX)

| ID | Opis | Dotyczy |
|---|---|---|
| A-NIS-01 | `int[]` bez `[FromBody]` w kontrolerze (Delete, TransformToStorno) | P-11, P-15 |
| A-NIS-02 | Własne try/catch w kontrolerach obok ExceptionMiddleware | `DocumentController`, `BankAccountController` |
| A-NIS-03 | Inline LINQ projekcja w AutoMapper profilu zamiast osobnego mapowania | AM-06 |
| A-NIS-04 | Null-forgiving operator `!` bez guard clause | `UserFirmProfile`, `DocumentProfile` |
| A-NIS-05 | Brak `AsNoTracking()` w zapytaniach read-only | Repozytoria |
| A-NIS-06 | Brak cache dla ANAF | `FirmService` |
| A-NIS-07 | Brak sortowania na listach | Repozytoria |
| A-NIS-08 | Sidebar bez responsywności (brak mobile support) | `SidebarComponent` |

---

## Podsumowanie

| Kategoria | Liczba anomalii |
|---|---|
| Krytyczne | 4 |
| Wysokie | 8 |
| Średnie | 8 |
| Niskie | 8 |
| **ŁĄCZNIE** | **28** |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — skonsolidowane anomalie z całej dokumentacji. |
