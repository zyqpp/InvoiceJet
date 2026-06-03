# S-01. Słownik pojęć biznesowych — InvoiceJet

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| ID | S-01 |
| Nazwa | Słownik pojęć biznesowych |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Data | 2026-05-31 |
| Status | Szkic |
| Plik | `doc_AI/_slowniki/slownik_biznesowy.md` |

## Streszczenie

Słownik definiuje pojęcia domenowe używane w projekcie InvoiceJet (wewnętrzna nazwa: Facturila) — aplikacji do wystawiania faktur na rynek rumuński. Każde pojęcie odnosi się do realiów rumuńskich przepisów podatkowych lub do modelu danych systemu. Definicje są spójne z encjami bazy danych i terminologią użytą w kodzie źródłowym.

---

## Pojęcia biznesowe

### firma — własna firma użytkownika {#firma-wlasna}

Firma zarejestrowana przez użytkownika w systemie jako jego firma wystawiająca dokumenty. Przechowywana w encji `Firm`. Powiązana z użytkownikiem przez encję `UserFirm`. W kontekście dokumentu pełni rolę **sprzedawcy** (Seller). Jeden użytkownik może mieć wiele firm.

### firma — firma-klient {#firma-klient}

Firma będąca odbiorcą dokumentu (kontrahentem). Przechowywana również w encji `Firm`, lecz powiązana z dokumentem jako pole `ClientId` w encji `Document`. W kodzie i dokumentacji nazywana **Client**. Nie wymaga konta w systemie.

### klient {#klient}

Synonim pojęcia **firma-klient**. Kontrahent — odbiorca faktury lub innego dokumentu. Identyfikowany przez `Firm.Id` po stronie klienta. W UI widoczny jako lista na ekranie zarządzania firmami (EKRAN-04).

### dokument {#dokument}

Nadrzędne pojęcie dla wszystkich typów dokumentów wystawianych w systemie: faktury, proformy i storna. Przechowywany w encji `Document`. Każdy dokument ma przypisany `DocumentTypeId` (1, 2 lub 3), `DocumentSeriesId`, datę wystawienia, sprzedawcę i klienta.

### faktura (faktura VAT) {#faktura}

Dokument handlowy z `DocumentTypeId = 1`. Rumuska nazwa: *Factură*. Potwierdza sprzedaż towaru lub usługi. Zawiera stawkę TVA, dane sprzedawcy i klienta, pozycje produktów oraz łączne kwoty. Generowany PDF korzysta z szablonu `InvoiceDocument`.

### faktura proforma {#faktura-proforma}

Dokument z `DocumentTypeId = 2`. Rumuska nazwa: *Factură Proformă*. Oferta cenowa poprzedzająca wystawienie faktury właściwej — nie jest dokumentem księgowym. W systemie traktowana jak faktura, lecz z odrębną serią numeracji.

### faktura storno (korekta) {#faktura-storno}

Dokument z `DocumentTypeId = 3`. Rumuska nazwa: *Storno*. Koryguje lub anuluje wcześniej wystawioną fakturę. Tworzona przez operację `TransformToStorno` w `DocumentService`. Kwoty pozycji są negowane (mnożone przez -1).

### seria dokumentów {#seria-dokumentow}

Szablon numeracji dokumentów przechowywany w encji `DocumentSeries`. Składa się z pola `SeriesName` (prefiks, np. `"FV"`) i `CurrentNumber` (bieżący licznik). Numer dokumentu generowany jest jako `SeriesName + CurrentNumber.ToString("D4")`, np. `FV0015`. Każda seria należy do konkretnej firmy użytkownika (`UserFirmId`).

### konto bankowe {#konto-bankowe}

Konto bankowe przypisane do firmy użytkownika, przechowywane w encji `BankAccount`. Drukowane na fakturze jako dane do przelewu. Usunięcie konta bankowego powoduje kaskadowe usunięcie powiązanych dokumentów (CASCADE DELETE — anomalia A-KRIT-01).

### produkt {#produkt}

Pozycja katalogowa przechowywana w encji `Product`. Zawiera nazwę, jednostkę miary, cenę jednostkową i stawkę TVA. Produkt jest dołączany do dokumentu przez encję `DocumentProduct`. Nazwa produktu objęta unikalnym indeksem globalnym (anomalia A-WYS-05).

### CUI {#cui}

**Cod Unic de Identificare** — rumuński odpowiednik polskiego NIP. Unikalny numer identyfikacyjny firmy w rejestrze rumuńskim. Przechowywany w polu `Firm.CUI`. Używany do weryfikacji firmy przez API ANAF. Alternatywna rozwinięta forma: *Cod Unic de Înregistrare*.

### TVA {#tva}

**Taxa pe Valoarea Adăugată** — rumuński podatek od wartości dodanej (odpowiednik polskiego VAT). Stawka TVA przechowywana jest przy produkcie (`Product.TVA`) i przenoszona na pozycje dokumentu (`DocumentProduct`). Standardowa stawka w Rumunii: 19%.

### ANAF {#anaf}

**Agenția Națională de Administrare Fiscală** — rumuński urząd skarbowy i rejestr firm. System InvoiceJet integruje się z publicznym API ANAF (`INT-ANAF`) w celu automatycznego pobierania danych firmy na podstawie CUI. Wywołanie realizowane przez `FirmService.GetFirmDataFromAnaf()`.

### RON {#ron}

**Leu rumuński** — podstawowa waluta dokumentów wystawianych w systemie InvoiceJet. Skrót ISO 4217: RON. Wszystkie kwoty na fakturach wyrażone są w RON. System nie obsługuje wielu walut.

### onboarding {#onboarding}

Sekwencja pierwszych kroków wykonywanych przez użytkownika po rejestracji w systemie: (1) rejestracja konta, (2) dodanie własnej firmy, (3) dodanie konta bankowego, (4) dodanie produktów do katalogu, (5) wystawienie pierwszego dokumentu. Brak dedykowanego ekranu onboardingowego — użytkownik przechodzi przez kolejne sekcje aplikacji.

### UserFirm {#userfirm}

Encja pośrednicząca łącząca użytkownika (`User`) z jego firmą (`Firm`). Przechowuje pole `UserFirmId`, które jest kluczowym identyfikatorem izolacji danych w systemie. Każde zapytanie do bazy filtruje dane przez `UserFirmId` pobierany z claimu JWT (`userId`). Gwarantuje, że użytkownik widzi tylko zasoby swojej firmy.

---

## Wątpliwości i braki

| ID | Wątpliwość | Status |
|---|---|---|
| W-01 | Czy jeden użytkownik może mieć wiele firm (wiele rekordów `UserFirm`)? Kod sugeruje tak, ale UI nie oferuje przełączania firm. | Do_zdefiniowania |
| W-02 | Czy `Firm` dla klienta i `Firm` dla sprzedawcy to ten sam rekord w tabeli? Rozróżnienie wyłącznie przez kontekst powiązania. | Do_zdefiniowania |
| W-03 | Standardowa stawka TVA 19% — czy system obsługuje inne stawki (0%, 5%, 9%)? | Do_zdefiniowania |

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — 15 pojęć biznesowych. |
