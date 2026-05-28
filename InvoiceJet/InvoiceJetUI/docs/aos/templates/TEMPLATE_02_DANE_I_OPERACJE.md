# [NAZWA_EKRANU] — Dane i Operacje

---

## 1. Pola formularza / Grid

### 1.1 Struktura pól

[Jeśli ekran zawiera formularz — opisz pola. Jeśli grid — opisz kolumny.]

| Nazwa pola | Typ | Wymagane | Opis | Walidatory | Dane techniczne |
|---|---|---|---|---|---|
| [Nazwa pola] | `text` / `number` / `date` / itp. | Tak / Nie | [Opis biznesowy] | `Validators.required`, `pattern: [regex]` | `formControlName: \`[nazwa]\`` |
| [Kolumna gridu] | text / link / action | N/D | [Opis kolumny] | N/D | `matColumnDef: \`[nazwa]\`` |
| N/D | N/D | N/D | N/D | N/D | N/D |

### 1.2 Szczegółowe opisy pól

#### Pole: [Nazwa pola 1]
- **Opis biznesowy**: [Co to pole reprezentuje dla użytkownika]
- **Typ**: `text input` / `number` / `date picker` / `select` / `checkbox` / itp.
- **Wymagalność**: Pole jest [wymagane / opcjonalne / wymagane gdy [warunek]]
- **Dostępność**: Pole jest [zawsze edytowalne / tylko do odczytu / dezaktywowane gdy [warunek]]
- **Widoczność**: Pole jest [zawsze widoczne / widoczne wyłącznie gdy [warunek]]
- **Walidatory**: 
  - `Validators.required` — Pole jest wymagane
  - `Validators.minLength(n)` — Minimalna długość: [n] znaków
  - `Validators.pattern([regex])` — Wzorzec: [regex]
  - [inne walidatory]
- **Tekst podpowiedzi (placeholder)**: "[tekst]"
- **Etykieta**: "[tekst etykiety]"
- **Słownik wartości** (jeśli dotyczy): `[Nazwa słownika]` — wartości: `[wartość1]`, `[wartość2]`, itd.
- **Dane techniczne**: 
  - `formControlName: \`[nazwa]\``
  - Element: `<mat-form-field>` / `<input>` / `<mat-select>` / itp.
  - Plik: [nazwa komponentu / dialogu]
- **Logika specjalna** (jeśli istnieje): [Opis autouzupełniania, warunkowych zależności, zmian kasdowych, itp.]
- **Komunikat błędu**: "[tekst erroru z mat-error]"

#### Pole: [Nazwa pola 2]
[Powtórz schemat dla każdego pola]

---

## 2. Operacje i przyciski

### 2.1 Tabela operacji

| Przycisk / Operacja | Typ | Warunek dostępności | Akcja | Rezultat |
|---|---|---|---|---|
| Przycisk [Nazwa] | `button` / `icon-button` / `menu-item` | Zawsze aktywny / Nieaktywny gdy [warunek] | Otwiera dialog / Wywołuje API / Nawiguje | [Opis rezultatu] |
| Przycisk [Nazwa 2] | `button` | Aktywny gdy formularz jest `valid` | Zapisuje dane | Komunikat sukcesu + odświeżenie |
| N/D | N/D | N/D | N/D | N/D |

### 2.2 Szczegółowe opisy operacji

#### Operacja: [Nazwa operacji 1]
- **Przycisk**: [Typ przycisku, etykieta UI] — `[formControlName]` / `[click handler]`
- **Warunek dostępności**: Przycisk jest [zawsze aktywny / nieaktywny gdy [warunek z kodu]]
- **Walidacja**: Przed wykonaniem operacja sprawdza [opisz walidację]
- **Akcja**: 
  - Typ: `API call` / `Dialog` / `Navigation` / `Data operation`
  - Szczegóły: [Opis poniżej]
- **Wywołanie API** (jeśli dotyczy):
  - Metoda HTTP: `POST` / `PUT` / `DELETE` / itp.
  - Endpoint: `[HTTP_METHOD] [ścieżka]`
  - Parametry: [Opis parametrów, jak są pobierane z formularza]
  - Body: `[typ obiektu np. IFirm]` — cechy [lista pól]
- **Po pomyślnym wykonaniu**:
  - Komunikat: "[tekst komunikatu sukcesu]"
  - Rezultat: [Zamknięcie dialogu / Nawigacja / Odświeżenie listy / itp.]
- **Obsługa błędu**:
  - Komunikat błędu: "[tekst z API]"
  - Zachowanie: [Jak obsługiwany jest błąd — czy wyświetlony komunikat, ponowna próba, itp.]
- **Dane techniczne**: 
  - Handler: `[nazwa metody z .ts]`
  - Serwis: `[nazwa].service.ts`
  - Metoda serwisu: `[nazwa metody serwisu]()`

#### Dialog: [Nazwa dialogu]
- **Otwarcie**: Kliknięcie przycisku [Nazwa] otwiera dialog
- **Tryb**: 
  - Dodawanie (nowy rekord): Parametr `data` = `null`, pola puste
  - Edycja (istniejący rekord): Parametr `data` zawiera `[typ obiektu]`, pola wypełnione
- **Komponenty dialogu**: [Opis pól w dialogu — użyj schematu z sekcji 1.2]
- **Przyciski dialogu**: 
  - Zapis formularza: Zawiera walidację, wysyła `PUT /api/[endpoint]`
  - Anulowanie operacji: Zamyka dialog bez zapisania
- **Rezultat**:
  - Sukces: Dialog zamykany, zwracany obiekt `[typ]`, lista jest odświeżana
  - Anulowanie: Dialog zamykany bez wyniku (`undefined`)

---

## 3. Sekcja filtrów (jeśli istnieje)

> [Jeśli ekran nie zawiera sekcji filtrów, użyj: "Ekran nie zawiera dedykowanej sekcji filtrów."]

| Filtr | Typ | Opis | Efekt |
|---|---|---|---|
| [Nazwa filtru] | `text` / `select` / `date-range` / itp. | [Opis] | Filtruje grid po [cesze] |

---

## 4. Sortowanie i paginacja (jeśli istnieje)

> [Jeśli ekran nie zawiera gridu, użyj: "Ekran nie zawiera komponentu gridu."]

### Sortowanie
- Dostępne kolumny do sortowania: [Kolumna 1], [Kolumna 2], [Kolumna 3]
- Domyślne sortowanie: Po kolumnie [X] malejąco / rosnąco
- Dane techniczne: `matSort`, `[matSortHeader]`

### Paginacja
- Liczba wierszy na stronę: [10 / 25 / 50] (domyślnie: [X])
- Całkowita liczba rekordów: Pobierana z API
- Dane techniczne: `<mat-paginator>`, `pageSizeOptions: [10, 25, 50]`

---

## 5. Akcje na wierszach gridu (jeśli istnieje)

> [Jeśli grid nie zawiera akcji na wierszach, użyj: "Grid nie zawiera dedykowanych akcji na wierszach."]

| Akcja | Typ | Wyzwalacz | Rezultat |
|---|---|---|---|
| Edycja | Icon button | Kliknięcie ikony edit na wierszu | Otwarcie dialogu edycji |
| Usunięcie | Icon button | Kliknięcie ikony delete na wierszu | Potwierdzenie + usunięcie |
| Menu kontekstowe | ⋮ icon | Kliknięcie ikony menu | Lista akcji |

---

## 6. Komunikaty i powiadomienia

### Komunikaty sukcesu
| Operacja | Komunikat | Typ | Opis |
|---|---|---|---|
| Zapis formularza | "[tekst z MatSnackBar]" | `success` | Wyświetlany przez [n] sekund |
| Usunięcie rekordu | "[tekst]" | `success` | N/D |

### Komunikaty błędów
| Błąd | Komunikat | Źródło | Obsługa |
|---|---|---|---|
| Pole wymagane nie wypełnione | "[tekst mat-error]" | `mat-error` inline | Blokuje zapis formularza |
| API error 400 | "[tekst z serwera]" | `MatSnackBar` | Wyświetlany, użytkownik może retry |
| API error 500 | "[tekst fallback]" | `MatSnackBar` | Wyświetlany komunikat ogólny |

---

## 7. Stany ładowania

| Stan | Trigger | UI feedback | Opis |
|---|---|---|---|
| Ładowanie listy | `componentDidInit` / przeładowanie | Spinner / skeleton | Czekanie na `GET [endpoint]` |
| Wysyłanie formularza | Kliknięcie Zapis | Disabled button + spinner | Czekanie na `POST /PUT [endpoint]` |

---

## Następne sekcje

- Logika biznesowa i przepływy: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
