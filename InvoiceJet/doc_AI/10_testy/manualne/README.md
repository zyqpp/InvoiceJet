# Testy manualne — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-MAN-INDEX |
| Typ dokumentu | indeks scenariuszy testowych manualnych |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Katalog zawiera manualne scenariusze testowe pogrupowane według obszarów funkcjonalnych aplikacji InvoiceJet. Testy obejmują ścieżki happy path, scenariusze negatywne oraz anomalie krytyczne wykryte podczas analizy kodu.

## Spis obszarów

| Obszar | Plik | Zakres TC | Liczba TC |
|---|---|---|---|
| Autentykacja | `autentykacja/testy_autentykacji.md` | TC-100 – TC-106 | 7 |
| Firma i klienci | `firma/testy_firmy.md` | TC-110 – TC-114 | 5 |
| Produkty | `produkty/testy_produktow.md` | TC-120 – TC-123 | 4 |
| Konta bankowe | `konta_bankowe/testy_kont_bankowych.md` | TC-130 – TC-132 | 3 |
| Serie dokumentów | `serie_dokumentow/testy_serii_dokumentow.md` | TC-140 – TC-143 | 4 |
| Dokumenty | `dokumenty/testy_dokumentow.md` | TC-150 – TC-157 | 8 |

## Dane testowe wspólne

| ID | Dane | Opis |
|---|---|---|
| DT-01 | email: `test@example.com`, hasło: `Test@123` | Konto testowe podstawowe |
| DT-02 | email: `test2@example.com`, hasło: `Test@123` | Konto testowe drugie (testy izolacji) |
| DT-03 | CUI: `12345678`, firmName: `TEST SRL` | Firma testowa |
| DT-04 | SeriesName: `FV`, currentNumber: `1`, documentTypeId: `1` | Seria testowa — faktury |
| DT-05 | SeriesName: `PRF`, currentNumber: `1`, documentTypeId: `2` | Seria testowa — proformy |
| DT-06 | IBAN: `RO49AAAA1B31007593840000`, currency: `RON` | Konto bankowe testowe |

## Konwencja statusów

| Status | Znaczenie |
|---|---|
| Nie przetestowany | Scenariusz nie był jeszcze uruchamiany |
| Zaliczony | Test przeszedł zgodnie z oczekiwanym wynikiem |
| Niezaliczony | Wynik rzeczywisty różni się od oczekiwanego |
| Zablokowany | Test nie może być uruchomiony z powodu błędu środowiska lub innego TC |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
