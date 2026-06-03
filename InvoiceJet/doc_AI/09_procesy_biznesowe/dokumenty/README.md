# dokumenty — Procesy biznesowe dokumentów handlowych

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-DOC-README |
| Typ dokumentu | README grupy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Zakres grupy

Procesy związane z tworzeniem, konwersją i eksportem dokumentów handlowych: faktur, proform, faktur storno oraz plików PDF.

## Pliki

| Plik | ID dokumentu | Typ dokumentu | Opis |
|---|---|---|---|
| [wystawienie_faktury.md](wystawienie_faktury.md) | BPMN-DOC-01 | Faktura (TypeId=1) | Pełny flow: autouzupełnienie, formularz, zapis, PDF. |
| [wystawienie_proformy.md](wystawienie_proformy.md) | BPMN-DOC-02 | Proforma (TypeId=2) | Identyczny flow jak faktura, różni się typem dokumentu. |
| [wystawienie_storno.md](wystawienie_storno.md) | BPMN-DOC-03 | Storno (TypeId=3) | Konwersja istniejącego dokumentu na storno (PUT). |
| [eksport_pdf.md](eksport_pdf.md) | BPMN-DOC-04 | — | Generowanie PDF przez QuestPDF, pobranie przez przeglądarkę. |
| **[szablon_dokumentu_pdf.md](szablon_dokumentu_pdf.md)** | PDF-TEMPLATE | wszystkie typy | **Kompletna dokumentacja szablonu PDF: sekcje, pola, źródła danych, obliczenia, anomalie.** |

## Technologie

- `GET /api/Document/GetDocumentAutofillInfo/{typeId}` — dane autouzupełnienia
- `POST /api/Document/Add` — zapis nowego dokumentu
- `PUT /api/Document/TransformToStorno` — konwersja na storno
- `POST /api/Document/GetPdfStream` — generowanie i strumieniowanie PDF
- `POST /api/Document/GenerateInvoicePdf` — generowanie PDF jako bajty
- QuestPDF 2024.3.10 Community — biblioteka generowania PDF

## Typy dokumentów

| TypeId | Nazwa | Szablon PDF |
|---|---|---|
| 1 | Faktura (Invoice) | InvoiceDocument |
| 2 | Proforma (ProformaInvoice) | ProformaDocument |
| 3 | Faktura storno (StornoInvoice) | StornoDocument |

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
