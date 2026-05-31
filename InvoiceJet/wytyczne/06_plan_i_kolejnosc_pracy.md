# 06. Plan i kolejność pracy

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Zasada porządkowa

Dokumentacja powstaje **od warstw najniższych do najwyższych** oraz **od inwentaryzacji do opisu**.

Kolejność:
1. Katalogujemy artefakty z kodu (bez opisów) → listy inwentaryzacyjne
2. Opisujemy warstwę danych (DB → DTO → LINQ → AutoMapper)
3. Opisujemy API (kontrakty HTTP)
4. Opisujemy role i uprawnienia
5. Opisujemy ekrany (Angular components)
6. Opisujemy procesy techniczne i algorytmy
7. Tworzymy model biznesowy
8. Tworzymy UC i BPMN
9. Tworzymy testy
10. Finalizujemy słowniki, mapowania, README

## B. Fazy

### Faza 0 — Archiwizacja

**Cel:** odcięcie się od starej dokumentacji.
**Wykonawca:** Agent-Archiwista.
**Działania:**
1. Utworzenie `archiwum/` w roocie projektu.
2. Przeniesienie starej dokumentacji z `InvoiceJetAPI/docs/` do `archiwum/`.
3. Utworzenie `archiwum/README.md` z ostrzeżeniem.
4. Raport archiwizacji.

**DoD:** stara dokumentacja przeniesiona, nowa (`doc_AI/`) jeszcze pusta.

### Faza 1 — Rozpoznanie projektu

**Cel:** ustalenie stosu technologicznego i inwentaryzacja artefaktów.
**Wykonawca:** Agent-Eksplorator.
**Produkty:**
- `doc_AI/00_meta/02_stos_technologiczny.md`
- `doc_AI/00_meta/05_drzewo_projektu.md`
- `doc_AI/_mapowania/inwentaryzacja_ekranow.md`
- `doc_AI/_mapowania/inwentaryzacja_api.md`
- `doc_AI/_mapowania/inwentaryzacja_encji.md`
- `doc_AI/_mapowania/inwentaryzacja_dto.md`
- `doc_AI/_mapowania/inwentaryzacja_rol.md`

**DoD:** każdy typ artefaktu ma swoją listę inwentaryzacyjną.

### Faza 2 — Szkielet katalogów i szablony

**Cel:** stworzenie struktury `doc_AI/` i materializacja szablonów.
**Wykonawca:** Agent-Szablonowy.
**DoD:** każdy katalog z `02_struktura_dokumentacji.md` istnieje i ma `README.md`.

### Faza 3 — Model danych

**Cel:** kompletny opis warstwy danych.
**Podfazy:** 3a DB, 3b DTO, 3c LINQ, 3d AutoMapper, 3e Skrypty/Seeder.
**DoD:** każda encja, DTO, profil AutoMapper ma dokument.

### Faza 4 — API i integracje

**Cel:** opis endpointów API (ASP.NET Core) i integracji (ANAF).
**Podfazy:** 4a endpointy frontu (31 endpointów), 4b ANAF.
**DoD:** każdy endpoint ma dokument z żądaniem, odpowiedzią, danymi testowymi.

### Faza 5 — Role i uprawnienia

**Cel:** opis ról (`User`), uprawnień (JWT), macierzy.
**DoD:** `lista_rol.md`, `macierz_role_uprawnienia.md`, plik roli `User.md`.

### Faza 6 — Ekrany

**Cel:** opis ekranów Angular.
**Podfazy:** 6a Wspólne (navbar, sidebar), 6b Mapa przejść, 6c Ekrany właściwe.
**Wejścia:** gotowe API (faza 4), model danych (faza 3), role (faza 5).
**DoD:** każdy ekran z inwentaryzacji ma katalog z `ekran.md`.

### Faza 7 — Procesy i algorytmy

**Cel:** opis procesów technicznych i algorytmów backend + frontend.
**DoD:** każdy zidentyfikowany proces i algorytm ma dokument.

### Faza 8 — Model biznesowy

**Cel:** model klas biznesowych i aktorów.
**Wejścia:** model danych, DTO, role.

### Faza 9 — UC i BPMN

**Cel:** przypadki użycia dla każdej grupy menu, BPMN dla głównych procesów.
**Wykonawcy:** Agent-UC (najpierw), Agent-Modelarz-BPMN (potem).

### Faza 10 — Testy

**Cel:** scenariusze testowe i mapy pokrycia.

### Faza 11 — Słowniki, mapowania, README katalogów

**Cel:** finalizacja warstwy nawigacyjnej.
**Wejścia:** wszystkie wcześniejsze fazy zakończone.

### Faza 12 — Walidacja

**Cel:** weryfikacja spójności dokumentacji.
**DoD:** raport walidacyjny z zerową liczbą krytycznych niezgodności.

### Faza 13 — Akceptacja

**Cel:** formalna akceptacja przez właściciela projektu.
**DoD:** każdy dokument ma status `zaakceptowany`, wersja `1.0`.

## C. Punkty kontrolne (bezwzględne)

1. Po fazie 0 — czy archiwizacja kompletna?
2. Po fazie 1 — czy inwentaryzacja poprawna?
3. Po fazie 2 — czy szkielet zaakceptowany?
4. Po fazie 6 — czy ekrany wystarczająco precyzyjne?
5. Po fazie 12 — przed akceptacją finalną.

## D. Reguły równoległości

- Fazy 3 i 5 mogą biec równolegle po fazie 2.
- Fazy 7a (procesy) i 7b (algorytmy) mogą biec równolegle po fazie 4.
- Faza 6 blokuje fazę 9.
- Faza 10 wymaga zakończenia fazy 9.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
