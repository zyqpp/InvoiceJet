# Ekran: Dane firmy (Firm Details)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-04 |
| Trasa | `/dashboard/firm-details` |
| Komponent | `FirmDetailsComponent` |
| Plik | `src/app/components/firm/firm-details/firm-details.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Ekran zarządzania danymi własnej firmy (wystawiającego faktury). Przy pierwszym wejściu bez firmy — formularz dodawania. Gdy firma istnieje — formularz edycji z przyciskiem "Save" aktywnym tylko przy zmianach.

## Pola formularza

| Pole | Kontrolka | Opis |
|---|---|---|
| `firmName` | `mat-form-field` | Nazwa firmy |
| `cuiValue` | `mat-form-field` | CUI (NIP rumuński) + przycisk ikona chmury (ANAF) |
| `regCom` | `mat-form-field` | Numer rejestracji handlowej |
| `address` | `mat-form-field` | Adres |
| `county` | `mat-form-field` | Okręg |
| `city` | `mat-form-field` | Miasto |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | `GET /api/Firm/GetUserActiveFirm` |
| Submit (edycja) | `PUT /api/Firm/EditFirm/false` |
| Submit (dodanie) | `POST /api/Firm/AddFirm/false` |
| Ikona chmury (ANAF) | `GET /api/Firm/fromAnaf/{cuiValue}` → autouzupełnienie pól |

## Metody

| Metoda | Opis |
|---|---|
| `onSubmit()` | Sprawdza `currentUserFirm` → AddFirm lub EditFirm |
| `onCloudIconClick()` | Pobiera dane z ANAF i wypełnia formularz |
| `isFormChanged()` | Sprawdza czy formularz zmieniony (UWAGA: błędna implementacja — zawsze `false`) |
| `addNewClient()` | Niezaimplementowana — tylko `console.log("Add new client")` |

## Anomalie

| # | Anomalia |
|---|---|
| FA-01 | `isFormChanged()` — błędna logika: `JSON.stringify(this.initialFormValues.value)` vs `JSON.stringify(this.initialFormValues)` — `initialFormValues` to plain object, więc `.value` to `undefined`; wynik zawsze `false` |
| FA-02 | `addNewClient()` niezaimplementowana |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
