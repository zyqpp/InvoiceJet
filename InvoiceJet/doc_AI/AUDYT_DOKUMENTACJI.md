# Raport audytu dokumentacji doc_AI — InvoiceJet

| Pole | Wartość |
|---|---|
| ID dokumentu | AUDYT-01 |
| Typ dokumentu | raport audytu |
| Wersja | 0.2 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Dokumentacja w `doc_AI/` jest **niekompletna i częściowo niezgodna z wytycznymi** określonymi w `wytyczne/02_struktura_dokumentacji.md` i `wytyczne/06_plan_i_kolejnosc_pracy.md`. Poprzednia sesja agenta wykonała Fazy 1–10 w trybie skróconym: zamiast wymaganej granularnej struktury podfolderów i plików stworzono dokumenty zbiorcze. Wiele wymaganych plików i folderów po prostu nie istnieje. Konwencje nazewnicze w kilku miejscach odbiegają od specyfikacji. Raport nie zawiera żadnych zmian w dokumentacji — jest wyłącznie diagnozą i wytyczną do pracy.

---

## CZĘŚĆ 1 — Niezgodności z wytycznymi (błędna struktura lub nazewnictwo)

Pliki istnieją, ale są umieszczone w złym miejscu lub mają złą nazwę niezgodną ze specyfikacją z `wytyczne/02_struktura_dokumentacji.md`.

### NZ-01 — `01_ekrany/` — foldery z angielskimi nazwami zamiast polskich

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md § D`):**
```
01_ekrany/
├── 00_wspolne/
├── firma/
│   ├── dane_firmy/
│   ├── klienci/
│   └── konta_bankowe/
├── produkty/
├── serie_dokumentow/
├── faktury/
├── faktury_proforma/
└── faktury_storno/
```

**Stan faktyczny:**
```
01_ekrany/
├── _wspolne/          ← powinno być: 00_wspolne/
├── firm_details/      ← powinno być: firma/dane_firmy/
├── clients/           ← powinno być: firma/klienci/
├── bank_accounts/     ← powinno być: firma/konta_bankowe/
├── products/          ← powinno być: produkty/
├── document_series/   ← powinno być: serie_dokumentow/
├── invoices/          ← powinno być: faktury/
├── invoice_proformas/ ← powinno być: faktury_proforma/
└── invoice_stornos/   ← powinno być: faktury_storno/
```

**Skutek:** Linki w README i INDEX wskazują na foldery z polskimi nazwami — żaden nie istnieje. Nawigacja jest zepsuta.

---

### NZ-02 — `01_ekrany/` — pliki ekranów w złej lokalizacji i złej nazwie

**Specyfikacja:** Każdy ekran ma **własny podfolder** z plikiem `ekran.md` wewnątrz:
```
01_ekrany/faktury/lista_faktur/ekran.md
01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md
```

**Stan faktyczny:** Pliki są umieszczone bezpośrednio w folderze grupy, z nazwą opisową:
```
01_ekrany/invoices/invoices.md
01_ekrany/invoices/add-or-edit-invoice.md
```

**Skutek:** Brak struktury per-ekran, brak możliwości dodania plików `pola/`, `operacje/` obok `ekran.md` w przyszłości.

---

### NZ-03 — `02_procesy/` — pliki płaskie zamiast w podfolderach

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md § E`):**
```
02_procesy/
├── autentykacja/rejestracja/proces.md
├── autentykacja/logowanie/proces.md
├── firma/dodaj_firme/proces.md
├── firma/pobierz_z_anaf/proces.md
...
└── dokumenty/transformuj_na_storno/proces.md
```

**Stan faktyczny:**
```
02_procesy/
├── P-01_RegisterUser.md
├── P-02_LoginUser.md
...
└── P-15_TransformToStorno.md
```

**Skutek:** Zbiorcze pliki (jeden plik = jeden proces) zamiast wymaganej struktury podfolderów. Nazwy angielskie zamiast polskich. Brak podfolderów uniemożliwia rozbudowę o plik `scenariusze_testowe.md` czy `analiza_bledow.md` per proces.

---

### NZ-04 — `03_algorytmy/` — pliki płaskie zamiast w podfolderach

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md § F`):**
```
03_algorytmy/
├── walidacji/walidacja_hasla.md
├── autoryzacyjne/tworzenie_tokenu_jwt.md
├── autoryzacyjne/weryfikacja_tokenu_jwt.md
├── generowania_pdf/generuj_pdf_na_dysk.md
├── generowania_pdf/generuj_pdf_stream.md
├── wyliczeniowe/obliczanie_wartosci_dokumentu.md
└── dedykowane/seed_typow_dokumentow.md
```

**Stan faktyczny:**
```
03_algorytmy/
├── ALG-01_JwtAuthentication.md
├── ALG-02_DocumentNumberGeneration.md
...
└── ALG-10_DataIsolationPattern.md
```

**Skutek:** Brak podziału na kategorie (`walidacji/`, `autoryzacyjne/`, itd.), angielskie nazwy plików.

---

### NZ-05 — `05_model_danych/` — błędna numeracja podfolderów

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md § H`):**
```
05_model_danych/
├── 01_db/
├── 02_dto/
├── 03_linq/
├── 04_zapytania_bezposrednie/
├── 05_automapper/
└── 06_skrypty/
```

**Stan faktyczny:**
```
05_model_danych/
├── 01_db/       ✅
├── 02_linq/     ← powinno być: 03_linq/
├── 03_dto/      ← powinno być: 02_dto/
└── 04_automapper/ ← powinno być: 05_automapper/
```

**Skutek:** DTO jest pod numerem 3 zamiast 2 (zgodnie ze spec: DB→DTO→LINQ→AutoMapper). Linki w `05_model_danych/README.md` są zepsute bo wskazują na prawidłowe numery ze specyfikacji.

---

### NZ-06 — `_szablony/` — błędny prefiks nazw szablonów

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md`, `_szablony/README.md`):**
Pliki szablonów mają prefix `SZABLON_`, np. `SZABLON_ekran.md`, `SZABLON_pole.md`.

**Stan faktyczny:**
Istniejące 4 szablony mają prefix `TEMPLATE_`: `TEMPLATE_EKRAN.md`, `TEMPLATE_PROCES.md`, `TEMPLATE_ENDPOINT.md`, `TEMPLATE_DTO.md`.

**Skutek:** Niezgodność z konwencją i z README katalogu.

---

### NZ-07 — `04_api_i_integracje/` — błędna struktura integracji zewnętrznych

**Specyfikacja (`wytyczne/02_struktura_dokumentacji.md § G`):**
```
04_api_i_integracje/
└── 02_systemy_dziedzinowe/
    ├── README.md
    └── anaf/
        └── pobierz_dane_firmy.md
```

**Stan faktyczny:**
```
04_api_i_integracje/
├── 02_anaf/ANAF_integracja.md
└── 03_db_seeder/DbSeeder.md
```

**Skutek:** DbSeeder nie jest integracją zewnętrzną — powinien być w `05_model_danych/06_skrypty/`. Folder `anaf/` powinien być wewnątrz `02_systemy_dziedzinowe/`.

---

## CZĘŚĆ 2 — Brakujące pliki i foldery (dokumentacja niekompletna)

### SEKCJA `01_ekrany/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `01_ekrany/mapa_przejsc.md` | ❌ brak |
| `01_ekrany/00_wspolne/README.md` | ❌ brak |
| `01_ekrany/00_wspolne/navbar/ekran.md` | ❌ brak (jest `_wspolne/navbar.md`) |
| `01_ekrany/00_wspolne/sidebar/ekran.md` | ❌ brak (jest `_wspolne/sidebar.md`) |
| `01_ekrany/00_wspolne/modale_wspolne/token_expired_dialog/modal.md` | ❌ brak |
| `01_ekrany/login/README.md` | ❌ brak |
| `01_ekrany/login/ekran.md` | ❌ brak (jest `login/login.md`) |
| `01_ekrany/register/README.md` | ❌ brak |
| `01_ekrany/register/ekran.md` | ❌ brak |
| `01_ekrany/dashboard/README.md` | ❌ brak |
| `01_ekrany/dashboard/ekran.md` | ❌ brak |
| `01_ekrany/firma/README.md` | ❌ brak (folder nie istnieje) |
| `01_ekrany/firma/dane_firmy/ekran.md` | ❌ brak |
| `01_ekrany/firma/klienci/README.md` | ❌ brak |
| `01_ekrany/firma/klienci/ekran.md` | ❌ brak |
| `01_ekrany/firma/konta_bankowe/ekran.md` | ❌ brak |
| `01_ekrany/produkty/README.md` | ❌ brak |
| `01_ekrany/produkty/ekran.md` | ❌ brak |
| `01_ekrany/serie_dokumentow/README.md` | ❌ brak |
| `01_ekrany/serie_dokumentow/ekran.md` | ❌ brak |
| `01_ekrany/faktury/lista_faktur/ekran.md` | ❌ brak |
| `01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md` | ❌ brak |
| `01_ekrany/faktury_proforma/lista_faktur_proforma/ekran.md` | ❌ brak |
| `01_ekrany/faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md` | ❌ brak |
| `01_ekrany/faktury_storno/lista_faktur_storno/ekran.md` | ❌ brak |
| `01_ekrany/faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` | ❌ brak |

**Łącznie brakuje:** ~26 plików + ~15 folderów w sekcji ekranów

---

### SEKCJA `02_procesy/` — braki

Zgodnie ze specyfikacją każdy proces powinien mieć swój podfolder z `proces.md`:

| Wymagany folder/plik | Status |
|---|---|
| `02_procesy/autentykacja/README.md` | ❌ brak |
| `02_procesy/autentykacja/rejestracja/proces.md` | ❌ brak |
| `02_procesy/autentykacja/logowanie/proces.md` | ❌ brak |
| `02_procesy/firma/README.md` | ❌ brak |
| `02_procesy/firma/dodaj_firme/proces.md` | ❌ brak |
| `02_procesy/firma/pobierz_z_anaf/proces.md` | ❌ brak |
| `02_procesy/firma/edytuj_firme/proces.md` | ❌ brak |
| `02_procesy/firma/pobierz_aktywna_firme/proces.md` | ❌ brak |
| `02_procesy/firma/pobierz_firmy_klientow/proces.md` | ❌ brak |
| `02_procesy/firma/usun_firme/proces.md` | ❌ brak |
| `02_procesy/produkty/README.md` | ❌ brak |
| `02_procesy/produkty/pobierz_produkty/proces.md` | ❌ brak |
| `02_procesy/produkty/dodaj_produkt/proces.md` | ❌ brak |
| `02_procesy/produkty/edytuj_produkt/proces.md` | ❌ brak |
| `02_procesy/produkty/usun_produkty/proces.md` | ❌ brak |
| `02_procesy/konta_bankowe/README.md` | ❌ brak |
| `02_procesy/konta_bankowe/pobierz_konta/proces.md` | ❌ brak |
| `02_procesy/konta_bankowe/dodaj_konto/proces.md` | ❌ brak |
| `02_procesy/konta_bankowe/edytuj_konto/proces.md` | ❌ brak |
| `02_procesy/konta_bankowe/usun_konta/proces.md` | ❌ brak |
| `02_procesy/serie_dokumentow/README.md` | ❌ brak |
| `02_procesy/serie_dokumentow/pobierz_serie/proces.md` | ❌ brak |
| `02_procesy/serie_dokumentow/dodaj_serie/proces.md` | ❌ brak |
| `02_procesy/serie_dokumentow/edytuj_serie/proces.md` | ❌ brak |
| `02_procesy/serie_dokumentow/usun_serie/proces.md` | ❌ brak |
| `02_procesy/dokumenty/README.md` | ❌ brak |
| `02_procesy/dokumenty/dodaj_dokument/proces.md` | ❌ brak |
| `02_procesy/dokumenty/edytuj_dokument/proces.md` | ❌ brak |
| `02_procesy/dokumenty/pobierz_dokumenty/proces.md` | ❌ brak |
| `02_procesy/dokumenty/usun_dokumenty/proces.md` | ❌ brak |
| `02_procesy/dokumenty/generuj_pdf/proces.md` | ❌ brak |
| `02_procesy/dokumenty/pobierz_pdf_stream/proces.md` | ❌ brak |
| `02_procesy/dokumenty/dashboard_statystyki/proces.md` | ❌ brak |
| `02_procesy/dokumenty/transformuj_na_storno/proces.md` | ❌ brak |

**Uwaga:** Pliki `P-01_RegisterUser.md` ... `P-15_TransformToStorno.md` zawierają wartościową treść, która powinna zostać **przeniesiona** do właściwych `proces.md`.

---

### SEKCJA `03_algorytmy/` — braki

| Wymagany folder/plik | Odpowiednik w dokum. (do przeniesienia) |
|---|---|
| `03_algorytmy/walidacji/README.md` | ❌ brak |
| `03_algorytmy/walidacji/walidacja_hasla.md` | → z `ALG-03_PasswordHashingVerification.md` |
| `03_algorytmy/autoryzacyjne/README.md` | ❌ brak |
| `03_algorytmy/autoryzacyjne/tworzenie_tokenu_jwt.md` | → z `ALG-04_JwtTokenCreation.md` |
| `03_algorytmy/autoryzacyjne/weryfikacja_tokenu_jwt.md` | → z `ALG-01_JwtAuthentication.md` |
| `03_algorytmy/generowania_pdf/README.md` | ❌ brak |
| `03_algorytmy/generowania_pdf/generuj_pdf_na_dysk.md` | → z `ALG-07_PdfGeneration.md` (część) |
| `03_algorytmy/generowania_pdf/generuj_pdf_stream.md` | → z `ALG-07_PdfGeneration.md` (część) |
| `03_algorytmy/wyliczeniowe/README.md` | ❌ brak |
| `03_algorytmy/wyliczeniowe/obliczanie_wartosci_dokumentu.md` | → z `ALG-05_DocumentTotalCalculation.md` |
| `03_algorytmy/dedykowane/README.md` | ❌ brak |
| `03_algorytmy/dedykowane/seed_typow_dokumentow.md` | ❌ brak (brak osobnego dokumentu) |

---

### SEKCJA `04_api_i_integracje/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `04_api_i_integracje/01_api_frontend/README.md` | ❌ brak |
| `04_api_i_integracje/01_api_frontend/lista_api.md` | ❌ brak (kluczowy!) |
| `04_api_i_integracje/02_systemy_dziedzinowe/README.md` | ❌ brak |
| `04_api_i_integracje/02_systemy_dziedzinowe/anaf/pobierz_dane_firmy.md` | ❌ brak (jest `02_anaf/ANAF_integracja.md` — zła lokalizacja) |

---

### SEKCJA `05_model_danych/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `05_model_danych/01_db/README.md` | ❌ brak |
| `05_model_danych/01_db/dbo/erd_dbo.md` | ❌ brak |
| `05_model_danych/02_dto/README.md` | ❌ brak (folder ma numer 03, nie 02) |
| `05_model_danych/02_dto/spis_dto.md` | ❌ brak |
| `05_model_danych/04_zapytania_bezposrednie/README.md` | ❌ brak (folder nie istnieje) |
| `05_model_danych/06_skrypty/README.md` | ❌ brak (folder nie istnieje) |
| `05_model_danych/06_skrypty/DbSeeder.md` | ❌ brak (jest w złej lokalizacji: `04_api_i_integracje/03_db_seeder/`) |

---

### SEKCJA `06_role_i_uprawnienia/` — braki

| Wymagany plik | Status |
|---|---|
| `06_role_i_uprawnienia/lista_uprawnien.md` | ❌ brak |

---

### SEKCJA `07_use_case/` — braki

Specyfikacja wskazuje podfoldery per obszar:

| Wymagany plik/folder | Status |
|---|---|
| `07_use_case/globalny/README.md` | ❌ brak |
| `07_use_case/globalny/uc_autentykacja.md` | ❌ brak (jest `UC-01_ZarzadzanieKontem.md` — zła lokalizacja i nazwa) |
| `07_use_case/firma/README.md` | ❌ brak |
| `07_use_case/firma/uc_firma.md` | ❌ brak |
| `07_use_case/produkty/uc_produkty.md` | ❌ brak |
| `07_use_case/konta_bankowe/uc_konta_bankowe.md` | ❌ brak |
| `07_use_case/serie_dokumentow/uc_serie_dokumentow.md` | ❌ brak |
| `07_use_case/dokumenty/README.md` | ❌ brak |
| `07_use_case/dokumenty/uc_faktury.md` | ❌ brak |
| `07_use_case/dokumenty/uc_faktury_proforma.md` | ❌ brak |
| `07_use_case/dokumenty/uc_faktury_storno.md` | ❌ brak |
| `07_use_case/dokumenty/uc_dashboard.md` | ❌ brak |

---

### SEKCJA `08_model_biznesowy/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `08_model_biznesowy/model_glowny.md` | ❌ brak (jest `model_biznesowy.md` — nieprawidłowa nazwa) |
| `08_model_biznesowy/perspektywy/perspektywa_dokumentow.md` | ❌ brak |
| `08_model_biznesowy/klasy/Uzytkownik.md` | ❌ brak |
| `08_model_biznesowy/klasy/Firma.md` | ❌ brak |
| `08_model_biznesowy/klasy/Klient.md` | ❌ brak |
| `08_model_biznesowy/klasy/ProduktKatalogowy.md` | ❌ brak |
| `08_model_biznesowy/klasy/KontoBankowe.md` | ❌ brak |
| `08_model_biznesowy/klasy/SeriaDokumentow.md` | ❌ brak |
| `08_model_biznesowy/klasy/Dokument.md` | ❌ brak |
| `08_model_biznesowy/klasy/PozycjaDokumentu.md` | ❌ brak |
| `08_model_biznesowy/aktorzy/Uzytkownik.md` | ❌ brak |

---

### SEKCJA `09_procesy_biznesowe/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `09_procesy_biznesowe/mapa_procesow.md` | ❌ brak |
| `09_procesy_biznesowe/autentykacja/README.md` | ❌ brak |
| `09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md` | ❌ brak (jest `BPMN-02_Rejestracja_i_OnBoarding.md` — zła lokalizacja i nazwa) |
| `09_procesy_biznesowe/firma/README.md` | ❌ brak |
| `09_procesy_biznesowe/firma/zarzadzanie_firma.md` | ❌ brak |
| `09_procesy_biznesowe/dokumenty/README.md` | ❌ brak |
| `09_procesy_biznesowe/dokumenty/wystawienie_faktury.md` | ❌ brak (jest `BPMN-01_WystawienieFaktury.md` — zła lokalizacja i nazwa) |
| `09_procesy_biznesowe/dokumenty/wystawienie_proformy.md` | ❌ brak |
| `09_procesy_biznesowe/dokumenty/wystawienie_storno.md` | ❌ brak |
| `09_procesy_biznesowe/dokumenty/eksport_pdf.md` | ❌ brak |
| `09_procesy_biznesowe/konfiguracja/README.md` | ❌ brak |
| `09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md` | ❌ brak |

---

### SEKCJA `10_testy/` — braki

| Wymagany plik/folder | Status |
|---|---|
| `10_testy/manualne/README.md` | ❌ brak |
| `10_testy/manualne/autentykacja/` | ❌ brak (całe podfoldery) |
| `10_testy/manualne/firma/` | ❌ brak |
| `10_testy/manualne/produkty/` | ❌ brak |
| `10_testy/manualne/konta_bankowe/` | ❌ brak |
| `10_testy/manualne/serie_dokumentow/` | ❌ brak |
| `10_testy/manualne/dokumenty/` | ❌ brak |
| `10_testy/automatyczne/README.md` | ❌ brak |
| `10_testy/automatyczne/api/` | ❌ brak |
| `10_testy/pokrycie/pokrycie_uc.md` | ❌ brak |
| `10_testy/pokrycie/pokrycie_procesow.md` | ❌ brak |
| `10_testy/pokrycie/pokrycie_ekranow.md` | ❌ brak |

---

### SEKCJA `_mapowania/` — braki (9 map krzyżowych)

Wszystkie mapy fazy 11 (`wytyczne/07_mapowania_i_slowniki.md § B`) nie istnieją:

| Mapa | Plik | Status |
|---|---|---|
| M-02 | `mapa_db_dto_ekrany.md` | ❌ brak |
| M-03 | `mapa_api_dto_linq_db.md` | ❌ brak |
| M-04 | `mapa_uc_bpmn.md` | ❌ brak |
| M-05 | `mapa_warstwowa.md` | ❌ brak |
| M-06 | `pokrycie_testow.md` | ❌ brak |
| M-07 | `mapa_rol_ekranow_operacji.md` | ❌ brak |
| M-08 | `mapa_uprawnien_api.md` | ❌ brak |
| M-09 | `mapa_integracji_procesow.md` | ❌ brak |
| M-10 | `mapa_przejsc_ekranow.md` | ❌ brak |

---

### SEKCJA `_slowniki/` — braki (4 słowniki z 5 wymaganych)

Wymagane przez `wytyczne/07_mapowania_i_slowniki.md § D`:

| Słownik | Plik | Status |
|---|---|---|
| S-01 | `slownik_biznesowy.md` | ❌ brak (jest `slownik_pojec.md` — połączony, niezgodna nazwa) |
| S-02 | `slownik_techniczny.md` | ❌ brak (połączony z S-01 w `slownik_pojec.md`) |
| S-03 | `slownik_elementow_dokumentacji.md` | ❌ brak |
| S-04 | `slownik_skrotow.md` | ❌ brak |
| S-05 | `slownik_prefiksow_id.md` | ❌ brak |

---

### SEKCJA `_szablony/` — braki (16 szablonów z 20 wymaganych)

Wymagane przez `_szablony/README.md` (prefix `SZABLON_`):

| Szablon | Status |
|---|---|
| `SZABLON_ekran.md` | ❌ brak (jest `TEMPLATE_EKRAN.md` — zły prefiks) |
| `SZABLON_pole.md` | ❌ brak |
| `SZABLON_operacja.md` | ❌ brak |
| `SZABLON_filtr.md` | ❌ brak |
| `SZABLON_tabela.md` | ❌ brak |
| `SZABLON_modal.md` | ❌ brak |
| `SZABLON_powiadomienie.md` | ❌ brak |
| `SZABLON_proces.md` | ❌ brak (jest `TEMPLATE_PROCES.md` — zły prefiks) |
| `SZABLON_algorytm.md` | ❌ brak |
| `SZABLON_api_endpoint.md` | ❌ brak (jest `TEMPLATE_ENDPOINT.md` — zły prefiks) |
| `SZABLON_integracja.md` | ❌ brak |
| `SZABLON_tabela_db.md` | ❌ brak |
| `SZABLON_dto.md` | ❌ brak (jest `TEMPLATE_DTO.md` — zły prefiks) |
| `SZABLON_linq.md` | ❌ brak |
| `SZABLON_automapper.md` | ❌ brak |
| `SZABLON_rola.md` | ❌ brak |
| `SZABLON_uc.md` | ❌ brak |
| `SZABLON_bpmn_proces.md` | ❌ brak |
| `SZABLON_scenariusz_testowy.md` | ❌ brak |
| `SZABLON_readme_katalogu.md` | ❌ brak |

---

## CZĘŚĆ 3 — Zestawienie zbiorcze

### Stan realizacji poszczególnych faz

| Faza | Opis | Status |
|---|---|---|
| Faza 0 | Archiwizacja | ✅ Zrobione |
| Faza 1 | Rozpoznanie i inwentaryzacja | ✅ Zrobione |
| Faza 2 | Szkielet katalogów i szablony | ⚠️ Częściowo — foldery istnieją, szablony niezgodne z konwencją |
| Faza 3 | Model danych (DB, DTO, LINQ, AutoMapper) | ⚠️ Częściowo — treść istnieje, struktura niezgodna ze spec |
| Faza 4 | API i integracje | ⚠️ Częściowo — endpointy opisane, brak lista_api.md i README |
| Faza 5 | Role i uprawnienia | ⚠️ Częściowo — brak lista_uprawnien.md |
| Faza 6 | Ekrany | ⚠️ Częściowo — treść istnieje, struktura i nazwy niezgodne ze spec |
| Faza 7 | Procesy i algorytmy | ⚠️ Częściowo — treść istnieje, struktura podfolderów brakuje |
| Faza 8 | Model biznesowy | ⚠️ Częściowo — jeden zbiorczy plik zamiast struktury klas |
| Faza 9 | UC i BPMN | ⚠️ Częściowo — 4 UC i 2 BPMN zamiast pełnego pokrycia |
| Faza 10 | Testy | ⚠️ Szczątkowe — jeden plik zamiast struktury |
| Faza 11 | Słowniki, mapowania, README | ❌ Nie zrobione — mapy krzyżowe i słowniki brakują |
| Faza 12 | Walidacja | ❌ Nie zrobione |
| Faza 13 | Akceptacja | ❌ Nie zrobione |

---

## CZĘŚĆ 4 — Plan działań naprawczych

### Krok 1 — Napraw strukturę szablonów (Faza 2)

Stworzyć 16 brakujących szablonów z prefiksem `SZABLON_` w `_szablony/`.  
Zrobi to Agent-Szablonowy.

---

### Krok 2 — Napraw strukturę `01_ekrany/` (Faza 6)

1. Utwórz polskie foldery zgodnie ze specyfikacją (`firma/`, `faktury/`, itd.).
2. W każdym folderze utwórz `README.md` i `ekran.md` (przenosząc i przepisując treść z istniejących plików).
3. Utwórz `mapa_przejsc.md`.

Istniejące pliki (np. `invoices/invoices.md`) zawierają wartościową treść — należy ją przenieść do `faktury/lista_faktur/ekran.md`.

---

### Krok 3 — Napraw strukturę `02_procesy/` (Faza 7)

Utwórz podfoldery i przenieś treść z plików `P-XX_*.md` do odpowiednich `proces.md`.

---

### Krok 4 — Napraw strukturę `03_algorytmy/` (Faza 7)

Utwórz kategorie (`walidacji/`, `autoryzacyjne/`, itd.) i przenieś treść z `ALG-XX_*.md`.

---

### Krok 5 — Napraw numerację i strukturę `05_model_danych/` (Faza 3)

Przemianuj foldery na zgodne ze specyfikacją (02_dto, 03_linq, 05_automapper).  
Utwórz `02_dto/spis_dto.md`, `01_db/README.md`, `01_db/dbo/erd_dbo.md`.  
Przenieś `DbSeeder.md` do `06_skrypty/`.

---

### Krok 6 — Uzupełnij `04_api_i_integracje/` (Faza 4)

Utwórz `01_api_frontend/lista_api.md`, `01_api_frontend/README.md`, `02_systemy_dziedzinowe/` ze strukturą.

---

### Krok 7 — Uzupełnij `06_role_i_uprawnienia/` (Faza 5)

Utwórz `lista_uprawnien.md`.

---

### Krok 8 — Uzupełnij `07_use_case/`, `08_model_biznesowy/`, `09_procesy_biznesowe/` (Fazy 8–9)

Utwórz pełną strukturę podfolderów i brakujące pliki per obszar.

---

### Krok 9 — Uzupełnij `10_testy/` (Faza 10)

Utwórz strukturę testów manualnych i pliki pokrycia.

---

### Krok 10 — Uzupełnij `_slowniki/` i `_mapowania/` (Faza 11)

Utwórz 5 odrębnych słowników (S-01..S-05) i 9 map krzyżowych (M-02..M-10).  
To jest **najcenniejsza** brakująca warstwa dokumentacji dla AI/RAG.

---

## Wątpliwości i braki

- Czy pliki z nieprawidłowymi nazwami/lokalizacjami (np. `P-01_RegisterUser.md`, `ALG-01_*.md`) mają zostać **usunięte** po przeniesieniu treści, czy **zachowane** jako archiwum?
- Czy istniejąca treść w plikach zbiorczych (np. `model_biznesowy.md`) jest wystarczająca do rozbicia na osobne pliki klas, czy wymaga uzupełnienia?
- Decyzja właściciela projektu: czy `slownik_pojec.md` i `slownik_anomalii.md` (istniejące, wartościowe) zostają jako dodatkowe dokumenty obok wymaganych S-01..S-05?

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja raportu — błędna perspektywa (README jako źródło problemu). |
| 0.2 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Poprawiona perspektywa: dokumentacja niekompletna i niezgodna z wytycznymi. Pełna lista braków i planu naprawczego. |
