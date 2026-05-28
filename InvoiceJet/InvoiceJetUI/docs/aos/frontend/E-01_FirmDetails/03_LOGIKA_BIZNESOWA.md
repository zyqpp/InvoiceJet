# Szczegóły firmy — Logika Biznesowa

---

## 1. Przepływy danych

### 1.1 Pobieranie danych firmy (Read)

**Scenariusz**: Załadowanie ekranu Szczegóły firmy

1. Użytkownik nawiguje do ekranu (URL: `/dashboard/firm-details`)
2. Guard: `AuthGuard` sprawdza uprawnienia (obecność tokena JWT)
3. Komponent: `FirmDetailsComponent` w `ngOnInit()` wywołuje serwis
4. Serwis: `FirmService.getUserActiveFirm()`
5. Żądanie HTTP: `GET /Firm/GetUserActiveFirm/`
6. Odpowiedź API: Obiekt `IFirm` (dane firmy użytkownika)
7. Transformacja: Brak transformacji — dane mapowane bezpośrednio na pola formularza
8. Renderowanie: Formularz reaktywny `firmDetailsForm` wypełniany przez `patchValue()`

**Diagram przepływu**:
```
ngOnInit()
    ↓
firmService.getUserActiveFirm()
    ↓
httpClient.get<IFirm>('/Firm/GetUserActiveFirm/')
    ↓
subscribe({ next: (firm) => ... })
    ↓
if (firm) → this.currentUserFirm = firm
    ↓
firmDetailsForm.patchValue({
    firmName: firm.name,
    cuiValue: firm.cui,
    regCom: firm.regCom,
    address: firm.address,
    county: firm.county,
    city: firm.city
})
    ↓
this.initialFormValues = firmDetailsForm.value
    ↓
Template: mat-progress-bar znika (*ngIf="!currentUserFirm")
```

**Mapping pól API → Formularz**:

| Pole `IFirm` | `formControlName` | Typ |
|---|---|---|
| `name` | `firmName` | `string` |
| `cui` | `cuiValue` | `string` |
| `regCom` | `regCom` | `string \| null` |
| `address` | `address` | `string` |
| `county` | `county` | `string` |
| `city` | `city` | `string` |

---

### 1.2 Edycja danych firmy (Write — tryb edycji)

**Scenariusz**: Zapis formularza — firma istnieje (`currentUserFirm.id !== 0`)

1. Użytkownik modyfikuje pola formularza i klika przycisk Zapis formularza
2. Walidacja frontendowa: `if (this.firmDetailsForm.invalid) return`
3. Przygotowanie danych:
   - Pobranie wartości z `firmDetailsForm.value`
   - Konstrukcja obiektu `IFirm` z polami z formularza i `id` z `currentUserFirm`
4. Serwis: `FirmService.editFirm(firm, false)`
5. Żądanie HTTP: `PUT /Firm/EditFirm/false`
6. Body: Obiekt `IFirm`
7. Odpowiedź API: Obiekt `IFirm` (zaktualizowany rekord)
8. Obsługa sukcesu: Komunikat `ToastrService`: "Firm details updated successfully."

**Kod (schema)**:
```typescript
const firm: IFirm = {
  id: this.currentUserFirm?.id! ?? 0,
  name: this.firmDetailsForm.value.firmName!,
  cui: this.firmDetailsForm.value.cuiValue!,
  regCom: this.firmDetailsForm.value.regCom! ?? null,
  address: this.firmDetailsForm.value.address!,
  county: this.firmDetailsForm.value.county!,
  city: this.firmDetailsForm.value.city!,
};

this.firmService.editFirm(firm, false).subscribe({
  next: () => {
    this.toastr.success("Firm details updated successfully.", "Success");
  },
});
```

---

### 1.3 Tworzenie nowej firmy (Write — tryb tworzenia)

**Scenariusz**: Zapis formularza — firma nie istnieje (`currentUserFirm.id === 0`)

Przepływ identyczny jak w sekcji 1.2, z jedną różnicą:

- Serwis: `FirmService.addFirm(firm, false)`
- Żądanie HTTP: `POST /Firm/AddFirm/false`
- Body: Obiekt `IFirm` z `id: 0`
- Komunikat sukcesu: "Firm details updated successfully." (identyczny jak w trybie edycji)

---

### 1.4 Autouzupełnianie z ANAF (Read — integracja zewnętrzna)

**Scenariusz**: Pobieranie danych z ANAF na podstawie CUI

1. Użytkownik klika przycisk Pobieranie danych z ANAF (ikona `cloud_download`)
2. Komponent: `FirmDetailsComponent.onCloudIconClick()`
3. Odczytanie wartości CUI: `this.firmDetailsForm.value.cuiValue`
4. Serwis: `FirmService.getFirmFromAnaf(cuiValue)`
5. Żądanie HTTP: `GET /Firm/fromAnaf/{cuiValue}`
6. Odpowiedź API: Obiekt `IFirm` (dane firmy z rejestru ANAF)
7. Autouzupełnianie: `firmDetailsForm.patchValue()` — pola: `firmName`, `regCom`, `address`, `county`, `city`
8. Komunikat sukcesu: "Firm details fetched successfully."

**Diagram przepływu**:
```
onCloudIconClick()
    ↓
firmService.getFirmFromAnaf(firmDetailsForm.value.cuiValue)
    ↓
httpClient.get<IFirm>('/Firm/fromAnaf/{cuiValue}')
    ↓
subscribe({ next: (firm) => ... })
    ↓
firmDetailsForm.patchValue({
    firmName: firm.name,
    regCom: firm.regCom,
    address: firm.address,
    county: firm.county,
    city: firm.city
})
    ↓
toastr.success("Firm details fetched successfully.", "Success")
```

**Pola autouzupełniane przez ANAF**:

| Pole `IFirm` z ANAF | `formControlName` | Autouzupełniane |
|---|---|---|
| `name` | `firmName` | Tak |
| `cui` | `cuiValue` | **Nie** — pole CUI jest źródłem zapytania, nie jest nadpisywane |
| `regCom` | `regCom` | Tak |
| `address` | `address` | Tak |
| `county` | `county` | Tak |
| `city` | `city` | Tak |

---

## 2. Reguły biznesowe

### 2.1 Reguły walidacji

| Reguła | Opis | Implementacja | Komunikat |
|---|---|---|---|
| Nazwa firmy wymagana | Pole Nazwa firmy musi mieć wartość | Frontend: `Validators.required` | "Firm Name is required" |
| CUI wymagane | Pole CUI musi mieć wartość | Frontend: `Validators.required` | "CUI Value is required" |
| Adres wymagany | Pole Adres musi mieć wartość | Frontend: `Validators.required` | "Address is required" |
| Województwo wymagane | Pole Województwo musi mieć wartość | Frontend: `Validators.required` | "County is required" |
| Miasto wymagane | Pole Miasto musi mieć wartość | Frontend: `Validators.required` | "City is required" |

### 2.2 Logika specjalna

**Reguła 1: Rozróżnienie trybu edycji i tworzenia**
- **Wyzwalacz**: Kliknięcie przycisku Zapis formularza
- **Warunek**: `this.currentUserFirm.id !== 0`
- **Akcja trybu edycji**: Wywołanie `PUT /Firm/EditFirm/false`
- **Akcja trybu tworzenia**: Wywołanie `POST /Firm/AddFirm/false`
- **Skutek UI**: Etykieta przycisku zmienia się: "Update" (edycja) lub "Submit" (tworzenie)

**Reguła 2: Parametr `isClient` zawsze `false`**
- **Kontekst**: Ekran Szczegóły firmy dotyczy firmy użytkownika (wystawcy), nie klienta (odbiorcy)
- **Implementacja**: Wywołania `addFirm(firm, false)` i `editFirm(firm, false)` — parametr `isClient` ustawiony na `false`
- **Skutek**: Backend rozróżnia firmę użytkownika od klientów na podstawie tego parametru

---

## 3. Integracje z API

### 3.1 Endpointy używane w ekranie

| Endpoint | Metoda | Opis | Parametry | Odpowiedź | Serwis |
|---|---|---|---|---|---|
| `/Firm/GetUserActiveFirm/` | `GET` | Pobieranie danych firmy użytkownika | Brak (identyfikacja po tokenie JWT) | `IFirm` | `FirmService.getUserActiveFirm()` |
| `/Firm/EditFirm/false` | `PUT` | Aktualizacja danych firmy użytkownika | Body: `IFirm`, Path: `isClient=false` | `IFirm` | `FirmService.editFirm(firm, false)` |
| `/Firm/AddFirm/false` | `POST` | Tworzenie nowej firmy użytkownika | Body: `IFirm`, Path: `isClient=false` | `IFirm` | `FirmService.addFirm(firm, false)` |
| `/Firm/fromAnaf/{cuiValue}` | `GET` | Pobieranie danych firmy z ANAF | Path: `cuiValue` (string) | `IFirm` | `FirmService.getFirmFromAnaf(cuiValue)` |

### 3.2 Obsługa błędów HTTP

| Status | Obsługa w kodzie | Uwagi |
|---|---|---|
| 200 OK | Komunikat sukcesu (toastr) | Jedyny obsługiwany scenariusz |
| 400–500 | Brak jawnej obsługi | [WYMAGA WERYFIKACJI — czy interceptor HTTP aplikacji obsługuje błędy globalnie] |

---

## 4. Warunki biznesowe i dostępność

### 4.1 Warunki wyświetlania elementów

| Element | Warunek widoczności | Kod |
|---|---|---|
| `mat-progress-bar` | Widoczny gdy firma nie jest załadowana | `*ngIf="!currentUserFirm"` |
| Komunikat błędu formularza | Widoczny gdy `errorMessage` nie jest `null` | `*ngIf="errorMessage"` |
| Etykieta przycisku "Update" | Widoczna gdy firma użytkownika istnieje | `{{ currentUserFirm ? "Update" : "Submit" }}` |

### 4.2 Warunki dostępności operacji

| Operacja | Warunek dostępności | Efekt gdy niedostępna |
|---|---|---|
| Zapis formularza | `firmDetailsForm.valid === true` (sprawdzane w `onSubmit()`) | Metoda przerywa wykonanie (`return`), komunikat: "Please fill all the required fields" |
| Pobieranie danych z ANAF | Brak warunku — przycisk zawsze aktywny | N/D |

---

## 5. Logika powiązań między polami (Cascading)

**Powiązanie 1: Autouzupełnianie z ANAF**
- **Pole wyzwalające**: Pole CUI (pośrednio — przez kliknięcie przycisku `cloud_download`)
- **Pola zależne**: Nazwa firmy, RegCom, Adres, Województwo, Miasto
- **Logika**: Kliknięcie przycisku Pobieranie danych z ANAF wywołuje API z wartością CUI i wypełnia 5 pól formularza wartościami z odpowiedzi
- **Kod**:
  ```typescript
  this.firmService.getFirmFromAnaf(this.firmDetailsForm.value.cuiValue)
    .subscribe({
      next: (firm) => {
        this.firmDetailsForm.patchValue({
          firmName: firm.name,
          regCom: firm.regCom,
          address: firm.address,
          county: firm.county,
          city: firm.city,
        });
      },
    });
  ```

---

## 6. Znane problemy i uwagi

| Problem | Opis | Priorytet | Status |
|---|---|---|---|
| Niespójność walidacji pola RegCom | HTML zawiera `required` i `mat-error`, ale `FormControl` w TS nie posiada `Validators.required`. Komunikat błędu nie zostanie wyświetlony. | Średni | [WYMAGA WERYFIKACJI Z ZESPOŁEM] |
| Bug w `isFormChanged()` | Metoda porównuje `this.initialFormValues.value` z `this.initialFormValues` zamiast `this.firmDetailsForm.value` z `this.initialFormValues`. Zawsze zwraca `true`. Metoda nie jest używana w szablonie. | Niski | [WYMAGA WERYFIKACJI Z ZESPOŁEM] |
| Brak obsługi błędów API | Subskrypcje w `onSubmit()` i `onCloudIconClick()` nie zawierają bloku `error`. Błędy HTTP nie są obsługiwane jawnie. | Wysoki | [WYMAGA WERYFIKACJI — czy interceptor globalny obsługuje błędy] |
| Brak walidacji CUI przed wywołaniem ANAF | Przycisk ANAF jest aktywny nawet gdy pole CUI jest puste. Wywołanie API z pustym CUI. | Średni | [WYMAGA WERYFIKACJI Z ZESPOŁEM] |
| Martwa metoda `addNewClient()` | Metoda w TS zawiera tylko `console.log("Add new client")`. Nie jest wywoływana z szablonu HTML. | Niski | [WYMAGA WERYFIKACJI — czy metoda jest planowana do usunięcia] |
| Brak odświeżenia danych po zapisie | Po pomyślnym zapisie ekran nie wywołuje ponownie `getUserActiveFirm()`. Dane w formularzu mogą być niezsynchronizowane z bazą. | Średni | [WYMAGA WERYFIKACJI Z ZESPOŁEM] |
| `initialFormValues` zapisywany przed odpowiedzią API | W `ngOnInit()` wartość `initialFormValues` jest przypisywana synchronicznie, przed zakończeniem asynchronicznego `subscribe()`. Wartości inicjalne mogą zawierać puste pola zamiast danych z API. | Średni | [WYMAGA WERYFIKACJI Z ZESPOŁEM] |

---

## Poprzednie sekcje

- Metadane: [00_METADANE.md](00_METADANE.md)
- Przegląd: [01_PRZEGLĄD.md](01_PRZEGLĄD.md)
- Dane i operacje: [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md)

## Następna sekcja

- Scenariusze testowe: [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md)
