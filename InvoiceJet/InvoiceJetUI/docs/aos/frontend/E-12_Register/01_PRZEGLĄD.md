# Register — Przegląd

---

## 1. Układ ekranu

### 1.1 Diagram struktury

```
┌──────────────────────────────────────────────────────────────────────────┐
│ [Pasek nawigacyjny — NavbarComponent]              [Login] [Register]    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                         ┌──────────────────────────┐                     │
│                         │ Register                 │                     │
│                         ├──────────────────────────┤                     │
│                         │ First Name   Last Name   │                     │
│                         │ Email        Password    │                     │
│                         │ Password Confirmation    │                     │
│                         │                [Submit]  │                     │
│                         └──────────────────────────┘                     │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Opis układu

Ekran składa się z publicznego paska nawigacyjnego i formularza rejestracji umieszczonego w `mat-card`. Menu boczne nie jest renderowane dla trasy `/register`.

Formularz zawiera pola `First Name`, `Last Name`, `Email`, `Password` i `Password Confirmation`. Pola hasła mają przyciski zmiany widoczności tekstu.

---

## 2. Komponenty główne

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek nawigacyjny | `NavbarComponent` | Pokazuje linki `Login` i `Register`, ponieważ trasa jest publiczna. |
| Karta formularza | `mat-card` | Zawiera tytuł `Register`, pola formularza i przycisk Submit. |
| Formularz rejestracji | `form [formGroup]="registerForm"` | Formularz reaktywny z walidatorami Angular. |
| Stopka błędu | `mat-card-footer` | Renderowana tylko gdy `errorMessage` ma wartość. |

---

## 3. Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Pole First Name | `input matInput` | Przyjmuje imię użytkownika. |
| Pole Last Name | `input matInput` | Przyjmuje nazwisko użytkownika. |
| Pole Email | `input matInput` | Przyjmuje adres email. |
| Pole Password | `input matInput` | Przyjmuje hasło. |
| Pole Password Confirmation | `input matInput` | Przyjmuje potwierdzenie hasła. |
| Przycisk widoczności hasła | `button mat-icon-button` | Przełącza wspólną flagę `hide`. |
| Przycisk Submit | `button mat-raised-button` | Wysyła formularz przez `(ngSubmit)="onSubmit()"`. |

---

## 4. Scenariusz główny

1. Użytkownik przechodzi do ekranu `/register`.
2. `AppComponent` rozpoznaje trasę publiczną i nie renderuje menu bocznego.
3. `RegisterComponent` renderuje `registerForm`.
4. Formularz blokuje wysłanie w metodzie `onSubmit()`, jeżeli `registerForm.invalid` ma wartość `true`.
5. Dla poprawnego formularza komponent buduje obiekt `IRegisterUser`.
6. `AuthService.register(user)` wysyła żądanie rejestracji.
7. Po sukcesie token z odpowiedzi jest zapisywany jako `authToken` w `localStorage`.
8. Router nawiguje do `dashboard`.

---

## 5. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Stan początkowy | Wszystkie pola formularza zawierają pusty tekst. | Wejście na `/register`. |
| Formularz niepoprawny | Co najmniej jedno wymagane pole jest puste albo email ma niepoprawny format. | Zmiana wartości pól. |
| Formularz poprawny | Wszystkie wymagane pola mają wartości i email przechodzi `Validators.email`. | Wypełnienie pól. |
| Widoczne hasło | Oba pola hasła mają typ `text`. | Kliknięcie ikony widoczności. |
| Ukryte hasło | Oba pola hasła mają typ `password`. | Wartość `hide = true`. |
| Rejestracja zakończona sukcesem | Token jest zapisany w `localStorage`. | Sukces `AuthService.register(user)`. |

---

## 6. Dostępność i uprawnienia

| Warunek | Efekt |
|---|---|
| Wejście na `/register` bez tokenu | Ekran jest dostępny. |
| Wejście na `/register` z tokenem | Ekran jest dostępny. Kod nie przekierowuje automatycznie zalogowanego użytkownika. |
| Sukces rejestracji | Token zostaje zapisany i aplikacja przechodzi do `dashboard`. |

---

## 7. Notatki techniczne

- Komponent ekranu: `RegisterComponent`.
- Model formularza: `IRegisterUser`.
- Serwis HTTP: `AuthService`.
- Formularz: `registerForm: FormGroup`.
- Klucz tokenu w `localStorage`: `authToken`.
- Flaga widoczności hasła: `hide`.

---

## Następne sekcje

- Szczegółowe dane o polach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika frontendowa i przepływy UI: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
