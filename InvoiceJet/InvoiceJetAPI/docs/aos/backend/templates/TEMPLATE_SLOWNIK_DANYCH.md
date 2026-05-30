<!--
SZABLON SLOWNIK_DANYCH — pełny słownik danych backendu.
Plik docelowy: docs/aos/backend/SLOWNIK_DANYCH.md
ZAKRES: tabele i kolumny (z snapshotu migracji), relacje, enumy, tabele słownikowe, seed.
ŹRÓDŁA: Infrastructure/Migrations/InvoiceJetDbContextModelSnapshot.cs, Domain/Models, Domain/Enums, Seeders/DbSeeder.
-->

# Słownik danych — InvoiceJetAPI

**Data aktualizacji:** RRRR-MM-DD
**Źródło prawdy:** snapshot migracji + `Domain/Models` + `Domain/Enums` + `DbSeeder`

---

## 1. Spis tabel

| Tabela | Encja | Krótki opis | Procesy używające |
|---|---|---|---|
| `[Table]` | `[Entity]` | [opis] | `P-XX`, `P-YY` |

---

## 2. Tabele — szczegóły kolumn
<!-- Po jednej sekcji dla KAŻDEJ tabeli. Wszystkie kolumny z typem SQL, nullability, kluczem, indeksem. -->

### `[Table]`
Encja: `[Entity].cs`. Snapshot: `InvoiceJetDbContextModelSnapshot.cs › Entity("[...]")`.

| Kolumna | Typ SQL | Nullable | Klucz | Indeks | Domyślna |
|---|---|---|---|---|---|
| `Id` | `int IDENTITY` | nie | PK | — | — |
| `[Column]` | `[nvarchar(max)]` | [tak/nie] | [FK→Table.Id] | [unikalny / brak] | — |

Relacje wychodzące:

| FK | → Tabela | Kierunek | Kaskada |
|---|---|---|---|
| `[FkId]` | `[Other]` | [1..N] | [Restrict / Cascade] |

---

## 3. Enumy

### `[EnumName]` (`Domain/Enums/[File].cs`)

| Wartość | Nazwa | Użycie |
|---|---|---|
| `1` | `[Name]` | [pole encji / scenariusz] |

---

## 4. Tabele słownikowe (lookupy)

### `[LookupTable]`
| Id | Nazwa | Pochodzenie |
|---|---|---|
| `1` | `[Name]` | seed (`DbSeeder.[Method]`) / migracja |

---

## 5. Seed (`DbSeeder`)
<!-- Co konkretnie wstawia DbSeeder przy starcie aplikacji. -->

| Co | Plik / metoda | Kiedy |
|---|---|---|
| [np. Typy dokumentów] | `DbSeeder.cs › SeedDocumentTypes` | przy starcie aplikacji |

---
<!-- ===== PRZYKŁAD (Document) — usuń przed oddaniem =====
Tabela Document — encja Document.cs.
Kolumny: Id (int IDENTITY, PK), DocumentNumber (nvarchar(max), not null), IssueDate (datetime2),
DueDate (datetime2, nullable), TotalPrice (decimal(18,2)), UnitPrice (decimal(18,2)),
DocumentStatusId (int, FK→DocumentStatus), DocumentTypeId (int, FK→DocumentType), BankAccountId (int, FK),
ClientId (int, nullable, FK→Firm), UserFirmId (int, nullable, FK→UserFirm).
Indeksy: na każdym FK (BankAccountId, ClientId, DocumentStatusId, DocumentTypeId, UserFirmId).
Enum DocumentStatusEnum: Unpaid, Paid, Overdue, Cancelled, Storno.
Seed: DbSeeder.SeedDocumentTypes wstawia 3 typy: Invoice, Proforma, Storno.
===== KONIEC PRZYKŁADU ===== -->
