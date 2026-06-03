# Dokumentacja AOS — InvoiceJet

| Pole | Wartość |
|---|---|
| Wersja dokumentacji | 0.1 (szkic) |
| Status | W budowie |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Czym jest InvoiceJet

InvoiceJet (wewnętrzna nazwa `Facturila`) to aplikacja webowa do wystawiania faktur dla małych firm. Umożliwia rejestrację firmy, zarządzanie klientami (firmami klientów), produktami, kontami bankowymi i seriami dokumentów, wystawianie trzech typów dokumentów (faktura, faktura proforma, faktura storno) oraz eksport do PDF. Integruje się z rumuńskim rejestrem firm ANAF w celu wyszukiwania danych kontrahentów po numerze CUI.

## Stos technologiczny

| Warstwa | Technologia |
|---|---|
| Backend | ASP.NET Core 8, EF Core 8, SQL Server |
| Frontend | Angular 16, Angular Material |
| Autentykacja | JWT (BCrypt, HmacSha512) |
| PDF | QuestPDF Community |
| Integracja zewnętrzna | ANAF API (rumuński rejestr firm) |

## Mapa katalogu `doc_AI/`

```
doc_AI/
├── README.md                    ← ten plik
├── 00_meta/                     ← stos tech, architektura, drzewo projektu
├── 01_ekrany/                   ← ekrany Angular (komponenty UI)
├── 02_procesy/                  ← procesy techniczne backend + frontend
├── 03_algorytmy/                ← algorytmy walidacji, PDF, autoryzacji
├── 04_api_i_integracje/         ← endpointy API (31) + ANAF
├── 05_model_danych/             ← DB, DTO, LINQ, AutoMapper
├── 06_role_i_uprawnienia/       ← role, uprawnienia, macierz
├── 07_use_case/                 ← diagramy UC
├── 08_model_biznesowy/          ← model klas biznesowych
├── 09_procesy_biznesowe/        ← diagramy BPMN (lub Mermaid)
├── 10_testy/                    ← scenariusze testowe
├── _mapowania/                  ← mapy krzyżowe i inwentaryzacje
├── _slowniki/                   ← słowniki pojęć
└── _szablony/                   ← gotowe szablony do skopiowania
```

## Od czego zacząć

**Nowy programista (backend):** zacznij od [`05_model_danych/01_db/erd_globalny.md`](05_model_danych/01_db/erd_globalny.md) → [`04_api_i_integracje/01_api_frontend/lista_api.md`](04_api_i_integracje/01_api_frontend/lista_api.md) → `00_meta/06_globalne_mechanizmy.md`.

**Nowy programista (frontend):** zacznij od [`01_ekrany/mapa_przejsc.md`](01_ekrany/mapa_przejsc.md) → poszczególne ekrany → `04_api_i_integracje/01_api_frontend/lista_api.md`.

**Analityk:** zacznij od `00_meta/01_o_projekcie.md` → `07_use_case/` → `09_procesy_biznesowe/`.

**Agent AI / RAG:** zacznij od `_mapowania/mapa_warstwowa.md` (mapa UC → DB).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet strony startowej. |
