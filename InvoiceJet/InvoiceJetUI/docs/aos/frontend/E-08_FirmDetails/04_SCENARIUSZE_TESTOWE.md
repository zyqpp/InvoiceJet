# Szczegóły firmy — Scenariusze Testowe

**Przeznaczenie**: Dokument dla QA — kroki testowe, selektory, dane wejściowe  
**Referencje**: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)

---

## 1. Scenariusz: Załadowanie ekranu i wyświetlenie danych firmy

**Typ**: Happy Path  
**Cel**: Weryfikacja poprawnego załadowania i wyświetlenia danych firmy użytkownika  
**Warunek wstępny**: Użytkownik zalogowany, firma użytkownika istnieje w bazie

### Kroki testowe

| Lp. | Akcja | Selektor / Element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Nawiguj do ekranu Szczegóły firmy | URL: `/dashboard/firm-details` | N/D | Ekran załadowany, `mat-progress-bar` widoczny |
| 2 | Oczekuj na załadowanie danych | `mat-progress-bar` | N/D | `mat-progress-bar` znika, formularz wyświetla dane firmy |
| 3 | Zweryfikuj Pole Nazwa firmy | `input[formControlName="firmName"]` | N/D | Pole wypełnione nazwą firmy z bazy |
| 4 | Zweryfikuj Pole CUI | `input[formControlName="cuiValue"]` | N/D | Pole wypełnione numerem CUI z bazy |
| 5 | Zweryfikuj Pole RegCom | `input[formControlName="regCom"]` | N/D | Pole wypełnione numerem RegCom (lub puste jeśli brak w bazie) |
| 6 | Zweryfikuj Pole Adres | `input[formControlName="address"]` | N/D | Pole wypełnione adresem z bazy |
| 7 | Zweryfikuj Pole Województwo | `input[formControlName="county"]` | N/D | Pole wypełnione województwem z bazy |
| 8 | Zweryfikuj Pole Miasto | `input[formControlName="city"]` | N/D | Pole wypełnione miastem z bazy |
| 9 | Zweryfikuj przycisk | `button[type="submit"]` | N/D | Przycisk wyświetla tekst "Update" |

---

## 2. Scenariusz: Edycja danych firmy — happy path

**Typ**: Happy Path  
**Cel**: Weryfikacja poprawnego zapisu zmodyfikowanych danych firmy  
**Warunek wstępny**: Ekran załadowany, formularz wypełniony danymi firmy

### Kroki testowe

| Lp. | Akcja | Selektor / Element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zmień wartość pola Nazwa firmy | `input[formControlName="firmName"]` | "Nowa Nazwa Firmy SRL" | Pole zaktualizowane, brak błędu walidacji |
| 2 | Zmień wartość pola Adres | `input[formControlName="address"]` | "Str. Exemplu nr. 42" | Pole zaktualizowane, brak błędu walidacji |
| 3 | Kliknij przycisk Zapis formularza | `button[type="submit"]` | N/D | Żądanie `PUT /Firm/EditFirm/false` wysłane |
| 4 | Zweryfikuj komunikat sukcesu | Komponent toastr | N/D | Komunikat: "Firm details updated successfully." (typ: success) |

---

## 3. Scenariusz: Walidacja pól wymaganych

**Typ**: Validation Test  
**Cel**: Weryfikacja poprawności walidacji pól wymaganych  
**Warunek wstępny**: Ekran załadowany

### Kroki testowe

| Lp. | Akcja | Selektor | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wyczyść Pole Nazwa firmy | `input[formControlName="firmName"]` | "" (puste) | Komunikat `mat-error`: "Firm Name is required" |
| 2 | Wyczyść Pole CUI | `input[formControlName="cuiValue"]` | "" (puste) | Komunikat `mat-error`: "CUI Value is required" |
| 3 | Wyczyść Pole Adres | `input[formControlName="address"]` | "" (puste) | Komunikat `mat-error`: "Address is required" |
| 4 | Wyczyść Pole Województwo | `input[formControlName="county"]` | "" (puste) | Komunikat `mat-error`: "County is required" |
| 5 | Wyczyść Pole Miasto | `input[formControlName="city"]` | "" (puste) | Komunikat `mat-error`: "City is required" |
| 6 | Kliknij przycisk Zapis formularza | `button[type="submit"]` | N/D | Formularz nie jest wysłany. Komunikat: "Please fill all the required fields" wyświetlony w `div.p-error` |

---

## 4. Scenariusz: Autouzupełnianie danych z ANAF

**Typ**: Integration Test  
**Cel**: Weryfikacja poprawnego pobierania i autouzupełniania danych z ANAF  
**Warunek wstępny**: Ekran załadowany, pole CUI wypełnione prawidłowym numerem CUI

### Kroki testowe

| Lp. | Akcja | Selektor | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wpisz numer CUI | `input[formControlName="cuiValue"]` | "12345678" | Pole CUI wypełnione |
| 2 | Kliknij przycisk Pobieranie danych z ANAF | `button mat-icon-button` (ikona `cloud_download`) | N/D | Żądanie `GET /Firm/fromAnaf/12345678` wysłane |
| 3 | Zweryfikuj autouzupełnianie Nazwa firmy | `input[formControlName="firmName"]` | N/D | Pole wypełnione wartością z odpowiedzi ANAF |
| 4 | Zweryfikuj autouzupełnianie RegCom | `input[formControlName="regCom"]` | N/D | Pole wypełnione wartością z odpowiedzi ANAF |
| 5 | Zweryfikuj autouzupełnianie Adres | `input[formControlName="address"]` | N/D | Pole wypełnione wartością z odpowiedzi ANAF |
| 6 | Zweryfikuj autouzupełnianie Województwo | `input[formControlName="county"]` | N/D | Pole wypełnione wartością z odpowiedzi ANAF |
| 7 | Zweryfikuj autouzupełnianie Miasto | `input[formControlName="city"]` | N/D | Pole wypełnione wartością z odpowiedzi ANAF |
| 8 | Zweryfikuj komunikat sukcesu | Komponent toastr | N/D | Komunikat: "Firm details fetched successfully." (typ: success) |
| 9 | Zweryfikuj edytowalność pól | Wszystkie pola | N/D | Pola pozostają edytowalne po autouzupełnieniu |

---

## 5. Scenariusz: Autouzupełnianie ANAF z pustym CUI

**Typ**: Edge Case  
**Cel**: Weryfikacja zachowania gdy CUI jest puste  
**Warunek wstępny**: Ekran załadowany, pole CUI puste

### Kroki testowe

| Lp. | Akcja | Selektor | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wyczyść Pole CUI | `input[formControlName="cuiValue"]` | "" (puste) | Pole CUI puste |
| 2 | Kliknij przycisk Pobieranie danych z ANAF | `button mat-icon-button` (ikona `cloud_download`) | N/D | [WYMAGA WERYFIKACJI — brak walidacji w kodzie; oczekiwane zachowanie: błąd API lub brak akcji] |

---

## 6. Scenariusz: Tworzenie nowej firmy (nowy użytkownik)

**Typ**: Happy Path  
**Cel**: Weryfikacja tworzenia firmy dla użytkownika bez istniejącej firmy  
**Warunek wstępny**: Użytkownik zalogowany, brak firmy w bazie (API zwraca firmę z `id === 0` lub `null`)

### Kroki testowe

| Lp. | Akcja | Selektor | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Nawiguj do ekranu | URL: `/dashboard/firm-details` | N/D | Formularz pusty, przycisk "Submit" widoczny |
| 2 | Wypełnij Pole Nazwa firmy | `input[formControlName="firmName"]` | "Test SRL" | Pole wypełnione |
| 3 | Wypełnij Pole CUI | `input[formControlName="cuiValue"]` | "99887766" | Pole wypełnione |
| 4 | Wypełnij Pole Adres | `input[formControlName="address"]` | "Str. Test 1" | Pole wypełnione |
| 5 | Wypełnij Pole Województwo | `input[formControlName="county"]` | "Bucuresti" | Pole wypełnione |
| 6 | Wypełnij Pole Miasto | `input[formControlName="city"]` | "Sector 1" | Pole wypełnione |
| 7 | Kliknij przycisk Zapis formularza | `button[type="submit"]` | N/D | Żądanie `POST /Firm/AddFirm/false` wysłane |
| 8 | Zweryfikuj komunikat sukcesu | Komponent toastr | N/D | Komunikat: "Firm details updated successfully." |

---

## 7. Scenariusz: Dostęp bez autoryzacji

**Typ**: Access Control  
**Cel**: Weryfikacja ochrony ekranu przed nieautoryzowanym dostępem  
**Warunek wstępny**: Użytkownik niezalogowany (brak tokena JWT)

### Kroki testowe

| Lp. | Akcja | Selektor | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Nawiguj bezpośrednio do `/dashboard/firm-details` | URL bar | N/D | `AuthGuard` blokuje dostęp |
| 2 | Zweryfikuj przekierowanie | URL | N/D | Użytkownik przekierowany do `/login` |

---

## 8. Tabela selektorów i lokalizatorów

| Element | Selektor CSS | Opis |
|---|---|---|
| Pole Nazwa firmy | `input[formControlName="firmName"]` | Input tekstowy w `mat-form-field` |
| Pole CUI | `input[formControlName="cuiValue"]` | Input tekstowy z przyciskiem ANAF |
| Pole RegCom | `input[formControlName="regCom"]` | Input tekstowy |
| Pole Adres | `input[formControlName="address"]` | Input tekstowy |
| Pole Województwo | `input[formControlName="county"]` | Input tekstowy |
| Pole Miasto | `input[formControlName="city"]` | Input tekstowy |
| Przycisk ANAF | `button[matSuffix] mat-icon-button` | Ikona `cloud_download` wewnątrz pola CUI |
| Przycisk Zapis | `button[type="submit"]` | `mat-raised-button` color primary |
| Pasek postępu | `mat-progress-bar` | Widoczny podczas ładowania |
| Komunikat błędu | `div.p-error` | Komunikat ogólny pod formularzem |
| Komunikat walidacji pola | `mat-error` | Pod polem z błędem walidacji |

---

## 9. Dane testowe

### Zestaw 1: Dane prawidłowe (edycja)

```json
{
  "firmName": "Exemplu SRL",
  "cuiValue": "12345678",
  "regCom": "J40/1234/2023",
  "address": "Str. Victoriei nr. 10",
  "county": "Bucuresti",
  "city": "Sector 3"
}
```

### Zestaw 2: Dane prawidłowe (tworzenie)

```json
{
  "firmName": "Noua Firma SRL",
  "cuiValue": "87654321",
  "regCom": null,
  "address": "Bd. Unirii nr. 5",
  "county": "Cluj",
  "city": "Cluj-Napoca"
}
```

### Zestaw 3: Dane z błędami walidacji

```json
{
  "firmName": "",
  "cuiValue": "",
  "regCom": "",
  "address": "",
  "county": "",
  "city": ""
}
```

---

## 10. Notatki dla testerów

- Pole RegCom posiada atrybut `required` w HTML ale nie posiada walidatora w TS — komunikat `mat-error` "Registration Number is required" nie zostanie wyświetlony przez Angular Reactive Forms. Zweryfikować czy to zamierzone zachowanie.
- Przycisk ANAF jest aktywny nawet gdy pole CUI jest puste — zweryfikować zachowanie API przy pustym parametrze.
- Brak jawnej obsługi błędów API — zweryfikować czy interceptor globalny wyświetla komunikaty błędów.
- Po zapisie formularza ekran nie odświeża danych z API — zweryfikować czy dane w formularzu odpowiadają danym w bazie.

---

## Poprzednie sekcje

- Metadane: [00_METADANE.md](00_METADANE.md)
- Przegląd: [01_PRZEGLĄD.md](01_PRZEGLĄD.md)
- Dane i operacje: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)
- Logika biznesowa: [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md)
