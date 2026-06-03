# Dialog: Dodaj/Edytuj klienta (Add/Edit Client Dialog)

| Atrybut | Wartość |
|---|---|
| ID | DIALOG-01 |
| Komponent | `AddEditClientDialogComponent` |
| Plik | `src/app/components/clients/add-edit-client-dialog/add-edit-client-dialog.component.ts` |
| Otwierany z | EKRAN-05 (lista klientów) |
| Typ | `MatDialog` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Modal Angular Material do dodawania i edycji danych klienta (firmy). Otwierany z `ClientsComponent` przez `MatDialog.open()`. Dane klienta przekazywane przez `MAT_DIALOG_DATA`.

## Pola formularza

| Pole | Kontrolka | Walidacja | Opis |
|---|---|---|---|
| `firmName` | `mat-form-field` | required | Nazwa firmy klienta |
| `cuiValue` | `mat-form-field` | — | CUI/NIP rumuński + ikona chmury (ANAF) |
| `regCom` | `mat-form-field` | — | Numer rejestracji handlowej |
| `address` | `mat-form-field` | — | Adres |
| `county` | `mat-form-field` | — | Okręg |
| `city` | `mat-form-field` | — | Miasto |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `client` | `IFirm \| null` | `null` = tryb dodawania; obiekt = tryb edycji |

## Przepływ

### Tryb dodawania (client = null)
1. Formularz pusty
2. Submit → `POST /api/Firm/AddFirm/true` (`isClient=true`)
3. Dialog zamknięty z wynikiem → lista odświeżona

### Tryb edycji (client ≠ null)
1. Formularz wypełniony danymi klienta
2. Submit → `PUT /api/Firm/EditFirm/true` (`isClient=true`)
3. Dialog zamknięty z wynikiem → lista odświeżona

### Autouzupełnienie ANAF
- Ikona chmury → `GET /api/Firm/fromAnaf/{cuiValue}` → wypełnienie pól

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie klienta | `POST /api/Firm/AddFirm/true` |
| Edycja klienta | `PUT /api/Firm/EditFirm/true` |
| ANAF autouzupełnienie | `GET /api/Firm/fromAnaf/{cuiValue}` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
