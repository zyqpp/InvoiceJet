# Use Case: Zarządzanie klientami

| Atrybut | Wartość |
|---|---|
| ID | UC-03 |
| Aktor | Użytkownik (zalogowany) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Diagram (PlantUML)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor "Użytkownik" as U
actor "ANAF (rejestr)" as ANAF <<external>>

rectangle "InvoiceJet — Zarządzanie klientami" {
  usecase "Wyświetl listę klientów" as UC1
  usecase "Dodaj klienta" as UC2
  usecase "Edytuj klienta" as UC3
  usecase "Usuń klienta" as UC4
  usecase "Pobierz dane klienta z ANAF" as UC5
}

U --> UC1
U --> UC2
U --> UC3
U --> UC4
ANAF --> UC5
UC5 ..> UC2 : <<extend>>
UC5 ..> UC3 : <<extend>>

note right of UC5
  GET /api/Firm/fromAnaf/{cui}
  Autouzupełnia pola formularza
end note

note right of UC4
  PUT /api/Firm/DeleteFirms
  Hard delete — blokada gdy
  klient ma powiązane faktury
end note
@enduml
```

## Scenariusze

### Dodanie klienta

1. Użytkownik otwiera EKRAN-05 (Klienci)
2. Klik "Dodaj klienta" → DIALOG-01
3. Opcjonalnie: podaje CUI i klika ikonę chmury → autouzupełnienie z ANAF
4. Wypełnia/weryfikuje dane
5. Zapisuje → `POST /api/Firm/AddFirm/true`

### Edycja klienta

1. Użytkownik klika "Edytuj" przy kliencie → DIALOG-01 (tryb edycji)
2. Modyfikuje dane
3. Zapisuje → `PUT /api/Firm/EditFirm/true`

### Usunięcie klienta

1. Użytkownik klika "Usuń" przy kliencie
2. Potwierdzenie (jeśli dialog) → `PUT /api/Firm/DeleteFirms`
3. Klient usunięty (hard delete)

## Ważna uwaga

Klient w InvoiceJet to firma (`Firm`) z flagą `isClient=true` powiązana z `UserFirm`. Ta sama tabela `Firm` służy zarówno do przechowywania własnej firmy jak i firm klientów.

## Powiązane endpointy

| Akcja | Endpoint |
|---|---|
| Lista klientów | `GET /api/Firm/GetUserClientFirms` |
| Dodanie | `POST /api/Firm/AddFirm/true` |
| Edycja | `PUT /api/Firm/EditFirm/true` |
| Usunięcie | `PUT /api/Firm/DeleteFirms` |
| ANAF | `GET /api/Firm/fromAnaf/{cui}` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
