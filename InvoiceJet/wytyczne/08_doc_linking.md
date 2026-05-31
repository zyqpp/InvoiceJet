---
name: doc-linking
description: >-
  Zasady i mapa linkowania w dokumentacji InvoiceJet. Używaj gdy: piszesz nowy
  dokument (doc_user lub doc_AI/AOS), edytujesz istniejący, robisz review
  linkowania, dodajesz sekcję "Powiązane", ktoś pyta "jak zlinkować X z Y".
  Trigger: "zlinkuj", "dodaj linki", "review linkowania", "brakuje linków",
  pisanie/edycja jakiegokolwiek pliku .md w doc_user/ lub doc_AI/.
  Zasada: każde odwołanie do innego dokumentu musi być klikalnym linkiem.
---

# Skill: doc-linking — Linkowanie w dokumentacji InvoiceJet

## Zasada naczelna

> **Jeśli wymieniasz coś, do czego istnieje dokument — zawsze wstaw link.**
> Czytający nie powinien szukać — powinien kliknąć.

Dotyczy OBU systemów dokumentacji:
- **`doc_user/`** — dokumentacja użytkownika końcowego
- **`doc_AI/`** — dokumentacja techniczna AOS (Agent-Oriented Specification)

---

## 1. Kiedy linkować?

### ✅ Zawsze linkuj gdy:
- Wymieniasz nazwę ekranu (np. „Lista faktur", „Klienci", „Dashboard")
- Odwołujesz się do procesu lub instrukcji (np. „wystawianie faktury")
- Wymieniasz endpoint API (np. `GET /api/Document/GetDocumentTableRecords`)
- Wymieniasz tabelę bazy danych (np. `dbo.Document`, `dbo.Firm`)
- Wymieniasz DTO, AutoMapper profile, algorytm z identyfikatorem
- Piszesz „więcej szczegółów", „patrz", „szczegóły w", „opisano w"
- Wymieniasz inny dokument w sekcji „Powiązane" / „Rejestr zmian" / „Anomalie"
- Na końcu dokumentu — sekcja nawigacyjna (Powiązane / Następny krok)

### ❌ Nie linkuj gdy:
- Chodzi o ogólne pojęcie, nie konkretny dokument (np. „faktura VAT" jako pojęcie)
- Link prowadziłby do tego samego pliku (samolinkowanie)
- Fraza jest wewnątrz bloku kodu ` ``` `

---

## 2. Obliczanie ścieżek względnych

Zawsze używaj ścieżek **względnych** (nie absolutnych, nie zaczynających się od `/`).

```
# Ten sam folder:
od: 01_ekrany/10_faktury.md
do: 01_ekrany/10b_formularz_faktury.md
→  10b_formularz_faktury.md

# Między folderami (doc_user):
od: 02_procesy/P-06_wystawianie_faktury.md
do: 01_ekrany/10_faktury.md
→  ../01_ekrany/10_faktury.md

# Głęboka zagnieżdżona ścieżka (doc_AI):
od: 01_ekrany/faktury/lista_faktur/ekran.md
do: 04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md
→  ../../../04_api_i_integracje/01_api_frontend/document/GET_Document_GetTableRecords.md
```

**Reguła pomocnicza:** policz ile `../` potrzebujesz — tyle ile folderów musisz „wyjść" z pliku źródłowego.

---

## 3. Mapa linków — `doc_user/`

### Ekrany (`doc_user/01_ekrany/`)

| Nazwa w tekście | Plik docelowy |
|---|---|
| Logowanie, ekran logowania | `01_logowanie.md` |
| Rejestracja | `02_rejestracja.md` |
| Nawigacja, menu boczne, pasek górny, sidebar, navbar | `03_nawigacja.md` |
| Dashboard, pulpit główny | `04_dashboard.md` |
| Dane firmy, Firm Details | `05_dane_firmy.md` |
| Klienci, Clients, baza klientów | `06_klienci.md` |
| Konta bankowe, Bank Accounts | `07_konta_bankowe.md` |
| Produkty, Products, katalog produktów | `08_produkty.md` |
| Serie dokumentów, Document Series, numeracja | `09_serie_dokumentow.md` |
| Faktury (lista), Invoices, lista faktur | `10_faktury.md` |
| Formularz faktury, dodawanie/edycja faktury | `10b_formularz_faktury.md` |
| Proformy (lista), Invoice Proformas | `11_proformy.md` |
| Storna (lista), Invoice Stornos, faktury korygujące | `12_storna.md` |

*Ścieżki z `02_procesy/` → dodaj prefix `../01_ekrany/`*
*Ścieżki z `01_ekrany/` → użyj nazwy pliku bezpośrednio*

### Procesy (`doc_user/02_procesy/`)

| Nazwa w tekście | Plik docelowy |
|---|---|
| Rejestracja konta, zakładanie konta | `P-01_rejestracja.md` |
| Logowanie (instrukcja) | `P-02_logowanie.md` |
| Konfiguracja danych firmy | `P-03_konfiguracja_firmy.md` |
| Dodanie konta bankowego | `P-04_dodawanie_konta_bankowego.md` |
| Zarządzanie produktami | `P-05_zarzadzanie_produktami.md` |
| Konfiguracja serii dokumentów, numeracja | `P-05b_konfiguracja_serii.md` |
| Wystawianie faktury | `P-06_wystawianie_faktury.md` |
| Faktura korygująca, storno, Transform to Storno | `P-07_faktura_korygujaca.md` |
| Dodanie kontrahenta, dodanie klienta | `P-08_dodawanie_kontrahenta.md` |
| Wystawianie proformy | `P-09_wystawianie_proformy.md` |
| Generowanie PDF, podgląd PDF | `P-10_generowanie_pdf.md` |

*Ścieżki z `01_ekrany/` → dodaj prefix `../02_procesy/`*
*Ścieżki z `02_procesy/` → użyj nazwy pliku bezpośrednio*

---

## 4. Mapa linków — `doc_AI/`

Ścieżki podane względem korzenia `doc_AI/`.

### Ekrany (`01_ekrany/`)

| Ekran | Ścieżka |
|---|---|
| Login | `01_ekrany/login/ekran.md` |
| Register | `01_ekrany/register/ekran.md` |
| Dashboard | `01_ekrany/dashboard/ekran.md` |
| Dane firmy | `01_ekrany/firma/dane_firmy/ekran.md` |
| Klienci | `01_ekrany/firma/klienci/ekran.md` |
| Dialog: dodaj klienta | `01_ekrany/firma/klienci/dialog_dodaj_klienta/modal.md` |
| Konta bankowe | `01_ekrany/firma/konta_bankowe/ekran.md` |
| Dialog: dodaj konto | `01_ekrany/firma/konta_bankowe/dialog_dodaj_konto/modal.md` |
| Produkty | `01_ekrany/produkty/ekran.md` |
| Dialog: dodaj produkt | `01_ekrany/produkty/dialog_dodaj_produkt/modal.md` |
| Serie dokumentów | `01_ekrany/serie_dokumentow/ekran.md` |
| Dialog: dodaj serię | `01_ekrany/serie_dokumentow/dialog_dodaj_serie/modal.md` |
| Faktury (lista) | `01_ekrany/faktury/lista_faktur/ekran.md` |
| Faktura (formularz) | `01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md` |
| Proformy (lista) | `01_ekrany/faktury_proforma/lista_faktur_proforma/ekran.md` |
| Proforma (formularz) | `01_ekrany/faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md` |
| Storna (lista) | `01_ekrany/faktury_storno/lista_faktur_storno/ekran.md` |
| Storno (formularz) | `01_ekrany/faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` |
| Navbar | `01_ekrany/00_wspolne/navbar/ekran.md` |
| Sidebar | `01_ekrany/00_wspolne/sidebar/ekran.md` |
| PDF Viewer (modal) | `01_ekrany/00_wspolne/modale_wspolne/pdf_viewer/modal.md` |
| Token Expired Dialog | `01_ekrany/00_wspolne/modale_wspolne/token_expired_dialog/modal.md` |
| BaseInvoiceComponent | `01_ekrany/00_wspolne/base_invoice_component/ekran.md` |

### API (`04_api_i_integracje/01_api_frontend/`)

| Endpoint | Ścieżka (względem `01_api_frontend/`) |
|---|---|
| POST /Auth/register | `auth/POST_Auth_register.md` |
| POST /Auth/login | `auth/POST_Auth_login.md` |
| GET /Firm/GetUserActiveFirm | `firm/GET_Firm_GetUserActiveFirm.md` |
| POST /Firm/AddFirm | `firm/POST_Firm_AddFirm.md` |
| PUT /Firm/EditFirm | `firm/PUT_Firm_EditFirm.md` |
| GET /Firm/fromAnaf | `firm/GET_Firm_fromAnaf.md` |
| GET /Firm/GetUserClientFirms | `firm/GET_Firm_GetUserClientFirms.md` |
| PUT /Firm/DeleteFirms | `firm/PUT_Firm_DeleteFirms.md` |
| GET /BankAccount/GetAll | `bank_account/GET_BankAccount_GetAll.md` |
| POST /BankAccount/Add | `bank_account/POST_BankAccount_Add.md` |
| PUT /BankAccount/Edit | `bank_account/PUT_BankAccount_Edit.md` |
| PUT /BankAccount/Delete | `bank_account/PUT_BankAccount_Delete.md` |
| GET /Product/GetAll | `product/GET_Product_GetAll.md` |
| POST /Product/Add | `product/POST_Product_Add.md` |
| PUT /Product/Edit | `product/PUT_Product_Edit.md` |
| PUT /Product/Delete | `product/PUT_Product_Delete.md` |
| GET /DocumentSeries/GetAll | `document_series/GET_DocumentSeries_GetAll.md` |
| POST /DocumentSeries/Add | `document_series/POST_DocumentSeries_Add.md` |
| PUT /DocumentSeries/Update | `document_series/PUT_DocumentSeries_Update.md` |
| PUT /DocumentSeries/Delete | `document_series/PUT_DocumentSeries_Delete.md` |
| GET /Document/GetTableRecords | `document/GET_Document_GetTableRecords.md` |
| GET /Document/GetById | `document/GET_Document_GetById.md` |
| POST /Document/Add | `document/POST_Document_Add.md` |
| PUT /Document/Edit | `document/PUT_Document_Edit.md` |
| PUT /Document/Delete | `document/PUT_Document_Delete.md` |
| POST /Document/GeneratePdf | `document/POST_Document_GeneratePdf.md` |
| POST /Document/GetPdfStream | `document/POST_Document_GetPdfStream.md` |
| GET /Document/GetAutofillInfo | `document/GET_Document_GetAutofillInfo.md` |
| GET /Document/GetDashboardStats | `document/GET_Document_GetDashboardStats.md` |
| PUT /Document/TransformToStorno | `document/PUT_Document_TransformToStorno.md` |

### Tabele DB (`05_model_danych/01_db/dbo/`)

| Tabela | Plik |
|---|---|
| dbo.User | `dbo.User.md` |
| dbo.Firm | `dbo.Firm.md` |
| dbo.UserFirm | `dbo.UserFirm.md` |
| dbo.BankAccount | `dbo.BankAccount.md` |
| dbo.Product | `dbo.Product.md` |
| dbo.Document | `dbo.Document.md` |
| dbo.DocumentProduct | `dbo.DocumentProduct.md` |
| dbo.DocumentSeries | `dbo.DocumentSeries.md` |
| dbo.DocumentStatus | `dbo.DocumentStatus.md` |
| dbo.DocumentType | `dbo.DocumentType.md` |

### DTO (`05_model_danych/02_dto/`)

| DTO | Plik |
|---|---|
| RegisterUserDto | `DTO-01_RegisterUserDto.md` |
| LoginUserDto | `DTO-02_LoginUserDto.md` |
| FirmRequestDto | `DTO-03_FirmRequestDto.md` |
| BankAccountRequestDto | `DTO-04_BankAccountRequestDto.md` |
| ProductRequestDto | `DTO-05_ProductRequestDto.md` |
| DocumentSeriesRequestDto | `DTO-06_DocumentSeriesRequestDto.md` |
| DocumentRequestDto | `DTO-07_DocumentRequestDto.md` |
| DocumentProductRequestDto | `DTO-08_DocumentProductRequestDto.md` |
| DocumentTableRecordDto | `DTO-09_DocumentTableRecordDto.md` |
| DocumentAutofillInfoDto | `DTO-10_DocumentAutofillInfoDto.md` |
| DocumentStatusDto | `DTO-11_DocumentStatusDto.md` |
| DashboardStatsDto | `DTO-12_DashboardStatsDto.md` |

### Algorytmy (`03_algorytmy/`)

| Algorytm | Plik |
|---|---|
| ALG-01 JWT Authentication | `ALG-01_JwtAuthentication.md` |
| ALG-02 Document Number Generation | `ALG-02_DocumentNumberGeneration.md` |
| ALG-03 Password Hashing | `ALG-03_PasswordHashingVerification.md` |
| ALG-04 JWT Token Creation | `ALG-04_JwtTokenCreation.md` |
| ALG-05 Document Total Calculation | `ALG-05_DocumentTotalCalculation.md` |
| ALG-06 ANAF Integration | `ALG-06_AnafIntegration.md` |
| ALG-07 PDF Generation | `ALG-07_PdfGeneration.md` |
| ALG-08 Transform to Storno | `ALG-08_TransformToStorno.md` |
| ALG-09 Exception Middleware Pipeline | `ALG-09_ExceptionMiddlewarePipeline.md` |
| ALG-10 Data Isolation Pattern | `ALG-10_DataIsolationPattern.md` |

---

## 5. Wzorce gotowych fragmentów

### Koniec ekranu — doc_user

```markdown
---

📖 Instrukcja krok po kroku: [P-XX Nazwa procesu](../02_procesy/P-XX_nazwa.md)

🔗 Powiązane: [Ekran A](ekran_a.md) · [Ekran B](ekran_b.md)
```

### Koniec procesu — doc_user

```markdown
---

🖥️ Opis ekranu: [Nazwa ekranu](../01_ekrany/XX_nazwa.md)

➡️ Następny krok: [P-XX Nazwa](P-XX_nazwa.md)
```

### Tabela "Powiązane" — doc_AI (ekran lub proces)

```markdown
## Powiązane

| Typ | Dokument |
|---|---|
| Ekran | [Lista faktur](../../faktury/lista_faktur/ekran.md) |
| API | [POST /Document/Add](../../../04_api_i_integracje/01_api_frontend/document/POST_Document_Add.md) |
| Model | [dbo.Document](../../../05_model_danych/01_db/dbo/dbo.Document.md) |
| DTO | [DocumentRequestDto](../../../05_model_danych/02_dto/DTO-07_DocumentRequestDto.md) |
| Algorytm | [ALG-05 Document Total Calculation](../../../03_algorytmy/ALG-05_DocumentTotalCalculation.md) |
| Proces | [P-08 AddDocument](../../../02_procesy/P-08_AddDocument.md) |
```

### README/index folderu

```markdown
# Nazwa folderu

Krótki opis zawartości (1–2 zdania).

## Zawartość

| Plik | Opis |
|---|---|
| [nazwa.md](nazwa.md) | Co opisuje |

---
⬆️ [Folder nadrzędny](../README.md) · 🔗 [Powiązany folder](../inny/README.md)
```

---

## 6. Tryb: pisanie nowego dokumentu

1. Wczytaj ten skill na początku sesji
2. Pisząc każdy akapit — przy każdej nazwie ekranu/procesu/API/modelu sprawdź mapę §3/§4 i wstaw link
3. Na końcu dokumentu dodaj sekcję nawigacyjną wg §5
4. Jeśli to dokument AOS — dodaj tabelę `## Powiązane`

---

## 7. Tryb: review linkowania

Szukaj tych fraz — każda **bez linku** to błąd:

**doc_user i doc_AI:**
`logowani` · `rejestracj` · `dashboard` · `pulpit` · `dane firmy` · `klientów` · `kontrahent`
`konta bankowe` · `produktów` · `serii dokumentów` · `faktur` · `proform` · `storn`

**Tylko doc_AI:**
`GET /api/` · `POST /api/` · `PUT /api/` · `dbo.` · `Dto` · `RequestDto`
`ALG-` · `EKRAN-` · `DIALOG-` · `LAYOUT-` · `DTO-` · `AM-` · `LINQ-`

**Universalne:**
`patrz` · `szczegóły w` · `więcej w` · `opisano w` · `zob.`

---

## 8. Aktualizacja tej mapy

Gdy dodajesz nowe dokumenty do `doc_user/` lub `doc_AI/`:
1. Dodaj wiersz do odpowiedniej tabeli w §3 lub §4
2. Zcommituj zmianę w tym pliku razem z nowym dokumentem
