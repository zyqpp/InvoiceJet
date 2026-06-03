---
name: plantuml-usecase
description: >-
  Twórz i poprawiaj diagramy PlantUML UseCase dla dokumentacji AOS InvoiceJet.
  Trigger: "diagram use case", "diagram przypadków użycia", "popraw diagram UC",
  "zamień Mermaid na PlantUML UseCase", "narysuj use case". Produkuje blok
  ```plantuml @startuml usecase ... @enduml``` gotowy do osadzenia w Markdown.
  ZAWSZE waliduj składnię przed wstawieniem (checklist §5).
---

# Skill: plantuml-usecase

Profesjonalne diagramy PlantUML UseCase dla dokumentacji InvoiceJet.

---

## 1. Kluczowa różnica: UseCase vs Flowchart

| | PlantUML UseCase | Mermaid Flowchart |
|---|---|---|
| **Pokazuje** | KTO może CO zrobić (aktorzy + przypadki użycia) | JAK działa (kroki, decyzje, przepływ) |
| **Jednostka** | Przypadek użycia (owal) — cel aktora | Krok procesu (prostokąt/romb) |
| **Relacje** | association, include, extend, generalization | strzałki warunkowe, pętle |
| **Zastosowanie** | requirements, scope systemu | opis procesu technicznego |

> **Zasada:** UseCase diagram odpowiada na pytanie „Co system umożliwia aktorowi?", nie „Jak to technicznie działa?".

---

## 2. Składnia PlantUML UseCase

### Minimalna struktura

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle

actor "Nazwa aktora" as A

rectangle "Nazwa systemu" {
  usecase "Opis przypadku" as UC1
  usecase "Inny przypadek" as UC2
}

A --> UC1
A --> UC2
@enduml
```

### Elementy składni

| Element | Składnia | Opis |
|---|---|---|
| Aktor | `actor "Nazwa" as A` | Ludzik lub `actor "Nazwa" as A <<system>>` dla zewnętrznego |
| Przypadek użycia | `usecase "Opis" as UCn` | Owal; opis = cel użytkownika |
| Granica systemu | `rectangle "System" { ... }` | Prostokąt otaczający use case'y |
| Asocjacja | `A --> UC1` | Aktor inicjuje UC |
| Include | `UC1 ..> UC2 : <<include>>` | UC2 ZAWSZE wykonywany w ramach UC1 |
| Extend | `UC2 ..> UC1 : <<extend>>` | UC2 opcjonalnie rozszerza UC1 |
| Generalizacja aktora | `Admin --|> User` | Admin dziedziczy po User |
| Generalizacja UC | `UC2 --|> UC1` | UC2 specjalizuje UC1 |
| Nota | `note right of UC1 : tekst` | Komentarz |

### Kierunek

```plantuml
left to right direction   " poziomy układ (zalecany dla małych diagramów)
top to bottom direction   " pionowy układ (domyślny, dobry dla dużych)
```

### Skinparam (opcjonalnie)

```plantuml
skinparam usecase {
  BackgroundColor LightBlue
  BorderColor DarkBlue
  ArrowColor DarkBlue
}
skinparam actor {
  BackgroundColor LightYellow
}
```

---

## 3. Wzorce dla InvoiceJet

### Jeden aktor, wiele UC

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor "Użytkownik" as U

rectangle "InvoiceJet — [OBSZAR]" {
  usecase "Wyświetl listę X" as UC1
  usecase "Dodaj X" as UC2
  usecase "Edytuj X" as UC3
  usecase "Usuń X" as UC4
}

U --> UC1
U --> UC2
U --> UC3
U --> UC4
@enduml
```

### Z relacją include (wspólne prereq)

```plantuml
@startuml
left to right direction
actor "Użytkownik" as U

rectangle "InvoiceJet" {
  usecase "Wystaw fakturę" as UC1
  usecase "Wystaw proformę" as UC2
  usecase "Zaloguj się" as UC_AUTH
  usecase "Wybierz klienta" as UC_CLIENT
}

U --> UC1
U --> UC2
UC1 ..> UC_AUTH : <<include>>
UC2 ..> UC_AUTH : <<include>>
UC1 ..> UC_CLIENT : <<include>>
@enduml
```

### Z relacją extend (opcjonalne kroki)

```plantuml
@startuml
left to right direction
actor "Użytkownik" as U

rectangle "InvoiceJet" {
  usecase "Zapisz fakturę" as UC1
  usecase "Generuj PDF" as UC2
  usecase "Pobierz PDF" as UC3
}

U --> UC1
UC2 ..> UC1 : <<extend>>
UC3 ..> UC2 : <<extend>>
@enduml
```

### Wielu aktorów

```plantuml
@startuml
left to right direction
actor "Użytkownik" as U
actor "System ANAF" as ANAF <<external>>

rectangle "InvoiceJet — Firma" {
  usecase "Edytuj dane firmy" as UC1
  usecase "Pobierz dane z ANAF" as UC2
  usecase "Dodaj klienta" as UC3
}

U --> UC1
U --> UC3
UC2 ..> UC1 : <<extend>>
ANAF --> UC2
@enduml
```

---

## 4. Konwersja z Mermaid flowchart → PlantUML UseCase

Gdy zamieniasz Mermaid flowchart na PlantUML UseCase:

1. **Zidentyfikuj aktorów** — kto inicjuje akcje (człowiek, system zewnętrzny)
2. **Zidentyfikuj use case'y** — CELE aktora (czasownik + rzeczownik), nie kroki techniczne
3. **Wyrzuć techniczne szczegóły** — API calls, błędy 400/500, console.log → to do scenariuszy, nie diagramu
4. **Zidentyfikuj relacje:**
   - Krok ZAWSZE poprzedza inny → `<<include>>`
   - Krok jest OPCJONALNY → `<<extend>>`
   - Ten sam aktor robi podobne rzeczy → generalizacja
5. **Granica systemu** = jeden prostokąt `rectangle "InvoiceJet — [Obszar]"`

### Przykład konwersji

**Mermaid (ZŁY format dla UC):**
```mermaid
flowchart TD
  Start --> Login[POST /api/Auth/login]
  Login --> JWT[Generuj JWT]
  JWT --> Dashboard
```

**PlantUML UseCase (DOBRY):**
```plantuml
@startuml
left to right direction
actor "Użytkownik" as U
rectangle "InvoiceJet — Autentykacja" {
  usecase "Zarejestruj się" as UC1
  usecase "Zaloguj się" as UC2
  usecase "Wyloguj się" as UC3
}
U --> UC1
U --> UC2
U --> UC3
@enduml
```

---

## 5. Checklist walidacji — PRZED wstawieniem

- [ ] `@startuml` na początku, `@enduml` na końcu
- [ ] Każdy `usecase` ma alias (`as UCn`)
- [ ] Każdy `actor` ma alias (`as A`)
- [ ] Brak `;` w labelach
- [ ] Brak polskich znaków w aliasach (A, UC1 — nie „Użytkownik")
- [ ] Polskie znaki OK w labelach w `" "` (np. `actor "Użytkownik" as U`)
- [ ] Każdy `rectangle { }` jest zamknięty
- [ ] Relacje `..>` ze stereotypem (`<<include>>` / `<<extend>>`) są w `" "` (np. `: <<include>>`)
- [ ] Brak kroków technicznych (API calls, błędy HTTP) w diagramie — te idą do scenariuszy
- [ ] Maksymalnie 10–12 use case'ów na diagramie (czytelność)

---

## 6. Wzorzec dokumentu UseCase (sekcja Diagram)

W każdym pliku `.md` z UC zastąp sekcję `## Diagram` tym wzorcem:

```markdown
## Diagram (PlantUML UseCase)

```plantuml
@startuml
left to right direction
skinparam packageStyle rectangle
actor "Użytkownik" as U

rectangle "InvoiceJet — [Obszar]" {
  usecase "Przypadek 1" as UC1
  usecase "Przypadek 2" as UC2
}

U --> UC1
U --> UC2
@enduml
```
```

---

## 7. Powiązane

- Wytyczne diagramów: [`wytyczne/01_zasady_zlote_i_ogolne.md`](../../../InvoiceJet/wytyczne/01_zasady_zlote_i_ogolne.md) §RO-01
- Skill `mermaid-diagrams`: dla diagramów sekwencji, flowchart, klas
- Wzorzec istniejący: [`doc_AI/07_use_case/UC-01_ZarzadzanieKontem.md`](../../../InvoiceJet/doc_AI/07_use_case/UC-01_ZarzadzanieKontem.md)
