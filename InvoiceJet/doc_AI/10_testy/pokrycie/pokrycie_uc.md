# Pokrycie testami — Use Case

| Pole | Wartość |
|---|---|
| ID dokumentu | TEST-COV-UC |
| Typ dokumentu | macierz pokrycia use case |
| Wersja | 0.1 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Macierz pokrycia mapuje scenariusze testowe manualne na udokumentowane przypadki użycia (Use Case) projektu InvoiceJet. Status pokrycia wskazuje, czy wszystkie ścieżki UC (główna i alternatywne) mają przypisane scenariusze testowe.

## Tabela pokrycia UC

| ID UC | Nazwa UC | Powiązane testy (TC-NNN) | Status pokrycia |
|---|---|---|---|
| UC-Globalny-Autentykacja | Autentykacja użytkownika | TC-100, TC-101, TC-102, TC-103, TC-104, TC-105, TC-106 | Pełne |
| UC-Globalny-Autentykacja (A1) | Rejestracja — e-mail zajęty | TC-103 | Pełne |
| UC-Globalny-Autentykacja (A2) | Rejestracja — hasło za słabe | TC-101, TC-102 | Pełne |
| UC-Globalny-Autentykacja (A3) | Logowanie — błędne dane | TC-105 | Pełne |
| UC-Globalny-Autentykacja (A4) | Wygaśnięcie sesji JWT | TC-106 | Pełne |
| UC-Firma-DodajFirme | Dodanie własnej firmy | TC-110 | Pełne |
| UC-Firma-ANAF | Autouzupełnienie z ANAF | TC-111, TC-114 | Pełne |
| UC-Firma-EdytujFirme | Edycja danych firmy | TC-112 | Pełne |
| UC-Firma-DodajKlienta | Dodanie klienta | TC-113, TC-114 | Pełne |
| UC-Produkt-Dodaj | Dodanie produktu | TC-120 | Pełne |
| UC-Produkt-Edytuj | Edycja produktu | TC-121 | Pełne |
| UC-Produkt-Usun | Usunięcie produktu | TC-122 | Pełne |
| UC-Produkt-UniqueIndex | Konflikt unikalności nazwy produktu | TC-123 | Pełne |
| UC-KontoBankowe-Dodaj | Dodanie konta bankowego | TC-130 | Pełne |
| UC-KontoBankowe-Edytuj | Edycja konta bankowego | TC-131 | Pełne |
| UC-KontoBankowe-Usun | Usunięcie konta bankowego | TC-132 | Pełne |
| UC-SeriaDokumentow-Dodaj | Dodanie serii dokumentów | TC-140 | Pełne |
| UC-SeriaDokumentow-Edytuj | Edycja serii | TC-141 | Pełne |
| UC-SeriaDokumentow-Usun | Usunięcie serii | TC-142 | Pełne |
| UC-SeriaDokumentow-Numeracja | Generowanie kolejnych numerów | TC-143 | Pełne |
| UC-Dokumenty-Faktury | Wystawianie i zarządzanie fakturami | TC-150, TC-153, TC-155, TC-156 | Pełne |
| UC-Dokumenty-Faktury (A1) | Brak konfiguracji (seria, konto) | TC-140, TC-130 (warunki wstępne) | Częściowe |
| UC-Dokumenty-FakturyProforma | Wystawianie i zarządzanie proformami | TC-151, TC-154 | Pełne |
| UC-Dokumenty-FakturyProforma (A1) | Brak serii dla proformy | TC-140 (warunki wstępne) | Częściowe |
| UC-Dokumenty-FakturyStorno | Konwersja na storno | TC-152 | Pełne |
| UC-Dokumenty-Dashboard | Statystyki dashboardu | TC-157 | Pełne |
| UC-Dokumenty-GenerujPDF | Generowanie PDF faktury | TC-153 | Pełne |
| UC-Dokumenty-GenerujPDF-Proforma | Generowanie PDF proformy (anomalia) | TC-154 | Pełne |

## Legenda statusów

| Status | Opis |
|---|---|
| Pełne | Wszystkie ścieżki UC (główna i alternatywne) pokryte scenariuszami testowymi |
| Częściowe | Scenariusz główny pokryty; niektóre ścieżki alternatywne pokryte pośrednio (przez warunki wstępne innych TC) |
| Brak | Brak scenariuszy testowych dla tego UC |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
