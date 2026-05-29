# Dokumentacja AOS aplikacji InvoiceJet

**Status:** Roboczy
**Zakres:** dokumentacja end-to-end laczaca frontend, backend i baze danych.

## Jak czytac dokumentacje

Dokumentacja aplikacyjna jest trzecim poziomem AOS. Warstwa frontendu opisuje ekrany. Warstwa backendu opisuje procesy API. Warstwa aplikacyjna laczy te informacje w przeplywy widoczne dla uzytkownika.

## Struktura

```text
docs/aos/application/
├── README.md
├── REJESTR_PRZEPLYWOW_APLIKACJI.md
├── MAPA_NAWIGACJI_I_MAKIET.md
├── navigation/
├── templates/
└── flows/
```

## Role

| Rola | Sciezka czytania |
|---|---|
| Analityk | `MAPA_NAWIGACJI_I_MAKIET.md`, rejestr przeplywow, przeglad `A-XX`. |
| Developer | mapy pol, operacje, sledzenie zrodel. |
| Tester | scenariusze E2E, walidacje, bledy i skutki w bazie. |
| PM/PO | mapa nawigacji, status przeplywow, historia zmian. |

## Reprezentacyjny przyklad weryfikacyjny

Dokument [PRZYKLAD_WERYFIKACYJNY_A-05_IssueNewInvoice.md](PRZYKLAD_WERYFIKACYJNY_A-05_IssueNewInvoice.md) pokazuje jeden kompletny slad od pola UI i akcji przycisku do endpointu API i skutku w bazie.
To jest punkt kontrolny jak czytac i weryfikowac jakosc dokumentacji aplikacyjnej bez uruchamiania kodu.
W przykladzie celowo uzyto tylko istniejacych dokumentow frontendu, backendu i warstwy aplikacyjnej.

## Zrodla

- AOS frontendu: `InvoiceJet/InvoiceJetUI/docs`
- AOS backendu: `InvoiceJet/InvoiceJetAPI/docs`
- Dokumenty technologiczne: `docs/stos-technologiczny.md`, `docs/struktura-katalogow-frontend.md`
