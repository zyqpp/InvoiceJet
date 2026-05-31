# Formularz faktury — dodawanie i edycja

## Co to jest?
Formularz do wystawienia nowej faktury lub edycji istniejącej. Działa tak samo dla faktur zwykłych i proform — różni je tylko typ dokumentu.

## Sekcja: dane dokumentu

| Pole | Opis |
|---|---|
| **Client** | Kontrahent — wpisz fragment nazwy, a system podpowie z Twojej bazy klientów |
| **Document Series** | Seria numeracyjna — wybierz z listy (wcześniej skonfigurowanej) |
| **Issue Date** | Data wystawienia — wybierz z kalendarza |
| **Due Date** | Termin płatności — wybierz z kalendarza |
| **Status** | Status płatności: **Unpaid** (nieopłacona) lub **Paid** (opłacona) |

## Sekcja: pozycje faktury (tabela produktów)

Tutaj dodajesz, co sprzedajesz. Każda pozycja to jeden wiersz tabeli.

| Kolumna | Opis |
|---|---|
| **Name** | Nazwa produktu/usługi — wpisz ręcznie lub wybierz z katalogu |
| **Unit Price** | Cena za jednostkę |
| **Quantity** | Ilość |
| **Unit of Measurement** | Jednostka miary (szt., kg, godz. itd.) |
| **TVA Value** | Stawka VAT (%) |
| **Contains TVA** | Czy podana cena jest brutto (z VAT) |
| **Total Price** | Wartość wiersza (wyliczana automatycznie) |
| **Actions** | Usuń tę pozycję |

## Przyciski akcji

| Przycisk | Co robi |
|---|---|
| **Add Product** (lub „+") | Dodaje nowy wiersz do tabeli pozycji |
| **Save** | Zapisuje fakturę |
| **Preview PDF** | Otwiera podgląd faktury w formacie PDF (bez zapisywania) |
| **Generate PDF** | Generuje i zapisuje plik PDF faktury |

## Podgląd PDF
Po kliknięciu **Preview PDF** otworzy się okno z gotowym dokumentem. Możesz go obejrzeć, a następnie zamknąć okno i wrócić do edycji.

## Ważne informacje
- Przed wystawieniem faktury musisz mieć uzupełnione [dane firmy](05_dane_firmy.md) i przynajmniej jedną [serię dokumentów](09_serie_dokumentow.md)
- Klientów możesz dodawać do bazy na bieżąco — jeśli nie ma go na liście podpowiedzi, wejdź do zakładki [Klienci](06_klienci.md) i dodaj go tam najpierw
- Pozycje faktury możesz wpisać ręcznie lub skorzystać z podpowiedzi z [katalogu produktów](08_produkty.md)
- Wartość każdej pozycji i suma całkowita są wyliczane automatycznie
