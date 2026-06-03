# 03_algorytmy — Algorytmy InvoiceJet

## Struktura (dwie warstwy)

Folder ma **dwie warstwy** dokumentacji algorytmów:

| Warstwa | Lokalizacja | Opis |
|---|---|---|
| **Źródłowa (legacy)** | `ALG-01` … `ALG-10` w tym folderze | Oryginalne, skrócone. Zachowane dla kompatybilności z istniejącymi linkami. |
| **Kategoryczna (primary)** | podfoldery `autoryzacyjne/` `walidacji/` `generowania_pdf/` `wyliczeniowe/` `dedykowane/` | Szczegółowe, kategoryzowane. **To jest źródło prawdy.** |

> ⚠️ **Duplikaty są celowe.** Pliki `ALG-01..10` mają odpowiedniki w podfolderach. Docelowo `ALG-XX` powinny stać się stubami/przekierowaniami. Na razie obie warstwy współistnieją.

---

## Mapa nakładania się

| Plik root | Odpowiednik w podfolderze | Uwagi |
|---|---|---|
| [ALG-01_JwtAuthentication.md](ALG-01_JwtAuthentication.md) | [autoryzacyjne/weryfikacja_tokenu_jwt.md](autoryzacyjne/weryfikacja_tokenu_jwt.md) | duplikat |
| [ALG-02_DocumentNumberGeneration.md](ALG-02_DocumentNumberGeneration.md) | [dedykowane/generowanie_numeru_dokumentu.md](dedykowane/generowanie_numeru_dokumentu.md) | duplikat |
| [ALG-03_PasswordHashingVerification.md](ALG-03_PasswordHashingVerification.md) | [walidacji/walidacja_hasla.md](walidacji/walidacja_hasla.md) | duplikat |
| [ALG-04_JwtTokenCreation.md](ALG-04_JwtTokenCreation.md) | [autoryzacyjne/tworzenie_tokenu_jwt.md](autoryzacyjne/tworzenie_tokenu_jwt.md) | duplikat |
| [ALG-05_DocumentTotalCalculation.md](ALG-05_DocumentTotalCalculation.md) | [wyliczeniowe/obliczanie_wartosci_dokumentu.md](wyliczeniowe/obliczanie_wartosci_dokumentu.md) | duplikat + **błąd w ALG-05** (formuła backendu nieaktualna) |
| [ALG-06_AnafIntegration.md](ALG-06_AnafIntegration.md) | [dedykowane/integracja_anaf.md](dedykowane/integracja_anaf.md) | duplikat |
| [ALG-07_PdfGeneration.md](ALG-07_PdfGeneration.md) | [generowania_pdf/generuj_pdf_na_dysk.md](generowania_pdf/generuj_pdf_na_dysk.md) + [generowania_pdf/generuj_pdf_stream.md](generowania_pdf/generuj_pdf_stream.md) | split na dwa pliki |
| [ALG-08_TransformToStorno.md](ALG-08_TransformToStorno.md) | [dedykowane/transformacja_na_storno.md](dedykowane/transformacja_na_storno.md) | duplikat |
| [ALG-09_ExceptionMiddlewarePipeline.md](ALG-09_ExceptionMiddlewarePipeline.md) | [dedykowane/pipeline_obslugi_wyjatkow.md](dedykowane/pipeline_obslugi_wyjatkow.md) | duplikat |
| [ALG-10_DataIsolationPattern.md](ALG-10_DataIsolationPattern.md) | [dedykowane/izolacja_danych_userfirm.md](dedykowane/izolacja_danych_userfirm.md) | duplikat |

---

## Algorytmy tylko w podfolderach (bez odpowiednika root)

| Plik | Opis |
|---|---|
| [dedykowane/seed_typow_dokumentow.md](dedykowane/seed_typow_dokumentow.md) | DbSeeder — seedowanie DocumentType i DocumentStatus przy starcie |
| [wyliczeniowe/obliczanie_ceny_pozycji.md](wyliczeniowe/obliczanie_ceny_pozycji.md) | Obliczanie ceny brutto jednej pozycji (frontend) |
| [wyliczeniowe/aktualizacja_produktow_dokumentu.md](wyliczeniowe/aktualizacja_produktow_dokumentu.md) | UpdateDocumentProducts — zapis pozycji i sum do DB |
| [dedykowane/zarzadzanie_relacja_userfirm.md](dedykowane/zarzadzanie_relacja_userfirm.md) | ManageUserFirmRelation — powiązanie firmy z userem |
| [dedykowane/inicjalizacja_serii_dokumentow.md](dedykowane/inicjalizacja_serii_dokumentow.md) | AddInitialDocumentSeries — domyślne serie przy pierwszej firmie |

---

## Indeks wszystkich algorytmów (primary — podfoldery)

### Autoryzacyjne
| Plik | Opis |
|---|---|
| [autoryzacyjne/weryfikacja_tokenu_jwt.md](autoryzacyjne/weryfikacja_tokenu_jwt.md) | Pipeline JWT: backend + interceptor Angular + AuthGuard |
| [autoryzacyjne/tworzenie_tokenu_jwt.md](autoryzacyjne/tworzenie_tokenu_jwt.md) | AuthService.CreateToken() — claims, HmacSha512, 10min TTL |

### Walidacji
| Plik | Opis |
|---|---|
| [walidacji/walidacja_hasla.md](walidacji/walidacja_hasla.md) | Regex + BCrypt; 7 dozwolonych znaków specjalnych |

### Generowania PDF
| Plik | Opis |
|---|---|
| [generowania_pdf/generuj_pdf_na_dysk.md](generowania_pdf/generuj_pdf_na_dysk.md) | **BUG:** hardcoded InvoiceDocument niezależnie od typu |
| [generowania_pdf/generuj_pdf_stream.md](generowania_pdf/generuj_pdf_stream.md) | Poprawna ścieżka z fabryką (Preview PDF) |

### Wyliczeniowe
| Plik | Opis |
|---|---|
| [wyliczeniowe/obliczanie_ceny_pozycji.md](wyliczeniowe/obliczanie_ceny_pozycji.md) | Cena brutto wiersza: `UnitPrice × Qty × (1 + VAT/100)` — **frontend** |
| [wyliczeniowe/obliczanie_wartosci_dokumentu.md](wyliczeniowe/obliczanie_wartosci_dokumentu.md) | Suma netto i brutto dokumentu — frontend + backend |
| [wyliczeniowe/aktualizacja_produktow_dokumentu.md](wyliczeniowe/aktualizacja_produktow_dokumentu.md) | UpdateDocumentProducts — zapis pozycji i aktualizacja sum w Document |

### Dedykowane
| Plik | Opis |
|---|---|
| [dedykowane/generowanie_numeru_dokumentu.md](dedykowane/generowanie_numeru_dokumentu.md) | `SeriesName + CurrentNumber.D4` — **race condition!** |
| [dedykowane/transformacja_na_storno.md](dedykowane/transformacja_na_storno.md) | Zmiana DocumentTypeId=3 — **brak atomowości** |
| [dedykowane/integracja_anaf.md](dedykowane/integracja_anaf.md) | POST do ANAF API po CUI |
| [dedykowane/pipeline_obslugi_wyjatkow.md](dedykowane/pipeline_obslugi_wyjatkow.md) | ExceptionMiddleware → mapa wyjątek → HTTP |
| [dedykowane/izolacja_danych_userfirm.md](dedykowane/izolacja_danych_userfirm.md) | UserFirm-based isolation — luka przy edycji |
| [dedykowane/seed_typow_dokumentow.md](dedykowane/seed_typow_dokumentow.md) | DbSeeder przy starcie aplikacji |
| [dedykowane/zarzadzanie_relacja_userfirm.md](dedykowane/zarzadzanie_relacja_userfirm.md) | ManageUserFirmRelation — powiązanie firma↔user |
| [dedykowane/inicjalizacja_serii_dokumentow.md](dedykowane/inicjalizacja_serii_dokumentow.md) | AddInitialDocumentSeries — domyślne serie przy pierwszej firmie |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
| 0.2 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Reorganizacja — dodano podkatalogi. |
| 0.3 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pełna mapa nakładania się, dodano brakujące algorytmy. |
