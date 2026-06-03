# InvoiceJet — Indeks dokumentacji doc_AI

| Atrybut | Wartość |
|---|---|
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |
| Wersja | 2.0 |

## Opis

Kompletna dokumentacja systemu InvoiceJet — aplikacji do fakturowania dla rynku rumuńskiego.

**Frontend:** Angular 16 + Angular Material  
**Backend:** ASP.NET Core 8 (Clean Architecture) + EF Core 8 + SQL Server  
**Hosting:** Azure  

---

## Struktura dokumentacji

### `_mapowania/` — Inwentaryzacje i mapy krzyżowe (punkt startowy analizy)

#### Inwentaryzacje

| Plik | Opis |
|---|---|
| `inwentaryzacja_ekranow.md` | 17 tras, 14 ekranów, 6 dialogów, anomalie UI |
| `inwentaryzacja_encji.md` | 10 encji DB z polami |
| `inwentaryzacja_dto.md` | 14 DTO z polami i anomaliami |
| `inwentaryzacja_automappera.md` | 7 profili AutoMapper z kodem |
| `inwentaryzacja_rol.md` | 1 rola (User), JWT, anomalie bezpieczeństwa |
| `inwentaryzacja_procesow.md` | 15 procesów backendowych (P-01..P-15) |
| `inwentaryzacja_algorytmow.md` | 10 algorytmów (ALG-01..ALG-10) |
| `inwentaryzacja_api.md` | 31 endpointów API |
| `inwentaryzacja_linq.md` | 5 zapytań LINQ (LINQ-01..LINQ-05) |

#### Mapy krzyżowe

| Plik | ID | Opis |
|---|---|---|
| `mapa_db_dto_ekrany.md` | M-02 | Kolumna DB ↔ pole DTO ↔ pole UI |
| `mapa_api_dto_linq_db.md` | M-03 | Endpoint ↔ DTO ↔ LINQ ↔ tabela |
| `mapa_uc_bpmn.md` | M-04 | UC ↔ procesy biznesowe |
| `mapa_warstwowa.md` | M-05 | UC → ekran → API → DB |
| `pokrycie_testow.md` | M-06 | UC / ekran ↔ scenariusze testowe |
| `mapa_rol_ekranow_operacji.md` | M-07 | Rola × ekran × operacja |
| `mapa_uprawnien_api.md` | M-08 | Uprawnienie ↔ endpointy |
| `mapa_integracji_procesow.md` | M-09 | Integracja (ANAF) ↔ procesy |
| `mapa_przejsc_ekranow.md` | M-10 | Diagram przejść między ekranami |

---

### `00_meta/` — Metadokumenty projektu

| Plik | ID | Opis |
|---|---|---|
| `01_o_projekcie.md` | — | Opis biznesowy, dług techniczny |
| `02_stos_technologiczny.md` | — | Tabela technologii i wersji |
| `03_architektura_aplikacji.md` | — | Clean Architecture, pipeline HTTP |
| `04_jak_poruszac_sie_po_aplikacji.md` | — | Przewodnik nawigacji po dokumentacji |
| `05_drzewo_projektu.md` | — | Drzewo katalogów projektu |
| `06_globalne_mechanizmy.md` | — | JWT, interceptors, UoW, CORS, QuestPDF |

---

### `01_ekrany/` — Ekrany i komponenty Angular

> Nowe pliki (`ekran.md`, `modal.md`) to główne lokalizacje dokumentacji. Stare pliki angielskie zachowane dla kompatybilności.

#### Ekrany glowne (nowa polska struktura)

| Plik | ID | Opis |
|---|---|---|
| `login/ekran.md` | EKRAN-01 | Logowanie |
| `register/ekran.md` | EKRAN-02 | Rejestracja |
| `dashboard/ekran.md` | EKRAN-03 | Dashboard ze statystykami |
| `firma/dane_firmy/ekran.md` | EKRAN-04 | Dane wlasnej firmy |
| `firma/klienci/ekran.md` | EKRAN-05 | Lista klientow |
| `firma/konta_bankowe/ekran.md` | EKRAN-06 | Konta bankowe |
| `produkty/ekran.md` | EKRAN-07 | Katalog produktow |
| `serie_dokumentow/ekran.md` | EKRAN-08 | Serie numeracji |
| `faktury/lista_faktur/ekran.md` | EKRAN-09 | Lista faktur |
| `faktury/dodaj_edytuj_fakture/ekran.md` | EKRAN-10 | Formularz faktury |
| `faktury_proforma/lista_faktur_proforma/ekran.md` | EKRAN-11 | Lista proform |
| `faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md` | EKRAN-12 | Formularz proformy |
| `faktury_storno/lista_faktur_storno/ekran.md` | EKRAN-13 | Lista stoern |
| `faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` | EKRAN-14 | Formularz storna |

#### Dialogi (nowa polska struktura)

| Plik | ID | Opis |
|---|---|---|
| `firma/klienci/dialog_dodaj_klienta/modal.md` | DIALOG-01 | Dialog klienta |
| `firma/konta_bankowe/dialog_dodaj_konto/modal.md` | DIALOG-02 | Dialog konta bankowego |
| `produkty/dialog_dodaj_produkt/modal.md` | DIALOG-03 | Dialog produktu |
| `serie_dokumentow/dialog_dodaj_serie/modal.md` | DIALOG-04 | Dialog serii |
| `00_wspolne/modale_wspolne/pdf_viewer/modal.md` | DIALOG-05 | Podglad PDF |
| `00_wspolne/modale_wspolne/token_expired_dialog/modal.md` | DIALOG-06 | Dialog wygasniecia tokenu |

#### Wspolne komponenty

| Plik | ID | Opis |
|---|---|---|
| `00_wspolne/navbar/ekran.md` | LAYOUT-01 | NavbarComponent |
| `00_wspolne/sidebar/ekran.md` | LAYOUT-02 | SidebarComponent |
| `00_wspolne/base_invoice_component/ekran.md` | BASE-01 | BaseInvoiceComponent (abstrakt) |

#### Dodatkowe pliki

| Plik | Opis |
|---|---|
| `mapa_przejsc.md` | Mapa przejsc miedzy ekranami (lokalna) |

---

### `02_procesy/` — Procesy techniczne (Backend)

> Nowe pliki `proces.md` w podfolderach to glowna dokumentacja. Stare P-01..P-15 zachowane dla kompatybilnosci.

#### Autentykacja

| Plik | Opis |
|---|---|
| `autentykacja/rejestracja/proces.md` | Rejestracja uzytkownika |
| `autentykacja/logowanie/proces.md` | Logowanie |

#### Firma

| Plik | Opis |
|---|---|
| `firma/dodaj_firme/proces.md` | Dodawanie firmy |
| `firma/edytuj_firme/proces.md` | Edycja firmy |
| `firma/usun_firme/proces.md` | Usuniecie firmy |
| `firma/pobierz_aktywna_firme/proces.md` | Pobieranie aktywnej firmy |
| `firma/pobierz_firmy_klientow/proces.md` | Pobieranie firm klientow |
| `firma/pobierz_z_anaf/proces.md` | Pobieranie danych z ANAF |

#### Produkty

| Plik | Opis |
|---|---|
| `produkty/dodaj_produkt/proces.md` | Dodawanie produktu |
| `produkty/edytuj_produkt/proces.md` | Edycja produktu |
| `produkty/pobierz_produkty/proces.md` | Pobieranie produktow |
| `produkty/usun_produkty/proces.md` | Usuniecie produktow |

#### Konta bankowe

| Plik | Opis |
|---|---|
| `konta_bankowe/dodaj_konto/proces.md` | Dodawanie konta bankowego |
| `konta_bankowe/edytuj_konto/proces.md` | Edycja konta bankowego |
| `konta_bankowe/pobierz_konta/proces.md` | Pobieranie kont bankowych |
| `konta_bankowe/usun_konta/proces.md` | Usuniecie kont bankowych |

#### Serie dokumentow

| Plik | Opis |
|---|---|
| `serie_dokumentow/dodaj_serie/proces.md` | Dodawanie serii |
| `serie_dokumentow/edytuj_serie/proces.md` | Edycja serii |
| `serie_dokumentow/pobierz_serie/proces.md` | Pobieranie serii |
| `serie_dokumentow/usun_serie/proces.md` | Usuniecie serii |

#### Dokumenty

| Plik | Opis |
|---|---|
| `dokumenty/dodaj_dokument/proces.md` | Dodawanie dokumentu |
| `dokumenty/edytuj_dokument/proces.md` | Edycja dokumentu |
| `dokumenty/pobierz_dokumenty/proces.md` | Pobieranie dokumentow |
| `dokumenty/usun_dokumenty/proces.md` | Usuniecie dokumentow |
| `dokumenty/generuj_pdf/proces.md` | Generowanie PDF |
| `dokumenty/pobierz_autouzupelnienie/proces.md` | Dane autouzupelnienia |
| `dokumenty/dashboard_statystyki/proces.md` | Statystyki dashboardu |
| `dokumenty/transformuj_na_storno/proces.md` | Konwersja na storno |

---

### `03_algorytmy/` — Algorytmy i mechanizmy

> Nowe pliki w podfolderach kategorii to glowna dokumentacja. Stare ALG-01..ALG-10 zachowane dla kompatybilnosci.

#### Walidacji

| Plik | Opis |
|---|---|
| `walidacji/walidacja_hasla.md` | Walidacja hasla (BCrypt) |

#### Autoryzacyjne

| Plik | Opis |
|---|---|
| `autoryzacyjne/weryfikacja_tokenu_jwt.md` | Weryfikacja tokenu JWT |
| `autoryzacyjne/tworzenie_tokenu_jwt.md` | Tworzenie tokenu JWT |

#### Generowania PDF

| Plik | Opis |
|---|---|
| `generowania_pdf/generuj_pdf_na_dysk.md` | Generowanie PDF na dysk |
| `generowania_pdf/generuj_pdf_stream.md` | Generowanie PDF jako stream |

#### Wyliczeniowe

| Plik | Opis |
|---|---|
| `wyliczeniowe/obliczanie_wartosci_dokumentu.md` | Obliczanie wartosci dokumentu |

#### Dedykowane

| Plik | Opis |
|---|---|
| `dedykowane/generowanie_numeru_dokumentu.md` | Generowanie numeru dokumentu |
| `dedykowane/integracja_anaf.md` | Integracja z ANAF |
| `dedykowane/transformacja_na_storno.md` | Transformacja na storno |
| `dedykowane/pipeline_obslugi_wyjatkow.md` | Pipeline obslugi wyjatkow |
| `dedykowane/izolacja_danych_userfirm.md` | Izolacja danych miedzy uzytkownikami |
| `dedykowane/seed_typow_dokumentow.md` | Seed typow dokumentow (DbSeeder) |

---

### `04_api_i_integracje/`

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
| `ANAF_integracja.md` | Szczegoly integracji z API ANAF |

#### `03_db_seeder/` — Seedowanie danych

| Plik | Opis |
|---|---|
| `DbSeeder.md` | Inicjalizacja danych slownikowych |

---

### `05_model_danych/` — Model danych

#### `01_db/` — Baza danych

| Plik | Opis |
|---|---|
| `erd_globalny.md` | ERD — diagram encji (globalny) |
| `dbo/erd_dbo.md` | ERD schematu dbo |
| `spis_schem_i_tabel.md` | Spis 10 tabel, FK, indeksy |
| `dbo/dbo.User.md` | Tabela User |
| `dbo/dbo.Firm.md` | Tabela Firm |
| `dbo/dbo.UserFirm.md` | Tabela UserFirm |
| `dbo/dbo.UserFirm_relations.md` | Relacje UserFirm |
| `dbo/dbo.BankAccount.md` | Tabela BankAccount |
| `dbo/dbo.Product.md` | Tabela Product |
| `dbo/dbo.DocumentSeries.md` | Tabela DocumentSeries |
| `dbo/dbo.Document.md` | Tabela Document |
| `dbo/dbo.DocumentProduct.md` | Tabela DocumentProduct |
| `dbo/dbo.DocumentStatus.md` | Tabela DocumentStatus |
| `dbo/dbo.DocumentType.md` | Tabela DocumentType |

#### `02_dto/` — Data Transfer Objects

| Plik | ID | Opis |
|---|---|---|
| `spis_dto.md` | — | Spis wszystkich DTO |
| `DTO-01_RegisterUserDto.md` | DTO-01 | Rejestracja |
| `DTO-02_LoginUserDto.md` | DTO-02 | Logowanie |
| `DTO-03_FirmRequestDto.md` | DTO-03 | Dane firmy |
| `DTO-04_BankAccountRequestDto.md` | DTO-04 | Konto bankowe |
| `DTO-05_ProductRequestDto.md` | DTO-05 | Produkt |
| `DTO-06_DocumentSeriesRequestDto.md` | DTO-06 | Seria dokumentow |
| `DTO-07_DocumentRequestDto.md` | DTO-07 | Dokument (glowny) |
| `DTO-08_DocumentProductRequestDto.md` | DTO-08 | Pozycja dokumentu |
| `DTO-09_DocumentTableRecordDto.md` | DTO-09 | Rekord listy dokumentow |
| `DTO-10_DocumentAutofillInfoDto.md` | DTO-10 | Dane autouzupelnienia |
| `DTO-11_DocumentStatusDto.md` | DTO-11 | Status dokumentu |
| `DTO-12_DashboardStatsDto.md` | DTO-12 | Statystyki dashboardu |
| `DTO-13_UserDto.md` | DTO-13 | Token JWT (response auth) |
| `DTO-14_UserFirmDto.md` | DTO-14 | Powiazanie User-Firm |

#### `03_linq/` — Zapytania LINQ

| Plik | ID | Opis |
|---|---|---|
| `LINQ-01_GetDocumentById.md` | LINQ-01 | Pelny dokument z Include |
| `LINQ-02_GetTableRecords.md` | LINQ-02 | Lista dokumentow |
| `LINQ-03_GetDashboardStats.md` | LINQ-03 | Statystyki z agregacja |
| `LINQ-04_GetUserActiveFirm.md` | LINQ-04 | Aktywna firma uzytkownika |
| `LINQ-05_GetUserClientFirms.md` | LINQ-05 | Firmy klientow uzytkownika |

#### `04_zapytania_bezposrednie/` — Zapytania bezposrednie SQL

| Stan | Opis |
|---|---|
| (pusty) | Zarezerwowane — brak zapytan SQL w biezacej wersji |

#### `05_automapper/` — Profile AutoMapper

| Plik | ID | Opis |
|---|---|---|
| `AM-01_AuthProfile.md` | AM-01 | RegisterUserDto → User |
| `AM-02_FirmProfile.md` | AM-02 | FirmRequestDto ↔ Firm |
| `AM-03_BankAccountProfile.md` | AM-03 | BankAccountRequestDto ↔ BankAccount |
| `AM-04_ProductProfile.md` | AM-04 | ProductRequestDto ↔ Product |
| `AM-05_DocumentSeriesProfile.md` | AM-05 | DocumentSeriesRequestDto ↔ DocumentSeries |
| `AM-06_DocumentProfile.md` | AM-06 | Document ↔ DTOs (zlozone mapowania) |
| `AM-07_UserFirmProfile.md` | AM-07 | UserFirm → FirmRequestDto (Seller) |

#### `06_skrypty/` — Skrypty inicjalizacyjne

| Plik | Opis |
|---|---|
| `DbSeeder.md` | Inicjalizacja danych slownikowych (typy dokumentow, statusy) |

---

### `06_role_i_uprawnienia/`

| Plik | Opis |
|---|---|
| `lista_rol.md` | Lista rol (tylko "User") |
| `User.md` | Uprawnienia roli User |
| `macierz_role_uprawnienia.md` | Macierz endpoint x rola |
| `lista_uprawnien.md` | Lista uprawnien UPR-01..UPR-12 |
| `audyt_bezpieczenstwa.md` | Audyt bezpieczenstwa |

---

### `07_use_case/` — Przypadki uzycia

> Nowa struktura podfolderow — zastepuje stare UC-01..UC-04.

#### globalny/

| Plik | Opis |
|---|---|
| `globalny/uc_autentykacja.md` | Rejestracja, logowanie, wylogowanie |

#### firma/

| Plik | Opis |
|---|---|
| `firma/uc_firma.md` | Zarzadzanie firma i klientami |

#### produkty/ i konfiguracja/

| Plik | Opis |
|---|---|
| `produkty/uc_produkty.md` | Zarzadzanie produktami |
| `konta_bankowe/uc_konta_bankowe.md` | Zarzadzanie kontami bankowymi |
| `serie_dokumentow/uc_serie_dokumentow.md` | Zarzadzanie seriami dokumentow |

#### dokumenty/

| Plik | Opis |
|---|---|
| `dokumenty/uc_faktury.md` | Wystawianie i zarzadzanie fakturami |
| `dokumenty/uc_faktury_proforma.md` | Wystawianie i zarzadzanie proformami |
| `dokumenty/uc_faktury_storno.md` | Wystawianie i zarzadzanie stornami |
| `dokumenty/uc_dashboard.md` | Podglad statystyk (dashboard) |

---

### `08_model_biznesowy/`

| Plik | Opis |
|---|---|
| `model_glowny.md` | Diagram klas — model domenowy |
| `model_biznesowy.md` | Opis produktu, segment rynku, dlug techniczny (legacy) |

#### klasy/

| Plik | Opis |
|---|---|
| `klasy/Uzytkownik.md` | Klasa biznesowa Uzytkownik |
| `klasy/Firma.md` | Klasa biznesowa Firma |
| `klasy/Klient.md` | Klasa biznesowa Klient |
| `klasy/KontoBankowe.md` | Klasa biznesowa KontoBankowe |
| `klasy/ProduktKatalogowy.md` | Klasa biznesowa ProduktKatalogowy |
| `klasy/SeriaDokumentow.md` | Klasa biznesowa SeriaDokumentow |
| `klasy/Dokument.md` | Klasa biznesowa Dokument |
| `klasy/PozycjaDokumentu.md` | Klasa biznesowa PozycjaDokumentu |

#### perspektywy/ i aktorzy/

| Plik | Opis |
|---|---|
| `perspektywy/perspektywa_dokumentow.md` | Perspektywa domeny dokumentow |
| `aktorzy/Uzytkownik.md` | Aktor: Uzytkownik systemu |

---

### `09_procesy_biznesowe/` — Procesy BPMN

> Nowa struktura podfolderow — zastepuje stare BPMN-01..BPMN-02.

| Plik | Opis |
|---|---|
| `mapa_procesow.md` | Mapa wszystkich procesow biznesowych |

#### autentykacja/

| Plik | Opis |
|---|---|
| `autentykacja/rejestracja_i_logowanie.md` | BPMN — rejestracja i logowanie |

#### firma/

| Plik | Opis |
|---|---|
| `firma/zarzadzanie_firma.md` | BPMN — zarzadzanie firma |

#### dokumenty/

| Plik | Opis |
|---|---|
| `dokumenty/wystawienie_faktury.md` | BPMN — wystawienie faktury |
| `dokumenty/wystawienie_proformy.md` | BPMN — wystawienie proformy |
| `dokumenty/wystawienie_storno.md` | BPMN — wystawienie storna |
| `dokumenty/eksport_pdf.md` | BPMN — eksport do PDF |

#### konfiguracja/

| Plik | Opis |
|---|---|
| `konfiguracja/konfiguracja_firmy.md` | BPMN — konfiguracja firmy |

---

### `10_testy/`

> Nowa struktura podfolderowa — zastepuje stary plan_testow.md.

#### manualne/

| Plik | Opis |
|---|---|
| `manualne/autentykacja/testy_autentykacji.md` | Testy manualne — autentykacja |
| `manualne/firma/testy_firmy.md` | Testy manualne — firma |
| `manualne/produkty/testy_produktow.md` | Testy manualne — produkty |
| `manualne/konta_bankowe/testy_kont_bankowych.md` | Testy manualne — konta bankowe |
| `manualne/serie_dokumentow/testy_serii_dokumentow.md` | Testy manualne — serie dokumentow |
| `manualne/dokumenty/testy_dokumentow.md` | Testy manualne — dokumenty |

#### automatyczne/

| Plik | Opis |
|---|---|
| `automatyczne/README.md` | Plan testow automatycznych |
| `automatyczne/api/README.md` | Testy API (zarezerwowane) |

#### pokrycie/

| Plik | Opis |
|---|---|
| `pokrycie/pokrycie_uc.md` | Pokrycie testami — przypadkow uzycia |
| `pokrycie/pokrycie_procesow.md` | Pokrycie testami — procesow |
| `pokrycie/pokrycie_ekranow.md` | Pokrycie testami — ekranow |

#### Pliki zachowane (legacy)

| Plik | Opis |
|---|---|
| `plan_testow.md` | Oryginalny plan testow (legacy) |

---

### `_slowniki/` — Slowniki

| Plik | Opis |
|---|---|
| `slownik_biznesowy.md` | Slownik terminow biznesowych |
| `slownik_techniczny.md` | Slownik terminow technicznych |
| `slownik_elementow_dokumentacji.md` | Slownik elementow dokumentacji |
| `slownik_skrotow.md` | Slownik skrotow i akronimow |
| `slownik_prefiksow_id.md` | Slownik prefiksow identyfikatorow |
| `slownik_pojec.md` | Ogolny slownik pojec (legacy) |
| `slownik_anomalii.md` | Skonsolidowana lista 28 anomalii (4 krytyczne!) |

---

### `_szablony/` — Szablony dokumentow

> 20 szablonow SZABLON_* + 4 legacy TEMPLATE_*

| Plik | Opis |
|---|---|
| `SZABLON_algorytm.md` | Szablon opisu algorytmu |
| `SZABLON_api_endpoint.md` | Szablon endpointu API |
| `SZABLON_automapper.md` | Szablon profilu AutoMapper |
| `SZABLON_bpmn_proces.md` | Szablon procesu BPMN |
| `SZABLON_dto.md` | Szablon DTO |
| `SZABLON_ekran.md` | Szablon ekranu Angular |
| `SZABLON_filtr.md` | Szablon filtru |
| `SZABLON_integracja.md` | Szablon integracji zewnetrznej |
| `SZABLON_linq.md` | Szablon zapytania LINQ |
| `SZABLON_modal.md` | Szablon modalu/dialogu |
| `SZABLON_operacja.md` | Szablon operacji CRUD |
| `SZABLON_pole.md` | Szablon pola formularza |
| `SZABLON_powiadomienie.md` | Szablon powiadomienia |
| `SZABLON_proces.md` | Szablon procesu technicznego |
| `SZABLON_readme_katalogu.md` | Szablon README katalogu |
| `SZABLON_rola.md` | Szablon roli |
| `SZABLON_scenariusz_testowy.md` | Szablon scenariusza testowego |
| `SZABLON_tabela.md` | Szablon tabeli |
| `SZABLON_tabela_db.md` | Szablon tabeli bazy danych |
| `SZABLON_uc.md` | Szablon przypadku uzycia |

---

## TOP 4 Anomalie krytyczne

| ID | Opis | Ryzyko |
|---|---|---|
| A-KRIT-01 | **CASCADE DELETE konta bankowego usuwa faktury** | Utrata danych |
| A-KRIT-02 | **TransformToStorno — brak atomowosci** | Czesciowa konwersja |
| A-KRIT-03 | **Race condition na numerach dokumentow** | Duplikaty |
| A-KRIT-04 | **GenerateInvoicePdf hardkoduje szablon faktury** | Bledne PDF dla proform/stoern |

---

## Statystyki dokumentacji

| Kategoria | Liczba plikow |
|---|---|
| Inwentaryzacje | 9 |
| Mapy krzyzowe | 9 |
| Metadokumenty | 6 |
| Ekrany (nowa pl. struktura) | 14 ekran.md + 6 modal.md + 3 wspolne = 23 |
| Procesy (nowa pl. struktura) | 28 proces.md w podfolderach |
| Algorytmy (nowa struktura) | 11 nowych + 10 legacy = 21 |
| Endpointy API | 31 |
| Integracje zewnetrzne | 2 |
| Model danych (DB) | 14 (12 tabel + erd_dbo + spis) |
| DTO | 16 (14 DTO + spis_dto + README) |
| LINQ | 5 |
| AutoMapper profile | 7 |
| Role i uprawnienia | 5 |
| Use Cases (nowa struktura) | 9 uc_*.md w podfolderach |
| Model biznesowy | 11 (model_glowny + 8 klas + perspektywy + aktorzy) |
| Procesy BPMN (nowa struktura) | 7 (mapa + 6 procesow) |
| Testy (nowa struktura) | 13 (6 manualnych + 3 automatyczne + 3 pokrycie + legacy) |
| Slowniki | 7 (5 nowych + 2 legacy) |
| Szablony | 24 (20 SZABLON + 4 TEMPLATE legacy) |
| **LACZNIE** | **~250+ plikow** |
