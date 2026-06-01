# BP-FIRM-02 Zarządzanie klientami (kontrahentami)

| Pole | Wartość |
|---|---|
| ID dokumentu | BP-FIRM-02 |
| Obszar | Firma |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-01 |

## Cel biznesowy

Umożliwić użytkownikowi budowanie i utrzymywanie bazy kontrahentów (klientów), których dane będą dostępne do wyboru przy wystawianiu dokumentów handlowych.

## Kontekst

Użytkownik zarządza klientami na ekranie „Klienci" (`/dashboard/clients`). Każdy klient to firma zapisana w bazie z flagą „klient" — dzięki czemu pojawia się na liście wyboru w formularzu faktury. System umożliwia autouzupełnienie danych klienta z rejestru ANAF na podstawie numeru CUI.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Dodaje, edytuje i zarządza listą klientów |
| Aplikacja (Frontend) | Wyświetla listę klientów, obsługuje dialog dodawania/edycji |
| Serwer (API) | Zapisuje dane klienta, powiązuje z kontem użytkownika |
| Baza danych | Trwale przechowuje dane klientów |
| ANAF API (opcjonalnie) | Dostarcza dane rejestrowe klienta na podstawie numeru CUI |

## Warunki wejścia

- Użytkownik zalogowany
- Ekran klientów otwarty

## Przebieg główny — Dodanie klienta

1. **Użytkownik** otwiera ekran „Klienci" i klika „Dodaj klienta"
2. **Aplikacja** wyświetla dialog z formularzem danych klienta
3. **Użytkownik** opcjonalnie wpisuje numer CUI klienta i klika ikonę autouzupełnienia
4. **Aplikacja** pobiera dane klienta z rejestru ANAF i wypełnia pola formularza
5. **Użytkownik** weryfikuje, uzupełnia lub poprawia dane i klika „Zapisz"
6. **Serwer** zapisuje dane klienta i powiązuje go z kontem użytkownika jako kontrahent
7. **System** zamyka dialog; klient pojawia się na liście klientów i w selektorach formularzy dokumentów

## Przebieg główny — Edycja danych klienta

1. **Użytkownik** otwiera ekran „Klienci", klika przycisk edycji przy wybranym kliencie
2. **Aplikacja** wyświetla dialog z wypełnionym formularzem danych klienta
3. **Użytkownik** modyfikuje wybrane pola i klika „Zapisz"
4. **Serwer** aktualizuje dane klienta w bazie
5. **System** zamyka dialog; zaktualizowane dane klienta widoczne na liście i w dokumentach

## Przebieg główny — Usunięcie klienta

1. **Użytkownik** klika ikonę usunięcia przy wybranym kliencie
2. **Aplikacja** wyświetla pytanie o potwierdzenie
3. **Użytkownik** potwierdza
4. **Serwer** usuwa powiązanie klienta z kontem użytkownika
5. **System** odświeża listę klientów

## Reguły biznesowe

| ID | Reguła | Objaśnienie |
|---|---|---|
| RB-01 | Klient powiązany jest wyłącznie z kontem użytkownika | Lista klientów widoczna tylko dla właściciela konta |
| RB-02 | Klient pojawia się w selektorach formularza faktury | Po dodaniu klienta jest dostępny do wyboru przy wystawianiu dokumentów |
| RB-03 | CUI służy do autouzupełnienia z ANAF | Wpisanie CUI i kliknięcie ikony chmury pobiera dane z rejestru |
| RB-04 | Dane z ANAF można modyfikować przed zapisem | Pobranie z ANAF to tylko sugestia |
| RB-05 | Klient i własna firma używają tego samego mechanizmu zapisu | Różnicą jest flaga `isClient` przy zapisie |

## Wyjątki i scenariusze alternatywne

| ID | Scenariusz | Warunek | Reakcja systemu |
|---|---|---|---|
| WYJ-01 | ANAF niedostępny | Serwis ANAF nie odpowiada | Komunikat o niedostępności; użytkownik wpisuje dane ręcznie |
| WYJ-02 | CUI nieznany w ANAF | Numer CUI nie figuruje w rejestrze | Komunikat „Firma nie znaleziona"; użytkownik wpisuje dane ręcznie |
| WYJ-03 | Anulowanie dodawania | Użytkownik zamknął dialog bez zapisu | Dialog zamknięty; klient nie dodany |
| WYJ-04 | Błąd zapisu | Tymczasowy błąd bazy danych | Ogólny komunikat błędu; możliwość ponowienia próby |

## Wynik procesu

Po dodaniu klienta:
- Dane klienta zapisane i powiązane z kontem użytkownika
- Klient dostępny do wyboru w formularzu wystawiania faktury / proformy / storno

Po edycji:
- Zaktualizowane dane klienta widoczne na liście i przy kolejnym wystawieniu dokumentu

Po usunięciu:
- Klient niewidoczny na liście i niewidoczny w selektorach formularzy

## Diagram sekwencji

```mermaid
sequenceDiagram
    autonumber
    participant U as Użytkownik
    participant FE as Aplikacja (Frontend)
    participant API as Serwer (API)
    participant DB as Baza danych
    participant ANAF as ANAF API

    U->>FE: Otwiera ekran Klienci
    FE->>API: Pobierz listę klientów użytkownika
    API->>DB: Zapytanie o klientów powiązanych z firmą użytkownika
    DB-->>API: Lista klientów
    API-->>FE: Lista klientów
    FE-->>U: Wyświetla listę klientów z przyciskami akcji

    U->>FE: Klik Dodaj klienta
    FE-->>U: Dialog z formularzem klienta

    opt Autouzupełnienie z ANAF
        U->>FE: Wpisuje CUI klienta i klika ikonę autouzupełnienia
        FE->>API: Pobierz dane firmy po numerze CUI
        API->>ANAF: Zapytanie do rejestru firm
        ANAF-->>API: Dane rejestrowe firmy
        API-->>FE: Dane klienta
        FE-->>U: Autouzupełnione pola formularza
    end

    U->>FE: Weryfikuje i uzupełnia dane klienta, klika Zapisz
    FE->>API: Wyślij dane nowego klienta (jako kontrahent)
    API->>DB: Zapisz dane klienta
    DB-->>API: Klient zapisany z identyfikatorem
    API->>DB: Utwórz powiązanie klienta z kontem użytkownika (flaga: klient)
    DB-->>API: Powiązanie zapisane
    API-->>FE: Klient dodany
    FE-->>U: Dialog zamknięty; klient na liście i w selektorach dokumentów
```

## Powiązania analityczne

| Typ | Dokument |
|---|---|
| Use Case | [UC-03 Zarządzanie klientami](../../07_use_case/UC-03_ZarzadzanieKlientami.md) |
| Use Case | [uc_firma](../../07_use_case/firma/uc_firma.md) |
| Proces powiązany | [BP-FIRM-01 Dane firmy](./BP-FIRM-01_dane_firmy.md) |
| Proces powiązany | [BP-DOC-01 Wystawienie faktury](../dokumenty/BP-DOC-01_wystawienie_faktury.md) |

## Powiązania techniczne

| Typ | Dokument |
|---|---|
| Proces techniczny | [dodaj_firme/proces.md](../../02_procesy/firma/dodaj_firme/proces.md) |
| Proces techniczny | [edytuj_firme/proces.md](../../02_procesy/firma/edytuj_firme/proces.md) |
| Proces techniczny | [pobierz_z_anaf/proces.md](../../02_procesy/firma/pobierz_z_anaf/proces.md) |
| API | [POST /api/Firm/AddFirm](../../04_api_i_integracje/01_api_frontend/firm/POST_Firm_AddFirm.md) |
| API | [PUT /api/Firm/EditFirm](../../04_api_i_integracje/01_api_frontend/firm/PUT_Firm_EditFirm.md) |
| API | [GET /api/Firm/fromAnaf](../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_fromAnaf.md) |
| Model DB | [dbo.Firm](../../05_model_danych/01_db/dbo/dbo.Firm.md) |
| Model DB | [dbo.UserFirm](../../05_model_danych/01_db/dbo/dbo.UserFirm.md) |

## Wątpliwości i braki

- Brak walidacji unikalności CUI klientów — można dodać tego samego klienta wielokrotnie
- Brak możliwości scalenia duplikatów klientów
- Usunięcie klienta: brak informacji o tym co dzieje się z wystawionymi fakturami dla tego klienta (klucz obcy w DB)
- Edycja klienta: zaktualizowane dane mogą nie odzwierciedlać danych na już wystawionych dokumentach (dokumenty przechowują snapshot danych)

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-06-01 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja BP — na podstawie BPMN-FIRMA-01 i PROC-AddFirm (isClient=true); format analityczny BP-NN |
