# Słownik pojęć domenowych i biznesowych
## Wytyczne językowe AOS — Część 3 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS dla aplikacji InvoiceJet  
**Zasada:** Pojęcia domenowe mają ściśle określone znaczenie w kontekście tej aplikacji. Polskie odpowiedniki (NIP, KRS, VAT) są niedopuszczalne jako zamienniki rumuskich odpowiedników (CUI, RegCom, TVA).

---

## 1. Typy dokumentów finansowych

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **dokument** | Ogólna nazwa dla faktury, faktury proforma lub faktury storno wytworzonych w systemie. Odpowiada encji `Document` w bazie. | pismo, zapis finansowy |
| **faktura** | Dokument sprzedaży. Typ: `Factura`. Dokument księgowy. | invoice (w opisach biznesowych po polsku) |
| **faktura proforma** | Dokument pro forma. Typ: `Factura Proforma`. Nie jest dokumentem księgowym. | proforma (bez słowa "faktura"), oferta |
| **faktura storno** | Dokument korygujący fakturę. Typ: `Factura Storno`. | korekta faktury, storno (bez słowa "faktura" w kontekście typu dokumentu) |

---

## 2. Podmioty i strony dokumentu

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **klient** | Firma zarejestrowana w systemie jako odbiorca dokumentów. Odpowiada encji `Firm` z relacją w `UserFirm` gdzie `IsClient = true`. | kontrahent (w opisach UI), odbiorca (gdy nie chodzi o pole na dokumencie), nabywca |
| **firma użytkownika** | Firma zalogowanego użytkownika — wystawca dokumentów. | moja firma, firma własna |
| **użytkownik** | Zalogowana osoba korzystająca z systemu. Odpowiada encji `User`. | pracownik, operator |

---

## 3. Dane identyfikacyjne firm

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **CUI** | Numer identyfikacji podatkowej firmy w Rumunii (*Codul Unic de Identificare*). Odpowiada kolumnie `Firm.CUI`. | NIP (to jest polski odpowiednik — niedopuszczalny zamiennik), numer podatkowy |
| **RegCom** | Numer rejestracji firmy w rumuńskim rejestrze handlowym. Odpowiada kolumnie `Firm.RegCom`. | KRS (to jest polski odpowiednik — niedopuszczalny zamiennik), numer rejestrowy |
| **TVA** | Podatek od wartości dodanej stosowany w Rumunii. Wartość procentowa, np. 19%. | VAT (w kontekście tej aplikacji), podatek ogólnie |

---

## 4. Elementy dokumentu i ustawienia

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **seria dokumentów** | Ciąg numeracyjny przypisany do typu dokumentu, definiujący schemat numerowania, np. `2024/001`. Odpowiada encji `DocumentSeries`. | seria faktur, numeracja, schemat numerowania |
| **numer dokumentu** | Unikalny identyfikator dokumentu wygenerowany zgodnie z serią, np. `20240007`. Odpowiada kolumnie `Document.DocumentNumber`. | numer faktury (chyba że mowa o konkretnym typie), ID dokumentu |
| **konto bankowe** | Rachunek bankowy przypisany do firmy użytkownika, używany na dokumentach. Odpowiada encji `BankAccount`. | rachunek, konto |
| **waluta** | Oznaczenie waluty rachunku bankowego lub dokumentu. Wartości ze słownika `Currency`. | currency (w opisach biznesowych po polsku) |
| **status dokumentu** | Stan realizacji dokumentu. Wartości: `Unpaid`, `Paid`. Odpowiada encji `DocumentStatus`. | stan faktury, status płatności (gdy mowa o statusie dokumentu jako całości) |

---

## 5. Produkty i pozycje dokumentu

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **produkt** | Pozycja cennikowa zdefiniowana w systemie, dodawana do dokumentów. Odpowiada encji `Product`. | usługa (chyba że kontekst jednoznacznie wskazuje na usługę), towar, artykuł |
| **pozycja dokumentu** | Pojedynczy wiersz produktu na dokumencie z ilością, ceną jednostkową i wartością TVA. Odpowiada encji `DocumentProduct`. | linia dokumentu, pozycja faktury (chyba że mowa o fakturze), item |

---

## 6. Integracje zewnętrzne

| Termin obowiązujący | Definicja biznesowa | Nazwy zakazane |
|---|---|---|
| **ANAF** | Zewnętrzna usługa API rumuńskiej administracji podatkowej. Używana do pobierania danych firmy na podstawie CUI. | zewnętrzne API (gdy można użyć pełnej nazwy ANAF), serwis podatkowy, API podatkowe |

---

## 7. Operacje na danych (warstwa UI)

Poniższe terminy opisują operacje z perspektywy użytkownika — co widzi i co robi w interfejsie.

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **dodanie rekordu** | Operacja tworzenia nowego wpisu przez wypełnienie formularza i zapis (dialog Add lub formularz tworzenia). | dodanie wpisu, wstawienie, zapis nowego |
| **edycja rekordu** | Operacja modyfikacji istniejącego wpisu (dialog Edit lub formularz edycji). | zmiana, aktualizacja (gdy mowa o operacji UI), modyfikacja wpisu |
| **usunięcie rekordu** | Operacja trwałego usunięcia wpisu z bazy danych inicjowana z UI. | kasowanie, wymazanie, skasowanie |
| **zapis formularza** | Operacja walidacji formularza i wysłania danych do API (`POST` lub `PUT`). | submit, wysłanie, potwierdzenie |
| **anulowanie operacji** | Zamknięcie dialogu lub formularza bez wysyłania danych do API. | rezygnacja, cofnięcie, odrzucenie |
| **odświeżenie listy** | Ponowne pobranie danych z API i renderowanie gridu z aktualnymi danymi. | reload, przeładowanie, aktualizacja widoku |
| **zaznaczenie wiersza** | Aktywacja pola wyboru przy wierszu gridu w celu wskazania rekordów do operacji zbiorczej. | selekcja, wybór, oznaczenie |
| **komunikat sukcesu** | Powiadomienie `MatSnackBar` potwierdzające pomyślne wykonanie operacji. | alert sukcesu, notyfikacja, toast (ang.) |
| **komunikat błędu** | Powiadomienie `MatSnackBar` lub komunikat `mat-error` informujący o niepowodzeniu operacji lub błędzie walidacji. | alert błędu, error message (ang. w opisach biznesowych) |
