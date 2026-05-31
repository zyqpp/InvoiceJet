# E-10_POLA — Pola formularza faktury

| Pole | Wartość |
|---|---|
| ID dokumentu | E-10-POLA |
| Ekran nadrzędny | [E-10 Formularz faktury](E-10_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## POLE-E10-01 Client

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Client Name or CUI" |
| Nazwa w kodzie | `invoiceForm.get('client')` |
| Typ | `mat-autocomplete` — szczegóły: [FILTR-E10-01](E-10_FILTR-01.md) |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `Client: FirmRequestDto` |
| Pole DB | `Document.ClientId` → [dbo.Firm](../../../05_model_danych/01_db/dbo/dbo.Firm.md).`Id` |
| Walidacja | `Validators.required` |
| Domyślna wartość | `null` |

## POLE-E10-02 Issue Date

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Issue Date" |
| Nazwa w kodzie | `invoiceForm.get('issueDate')` |
| Typ | `mat-datepicker` |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `IssueDate: DateTime` |
| Pole DB | `Document.IssueDate` — [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Walidacja | `Validators.required` |
| Domyślna wartość | `new Date()` (dzisiaj) |

## POLE-E10-03 Due Date

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Due Date" |
| Nazwa w kodzie | `invoiceForm.get('dueDate')` |
| Typ | `mat-datepicker` |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DueDate: DateTime` (nullable) |
| Pole DB | `Document.DueDate` (nullable) — [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| Walidacja | `dueDateValidator` — musi być po `issueDate` |
| Wymagalność | opcjonalne |
| Domyślna wartość | `null` |

## POLE-E10-04 Document Series

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Document Series" |
| Nazwa w kodzie | `invoiceForm.get('documentSeries')` |
| Typ | `mat-select` |
| Źródło danych | `invoiceAutofillData.documentSeries` (tylko `DocumentTypeId=1`) |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DocumentSeries: DocumentSeriesRequestDto` |
| Algorytm numerowania | [ALG-02 Generowanie numeru dokumentu](../../../03_algorytmy/ALG-02_DocumentNumberGeneration.md) |
| Walidacja | brak (anomalia BA-05) |
| Domyślna wartość | `null` |

## POLE-E10-05 Document Status

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Status" |
| Nazwa w kodzie | `invoiceForm.get('documentStatus')` |
| Typ | `mat-select` |
| Źródło danych | `invoiceAutofillData.documentStatuses` (seedowane) |
| Pole DTO | [DTO-07](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) → `DocumentStatusId: int` |
| Pole DB | `Document.DocumentStatusId` → [dbo.DocumentStatus](../../../05_model_danych/01_db/dbo/dbo.DocumentStatus.md).`Id` |
| Wartości | `Unpaid` (id=1), `Paid` (id=2) — seedowane |
| Walidacja | brak (anomalia BA-05) |
| Domyślna wartość | `null` (backend ustawia `Unpaid` przy dodaniu) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-10_ekran.md. |
