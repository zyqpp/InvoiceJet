# Proces biznesowy: Wystawienie proformy

| Pole | Wartość |
|---|---|
| ID dokumentu | BPMN-DOC-02 |
| Typ dokumentu | proces biznesowy |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Proces wystawienia proformy (DocumentTypeId = 2) jest identyczny jak wystawienie faktury — różnica polega wyłącznie na przekazaniu `TypeId=2` w żądaniu autouzupełnienia i zapisie dokumentu. Backend dobiera inną serię numeracji (DocumentSeries powiązaną z typem 2) oraz QuestPDF używa szablonu `ProformaDocument` zamiast `InvoiceDocument`. Frontend wyświetla ten sam formularz z etykietą "Proforma".

## Uczestnicy

| Uczestnik | Rola |
|---|---|
| Użytkownik | Inicjator akcji (wystawia proformę) |
| Frontend (Angular) | Warstwa prezentacji — formularz proformy, obliczenia na żywo |
| Backend (API) | Logika biznesowa — zapis dokumentu z TypeId=2, aktualizacja serii |
| SQL Server | Trwałe przechowywanie danych dokumentów |
| ANAF API | Autouzupełnienie danych klienta po CUI (opcjonalne) |

## Diagram procesu (Mermaid sequenceDiagram)

```mermaid
sequenceDiagram
    participant U as Użytkownik
    participant FE as Frontend (Angular)
    participant BE as Backend (API)
    participant DB as SQL Server
    participant ANAF as ANAF API

    U->>FE: Klik "Nowa proforma"
    FE->>BE: GET /api/Document/GetDocumentAutofillInfo/2
    BE->>DB: SELECT DocumentSeries (TypeId=2), Clients, BankAccounts, Products, Statuses
    DB-->>BE: Dane autouzupełnienia (serie proform)
    BE-->>FE: DocumentAutofillInfoDto
    FE-->>U: Formularz z selektorami proformy

    opt Autouzupełnienie klienta z ANAF
        U->>FE: Wpisuje CUI + klik ikony chmury
        FE->>BE: GET /api/Firm/fromAnaf/{cui}
        BE->>ANAF: POST [{ cui, data }]
        ANAF-->>BE: Dane firmy klienta
        BE-->>FE: FirmRequestDto
        FE-->>U: Autouzupełnione pola klienta
    end

    U->>FE: Wypełnia formularz: seria, klient, konto bankowe, data, termin płatności
    U->>FE: Dodaje pozycje dokumentu (produkt, ilość, cena, VAT)
    FE-->>U: Sumy obliczane na żywo (netto / VAT / brutto)
    U->>FE: Klik "Zapisz"

    FE->>BE: POST /api/Document/Add (DocumentRequestDto, TypeId=2)
    BE->>DB: INSERT Document (DocumentTypeId=2)
    BE->>DB: INSERT DocumentProducts[]
    BE->>DB: UPDATE DocumentSeries SET CurrentNumber = CurrentNumber + 1
    DB-->>BE: OK
    BE-->>FE: 201 Created + { documentId }

    FE->>FE: router.navigate("/dashboard/proforma-invoices")
    FE-->>U: Lista proform z nową proformą

    opt Generowanie PDF
        U->>FE: Klik "PDF" przy proformie
        FE->>BE: POST /api/Document/GetPdfStream (DocumentRequestDto)
        BE->>DB: SELECT Document z pełnymi JOINami
        DB-->>BE: Document data (TypeId=2)
        BE->>BE: InvoiceDocumentFactory.Create(2) → ProformaDocument
        BE->>BE: QuestPDF GeneratePdf() → MemoryStream
        BE-->>FE: FileStreamResult (application/pdf)
        FE-->>U: PDF proformy otwarty w przeglądarce
    end
```

## Kroki procesu

| # | Krok | Uczestnik | Opis |
|---|---|---|---|
| 1 | Inicjacja | Użytkownik | Klik "Nowa proforma" na liście proform. |
| 2 | Pobranie danych autouzupełnienia | Frontend / Backend | GET `/api/Document/GetDocumentAutofillInfo/2` — serie proform, klienci, konta, produkty. |
| 3 | Wyświetlenie formularza | Frontend | Formularz identyczny z fakturą — etykieta "Proforma". |
| 4 | Autouzupełnienie klienta (opcja) | Użytkownik / Frontend / Backend / ANAF | Wpisanie CUI → GET fromAnaf → autouzupełnienie pól klienta. |
| 5 | Wypełnienie nagłówka | Użytkownik | Seria numeracji proform, klient, konto bankowe, daty. |
| 6 | Dodanie pozycji | Użytkownik | Produkty z katalogu lub ręcznie — ilość, cena, VAT. |
| 7 | Obliczenia na żywo | Frontend | Sumy netto / VAT / brutto aktualizowane w czasie rzeczywistym. |
| 8 | Zapis dokumentu | Frontend / Backend / DB | POST `/api/Document/Add` z TypeId=2 → INSERT Document + Products + UPDATE Series. |
| 9 | Przekierowanie | Frontend | router.navigate na listę proform; nowa proforma widoczna. |
| 10 | Generowanie PDF (opcja) | Użytkownik / Frontend / Backend | POST GetPdfStream → Factory.Create(2) → ProformaDocument → QuestPDF. |

## Obsługa wyjątków

| Sytuacja | Reakcja systemu |
|---|---|
| Brak wymaganego pola (walidacja frontend) | Blokada wysłania; komunikat inline w formularzu. |
| Brak serii numeracji dla proform | Backend 404; frontend toastr error; użytkownik musi skonfigurować serię. |
| ANAF niedostępny | Backend zwraca błąd; frontend toastr; użytkownik wpisuje dane ręcznie. |
| JWT wygasa w trakcie edycji | JwtInterceptor 401 → TokenExpiredDialog → /login; dane przepadają. |
| Błąd QuestPDF przy GetPdfStream | Backend 500; ExceptionMiddleware zwraca ogólny komunikat. |

## Powiązane procesy techniczne

| Proces | Link |
|---|---|
| Wystawienie faktury (BPMN) | `wystawienie_faktury.md` |
| Eksport PDF (BPMN) | `eksport_pdf.md` |
| Generuj PDF (techniczny) | `../../02_procesy/dokumenty/generuj_pdf/proces.md` |

## Wątpliwości i braki

- `GenerateInvoicePdf` (drugi endpoint PDF) ignoruje TypeId i zawsze generuje szablon faktury zwykłej — proforma generuje się z błędnym szablonem jeśli wywołany przez ten endpoint (anomalia PDF-01).
- Brak konwersji proformy na fakturę (odwrotny kierunek do storno) — nie ma dedykowanego endpointu.
- Identyczny formularz jak faktura może mylić użytkownika — brak wyraźnego oznaczenia "Proforma" w nagłówku formularza.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — wzorowana na BPMN-DOC-01, dostosowana do TypeId=2. |
