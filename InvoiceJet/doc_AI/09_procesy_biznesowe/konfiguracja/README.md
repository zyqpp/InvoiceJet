# konfiguracja — Procesy biznesowe konfiguracji systemu

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-KONF-README |
| Typ dokumentu | README grupy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Zakres grupy

Procesy związane z konfiguracją danych niezbędnych do wystawiania dokumentów: zarządzanie katalogiem produktów, kontami bankowymi oraz seriami numeracji dokumentów.

## Pliki

| Plik | ID dokumentu | Opis |
|---|---|---|
| `konfiguracja_firmy.md` | BPMN-KONF-01 | Zarządzanie produktami, kontami bankowymi i seriami numeracji dokumentów. |

## Technologie

- `POST /api/Product/Add`, `PUT /api/Product/Edit/{id}`, `DELETE /api/Product/Delete/{id}` — zarządzanie produktami
- `POST /api/BankAccount/Add`, `PUT /api/BankAccount/Edit/{id}`, `DELETE /api/BankAccount/Delete/{id}` — konta bankowe
- `POST /api/DocumentSeries/Add`, `PUT /api/DocumentSeries/Edit/{id}`, `DELETE /api/DocumentSeries/Delete/{id}` — serie numeracji

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
