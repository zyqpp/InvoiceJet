# S-03. Słownik elementów dokumentacji — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| ID | S-03 |
| Nazwa | Słownik elementów dokumentacji |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Data | 2026-05-31 |
| Status | Szkic |
| Plik | `doc_AI/_slowniki/slownik_elementow_dokumentacji.md` |

## Streszczenie

Słownik definiuje precyzyjnie typy artefaktów używanych w dokumentacji AOS projektu InvoiceJet. Każda definicja określa zakres pojęcia, sposób identyfikacji (prefiks ID) oraz powiązanie z kodem źródłowym. Spójne stosowanie tych definicji jest warunkiem poprawnego linkowania między dokumentami i mapami krzyżowymi.

---

## Elementy dokumentacji

### ekran {#ekran}

Komponent Angular posiadający własny widok (szablon HTML) i trasę routingową — odpowiada jednemu adresowi URL w aplikacji SPA. Ekran jest najwyższym poziomem UI, zawiera sekcje ekranu, pola, tabele i operacje. Prefiks ID: `EKRAN-`. Przykład: `EKRAN-Login` (komponent `login.component.ts`). Ekrany inwentaryzowane w pliku `inwentaryzacja_ekranow.md`.

### sekcja ekranu {#sekcja-ekranu}

Logicznie wyodrębniona część ekranu, nie posiadająca własnej trasy routingowej. Może być realizowana przez Angular `@ViewChild`, komponent zagnieżdżony lub blok HTML z własnym nagłówkiem. Przykłady sekcji: nagłówek z filtrami, lista wyników, panel szczegółów, formularz dodawania. Sekcje opisywane jako podpunkty dokumentu ekranu.

### pole {#pole}

Pojedynczy element interaktywny lub informacyjny w formularzu albo kolumna w tabeli UI. Pole ma typ (tekst, data, liczba, select, checkbox), etykietę widoczną dla użytkownika oraz mapowanie na pole DTO lub encji. Prefiks ID: `POLE-`. Przykład: `POLE-Login-Email` (pole e-mail na ekranie logowania).

### operacja {#operacja}

Akcja wykonywana przez użytkownika: kliknięcie przycisku, wybranie opcji z menu, skrót klawiszowy lub link nawigacyjny prowadzący do zmiany stanu systemu lub nawigacji. Każda operacja ma określony efekt (wywołanie endpointu, przejście ekranowe, otwarcie modalu). Prefiks ID: `OP-`. Przykład: `OP-Login-Zaloguj`.

### filtr {#filtr}

Pole lub zestaw pól umożliwiających zawężenie zbioru rekordów wyświetlanych w tabeli ekranu. Filtry działają po stronie frontendu (Angular) lub wysyłają parametry zapytania do API. Prefiks ID: `FILTR-`. Przykład: `FILTR-Faktury-TypDokumentu` (filtr po typie dokumentu na liście faktur).

### tabela ekranu {#tabela-ekranu}

Lista lub grid danych wyświetlanych użytkownikowi — realizowana przez Angular Material `MatTable` lub podobny komponent. Zawiera kolumny odpowiadające polom DTO. W projekcie InvoiceJet tabele nie posiadają paginacji (anomalia A-SR-03). Prefiks ID: `TAB-`. Przykład: `TAB-Faktury-Lista`.

### modal / dialog {#modal}

Okno nakładkowe (overlay) wyświetlane ponad głównym widokiem ekranu. W projekcie realizowany przez `MatDialog` z Angular Material. Blokuje interakcję z tłem do czasu zamknięcia. Zawiera formularz lub informację + przyciski akcji (Zapisz/Anuluj). Prefiks ID: `MODAL-`. Przykład: `MODAL-Klienci-DodajKlienta`.

### powiadomienie {#powiadomienie}

Krótkotrwały komunikat zwrotny dla użytkownika po wykonaniu operacji: toast, snackbar lub alert. W projekcie realizowany przez Angular Material `MatSnackBar`. Może informować o sukcesie, błędzie lub ostrzeżeniu. Nie blokuje interfejsu. Prefiks ID: `POW-`. Przykład: `POW-Faktury-ZapisanoFakture`.

### proces techniczny {#proces-techniczny}

Sekwencja kroków wykonywanych po stronie backendu w odpowiedzi na żądanie HTTP: od kontrolera, przez serwis i repozytorium, do bazy danych i z powrotem. Dokumentowany jako lista kroków z referencjami do klas i metod. Prefiks ID: `PROC-`. Przykład: `PROC-Rejestracja`. Procesy inwentaryzowane w `inwentaryzacja_procesow.md`.

### algorytm {#algorytm}

Jednoznaczna procedura obliczeniowa lub decyzyjna realizowana przez konkretną metodę lub zestaw metod w kodzie backendowym lub frontendowym. Różni się od procesu technicznego tym, że skupia się na logice wewnętrznej (warunki, pętle, obliczenia) a nie na sekwencji wywołań warstw. Prefiks ID: `ALG-`. Przykład: `ALG-WalidacjaHasla`. Algorytmy inwentaryzowane w `inwentaryzacja_algorytmow.md`.

### endpoint API {#endpoint-api}

Kontrakt HTTP udostępniany przez backend: metoda HTTP (GET/POST/PUT/DELETE) + ścieżka URL + DTO żądania (Request) + DTO odpowiedzi (Response) + kody statusu. Dokumentowany jako tabela kontraktu z przykładem JSON. Prefiks ID: `API-`. Przykład: `API-PostAuthRegister`. Endpointy inwentaryzowane w `inwentaryzacja_api.md`.

### przypadek użycia / UC {#uc}

Scenariusz opisujący interakcję aktora (użytkownika) z systemem w celu osiągnięcia określonego celu biznesowego. Zawiera: aktora, warunek wstępny, scenariusz główny (kroki), scenariusze alternatywne i warunek końcowy. Prefiks ID: `UC-`. Przykład: `UC-WystawienieFaktury`.

### proces biznesowy / BPMN {#bpmn}

Diagram sekwencji czynności biznesowych zapisany w notacji BPMN (Business Process Model and Notation). Przedstawia przepływ pracy z perspektywy biznesowej, z podziałem na tory (swimlane): użytkownik, system, zewnętrzne serwisy. Prefiks ID: `BPMN-`. Przykład: `BPMN-WystawienieFaktury`.

### scenariusz testowy {#scenariusz-testowy}

Ustrukturyzowany opis testu zawierający: identyfikator, tytuł, warunki wstępne, kroki do wykonania, dane wejściowe i oczekiwany wynik. Pokrywa jedną ścieżkę (szczęśliwą lub alternatywną) przypadku użycia. Prefiks ID: `TEST-`. Przykład: `TEST-Rejestracja-SzczesliwaSciezka`. Pokrycie testów mapowane w `pokrycie_testow.md`.

### inwentaryzacja {#inwentaryzacja}

Lista wszystkich artefaktów danego typu zidentyfikowanych w projekcie, wraz z lokalizacją w kodzie i linkami do dokumentów AOS. Format: tabela z kolumnami: ID, nazwa artefaktu (1:1 z kodu), lokalizacja w kodzie, link do dokumentu, status (`brak` / `szkic` / `gotowy` / `zaakceptowany`). Pliki inwentaryzacji żyją w katalogu `doc_AI/_mapowania/`.

### mapa krzyżowa {#mapa-krzyzowa}

Tabela powiązań między artefaktami dwóch różnych typów, np. API ↔ DTO, ekrany ↔ operacje, UC ↔ procesy biznesowe. Umożliwia nawigację w obu kierunkach. Każde powiązanie zapisane w mapie jest równoważne linkowi w sekcji „Powiązania" dokumentu. Pliki map krzyżowych żyją w katalogu `doc_AI/_mapowania/`.

---

## Wątpliwości i braki

| ID | Wątpliwość | Status |
|---|---|---|
| W-01 | Różnica między `EKRAN-` a `LAYOUT-XX` (klasa layoutu) nie jest w tej definicji uwzględniona — `LAYOUT-XX` używany w `slownik_pojec.md`. | Do_zdefiniowania |
| W-02 | Czy `DIALOG-XX` (z `slownik_pojec.md`) jest synonimem `MODAL-` (z wytycznych)? Wymaga ujednolicenia prefiksów. | Do_zdefiniowania |
| W-03 | Definicja „sekcji ekranu" — brak jednoznacznego kryterium granicy między sekcją a ekranem zagnieżdżonym. | Do_zdefiniowania |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 16 elementów dokumentacji. |
