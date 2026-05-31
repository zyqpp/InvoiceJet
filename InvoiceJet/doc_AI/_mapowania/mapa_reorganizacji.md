# Mapa reorganizacji dokumentacji — wytyczna dla agentów Fali 2

| Pole | Wartość |
|---|---|
| ID dokumentu | WEWN-MAPA-REORG |
| Typ dokumentu | wewnętrzny — wytyczna dla agentów |
| Autor | Agent Claudiusz Sonte 4.6 max (Agent-Orkiestrator) |
| Data | 2026-05-31 |
| Status | roboczy |

## Cel dokumentu

Mapa powiązań między istniejącymi plikami dokumentacji a docelową strukturą wg wytycznych.
Służy agentom Fali 2 jako instrukcja: skąd brać treść → gdzie umieszczać.

---

## T-04: Reorganizacja `01_ekrany/`

### Mapowanie folder źródłowy → folder docelowy

| Folder źródłowy (faktyczny) | Folder docelowy (wg spec) | Plik źródłowy → docelowy |
|---|---|---|
| `_wspolne/` | `00_wspolne/` | (rename/recreate) |
| `_wspolne/navbar.md` | `00_wspolne/navbar/ekran.md` | przenieś treść |
| `_wspolne/sidebar.md` | `00_wspolne/sidebar/ekran.md` | przenieś treść |
| `_wspolne/token-expired-dialog.md` | `00_wspolne/modale_wspolne/token_expired_dialog/modal.md` | przenieś treść |
| `_wspolne/app-component.md` | `00_wspolne/app_component/ekran.md` | przenieś treść |
| `_wspolne/base-invoice-component.md` | `00_wspolne/base_invoice_component/ekran.md` | przenieś treść |
| `_wspolne/angular-services.md` | `00_wspolne/angular_services.md` | zostaw lub przenieś |
| `_wspolne/routing.md` | `00_wspolne/routing.md` | zostaw lub przenieś |
| `_wspolne/pdf-viewer.md` | `00_wspolne/modale_wspolne/pdf_viewer/modal.md` | przenieś treść |
| `login/login.md` | `login/ekran.md` | przenieś treść |
| `register/register.md` | `register/ekran.md` | przenieś treść |
| `dashboard/dashboard.md` | `dashboard/ekran.md` | przenieś treść |
| `firm_details/firm-details.md` | `firma/dane_firmy/ekran.md` | przenieś treść |
| `clients/clients.md` | `firma/klienci/ekran.md` | przenieś treść |
| `clients/add-edit-client-dialog.md` | `firma/klienci/dialog_dodaj_klienta/modal.md` | przenieś treść |
| `bank_accounts/bank-accounts.md` | `firma/konta_bankowe/ekran.md` | przenieś treść |
| `bank_accounts/add-or-edit-bank-account-dialog.md` | `firma/konta_bankowe/dialog_dodaj_konto/modal.md` | przenieś treść |
| `products/products.md` | `produkty/ekran.md` | przenieś treść |
| `products/add-or-edit-product-dialog.md` | `produkty/dialog_dodaj_produkt/modal.md` | przenieś treść |
| `document_series/document-series.md` | `serie_dokumentow/ekran.md` | przenieś treść |
| `document_series/add-or-edit-document-series-dialog.md` | `serie_dokumentow/dialog_dodaj_serie/modal.md` | przenieś treść |
| `invoices/invoices.md` | `faktury/lista_faktur/ekran.md` | przenieś treść |
| `invoices/add-or-edit-invoice.md` | `faktury/dodaj_edytuj_fakture/ekran.md` | przenieś treść |
| `invoice_proformas/invoice-proformas.md` | `faktury_proforma/lista_faktur_proforma/ekran.md` | przenieś treść |
| `invoice_proformas/add-or-edit-invoice-proforma.md` | `faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md` | przenieś treść |
| `invoice_stornos/invoice-stornos.md` | `faktury_storno/lista_faktur_storno/ekran.md` | przenieś treść |
| `invoice_stornos/add-or-edit-invoice-storno.md` | `faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` | przenieś treść |
| (brak) | `mapa_przejsc.md` | stwórz nowy |

### README do stworzenia w `01_ekrany/`

Każdy folder grupy potrzebuje `README.md`:
`00_wspolne/README.md`, `login/README.md`, `register/README.md`, `dashboard/README.md`,
`firma/README.md`, `firma/dane_firmy/README.md`, `firma/klienci/README.md`,
`firma/konta_bankowe/README.md`, `produkty/README.md`, `serie_dokumentow/README.md`,
`faktury/README.md`, `faktury_proforma/README.md`, `faktury_storno/README.md`

---

## T-05: Reorganizacja `02_procesy/`

### Mapowanie plik źródłowy → plik docelowy

| Plik źródłowy (P-XX) | Folder docelowy | Plik docelowy |
|---|---|---|
| `P-01_RegisterUser.md` | `autentykacja/rejestracja/` | `proces.md` |
| `P-02_LoginUser.md` | `autentykacja/logowanie/` | `proces.md` |
| `P-03_ManageFirm.md` (część: AddFirm, EditFirm, GetActiveFirm, GetClients) | `firma/` | kilka podfolderów: `dodaj_firme/`, `edytuj_firme/`, `pobierz_aktywna_firme/`, `pobierz_firmy_klientow/` |
| `P-04_GetFirmFromAnaf.md` | `firma/pobierz_z_anaf/` | `proces.md` |
| `P-05_ManageBankAccounts.md` | `konta_bankowe/` | `pobierz_konta/`, `dodaj_konto/`, `edytuj_konto/`, `usun_konta/` |
| `P-06_ManageProducts.md` | `produkty/` | `pobierz_produkty/`, `dodaj_produkt/`, `edytuj_produkt/`, `usun_produkty/` |
| `P-07_ManageDocumentSeries.md` | `serie_dokumentow/` | `pobierz_serie/`, `dodaj_serie/`, `edytuj_serie/`, `usun_serie/` |
| `P-08_AddDocument.md` | `dokumenty/dodaj_dokument/` | `proces.md` |
| `P-09_EditDocument.md` | `dokumenty/edytuj_dokument/` | `proces.md` |
| `P-10_GetDocuments.md` | `dokumenty/pobierz_dokumenty/` | `proces.md` |
| `P-11_DeleteDocument.md` | `dokumenty/usun_dokumenty/` | `proces.md` |
| `P-12_GeneratePdf.md` | `dokumenty/generuj_pdf/` | `proces.md` |
| `P-13_GetDocumentAutofillInfo.md` | `dokumenty/pobierz_autouzupelnienie/` | `proces.md` |
| `P-14_GetDashboardStats.md` | `dokumenty/dashboard_statystyki/` | `proces.md` |
| `P-15_TransformToStorno.md` | `dokumenty/transformuj_na_storno/` | `proces.md` |

### Uwaga dla agenta T-05

P-03 opisuje CRUD firmy — to wiele operacji w jednym pliku. Podziel treść na osobne `proces.md` per operacja. Jeśli trudno rozdzielić, zrób jeden `proces.md` w `firma/` i linkuj do niego z podfolderów.

---

## T-06: Reorganizacja `03_algorytmy/`

### Mapowanie plik źródłowy → kategoria → plik docelowy

| Plik źródłowy | Kategoria | Plik docelowy |
|---|---|---|
| `ALG-01_JwtAuthentication.md` | `autoryzacyjne/` | `weryfikacja_tokenu_jwt.md` |
| `ALG-02_DocumentNumberGeneration.md` | `dedykowane/` | `generowanie_numeru_dokumentu.md` |
| `ALG-03_PasswordHashingVerification.md` | `walidacji/` | `walidacja_hasla.md` |
| `ALG-04_JwtTokenCreation.md` | `autoryzacyjne/` | `tworzenie_tokenu_jwt.md` |
| `ALG-05_DocumentTotalCalculation.md` | `wyliczeniowe/` | `obliczanie_wartosci_dokumentu.md` |
| `ALG-06_AnafIntegration.md` | `dedykowane/` | `integracja_anaf.md` |
| `ALG-07_PdfGeneration.md` | `generowania_pdf/` | — podziel na: `generuj_pdf_na_dysk.md` i `generuj_pdf_stream.md` |
| `ALG-08_TransformToStorno.md` | `dedykowane/` | `transformacja_na_storno.md` |
| `ALG-09_ExceptionMiddlewarePipeline.md` | `dedykowane/` | `pipeline_obslugi_wyjatkow.md` |
| `ALG-10_DataIsolationPattern.md` | `dedykowane/` | `izolacja_danych_userfirm.md` |

### README do stworzenia w `03_algorytmy/`

`walidacji/README.md`, `autoryzacyjne/README.md`, `generowania_pdf/README.md`,
`wyliczeniowe/README.md`, `dedykowane/README.md`

---

## T-07: Fix `05_model_danych/`

### Foldery do stworzenia (nowe)

| Folder | Zawartość |
|---|---|
| `02_dto/` | Wszystkie pliki DTO-01..DTO-14 + `spis_dto.md` + `README.md` |
| `04_zapytania_bezposrednie/` | `README.md` (na razie pusty — brak zapytań bezpośrednich w projekcie) |
| `06_skrypty/` | `DbSeeder.md` + `README.md` |

### Istniejące foldery do zachowania (bez przemianowania — pliki w nich są poprawne)

Uwaga: Istniejące foldery `02_linq/`, `03_dto/`, `04_automapper/` mają błędną numerację wg spec, ale ich zawartość jest wartościowa. Strategia: **stwórz nowe foldery z prawidłowymi numerami i SKOPIUJ/przenieś treść**. Nie usuwaj starych — właściciel projektu zdecyduje po audycie.

| Folder istniejący | Folder docelowy (wg spec) | Działanie |
|---|---|---|
| `02_linq/` | `03_linq/` | Stwórz `03_linq/` z README + skopiuj pliki LINQ-01..05 |
| `03_dto/` | `02_dto/` | Stwórz `02_dto/` z README + spis_dto.md + skopiuj pliki DTO-01..14 |
| `04_automapper/` | `05_automapper/` | Stwórz `05_automapper/` z README + skopiuj pliki AM-01..07 |

### Brakujące pliki do stworzenia

| Plik | Zawartość |
|---|---|
| `01_db/README.md` | README katalogu bazy danych |
| `01_db/dbo/erd_dbo.md` | ERD dla schematu dbo (Mermaid erDiagram — skrócony, tylko schemat dbo) |
| `02_dto/spis_dto.md` | Tabela: nazwa DTO, cel, kierunek (request/response), powiązany endpoint |
| `06_skrypty/DbSeeder.md` | Opis DbSeeder — przenieś treść z `04_api_i_integracje/03_db_seeder/DbSeeder.md` |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Mapa reorganizacji dla agentów Fali 2. |
