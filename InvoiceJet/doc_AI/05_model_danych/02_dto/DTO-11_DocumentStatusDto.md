# DTO: DocumentStatusDto

| Atrybut | Wartość |
|---|---|
| ID | DTO-11 |
| Plik | `InvoiceJet.Application/DTOs/DocumentStatusDto.cs` |
| Kierunek | Response (zagnieżdżony w DocumentAutofillInfoDto) |
| Kontekst | Element listy `DocumentAutofillInfoDto.DocumentStatuses` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pola

| Pole | Typ C# | Nullable | Opis |
|---|---|---|---|
| `Id` | `int` | NIE | ID statusu |
| `Name` | `string` | NIE | Nazwa statusu (np. "Trimisa", "Platita") |

## Statusy w DB (seedowane)

| Id | Name (rumuński) |
|---|---|
| 1 | Trimisa (Wysłana) |
| 2 | Platita (Zapłacona) |
| 3 | Anulata (Anulowana) |
| 4 | Refuzata (Odrzucona) |

*Dokładne wartości zależne od DbSeeder — weryfikacja wymagana.*

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
