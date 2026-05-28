# [NAZWA_EKRANU] — Logika Biznesowa

---

## 1. Przepływy danych

### 1.1 Pobieranie danych (Read)

**Scenariusz**: Załadowanie ekranu

1. Użytkownik nawiguje do ekranu `[nazwa]` (URL: `/[ścieżka]`)
2. Hook / Guard: `[nazwa].guard.ts` sprawdza uprawnienia
3. Komponent: `[nazwa].component.ts` w `ngOnInit()` wywołuje serwis
4. Serwis: `[serwis].service.ts` — metoda `[getNazwa]()`
5. Żądanie HTTP: `GET [endpoint]` (np. `GET /api/clients`)
6. Odpowiedź API: Tablica `[typ modelu]` (np. `IFirm[]`)
7. Transformacja: [Opis transformacji danych w serwisie, jeśli istnieje]
8. Renderowanie: Grid / lista / formularz wyświetla dane

**Diagram przepływu**:
```
ngOnInit()
    ↓
[serwis].get[Nazwa]()
    ↓
[httpClient].get([endpoint])
    ↓
pipe(map(...), catchError(...))
    ↓
Zwrot Observable<[typ]>
    ↓
subscribe() w komponencie
    ↓
[this.dane] = [wartość]
    ↓
Template: *ngFor / *ngIf renderuje dane
```

---

### 1.2 Tworzenie / Edycja danych (Write)

**Scenariusz**: Zapis formularza

1. Użytkownik wypełnia formularz i klika [Przycisk Zapis]
2. Walidacja frontendowa: `if (this.form.valid)`
3. Przygotowanie danych: 
   - Pobranie wartości z `formGroup.value`
   - Transformacja: [Opis transformacji z formularza na model API]
4. Serwis: `[serwis].service.ts` — metoda `[create/update][Nazwa]()`
5. Żądanie HTTP: `POST [endpoint]` / `PUT [endpoint]/{id}`
6. Parametry:
   - Path params: `{id}` — pochodzi z `this.activatedRoute.snapshot.params.id`
   - Body: `[typ modelu]` — zawiera pola [pole1, pole2, ...]
7. Odpowiedź API: `[typ modelu]` — zwracany zaktualizowany/nowy rekord
8. Obsługa: 
   - Sukces: Komunikat + nawigacja / zamknięcie dialogu
   - Błąd: Komunikat błędu + formularz pozostaje otwarty do edycji

**Kod (schema)**:
```typescript
this.service.update(this.form.value).subscribe({
  next: (result) => {
    // Sukces: snackbar + refresh
  },
  error: (err) => {
    // Błąd: wyświetl komunikat
  }
})
```

---

### 1.3 Usuwanie danych (Delete)

**Scenariusz**: Usunięcie rekordu

1. Użytkownik klika przycisk [Usunięcie rekordu]
2. Dialog potwierdzenia: "Na pewno chcesz usunąć?"
3. Potwierdzenie: `DELETE [endpoint]/{id}`
4. ID: Pochodzi z `[wybranego wiersza gridu / parametru routera]`
5. Odpowiedź: HTTP 200 OK lub `{ success: true }`
6. Rezultat: Komunikat sukcesu + odświeżenie listy

---

## 2. Reguły biznesowe

### 2.1 Reguły walidacji

| Reguła | Opis | Implementacja | Komunikat |
|---|---|---|---|
| [Nazwa reguły] | [Warunek] | Frontend: `Validators.*` / Backend: API validation | "[tekst błędu]" |
| Pole CUI wymagane | CUI musi być 13-cyfrowy numer rumuński | `pattern: /^\d{13}$/` | "CUI musi zawierać 13 cyfr" |
| E-mail unikalny | Email nie może się powtarzać w bazie | Backend: API 400 | "Email już istnieje w systemie" |

### 2.2 Reguły biznesowe (logika specjalna)

**Reguła 1: [Nazwa reguły]**
- **Wyzwalacz**: [Zdarzenie, np. "Po wpisaniu wartości w pole CUI"]
- **Warunek**: [Opis warunku z kodu]
- **Akcja**: [Co się dzieje]
  - Metoda serwisu: `[serwis].[metoda]()`
  - Endpoint: `GET [endpoint]`
  - Transformacja wyników: [Opis]
- **Skutek**: [Co widzi użytkownik — autouzupełnianie, poradę, zmiana stanu innego pola]
- **Kod techniczny**: 
  - Komponent: `[nazwa].component.ts` — method `[on[Nazwa]]()`
  - Serwis: `[serwis].service.ts` — method `[get/fetch[Nazwa]]()`

**Reguła 2: [Przykład: Autouzupełnianie danych z ANAF]**
- **Wyzwalacz**: Kliknięcie przycisku "Pobierz dane z ANAF"
- **Warunek**: Pole CUI jest wypełnione i jest poprawne (`pattern` passed)
- **Akcja**:
  1. Disable form fields (zabezpieczenie przed edycją)
  2. Pokaz spinner (stan ładowania)
  3. Wywołaj `firmService.getFirmByCui(cui)`
  4. API: `GET /api/anaf/{cui}`
  5. Odpowiedź: `{ name, regCom, address, county, city, tva }`
- **Skutek**: 
  - Autouzupełnianie pól: Nazwa firmy, RegCom, Adres, Województwo, Miasto
  - Pola są [edytowalne / read-only] po autouzupełnieniu
  - Komunikat: "[Dane pobrane z ANAF]"
- **Obsługa błędu**: 
  - 404: "Firma nie znaleziona"
  - 500: "Błąd usługi ANAF"

---

## 3. Integracje z API

### 3.1 Endpointy używane w ekranie

| Endpoint | Metoda | Opis | Parametry | Odpowiedź |
|---|---|---|---|---|
| `/api/firms` | `GET` | Pobierz listę firm | `page?: number`, `size?: number` | `{ data: IFirm[], total: number }` |
| `/api/firms/{id}` | `GET` | Pobierz szczegóły firmy | `id: string` (path) | `IFirm` |
| `/api/firms` | `POST` | Utwórz nową firmę | Body: `IFirm` (bez `id`) | `IFirm` (z nowym `id`) |
| `/api/firms/{id}` | `PUT` | Aktualizuj firmę | Path: `id`, Body: `IFirm` | `IFirm` |
| `/api/firms/{id}` | `DELETE` | Usuń firmę | `id: string` (path) | `{ success: boolean }` |
| `/api/anaf/{cui}` | `GET` | Pobierz dane z ANAF | `cui: string` (path) | `{ name, regCom, ... }` |

### 3.2 Obsługa błędów HTTP

| Status | Przyczyna | Obsługa | Komunikat użytkownika |
|---|---|---|---|
| 400 Bad Request | Nieprawidłowe dane | Wyświetl błędy walidacji | "[tekst z API]" |
| 401 Unauthorized | Brak tokena JWT / token wygasł | Przekieruj do logowania | "Sesja wygasła, zaloguj się ponownie" |
| 403 Forbidden | Brak uprawnień do zasobu | Wyświetl komunikat + powrót | "Nie masz uprawnień do tej operacji" |
| 404 Not Found | Zasób nie istnieje | Wyświetl komunikat + powrót | "Rekord nie znaleziony" |
| 500 Server Error | Błąd serwera | Wyświetl komunikat + retry | "Błąd serwera, spróbuj później" |

---

## 4. Warunki biznesowe i dostępność

### 4.1 Warunki wyświetlania elementów

| Element | Warunek widoczności | Kod |
|---|---|---|
| [Element 1] | Zawsze widoczny | N/A |
| [Element 2] | Widoczny gdy `userRole === 'Admin'` | `*ngIf="currentUser.role === 'Admin'"` |
| [Przycisk 3] | Widoczny gdy formularz jest `valid` | `*ngIf="form.valid"` |
| [Sekcja 4] | Widoczny gdy `isDarkMode === true` | `*ngIf="isDarkMode | async"` |

### 4.2 Warunki dostępności operacji

| Operacja | Warunek dostępności | Efekt gdy niedostępna |
|---|---|---|
| Zapis formularza | `form.valid === true` | Przycisk disabled + tooltip "Wypełnij wymagane pola" |
| Edycja rekordu | `userRole !== 'Viewer'` | Ikona disabled |
| Eksport danych | `rows.length > 0` | Przycisk disabled + "Brak danych do eksportu" |

---

## 5. Logika powiązań między polami (Cascading)

> [Jeśli ekran nie zawiera zależności między polami, użyj: "Ekran nie zawiera powiązań między polami."]

**Powiązanie 1: [Nazwa]**
- **Pole wyzwalające**: [Nazwa pola]
- **Pola zależne**: [Pole 1, Pole 2, ...]
- **Logika**: Gdy pole wyzwalające zmienia wartość na [X], pole zależne [zmienia opcje / jest czyszczane / jest pokazane / jest ukryte]
- **Kod**: 
  ```typescript
  this.form.get('parentField')?.valueChanges
    .pipe(switchMap(value => this.service.getDependentData(value)))
    .subscribe(data => {
      this.form.patchValue({ childField: ... })
    })
  ```

---

## 6. Performance i optymalizacje

- **Debounce na input fields**: [Tak / Nie / [n]ms] — opis
- **Lazy loading**: [Opis jeśli istnieje]
- **Caching**: [Opis jeśli istnieje]
- **Virtual scrolling**: [Jeśli grid zawiera dużo wierszy — `virtual-scroll`]

---

## 7. Notatki i Known Issues

- [WYMAGA WERYFIKACJI — jeśli coś nie jest jasne]
- [Known Issue: Opis problemu]
- [TODO: Przyszłe ulepszenie]

---

## Poprzednie sekcje

- Metadane: [00_METADANE.md](00_METADANE.md)
- Przegląd: [01_PRZEGLĄD.md](01_PRZEGLĄD.md)
- Pola i operacje: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)

## Następna sekcja

- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
