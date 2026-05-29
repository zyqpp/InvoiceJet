# Przyklad weryfikacyjny A-05 IssueNewInvoice

## Cel i kryterium potwierdzenia

Celem jest potwierdzenie, ze dokumentacja aplikacyjna pozwala przejsc caly slad:
`UI -> Front Service -> API -> Backend -> DB`.

Kryterium potwierdzenia:

- dla jednego pola i jednej akcji mozna wskazac mapowanie do endpointu, DTO, encji i `Tabela.Kolumna`,
- dla tej samej akcji mozna wskazac skutek w danych oraz rezultat w UI,
- kazdy krok ma dowod w istniejacej dokumentacji AOS.

## Wybrany przypadek (1 pole + 1 akcja + 1 skutek)

- Pole UI: `Document Series` na ekranie szczegolow faktury.
- Akcja UI: klik `Issue`.
- Skutek danych: zapis nowego `Document` oraz zwiekszenie `DocumentSeries.CurrentNumber`.

## Slad E2E

| Warstwa | Element | Dowod |
|---|---|---|
| UI | Pole `formControlName=\"documentSeries\"` | [A-05: 02_MAPA_POL_UI_DO_DANYCH.md](flows/A-05_IssueNewInvoice/02_MAPA_POL_UI_DO_DANYCH.md) |
| Front Service | `onSubmit()` oraz `DocumentService.addDocument()` | [A-05: 03_OPERACJE_I_PRZYCISKI.md](flows/A-05_IssueNewInvoice/03_OPERACJE_I_PRZYCISKI.md) |
| API | `POST /api/Document/AddDocument` | [A-05: 03_OPERACJE_I_PRZYCISKI.md](flows/A-05_IssueNewInvoice/03_OPERACJE_I_PRZYCISKI.md), [P-01: 02_KONTRAKT_API.md](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/02_KONTRAKT_API.md) |
| Backend | `DocumentController.AddDocument()` -> `DocumentService.AddDocument()` | [A-05: 03_OPERACJE_I_PRZYCISKI.md](flows/A-05_IssueNewInvoice/03_OPERACJE_I_PRZYCISKI.md), [P-01: 03_LOGIKA_APLIKACYJNA.md](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/03_LOGIKA_APLIKACYJNA.md) |
| DB | `Document.DocumentNumber`, `Document.DocumentTypeId`, `DocumentSeries.CurrentNumber` | [A-05: 02_MAPA_POL_UI_DO_DANYCH.md](flows/A-05_IssueNewInvoice/02_MAPA_POL_UI_DO_DANYCH.md), [A-05: 03_OPERACJE_I_PRZYCISKI.md](flows/A-05_IssueNewInvoice/03_OPERACJE_I_PRZYCISKI.md), [P-01: 04_DANE_MODELE_MAPOWANIA.md](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/04_DANE_MODELE_MAPOWANIA.md) |

## Scenariusz testowy (expected UI/API/DB)

| Krok | Akcja | Expected UI | Expected API | Expected DB |
|---|---|---|---|---|
| 1 | Wejscie na `/dashboard/add-invoice` | Formularz widoczny, dane pomocnicze zaladowane | `GET /api/Document/GetDocumentAutofillInfo/1` | Brak zapisu |
| 2 | Wybor `Document Series` i uzupelnienie danych | Formularz przechodzi walidacje | Brak wywolania zapisu przed submit | Brak zapisu |
| 3 | Klik `Issue` | Po sukcesie toastr i powrot do `/dashboard/invoices` | `POST /api/Document/AddDocument` zwraca `200 OK` | Nowy rekord `Document`; inkrementacja `DocumentSeries.CurrentNumber` |

## Dowody i linki

- Dokument aplikacyjny:
  [A-05 00_METADANE](flows/A-05_IssueNewInvoice/00_METADANE.md),
  [A-05 02_MAPA_POL_UI_DO_DANYCH](flows/A-05_IssueNewInvoice/02_MAPA_POL_UI_DO_DANYCH.md),
  [A-05 03_OPERACJE_I_PRZYCISKI](flows/A-05_IssueNewInvoice/03_OPERACJE_I_PRZYCISKI.md),
  [A-05 06_SCENARIUSZE_TESTOWE_E2E](flows/A-05_IssueNewInvoice/06_SCENARIUSZE_TESTOWE_E2E.md).
- Dokument frontendu:
  [E-05_InvoiceDetails 02_DANE_I_OPERACJE](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-05_InvoiceDetails/02_DANE_I_OPERACJE.md),
  [E-05_InvoiceDetails 04_SCENARIUSZE_TESTOWE](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-05_InvoiceDetails/04_SCENARIUSZE_TESTOWE.md).
- Dokument backendu:
  [P-01_IssueNewInvoice 02_KONTRAKT_API](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/02_KONTRAKT_API.md),
  [P-01_IssueNewInvoice 03_LOGIKA_APLIKACYJNA](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/03_LOGIKA_APLIKACYJNA.md),
  [P-01_IssueNewInvoice 04_DANE_MODELE_MAPOWANIA](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-01_IssueNewInvoice/04_DANE_MODELE_MAPOWANIA.md),
  [P-12_GetDocumentAutofillInfo 02_KONTRAKT_API](../../../InvoiceJet/InvoiceJetAPI/docs/aos/backend/processes/P-12_GetDocumentAutofillInfo/02_KONTRAKT_API.md).

## Wynik weryfikacji

`POTWIERDZONO`

Dokumentacja aplikacyjna zawiera komplet informacji pozwalajacy odtworzyc reprezentacyjny przypadek od makiety do skutku w bazie.
Brakujace metadane runtime agenta (poziom inteligencji i pelny kontekst historyczny) sa oznaczane markerem `N/D [WYMAGA WERYFIKACJI]` w historiach zmian.
