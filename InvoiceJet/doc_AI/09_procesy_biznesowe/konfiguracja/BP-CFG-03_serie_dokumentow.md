# BP-CFG-03 Konfiguracja serii numeracji dokumentów

| Pole | Wartość |
|---|---|
| ID dokumentu | BP-CFG-03 |
| Obszar | Konfiguracja |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-01 |

## Cel biznesowy

Umożliwić użytkownikowi zarządzanie seriami numeracji dokumentów — definiowanie prefiksów i sekwencji liczników dla faktur, proform i storno, zgodnie z wymaganiami ewidencyjnymi firmy.

## Kontekst

Użytkownik zarządza seriami numeracji na ekranie „Serie dokumentów" (`/dashboard/document-series`). Seria numeracji to prefiks (np. „FV", „PROF") + automatycznie inkrementowany licznik. System tworzy domyślne serie automatycznie przy pierwszym dodaniu firmy. Użytkownik może tworzyć dodatkowe serie lub modyfikować istniejące. Każdy typ dokumentu (faktura, proforma, storno) korzysta z osobnej serii.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Zarządza listą serii numeracji |
| Aplikacja (Frontend) | Wyświetla listę serii, obsługuje dialogi dodawania i edycji |
| Serwer (API) | Zapisuje, aktualizuje lub usuwa serie; przypisuje do firmy użytkownika |
| Baza danych | Trwale przechowuje serie i bieżące wartości liczników |

## Warunki wejścia

- Użytkownik zalogowany
- Dane własnej firmy wypełnione

## Przebieg główny — Dodanie serii numeracji

1. **Użytkownik** otwiera ekran „Serie dokumentów"
2. **Aplikacja** pobiera i wyświetla listę istniejących serii z ich prefiksami i bieżącymi licznikami
3. **Użytkownik** klika „Dodaj serię"
4. **Aplikacja** wyświetla dialog z formularzem: prefiks serii, typ dokumentu (faktura / proforma / storno), numer startowy
5. **Użytkownik** wypełnia formularz i klika „Zapisz"
6. **Serwer** przypisuje serię do firmy użytkownika z licznikiem ustawionym na wartość startową (domyślnie 1)
7. **System** zamyka dialog; nowa seria widoczna na liście i w selektorach formularzy dokumentów

## Przebieg główny — Edycja serii numeracji

1. **Użytkownik** klika przycisk edycji przy wybranej serii
2. **Aplikacja** wyświetla dialog z aktualnym prefiksem i bieżącą wartością licznika
3. **Użytkownik** modyfikuje prefiks i klika „Zapisz"
4. **Serwer** aktualizuje dane serii
5. **System** zamyka dialog; zaktualizowana seria widoczna na liście

## Przebieg główny — Usunięcie serii numeracji

1. **Użytkownik** klika ikonę usunięcia przy wybranej serii
2. **Aplikacja** wyświetla pytanie o potwierdzenie
3. **Użytkownik** potwierdza
4. **Serwer** usuwa serię
5. **System** odświeża listę serii

## Reguły biznesowe

| ID | Reguła | Objaśnienie |
|---|---|---|
| RB-01 | Seria numeracji powiązana jest z firmą i typem dokumentu | Każda seria przypisana do jednego z trzech typów: faktura, proforma, storno |
| RB-02 | Numer dokumentu = prefiks + licznik czterocyfrowy | Przykład: prefiks „FV" + licznik 15 = „FV0015" |
| RB-03 | Licznik serii zwiększany jest automatycznie przy każdym dokumencie | Użytkownik nie wpisuje numeru ręcznie |
| RB-04 | Domyślne serie tworzone są automatycznie przy pierwszej firmie | System tworzy serie z prefiksami dla wszystkich 3 typów dokumentów |
| RB-05 | Użytkownik może stworzyć wiele serii dla tego samego typu | Możliwe np. dwie serie faktur z różnymi prefiksami |

## Wyjątki i scenariusze alternatywne

| ID | Scenariusz | Warunek | Reakcja systemu |
|---|---|---|---|
| WYJ-01 | Brak serii przy wystawianiu faktury | Użytkownik nie ma żadnej serii dla danego typu | Lista serii pusta w formularzu faktury; zapis niemożliwy; brak wyraźnego komunikatu kierującego |
| WYJ-02 | Usunięcie serii używanej w dokumentach | Seria ma dokumenty z przypisanym numerem | Zachowanie nieokreślone — możliwy błąd klucza obcego w bazie |
| WYJ-03 | Zduplikowany prefiks serii | Użytkownik tworzy dwie serie z tym samym prefiksem dla tego samego typu | System nie blokuje — możliwe zduplikowane numery dokumentów |

## Wynik procesu

Po dodaniu serii:
- Seria przypisana do firmy użytkownika z licznikiem startowym
- Seria dostępna do wyboru w formularzu wystawiania dokumentu danego typu
- Kolejne dokumenty używają tej serii i inkrementują licznik

## Diagram sekwencji

```mermaid
sequenceDiagram
    autonumber
    participant U as Użytkownik
    participant FE as Aplikacja (Frontend)
    participant API as Serwer (API)
    participant DB as Baza danych

    U->>FE: Otwiera ekran Serie dokumentów
    FE->>API: Pobierz serie numeracji firmy
    API->>DB: Zapytanie o serie powiązane z firmą użytkownika
    DB-->>API: Lista serii (prefiks, typ, bieżący licznik)
    API-->>FE: Lista serii
    FE-->>U: Lista serii z przyciskami Dodaj / Edytuj / Usuń

    U->>FE: Klik Dodaj serię
    FE-->>U: Dialog z formularzem serii
    U->>FE: Wypełnia: prefiks, typ dokumentu, numer startowy
    U->>FE: Klik Zapisz

    FE->>API: Wyślij dane nowej serii numeracji
    API->>DB: Pobierz identyfikator firmy użytkownika
    DB-->>API: Identyfikator firmy
    API->>DB: Zapisz serię powiązaną z firmą (licznik = wartość startowa)
    DB-->>API: Seria zapisana
    API-->>FE: Seria dodana
    FE-->>U: Dialog zamknięty; seria na liście i dostępna w formularzach
```

## Powiązania analityczne

| Typ | Dokument |
|---|---|
| Use Case | [uc_serie_dokumentow](../../07_use_case/serie_dokumentow/uc_serie_dokumentow.md) |
| Proces powiązany | [BP-CFG-01 Onboarding](./BP-CFG-01_onboarding.md) |
| Proces powiązany | [BP-DOC-01 Wystawienie faktury](../dokumenty/BP-DOC-01_wystawienie_faktury.md) |
| Proces powiązany | [BP-DOC-02 Wystawienie proformy](../dokumenty/BP-DOC-02_wystawienie_proformy.md) |

## Powiązania techniczne

| Typ | Dokument |
|---|---|
| Proces techniczny | [dodaj_serie/proces.md](../../02_procesy/serie_dokumentow/dodaj_serie/proces.md) |
| API | [POST /api/DocumentSeries/Add](../../04_api_i_integracje/01_api_frontend/document_series/POST_DocumentSeries_Add.md) |
| Model DB | [dbo.DocumentSeries](../../05_model_danych/01_db/dbo/dbo.DocumentSeries.md) |
| Algorytm | [generowanie_numeru_dokumentu](../../03_algorytmy/dedykowane/generowanie_numeru_dokumentu.md) |

## Wątpliwości i braki

- Brak walidacji unikalności prefiksu serii per typ per firma — możliwe zduplikowane serie dające identyczne numery dokumentów
- Brak walidacji formatu prefiksu — możliwe wpisanie znaków specjalnych w nazwie serii
- Usunięcie serii przypisanej do dokumentów może skutkować błędem klucza obcego w bazie
- Brak informacji o konsekwencjach ręcznej zmiany bieżącego numeru licznika

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-06-01 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja BP — na podstawie PROC-AddDocumentSeries i BPMN-KONF-01; format analityczny BP-NN |
