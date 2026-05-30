# Dokumentacja AOS — Backend InvoiceJetAPI

**Status:** Framework gotowy. Re-dokumentacja procesów w toku.
**Data aktualizacji:** 2026-05-29

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
        ├── templates/                # Szablony do skopiowania (8 dla procesu + 7 katalogów)
        ├── processes/                # (pusty) — nowe procesy P-XX powstają tutaj
        └── _archive/                 # Stara dokumentacja (poprzednia wersja frameworka)
```

---

## Kontrakt dokumentu procesu

Każdy proces w `docs/aos/backend/processes/P-XX_NazwaProcesu/` zawiera 8 plików (szablony w `docs/aos/backend/templates/`):

- `00_METADANE.md`, `01_PRZEGLAD_PROCESU.md`, `02_KONTRAKT_API.md`,
- `03_LOGIKA_APLIKACYJNA.md` (kręgosłup — algorytm),
- `04_DANE_MODELE_MAPOWANIA.md` (do poziomu kolumn),
- `05_BLEDY_BEZPIECZENSTWO.md` (katalog walidacji + błędy + bezpieczeństwo),
- `06_SCENARIUSZE_TESTOWE.md` (realne dane testowe),
- `HISTORIA_ZMIAN.md`.

Definicja Ukończenia każdego pliku: `BackendAgentAI/03_MARKERY_I_WERYFIKACJA.md` (sekcja 3).

---

## Katalogi przekrojowe (poziom `docs/aos/backend/`)

Tworzone i aktualizowane przy re-dokumentacji (szablony w `templates/`):

- `KATALOG_API.md` — wszystkie endpointy 1:1
- `SLOWNIK_DANYCH.md` — tabele, kolumny, enumy, lookupy, seed
- `KATALOG_WYJATKOW.md` — wyjątek → status HTTP (w tym niemapowane → 500)
- `MODEL_DOMENY.md` — diagram ER + jawne konfiguracje EF Core
- `ZAGADNIENIA_PRZEKROJOWE.md` — JWT, middleware, UoW, AutoMapper, CORS, ANAF, QuestPDF
- `KATALOG_DANYCH_TESTOWYCH.md` — globalne fixture'y `DT-XX`
- `MAPA_FULLSTACK.md` — most do AOS frontendu (odłożone)

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

`docs/aos/backend/_archive/` zawiera poprzednią dokumentację (19 procesów wytworzonych na starych, chudych szablonach + stary rejestr). **Nie jest źródłem prawdy** — szczegóły w `_archive/README.md`.
