# Szczegóły firmy — Dane i Operacje

---

## Zrzut ekranu

![Ekran Szczegóły firmy](screenshot.png)

---

## 1. Formularz danych firmy

### 1.1 Struktura formularza

Ekran zawiera jeden formularz reaktywny `firmDetailsForm: FormGroup` zdefiniowany w konstruktorze komponentu `FirmDetailsComponent`.

> Ekran nie zawiera komponentu gridu. Dane prezentowane są w formularzu.

### 1.2 Tabela pól

| Nazwa pola | Etykieta UI | Typ elementu | `formControlName` | Wymagane (TS) | Wymagane (HTML) | Walidatory | Komunikat błędu |
|---|---|---|---|---|---|---|---|
| Pole Nazwa firmy | "Firm Name" | `mat-input` (text) | `firmName` | Tak | Tak | `Validators.required` | "Firm Name is required" |
| Pole CUI | "CUI Value" | `mat-input` (text) | `cuiValue` | Tak | Tak | `Validators.required` | "CUI Value is required" |
| Pole RegCom | "Registration Number (RegCom)" | `mat-input` (text) | `regCom` | **Nie** | Tak | Brak walidatora w TS | "Registration Number is required" |
| Pole Adres | "Address" | `mat-input` (text) | `address` | Tak | Tak | `Validators.required` | "Address is required" |
| Pole Województwo | "County" | `mat-input` (text) | `county` | Tak | Tak | `Validators.required` | "County is required" |
| Pole Miasto | "City" | `mat-input` (text) | `city` | Tak | Tak | `Validators.required` | "City is required" |

### 1.3 Szczegółowe opisy pól

#### Pole: Nazwa firmy

- **Opis biznesowy**: Nazwa firmy użytkownika (wystawcy dokumentów).
- **Typ**: `mat-input` (text)
- **Wymagalność**: Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "Firm Name is required".
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: `Validators.required`
- **Etykieta**: "Firm Name"
- **Dane techniczne**:
  - `formControlName: \`firmName\``
  - Element: `<mat-form-field>` z `<input matInput>`
  - Mapping do modelu: `IFirm.name`
- **Logika specjalna**: Pole jest autouzupełniane wartością z ANAF po kliknięciu przycisku Pobieranie danych z ANAF.

#### Pole: CUI

- **Opis biznesowy**: CUI firmy użytkownika — unikalny numer identyfikacji podatkowej w Rumunii (*Codul Unic de Identificare*).
- **Typ**: `mat-input` (text) z przyciskiem ikony `cloud_download` jako suffix
- **Wymagalność**: Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "CUI Value is required".
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: `Validators.required`
- **Etykieta**: "CUI Value"
- **Dane techniczne**:
  - `formControlName: \`cuiValue\``
  - Element: `<mat-form-field>` z `<input matInput>` i `<button mat-icon-button matSuffix>`
  - Mapping do modelu: `IFirm.cui`
- **Logika specjalna**: Pole zawiera przycisk ikony (`cloud_download`) wywołujący operację Pobieranie danych z ANAF. Wartość pola CUI jest przekazywana jako parametr do `firmService.getFirmFromAnaf(cuiValue)`.

#### Pole: RegCom

- **Opis biznesowy**: RegCom firmy użytkownika — numer rejestracji firmy w rumuńskim rejestrze handlowym.
- **Typ**: `mat-input` (text)
- **Wymagalność**: Pole jest opcjonalne. Pole nie posiada walidatora `Validators.required` w `FormGroup`. [UWAGA: Szablon HTML zawiera atrybut `required` oraz komunikat `mat-error` "Registration Number is required", ale `FormControl` w TS nie posiada `Validators.required`. Komunikat `mat-error` nie zostanie wyświetlony bez walidatora w TS — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: Brak walidatora w `FormGroup`. Atrybut `required` w HTML nie ma wpływu na walidację formularza reaktywnego.
- **Etykieta**: "Registration Number (RegCom)"
- **Dane techniczne**:
  - `formControlName: \`regCom\``
  - `FormControl` inicjalizowany wartością `null`
  - Mapping do modelu: `IFirm.regCom` (typ: `string | null`, opcjonalny)
- **Logika specjalna**: Pole jest autouzupełniane wartością z ANAF po kliknięciu przycisku Pobieranie danych z ANAF.

#### Pole: Adres

- **Opis biznesowy**: Adres siedziby firmy użytkownika.
- **Typ**: `mat-input` (text)
- **Wymagalność**: Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "Address is required".
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: `Validators.required`
- **Etykieta**: "Address"
- **Dane techniczne**:
  - `formControlName: \`address\``
  - Mapping do modelu: `IFirm.address`
- **Logika specjalna**: Pole jest autouzupełniane wartością z ANAF po kliknięciu przycisku Pobieranie danych z ANAF.

#### Pole: Województwo

- **Opis biznesowy**: Województwo (county) siedziby firmy użytkownika.
- **Typ**: `mat-input` (text)
- **Wymagalność**: Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "County is required".
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: `Validators.required`
- **Etykieta**: "County"
- **Dane techniczne**:
  - `formControlName: \`county\``
  - Mapping do modelu: `IFirm.county`
- **Logika specjalna**: Pole jest autouzupełniane wartością z ANAF po kliknięciu przycisku Pobieranie danych z ANAF.

#### Pole: Miasto

- **Opis biznesowy**: Miasto siedziby firmy użytkownika.
- **Typ**: `mat-input` (text)
- **Wymagalność**: Pole jest wymagane. Brak wartości blokuje zapis formularza i wywołuje komunikat: "City is required".
- **Dostępność**: Pole jest edytowalne.
- **Widoczność**: Pole jest widoczne.
- **Walidatory**: `Validators.required`
- **Etykieta**: "City"
- **Dane techniczne**:
  - `formControlName: \`city\``
  - Mapping do modelu: `IFirm.city`
- **Logika specjalna**: Pole jest autouzupełniane wartością z ANAF po kliknięciu przycisku Pobieranie danych z ANAF.

---

## 2. Operacje i przyciski

### 2.1 Tabela operacji

| Przycisk / Operacja | Etykieta UI | Typ | Warunek dostępności | Akcja | Rezultat |
|---|---|---|---|---|---|
| Przycisk Pobieranie danych z ANAF | Ikona `cloud_download` | `mat-icon-button` (suffix w polu CUI) | Zawsze aktywny | Wywołuje `GET /Firm/fromAnaf/{cuiValue}` | Autouzupełnianie 5 pól formularza + komunikat sukcesu |
| Przycisk Zapis formularza | "Update" / "Submit" | `mat-raised-button` (primary, type=submit) | Zawsze aktywny (walidacja w `onSubmit()`) | Walidacja + `PUT /Firm/EditFirm/false` lub `POST /Firm/AddFirm/false` | Komunikat sukcesu |

### 2.2 Szczegółowe opisy operacji

#### Operacja: Pobieranie danych z ANAF

- **Przycisk**: Ikona `cloud_download` (mat-icon-button, type=button) — suffix w polu CUI
- **Warunek dostępności**: Przycisk jest zawsze aktywny. [UWAGA: Brak walidacji czy pole CUI jest wypełnione przed wywołaniem ANAF — WYMAGA WERYFIKACJI Z ZESPOŁEM]
- **Akcja**:
  - Typ: `API call`
  - Wywołanie: `firmService.getFirmFromAnaf(this.firmDetailsForm.value.cuiValue)`
- **Wywołanie API**:
  - Metoda HTTP: `GET`
  - Endpoint: `GET /Firm/fromAnaf/{cuiValue}`
  - Parametry: `cuiValue` — wartość pola CUI z formularza (path param)
- **Po pomyślnym wykonaniu**:
  - Autouzupełnianie pól: Nazwa firmy, RegCom, Adres, Województwo, Miasto
  - Pola pozostają edytowalne po autouzupełnieniu
  - Komunikat sukcesu (`ToastrService`): "Firm details fetched successfully." (tytuł: "Success")
- **Obsługa błędu**:
  - Brak jawnej obsługi błędów w kodzie (brak bloku `error` w `subscribe()`) [WYMAGA WERYFIKACJI — czy interceptor globalny obsługuje błędy HTTP]

#### Operacja: Zapis formularza

- **Przycisk**: "Update" (tryb edycji) lub "Submit" (tryb tworzenia) — `mat-raised-button`, color primary, type=submit
- **Warunek dostępności**: Przycisk jest zawsze aktywny. Walidacja formularza wykonywana jest w metodzie `onSubmit()`.
- **Walidacja**: Przed wykonaniem operacja sprawdza stan formularza reaktywnego `firmDetailsForm`. Zapis jest możliwy wyłącznie gdy formularz jest w stanie `valid`. Gdy formularz jest `invalid`, metoda `onSubmit()` przerywa wykonanie (`return`).
- **Akcja**:
  - Tryb edycji (`currentUserFirm.id !== 0`): Wywołuje `PUT /Firm/EditFirm/false`
  - Tryb tworzenia (`currentUserFirm.id === 0` lub brak firmy): Wywołuje `POST /Firm/AddFirm/false`
- **Wywołanie API (edycja)**:
  - Metoda HTTP: `PUT`
  - Endpoint: `PUT /Firm/EditFirm/false`
  - Body: Obiekt `IFirm` — zawiera pola: `id`, `name`, `cui`, `regCom`, `address`, `county`, `city`
  - Parametr `isClient`: `false` (firma użytkownika, nie klient)
- **Wywołanie API (tworzenie)**:
  - Metoda HTTP: `POST`
  - Endpoint: `POST /Firm/AddFirm/false`
  - Body: Obiekt `IFirm` — `id` ustawione na `0`
  - Parametr `isClient`: `false`
- **Po pomyślnym wykonaniu**:
  - Komunikat sukcesu (`ToastrService`): "Firm details updated successfully." (tytuł: "Success")
  - Ekran nie wykonuje nawigacji po zapisie
  - Ekran nie odświeża danych z API po zapisie
- **Obsługa błędu (walidacja frontendowa)**:
  - Gdy formularz jest `invalid` i warunek `this.firmDetailsForm.valid` zwraca `false` w drugiej gałęzi: wyświetlany jest komunikat `errorMessage`: "Please fill all the required fields"
- **Obsługa błędu (API)**:
  - Brak jawnej obsługi błędów API w kodzie [WYMAGA WERYFIKACJI — czy interceptor globalny obsługuje błędy HTTP]

---

## 3. Sekcja filtrów

> Ekran nie zawiera dedykowanej sekcji filtrów.

---

## 4. Sortowanie i paginacja

> Ekran nie zawiera komponentu gridu. Dane prezentowane są w formularzu.

---

## 5. Akcje na wierszach gridu

> Ekran nie zawiera komponentu gridu.

---

## 6. Komunikaty i powiadomienia

### Komunikaty sukcesu

| Operacja | Komunikat | Typ | Biblioteka |
|---|---|---|---|
| Zapis formularza (edycja) | "Firm details updated successfully." | `success` | `ToastrService` (ngx-toastr) |
| Zapis formularza (tworzenie) | "Firm details updated successfully." | `success` | `ToastrService` (ngx-toastr) |
| Pobieranie danych z ANAF | "Firm details fetched successfully." | `success` | `ToastrService` (ngx-toastr) |

### Komunikaty błędów

| Błąd | Komunikat | Źródło | Lokalizacja |
|---|---|---|---|
| Pole Nazwa firmy puste | "Firm Name is required" | `mat-error` inline | Pod polem Nazwa firmy |
| Pole CUI puste | "CUI Value is required" | `mat-error` inline | Pod polem CUI |
| Pole RegCom puste | "Registration Number is required" | `mat-error` inline | Pod polem RegCom [UWAGA: Komunikat zdefiniowany w HTML ale walidator `Validators.required` nie istnieje w TS — komunikat nie zostanie wyświetlony] |
| Pole Adres puste | "Address is required" | `mat-error` inline | Pod polem Adres |
| Pole Województwo puste | "County is required" | `mat-error` inline | Pod polem Województwo |
| Pole Miasto puste | "City is required" | `mat-error` inline | Pod polem Miasto |
| Formularz invalid (ogólny) | "Please fill all the required fields" | `div.p-error` | Pod formularzem, nad przyciskiem |

---

## 7. Stany ładowania

| Stan | Wyzwalacz | Feedback UI | Opis |
|---|---|---|---|
| Ładowanie danych firmy | Załadowanie ekranu (`ngOnInit`) | `mat-progress-bar` (mode: query) | Widoczny gdy `currentUserFirm === null` |

---

## Następne sekcje

- Logika biznesowa i przepływy: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
