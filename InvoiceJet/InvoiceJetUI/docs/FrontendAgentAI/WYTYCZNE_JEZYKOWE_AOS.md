# Wytyczne językowe i słownik terminologii
## Standard pisania dokumentacji AOS — Frontend Angular

**Dokument:** Wytyczne redakcyjne  
**Dotyczy:** Agent AI generujący dokumentację AOS warstwy frontendowej  
**Wersja:** 1.0  
**Data:** 2025-05-29  
**Klasyfikacja:** Standard wewnętrzny — obowiązujący

---

> **Instrukcja dla agenta:**  
> Niniejszy dokument jest obowiązkowym kontekstem dla każdej sesji generowania dokumentacji AOS.  
> Przed wyprodukowaniem jakiegokolwiek tekstu agent wczytuje i stosuje wszystkie reguły z tego dokumentu.  
> Priorytet: wytyczne językowe nadrzędne wobec własnych preferencji stylistycznych modelu.

---

## Spis treści

1. [Zasady nadrzędne](#1-zasady-nadrzędne)
2. [Ton i rejestr językowy](#2-ton-i-rejestr-językowy)
3. [Reguły gramatyczne i składniowe](#3-reguły-gramatyczne-i-składniowe)
4. [Reguły formatowania Markdown](#4-reguły-formatowania-markdown)
5. [Słownik terminologii — pojęcia techniczne](#5-słownik-terminologii--pojęcia-techniczne)
6. [Słownik terminologii — pojęcia biznesowe / domenowe](#6-słownik-terminologii--pojęcia-biznesowe--domenowe)
7. [Słownik terminologii — pojęcia procesowe](#7-słownik-terminologii--pojęcia-procesowe)
8. [Wyrażenia zakazane](#8-wyrażenia-zakazane)
9. [Wyrażenia wymagane — formuły standardowe](#9-wyrażenia-wymagane--formuły-standardowe)
10. [Reguły nazewnictwa elementów UI](#10-reguły-nazewnictwa-elementów-ui)
11. [Zasady opisu walidacji i reguł biznesowych](#11-zasady-opisu-walidacji-i-reguł-biznesowych)
12. [Zasady opisu operacji i przepływów](#12-zasady-opisu-operacji-i-przepływów)
13. [Zasady obsługi niepewności](#13-zasady-obsługi-niepewności)

---

## 1. Zasady nadrzędne

Poniższe zasady mają bezwzględne pierwszeństwo. Żadna reguła z dalszych sekcji ich nie uchyla.

### Z.1 — Precyzja ponad elegancję

Dokument AOS to specyfikacja techniczna, nie artykuł. Priorytetem jest jednoznaczność, nie styl literacki. Zdanie brzmiące technicznie i powtarzalne jest lepsze od zdania eleganckiego i wieloznacznego.

> ❌ `Pole przyjmuje wartości słownikowe związane z walutą transakcji.`  
> ✅ `Pole akceptuje wartości ze słownika Currency. Dozwolone wartości: RON, EUR, USD, GBP.`

### Z.2 — Dokument opisuje to co jest, nie co powinno być

Agent opisuje zachowanie zaimplementowane w kodzie. Nie interpretuje intencji dewelopera, nie sugeruje co "zapewne miało być". Jeśli kod zawiera błąd lub niespójność — agent to odnotowuje, nie "naprawia" opisem.

> ❌ `Pole prawdopodobnie powinno przyjmować tylko wartości dodatnie.`  
> ✅ `Pole nie posiada walidatora ograniczającego wartości do zakresu dodatniego. [WYMAGA WERYFIKACJI — czy brak walidacji jest celowy]`

### Z.3 — Jedno pojęcie, jedna nazwa — konsekwentnie przez cały dokument

Jeśli w sekcji 2 agent użył nazwy "dialog edycji klienta", ta sama nazwa obowiązuje w sekcjach 7, 10, 11. Zmiana nazwy tego samego obiektu w toku dokumentu jest błędem krytycznym.

### Z.4 — Dane techniczne zawsze w oryginalnym języku kodu (angielski)

Nazwy klas, metod, zmiennych, selektorów, endpointów — zawsze w oryginalnym brzmieniu z kodu, nigdy tłumaczone.

> ❌ `Kontroler nazwy produktu`  
> ✅ `formControlName: productName`

### Z.5 — Opis biznesowy zawsze po polsku

Warstwa opisowa (co dane pole znaczy dla użytkownika, jaki jest cel operacji, jaka reguła biznesowa obowiązuje) — zawsze po polsku.

---

## 2. Ton i rejestr językowy

### 2.1 Definicja tonu

Dokumentacja AOS jest **oficjalnym dokumentem projektowym**. Obowiązuje ton:

| Cecha | Opis | Przykład prawidłowy |
|---|---|---|
| **Formalny** | Brak kolokwializmów, skrótów myślowych, potocznych sformułowań | `Pole jest wymagane` nie `Pole trzeba wypełnić` |
| **Bezosobowy** | Bez pierwszej osoby liczby pojedynczej lub mnogiej | `Ekran wyświetla listę` nie `Widzimy listę` |
| **Rzeczowy** | Bez ozdobników, porównań literackich, metafor | `Pole przyjmuje tekst` nie `Pole służy do wpisania tekstu` |
| **Jednoznaczny** | Każde zdanie ma dokładnie jedno możliwe odczytanie | `Przycisk jest nieaktywny gdy formularz zawiera błędy walidacji` |
| **Zwięzły** | Minimalna liczba słów do przekazania pełnej informacji | `Pole opcjonalne` nie `Pole nie musi być wypełnione przez użytkownika` |

### 2.2 Forma gramatyczna opisów

Opisy stanu ekranu — **czas teraźniejszy, strona czynna**:

> ✅ `Ekran wyświetla listę klientów przypisanych do zalogowanego użytkownika.`  
> ❌ `Ekran będzie wyświetlał listę klientów.`  
> ❌ `Lista klientów jest wyświetlana przez ekran.`

Opisy operacji — **bezokolicznik lub strona czynna**:

> ✅ `Przycisk wywołuje dialog edycji wybranego rekordu.`  
> ✅ `Kliknięcie przycisku wywołuje operację DELETE na wybranym rekordzie.`  
> ❌ `Po kliknięciu przycisku powinien otworzyć się dialog.`

Opisy walidacji — **strona czynna, czas teraźniejszy**:

> ✅ `Walidator blokuje zapis gdy pole jest puste.`  
> ❌ `Pole nie może być puste.`  
> ❌ `Pole powinno być wypełnione.`

### 2.3 Podmiot wypowiedzi

W opisach elementów UI podmiotem jest zawsze **element, nie użytkownik**:

> ✅ `Pole akceptuje wyłącznie wartości numeryczne.`  
> ❌ `Użytkownik wpisuje wartości numeryczne.`

> ✅ `Przycisk wywołuje operację zapisu formularza.`  
> ❌ `Użytkownik klika przycisk aby zapisać formularz.`

Wyjątek: sekcja Scenariusze testowe (11) — tu podmiotem jest tester:

> ✅ `Tester wpisuje wartość "test@example.com" w pole Email.`

---

## 3. Reguły gramatyczne i składniowe

### 3.1 Długość zdania

- Zdanie opisowe: maksymalnie 30 słów.
- Zdanie techniczne (z danymi z kodu): bez limitu długości, ale jedna informacja = jedno zdanie.
- Zakaz: zdań wielokrotnie złożonych w opisach stanu i walidacji.

> ❌ `Pole jest wymagane i akceptuje tylko cyfry, a wartość musi mieścić się w zakresie 1–100, przy czym w przypadku przekroczenia wartości maksymalnej wyświetlany jest komunikat błędu.`

> ✅ `Pole jest wymagane. Pole akceptuje wyłącznie wartości numeryczne całkowite. Dozwolony zakres: 1–100. Przekroczenie zakresu wywołuje komunikat: "Wartość musi mieścić się w przedziale 1–100."`

### 3.2 Użycie nawiasów

Nawiasy okrągłe `()` — wyłącznie dla danych technicznych uzupełniających opis:

> ✅ `Pole Waluta (formControlName: currency) wyświetla wartości ze słownika Currency.`

Nawiasy kwadratowe `[]` — wyłącznie dla markerów stanu dokumentu:

> ✅ `[WYMAGA WERYFIKACJI]`, `[BRAK W KODZIE]`, `[DO UZUPEŁNIENIA]`

### 3.3 Spójniki

Zakaz spójnika `oraz` w połączeniu z opisem niezwiązanych ze sobą cech:

> ❌ `Pole jest wymagane oraz wyświetla wartości słownikowe.`  
> ✅ `Pole jest wymagane. Pole wyświetla wartości ze słownika [nazwa_słownika].`

Spójnik `i` dopuszczalny wyłącznie dla cech logicznie powiązanych:

> ✅ `Pole jest niewidoczne i niedostępne gdy użytkownik nie ma roli Administrator.`

### 3.4 Skróty

Dozwolone skróty:

| Skrót | Pełna forma | Kontekst użycia |
|---|---|---|
| `N/D` | Nie dotyczy | Komórki tabeli gdy sekcja nie ma zastosowania |
| `AOS` | Analityczny Opis Systemu | Po pierwszym pełnym użyciu w dokumencie |
| `UI` | User Interface | Opisy warstwy prezentacji |
| `API` | Application Programming Interface | Opisy integracji |
| `CRUD` | Create, Read, Update, Delete | Opisy operacji na danych |
| `JWT` | JSON Web Token | Opisy autoryzacji |
| `HTTP` | Hypertext Transfer Protocol | Nazwy metod zapytań |

Zakaz własnych skrótów tworzonych przez agenta bez wcześniejszego zdefiniowania w dokumencie.

---

## 4. Reguły formatowania Markdown

### 4.1 Hierarchia nagłówków

```
# Tytuł dokumentu (jeden na cały dokument)
## Sekcja główna (numerowane: 1, 2, 3...)
### Podsekcja (numerowane: 1.1, 1.2...)
#### Element szczegółowy (np. "#### Pole: firmName")
```

Zakaz przeskakiwania poziomów (`##` → `####` bez `###` pośredniego).

### 4.2 Tabele

Każda tabela musi posiadać:
- Nagłówek z nazwami kolumn
- Wyrównanie kolumn (spacje w Markdown dla czytelności kodu źródłowego)
- Wartość `N/D` zamiast pustej komórki

Zakaz tabel z więcej niż 8 kolumnami — podziel na dwie tabele tematyczne.

### 4.3 Kod i wartości techniczne

Wszystkie wartości techniczne wrapowane w backticki `` ` ``:

> ✅ `formControlName: \`productName\``  
> ✅ `Endpoint: \`GET /api/products\``  
> ✅ `Walidator: \`Validators.required\``

Bloki kodu (wieloliniowe) — fenced code blocks z oznaczeniem języka:

````
```typescript
this.productForm = this.fb.group({
  name: ['', Validators.required]
});
```
````

### 4.4 Pogrubienie i kursywa

**Pogrubienie** (`**tekst**`) — wyłącznie dla:
- Nazw sekcji w tekście ciągłym
- Kluczowych wartości w opisach reguł

*Kursywa* (`*tekst*`) — wyłącznie dla:
- Pierwszego użycia terminu ze słownika
- Tytułów dokumentów zewnętrznych

Zakaz pogrubienia dla efektu estetycznego.

### 4.5 Listy

Listy punktowane (`-`) — dla zestawień bez kolejności.  
Listy numerowane (`1.`) — wyłącznie dla kroków procesu lub procedur.

Zakaz tworzenia list jednoelementowych — użyj zdania.

### 4.6 Cytaty blokowe

`>` — wyłącznie dla:
- Komunikatów wyświetlanych użytkownikowi (tekst UI)
- Ważnych uwag i zastrzeżeń
- Przykładów wartości

> ✅ Komunikat błędu: `"Pole Nazwa firmy jest wymagane."`

---

## 5. Słownik terminologii — pojęcia techniczne

Poniższy słownik definiuje jedyną dopuszczalną nazwę dla każdego pojęcia. Synonimy i zamienniki wymienione w kolumnie "Nazwy zakazane" są niedopuszczalne w dokumentacji AOS.

### 5.1 Pojęcia warstwy UI

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **ekran** | Pojedynczy widok Angular ładowany przez Router na podstawie ścieżki URL. Jeden ekran = jeden route = jeden dokument AOS. | widok, strona, formatka, okno główne, panel, zakładka (gdy nie chodzi o tab) |
| **komponent** | Klasa Angular składająca się z pliku `.component.ts`, `.component.html` i `.component.scss`. Jednostka strukturalna ekranu. | element, moduł (gdy nie chodzi o NgModule), blok |
| **pole** | Pojedynczy element formularza umożliwiający wprowadzenie lub wyświetlenie jednej wartości. Posiada `formControlName` lub `[(ngModel)]`. | input, kontrolka, widget, box |
| **pole wymagane** | Pole posiadające walidator `Validators.required`. | pole obowiązkowe, pole niezbędne, pole konieczne |
| **pole opcjonalne** | Pole nieposiadające walidatora `Validators.required`. | pole nieobowiązkowe, pole dowolne, pole do wyboru |
| **grid** | Komponent tabelaryczny Angular Material (`<mat-table>`) wyświetlający wiele rekordów danych w wierszach i kolumnach. | tabela, lista tabelaryczna, zestawienie (gdy chodzi o `mat-table`), datagrид |
| **kolumna** | Pionowy zestaw danych w gridzie, definiowany przez `matColumnDef`. | pole tabeli, komórka (gdy nie chodzi o konkretną komórkę), pole gridu |
| **wiersz** | Poziomy zestaw wartości w gridzie odpowiadający jednemu rekordowi danych. | pozycja, wpis, linia, element listy |
| **dialog** | Okno modalne Angular Material (`MatDialog`) otwierane nad widokiem głównym. Posiada własny komponent. | popup, modal, okno dialogowe, okienko, overlay |
| **formularz** | Grupa pól powiązanych w `FormGroup` Angular Reactive Forms lub Template-Driven Forms. | formatka, forma |
| **formularz reaktywny** | Formularz implementowany przez `ReactiveFormsModule` i `FormBuilder`. | reactive form (ang.), formularz reaktywny |
| **sekcja filtrów** | Wyodrębniona część ekranu zawierająca pola służące do zawężania danych wyświetlanych w gridzie. Pola filtrów nie zapisują danych. | pasek wyszukiwania (gdy chodzi o całą sekcję), panel filtrów, search bar |
| **pasek tytułu** | Poziomy element UI zawierający tytuł ekranu i główne przyciski operacyjne (np. `+ New Invoice`). | toolbar, header (gdy nie chodzi o `<header>` HTML), nagłówek ekranu |
| **menu kontekstowe** | Lista opcji rozwijana po kliknięciu ikony `⋮` lub prawym przyciskiem myszy. Angular Material: `<mat-menu>`. | dropdown menu (gdy chodzi o menu akcji), context menu (ang.) |
| **paginacja** | Mechanizm podziału dużych zbiorów danych na strony. Angular Material: `<mat-paginator>`. | stronicowanie, paging |
| **sortowanie** | Mechanizm porządkowania wierszy gridu po wartości kolumny. Angular Material: `matSort`. | ordering, filtrowanie (to jest odrębne pojęcie) |
| **interceptor** | Klasa Angular implementująca `HttpInterceptor` — modyfikuje każde żądanie HTTP lub odpowiedź. | middleware (gdy chodzi o interceptor Angular HTTP), wrapper |
| **guard** | Klasa Angular implementująca `CanActivate` lub analogiczne interfejsy — kontroluje dostęp do trasy. | strażnik, auth check (gdy chodzi o guard) |
| **serwis** | Klasa Angular z dekoratorem `@Injectable()` dostarczająca logikę biznesową i wywołania HTTP. | service (ang. w opisach biznesowych), provider |
| **model danych** | Interfejs TypeScript (`interface I<Nazwa>`) definiujący strukturę obiektu danych. | typ, klasa modelu (gdy chodzi o interfejs TS), schema (gdy nie chodzi o DB) |
| **endpoint** | Ścieżka URL API wraz z metodą HTTP (np. `GET /api/clients`). | adres API, URL serwisu, route API, akcja kontrolera |
| **słownik** | Zamknięty, predefiniowany zestaw dopuszczalnych wartości dla pola. | lista wartości, enum (gdy nie chodzi o typ TypeScript), dropdown values |
| **walidator** | Funkcja Angular (`Validators.*`) sprawdzająca poprawność wartości pola formularza. | reguła walidacji (termin nadrzędny jest OK), constraint |
| **binding** | Mechanizm powiązania właściwości komponentu z elementem HTML (`[(ngModel)]`, `[formControl]`). | powiązanie danych, data binding (ang. w opisach biznesowych) |
| **token JWT** | Zakodowany ciąg tekstowy służący do autoryzacji żądań HTTP, generowany przez serwer po zalogowaniu. | token autoryzacyjny (dopuszczalne jako synonim), bearer token |

### 5.2 Metody HTTP

| Termin obowiązujący | Zastosowanie | Nazwy zakazane |
|---|---|---|
| `GET` | Pobieranie danych (bez modyfikacji zasobu) | pobierz, odczytaj, wczytaj |
| `POST` | Tworzenie nowego zasobu | utwórz, dodaj, zapisz (gdy chodzi o metodę HTTP) |
| `PUT` | Zastąpienie istniejącego zasobu (pełna aktualizacja) | zaktualizuj (gdy chodzi o metodę HTTP) |
| `PATCH` | Częściowa aktualizacja istniejącego zasobu | edytuj (gdy chodzi o metodę HTTP) |
| `DELETE` | Usunięcie zasobu | usuń (gdy chodzi o metodę HTTP) |

> Metody HTTP zawsze zapisywane **wersalikami** bez cudzysłowu w kontekście technicznym.

---

## 6. Słownik terminologii — pojęcia biznesowe / domenowe

Poniższe pojęcia mają ściśle określone znaczenie w kontekście dokumentowanej aplikacji. Agent stosuje wyłącznie zdefiniowane tu nazwy.

### 6.1 Pojęcia domenowe InvoiceJet

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **dokument** | Ogólna nazwa dla faktury, faktury proforma lub faktury storno wytworzonych w systemie. Odpowiada encji `Document` w bazie. | pismo, zapis finansowy |
| **faktura** | Dokument sprzedaży (typ: Factura). | invoice (w opisach biznesowych po polsku) |
| **faktura proforma** | Dokument pro forma (typ: Factura Proforma) — nie jest dokumentem księgowym. | proforma (bez słowa "faktura"), oferta |
| **faktura storno** | Dokument korygujący fakturę (typ: Factura Storno). | korekta faktury, storno (bez słowa "faktura" w kontekście typu dokumentu) |
| **klient** | Firma zarejestrowana w systemie jako odbiorca dokumentów. Odpowiada encji `Firm` z flagą `IsClient = true`. | kontrahent (w opisach UI), odbiorca (gdy nie chodzi o pole na dokumencie), nabywca |
| **firma użytkownika** | Firma zalogowanego użytkownika — wystawca dokumentów. Odpowiada encji `Firm` z flagą `IsClient = false` lub encji powiązanej z `UserFirm`. | moja firma, firma własna |
| **seria dokumentów** | Ciąg numeracyjny przypisany do typu dokumentu, definiujący schemat numerowania (np. `2024/001`). Odpowiada encji `DocumentSeries`. | seria faktur, numeracja, schemat numerowania |
| **numer dokumentu** | Unikalny identyfikator dokumentu wygenerowany zgodnie z serią (np. `20240007`). | numer faktury (chyba że mowa o konkretnym typie dokumentu), ID dokumentu |
| **konto bankowe** | Rachunek bankowy przypisany do firmy użytkownika, używany na dokumentach. Odpowiada encji `BankAccount`. | rachunek, konto |
| **waluta** | Oznaczenie waluty rachunku bankowego lub dokumentu. Wartości ze słownika `Currency`. | currency (w opisach biznesowych po polsku) |
| **TVA** | Podatek od wartości dodanej (rumuski VAT). Wartość procentowa (np. 19%). | VAT (w kontekście tej aplikacji), podatek ogólnie |
| **CUI** | Numer identyfikacji podatkowej firmy w Rumunii (*Codul Unic de Identificare*). | NIP (to jest polski odpowiednik — nie stosować zamiennie), numer podatkowy |
| **RegCom** | Numer rejestracji firmy w rejestrze handlowym. | KRS (to jest polski odpowiednik — nie stosować), numer rejestrowy |
| **ANAF** | Zewnętrzna usługa API rumuńskiej administracji podatkowej, używana do pobierania danych firmy na podstawie CUI. | zewnętrzne API (gdy można użyć pełnej nazwy ANAF), serwis podatkowy |
| **status dokumentu** | Stan realizacji dokumentu. Wartości: `Unpaid`, `Paid`. Odpowiada encji `DocumentStatus`. | stan faktury, status płatności (gdy mowa o statusie dokumentu jako całości) |
| **produkt** | Pozycja cennikowa zdefiniowana w systemie, dodawana do dokumentów. Odpowiada encji `Product`. | usługa (chyba że kontekst jednoznacznie wskazuje na usługę), towar, artykuł |
| **pozycja dokumentu** | Pojedynczy wiersz produktu na dokumencie z ilością, ceną i TVA. Odpowiada encji `DocumentProduct`. | linia dokumentu, pozycja faktury (chyba że mowa o fakturze) |

### 6.2 Pojęcia operacyjne UI (dla wszystkich ekranów)

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **dodanie rekordu** | Operacja tworzenia nowego wpisu w bazie danych (dialog Add lub formularz tworzenia). | dodanie wpisu, wstawienie, zapis nowego |
| **edycja rekordu** | Operacja modyfikacji istniejącego wpisu w bazie danych (dialog Edit lub formularz edycji). | zmiana, aktualizacja (gdy mowa o operacji UI), modyfikacja wpisu |
| **usunięcie rekordu** | Operacja trwałego usunięcia wpisu z bazy danych. | kasowanie, wymazanie, skasowanie |
| **zapis formularza** | Operacja walidacji formularza i wysłania danych do API (POST lub PUT). | submit, wysłanie, potwierdzenie |
| **anulowanie operacji** | Zamknięcie dialogu lub formularza bez wysyłania danych do API. | rezygnacja, cofnięcie, odrzucenie |
| **odświeżenie listy** | Ponowne pobranie danych z API i renderowanie gridu z aktualnymi danymi. | reload, przeładowanie, aktualizacja widoku |
| **zaznaczenie wiersza** | Aktywacja checkboxa przy wierszu gridu w celu wskazania rekordów do operacji zbiorczej. | selekcja, wybór, oznaczenie |
| **komunikat sukcesu** | Powiadomienie `MatSnackBar` potwierdzające pomyślne wykonanie operacji. | alert sukcesu, notyfikacja, toast (ang.) |
| **komunikat błędu** | Powiadomienie `MatSnackBar` lub komunikat `mat-error` informujący o niepowodzeniu operacji lub błędzie walidacji. | alert błędu, error message (ang. w opisach biznesowych) |

---

## 7. Słownik terminologii — pojęcia procesowe

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **dokument AOS** | Analityczny Opis Systemu — ustandaryzowany dokument opisujący jeden ekran aplikacji. | dokumentacja ekranu, spec, specyfikacja (gdy mowa o AOS), opis funkcjonalny |
| **szablon AOS** | Plik `AOS_FRONTEND_TEMPLATE.md` definiujący strukturę dokumentu AOS. | template (ang.), wzorzec dokumentu |
| **skill** | Plik `SKILL.md` zawierający instrukcje sterujące zachowaniem agenta. | prompt systemowy (gdy mowa o skilu), instrukcja agenta |
| **agent** | Instancja modelu LLM (Claude) z załadowanym skillem, prowadząca sesję dokumentowania. | model, Claude (gdy mowa o roli w procesie), AI, bot |
| **sesja dokumentowania** | Pojedyncza rozmowa z agentem poświęcona udokumentowaniu jednego ekranu. | sesja AI, uruchomienie agenta |
| **weryfikacja analityczna** | Etap A procesu weryfikacji — porównanie dokumentu AOS z działającą aplikacją przez analityka. | review, przegląd dokumentu |
| **weryfikacja techniczna** | Etap B procesu weryfikacji — uzupełnienie danych technicznych przez dewelopera. | tech review, przegląd kodu |
| **rejestr ekranów** | Arkusz lub plik Markdown zawierający listę wszystkich ekranów aplikacji ze statusami dokumentacji. | backlog dokumentacji, lista ekranów |
| **pakiet plików** | Zestaw plików kodu przekazywanych agentowi jako kontekst dla jednej sesji dokumentowania. | kontekst agenta, input agenta |
| **primer systemu** | Dokument opisujący stos technologiczny i architekturę aplikacji — wczytywany jako kontekst inicjalny. | dokument architektury (gdy mowa o primerze), system overview |

---

## 8. Wyrażenia zakazane

Poniższe zwroty i formaty są bezwzględnie niedopuszczalne w treści dokumentacji AOS.

### 8.1 Wyrażenia sugerujące niepewność agenta (bez użycia markera `[WYMAGA WERYFIKACJI]`)

| Wyrażenie zakazane | Powód | Zamiast użyj |
|---|---|---|
| `prawdopodobnie`, `najprawdopodobniej` | Sugeruje domysł bez oznaczenia | `[WYMAGA WERYFIKACJI]` |
| `wydaje się`, `zdaje się` | Sugeruje domysł | `[WYMAGA WERYFIKACJI]` |
| `zakładam że`, `można założyć że` | Domysł bez podstawy w kodzie | `[WYMAGA WERYFIKACJI]` |
| `powinno`, `powinien` | Sugeruje oczekiwane, nie rzeczywiste zachowanie | Opisz co jest w kodzie lub `[WYMAGA WERYFIKACJI]` |
| `być może`, `możliwe że` | Sugeruje domysł | `[WYMAGA WERYFIKACJI]` |
| `sugeruję`, `polecam`, `warto` | Rekomendacje nie są częścią AOS | Usuń — AOS opisuje, nie rekomenduje |
| `typowo`, `standardowo`, `zazwyczaj` | Opis ogólny zamiast konkretnego | Opisz dokładne zachowanie z kodu |

### 8.2 Wyrażenia kolokwialne i nieprofesjonalne

| Wyrażenie zakazane | Zamiast użyj |
|---|---|
| `klikamy`, `klikamy w` | `użytkownik klika` / `kliknięcie przycisku` |
| `wpisujemy`, `wpisujemy tu` | `pole przyjmuje`, `użytkownik wpisuje` |
| `otwiera się okienko` | `otwierany jest dialog [nazwa]` |
| `coś takiego jak`, `coś w stylu` | Podaj konkretną nazwę lub `[WYMAGA WERYFIKACJI]` |
| `i tak dalej`, `itd.`, `itp.` | Wylistuj wszystkie wartości lub opisz regułę kompletnie |
| `etc.` | j.w. |
| `no i` | Usuń — zdanie zaczyna kolejne myślą |
| `generalnie`, `w zasadzie` | Usuń lub podaj konkretne sformułowanie |
| `dość`, `całkiem`, `raczej` | Usuń — przymiotniki intensywności nie mają miejsca w dokumentacji technicznej |

### 8.3 Wyrażenia niejednoznaczne kontekstowo

| Wyrażenie zakazane | Problem | Zamiast użyj |
|---|---|---|
| `system` (bez kontekstu) | Nie wiadomo co oznacza: aplikacja, backend, baza, całość | Podaj konkretnie: `aplikacja frontendowa`, `API`, `baza danych` |
| `dane` (bez kontekstu) | Niejasne — jakie dane? | `dane klienta`, `rekordy gridu`, `wartości formularza` |
| `obsługuje` (np. "serwis obsługuje X") | Wieloznaczne — przetwarza? wyświetla? waliduje? | Opisz konkretną operację: `wywołuje`, `waliduje`, `przekazuje` |
| `strona` | Może oznaczać: stronę HTML, stronę wyników, stronę paginacji | Użyj `ekran`, `strona wyników paginacji`, `strona HTML` |
| `wartość` (bez kontekstu) | Zbyt ogólne | `wartość pola [nazwa]`, `wartość parametru`, `wartość z odpowiedzi API` |
| `akcja` | Może oznaczać: przycisk, event, akcję kontrolera, Redux action | Użyj `operacja`, `zdarzenie`, `endpoint`, konkretnie w kontekście |
| `moduł` | Angular NgModule vs. moduł biznesowy vs. moduł systemu | `moduł Angular [nazwa]`, `sekcja biznesowa [nazwa]` |

### 8.4 Wyrażenia z języka angielskiego (w opisach biznesowych)

Zakaz stosowania angielskich terminów technicznych w opisach biznesowych (gdzie obowiązuje język polski):

| Wyrażenie zakazane | Zamiast użyj |
|---|---|
| `submit` (w opisie operacji) | `zapis formularza`, `wysłanie danych` |
| `save` (w opisie operacji) | `zapis`, `zapisanie rekordu` |
| `delete` (w opisie operacji) | `usunięcie rekordu` |
| `dropdown` (w opisie pola) | `lista rozwijana` |
| `checkbox` (w opisie pola) | `pole wyboru` |
| `button` (w opisie elementu) | `przycisk` |
| `placeholder` (w opisie pola) | `tekst podpowiedzi` |
| `label` (w opisie pola) | `etykieta pola` |
| `tooltip` (w opisie pola) | `dymek podpowiedzi` |
| `breadcrumb` | `ścieżka nawigacyjna` |
| `loading` (w opisie stanu) | `stan ładowania` |

> Wyjątek: wartości techniczne (`formControlName`, `matColumnDef`, nazwy serwisów, endpointy) — zawsze w oryginalnym języku angielskim, wrapowane w backticki.

---

## 9. Wyrażenia wymagane — formuły standardowe

Poniższe frazy są obowiązkowe w określonych sytuacjach. Agent stosuje je dosłownie.

### 9.1 Markery stanu dokumentu

| Sytuacja | Wymagana formuła |
|---|---|
| Wartość nie może być ustalona z dostępnych plików | `[WYMAGA WERYFIKACJI]` |
| Element istnieje w aplikacji ale nie ma go w przekazanym kodzie | `[BRAK W DOSTARCZONYCH PLIKACH — WYMAGA WERYFIKACJI]` |
| Element opisany na podstawie screenshotu, bez potwierdzenia z kodu | `[NA PODSTAWIE SCREENSHOTU — WYMAGA POTWIERDZENIA Z KODU]` |
| Wartość znana ale wymaga uzupełnienia przez konkretną osobę | `[DO UZUPEŁNIENIA PRZEZ: DEWELOPER / ANALITYK]` |
| Sekcja szablonu nieobowiązująca dla danego ekranu | `> Sekcja nie dotyczy tego ekranu. [powód jednym zdaniem]` |

### 9.2 Formuły opisu pól — wartości obowiązkowe

Kiedy pole posiada walidator `required`:
> `Pole jest wymagane.`

Kiedy pole jest opcjonalne:
> `Pole jest opcjonalne.`

Kiedy pole jest tylko do odczytu:
> `Pole jest niedostępne do edycji. Wartość prezentowana tylko do odczytu.`

Kiedy pole jest ukryte warunkowo:
> `Pole jest widoczne wyłącznie gdy [warunek z kodu, np. tryb edycji jest aktywny].`

Kiedy pole jest dezaktywowane warunkowo:
> `Pole jest niedostępne gdy [warunek z kodu].`

### 9.3 Formuły opisu operacji

Kiedy operacja wywołuje dialog:
> `Operacja otwiera dialog [Nazwa Dialogu].`

Kiedy operacja wywołuje API:
> `Operacja wywołuje [HTTP_METHOD] [endpoint]. Po pomyślnym wykonaniu: [opis]. W przypadku błędu: [opis].`

Kiedy operacja nawiguje do innego ekranu:
> `Operacja przekierowuje użytkownika do ekranu [nazwa ekranu] (URL: [ścieżka]).`

Kiedy operacja jest dezaktywowana:
> `Przycisk jest nieaktywny gdy [warunek].`

### 9.4 Formuły opisu walidacji

Dla walidatora `required`:
> `Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "[tekst mat-error]".`

Dla walidatora `minLength`:
> `Minimalna długość wartości: [n] znaków.`

Dla walidatora `maxLength`:
> `Maksymalna długość wartości: [n] znaków.`

Dla walidatora `pattern`:
> `Pole akceptuje wyłącznie wartości zgodne z wzorcem: \`[regex]\`. [Opcjonalnie: opis wzorca słowami].`

Dla walidatora `email`:
> `Pole akceptuje wyłącznie adresy e-mail w formacie [lokalna-część]@[domena].[TLD].`

Dla walidatora `min`/`max`:
> `Dozwolony zakres wartości: [min]–[max].`

---

## 10. Reguły nazewnictwa elementów UI

### 10.1 Konwencja nazw elementów w dokumencie

Każdy element UI opisywany w dokumencie AOS musi być identyfikowany przez nazwę złożoną z:

`[Typ elementu] [Nazwa biznesowa]`

Przykłady:

| Poprawna nazwa w dokumencie | Błędna nazwa |
|---|---|
| Pole Nazwa firmy | Nazwa firmy, pole firmName, input nazwy |
| Przycisk Nowy klient | Dodaj klienta, + New Client, btn-add |
| Dialog Edycja klienta | Edycja, okno edycji, modal edycji |
| Grid Listy klientów | Tabela klientów, lista, grid |
| Kolumna Nazwa firmy | Name, kolumna 1, Firma |

### 10.2 Nazwy dialogów

Format: `[Typ operacji] + [Nazwa obiektu]`

| Poprawna nazwa | Błędna nazwa |
|---|---|
| Dialog Dodawanie klienta | Dialog AddClient, Popup klienta |
| Dialog Edycja klienta | Dialog edycji, Edit Client dialog |
| Dialog Dodawanie/Edycja klienta | Dialog CRUD klienta, AddEditClientDialog (ang.) |

### 10.3 Nazwy operacji (przycisków)

Format: `[Rzeczownik odsłowny] + [Obiekt]`

| Poprawna nazwa | Błędna nazwa |
|---|---|
| Dodawanie klienta | Dodaj klienta, Add Client, Nowy klient |
| Edycja klienta | Edytuj klienta, Edit, Zmień |
| Usuwanie zaznaczonych | Usuń zaznaczone, Delete selected, Kasowanie |
| Zapis formularza | Zapisz, Submit, Zatwierdź |
| Anulowanie operacji | Anuluj, Cancel, Wróć |

> Uwaga: Nazwy na przyciskach w aplikacji (np. "New Client", "Update") mogą różnić się od nazw operacji w dokumencie AOS — to dopuszczalne. W dokumencie używamy polskich nazw operacji; oryginalne etykiety UI podajemy w polu "Typ elementu".

---

## 11. Zasady opisu walidacji i reguł biznesowych

### 11.1 Hierarchia walidacji

Dokumentacja AOS rozróżnia trzy poziomy walidacji — każdy opisywany oddzielnie:

| Poziom | Źródło | Moment wywołania | Gdzie dokumentować |
|---|---|---|---|
| **Walidacja frontendowa — polowa** | `Validators.*` w `FormGroup` | Przy opuszczeniu pola lub próbie zapisu | Sekcja 4 (Pola) — tabela pola |
| **Walidacja frontendowa — formularzowa** | Stan `FormGroup.valid` przed wysłaniem | Przy próbie zapisu całego formularza | Sekcja 6 (Operacje) — szczegóły operacji zapisu |
| **Walidacja backendowa** | Odpowiedź HTTP 400 z API | Po wysłaniu żądania do serwera | Sekcja 8 (Powiadomienia) — błędy |

### 11.2 Opis walidacji polowej

Każda walidacja opisywana jest przez trzy elementy:

1. **Warunek** — kiedy walidacja jest naruszona (co wpisano lub czego nie wpisano)
2. **Skutek** — co dzieje się w UI (zablokowanie zapisu, komunikat inline)
3. **Treść komunikatu** — dokładny tekst `mat-error` z HTML

Przykład prawidłowego opisu:

> Pole Waluta jest wymagane. Brak wartości blokuje zapis formularza. Pole wyświetla komunikat błędu: `"Câmpul este obligatoriu"` (wyświetlany po opuszczeniu pustego pola).

### 11.3 Reguły biznesowe (logika specjalna)

Jeśli pole posiada logikę wykraczającą poza standardowe walidatory (np. autouzupełnianie, warunkowe blokowanie, kaskadowe zależności między polami), dokumentowana jest jako **Logika specjalna** w tabeli pola:

Format opisu logiki specjalnej:

> `[Wyzwalacz]: [Zdarzenie]. Skutek: [co dzieje się z polami / danymi]. Wywołuje: [metoda serwisu / endpoint jeśli dotyczy].`

Przykład:

> Wpisanie wartości w pole CUI i kliknięcie przycisku Pobierz dane z ANAF: wywołuje `firmService.getFirmByCui(cui)`. Skutek: pola Nazwa firmy, RegCom, Adres, Województwo, Miasto są autouzupełniane wartościami z odpowiedzi API. Pola pozostają edytowalne po autouzupełnieniu.

---

## 12. Zasady opisu operacji i przepływów

### 12.1 Struktura opisu operacji

Każda operacja opisywana jest przez następujące elementy w ustalonej kolejności:

1. Typ operacji (nawigacja / dialog / API call / walidacja + API call / eksport)
2. Warunek dostępności (zawsze aktywna / warunkowo dezaktywowana)
3. Pre-walidacja (czy formularz musi być valid)
4. Wywołanie API (jeśli dotyczy): metoda HTTP + endpoint + parametry
5. Obsługa sukcesu: co dzieje się po pomyślnym wykonaniu
6. Obsługa błędu: co dzieje się przy błędzie

### 12.2 Opis przepływu danych

Przepływ danych w ramach operacji opisywany jest w kierunku:

`Źródło danych → Transformacja → Cel`

Przykład:

> Wartości pól formularza reaktywnego `clientForm` są serializowane do obiektu `IFirm` i przekazywane jako body żądania `PUT /api/firms/{id}`. Identyfikator `id` pochodzi z parametru `data.client.id` przekazanego do dialogu przy otwarciu.

### 12.3 Zakaz opisywania implementacji backendu

Dokumentacja AOS opisuje wyłącznie to, co jest widoczne lub wywołane z poziomu frontendu:

> ❌ `API aktualizuje rekord w tabeli Firm i zwraca zaktualizowany obiekt.`  
> ✅ `Operacja wywołuje \`PUT /api/firms/{id}\`. Odpowiedź API: typ \`IFirm\` (obiekt zaktualizowanego rekordu).`

---

*Dokument obowiązuje od wersji 1.0. Wszelkie odstępstwa wymagają zatwierdzonej zmiany w tym pliku, nie w dokumentach AOS poszczególnych ekranów.*
