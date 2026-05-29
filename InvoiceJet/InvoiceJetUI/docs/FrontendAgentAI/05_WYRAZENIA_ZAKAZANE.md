# Wyrażenia zakazane
## Wytyczne językowe AOS — Część 5 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Zasada:** Żadne z poniższych wyrażeń nie może pojawić się w treści dokumentu AOS. Zakaz bezwzględny.

---

## 1. Wyrażenia sugerujące niepewność — bez użycia markera

Kiedy agent nie może ustalić wartości z kodu — **nie zgaduje i nie sugeruje**. Stosuje marker `[WYMAGA WERYFIKACJI]`.

| Wyrażenie zakazane | Powód | Prawidłowe zastąpienie |
|---|---|---|
| `prawdopodobnie`, `najprawdopodobniej` | Domysł bez podstawy w kodzie | `[WYMAGA WERYFIKACJI]` |
| `wydaje się`, `zdaje się` | Domysł | `[WYMAGA WERYFIKACJI]` |
| `zakładam że`, `można założyć że` | Domysł agenta — niedopuszczalny | `[WYMAGA WERYFIKACJI]` |
| `powinno`, `powinien` (w opisie zachowania) | Opisuje oczekiwane, nie rzeczywiste | Opisz co jest w kodzie lub `[WYMAGA WERYFIKACJI]` |
| `być może`, `możliwe że` | Domysł | `[WYMAGA WERYFIKACJI]` |
| `mogłoby`, `mogłaby` | Domysł | `[WYMAGA WERYFIKACJI]` |
| `typowo`, `standardowo`, `zazwyczaj` | Opis ogólny zamiast konkretnego z kodu | Opisz dokładne zachowanie z kodu |
| `w teorii`, `w praktyce` | Niespójność z zasadą Z.2 | Opisz jedno konkretne zachowanie z kodu |

---

## 2. Wyrażenia kolokwialne i nieprofesjonalne

| Wyrażenie zakazane | Prawidłowe zastąpienie |
|---|---|
| `klikamy`, `klikamy w`, `klikniemy` | `użytkownik klika` / `kliknięcie przycisku` |
| `wpisujemy`, `wpisujemy tu` | `pole przyjmuje` / `użytkownik wpisuje` |
| `otwiera się okienko` | `otwierany jest dialog [Nazwa dialogu]` |
| `coś takiego jak`, `coś w stylu` | Podaj konkretną nazwę lub `[WYMAGA WERYFIKACJI]` |
| `i tak dalej`, `itd.`, `itp.` | Wylistuj wszystkie wartości lub opisz regułę kompletnie |
| `etc.`, `i inne` | j.w. |
| `no i` (na początku zdania) | Usuń — zdanie zaczyna nową myśl samodzielnie |
| `generalnie`, `w zasadzie` | Usuń lub podaj konkretne sformułowanie |
| `dość`, `całkiem`, `raczej` (przymiotniki intensywności) | Usuń — przymiotniki stopnia nie mają miejsca w spec. technicznej |
| `trochę`, `nieco` | Usuń |
| `oczywiście`, `naturalnie` | Usuń — nie dodają informacji |
| `warto zauważyć`, `warto wspomnieć` | Usuń — jeśli informacja jest ważna, napisz ją wprost |
| `jak widać`, `jak wspomniano` | Usuń |
| `itd.` | Wylistuj lub opisz regułę |

---

## 3. Wyrażenia niejednoznaczne kontekstowo

Poniższe słowa są dopuszczalne **tylko z dookreśleniem**. Użycie bez kontekstu jest błędem.

| Wyrażenie zakazane (bez kontekstu) | Problem | Prawidłowe zastąpienie |
|---|---|---|
| `system` | Nieясne co oznacza: aplikacja, backend, baza, całość | `aplikacja frontendowa`, `API`, `baza danych`, `system InvoiceJet` |
| `dane` | Niejasne — jakie dane? | `dane klienta`, `rekordy gridu`, `wartości formularza`, `odpowiedź API` |
| `obsługuje` (np. "serwis obsługuje X") | Wieloznaczne — przetwarza? wyświetla? waliduje? | Opisz konkretną operację: `wywołuje`, `waliduje`, `przekazuje`, `renderuje` |
| `strona` | Może oznaczać: stronę HTML, stronę wyników, stronę paginacji | `ekran`, `strona wyników paginacji`, `strona HTML` |
| `wartość` (bez kontekstu) | Zbyt ogólne | `wartość pola [nazwa]`, `wartość parametru`, `wartość z odpowiedzi API` |
| `akcja` | Może oznaczać: przycisk, event, akcję kontrolera | `operacja`, `zdarzenie`, `endpoint` — konkretnie |
| `moduł` | Angular NgModule vs moduł biznesowy vs moduł systemu | `moduł Angular [nazwa]`, `sekcja biznesowa [nazwa]` |
| `komponent` (bez nazwy) | Nie wiadomo który | Zawsze podaj pełną nazwę: `komponent ClientsComponent` |
| `formularz` (bez nazwy) | Nie wiadomo który | `formularz reaktywny \`clientForm\`` lub `formularz dialogu Edycja klienta` |
| `przycisk` (bez nazwy) | Nie wiadomo który | `Przycisk Dodawanie klienta`, `Przycisk Zapis formularza` |

---

## 4. Anglicyzmy w opisach biznesowych

W opisach biznesowych (co pole znaczy, co operacja robi) obowiązuje język polski. Poniższe angielskie terminy są zakazane w warstwach opisowych — dopuszczalne wyłącznie jako wartości techniczne w backtickach.

| Wyrażenie zakazane (w opisach PL) | Polskie zastąpienie |
|---|---|
| `submit` | `zapis formularza`, `wysłanie danych` |
| `save` | `zapis`, `zapisanie rekordu` |
| `delete` | `usunięcie rekordu` |
| `dropdown` | `lista rozwijana` |
| `checkbox` | `pole wyboru` |
| `button` | `przycisk` |
| `placeholder` | `tekst podpowiedzi` |
| `label` | `etykieta pola` |
| `tooltip` | `dymek podpowiedzi` |
| `breadcrumb` | `ścieżka nawigacyjna` |
| `loading` (jako opis stanu) | `stan ładowania` |
| `layout` | `układ ekranu` |
| `sidebar` | `menu boczne` |
| `navbar` | `pasek nawigacyjny` |
| `header` (jako opis UI) | `nagłówek`, `pasek tytułu` |
| `footer` (jako opis UI) | `stopka` |
| `row` (jako opis UI) | `wiersz` |
| `column` (jako opis UI) | `kolumna` |
| `grid` | `grid` — ten termin jest wyjątkiem, dozwolony jako termin techniczny |

> **Zasada ogólna:** Jeśli termin angielski pojawia się jako opis tego co widzi użytkownik — zamień na polski. Jeśli pojawia się jako wartość techniczna (`matColumnDef`, `formControlName`, nazwa metody) — zostaw w oryginale w backtickach.

---

## 5. Wyrażenia rekomendacyjne — AOS opisuje, nie rekomenduje

Dokumentacja AOS nie zawiera opinii, sugestii ani rekomendacji agenta.

| Wyrażenie zakazane | Powód |
|---|---|
| `sugeruję`, `polecam` | AOS nie jest dokumentem rekomendacyjnym |
| `warto`, `należałoby` | j.w. |
| `lepiej byłoby`, `dobrą praktyką jest` | j.w. |
| `można by rozważyć` | j.w. |
| `wydaje się nieoptymalne` | j.w. |

Jeśli agent wykryje realny problem w kodzie (np. brak walidacji wymaganego pola), opisuje stan faktyczny bez oceniania:

> ❌ `Brak walidacji na tym polu wydaje się błędem.`  
> ✅ `Pole nie posiada walidatora `Validators.required`. [WYMAGA WERYFIKACJI — czy brak walidacji jest celowy]`
