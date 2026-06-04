# Formuły standardowe i markery stanu
## Wytyczne językowe AOS — Część 6 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Zasada:** Poniższe frazy są obowiązkowe w określonych sytuacjach. Agent stosuje je dosłownie — bez parafrazowania.

---

## 1. Markery stanu dokumentu

Markery informują czytelnika o kompletności danej informacji. Pisane **wersalikami w nawiasach kwadratowych**. Nie są nigdy usuwane przez agenta — usuwa je wyłącznie człowiek po weryfikacji.

| Sytuacja | Wymagany marker |
|---|---|
| Wartość nie może być ustalona z dostarczonych plików kodu | `[WYMAGA WERYFIKACJI]` |
| Element istnieje w UI (widoczny na screenie) ale brak go w przekazanym kodzie | `[BRAK W DOSTARCZONYCH PLIKACH — WYMAGA WERYFIKACJI]` |
| Wartość opisana wyłącznie na podstawie screenshotu, bez potwierdzenia z kodu | `[NA PODSTAWIE SCREENSHOTU — WYMAGA POTWIERDZENIA Z KODU]` |
| Sekcja szablonu nieobowiązująca dla danego ekranu | `> Sekcja nie dotyczy tego ekranu. [powód jednym zdaniem]` |
| Agent wykrywa potencjalny problem lub niespójność w kodzie | `[UWAGA: opis problemu — WYMAGA WERYFIKACJI Z ZESPOŁEM]` |

### Zasady użycia markerów

- Marker umieszczany bezpośrednio po wartości której dotyczy, w tej samej komórce tabeli lub zdaniu.
- Marker nigdy nie zastępuje całego opisu — opisz tyle ile można, marker dodaj dla brakującej części.
- Nie stosuj markera dla całej sekcji gdy brakuje tylko jednej wartości.

> ❌ `Pole CUI. [WYMAGA WERYFIKACJI]`  
> ✅ `Pole CUI (formControlName: \`cuiValue\`). Typ pola: \`mat-input\` (text). Etykieta: "CUI Value". Walidator: [WYMAGA WERYFIKACJI — brak pliku spec.ts]`

---

## 2. Formuły opisu stanu pola

Stosuj poniższe frazy dosłownie dla każdego z opisanych stanów.

### Wymagalność

| Stan pola | Wymagana formuła |
|---|---|
| Pole z `Validators.required` | `Pole jest wymagane.` |
| Pole bez `Validators.required` | `Pole jest opcjonalne.` |
| Wymagalność warunkowa | `Pole jest wymagane gdy [warunek z kodu].` |

### Widoczność

| Stan pola | Wymagana formuła |
|---|---|
| Zawsze widoczne | `Pole jest widoczne.` (lub pomijaj — stan domyślny) |
| Ukryte warunkowo (`*ngIf`) | `Pole jest widoczne wyłącznie gdy [warunek].` |
| Ukryte warunkowo (`[hidden]`) | `Pole jest widoczne wyłącznie gdy [warunek].` |

### Dostępność (edytowalność)

| Stan pola | Wymagana formuła |
|---|---|
| Zawsze edytowalne | `Pole jest edytowalne.` (lub pomijaj — stan domyślny) |
| Tylko do odczytu (`readonly`) | `Pole jest niedostępne do edycji. Wartość prezentowana tylko do odczytu.` |
| Dezaktywowane warunkowo (`[disabled]`) | `Pole jest niedostępne gdy [warunek z kodu].` |

---

## 3. Formuły opisu walidacji pola

Każda walidacja opisywana przez: **warunek naruszenia + skutek w UI + treść komunikatu**.

### Walidator: `Validators.required`
> `Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "[tekst mat-error z HTML]".`

### Walidator: `Validators.minLength(n)`
> `Minimalna długość wartości: [n] znaków. Wartość krótsza wywołuje komunikat: "[tekst mat-error z HTML]".`

### Walidator: `Validators.maxLength(n)`
> `Maksymalna długość wartości: [n] znaków.`

### Walidator: `Validators.pattern(regex)`
> `Pole akceptuje wyłącznie wartości zgodne z wzorcem: \`[regex]\`. [Opcjonalnie: opis wzorca słowami]. Niezgodna wartość wywołuje komunikat: "[tekst mat-error z HTML]".`

### Walidator: `Validators.email`
> `Pole akceptuje wyłącznie adresy e-mail w formacie [lokalna-część]@[domena].[TLD].`

### Walidator: `Validators.min(n)` / `Validators.max(n)`
> `Dozwolony zakres wartości: [min]–[max].`

### Walidator niestandardowy (custom)
> `Pole posiada walidator niestandardowy: \`[nazwaWalidatora]\`. Warunek błędu: [opis z kodu lub spec.ts]. Komunikat: "[tekst]".`

---

## 4. Formuły opisu operacji

### Operacja otwierająca dialog
> `Operacja otwiera dialog [Nazwa dialogu].`

### Operacja wywołująca API
> `Operacja wywołuje \`[METODA_HTTP] [endpoint]\`. Po pomyślnym wykonaniu: [opis skutku]. W przypadku błędu: [opis obsługi błędu].`

### Operacja nawigująca do ekranu
> `Operacja przekierowuje użytkownika do ekranu [Nazwa ekranu] (URL: \`[ścieżka]\`).`

### Przycisk dezaktywowany warunkowo
> `Przycisk jest nieaktywny gdy [warunek z kodu — np. \`invoiceForm.invalid\`].`

### Operacja z pre-walidacją formularza
> `Przed wykonaniem operacja sprawdza stan formularza reaktywnego \`[nazwaFormularza]\`. Zapis jest możliwy wyłącznie gdy formularz jest w stanie \`valid\`.`

---

## 5. Formuły opisu dialogu

### Tryb dodawania (nowy rekord)
> `Dialog otwierany jest w trybie dodawania. Parametr \`data\` ma wartość \`null\`. Pola formularza są puste.`

### Tryb edycji (istniejący rekord)
> `Dialog otwierany jest w trybie edycji. Parametr \`data\` zawiera obiekt \`[typ]\` z danymi wybranego rekordu. Pola formularza są wstępnie wypełnione wartościami z \`data\`.`

### Wynik po zamknięciu (sukces)
> `Po pomyślnym zapisie dialog zamykany jest z wynikiem: obiekt \`[typ]\` reprezentujący [opis]. Ekran nadrzędny odświeża listę po zamknięciu dialogu.`

### Wynik po anulowaniu
> `Po kliknięciu przycisku Anulowanie operacji dialog zamykany jest bez wyniku (\`undefined\`). Dane nie są zapisywane.`

---

## 6. Formuły dla sekcji niedotyczących ekranu

Gdy sekcja szablonu nie ma zastosowania do dokumentowanego ekranu — stosuj poniższe formuły zamiast zostawiać sekcję pustą:

| Sytuacja | Wymagana formuła |
|---|---|
| Ekran nie zawiera sekcji filtrów | `> Ekran nie zawiera dedykowanej sekcji filtrów.` |
| Ekran nie zawiera formularza poza gridem | `> Ekran nie zawiera samodzielnych pól formularza. Dane wprowadzane są wyłącznie przez dialogi.` |
| Ekran nie zawiera gridu | `> Ekran nie zawiera komponentu gridu. Dane prezentowane są w formularzu lub kartach.` |
| Ekran nie wywołuje dialogów | `> Ekran nie wywołuje okien modalnych.` |
| Ekran nie generuje komunikatów sukcesu | `> Ekran nie generuje komunikatów sukcesu. Operacje zwrotne realizowane przez nawigację.` |

---

## 7. Nazewnictwo elementów UI w dokumencie

Format nazwy elementu: **[Typ elementu] + [Nazwa biznesowa po polsku]**

| Typ elementu | Format | Przykład |
|---|---|---|
| Pole | `Pole [Nazwa]` | `Pole Nazwa firmy`, `Pole Data wystawienia` |
| Przycisk | `Przycisk [Operacja]` | `Przycisk Dodawanie klienta`, `Przycisk Zapis formularza` |
| Dialog | `Dialog [Operacja] [Obiektu]` | `Dialog Dodawanie klienta`, `Dialog Edycja konta bankowego` |
| Grid | `Grid [Nazwa listy]` | `Grid listy klientów`, `Grid listy faktur` |
| Kolumna | `Kolumna [Nazwa]` | `Kolumna Nazwa firmy`, `Kolumna Data wystawienia` |
| Sekcja | `Sekcja [Nazwa]` | `Sekcja filtrów`, `Sekcja szczegółów dokumentu` |

### Ważne: etykiety UI vs nazwy w dokumencie

Etykiety na przyciskach w aplikacji (np. `"New Client"`, `"Update"`) mogą różnić się od nazw w dokumencie AOS — to dopuszczalne. W dokumencie używamy polskich nazw operacji; oryginalne etykiety podajemy wyłącznie jako wartości techniczne.

> ✅ `Przycisk Dodawanie klienta (etykieta UI: "New Client")`  
> ❌ `Przycisk New Client`
