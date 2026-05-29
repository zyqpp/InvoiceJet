# Login — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]              [Login] [Register]    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                         ┌──────────────────────┐                         │
│                         │ Login                │                         │
│                         ├──────────────────────┤                         │
│                         │ Email                │                         │
│                         │ Password        [👁] │                         │
│                         │              [Submit]│                         │
│                         └──────────────────────┘                         │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z publicznego paska nawigacyjnego i formularza logowania umieszczonego w `mat-card`. Menu boczne nie jest renderowane dla trasy `/login`.

Formularz zawiera pola `Email` i `Password`. Pole hasła ma przycisk zmiany widoczności tekstu.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek nawigacyjny | `NavbarComponent` | Pokazuje linki `Login` i `Register`, ponieważ trasa jest publiczna. |
| Karta formularza | `mat-card` | Zawiera tytuł `Login`, pola formularza i przycisk Submit. |
| Formularz logowania | `form [formGroup]="loginForm"` | Formularz reaktywny z walidatorami Angular. |
| Komunikat błędu | `div.p-error` | Renderowany tylko gdy `errorMessage` ma wartość. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Pole Email | `input matInput` | Przyjmuje adres email użytkownika. |
| Pole Password | `input matInput` | Przyjmuje hasło. |
| Przycisk widoczności hasła | `button mat-icon-button` | Przełącza flagę `hide`. |
| Przycisk Submit | `button mat-raised-button` | Wysyła formularz przez `(ngSubmit)="onSubmit()"`. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/login`.
2. `AppComponent` rozpoznaje trasę publiczną i nie renderuje menu bocznego.
3. `LoginComponent` renderuje `loginForm`.
4. `onSubmit()` wykonuje logowanie tylko wtedy, gdy `loginForm.valid` ma wartość `true`.
5. Dla poprawnego formularza komponent buduje obiekt `ILoginUser`.
6. `AuthService.login(user)` wysyła żądanie logowania.
7. Po sukcesie token z odpowiedzi jest zapisywany jako `authToken` w `localStorage`.
8. Router nawiguje do `dashboard`.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Pola `email` i `password` zawierają pusty tekst. | Wejście na `/login`. |
| Formularz niepoprawny | Email jest pusty, email ma niepoprawny format albo hasło jest puste. | Zmiana wartości pól. |
| Formularz poprawny | Email przechodzi walidatory i hasło ma wartość. | Wypełnienie pól. |
| Widoczne hasło | Pole hasła ma typ `text`. | Kliknięcie ikony widoczności. |
| Ukryte hasło | Pole hasła ma typ `password`. | Wartość `hide = true`. |
| Logowanie zakończone sukcesem | Token jest zapisany w `localStorage`. | Sukces `AuthService.login(user)`. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| Wejście na `/login` bez tokenu | Ekran jest dostępny. |
| Wejście na `/login` z tokenem | Ekran jest dostępny. Kod nie przekierowuje automatycznie zalogowanego użytkownika. |
| Sukces logowania | Token zostaje zapisany i aplikacja przechodzi do `dashboard`. |

---

## 7. Notatki techniczne

- Komponent ekranu: `LoginComponent`.
- Model formularza: `ILoginUser`.
- Serwis HTTP: `AuthService`.
- Formularz: `loginForm: FormGroup`.
- Klucz tokenu w `localStorage`: `authToken`.
- Flaga widoczności hasła: `hide`.

---

## Następne sekcje

- Szczegółowe dane o polach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
