# P-06 — Jak wystawić fakturę

## Lista kontrolna — zanim zaczniesz
- ✅ [Uzupełnione dane firmy](P-03_konfiguracja_firmy.md) → [ekran Dane firmy](../01_ekrany/05_dane_firmy.md)
- ✅ [Skonfigurowana seria dokumentów dla faktur](P-05b_konfiguracja_serii.md) → [ekran Serie dokumentów](../01_ekrany/09_serie_dokumentow.md)
- ✅ Klient w bazie lub gotowość do jego dodania → [ekran Klienci](../01_ekrany/06_klienci.md)

---

## Kroki

### 1. Otwórz formularz nowej faktury
W [menu bocznym](../01_ekrany/03_nawigacja.md) kliknij **Invoices** → [Lista faktur](../01_ekrany/10_faktury.md) → kliknij **Add Invoice** → [Formularz faktury](../01_ekrany/10b_formularz_faktury.md).

### 2. Wybierz klienta
W polu **Client** wpisz kilka liter nazwy — pojawi się lista podpowiedzi z [bazy klientów](../01_ekrany/06_klienci.md). Kliknij właściwego klienta.

> Jeśli klienta nie ma na liście — wyjdź, przejdź do [Klientów](../01_ekrany/06_klienci.md), dodaj go ([P-08](P-08_dodawanie_kontrahenta.md)), wróć i kontynuuj.

### 3. Wybierz serię dokumentu
W polu **Document Series** wybierz serię z listy → [Serie dokumentów](../01_ekrany/09_serie_dokumentow.md). Numer faktury zostanie nadany automatycznie.

### 4. Ustaw daty
- **Issue Date** — data wystawienia (domyślnie dzisiaj)
- **Due Date** — termin płatności

### 5. Ustaw status płatności
- **Unpaid** — faktura nieopłacona (domyślnie)
- **Paid** — faktura już opłacona

### 6. Dodaj pozycje
Kliknij **Add Product** (lub „+") dla każdej pozycji:

| Pole | Co wpisać |
|---|---|
| **Name** | Wpisz nazwę lub wybierz z [katalogu produktów](../01_ekrany/08_produkty.md) |
| **Unit Price** | Cena jednostkowa |
| **Quantity** | Ilość |
| **Unit of Measurement** | Jednostka miary |
| **TVA Value** | Stawka VAT (%) |
| **Contains TVA** | Zaznacz jeśli cena jest brutto |

Wartość każdej pozycji wylicza się automatycznie. Powtórz dla każdej pozycji.

### 7. Zapisz fakturę
Kliknij **Save** ✅ — faktura pojawi się na [liście faktur](../01_ekrany/10_faktury.md).

### 8. (Opcjonalnie) Wygeneruj PDF
- **Preview PDF** — podgląd w oknie → szczegóły: [P-10](P-10_generowanie_pdf.md)
- **Generate PDF** — generuje plik PDF

---

## Edycja istniejącej faktury
Na [liście faktur](../01_ekrany/10_faktury.md) kliknij na wiersz faktury → [formularz edycji](../01_ekrany/10b_formularz_faktury.md) → zmień dane → **Save**.

---

## FAQ

**Czy mogę wystawić fakturę bez klienta z bazy?**
Nie — najpierw dodaj klienta: [P-08 Dodanie kontrahenta](P-08_dodawanie_kontrahenta.md).

**Czy mogę wpisać produkt spoza katalogu?**
Tak — wpisz nazwę ręcznie. Podpowiedzi z [katalogu produktów](../01_ekrany/08_produkty.md) są tylko ułatwieniem.

**Jak wystawić fakturę korygującą?**
→ [P-07 Faktura korygująca (storno)](P-07_faktura_korygujaca.md)
