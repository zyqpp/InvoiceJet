# firma — Procesy biznesowe zarządzania firmami

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-FIRMA-README |
| Typ dokumentu | README grupy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Zakres grupy

Procesy związane z dodawaniem i edycją firm — zarówno własnej firmy wystawiającego, jak i firm klientów. Obejmuje autouzupełnienie danych z ANAF API na podstawie numeru CUI (rumuński NIP).

## Pliki

| Plik | ID dokumentu | Opis |
|---|---|---|
| `zarzadzanie_firma.md` | BPMN-FIRMA-01 | Dodanie lub edycja firmy własnej / klienta z opcjonalnym autouzupełnieniem ANAF. |

## Technologie

- `POST /api/Firm/AddFirm/{isClient}` — dodanie firmy (własna: `false`, klient: `true`)
- `PUT /api/Firm/EditFirm/{id}` — edycja firmy
- `GET /api/Firm/fromAnaf/{cui}` — pobieranie danych z ANAF API
- `GET /api/Firm/GetUserActiveFirm` — pobranie aktywnej firmy użytkownika
- `GET /api/Firm/GetClientFirms` — lista klientów

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
