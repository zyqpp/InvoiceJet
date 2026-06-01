# BP-CFG-02 Zarządzanie kontami bankowymi

| Pole | Wartość |
|---|---|
| ID dokumentu | BP-CFG-02 |
| Obszar | Konfiguracja |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-01 |

## Cel biznesowy

Umożliwić użytkownikowi zarządzanie danymi kont bankowych firmy, które będą drukowane na fakturach jako informacje do przelewu dla klienta.

## Kontekst

Użytkownik zarządza kontami bankowymi na ekranie „Konta bankowe" (`/dashboard/bank-accounts`). Konto bankowe jest obowiązkowe do wystawienia faktury — bez niego zapis faktury jest zablokowany. Firma może mieć wiele kont bankowych w różnych walutach; użytkownik wybiera konkretne konto przy każdej fakturze.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Zarządza listą kont bankowych firmy |
| Aplikacja (Frontend) | Wyświetla listę kont, obsługuje dialogi dodawania i edycji |
| Serwer (API) | Zapisuje, aktualizuje lub usuwa konta bankowe |
| Baza danych | Trwale przechowuje dane kont bankowych |

## Warunki wejścia

- Użytkownik zalogowany
- Dane własnej firmy wypełnione (firma musi istnieć, by przypisać do niej konto)

## Przebieg główny — Dodanie konta bankowego

1. **Użytkownik** otwiera ekran „Konta bankowe"
2. **Aplikacja** pobiera i wyświetla listę istniejących kont bankowych firmy
3. **Użytkownik** klika „Dodaj konto"
4. **Aplikacja** wyświetla dialog z formularzem: nazwa banku, numer IBAN, waluta
5. **Użytkownik** wypełnia formularz i klika „Zapisz"
6. **Serwer** przypisuje konto do firmy użytkownika i zapisuje
7. **System** zamyka dialog; nowe konto widoczne na liście i w selektorach formularzy dokumentów

## Przebieg główny — Edycja konta bankowego

1. **Użytkownik** klika przycisk edycji przy wybranym koncie
2. **Aplikacja** wyświetla dialog z wypełnionym formularzem
3. **Użytkownik** modyfikuje dane i klika „Zapisz"
4. **Serwer** aktualizuje dane konta
5. **System** zamyka dialog; zaktualizowane dane widoczne na liście

## Przebieg główny — Usunięcie konta bankowego

1. **Użytkownik** klika ikonę usunięcia przy wybranym koncie
2. **Aplikacja** wyświetla pytanie o potwierdzenie
3. **Użytkownik** potwierdza
4. **Serwer** usuwa konto bankowe
5. **System** odświeża listę kont

## Reguły biznesowe

| ID | Reguła | Objaśnienie |
|---|---|---|
| RB-01 | Konto bankowe powiązane jest z firmą użytkownika | Konta widoczne i dostępne tylko dla właściciela firmy |
| RB-02 | Co najmniej jedno konto wymagane do wystawienia faktury | Brak konta blokuje zapis dokumentu |
| RB-03 | Firma może posiadać wiele kont bankowych | Użytkownik wybiera konto przy każdym dokumencie |
| RB-04 | Waluta konta może być różna | RON, EUR, USD i inne waluty |
| RB-05 | Numer IBAN nie jest walidowany po stronie serwera | Poprawność formatu IBAN weryfikowana wyłącznie przez formularz |

## Wyjątki i scenariusze alternatywne

| ID | Scenariusz | Warunek | Reakcja systemu |
|---|---|---|---|
| WYJ-01 | Próba wystawienia faktury bez konta | Użytkownik nie dodał żadnego konta bankowego | Zapis faktury zablokowany; komunikat o brakującym koncie |
| WYJ-02 | Usunięcie jedynego konta | Użytkownik chce usunąć ostatnie konto | System nie blokuje usunięcia — brak walidacji (po usunięciu faktury nie można wystawiać) |
| WYJ-03 | Usunięcie konta używanego w dokumentach | Konto przypisane do już wystawionych faktur | Zachowanie nieokreślone — możliwy błąd klucza obcego w bazie |

## Wynik procesu

Po dodaniu:
- Konto bankowe przypisane do firmy użytkownika
- Konto dostępne do wyboru w formularzu faktury / proformy / storno
- Dane konta drukowane na PDF dokumentów

Po usunięciu:
- Konto niewidoczne na liście i niewidoczne w selektorach

## Diagram sekwencji

```mermaid
sequenceDiagram
    autonumber
    participant U as Użytkownik
    participant FE as Aplikacja (Frontend)
    participant API as Serwer (API)
    participant DB as Baza danych

    U->>FE: Otwiera ekran Konta bankowe
    FE->>API: Pobierz konta bankowe firmy
    API->>DB: Zapytanie o konta bankowe firmy użytkownika
    DB-->>API: Lista kont bankowych
    API-->>FE: Lista kont
    FE-->>U: Lista kont z przyciskami Dodaj / Edytuj / Usuń

    U->>FE: Klik Dodaj konto
    FE-->>U: Dialog z formularzem konta bankowego
    U->>FE: Wypełnia: nazwa banku, numer IBAN, waluta
    U->>FE: Klik Zapisz

    FE->>API: Wyślij dane nowego konta bankowego
    API->>DB: Pobierz identyfikator firmy użytkownika
    DB-->>API: Identyfikator firmy
    API->>DB: Zapisz konto bankowe powiązane z firmą
    DB-->>API: Konto zapisane
    API-->>FE: Konto dodane
    FE-->>U: Dialog zamknięty; konto na liście i dostępne w formularzach
```

## Powiązania analityczne

| Typ | Dokument |
|---|---|
| Use Case | [uc_konta_bankowe](../../07_use_case/konta_bankowe/uc_konta_bankowe.md) |
| Proces powiązany | [BP-CFG-01 Onboarding](./BP-CFG-01_onboarding.md) |
| Proces powiązany | [BP-DOC-01 Wystawienie faktury](../dokumenty/BP-DOC-01_wystawienie_faktury.md) |

## Powiązania techniczne

| Typ | Dokument |
|---|---|
| Proces techniczny | [dodaj_konto/proces.md](../../02_procesy/konta_bankowe/dodaj_konto/proces.md) |
| API | [POST /api/BankAccount/Add](../../04_api_i_integracje/01_api_frontend/bank_account/POST_BankAccount_Add.md) |
| Model DB | [dbo.BankAccount](../../05_model_danych/01_db/dbo/dbo.BankAccount.md) |

## Wątpliwości i braki

- Brak walidacji formatu IBAN po stronie serwera — możliwe zapisanie błędnego numeru rachunku
- Brak limitu liczby kont bankowych per firma
- Usunięcie konta używanego w wystawionych dokumentach może spowodować błąd bazy danych (klucz obcy)
- Brak walidacji przy usunięciu ostatniego konta — po usunięciu nie można wystawiać faktur

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-06-01 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja BP — na podstawie PROC-AddBankAccount i BPMN-KONF-01; format analityczny BP-NN |
