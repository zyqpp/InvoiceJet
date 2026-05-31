# Jak wystawić fakturę

## Zanim zaczniesz — lista kontrolna
Upewnij się, że masz już:
- ✅ [Uzupełnione dane firmy](P-03_konfiguracja_firmy.md)
- ✅ [Skonfigurowaną serię dokumentów dla faktur](P-05b_konfiguracja_serii.md)
- ✅ Klienta w bazie lub gotowość do wpisania danych ręcznie

---

## Kroki

### 1. Otwórz formularz nowej faktury
W menu bocznym kliknij **Invoices**, następnie kliknij przycisk **Add Invoice**.

### 2. Wybierz klienta
W polu **Client** wpisz kilka liter nazwy firmy — pojawi się lista podpowiedzi z Twojej bazy kontrahentów. Kliknij właściwego klienta.

> Jeśli klienta nie ma na liście — wyjdź, przejdź do **Clients**, dodaj go, wróć i wystaw fakturę.

### 3. Wybierz serię dokumentu
W polu **Document Series** wybierz serię numeracyjną z listy. Numer faktury zostanie nadany automatycznie.

### 4. Ustaw daty
- **Issue Date** — data wystawienia (domyślnie dzisiaj)
- **Due Date** — termin płatności

### 5. Wybierz status płatności
- **Unpaid** — faktura jeszcze nieopłacona (domyślnie)
- **Paid** — faktura już opłacona

### 6. Dodaj pozycje (produkty/usługi)
Kliknij **Add Product** (lub „+"), aby dodać wiersz w tabeli pozycji. Dla każdej pozycji:

| Pole | Co wpisać |
|---|---|
| **Name** | Wpisz nazwę lub zacznij pisać, żeby wybrać z katalogu |
| **Unit Price** | Cena jednostkowa |
| **Quantity** | Ilość |
| **Unit of Measurement** | Jednostka miary (szt., godz. itp.) |
| **TVA Value** | Stawka VAT (%) |
| **Contains TVA** | Czy cena jest brutto? |

Wartość wiersza (**Total Price**) zostanie wyliczona automatycznie.

Powtórz dla każdej pozycji. Wiersze możesz usuwać ikoną w kolumnie **Actions**.

### 7. Zapisz fakturę
Kliknij **Save**. Faktura jest zapisana i pojawi się na liście faktur.

### 8. (Opcjonalnie) Wygeneruj lub podejrzyj PDF
- **Preview PDF** — podgląd faktury w oknie (bez zapisywania pliku)
- **Generate PDF** — generuje plik PDF faktury

---

## Edycja istniejącej faktury
W menu **Invoices** kliknij na wiersz faktury — otworzy się ten sam formularz z wypełnionymi danymi. Zmień co trzeba i kliknij **Save**.

---

## Często zadawane pytania

**Czy mogę wystawić fakturę bez klienta z bazy?**
Aplikacja wymaga wybrania klienta z listy podpowiedzi — najpierw dodaj go w sekcji Clients.

**Czy mogę dodać produkt spoza katalogu?**
Tak — po prostu wpisz nazwę ręcznie. Podpowiedzi z katalogu pojawiają się tylko jeśli taki produkt tam istnieje, ale nie musisz z nich korzystać.

**Jak poprawić wystawioną fakturę?**
Kliknij na nią na liście i edytuj. Jeśli faktura wymaga korekty formalnej (anulowania), użyj opcji [Transform to Storno](P-07_faktura_korygujaca.md).
