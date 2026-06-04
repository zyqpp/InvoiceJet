# Invoice Details — Scenariusze Testowe

**Przeznaczenie:** Dokument dla QA — kroki testowe, selektory, dane wejściowe

---

## 1. Scenariusz: Otwarcie ekranu dodawania faktury

**Typ:** Happy Path  
**Cel:** Weryfikacja inicjalizacji formularza dodawania faktury.  
**Warunek wstępny:** Użytkownik jest zalogowany. API zwraca dane autouzupełniania.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu dodawania faktury. | URL `/dashboard/add-invoice` | N/D | Ekran Invoice Details jest widoczny. |
| 2 | Poczekaj na zakończenie ładowania. | `mat-progress-bar` | N/D | Pasek ładowania znika. |
| 3 | Sprawdź pole Document Series. | `mat-select[formControlName="documentSeries"]` | N/D | Pole jest widoczne w trybie dodawania. |
| 4 | Sprawdź grid pozycji. | `table[mat-table]` | N/D | Widoczny jest jeden domyślny wiersz pozycji. |
| 5 | Sprawdź przycisk zapisu. | `button[type="submit"]` | N/D | Widoczny jest przycisk `Issue`. |

---

## 2. Scenariusz: Otwarcie ekranu edycji faktury

**Typ:** Happy Path  
**Cel:** Weryfikacja inicjalizacji formularza edycji faktury.  
**Warunek wstępny:** Użytkownik jest zalogowany. Istnieje dokument o podanym `id`.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu edycji faktury. | URL `/dashboard/edit-invoice/7` | N/D | Ekran Invoice Details jest widoczny. |
| 2 | Poczekaj na pobranie dokumentu. | `form[formGroup]` | N/D | Formularz jest wypełniony danymi dokumentu. |
| 3 | Sprawdź tytuł. | `h1` | N/D | Tytuł zawiera `Invoice Details -` i numer dokumentu. |
| 4 | Sprawdź chip statusu. | `mat-chip` | N/D | Widoczny jest status dokumentu. |
| 5 | Sprawdź pole Status. | `mat-select[formControlName="documentStatus"]` | N/D | Pole jest widoczne w trybie edycji. |
| 6 | Sprawdź przyciski. | `.controls button` | N/D | Widoczne są przyciski `Update` i `Preview`. |

---

## 3. Scenariusz: Wybór klienta przez autouzupełnianie

**Typ:** Functional  
**Cel:** Weryfikacja pola `Client Name or CUI`.  
**Warunek wstępny:** Formularz jest załadowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole klienta. | `input[formControlName="client"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz fragment nazwy albo CUI. | `input[formControlName="client"]` | `five` | Lista autouzupełniania filtruje klientów po nazwie albo CUI. |
| 3 | Wybierz opcję klienta. | `mat-option` | N/D | Pole przyjmuje obiekt `IFirm`, a w polu widoczna jest nazwa klienta. |

---

## 4. Scenariusz: Wybór produktu i autouzupełnienie pozycji

**Typ:** Functional  
**Cel:** Weryfikacja pola `Product Name`.  
**Warunek wstępny:** Formularz zawiera co najmniej jeden wiersz pozycji.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij pole Product Name. | `input[formControlName="name"]` | N/D | Pole przyjmuje fokus. |
| 2 | Wpisz fragment nazwy produktu. | `input[formControlName="name"]` | `logo` | Lista autouzupełniania filtruje produkty po nazwie. |
| 3 | Wybierz produkt. | `mat-option` | N/D | Pola `unitPrice`, `unitOfMeasurement`, `tvaValue` i `containsTva` są uzupełnione. |
| 4 | Sprawdź cenę całkowitą. | `input[formControlName="totalPrice"]` | N/D | Pole `totalPrice` zawiera przeliczoną wartość. |

---

## 5. Scenariusz: Dodanie i usunięcie pozycji dokumentu

**Typ:** Functional  
**Cel:** Weryfikacja dynamicznego `FormArray`.  
**Warunek wstępny:** Formularz jest załadowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij przycisk Add w kolumnie Actions. | `button[matTooltip="Add"]` | N/D | Do gridu dodany jest nowy wiersz pozycji. |
| 2 | Sprawdź przycisk Remove. | `button[color="warn"]` | N/D | Przycisk Remove jest widoczny, gdy liczba pozycji jest większa niż `1`. |
| 3 | Kliknij przycisk Remove w jednym wierszu. | `button[color="warn"]` | N/D | Wiersz jest usunięty z gridu. |

---

## 6. Scenariusz: Przeliczenie ceny całkowitej

**Typ:** Functional  
**Cel:** Weryfikacja przeliczenia `totalPrice`.  
**Warunek wstępny:** Formularz zawiera jeden wiersz pozycji.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wpisz cenę jednostkową. | `input[formControlName="unitPrice"]` | `100` | Pole zawiera wartość `100`. |
| 2 | Wpisz ilość. | `input[formControlName="quantity"]` | `2` | Pole zawiera wartość `2`. |
| 3 | Wpisz TVA. | `input[formControlName="tvaValue"]` | `19` | Pole zawiera wartość `19`. |
| 4 | Opuść pole, aby wywołać `(change)`. | `input[formControlName="tvaValue"]` | N/D | `totalPrice` przyjmuje wartość `238`. |

---

## 7. Scenariusz: Zapis nowej faktury

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji `Issue`.  
**Warunek wstępny:** Ekran `/dashboard/add-invoice` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Wypełnij wymagane pola nagłówka. | Pola formularza | Klient, data wystawienia, seria dokumentu | Formularz zawiera wymagane dane. |
| 2 | Wypełnij pozycję dokumentu. | Pola w gridzie | Produkt, cena, ilość, TVA | Pozycja ma poprawne wartości. |
| 3 | Kliknij Issue. | `button[type="submit"]` | N/D | Wywołana jest operacja dodania dokumentu. |
| 4 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Document added successfully`. |
| 5 | Sprawdź nawigację. | URL przeglądarki | N/D | Aplikacja przechodzi do `/dashboard/invoices`. |

---

## 8. Scenariusz: Zapis edytowanej faktury

**Typ:** Happy Path  
**Cel:** Weryfikacja operacji `Update`.  
**Warunek wstępny:** Ekran `/dashboard/edit-invoice/:id` jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Zmień wartość wybranego pola. | Dowolne edytowalne pole formularza | Nowa wartość | Pole zawiera nową wartość. |
| 2 | Kliknij Update. | `button[type="submit"]` | N/D | Wywołana jest operacja edycji dokumentu. |
| 3 | Sprawdź komunikat sukcesu. | `.toast-success` | N/D | Widoczny jest komunikat `Document updated successfully`. |
| 4 | Sprawdź nawigację. | URL przeglądarki | N/D | Aplikacja przechodzi do `/dashboard/invoices`. |

---

## 9. Scenariusz: Podgląd PDF

**Typ:** Functional  
**Cel:** Weryfikacja dialogu `PdfViewerComponent`.  
**Warunek wstępny:** Ekran edycji faktury jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Kliknij Preview. | Przycisk `Preview` w `.controls` | N/D | Wywołane jest pobranie strumienia PDF. |
| 2 | Poczekaj na odpowiedź. | `mat-dialog-container` | N/D | Otwiera się dialog podglądu PDF. |
| 3 | Sprawdź PDF. | `iframe.pdf-iframe` | N/D | `iframe` renderuje dokument PDF. |
| 4 | Kliknij Close. | `button[aria-label="Close PDF viewer"]` | N/D | Dialog jest zamknięty. |

---

## 10. Scenariusz: Walidacja formularza

**Typ:** Validation Test  
**Cel:** Weryfikacja blokady zapisu dla niepoprawnego formularza.  
**Warunek wstępny:** Ekran dodawania faktury jest otwarty.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Usuń wartość pola Issue Date. | `input[formControlName="issueDate"]` | Pusty tekst | Widoczny jest komunikat `Issue Date is required`. |
| 2 | Usuń nazwę produktu. | `input[formControlName="name"]` | Pusty tekst | Formularz staje się niepoprawny. |
| 3 | Kliknij Issue. | `button[type="submit"]` | N/D | `onSubmit()` kończy działanie bez wywołania zapisu. |

---

## 11. Scenariusz: Dostęp bez logowania

**Typ:** Access Control  
**Cel:** Weryfikacja działania `AuthGuard`.  
**Warunek wstępny:** Użytkownik nie jest zalogowany.

| Lp. | Akcja | Selektor / element | Dane wejściowe | Oczekiwany rezultat |
|---|---|---|---|---|
| 1 | Przejdź do ekranu dodawania faktury. | URL `/dashboard/add-invoice` | N/D | `AuthGuard` blokuje dostęp. |
| 2 | Sprawdź przekierowanie. | URL przeglądarki | N/D | Aplikacja przekierowuje do `/login`. |

---

## 12. Tabela selektorów

| Element | Selektor CSS / Angular |
|---|---|
| Formularz faktury | `form[formGroup]` |
| Pole klienta | `input[formControlName="client"]` |
| Pole Issue Date | `input[formControlName="issueDate"]` |
| Pole Due Date | `input[formControlName="dueDate"]` |
| Pole Document Series | `mat-select[formControlName="documentSeries"]` |
| Pole Status | `mat-select[formControlName="documentStatus"]` |
| Grid pozycji | `table[mat-table]` |
| Pole Product Name | `input[formControlName="name"]` |
| Pole Unit Price | `input[formControlName="unitPrice"]` |
| Pole Quantity | `input[formControlName="quantity"]` |
| Pole Unit of Measurement | `input[formControlName="unitOfMeasurement"]` |
| Pole TVA Value | `input[formControlName="tvaValue"]` |
| Pole Contains TVA | `mat-checkbox[formControlName="containsTva"]` |
| Pole Total Price | `input[formControlName="totalPrice"]` |
| Dialog PDF | `mat-dialog-container` |
| PDF iframe | `iframe.pdf-iframe` |

---

## 13. Dane testowe

### 13.1 Dane poprawne pozycji

```json
{
  "name": "Design Logo Vectorizat Five Star Solutions",
  "unitPrice": 100,
  "quantity": 2,
  "unitOfMeasurement": "buc",
  "tvaValue": 19,
  "containsTva": false,
  "totalPrice": 238
}
```

### 13.2 Dane niepoprawne pozycji

```json
{
  "name": "",
  "unitPrice": -1,
  "quantity": 0,
  "unitOfMeasurement": "",
  "tvaValue": -1,
  "containsTva": false,
  "totalPrice": -1
}
```
