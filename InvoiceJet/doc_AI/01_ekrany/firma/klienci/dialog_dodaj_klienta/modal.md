# AddEditClientDialogComponent — Dialog dodaj/edytuj klienta

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-Klienci-DodajKlienta |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Modal Angular Material do dodawania i edycji danych firmy klienta. Otwierany z ekranu listy klientów przez `MatDialog.open()`. Działa w dwóch trybach: dodawanie (dane klienta `null`) i edycja (dane klienta przekazane przez `MAT_DIALOG_DATA`). Obsługuje autouzupełnianie danych z rejestru ANAF na podstawie numeru CUI.

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-Klienci-DodajKlienta |
| Nazwa / tytuł w UI | Dodaj klienta / Edytuj klienta |
| Wywołany przez operację | OP-Klienci-DodajKlienta, OP-Klienci-EdytujKlienta |
| Ekran nadrzędny | `../ekran.md` (ClientsComponent) |
| Typ modalu | formularz |
| Zamknięcie przez Escape | tak |
| Zamknięcie przez klik tła | tak |

## Wizualizacja układu

```
┌────────────────────────────────────────┐
│ Dodaj klienta / Edytuj klienta     [X] │
├────────────────────────────────────────┤
│ Nazwa firmy:   [______________________]│
│ CUI:           [______________] [☁ ANAF]│
│ Reg. handlowy: [______________________]│
│ Adres:         [______________________]│
│ Okręg:         [______________________]│
│ Miasto:        [______________________]│
├────────────────────────────────────────┤
│ [Anuluj]                  [Zapisz]     │
└────────────────────────────────────────┘
```

## Pola modalu

| ID pola | Nazwa w UI | Typ | Wymagalność | Link do dokumentu |
|---|---|---|---|---|
| POLE-DodajKlienta-firmName | Nazwa firmy | mat-form-field (input) | wymagane | — |
| POLE-DodajKlienta-cuiValue | CUI/NIP | mat-form-field (input) | opcjonalne | — |
| POLE-DodajKlienta-regCom | Numer rejestracji handlowej | mat-form-field (input) | opcjonalne | — |
| POLE-DodajKlienta-address | Adres | mat-form-field (input) | opcjonalne | — |
| POLE-DodajKlienta-county | Okręg | mat-form-field (input) | opcjonalne | — |
| POLE-DodajKlienta-city | Miasto | mat-form-field (input) | opcjonalne | — |

## Dane wejściowe (MAT_DIALOG_DATA)

| Pole | Typ | Opis |
|---|---|---|
| `client` | `IFirm \| null` | `null` = tryb dodawania (pusty formularz); obiekt = tryb edycji (wypełniony formularz) |

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| Zapisz (tryb dodaj) | Wywołuje `POST /api/Firm/AddFirm/true` | Tak | tak (z wynikiem) |
| Zapisz (tryb edytuj) | Wywołuje `PUT /api/Firm/EditFirm/true` | Tak | tak (z wynikiem) |
| Anuluj | Zamknięcie bez zmian | Nie | tak |
| ☁ ANAF | Pobiera dane firmy z ANAF i wypełnia pola | `GET /api/Firm/fromAnaf/{cuiValue}` | nie |

## Przepływ

### Tryb dodawania (client = null)
1. Formularz pusty
2. Submit → `POST /api/Firm/AddFirm/true` (`isClient=true`)
3. Dialog zamknięty z wynikiem → lista klientów odświeżona

### Tryb edycji (client ≠ null)
1. Formularz wypełniony danymi klienta
2. Submit → `PUT /api/Firm/EditFirm/true` (`isClient=true`)
3. Dialog zamknięty z wynikiem → lista klientów odświeżona

### Autouzupełnienie ANAF
- Ikona chmury → `GET /api/Firm/fromAnaf/{cuiValue}` → wypełnienie pól formularza

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Dodanie klienta | `POST /api/Firm/AddFirm/true` |
| Edycja klienta | `PUT /api/Firm/EditFirm/true` |
| ANAF autouzupełnienie | `GET /api/Firm/fromAnaf/{cuiValue}` |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Sukces dodania | API zwróci 200/201 | Brak komunikatu dla użytkownika | Modal zamknięty; lista klientów odświeżona |
| Sukces edycji | API zwróci 200 | Brak komunikatu dla użytkownika | Modal zamknięty; lista klientów odświeżona |
| Błąd API | API zwróci 400/500 | Brak widocznego komunikatu (anomalia) | Modal pozostaje otwarty |
| Anulowanie | Użytkownik klika Anuluj lub Escape | Brak | Modal zamknięty, brak zmian |

## Powiązania z kodem

- Komponent modalu: `src/app/components/clients/add-edit-client-dialog/add-edit-client-dialog.component.ts`
- Szablon HTML: `src/app/components/clients/add-edit-client-dialog/add-edit-client-dialog.component.html`

## Wątpliwości i braki

- Brak widocznego komunikatu błędu dla użytkownika w przypadku niepowodzenia API.
- Parametr `isClient=true` w URL — jeden endpoint (`AddFirm`/`EditFirm`) obsługuje zarówno firmę własną jak i klientów, różniąc się tylko flagą.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `clients/add-edit-client-dialog.md`. |
