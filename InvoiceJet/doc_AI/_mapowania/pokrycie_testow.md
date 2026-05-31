# Pokrycie testów (M-06)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-06 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa wiąże obszary funkcjonalne (UC i ekrany) z planowanymi scenariuszami testów manualnych (TC-100..TC-159). Projekt InvoiceJet nie posiada testów automatycznych — wszystkie scenariusze mają status „Planowany". Mapa służy jako punkt startowy dla planowania pokrycia testowego.

## Tabela pokrycia testów

| Obszar | UC / Ekran | Scenariusz testowy | ID TC | Typ testu | Status pokrycia |
|---|---|---|---|---|---|
| Autentykacja | EKRAN-01 Login | Logowanie z poprawnymi danymi | TC-100 | Manualny | Planowany |
| Autentykacja | EKRAN-01 Login | Logowanie z błędnym hasłem | TC-101 | Manualny | Planowany |
| Autentykacja | EKRAN-01 Login | Logowanie z nieistniejącym emailem | TC-102 | Manualny | Planowany |
| Autentykacja | EKRAN-02 Register | Rejestracja z poprawnymi danymi | TC-103 | Manualny | Planowany |
| Autentykacja | EKRAN-02 Register | Rejestracja z istniejącym emailem | TC-104 | Manualny | Planowany |
| Autentykacja | EKRAN-02 Register | Rejestracja z niezgodnymi hasłami | TC-105 | Manualny | Planowany |
| Autentykacja | EKRAN-01/02 | Wylogowanie i brak dostępu do /dashboard | TC-106 | Manualny | Planowany |
| Autentykacja | EKRAN-01/02 | Wygaśnięcie tokenu JWT — wyświetlenie modalu | TC-107 | Manualny | Planowany |
| Dane firmy | EKRAN-04 | Podgląd danych własnej firmy | TC-108 | Manualny | Planowany |
| Dane firmy | EKRAN-04 | Edycja i zapis danych firmy | TC-109 | Manualny | Planowany |
| Dane firmy | EKRAN-04 | Autouzupełnienie z ANAF po numerze CUI | TC-110 | Manualny | Planowany |
| Dane firmy | EKRAN-04 | Autouzupełnienie z ANAF — błędny CUI | TC-111 | Manualny | Planowany |
| Klienci | EKRAN-05 | Wyświetlenie listy klientów | TC-112 | Manualny | Planowany |
| Klienci | EKRAN-05 + DIALOG-01 | Dodanie nowego klienta | TC-113 | Manualny | Planowany |
| Klienci | EKRAN-05 + DIALOG-01 | Edycja danych klienta | TC-114 | Manualny | Planowany |
| Klienci | EKRAN-05 | Usunięcie klienta (soft-delete) | TC-115 | Manualny | Planowany |
| Konta bankowe | EKRAN-06 | Wyświetlenie listy kont bankowych | TC-116 | Manualny | Planowany |
| Konta bankowe | EKRAN-06 + DIALOG-02 | Dodanie konta bankowego | TC-117 | Manualny | Planowany |
| Konta bankowe | EKRAN-06 + DIALOG-02 | Edycja konta bankowego | TC-118 | Manualny | Planowany |
| Konta bankowe | EKRAN-06 | Usunięcie konta bankowego (soft-delete) | TC-119 | Manualny | Planowany |
| Produkty | EKRAN-07 | Wyświetlenie listy produktów | TC-120 | Manualny | Planowany |
| Produkty | EKRAN-07 + DIALOG-03 | Dodanie produktu | TC-121 | Manualny | Planowany |
| Produkty | EKRAN-07 + DIALOG-03 | Edycja produktu | TC-122 | Manualny | Planowany |
| Produkty | EKRAN-07 | Usunięcie produktu (soft-delete) | TC-123 | Manualny | Planowany |
| Serie dokumentów | EKRAN-08 | Wyświetlenie listy serii | TC-124 | Manualny | Planowany |
| Serie dokumentów | EKRAN-08 + DIALOG-04 | Dodanie serii dokumentów | TC-125 | Manualny | Planowany |
| Serie dokumentów | EKRAN-08 + DIALOG-04 | Edycja serii dokumentów | TC-126 | Manualny | Planowany |
| Serie dokumentów | EKRAN-08 | Usunięcie serii (soft-delete) | TC-127 | Manualny | Planowany |
| Faktury | EKRAN-09 | Wyświetlenie listy faktur | TC-128 | Manualny | Planowany |
| Faktury | EKRAN-10 | Dodanie nowej faktury | TC-129 | Manualny | Planowany |
| Faktury | EKRAN-10 | Edycja istniejącej faktury | TC-130 | Manualny | Planowany |
| Faktury | EKRAN-09 | Usunięcie faktury (soft-delete) | TC-131 | Manualny | Planowany |
| Faktury | EKRAN-10 + DIALOG-05 | Podgląd PDF faktury (GetPdfStream) | TC-132 | Manualny | Planowany |
| Faktury | EKRAN-10 | Generowanie PDF faktury (pobierz plik) | TC-133 | Manualny | Planowany |
| Faktury | EKRAN-09 | Konwersja faktury na storno | TC-134 | Manualny | Planowany |
| Proformy | EKRAN-11 | Wyświetlenie listy proform | TC-135 | Manualny | Planowany |
| Proformy | EKRAN-12 | Dodanie nowej proformy | TC-136 | Manualny | Planowany |
| Proformy | EKRAN-12 | Edycja istniejącej proformy | TC-137 | Manualny | Planowany |
| Proformy | EKRAN-11 | Usunięcie proformy (soft-delete) | TC-138 | Manualny | Planowany |
| Proformy | EKRAN-12 + DIALOG-05 | Podgląd PDF proformy | TC-139 | Manualny | Planowany |
| Storna | EKRAN-13 | Wyświetlenie listy storn | TC-140 | Manualny | Planowany |
| Storna | EKRAN-14 | Podgląd i edycja storna | TC-141 | Manualny | Planowany |
| Storna | EKRAN-13 | Usunięcie storna (soft-delete) | TC-142 | Manualny | Planowany |
| Storna | EKRAN-14 + DIALOG-05 | Podgląd PDF storna | TC-143 | Manualny | Planowany |
| Dashboard | EKRAN-03 | Wyświetlenie statystyk — liczniki | TC-144 | Manualny | Planowany |
| Dashboard | EKRAN-03 | Wyświetlenie statystyk — wykres miesięczny | TC-145 | Manualny | Planowany |
| Dashboard | EKRAN-03 | Zmiana roku na dashboardzie | TC-146 | Manualny | Planowany |
| Izolacja danych | Wszystkie ekrany | Dane użytkownika A niewidoczne dla użytkownika B | TC-147 | Manualny | Planowany |
| Autoryzacja | Wszystkie ekrany /dashboard | Dostęp bez JWT — redirect na /login | TC-148 | Manualny | Planowany |
| Autoryzacja | Wszystkie endpointy API | Żądanie bez nagłówka Bearer — HTTP 401 | TC-149 | Manualny | Planowany |
| PDF | EKRAN-10 | Bug TC: PDF proformy zwraca template faktury zwykłej (API-28 bug) | TC-150 | Manualny | Planowany |
| Nawigacja | Wszystkie ekrany | Sidebar — nawigacja między wszystkimi sekcjami | TC-151 | Manualny | Planowany |
| Nawigacja | EKRAN-01/02 | Przejście Login ↔ Register | TC-152 | Manualny | Planowany |
| Walidacja | EKRAN-10 | Zapis faktury bez produktów | TC-153 | Manualny | Planowany |
| Walidacja | EKRAN-10 | Zapis faktury bez serii dokumentów | TC-154 | Manualny | Planowany |
| Walidacja | EKRAN-02 | Rejestracja — walidacja pól wymaganych | TC-155 | Manualny | Planowany |
| Soft-delete | EKRAN-05, 06, 07, 08, 09 | Usunięty rekord znika z listy po odświeżeniu | TC-156 | Manualny | Planowany |
| ANAF | EKRAN-04 | ANAF niedostępny — obsługa błędu | TC-157 | Manualny | Planowany |
| Token | Globalny | Token wygasły — modal + wylogowanie | TC-158 | Manualny | Planowany |
| Storno | EKRAN-09 | TransformToStorno — storno widoczne na liście storn | TC-159 | Manualny | Planowany |

## Obszary bez pokrycia (luki)

| Obszar | Uzasadnienie |
|---|---|
| Testy jednostkowe (unit) | Brak — projekt nie zawiera projektów testowych (.Tests) |
| Testy integracyjne | Brak — brak konfiguracji testowej bazy danych |
| Testy E2E (Cypress/Playwright) | Brak — brak konfiguracji narzędzi testów E2E |
| Testy wydajnościowe | Brak — poza zakresem MVP |
| Testy bezpieczeństwa | Brak — poza zakresem MVP; znane braki: brak granularnej autoryzacji, brak refresh token |

## Uwagi

- Numery TC-100..TC-159 są zarezerwowane dla testów manualnych zgodnie z konwencją katalogową `10_testy/manualne/`.
- Wszystkie scenariusze mają status „Planowany" — żaden nie jest wykonany ani zautomatyzowany.
- TC-150 jest scenariuszem weryfikacji **znalezionego buga** (API-28 hardcoded InvoiceDocument) — należy wykonać i udokumentować jako błąd.
- Izolacja danych (TC-147) jest krytyczna — wymaga dwóch kont testowych.
- Źródło: [inwentaryzacja_ekranow.md](inwentaryzacja_ekranow.md), [inwentaryzacja_api.md](inwentaryzacja_api.md)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 60 scenariuszy testowych, status: Planowany. |
