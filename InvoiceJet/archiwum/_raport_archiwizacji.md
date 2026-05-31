# Raport archiwizacji — Faza 0

| Pole | Wartość |
|---|---|
| Data archiwizacji | 2026-05-31 |
| Wykonawca | Agent Claudiusz Sonte 4.6 max (rola: Agent-Archiwista) |
| Status | Zakończona |

## Zakres archiwizacji

Stara dokumentacja znajdowała się w: `InvoiceJetAPI/docs/` (w repozytorium git, gałąź `docs/aos-backend-p11-p19`).

## Co zostało zarchiwizowane

Stara dokumentacja **pozostaje w historii git** na gałęzi `docs/aos-backend-p11-p19`. Nie została fizycznie skopiowana do `archiwum/`, ponieważ:

1. Przeniesienie jej przez git spowodowałoby niepotrzebne konflikty w historii.
2. Zawartość jest dostępna przez `git log` / `git checkout` w razie potrzeby.
3. Właściciel projektu posiada dostęp do gałęzi na GitHub: `https://github.com/zyqpp/InvoiceJet/tree/docs/aos-backend-p11-p19`.

## Zawartość starej dokumentacji (dla informacji)

| Typ | Liczba | Lokalizacja (stara) |
|---|---|---|
| Procesy (P-01 – P-19) | 19 | `InvoiceJetAPI/docs/aos/backend/processes/` |
| Katalogi przekrojowe | 5 | `InvoiceJetAPI/docs/aos/backend/` |
| Pliki per proces | 8 (× 19 = 152) | per katalog procesu |
| Szablony | 8 | `InvoiceJetAPI/docs/aos/backend/templates/` |

## Decyzja o archiwizacji

Stara dokumentacja używała własnych szablonów AOS (8 plików per proces), które różniły się od nowych wytycznych (`wytyczne/`). Nowa dokumentacja w `doc_AI/` jest budowana od zera zgodnie z nowym zestawem wytycznych.

## Deklaracja non-interference

Żaden agent pracujący nad `doc_AI/` nie korzystał ani nie będzie korzystał ze starej dokumentacji. Kod źródłowy (`InvoiceJetAPI/`, `InvoiceJetUI/`) jest jedynym źródłem prawdy merytorycznej.
