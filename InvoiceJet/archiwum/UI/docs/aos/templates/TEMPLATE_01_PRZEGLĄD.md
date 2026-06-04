# [NAZWA_EKRANU] — Przegląd

---

## 1. Layout ekranu

### Diagram struktury

```
┌─────────────────────────────────────────────────────────┐
│  [NAGŁÓWEK APLIKACJI — navbar z logo i menu]            │
├──────────────┬──────────────────────────────────────────┤
│              │  [TYTUŁ EKRANU]                           │
│  [SIDEBAR]   ├──────────────────────────────────────────┤
│  nawigacja   │  [SEKCJA — filtry / forma / grid]        │
│              │                                           │
│              │  [SEKCJA — lista / grid / szczegóły]     │
└──────────────┴──────────────────────────────────────────┘
```

[Dostosuj diagram do rzeczywistej struktury ekranu]

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| [Nazwa sekcji] | [Formularz / Grid / Dialog / Card] | [Krótki opis: co zawiera, do czego służy] |
| N/D | N/D | N/D |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk [Nazwa] | Button | [Co robi po kliknięciu] |
| Menu kontekstowe | Context Menu | [Dostępne opcje] |
| N/D | N/D | N/D |

---

## 3. Scenariusz główny (Golden Path)

Poniżej opisany jest główny scenariusz użytkownika na tym ekranie:

1. **Załadowanie ekranu**: Użytkownik nawiguje na ekran `[nazwa]` (URL: `/[ścieżka]`)
   - Ekran ładuje dane z API endpoint: `GET [endpoint]`
   - Wynik: [Opis co się wyświetla]

2. **Przeglądanie danych**: Użytkownik widzi [grid / listę / formularz] z następującymi danymi:
   - [Element 1]
   - [Element 2]
   - [Element 3]

3. **Akcja główna**: Użytkownik klika [przycisk/link]
   - Powoduje: [Nawigacja / Otwarcie dialogu / Wywołanie operacji]
   - Rezultat: [Co się dzieje]

4. **Powrót**: Użytkownik wraca do listy lub zamyka dialog
   - Dane są odświeżone / Zmiany są zapisane

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Ekran załadowany, dane pobrane | Otwarcie ekranu |
| Przetwarzanie | Czekanie na API | Kliknięcie przycisku akcji |
| Błąd | Komunikat błędu wyświetlony | Niepowodzenie API |
| Pusty | Brak danych do wyświetlenia | Baza pusta |

---

## 5. Dostępność i uprawnienia

| Uprawnienie | Efekt | Warunek |
|---|---|---|
| Brak roli | Przekierowanie do logowania | Użytkownik niezalogowany |
| [Rola X] | Dostęp pełny | Użytkownik ma rolę X |
| [Rola Y] | Dostęp ograniczony | Użytkownik ma rolę Y |

---

## 6. Integracje zewnętrzne

[Jeśli ekran integruje się z systemami zewnętrznymi — opisz tutaj]

- **ANAF API**: `GET /api/firms/anaf/{cui}` — pobieranie danych firmy
- **E-mail**: Wysyłanie powiadomień (jeśli dotyczy)
- N/D — ekran nie integruje się z systemami zewnętrznymi

---

## 7. Notatki techniczne

- [Flaga Angular, biblioteka Material, custom hook, itp.]
- [Dodatkowe informacje techniczne ważne do zrozumienia ekranu]
- [WYMAGA WERYFIKACJI — jeśli coś nie jest jasne z kodu]

---

## Następne sekcje

- Szczegółowe dane o polach, walidacji i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika biznesowa, przepływy, komunikaty: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
