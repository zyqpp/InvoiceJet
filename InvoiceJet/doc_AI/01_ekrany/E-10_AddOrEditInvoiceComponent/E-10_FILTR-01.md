# FILTR-E10-01 — Autocomplete klienta (Client Name or CUI)

| Pole | Wartość |
|---|---|
| ID | FILTR-E10-01 |
| Ekran nadrzędny | [E-10 Formularz faktury](E-10_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Client Name or CUI" |
| Nazwa w kodzie | `invoiceForm.get('client')` |
| Typ kontrolki | `mat-autocomplete` |
| Zawęża | lista podpowiedzi klientów |
| Parametr API | brak — klienckie filtrowanie na `invoiceAutofillData.clients` |
| Źródło danych autofill | [GET /api/Document/GetDocumentAutofillInfo/1](../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetAutofillInfo.md) → [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) → `Clients[]` |
| Pola filtrowane | `Firm.Name` (contains) + `Firm.Cui` (contains), case-insensitive |
| Domyślna wartość | `null` |
| Wymagany | tak (`Validators.required`) |

## Zachowanie

| Aspekt | Opis |
|---|---|
| Moment | `valueChanges` → `filterClients()` — na bieżąco przy wpisywaniu |
| Po wyborze | `displayFn(firm)` wyświetla `firm.name`; `invoiceForm.client` = `IFirm` object |
| Pola brane pod uwagę | `firm.name.includes(value) OR firm.cui.includes(value)` |

## Dane testowe

| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| Filtr po nazwie | `"ABC"` | lista firm z „ABC" w nazwie |
| Filtr po CUI | `"12345"` | lista firm z CUI zawierającym „12345" |
| Wybór firmy | klik podpowiedź | pole pokazuje `firm.name`, `client` = `IFirm` |
| Submit bez wyboru | puste pole | błąd walidacji (pole wymagane) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-10_ekran.md. |
