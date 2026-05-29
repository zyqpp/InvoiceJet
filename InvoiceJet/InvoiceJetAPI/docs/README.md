# Dokumentacja AOS — Backend InvoiceJetAPI

**Status:** Roboczy
**Data utworzenia:** 2026-05-29
**Zakres:** Dokumentacja procesów backendowych API.

---

## Struktura dokumentacji

```text
docs/
├── BackendAgentAI/
│   ├── 01_ZASADY_BACKEND_AOS.md
│   ├── 02_SLOWNIK_BACKEND.md
│   ├── 03_MARKERY_I_WERYFIKACJA.md
│   └── AOS_BACKEND_PROCESS_TEMPLATE.md
└── aos/
    └── backend/
        ├── REJESTR_PROCESOW_BACKEND.md
        ├── templates/
        └── processes/
            ├── P-01_IssueNewInvoice/
            └── P-02_AddFirm/
```

---

## Zasada podziału dokumentacji

Jeden proces backendowy opisuje jeden spójny przepływ API: od endpointu w kontrolerze, przez serwis aplikacyjny, DTO, repozytoria i encje, do skutku zapisu lub odpowiedzi API.

Dokument procesu nie opisuje zachowania frontendu. Jeżeli proces jest wywoływany przez frontend, dokument wskazuje wyłącznie kontrakt API i dane wejściowe.

---

## Komplet plików procesu

Każdy proces w `docs/aos/backend/processes/P-XX_NazwaProcesu/` zawiera:

- `00_METADANE.md`
- `01_PRZEGLAD_PROCESU.md`
- `02_KONTRAKT_API.md`
- `03_LOGIKA_APLIKACYJNA.md`
- `04_DANE_MODELE_MAPOWANIA.md`
- `05_BLEDY_BEZPIECZENSTWO.md`
- `06_SCENARIUSZE_TESTOWE.md`
- `HISTORIA_ZMIAN.md`

---

## Źródła prawdy

- Kontrolery: `InvoiceJet.Presentation/Controllers`
- Konfiguracja API: `InvoiceJet.Presentation/Program.cs`
- Middleware błędów: `InvoiceJet.Presentation/Middleware/ExceptionMiddleware.cs`
- Serwisy aplikacyjne: `InvoiceJet.Application/Services/Impl`
- DTO: `InvoiceJet.Application/DTOs`
- Mapowania: `InvoiceJet.Application/MappingProfiles`
- Encje i wyjątki: `InvoiceJet.Domain`
- Repozytoria i EF Core: `InvoiceJet.Infrastructure/Persistence`
