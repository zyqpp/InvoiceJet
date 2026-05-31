# InvoiceJet — Indeks dokumentacji doc_AI

| Atrybut | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |
| Wersja | 1.0 |

## Opis

Kompletna dokumentacja systemu InvoiceJet — aplikacji do fakturowania dla rynku rumuńskiego.

**Frontend:** Angular 16 + Angular Material  
**Backend:** ASP.NET Core 8 (Clean Architecture) + EF Core 8 + SQL Server  
**Hosting:** Azure  

---

## 📂 Struktura dokumentacji

### 📁 `_mapowania/` — Inwentaryzacje (punkt startowy analizy)

| Plik | Opis |
|---|---|
| `inwentaryzacja_ekranow.md` | 17 tras, 14 ekranów, 6 dialogów, anomalie UI |
| `inwentaryzacja_dto.md` | 14 DTO z polami i anomaliami |
| `inwentaryzacja_automappera.md` | 7 profili AutoMapper z kodem |
| `inwentaryzacja_rol.md` | 1 rola (User), JWT, anomalie bezpieczeństwa |
| `inwentaryzacja_procesow.md` | 15 procesów backendowych (P-01..P-15) |
| `inwentaryzacja_algorytmow.md` | 10 algorytmów (ALG-01..ALG-10) |

---

### 📁 `00_meta/` — Metadokumenty projektu

| Plik | ID | Opis |
|---|---|---|
| `01_o_projekcie.md` | — | Opis biznesowy, dług techniczny |
| `02_stos_technologiczny.md` | — | Tabela technologii i wersji |
| `03_architektura_aplikacji.md` | — | Clean Architecture, pipeline HTTP |
| `04_jak_poruszac_sie_po_aplikacji.md` | — | Przewodnik nawigacji po dokumentacji |
| `05_drzewo_projektu.md` | — | Drzewo katalogów projektu |
| `06_globalne_mechanizmy.md` | — | JWT, interceptors, UoW, CORS, QuestPDF |

---

### 📁 `01_ekrany/` — Ekrany i komponenty Angular

| Plik | ID | Opis |
|---|---|---|
| `login/login.md` | EKRAN-01 | Logowanie |
| `register/register.md` | EKRAN-02 | Rejestracja |
| `dashboard/dashboard.md` | EKRAN-03 | Dashboard ze statystykami |
| `firm_details/firm-details.md` | EKRAN-04 | Dane własnej firmy |
| `clients/clients.md` | EKRAN-05 | Lista klientów |
| `bank_accounts/bank-accounts.md` | EKRAN-06 | Konta bankowe |
| `products/products.md` | EKRAN-07 | Katalog produktów |
| `document_series/document-series.md` | EKRAN-08 | Serie numeracji |
| `invoices/invoices.md` | EKRAN-09 | Lista faktur |
| `invoices/add-or-edit-invoice.md` | EKRAN-10 | Formularz faktury |
| `invoice_proformas/invoice-proformas.md` | EKRAN-11 | Lista proform |
| `invoice_proformas/add-or-edit-invoice-proforma.md` | EKRAN-12 | Formularz proformy |
| `invoice_stornos/invoice-stornos.md` | EKRAN-13 | Lista stoern |
| `invoice_stornos/add-or-edit-invoice-storno.md` | EKRAN-14 | Formularz storna |
| `clients/add-edit-client-dialog.md` | DIALOG-01 | Dialog klienta |
| `bank_accounts/add-or-edit-bank-account-dialog.md` | DIALOG-02 | Dialog konta |
| `products/add-or-edit-product-dialog.md` | DIALOG-03 | Dialog produktu |
| `document_series/add-or-edit-document-series-dialog.md` | DIALOG-04 | Dialog serii |
| `_wspolne/pdf-viewer.md` | DIALOG-05 | Podgląd PDF |
| `_wspolne/token-expired-dialog.md` | DIALOG-06 | Dialog wygaśnięcia |
| `_wspolne/app-component.md` | LAYOUT-01 | AppComponent (root) |
| `_wspolne/navbar.md` | LAYOUT-02 | NavbarComponent |
| `_wspolne/sidebar.md` | LAYOUT-03 | SidebarComponent |
| `_wspolne/base-invoice-component.md` | BASE-01 | BaseInvoiceComponent (abstrakt) |

---

### 📁 `02_procesy/` — Procesy techniczne (Backend)

| Plik | ID | Opis |
|---|---|---|
| `P-01_RegisterUser.md` | P-01 | Rejestracja użytkownika |
| `P-02_LoginUser.md` | P-02 | Logowanie |
| `P-03_ManageFirm.md` | P-03 | Zarządzanie firmą |
| `P-04_GetFirmFromAnaf.md` | P-04 | Pobieranie danych z ANAF |
| `P-05_ManageBankAccounts.md` | P-05 | Zarządzanie kontami bankowymi |
| `P-06_ManageProducts.md` | P-06 | Zarządzanie produktami |
| `P-07_ManageDocumentSeries.md` | P-07 | Zarządzanie seriami numeracji |
| `P-08_AddDocument.md` | P-08 | Dodawanie dokumentu |
| `P-09_EditDocument.md` | P-09 | Edycja dokumentu |
| `P-10_GetDocuments.md` | P-10 | Pobieranie dokumentów |
| `P-11_DeleteDocument.md` | P-11 | Usunięcie dokumentu |
| `P-12_GeneratePdf.md` | P-12 | Generowanie PDF |
| `P-13_GetDocumentAutofillInfo.md` | P-13 | Dane autouzupełnienia |
| `P-14_GetDashboardStats.md` | P-14 | Statystyki dashboardu |
| `P-15_TransformToStorno.md` | P-15 | Konwersja na storno |

---

### 📁 `03_algorytmy/` — Algorytmy i mechanizmy

| Plik | ID | Opis |
|---|---|---|
| `ALG-01_JwtAuthentication.md` | ALG-01 | Pipeline JWT (frontend + backend) |
| `ALG-02_DocumentNumberGeneration.md` | ALG-02 | Generowanie numeru dokumentu |
| `ALG-03_PasswordHashingVerification.md` | ALG-03 | BCrypt haszowanie haseł |
| `ALG-04_JwtTokenCreation.md` | ALG-04 | Tworzenie tokenu JWT |
| `ALG-05_DocumentTotalCalculation.md` | ALG-05 | Obliczanie sum dokumentu |
| `ALG-06_AnafIntegration.md` | ALG-06 | Integracja z ANAF |
| `ALG-07_PdfGeneration.md` | ALG-07 | Generowanie PDF (QuestPDF) |
| `ALG-08_TransformToStorno.md` | ALG-08 | Konwersja na storno |
| `ALG-09_ExceptionMiddlewarePipeline.md` | ALG-09 | Obsługa wyjątków |
| `ALG-10_DataIsolationPattern.md` | ALG-10 | Izolacja danych między użytkownikami |

---

### 📁 `04_api_i_integracje/`

#### `01_api_frontend/` — Endpointy API

| Katalog | Endpointy |
|---|---|
| `auth/` | POST register, POST login |
| `firm/` | AddFirm, EditFirm, DeleteFirms, GetUserActiveFirm, GetUserClientFirms, fromAnaf |
| `bank_account/` | GetAll, Add, Edit, Delete |
| `product/` | GetAll, Add, Edit, Delete |
| `document_series/` | GetAll, Add, Update, Delete |
| `document/` | Add, Edit, GetTableRecords, GetById, Delete, GetAutofillInfo, GeneratePdf, GetPdfStream, GetDashboardStats, TransformToStorno |

#### `02_anaf/` — Integracja ANAF
| Plik | Opis |
|---|---|
| `ANAF_integracja.md` | Szczegóły integracji z API ANAF |

#### `03_db_seeder/` — Seedowanie danych
| Plik | Opis |
|---|---|
| `DbSeeder.md` | Inicjalizacja danych słownikowych |

---

### 📁 `05_model_danych/` — Model danych

#### `01_db/` — Baza danych
| Plik | Opis |
|---|---|
| `erd_globalny.md` | ERD — diagram encji |
| `spis_schem_i_tabel.md` | Spis 10 tabel, FK, indeksy |
| `dbo/dbo.User.md` ... `dbo.DocumentProduct.md` | 10 tabel szczegółowo |

#### `02_linq/` — Zapytania LINQ
| Plik | ID | Opis |
|---|---|---|
| `LINQ-01_GetDocumentById.md` | LINQ-01 | Pełny dokument z Include |
| `LINQ-02_GetTableRecords.md` | LINQ-02 | Lista dokumentów |
| `LINQ-03_GetDashboardStats.md` | LINQ-03 | Statystyki z agregacją |

#### `03_dto/` — Data Transfer Objects
| Plik | ID | Opis |
|---|---|---|
| `DTO-01_RegisterUserDto.md` | DTO-01 | Rejestracja |
| `DTO-02_LoginUserDto.md` | DTO-02 | Logowanie |
| `DTO-03_FirmRequestDto.md` | DTO-03 | Dane firmy |
| `DTO-04_BankAccountRequestDto.md` | DTO-04 | Konto bankowe |
| `DTO-05_ProductRequestDto.md` | DTO-05 | Produkt |
| `DTO-06_DocumentSeriesRequestDto.md` | DTO-06 | Seria dokumentów |
| `DTO-07_DocumentRequestDto.md` | DTO-07 | Dokument (główny) |
| `DTO-08_DocumentProductRequestDto.md` | DTO-08 | Pozycja dokumentu |
| `DTO-09_DocumentTableRecordDto.md` | DTO-09 | Rekord listy dokumentów |
| `DTO-10_DocumentAutofillInfoDto.md` | DTO-10 | Dane autouzupełnienia |
| `DTO-11_DocumentStatusDto.md` | DTO-11 | Status dokumentu |
| `DTO-12_DashboardStatsDto.md` | DTO-12 | Statystyki dashboardu |
| `DTO-13_UserDto.md` | DTO-13 | Token JWT (response auth) |
| `DTO-14_UserFirmDto.md` | DTO-14 | Powiązanie User-Firm |

#### `04_automapper/` — Profile AutoMapper
| Plik | ID | Opis |
|---|---|---|
| `AM-01_AuthProfile.md` | AM-01 | RegisterUserDto → User |
| `AM-02_FirmProfile.md` | AM-02 | FirmRequestDto ↔ Firm |
| `AM-03_BankAccountProfile.md` | AM-03 | BankAccountRequestDto ↔ BankAccount |
| `AM-04_ProductProfile.md` | AM-04 | ProductRequestDto ↔ Product |
| `AM-05_DocumentSeriesProfile.md` | AM-05 | DocumentSeriesRequestDto ↔ DocumentSeries |
| `AM-06_DocumentProfile.md` | AM-06 | Document ↔ DTOs (złożone mapowania) |
| `AM-07_UserFirmProfile.md` | AM-07 | UserFirm → FirmRequestDto (Seller) |

---

### 📁 `06_role_i_uprawnienia/`

| Plik | Opis |
|---|---|
| `lista_rol.md` | Lista ról (tylko "User") |
| `User.md` | Uprawnienia roli User |
| `macierz_role_uprawnienia.md` | Macierz endpoint × rola |

---

### 📁 `07_use_case/` — Przypadki użycia

| Plik | ID | Opis |
|---|---|---|
| `UC-01_ZarzadzanieKontem.md` | UC-01 | Rejestracja, logowanie, wylogowanie |
| `UC-02_WystawienieFaktury.md` | UC-02 | Wystawienie faktury/proformy/storna |
| `UC-03_ZarzadzanieKlientami.md` | UC-03 | CRUD klientów |
| `UC-04_KonwersjaNaStorno.md` | UC-04 | Konwersja dokumentów na storno |

---

### 📁 `08_model_biznesowy/`

| Plik | Opis |
|---|---|
| `model_biznesowy.md` | Opis produktu, segment rynku, dług techniczny |

---

### 📁 `09_procesy_biznesowe/` — Procesy BPMN

| Plik | ID | Opis |
|---|---|---|
| `BPMN-01_WystawienieFaktury.md` | BPMN-01 | Sekwencja wystawienia faktury |
| `BPMN-02_Rejestracja_i_OnBoarding.md` | BPMN-02 | Rejestracja i konfiguracja konta |

---

### 📁 `10_testy/`

| Plik | Opis |
|---|---|
| `plan_testow.md` | Plan testów z TC dla anomalii krytycznych |

---

### 📁 `_slowniki/` — Słowniki

| Plik | Opis |
|---|---|
| `slownik_pojec.md` | Słownik terminów biznesowych i technicznych |
| `slownik_anomalii.md` | Skonsolidowana lista 28 anomalii (4 krytyczne!) |

---

## 🚨 TOP 4 Anomalie krytyczne

| ID | Opis | Ryzyko |
|---|---|---|
| A-KRIT-01 | **CASCADE DELETE konta bankowego usuwa faktury** | Utrata danych |
| A-KRIT-02 | **TransformToStorno — brak atomowości** | Częściowa konwersja |
| A-KRIT-03 | **Race condition na numerach dokumentów** | Duplikaty |
| A-KRIT-04 | **GenerateInvoicePdf hardkoduje szablon faktury** | Błędne PDF dla proform/stoern |

---

## 📊 Statystyki dokumentacji

| Kategoria | Liczba plików |
|---|---|
| Inwentaryzacje | 6 |
| Metadokumenty | 6 |
| Ekrany i komponenty | 24 |
| Procesy techniczne | 15 |
| Algorytmy | 10 |
| Endpointy API | 31 |
| Integracje zewnętrzne | 2 |
| Model danych (DB) | 12 |
| LINQ | 3 |
| DTO | 14 |
| AutoMapper profile | 7 |
| Role i uprawnienia | 3 |
| Use Cases | 4 |
| Model biznesowy | 1 |
| Procesy BPMN | 2 |
| Testy | 1 |
| Słowniki | 2 |
| **ŁĄCZNIE** | **~143 pliki** |
