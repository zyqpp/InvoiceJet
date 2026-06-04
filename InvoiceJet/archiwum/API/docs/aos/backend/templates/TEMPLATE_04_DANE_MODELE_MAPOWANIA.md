<!--
SZABLON 04 — DANE, MODELE I MAPOWANIA (wymiar danych, do KOLUMN)
Odbiorca priorytetowy: DEVELOPER + TESTER. Schodzimy do poziomu kolumn DB (zasada ZB.8).
Źródła: DTO (Application/DTOs), encje (Domain/Models), snapshot migracji
(Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs), profile (Application/MappingProfiles).
Definicja ukończenia: 03_MARKERY_I_WERYFIKACJA.md → sekcja 3.
-->

# [NAZWA PROCESU] — Dane, modele i mapowania

## 1. DTO

### `[Dto]` (wejście / wyjście)

| Pole | Typ | Wymagane | Opis / źródło wartości |
|---|---|---|---|
| `[Field]` | `[int]` | [tak/nie] | [opis] |

> Atrybuty walidacyjne DTO: [lista lub: „Brak atrybutów walidacyjnych" + marker, jeżeli walidacja jest realizowana wyłącznie w serwisie.]

## 2. Encje i kolumny
<!-- Dla każdej dotykanej encji: tabela kolumn z typem SQL, nullability, kluczem, indeksem.
Źródło prawdy: snapshot migracji. Linkuj do SLOWNIK_DANYCH zamiast duplikować pełne definicje. -->

### Encja `[Entity]` → tabela `[Table]`
Kotwica: `[Entity].cs`, snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("[...]")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks |
|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — |
| `[Column]` | `[nvarchar(max)]` | [tak/nie] | [FK→Table] | [unikalny / brak] |

> Pełne definicje: `../../SLOWNIK_DANYCH.md#[Entity]`.

## 3. Relacje i kaskady
<!-- Tylko relacje istotne dla tego procesu. -->

| Z encji | Pole FK | Do encji | Kierunek | Kaskada |
|---|---|---|---|---|
| `[Entity]` | `[FkId]` | `[OtherEntity]` | [1..1 / 1..N / N..N] | [Restrict / Cascade / NoAction] |

## 4. Mapowania AutoMapper

| Źródło | Cel | Profil | Uwagi |
|---|---|---|---|
| `[Source]` | `[Target]` | `[Profile]` | [np. „ignoruje `Id`"] |

## 5. Zapytania (LINQ/SQL)
<!-- Najważniejsze zapytania wykonywane przez proces — krótki cytat + kotwica do repozytorium. -->

```csharp
// fragment zapytania (np. _context.BankAccount.Where(...).FirstOrDefaultAsync())
```

## 6. Użyte enumy i lookupy

| Element | Rodzaj | Plik | Wartości |
|---|---|---|---|
| `[Enum / Lookup]` | [enum / tabela słownikowa] | `[Enums/...cs]` / `[Models/...cs]` | [lista / link do SLOWNIK_DANYCH] |

---
<!-- ===== PRZYKŁAD (Document, fragment) — usuń przed oddaniem =====
Encja Document → tabela Document
| Id | int IDENTITY | nie | PK | — |
| DocumentNumber | nvarchar(max) | nie | — | — |
| TotalPrice | decimal(18,2) | nie | — | — |
| UserFirmId | int | tak | FK→UserFirm | indeks |
Mapowanie: DocumentRequestDto → Document (DocumentProfile) — uwaga: pomija UserFirmId (ustawiany w serwisie).
Enumy: DocumentStatusEnum (Unpaid=1, ...) — pełna lista w SLOWNIK_DANYCH.
===== KONIEC PRZYKŁADU ===== -->
