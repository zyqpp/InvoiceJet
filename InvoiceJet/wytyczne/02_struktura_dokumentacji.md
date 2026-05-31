# 02. Struktura dokumentacji

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Korzeń projektu

```
/  (G:\Projekty informatyczne\Gotowe aplikacje\InvoiceJet\InvoiceJet\)
├── PLAN.md                          # plan działania (produkt Agenta-Orkiestratora)
├── wytyczne/                        # niniejszy zestaw wytycznych (TYLKO DO CZYTANIA)
├── archiwum/                        # stara dokumentacja - NIE CZYTAĆ
│   └── README.md                    # ostrzeżenie dla agentów
├── doc_AI/                          # nowa dokumentacja projektu (główny katalog)
├── InvoiceJetAPI/                   # backend ASP.NET Core 8
└── InvoiceJetUI/                    # frontend Angular 16
```

## B. Struktura katalogu `doc_AI/`

```
doc_AI/
├── README.md                        # strona startowa dokumentacji AOS
├── 00_meta/                         # informacje o samym projekcie i nawigacja
├── 01_ekrany/                       # ekrany aplikacji (Angular components)
├── 02_procesy/                      # procesy techniczne (back/front)
├── 03_algorytmy/                    # algorytmy walidacji, wyliczeń, dostępu itd.
├── 04_api_i_integracje/             # API frontu i integracje z systemami dziedzinowymi
├── 05_model_danych/                 # DTO, LINQ, schemat DB, automapper, skrypty
├── 06_role_i_uprawnienia/           # role, uprawnienia, grupy użytkowników
├── 07_use_case/                     # przypadki użycia (UML)
├── 08_model_biznesowy/              # biznesowy model obiektów (nie 1:1 z DB)
├── 09_procesy_biznesowe/            # diagramy BPMN 2.0
├── 10_testy/                        # scenariusze testowe (ręczne, automatyczne)
├── _mapowania/                      # mapy krzyżowe między elementami
├── _slowniki/                       # słowniki pojęć biznesowych i technicznych
└── _szablony/                       # zmaterializowane szablony do skopiowania
```

Każdy z tych katalogów ma własny `README.md` jako mapę z drzewem zawartości, listą plików/podkatalogów z jednolinijkowymi opisami i krótkim opisem biznesowym celu sekcji. Opisy biznesowe finalizujemy na końcu projektu; szkielet README z drzewem powstaje od razu.

## C. Sekcja `00_meta/`

Zawartość:

- `01_o_projekcie.md` — co to jest AOS, jakie ma cele, jacy są jego użytkownicy.
- `02_stos_technologiczny.md` — wersje języków, frameworków, baz, bibliotek istotnych.
- `03_architektura_aplikacji.md` — diagramy warstw, granice modułów, wzorce.
- `04_jak_poruszac_sie_po_aplikacji.md` — przewodnik nawigacyjny: Ekran → API → DTO → LINQ → DB.
- `05_drzewo_projektu.md` — pełne drzewo katalogów projektu z opisem ról głównych folderów kodu.
- `06_globalne_mechanizmy.md` — przekrojowe mechanizmy (JWT, ExceptionMiddleware, UoW, BCrypt, CORS, QuestPDF).

## D. Sekcja `01_ekrany/`

```
01_ekrany/
├── README.md
├── 00_wspolne/                      # szkielet frontu, navbar, sidebar, modale wspólne
│   ├── README.md
│   ├── navbar/
│   ├── sidebar/
│   └── modale_wspolne/
├── login/
├── register/
├── dashboard/
├── firma/
│   ├── dane_firmy/
│   ├── klienci/
│   └── konta_bankowe/
├── produkty/
├── serie_dokumentow/
├── faktury/
│   ├── lista_faktur/
│   └── dodaj_edytuj_fakture/
├── faktury_proforma/
│   ├── lista_faktur_proforma/
│   └── dodaj_edytuj_fakture_proforma/
├── faktury_storno/
│   ├── lista_faktur_storno/
│   └── dodaj_edytuj_fakture_storno/
└── mapa_przejsc.md
```

## E. Sekcja `02_procesy/`

Procesy techniczne — backend + frontend. Podział na główne i pomocnicze.

```
02_procesy/
├── README.md
├── autentykacja/
├── firma/
├── produkty/
├── konta_bankowe/
├── serie_dokumentow/
└── dokumenty/
```

## F. Sekcja `03_algorytmy/`

```
03_algorytmy/
├── README.md
├── walidacji/
├── autoryzacyjne/
├── generowania_pdf/
├── wyliczeniowe/
└── dedykowane/
```

## G. Sekcja `04_api_i_integracje/`

```
04_api_i_integracje/
├── README.md
├── 01_api_frontend/
│   ├── README.md
│   ├── lista_api.md
│   ├── auth/
│   ├── firm/
│   ├── product/
│   ├── bank_account/
│   ├── document_series/
│   └── document/
└── 02_systemy_dziedzinowe/
    ├── README.md
    └── anaf/
```

## H. Sekcja `05_model_danych/`

```
05_model_danych/
├── README.md
├── 01_db/
│   ├── README.md
│   ├── spis_schem_i_tabel.md
│   ├── erd_globalny.md
│   └── dbo/
│       ├── dbo.User.md
│       ├── dbo.Firm.md
│       ├── dbo.BankAccount.md
│       ├── dbo.UserFirm.md
│       ├── dbo.Product.md
│       ├── dbo.DocumentType.md
│       ├── dbo.DocumentSeries.md
│       ├── dbo.Document.md
│       ├── dbo.DocumentProduct.md
│       ├── dbo.DocumentStatus.md
│       └── erd_dbo.md
├── 02_dto/
│   ├── README.md
│   ├── spis_dto.md
│   └── (per DTO)
├── 03_linq/
├── 04_zapytania_bezposrednie/
├── 05_automapper/
└── 06_skrypty/
```

## I. Sekcja `06_role_i_uprawnienia/`

```
06_role_i_uprawnienia/
├── README.md
├── lista_rol.md
├── lista_uprawnien.md
├── macierz_role_uprawnienia.md
└── User.md
```

## J–O. Pozostałe sekcje

Sekcje `07_use_case/`, `08_model_biznesowy/`, `09_procesy_biznesowe/`, `10_testy/`, `_mapowania/`, `_slowniki/`, `_szablony/` mają strukturę zgodną z oryginalnym `02_struktura_dokumentacji.md` z katalogu `wytyczne/`.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — zaadaptowana do projektu InvoiceJet (doc_AI zamiast docs/). |
