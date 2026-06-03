# P-07 — Jak wystawić fakturę korygującą (storno)

## Kiedy?
- Gdy popełniono błąd na fakturze i trzeba ją formalnie anulować lub poprawić
- Gdy klient zwrócił towar lub zrezygnował z usługi po wystawieniu faktury

> Faktura korygująca (storno) **nie jest tworzona od zera**. Aplikacja tworzy ją automatycznie na podstawie wskazanej faktury pierwotnej.

---

## Kroki

### 1. Przejdź do listy faktur
W [menu bocznym](../01_ekrany/03_nawigacja.md) kliknij **Invoices** → [Lista faktur](../01_ekrany/10_faktury.md).

### 2. Znajdź fakturę do skorygowania
Przewiń listę lub kliknij nagłówek kolumny, żeby posortować i łatwiej znaleźć właściwą fakturę.

### 3. Zaznacz fakturę
Kliknij checkbox (☐) po lewej stronie wiersza.

### 4. Kliknij „Transform to Storno"
Przycisk pojawi się po zaznaczeniu. Kliknij go.

### 5. Storno zostało utworzone ✅
System tworzy nowy dokument korygujący. Pojawi się na liście [Storn](../01_ekrany/12_storna.md).

### 6. (Opcjonalnie) Edytuj storno
1. W [menu bocznym](../01_ekrany/03_nawigacja.md) kliknij **Invoice Stornos** → [Lista storn](../01_ekrany/12_storna.md)
2. Kliknij na wiersz storna → [Formularz](../01_ekrany/10b_formularz_faktury.md)
3. Zmień dane → **Save**

### 7. (Opcjonalnie) Wygeneruj PDF
Z [formularza storna](../01_ekrany/10b_formularz_faktury.md) kliknij **Generate PDF** → [P-10](P-10_generowanie_pdf.md).

---

## FAQ

**Czy oryginalna faktura zostaje usunięta?**
Nie. Pozostaje na [liście faktur](../01_ekrany/10_faktury.md). Obok niej istnieje teraz dokument korygujący na [liście storn](../01_ekrany/12_storna.md).

**Czy mogę zrobić storno do proformy?**
Nie — opcja „Transform to Storno" działa wyłącznie dla faktur zwykłych → [Faktury](../01_ekrany/10_faktury.md).

**Czy mogę zaznaczyć kilka faktur naraz?**
Tak — dla każdej zaznaczonej faktury zostanie utworzone oddzielne storno.
