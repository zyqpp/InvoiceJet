# Slownik AOS aplikacyjnego

## 1. Pojecia główne

| Pojecie | Definicja |
|---|---|
| AOS aplikacyjny | Dokumentacja łącząca makietę, frontend, API, backend i bazę danych. |
| Mapa Nawigacji i Makiet | Dokument pokazujacy sekcję menu, pozycje menu, trasy, dialogi i makiety elementarne. |
| Przepływ aplikacyjny | Pełny ciąg operacji od elementu UI do skutku w API, backendzie i bazie. |
| Makieta elementarna | Najmniejszy widok wymagający osobnego opisu: ekran, formularz, dialog, podgląd PDF albo trasa edycji. |
| Pole UI | Pole formularza albo komorka gridu widoczna w makiecie. |
| Operacja UI | Przycisk, link, wybor z menu, zmiana filtra albo wysłanie formularza. |
| Ślad danych | Powiązanie pola UI z modelem TS, endpointem, DTO, encja i `Tabela.Kolumna`. |

## 2. Warstwy techniczne

| Warstwa | Przyklad | Opis w AOS aplikacyjnym |
|---|---|---|
| Makieta | `Invoice Details` | Widok, formularz, grid, dialog albo pasek nawigacji. |
| Komponent Angular | `AddOrEditInvoiceComponent` | Źródło pól, walidacji i handlerow UI. |
| Model TS | `IDocumentRequest` | Ksztalt danych wysyłanych z frontendu. |
| Serwis Angular | `DocumentService.addDocument()` | Miejsce wywołania HTTP. |
| Endpoint API | `POST /api/Document/AddDocument` | Kontrakt miedzy frontendem i backendem. |
| DTO backendu | `DocumentRequestDto` | Ksztalt danych po stronie API. |
| Serwis backendowy | `DocumentService.AddDocument()` | Logika aplikacyjna backendu. |
| Encja | `Document` | Model domenowy zapisywany przez EF Core. |
| Baza danych | `Document.DocumentNumber` | Tabela i kolumna wynikająca z migracji. |

## 3. Statusy dokumentacji

| Status | Znaczenie |
|---|---|
| Roboczy | Dokument wygenerowany i wymaga przegladu czlowieka. |
| Do weryfikacji | Dokument zawiera markery albo miejsca do potwierdzenia. |
| Zatwierdzony | Dokument zostal sprawdzony przez czlowieka. |
