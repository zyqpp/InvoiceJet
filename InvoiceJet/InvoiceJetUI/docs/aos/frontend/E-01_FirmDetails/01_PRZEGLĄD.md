# Szczegóły firmy — Przegląd

---

## Zrzut ekranu

![Ekran Szczegóły firmy](../../../../../../Screenshots/Picture4.png)

---

## 1. Layout ekranu

### 1.1 Diagram struktury

```
┌─────────────────────────────────────────────────────────┐
│  [NAGŁÓWEK APLIKACJI — NavbarComponent]                 │
├──────────────┬──────────────────────────────────────────┤
│              │  Firm Details                             │
│  [SIDEBAR]   ├──────────────────────────────────────────┤
│  SidebarCmp  │  ┌── mat-progress-bar (widoczny gdy     │
│              │  │   dane firmy nie są załadowane)       │
│              │  ├──────────────────────────────────────┐│
│              │  │ mat-card                             ││
│              │  │  ┌─────────────────────────────────┐ ││
│              │  │  │ Pole: Firm Name                 │ ││
│              │  │  ├─────────────────────────────────┤ ││
│              │  │  │ Pole: CUI Value    [☁ ANAF]    │ ││
│              │  │  ├─────────────────────────────────┤ ││
│              │  │  │ Pole: Registration Number       │ ││
│              │  │  │ Pole: Address                   │ ││
│              │  │  │ Pole: County                    │ ││
│              │  │  │ Pole: City                      │ ││
│              │  │  ├─────────────────────────────────┤ ││
│              │  │  │ [Komunikat błędu — warunkowy]   │ ││
│              │  │  │ [Przycisk: Update / Submit]     │ ││
│              │  │  └─────────────────────────────────┘ ││
│              │  └──────────────────────────────────────┘│
└──────────────┴──────────────────────────────────────────┘
```

### 1.2 Opis layoutu

Ekran składa się z pojedynczego komponentu `mat-card` zawierającego formularz reaktywny. Formularz zawiera 6 pól tekstowych (`mat-form-field` z `mat-input`) rozmieszczonych w dwóch wierszach:

- **Wiersz 1**: Pole Nazwa firmy (pełna szerokość)
- **Wiersz 2**: Pole CUI (pełna szerokość, z przyciskiem ikony ANAF po prawej stronie)
- **Wiersz 3**: Pola RegCom, Adres, Województwo, Miasto (w jednym rzędzie)

Pod polami wyświetlany jest warunkowy komunikat błędu oraz przycisk zapisu formularza.

---

## 2. Komponenty główne

### 2.1 Sekcje UI

| Sekcja | Typ | Opis |
|---|---|---|
| Pasek postępu | `mat-progress-bar` | Widoczny wyłącznie gdy dane firmy nie są załadowane (`*ngIf="!currentUserFirm"`) |
| Pasek tytułu | Nagłówek `<h1>` | Wyświetla tekst "Firm Details" |
| Formularz danych firmy | Formularz reaktywny | Zawiera 6 pól identyfikacyjnych firmy w komponencie `mat-card` |

### 2.2 Elementy sterujące

| Element | Typ | Funkcja |
|---|---|---|
| Przycisk Pobieranie danych z ANAF | `mat-icon-button` (ikona `cloud_download`) | Wywołuje autouzupełnianie pól z ANAF na podstawie wartości pola CUI |
| Przycisk Zapis formularza | `mat-raised-button` (primary) | Waliduje formularz i wywołuje operację zapisu (dodanie lub edycja firmy) |

---

## 3. Scenariusz główny (Golden Path)

1. **Załadowanie ekranu**: Użytkownik nawiguje do ekranu Szczegóły firmy (URL: `/dashboard/firm-details`)
   - Guard `AuthGuard` weryfikuje token JWT
   - Komponent wywołuje `firmService.getUserActiveFirm()`
   - Podczas ładowania widoczny jest `mat-progress-bar`

2. **Wyświetlenie danych**: Formularz wypełniany jest danymi firmy użytkownika
   - Pola formularza otrzymują wartości z odpowiedzi API (obiekt `IFirm`)
   - Pasek postępu znika po załadowaniu danych

3. **Edycja danych**: Użytkownik modyfikuje wartości pól formularza
   - Walidacja inline wyświetla komunikaty `mat-error` pod polami z błędami

4. **Opcjonalnie — autouzupełnianie z ANAF**: Użytkownik klika ikonę `cloud_download` przy polu CUI
   - Wywołanie `firmService.getFirmFromAnaf(cuiValue)`
   - Pola Nazwa firmy, RegCom, Adres, Województwo, Miasto autouzupełniają się wartościami z odpowiedzi API
   - Komunikat sukcesu: "Firm details fetched successfully."

5. **Zapis**: Użytkownik klika przycisk Zapis formularza
   - Formularz jest walidowany
   - Tryb edycji (`currentUserFirm.id !== 0`): wywołanie `PUT /Firm/EditFirm/false`
   - Tryb tworzenia (`currentUserFirm.id === 0`): wywołanie `POST /Firm/AddFirm/false`
   - Komunikat sukcesu: "Firm details updated successfully."

---

## 4. Stany ekranu

| Stan | Opis | Wyzwalacz |
|---|---|---|
| Ładowanie | Pasek postępu `mat-progress-bar` widoczny, formularz ukryty | Załadowanie ekranu, oczekiwanie na `GET /Firm/GetUserActiveFirm/` |
| Formularz załadowany (edycja) | Pola wypełnione danymi firmy, przycisk "Update" | Odpowiedź API zwraca firmę z `id > 0` |
| Formularz pusty (tworzenie) | Pola puste, przycisk "Submit" | Odpowiedź API zwraca firmę z `id === 0` lub brak firmy |
| Błąd walidacji | Komunikaty `mat-error` pod polami, komunikat "Please fill all the required fields" | Próba zapisu z niepoprawnymi danymi |

---

## 5. Dostępność i uprawnienia

| Uprawnienie | Efekt | Warunek |
|---|---|---|
| Niezalogowany | Przekierowanie do ekranu Logowanie (`/login`) | `AuthGuard` — brak tokena JWT |
| Zalogowany | Pełny dostęp do formularza | Token JWT jest prawidłowy |

---

## 6. Integracje zewnętrzne

- **ANAF**: Zewnętrzna usługa API rumuńskiej administracji podatkowej. Endpoint: `GET /Firm/fromAnaf/{cuiValue}`. Ekran pobiera dane firmy (nazwa, RegCom, adres, województwo, miasto) na podstawie numeru CUI.

---

## 7. Notatki techniczne

- Ekran nie zawiera gridu ani paginacji.
- Ekran nie wywołuje okien modalnych.
- Ekran nie zawiera dedykowanej sekcji filtrów.
- Komponent wykorzystuje `ToastrService` (biblioteka `ngx-toastr`) do wyświetlania komunikatów sukcesu.
- Formularz ma maksymalną szerokość 800px (zdefiniowaną w SCSS).
- [UWAGA: Brak obsługi błędów API w `subscribe()` — brak bloku `error` w `onSubmit()` i `onCloudIconClick()` — WYMAGA WERYFIKACJI Z ZESPOŁEM]

---

## Następne sekcje

- Szczegółowe dane o polach i operacjach: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika biznesowa i przepływy: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
