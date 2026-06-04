# ManageDocumentPdf — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono kompletną dokumentację procesu P-17 (8 plików): kontrakt API-28 i API-29, WAL-01A/WAL-01B/WAL-02B, dane/modele, bezpieczeństwo (kontrolerowy try/catch omijający middleware, połknięty błąd PDF, błędne konto bankowe, null-forgiving), scenariusze testowe, przegląd z 2 diagramami mermaid, metadane. |
| `1.1` | 2026-05-31 | Agent AI | Korekta po audycie kodu: `01_PRZEGLAD_PROCESU.md` — poprawiono błędne twierdzenie o użyciu wzorca fabryki przez API-28 (hardcoded `new InvoiceDocument`); dodano regułę biznesową o ograniczeniu fabryki do API-29; `05_BLEDY_BEZPIECZENSTWO.md` — dodano [UWAGA] o hardcoded `InvoiceDocument` w `GenerateInvoicePdf`; `ZAGADNIENIA_PRZEKROJOWE.md § 9` zaktualizowany równolegle o ten sam bug. |

## Notatki do katalogów przekrojowych

- `KATALOG_API.md` — **wymaga dodania** `API-28` i `API-29`.
- `KATALOG_WYJATKOW.md` — `UserHasNoAssociatedFirmException` już zarejestrowany w P-12; uwaga: w API-28 jest obsługiwany przez kontrolerowy try/catch (nie middleware).
- `KATALOG_DANYCH_TESTOWYCH.md` — brak nowych fixture'ów; używane `DT-01`, `DT-03`, `DT-05`, `DT-07`, `DT-08`.
