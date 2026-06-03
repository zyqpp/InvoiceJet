# PdfViewerComponent — Podgląd dokumentu PDF

| Pole | Wartość |
|---|---|
| ID dokumentu | MODAL-Wspolne-PdfViewer |
| Typ dokumentu | modal |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Komponent wyświetlania podglądu wygenerowanego pliku PDF dokumentu (faktury, proformy, storna). Wywoływany z formularzy dokumentów (EKRAN-10, EKRAN-12, EKRAN-14). Wywołuje endpoint API pobierający strumień PDF i renderuje go w przeglądarce — przez `<iframe>`, `<object>` lub otwarcie nowej karty (`window.open`).

## Charakterystyka modalu

| Atrybut | Wartość |
|---|---|
| ID modalu | MODAL-Wspolne-PdfViewer |
| Nazwa / tytuł w UI | Podgląd PDF |
| Wywołany przez operację | Klik „Podgląd PDF" / „Pobierz PDF" w formularzu dokumentu |
| Ekran nadrzędny | `../../../faktury/dodaj_edytuj_fakture/ekran.md`, `../../../faktury_proforma/dodaj_edytuj_fakture_proforma/ekran.md`, `../../../faktury_storno/dodaj_edytuj_fakture_storno/ekran.md` |
| Typ modalu | podgląd |
| Zamknięcie przez Escape | tak |
| Zamknięcie przez klik tła | tak |

## Wizualizacja układu

```
┌────────────────────────────────────────┐
│ Podgląd PDF                        [X] │
├────────────────────────────────────────┤
│                                        │
│   ┌──────────────────────────────┐     │
│   │                              │     │
│   │   [Renderowany dokument PDF] │     │
│   │   (<iframe> / <object>)      │     │
│   │                              │     │
│   └──────────────────────────────┘     │
│                                        │
└────────────────────────────────────────┘
```

## Pola modalu

Brak (modal podglądu, bez pól formularza).

## Operacje modalu

| Przycisk | Akcja | Wywołuje operację | Zamyka modal |
|---|---|---|---|
| [X] / Escape | Zamknięcie podglądu | Brak | tak |

## Przepływ wywołania

1. Użytkownik klika „Podgląd" / „Pobierz PDF" przy dokumencie
2. Wywołanie `POST /api/Document/GetPdfStream` z `{documentId}`
3. Odpowiedź to `application/pdf` (FileStreamResult)
4. Komponent renderuje PDF w `<iframe>` lub `<object>` albo otwiera nową kartę (`window.open`)

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Pobranie strumienia PDF | `POST /api/Document/GetPdfStream` |

## Możliwe wyniki

| Wynik | Warunki | Komunikat | Następna akcja |
|---|---|---|---|
| Sukces | PDF zwrócony przez API | Brak komunikatu — PDF renderowany | Podgląd widoczny |
| Anulowanie | Użytkownik klika [X] lub Escape | Brak | Modal zamknięty, brak zmian |
| Błąd API | Błąd generowania PDF | Brak komunikatu dla użytkownika (anomalia) | Brak reakcji w UI |

## Powiązania z kodem

- Komponent modalu: `src/app/components/pdf-viewer/pdf-viewer.component.ts`
- Szablon HTML: `src/app/components/pdf-viewer/pdf-viewer.component.html`

## Wątpliwości i braki

- PDF-01: `GenerateInvoicePdf` (endpoint osobny) hardkoduje `new InvoiceDocument()` — zawsze generuje fakturę zwykłą niezależnie od `DocumentTypeId`. `GetPdfStream` natomiast używa fabryki `InvoiceDocumentFactory` i generuje właściwy typ dokumentu.
- PDF-02: Brak walidacji po stronie frontendu czy dokument ma już wygenerowany PDF — zawsze wywołuje API niezależnie od stanu dokumentu.
- PDF-03: Niejasne czy komponent działa jako routing component czy MatDialog — kod wskazuje na oba tryby.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `_wspolne/pdf-viewer.md`. |
