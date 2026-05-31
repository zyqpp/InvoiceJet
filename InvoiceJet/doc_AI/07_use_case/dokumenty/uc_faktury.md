# Use Case: Wystawianie i zarządzanie fakturami

| Pole | Wartość |
|---|---|
| ID dokumentu | UC-Dokumenty-Faktury |
| Typ dokumentu | use case |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Przypadek użycia opisuje pełny cykl życia faktury (Factura, `documentTypeId=1`): wystawienie nowej faktury przez formularz, edycję istniejącej oraz opcjonalne wygenerowanie i pobranie pliku PDF. System automatycznie generuje numer dokumentu na podstawie wybranej serii numeracji i inkrementuje licznik. Faktury wymagają uprzedniego skonfigurowania firmy, serii numeracji i konta bankowego.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Zalogowany właściciel konta; wystawia i zarządza fakturami swojej firmy |

## Warunki wstępne

- Użytkownik zalogowany (ważny token JWT)
- Firma zdefiniowana w systemie (dane rejestrowe uzupełnione)
- Co najmniej jedna seria numeracji dla faktury (`documentTypeId=1`) zdefiniowana
- Co najmniej jedno konto bankowe zdefiniowane

## Scenariusz główny — Wystawienie faktury

1. Użytkownik przechodzi do `/dashboard/invoices` (lista faktur)
2. Klika „Nowa faktura" → przekierowanie na `/dashboard/add-invoice`
3. System wywołuje `GET /api/Document/GetDocumentAutofillInfo/1` i wypełnia selektory (seria, klienci, konta bankowe)
4. Użytkownik wybiera serię numeracji, klienta, konto bankowe, datę wystawienia i termin płatności
5. Użytkownik dodaje pozycje faktury: wybiera produkt z katalogu lub wpisuje dane ręcznie (nazwa, cena, ilość, VAT)
6. Frontend oblicza wartości netto, VAT i brutto w czasie rzeczywistym
7. Użytkownik klika „Zapisz" → system wywołuje `POST /api/Document/Add` z `documentTypeId=1`
8. Backend generuje numer dokumentu (np. `FV0015`) i inkrementuje licznik serii
9. Użytkownik zostaje przekierowany na listę faktur `/dashboard/invoices`

## Scenariusz główny — Edycja faktury

1. Użytkownik klika „Edytuj" przy wybranej fakturze na liście
2. Przekierowanie na `/dashboard/edit-invoice/:id`
3. System ładuje dane faktury: `GET /api/Document/GetDocumentById/{id}`
4. Formularz wypełniany istniejącymi danymi dokumentu
5. Użytkownik modyfikuje wymagane pola (np. pozycje, daty, konto bankowe)
6. Klika „Zapisz" → system wywołuje `PUT /api/Document/Edit`
7. Użytkownik zostaje przekierowany na listę faktur

## Scenariusz główny — Generowanie PDF

1. Użytkownik klika „PDF" przy wybranej fakturze na liście
2. System wywołuje `POST /api/Document/GetPdfStream` z ID dokumentu
3. Backend generuje plik PDF przy użyciu biblioteki QuestPDF
4. Plik PDF jest przesyłany strumieniowo do przeglądarki
5. Przeglądarka pobiera lub wyświetla plik PDF

## Scenariusze alternatywne

### A1: Brak wymaganych danych konfiguracyjnych

1. Użytkownik próbuje otworzyć formularz nowej faktury
2. `GET /api/Document/GetDocumentAutofillInfo/1` zwraca pustą listę serii lub kont bankowych
3. Formularz wyświetla ostrzeżenie o brakującej konfiguracji
4. Użytkownik musi najpierw skonfigurować serię lub konto bankowe

### A2: Błąd zapisu faktury

1. Użytkownik klika „Zapisz"
2. Backend zwraca błąd walidacji lub serwera
3. System wyświetla komunikat o błędzie
4. Formularz pozostaje otwarty z danymi użytkownika

### A3: Błąd generowania PDF

1. Użytkownik klika „PDF"
2. Backend zwraca błąd generowania (np. brak danych firmy)
3. System wyświetla komunikat o błędzie
4. Faktura pozostaje na liście — użytkownik może ponowić próbę

## Diagram (Mermaid flowchart)

```mermaid
flowchart TD
    Start([Start]) --> InvList[Lista faktur\n/dashboard/invoices]
    InvList --> Action{Akcja}

    Action -->|Nowa faktura| AddForm[/dashboard/add-invoice]
    AddForm --> Autofill[GET /api/Document/GetDocumentAutofillInfo/1\nSelektory: seria, klient, konto]
    Autofill --> AutoOK{Dane\ndostępne?}
    AutoOK -->|Brak serii lub konta| CfgWarn[Ostrzeżenie: brak konfiguracji\nPrzejdź do serii / kont]
    AutoOK -->|OK| FormFill[Uzupełnij formularz\nklient, daty, pozycje]
    FormFill --> Calc[Oblicz netto/VAT/brutto\nw czasie rzeczywistym]
    Calc --> Save[POST /api/Document/Add\ndocumentTypeId=1]
    Save --> SaveOK{Sukces?}
    SaveOK -->|Tak| NumGen[Backend generuje numer FVxxxx\nInkrementuje licznik serii]
    NumGen --> InvList
    SaveOK -->|Nie| SaveErr[Komunikat błędu]
    SaveErr --> FormFill

    Action -->|Edytuj| EditLoad[GET /api/Document/GetDocumentById\n/dashboard/edit-invoice/:id]
    EditLoad --> EditForm[Formularz z danymi]
    EditForm --> EditSave[PUT /api/Document/Edit]
    EditSave --> InvList

    Action -->|PDF| PdfReq[POST /api/Document/GetPdfStream]
    PdfReq --> PdfOK{Sukces?}
    PdfOK -->|Tak| PdfDl[Pobierz PDF\nQuestPDF stream]
    PdfOK -->|Nie| PdfErr[Komunikat błędu]
    PdfErr --> InvList
```

## Powiązane ekrany

| Ekran | Link |
|---|---|
| Lista faktur | `../../01_ekrany/faktury/lista_faktur/ekran.md` |
| Formularz dodaj/edytuj fakturę | `../../01_ekrany/faktury/dodaj_edytuj_fakture/ekran.md` |

## Powiązane procesy

| Proces | Link |
|---|---|
| Dodaj dokument | `../../02_procesy/dokumenty/dodaj_dokument/proces.md` |
| Generuj PDF | `../../02_procesy/dokumenty/generuj_pdf/proces.md` |

## Wątpliwości i braki

- Brak blokady edycji faktury po upływie okresu rozliczeniowego — użytkownik może edytować faktury z dowolnej daty.
- Zmiana `documentTypeId` przez API (PUT) nie jest zablokowana — możliwa ręczna zmiana typu faktury.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — rozszerzona na podstawie UC-02 z diagramem Mermaid. |
