# ManageBankAccounts — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono dokumentację procesu backendowego P-10 ManageBankAccounts. Pliki: 00_METADANE, 01_PRZEGLAD_PROCESU, 02_KONTRAKT_API (API-14–API-17), 03_LOGIKA_APLIKACYJNA (endpointy A–D), 04_DANE_MODELE_MAPOWANIA, 05_BLEDY_BEZPIECZENSTWO (WAL-01–WAL-04), 06_SCENARIUSZE_TESTOWE (TC-01–TC-07, TC-N01–TC-N04, TC-B01–TC-B08). Zidentyfikowano 5 UWAGI: błędne kody HTTP 500 zamiast 400/404 dla WAL-02/WAL-03, brak ownership check w Edit/Delete, użycie PUT zamiast DELETE, kaskada DB Document→BankAccount, niespójność parametrów Delete (body vs query string). Dodano nowy fixture DT-05. |

---

## Katalogi przekrojowe — stan po wersji 1.0

| Katalog | Wymagana akcja |
|---|---|
| `KATALOG_DANYCH_TESTOWYCH.md` | Dodać definicję fixture'u `DT-05` (Istniejące konto bankowe w aktywnej firmie) |
| `KATALOG_API.md` | Dodać endpointy `API-14`, `API-15`, `API-16`, `API-17` (jeśli plik istnieje) |
| `KATALOG_WYJATKOW.md` | Potwierdzić wpisy: `UserHasNoAssociatedFirmException` (400), `BankAccountAssociatedWithDocumentsException` (400); generyczny `Exception("Bank account not found.")` (500 — brak mapowania) (jeśli plik istnieje) |
