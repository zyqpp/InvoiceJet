# 07. Mapowania i słowniki

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Idea mapowań

Mapowania krzyżowe są warstwą **nawigacyjną** dokumentacji. Każda mapa łączy dwa typy artefaktów i pozwala wyjść od dowolnego punktu i dotrzeć do elementów w innej warstwie. Mapy żyją w `doc_AI/_mapowania/`.

## B. Wymagane mapy

**M-01. Inwentaryzacje** (powstają w Fazie 1):

Pliki: `inwentaryzacja_ekranow.md`, `inwentaryzacja_api.md`, `inwentaryzacja_encji.md`, `inwentaryzacja_dto.md`, `inwentaryzacja_linq.md`, `inwentaryzacja_automappera.md`, `inwentaryzacja_rol.md`, `inwentaryzacja_procesow.md`, `inwentaryzacja_algorytmow.md`.

Każda inwentaryzacja to tabela: nazwa artefaktu (1:1 z kodu), lokalizacja w kodzie (link), link do dokumentu (uzupełniany), status (`brak` / `szkic` / `gotowy` / `zaakceptowany`).

**M-02. Mapa pól w bazie ↔ DTO ↔ ekrany** — `mapa_db_dto_ekrany.md`.

**M-03. Mapa API ↔ DTO ↔ LINQ ↔ DB** — `mapa_api_dto_linq_db.md`.

**M-04. Mapa UC ↔ procesy biznesowe** — `mapa_uc_bpmn.md`.

**M-05. Mapa warstwowa UC → DB** — `mapa_warstwowa.md`.

**M-06. Mapa pokrycia testowego** — `pokrycie_testow.md`.

**M-07. Mapa ról ↔ ekrany ↔ operacje** — `mapa_rol_ekranow_operacji.md`.

**M-08. Mapa uprawnień ↔ endpointy API** — `mapa_uprawnien_api.md`.

**M-09. Mapa integracji ↔ procesy** — `mapa_integracji_procesow.md`.

**M-10. Mapa przejść między ekranami** — `mapa_przejsc_ekranow.md`.

## C. Idea słowników

Słowniki żyją w `doc_AI/_slowniki/`. Każde pojęcie ma stabilny anchor (`#nazwa-pojecia`) pozwalający linkować z dowolnego miejsca.

## D. Wymagane słowniki

**S-01. Słownik pojęć biznesowych** — `slownik_biznesowy.md`. Pojęcia: firma (kontrahent), klient, dokument, faktura, faktura proforma, faktura storno, seria dokumentów, konto bankowe, produkt, CUI (rumuński NIP), ANAF.

**S-02. Słownik pojęć technicznych** — `slownik_techniczny.md`. Pojęcia: DTO, LINQ, endpoint, JWT, BCrypt, AutoMapper, UnitOfWork, ExceptionMiddleware, QuestPDF, EF Core.

**S-03. Słownik elementów dokumentacji** — `slownik_elementow_dokumentacji.md`. Precyzyjne definicje: ekran, sekcja ekranu, pole, operacja, filtr, tabela ekranu, modal, powiadomienie, proces techniczny, algorytm, UC.

**S-04. Słownik skrótów** — `slownik_skrotow.md`. Skróty: AOS, BPMN, DTO, ERD, UC, RACI, RAG, ORM, JWT, BCrypt, CUI.

**S-05. Słownik prefiksów identyfikatorów** — `slownik_prefiksow_id.md`. Zamknięta lista prefiksów ID.

## E. Reguły utrzymania

Mapy są aktualizowane na bieżąco. Kompletna walidacja w Fazie 11.

## F. Reguła „nie zgaduj pojęć"

Jeżeli agent napotyka pojęcie nieznane — nie wymyśla definicji. Używa adnotacji `Do_zdefiniowania` i wpisuje w „Wątpliwości i braki".

## G. Reguła „mapa lub link"

Każde powiązanie między dwoma artefaktami musi być zapisane w co najmniej jednym z dwóch miejsc: link w sekcji „Powiązania" dokumentu albo wpis w mapie krzyżowej.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
