# Ekran: Klienci (Clients)

| Atrybut | Wartość |
|---|---|
| ID | EKRAN-05 |
| Trasa | `/dashboard/clients` |
| Komponent | `ClientsComponent` |
| Plik | `src/app/components/firm/clients/clients.component.ts` |
| AuthGuard | TAK |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista firm klientów z sortowaniem, paginacją, filtrowaniem i operacjami CRUD przez dialogi.

## Kolumny tabeli

`select`, `name`, `cui`, `regCom`, `address`, `county`, `city`

## Dialogi

| Dialog | Wywołanie | Cel |
|---|---|---|
| `AddEditClientDialogComponent` | `openNewClientDialog()` | Dodanie klienta |
| `AddEditClientDialogComponent` | `openEditClientDialog(firm)` | Edycja klienta |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie listy (ngOnInit) | `GET /api/Firm/GetUserClientFirms` |
| Usunięcie zaznaczonych | `PUT /api/Firm/DeleteFirms?firmIds=...` (query string) |

## Anomalie

- `console.log(firms)` w `getUserFirms()`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
