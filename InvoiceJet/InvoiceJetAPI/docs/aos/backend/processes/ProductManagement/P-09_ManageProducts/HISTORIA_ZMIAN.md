# ManageProducts — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono dokumentację procesu backendowego P-09 ManageProducts. Pliki: 00_METADANE, 01_PRZEGLAD_PROCESU, 02_KONTRAKT_API (API-10–API-13), 03_LOGIKA_APLIKACYJNA (endpointy A–D), 04_DANE_MODELE_MAPOWANIA, 05_BLEDY_BEZPIECZENSTWO (WAL-01–WAL-05), 06_SCENARIUSZE_TESTOWE (TC-01–TC-06, TC-N01–TC-N05, TC-B01–TC-B08). Zidentyfikowano 5 UWAGI wymagających weryfikacji z zespołem (błędne kody HTTP 500 zamiast 400/404, globalny indeks unikalny na Product.Name, brak walidacji nazwy w EditProduct, użycie PUT zamiast DELETE). Dodano nowy fixture DT-04 (istniejący produkt w aktywnej firmie). |

---

## Katalogi przekrojowe — stan po wersji 1.0

| Katalog | Wymagana akcja |
|---|---|
| `KATALOG_DANYCH_TESTOWYCH.md` | Dodać definicję fixture'u `DT-04` (Istniejący produkt w aktywnej firmie) |
| `KATALOG_API.md` | Dodać endpointy `API-10`, `API-11`, `API-12`, `API-13` (jeśli plik istnieje) |
| `KATALOG_WYJATKOW.md` | Potwierdzić wpisy: `UserHasNoAssociatedFirmException` (400), `ProductAssociatedWithInvoiceException` (400), `ProductWithSameNameExistsException` (500 — brak jawnego mapowania) (jeśli plik istnieje) |
