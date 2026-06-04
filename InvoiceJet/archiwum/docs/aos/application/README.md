# Dokumentacja AOS aplikacji InvoiceJet

**Status:** Roboczy
**Zakres:** dokumentacja end-to-end łącząca frontend, backend i bazę danych.

## Jak czytac dokumentacje

Dokumentacja aplikacyjna jest trzecim poziomem AOS. Warstwa frontendu opisuje ekrany. Warstwa backendu opisuje procesy API. Warstwa aplikacyjna łączy te informacje w przepływy widoczne dla użytkownika.

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

| Rola | Ścieżka czytania |
|---|---|
| Analityk | `MAPA_NAWIGACJI_I_MAKIET.md`, rejestr przepływów, przeglad `A-XX`. |
| Developer | mapy pól, operacje, śledzenie źródeł. |
| Tester | scenariusze E2E, walidacje, błędy i skutki w bazie. |
| PM/PO | mapa nawigacji, status przepływów, historia zmian. |

## Reprezentacyjny przyklad weryfikacyjny

Dokument [PRZYKLAD_WERYFIKACYJNY_A-05_IssueNewInvoice.md](PRZYKLAD_WERYFIKACYJNY_A-05_IssueNewInvoice.md) pokazuje jeden kompletny ślad od pola UI i akcji przycisku do endpointu API i skutku w bazie.
To jest punkt kontrolny jak czytac i weryfikowac jakość dokumentacji aplikacyjnej bez uruchamiania kodu.
W przykladzie celowo użyto tylko istniejacych dokumentów frontendu, backendu i warstwy aplikacyjnej.

## Źródła

- AOS frontendu: `InvoiceJet/InvoiceJetUI/docs`
- AOS backendu: `InvoiceJet/InvoiceJetAPI/docs`
- Dokumenty technologiczne: `docs/stos-technologiczny.md`, `docs/struktura-katalogow-frontend.md`
