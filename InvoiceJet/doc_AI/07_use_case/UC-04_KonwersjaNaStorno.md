# Use Case: Konwersja dokumentów na storno

| Atrybut | Wartość |
|---|---|
| ID | UC-04 |
| Aktor | Użytkownik (zalogowany) |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Diagram (PlantUML)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor "Użytkownik" as U

rectangle "InvoiceJet — Konwersja na storno" {
  usecase "Zaznacz dokumenty do anulowania" as UC1
  usecase "Przekształć fakturę w storno" as UC2
  usecase "Przekształć proformę w storno" as UC3
  usecase "Wyświetl listę storn" as UC4
  usecase "Edytuj storno" as UC5
  usecase "Generuj PDF storna" as UC6
}

U --> UC1
U --> UC2
U --> UC3
U --> UC4
U --> UC5
U --> UC6
UC2 ..> UC1 : <<include>>
UC3 ..> UC1 : <<include>>

note right of UC2
  PUT /api/Document/TransformToStorno
  Zmienia DocumentTypeId=3
  UWAGA: brak atomowości przy batch
  Operacja nieodwracalna przez UI
end note
@enduml
```

## Opis

Użytkownik może przekształcić istniejące dokumenty (faktury, proformy) w faktury storno bez ręcznego tworzenia nowego dokumentu.

## Scenariusz główny

1. Użytkownik otwiera EKRAN-13 (Storna) lub EKRAN-09 (Faktury)
2. Zaznacza jeden lub więcej dokumentów checkboxami
3. Klika "Przekształć na storno"
4. Backend: `PUT /api/Document/TransformToStorno` z tablicą ID
5. Dla każdego dokumentu: `DocumentTypeId` zmieniane na `3`
6. Lista odświeżana — dokumenty teraz widoczne jako storna

## Ograniczenia

- Zmiana dotyczy tylko `DocumentTypeId` — numer dokumentu pozostaje bez zmian
- Brak atomowości — częściowa konwersja możliwa przy błędzie
- Brak możliwości cofnięcia operacji przez UI

## Wymagania wstępne

- Dokumenty muszą istnieć w bazie
- Użytkownik musi być właścicielem dokumentów (przez UserFirm)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
