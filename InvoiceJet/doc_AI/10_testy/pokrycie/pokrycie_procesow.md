# Pokrycie testami — Procesy BPMN

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-COV-PROCESY |
| Typ dokumentu | macierz pokrycia procesów |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Macierz pokrycia mapuje scenariusze testowe manualne na procesy biznesowe (BPMN) udokumentowane w projekcie InvoiceJet. Procesy reprezentują przepływy end-to-end z perspektywy użytkownika systemu.

## Tabela pokrycia procesów

| ID Procesu | Nazwa Procesu | Powiązane testy (TC-NNN) | Status pokrycia |
|---|---|---|---|
| PROC-AUTH-REJ | Rejestracja nowego użytkownika | TC-100, TC-101, TC-102, TC-103 | Pełne |
| PROC-AUTH-LOG | Logowanie do systemu | TC-104, TC-105 | Pełne |
| PROC-AUTH-WYLOG | Wylogowanie z systemu | TC-106 (pośrednio — wygaśnięcie) | Częściowe |
| PROC-AUTH-JWT | Wygaśnięcie sesji JWT i przekierowanie | TC-106 | Pełne |
| PROC-FIRMA-DODAJ | Dodanie własnej firmy (onboarding) | TC-110, TC-111 | Pełne |
| PROC-FIRMA-EDYTUJ | Edycja danych własnej firmy | TC-112 | Pełne |
| PROC-KLIENT-DODAJ-RECZNIE | Dodanie klienta ręcznie | TC-113 | Pełne |
| PROC-KLIENT-DODAJ-ANAF | Dodanie klienta przez ANAF | TC-114 | Pełne |
| PROC-PROD-DODAJ | Dodanie produktu do katalogu | TC-120 | Pełne |
| PROC-PROD-EDYTUJ | Edycja produktu | TC-121 | Pełne |
| PROC-PROD-USUN | Usunięcie produktu (soft-delete) | TC-122 | Pełne |
| PROC-KONTO-DODAJ | Dodanie konta bankowego | TC-130 | Pełne |
| PROC-KONTO-EDYTUJ | Edycja konta bankowego | TC-131 | Pełne |
| PROC-KONTO-USUN | Usunięcie konta bankowego | TC-132 | Pełne |
| PROC-SERIA-DODAJ | Dodanie serii numeracji | TC-140 | Pełne |
| PROC-SERIA-EDYTUJ | Edycja serii numeracji | TC-141 | Pełne |
| PROC-SERIA-USUN | Usunięcie serii numeracji | TC-142 | Pełne |
| PROC-FAK-WYSTAW | Wystawienie faktury | TC-150, TC-143 | Pełne |
| PROC-FAK-EDYTUJ | Edycja faktury | TC-155 | Pełne |
| PROC-FAK-USUN | Usunięcie faktury (soft-delete) | TC-156 | Pełne |
| PROC-FAK-PDF | Generowanie PDF faktury | TC-153 | Pełne |
| PROC-PRF-WYSTAW | Wystawienie proformy | TC-151 | Pełne |
| PROC-PRF-PDF | Generowanie PDF proformy (anomalia) | TC-154 | Pełne |
| PROC-STORNO-KONWERSJA | Konwersja dokumentu na storno | TC-152 | Pełne |
| PROC-DASHBOARD | Podgląd statystyk rocznych | TC-157 | Pełne |
| PROC-ONBOARDING | Pełny onboarding (rejestracja → pierwsza faktura) | TC-100, TC-104, TC-110, TC-130, TC-140, TC-150 | Częściowe |

## Uwagi

- **PROC-AUTH-WYLOG:** Wylogowanie jako świadoma akcja użytkownika (klik „Wyloguj") nie ma dedykowanego scenariusza testowego — jest pokryte pośrednio. Rekomendowane dodanie TC-107 w przyszłości.
- **PROC-ONBOARDING:** Pełny przepływ onboardingowy jest pokryty osobnymi TC dla każdego kroku, ale brak scenariusza E2E łączącego wszystkie kroki w jednym teście.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
