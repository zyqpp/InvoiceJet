# Plan testów — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Stan testów w projekcie

**Aktualny stan:** Brak testów automatycznych — zarówno po stronie backendu jak i frontendu. Wszystkie testy są manualne.

## Priorytetowe scenariusze testowe

### Testy krytycznych anomalii

#### TC-01: CASCADE DELETE konta bankowego

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | Utwórz konto bankowe | Konto widoczne w liście |
| 2 | Utwórz fakturę z tym kontem | Faktura zapisana |
| 3 | Usuń konto bankowe | **Bug: faktura zostaje usunięta!** |
| 4 | Sprawdź listę faktur | Faktura zniknęła |

#### TC-02: Race condition numeracji (trudny do przetestowania manualnie)

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | Przygotuj serię z CurrentNumber=5 | Seria dostępna |
| 2 | Jednocześnie wyślij 2 żądania POST /Document/Add | Dwie faktury o różnych numerach |
| 3 | Sprawdź numery dokumentów | **Bug: możliwe 2x FV0005** |

#### TC-03: GenerateInvoicePdf generuje niepoprawny typ

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | Utwórz proformę | Proforma widoczna |
| 2 | Wywołaj POST /Document/GenerateInvoicePdf | PDF wygenerowany |
| 3 | Sprawdź tytuł dokumentu w PDF | **Bug: "Factura" zamiast "Factura Proforma"** |

### Testy happy path

#### TC-10: Rejestracja i pierwsze logowanie

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | POST /api/Auth/register z poprawnymi danymi | 200 OK + token |
| 2 | Odczytaj JWT z response | Zawiera userId, firstName, email |
| 3 | GET /api/Firm/GetUserActiveFirm z tokenem | 200 OK + null (brak firmy) |

#### TC-11: Pełny cykl faktury

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | Dodaj firmę | 201 Created |
| 2 | Dodaj konto bankowe | 201 Created |
| 3 | Dodaj serię FV (currentNumber=1) | 201 Created |
| 4 | Dodaj klienta | 201 Created |
| 5 | POST /Document/Add (faktura) | 201 Created, number=FV0001 |
| 6 | GET /DocumentSeries/GetAll | series.currentNumber=2 |
| 7 | GET /Document/GetTableRecords/1 | Lista z FV0001 |
| 8 | POST /Document/GetPdfStream | 200 OK + PDF stream |

#### TC-12: Walidacje haseł

| Hasło | Oczekiwany wynik |
|---|---|
| `Aa1!aaaa` | 200 OK (spełnia wymagania) |
| `aaaaaaa1!` | 400 (brak wielkiej litery) |
| `AAAAAAA1!` | 400 (brak małej litery) |
| `Aaaaaaa!!` | 400 (brak cyfry) |
| `Aaaaaaa1` | 400 (brak znaku specjalnego) |
| `Aa1!aaa` | 400 (za krótkie, 7 znaków) |
| `Aa1@aaaa` | 400 (znak `@` jest OK — test: 200) |

### Testy bezpieczeństwa

#### TC-20: Dostęp bez tokenu

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | GET /api/Document/GetTableRecords/1 bez nagłówka | 401 Unauthorized |
| 2 | GET /api/Product/GetAll bez nagłówka | 401 Unauthorized |

#### TC-21: Dostęp do zasobów innego użytkownika

| Krok | Akcja | Oczekiwany wynik |
|---|---|---|
| 1 | Zarejestruj Użytkownika A i B | Dwa konta |
| 2 | Użytkownik A tworzy produkt (id=99) | Produkt zapisany |
| 3 | Użytkownik B: PUT /Product/Edit {id: 99, ...} | **Bug: możliwa edycja cudzego produktu** |

## Dane testowe (fixtures)

| ID | Dane | Opis |
|---|---|---|
| DT-01 | email: `test@invoicejet.test`, password: `Test123!` | Konto testowe |
| DT-02 | CUI: `12345678`, firmName: `TEST SRL` | Firma testowa |
| DT-03 | SeriesName: `TEST`, currentNumber: `1`, documentTypeId: `1` | Seria testowa |

## Rekomendacje dla testów automatycznych

| Rodzaj testu | Framework | Priorytet |
|---|---|---|
| Unit tests (serwisy) | xUnit + Moq | WYSOKI |
| Integration tests (API) | WebApplicationFactory | WYSOKI |
| E2E tests (Angular) | Cypress / Playwright | ŚREDNI |
| Testy anomalii krytycznych | xUnit | KRYTYCZNY |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
