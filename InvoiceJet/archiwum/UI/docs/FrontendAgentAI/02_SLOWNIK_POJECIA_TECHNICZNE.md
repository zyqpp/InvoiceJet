# Słownik pojęć technicznych
## Wytyczne językowe AOS — Część 2 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Zasada:** Używaj wyłącznie terminów z kolumny "Termin obowiązujący". Synonimy z kolumny "Nazwy zakazane" są niedopuszczalne.

---

## 1. Elementy interfejsu użytkownika

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **ekran** | Pojedynczy widok Angular ładowany przez Router na podstawie ścieżki URL. Jeden ekran = jeden route = jeden dokument AOS. | widok, strona, formatka, okno główne, panel, zakładka (gdy nie chodzi o tab) |
| **komponent** | Klasa Angular składająca się z pliku `.component.ts`, `.component.html` i `.component.scss`. Jednostka strukturalna ekranu. | element, moduł (gdy nie chodzi o NgModule), blok |
| **pole** | Pojedynczy element formularza umożliwiający wprowadzenie lub wyświetlenie jednej wartości. Posiada `formControlName` lub `[(ngModel)]`. | input, kontrolka, widget, box |
| **pole wymagane** | Pole posiadające walidator `Validators.required`. | pole obowiązkowe, pole niezbędne, pole konieczne |
| **pole opcjonalne** | Pole nieposiadające walidatora `Validators.required`. | pole nieobowiązkowe, pole dowolne, pole do wyboru |
| **formularz** | Grupa pól powiązanych w `FormGroup` Angular Reactive Forms lub Template-Driven Forms. | formatka, forma |
| **formularz reaktywny** | Formularz implementowany przez `ReactiveFormsModule` i `FormBuilder`. | reactive form (ang.), formularz reaktywny |
| **grid** | Komponent tabelaryczny Angular Material (`<mat-table>`) wyświetlający wiele rekordów w wierszach i kolumnach. | tabela, lista tabelaryczna, zestawienie (gdy chodzi o `mat-table`), datagrid |
| **kolumna** | Pionowy zestaw danych w gridzie, definiowany przez `matColumnDef`. | pole tabeli, komórka (gdy nie chodzi o konkretną komórkę), pole gridu |
| **wiersz** | Poziomy zestaw wartości w gridzie odpowiadający jednemu rekordowi danych. | pozycja, wpis, linia, element listy |
| **dialog** | Okno modalne Angular Material (`MatDialog`) otwierane nad widokiem głównym. Posiada własny komponent. | popup, modal, okno dialogowe, okienko, overlay |
| **sekcja filtrów** | Wyodrębniona część ekranu zawierająca pola służące do zawężania danych wyświetlanych w gridzie. Pola filtrów nie zapisują danych. | pasek wyszukiwania (gdy chodzi o całą sekcję), panel filtrów, search bar |
| **pasek tytułu** | Poziomy element UI zawierający tytuł ekranu i główne przyciski operacyjne. | toolbar, header (gdy nie chodzi o `<header>` HTML), nagłówek ekranu |
| **menu kontekstowe** | Lista opcji rozwijana po kliknięciu ikony `⋮`. Angular Material: `<mat-menu>`. | dropdown menu (gdy chodzi o menu akcji), context menu (ang.) |
| **paginacja** | Mechanizm podziału zbioru danych na strony. Angular Material: `<mat-paginator>`. | stronicowanie, paging |
| **sortowanie** | Mechanizm porządkowania wierszy gridu po wartości kolumny. Angular Material: `matSort`. | ordering, filtrowanie (to jest odrębne pojęcie) |
| **lista rozwijana** | Pole wyboru wartości ze słownika. Angular Material: `<mat-select>`. | dropdown, select, combobox |
| **pole wyboru** | Pole binarne zaznaczone / niezaznaczone. Angular Material: `<mat-checkbox>`. | checkbox (ang. w opisach biznesowych) |
| **pole daty** | Pole do wprowadzania daty. Angular Material: `<mat-datepicker>`. | datepicker, kalen darz, date input |
| **etykieta pola** | Tekst opisujący pole, wyświetlany nad lub obok pola. Angular Material: `<mat-label>`. | label (ang. w opisach biznesowych), podpis pola |
| **tekst podpowiedzi** | Tekst wyświetlany wewnątrz pustego pola. Angular Material: `placeholder`. | placeholder (ang. w opisach biznesowych), hint |
| **dymek podpowiedzi** | Tekst wyświetlany po najechaniu kursorem na element. Angular Material: `matTooltip`. | tooltip (ang. w opisach biznesowych) |
| **komunikat walidacji** | Tekst błędu wyświetlany pod polem. Angular Material: `<mat-error>`. | error message, komunikat błędu pola (gdy nie chodzi o globalny błąd) |
| **ścieżka nawigacyjna** | Element UI pokazujący hierarchię lokalizacji użytkownika w aplikacji. | breadcrumb (ang.) |
| **stan ładowania** | Stan komponentu podczas oczekiwania na odpowiedź API. | loading, spinner (gdy nie chodzi o typ komponentu) |

---

## 2. Architektura Angular

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **interceptor** | Klasa Angular implementująca `HttpInterceptor` — modyfikuje każde żądanie HTTP lub odpowiedź przed przetworzeniem. | middleware (gdy chodzi o interceptor Angular HTTP), wrapper |
| **guard** | Klasa Angular implementująca `CanActivate` lub analogiczne interfejsy — kontroluje dostęp do trasy routera. | strażnik, auth check (gdy chodzi o guard) |
| **serwis** | Klasa Angular z dekoratorem `@Injectable()` dostarczająca logikę i wywołania HTTP. Wstrzykiwana przez DI. | service (ang. w opisach biznesowych), provider |
| **model danych** | Interfejs TypeScript (`interface I<Nazwa>`) definiujący strukturę obiektu. | typ, klasa modelu (gdy chodzi o interfejs TS), schema (gdy nie chodzi o DB) |
| **binding** | Mechanizm powiązania właściwości komponentu z elementem HTML. Typy: `[(ngModel)]`, `[formControl]`, `{{ }}`. | powiązanie danych, data binding (ang. w opisach biznesowych) |
| **walidator** | Funkcja Angular (`Validators.*`) sprawdzająca poprawność wartości pola formularza. | reguła walidacji (termin nadrzędny jest OK), constraint |
| **słownik** | Zamknięty, predefiniowany zestaw dopuszczalnych wartości dla pola. | lista wartości, enum (gdy nie chodzi o typ TypeScript), dropdown values |

---

## 3. Komunikacja HTTP

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **endpoint** | Ścieżka URL API wraz z metodą HTTP, np. `GET /api/clients`. | adres API, URL serwisu, route API, akcja kontrolera |
| **token JWT** | Zakodowany ciąg tekstowy służący do autoryzacji żądań HTTP, generowany po zalogowaniu. | token autoryzacyjny (dopuszczalne jako synonim), bearer token |
| **żądanie HTTP** | Pojedyncze wywołanie API wysłane przez `HttpClient`. | request (ang. w opisach biznesowych), zapytanie HTTP |
| **odpowiedź API** | Dane zwrócone przez serwer po wykonaniu żądania HTTP. | response (ang. w opisach biznesowych), wynik zapytania |

### Metody HTTP — zapis i zastosowanie

Metody HTTP zawsze zapisywane **wersalikami** bez cudzysłowu w kontekście technicznym.

| Metoda | Zastosowanie | Nazwy zakazane |
|---|---|---|
| `GET` | Pobieranie danych bez modyfikacji zasobu | pobierz, odczytaj, wczytaj |
| `POST` | Tworzenie nowego zasobu | utwórz, dodaj, zapisz (gdy chodzi o metodę HTTP) |
| `PUT` | Zastąpienie istniejącego zasobu (pełna aktualizacja) | zaktualizuj (gdy chodzi o metodę HTTP) |
| `PATCH` | Częściowa aktualizacja istniejącego zasobu | edytuj (gdy chodzi o metodę HTTP) |
| `DELETE` | Usunięcie zasobu | usuń (gdy chodzi o metodę HTTP) |
