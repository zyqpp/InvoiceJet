# Clients — Przegląd

---

## 1. Layout ekranu

### Diagram struktury

```
┌─────────────────────────────────────────────────────────┐
│  [NAGŁÓWEK APLIKACJI — navbar InvoiceJet]               │
├──────────────┬──────────────────────────────────────────┤
│              │  Klienci                                  │
│  [SIDEBAR]   │  [+ Dodaj klienta]  [Odśwież]  [Eksport]│
│  nawigacja   ├──────────────────────────────────────────┤
│              │  Sekcja filtrów:                          │
│              │  [Szukaj po nazwie] [Filtr: Typ]         │
│              ├──────────────────────────────────────────┤
│              │  Grid (Lista klientów):                   │
│              │  ┌─────────────────────────────────────┐ │
│              │  │ Nazwa │ CUI │ Email │ Akcje (⋮)   │ │
│              │  ├─────────────────────────────────────┤ │
│              │  │ Firma A │ 12345... │ firma@... │ ⋮│ │
│              │  │ Firma B │ 98765... │ firma@... │ ⋮│ │
│              │  └─────────────────────────────────────┘ │
│              │  [Paginacja: 1 2 3 ... Następna]        │
└──────────────┴──────────────────────────────────────────┘
```

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek tytułu | Header bar | Tytuł "Klienci" + główne przyciski operacyjne |
| Sekcja filtrów | Filter section | Pole do wyszukiwania i dropdown filtrów |
| Grid klientów | Mat-table | Lista firm z kolumnami: Nazwa, CUI, Email, Akcje |
| Paginacja | Paginator | Nawigacja po stronach, liczba wierszy na stronę |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk Dodaj klienta | Primary Button | Otwiera dialog dodawania nowego klienta |
| Przycisk Odśwież | Icon Button | Ponownie ładuje listę z API |
| Przycisk Eksport | Icon Button | Eksportuje dane do CSV (opcjonalnie) |
| Menu kontekstowe (⋮) | Context Menu | Opcje: Edycja, Usunięcie |

---

## 3. Scenariusz główny (Golden Path)

1. **Załadowanie ekranu**: Użytkownik nawiguje do `/clients`
   - Ekran ładuje dane z API: `GET /api/firms?isClient=true`
   - Wynik: Grid wyświetla listę firm jako klientów (max. 25 na stronę)

2. **Przeglądanie danych**: Użytkownik widzi grid z kolumnami:
   - Nazwa firmy
   - CUI (unikalny numer)
   - Email
   - Akcje (edycja, usunięcie)

3. **Akcja główna — Dodawanie klienta**:
   - Użytkownik klika **Przycisk Dodaj klienta**
   - Dialog otwiera się z formularzem
   - Użytkownik wypełnia pola: Nazwa, CUI, Email, Telefon, Adres
   - Klika **Zapis**
   - API: `POST /api/firms` z body `IFirm`
   - Rezultat: Nowy klient dodany, lista odświeżona, komunikat sukcesu

4. **Akcja — Edycja klienta**:
   - Użytkownik klika menu kontekstowe (⋮) na wierszu
   - Wybiera "Edycja"
   - Dialog otwiera się z danymi klienta
   - Użytkownik zmienia dane
   - Klika **Zapis**
   - API: `PUT /api/firms/{id}` z body `IFirm`
   - Rezultat: Klient zaktualizowany, lista odświeżona

5. **Akcja — Usunięcie klienta**:
   - Użytkownik klika menu kontekstowe (⋮)
   - Wybiera "Usunięcie"
   - Dialog potwierdzenia: "Na pewno chcesz usunąć klienta?"
   - Potwierdza
   - API: `DELETE /api/firms/{id}`
   - Rezultat: Klient usunięty, lista odświeżona

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Ekran załadowany, grid z danymi | Otwarcie ekranu |
| Ładowanie | Spinner wyświetlony | `GET /api/firms` w toku |
| Brak danych | "Brak klientów do wyświetlenia" | Tablica pusta |
| Błąd | Komunikat błędu | API zwrócił błąd 500 |
| Filtrowanie | Grid filtrowany po tekście | Użytkownik wpisuje w pole wyszukiwania |

---

## 5. Dostępność i uprawnienia

| Uprawnienie | Efekt | Warunek |
|---|---|---|
| Niezalogowany | Przekierowanie do logowania | Brak tokena JWT |
| Admin | Dostęp pełny (dodawanie, edycja, usunięcie) | `userRole === 'Admin'` |
| User | Dostęp do swojej firmy i klientów | `userRole === 'User'` |
| Viewer | Tylko odczyt | `userRole === 'Viewer'` |

---

## 6. Integracje zewnętrzne

- **ANAF API**: Nie bezpośrednio w tym ekranie (dostępne w dialogu edycji)
- **E-mail**: Wysyłanie powiadomień po dodaniu (backend)

---

## 7. Notatki techniczne

- Komponent: `ClientsComponent` w module `FirmModule`
- Serwis: `FirmService` — metody `getClients()`, `createFirm()`, `updateFirm()`, `deleteFirm()`
- Model: `IFirm` — zawiera pola: `id`, `name`, `cui`, `regCom`, `email`, `phone`, `address`, `city`, `county`, `tva`, `isClient`
- Material Components: `mat-table`, `mat-paginator`, `mat-sort`, `mat-form-field`

---

## Następne sekcje

- Szczegółowe dane o polach, walidacji i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika biznesowa, przepływy, komunikaty: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
