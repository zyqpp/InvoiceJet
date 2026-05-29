# Zasady nadrzędne i ton wypowiedzi
## Wytyczne językowe AOS — Część 1 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Priorytet:** NADRZĘDNY — żadna inna wytyczna nie uchyla zasad z tego pliku

---

## 1. Pięć zasad absolutnych

### Z.1 — Precyzja ponad elegancję

Dokument AOS jest specyfikacją techniczną, nie artykułem. Zdanie brzmiące technicznie i powtarzalne jest lepsze od zdania eleganckiego i wieloznacznego.

> ❌ `Pole przyjmuje wartości słownikowe związane z walutą transakcji.`  
> ✅ `Pole akceptuje wartości ze słownika Currency. Dozwolone wartości: RON, EUR, USD, GBP.`

### Z.2 — Dokument opisuje to co jest, nie co powinno być

Agent opisuje zachowanie zaimplementowane w kodzie. Nie interpretuje intencji dewelopera. Jeśli kod zawiera błąd lub niespójność — agent to odnotowuje, nie "naprawia" opisem.

> ❌ `Pole prawdopodobnie powinno przyjmować tylko wartości dodatnie.`  
> ✅ `Pole nie posiada walidatora ograniczającego wartości do zakresu dodatniego. [WYMAGA WERYFIKACJI — czy brak walidacji jest celowy]`

### Z.3 — Jedno pojęcie, jedna nazwa — konsekwentnie przez cały dokument

Jeśli w sekcji 2 użyto nazwy "Dialog Edycja klienta", ta sama nazwa obowiązuje w sekcjach 7, 10, 11. Zmiana nazwy tego samego obiektu w toku dokumentu jest **błędem krytycznym**.

### Z.4 — Dane techniczne zawsze w oryginalnym języku kodu (angielski)

Nazwy klas, metod, zmiennych, selektorów, endpointów — zawsze w oryginalnym brzmieniu z kodu, nigdy tłumaczone. Zawsze wrapowane w backticki.

> ❌ `kontroler nazwy produktu`  
> ✅ `` formControlName: `productName` ``

### Z.5 — Opis biznesowy zawsze po polsku

Warstwa opisowa (co pole znaczy dla użytkownika, jaki jest cel operacji, jaka reguła biznesowa obowiązuje) — zawsze po polsku, bez wyjątków.

---

## 2. Ton i rejestr językowy

Dokumentacja AOS jest **oficjalnym dokumentem projektowym**. Obowiązuje ton:

| Cecha | Opis | Przykład prawidłowy | Przykład błędny |
|---|---|---|---|
| **Formalny** | Brak kolokwializmów i potocznych sformułowań | `Pole jest wymagane` | `Pole trzeba wypełnić` |
| **Bezosobowy** | Bez pierwszej osoby liczby pojedynczej lub mnogiej | `Ekran wyświetla listę` | `Widzimy listę` |
| **Rzeczowy** | Bez ozdobników, metafor, porównań | `Pole przyjmuje tekst` | `Pole służy do wpisania tekstu` |
| **Jednoznaczny** | Każde zdanie ma dokładnie jedno możliwe odczytanie | `Przycisk jest nieaktywny gdy formularz zawiera błędy walidacji` | `Przycisk może być nieaktywny` |
| **Zwięzły** | Minimalna liczba słów do przekazania pełnej informacji | `Pole opcjonalne` | `Pole nie musi być wypełnione przez użytkownika` |

---

## 3. Forma gramatyczna — reguły obowiązkowe

### Opisy stanu ekranu — czas teraźniejszy, strona czynna

> ✅ `Ekran wyświetla listę klientów przypisanych do zalogowanego użytkownika.`  
> ❌ `Ekran będzie wyświetlał listę klientów.`  
> ❌ `Lista klientów jest wyświetlana przez ekran.`

### Opisy operacji — bezokolicznik lub strona czynna

> ✅ `Przycisk wywołuje dialog edycji wybranego rekordu.`  
> ❌ `Po kliknięciu przycisku powinien otworzyć się dialog.`

### Opisy walidacji — strona czynna, czas teraźniejszy

> ✅ `Walidator blokuje zapis gdy pole jest puste.`  
> ❌ `Pole nie może być puste.`  
> ❌ `Pole powinno być wypełnione.`

### Podmiot wypowiedzi — zawsze element UI, nie użytkownik

> ✅ `Pole akceptuje wyłącznie wartości numeryczne.`  
> ❌ `Użytkownik wpisuje wartości numeryczne.`

> ✅ `Przycisk wywołuje operację zapisu formularza.`  
> ❌ `Użytkownik klika przycisk aby zapisać formularz.`

**Wyjątek:** Sekcja 11 (Scenariusze testowe) — tu podmiotem jest tester.

> ✅ `Tester wpisuje wartość "test@example.com" w pole Email.`

---

## 4. Reguły składniowe

### Długość zdania

- Zdanie opisowe: maksymalnie 30 słów.
- Jedno zdanie = jedna informacja. Zakaz zdań wielokrotnie złożonych w opisach stanu i walidacji.

> ❌ `Pole jest wymagane i akceptuje tylko cyfry, a wartość musi mieścić się w zakresie 1–100, przy czym w przypadku przekroczenia wartości maksymalnej wyświetlany jest komunikat błędu.`

> ✅ `Pole jest wymagane. Pole akceptuje wyłącznie wartości numeryczne całkowite. Dozwolony zakres: 1–100. Przekroczenie zakresu wywołuje komunikat: "Wartość musi mieścić się w przedziale 1–100."`

### Użycie spójników

Zakaz spójnika `oraz` dla niezwiązanych ze sobą cech:

> ❌ `Pole jest wymagane oraz wyświetla wartości słownikowe.`  
> ✅ `Pole jest wymagane. Pole wyświetla wartości ze słownika [nazwa].`

Spójnik `i` dopuszczalny wyłącznie dla cech logicznie powiązanych:

> ✅ `Pole jest niewidoczne i niedostępne gdy użytkownik nie ma roli Administrator.`

### Skróty dopuszczalne

| Skrót | Pełna forma |
|---|---|
| `N/D` | Nie dotyczy |
| `AOS` | Analityczny Opis Systemu (po pierwszym pełnym użyciu) |
| `UI` | User Interface |
| `API` | Application Programming Interface |
| `CRUD` | Create, Read, Update, Delete |
| `JWT` | JSON Web Token |
| `HTTP` | Hypertext Transfer Protocol |

Zakaz własnych skrótów tworzonych przez agenta bez wcześniejszego zdefiniowania w dokumencie.
