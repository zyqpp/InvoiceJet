# Dokumentacja AOS — Backend InvoiceJetAPI

**Status:** ✅ Etap backend ukończony — 19 procesów, 152 pliki, 31 endpointów.
**Data aktualizacji:** 2026-05-30
**Branch z dokumentacją:** [`docs/aos-backend-p11-p19`](https://github.com/zyqpp/InvoiceJet/tree/docs/aos-backend-p11-p19)

---

## Zakres ukończony

| Obszar | Procesy | Endpointy |
|---|---|---|
| Autentykacja | P-01 RegisterUser, P-02 LoginUser | API-01, API-02 |
| Zarządzanie firmami | P-03 AddFirm, P-04 GetFirmFromAnaf, P-05 EditFirm, P-06 GetUserActiveFirm, P-07 GetUserClientFirms, P-08 ManageClientFirms | API-03 – API-09 |
| Produkty | P-09 ManageProducts | API-10 – API-13 |
| Konta bankowe | P-10 ManageBankAccounts | API-14 – API-17 |
| Serie dokumentów | P-11 ManageDocumentSeries | API-18 – API-21 |
| Dokumenty | P-12 AddDocument, P-13 EditDocument, P-14 GetDocuments, P-15 DeleteDocuments, P-16 GetDocumentAutofillInfo, P-17 ManageDocumentPdf, P-18 GetDashboardStats, P-19 TransformToStorno | API-22 – API-31 |

---

## Struktura dokumentacji

```text
docs/
├── BackendAgentAI/                    # Kontrakt wyjścia dla agenta (zasady i instrukcje)
│   ├── 01_ZASADY_BACKEND_AOS.md
│   ├── 02_SLOWNIK_BACKEND.md
│   ├── 03_MARKERY_I_WERYFIKACJA.md   # Definicja Ukończenia per plik
│   ├── 04_REGULY_DEKOMPOZYCJI.md     # Jednoznaczna reguła "proces vs endpoint"
│   ├── 05_KATALOGI_PRZEKROJOWE.md    # Spec katalogów przekrojowych
│   └── AOS_BACKEND_PROCESS_TEMPLATE.md
└── aos/
    └── backend/
        ├── KATALOG_API.md             # ✅ Spis 31 endpointów (API-01 – API-31)
        ├── KATALOG_WYJATKOW.md        # ✅ Rejestr wyjątków → kody HTTP
        ├── KATALOG_DANYCH_TESTOWYCH.md # ✅ Fixture'y DT-01 – DT-08
        ├── ZAGADNIENIA_PRZEKROJOWE.md # ✅ JWT, middleware, UoW, AutoMapper, CORS, QuestPDF
        ├── MAPA_PLIKOW_PROJEKTU.md    # ✅ Mapa plików projektu
        ├── templates/                 # Szablony 8 plików procesu
        ├── processes/                 # ✅ 19 procesów (P-01 – P-19), każdy 8 plików
        │   ├── Authentication/        #   P-01, P-02
        │   ├── FirmManagement/        #   P-03 – P-08
        │   ├── ProductManagement/     #   P-09
        │   ├── BankAccountManagement/ #   P-10
        │   ├── DocumentSeriesManagement/ # P-11
        │   └── DocumentManagement/   #   P-12 – P-19
        └── _archive/                  # Poprzednia wersja (nie jest źródłem prawdy)
```

---

## Kontrakt dokumentu procesu

Każdy proces w `docs/aos/backend/processes/<Obszar>/P-XX_NazwaProcesu/` zawiera 8 plików:

- `00_METADANE.md` — wizytówka: endpointy, DTO, encje, kotwice
- `01_PRZEGLAD_PROCESU.md` — cel biznesowy, diagram mermaid, reguły
- `02_KONTRAKT_API.md` — kontrakt HTTP z realnymi przykładami JSON
- `03_LOGIKA_APLIKACYJNA.md` — algorytm krok po kroku z kotwicami i cytatami kodu
- `04_DANE_MODELE_MAPOWANIA.md` — kolumny SQL, DTO, AutoMapper, LINQ
- `05_BLEDY_BEZPIECZENSTWO.md` — katalog WAL-XX, mapowanie wyjątków, autoryzacja
- `06_SCENARIUSZE_TESTOWE.md` — dane testowe: happy path + negative + brzegowe
- `HISTORIA_ZMIAN.md`

Definicja Ukończenia każdego pliku: `BackendAgentAI/03_MARKERY_I_WERYFIKACJA.md` (sekcja 3).

---

## Katalogi przekrojowe (poziom `docs/aos/backend/`)

| Plik | Status | Opis |
|---|---|---|
| `KATALOG_API.md` | ✅ gotowy | Wszystkie 31 endpointów z metodą HTTP, ścieżką, kontrolerem, procesem |
| `KATALOG_WYJATKOW.md` | ✅ gotowy | 9 zmapowanych wyjątków + 3 niemapowane (→500) + 2 do weryfikacji |
| `KATALOG_DANYCH_TESTOWYCH.md` | ✅ gotowy | Fixture'y DT-01 – DT-08 (globalne dane do testów) |
| `ZAGADNIENIA_PRZEKROJOWE.md` | ✅ gotowy | JWT, ExceptionMiddleware, UoW, AutoMapper, CORS, ANAF, QuestPDF |
| `MAPA_PLIKOW_PROJEKTU.md` | ✅ gotowy | Mapa plików projektu per kontroler/serwis |
| `SLOWNIK_DANYCH.md` | ⏳ planowany | Tabele, kolumny, enumy, lookupy, seed (etap przyszły) |
| `MODEL_DOMENY.md` | ⏳ planowany | Diagram ER + konfiguracje EF Core (etap przyszły) |
| `MAPA_FULLSTACK.md` | 🚫 poza zakresem | Most do AOS frontendu — etap fullstack |

---

## Źródła prawdy w kodzie

- Kontrolery: `InvoiceJet.Presentation/Controllers`
- Konfiguracja API: `InvoiceJet.Presentation/Program.cs`
- Middleware błędów: `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs`
- Seeder: `InvoiceJet.Presentation/Seeders/DbSeeder.cs`
- Serwisy aplikacyjne: `InvoiceJet.Application/Services/Impl`
- DTO: `InvoiceJet.Application/DTOs`
- Mapowania: `InvoiceJet.Application/MappingProfiles`
- Encje, enumy, wyjątki: `InvoiceJet.Domain`
- Repozytoria, EF Core, snapshot migracji: `InvoiceJet.Infrastructure/Persistence` + `InvoiceJet.Infrastructure/Migrations`

---

## Archiwum

`docs/aos/backend/_archive/` zawiera poprzednią dokumentację (19 procesów na starych szablonach). **Nie jest źródłem prawdy** — szczegóły w `_archive/README.md`.
