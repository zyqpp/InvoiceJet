# Slownik AOS aplikacyjnego

## 1. Pojecia glowne

| Pojecie | Definicja |
|---|---|
| AOS aplikacyjny | Dokumentacja laczaca makiete, frontend, API, backend i baze danych. |
| Mapa Nawigacji i Makiet | Dokument pokazujacy sekcje menu, pozycje menu, trasy, dialogi i makiety elementarne. |
| Przeplyw aplikacyjny | Pelny ciag operacji od elementu UI do skutku w API, backendzie i bazie. |
| Makieta elementarna | Najmniejszy widok wymagajacy osobnego opisu: ekran, formularz, dialog, podglad PDF albo trasa edycji. |
| Pole UI | Pole formularza albo komorka gridu widoczna w makiecie. |
| Operacja UI | Przycisk, link, wybor z menu, zmiana filtra albo wyslanie formularza. |
| Slad danych | Powiazanie pola UI z modelem TS, endpointem, DTO, encja i `Tabela.Kolumna`. |

## 2. Warstwy techniczne

| Warstwa | Przyklad | Opis w AOS aplikacyjnym |
|---|---|---|
| Makieta | `Invoice Details` | Widok, formularz, grid, dialog albo pasek nawigacji. |
| Komponent Angular | `AddOrEditInvoiceComponent` | Zrodlo pol, walidacji i handlerow UI. |
| Model TS | `IDocumentRequest` | Ksztalt danych wysylanych z frontendu. |
| Serwis Angular | `DocumentService.addDocument()` | Miejsce wywolania HTTP. |
| Endpoint API | `POST /api/Document/AddDocument` | Kontrakt miedzy frontendem i backendem. |
| DTO backendu | `DocumentRequestDto` | Ksztalt danych po stronie API. |
| Serwis backendowy | `DocumentService.AddDocument()` | Logika aplikacyjna backendu. |
| Encja | `Document` | Model domenowy zapisywany przez EF Core. |
| Baza danych | `Document.DocumentNumber` | Tabela i kolumna wynikajaca z migracji. |

## 3. Statusy dokumentacji

| Status | Znaczenie |
|---|---|
| Roboczy | Dokument wygenerowany i wymaga przegladu czlowieka. |
| Do weryfikacji | Dokument zawiera markery albo miejsca do potwierdzenia. |
| Zatwierdzony | Dokument zostal sprawdzony przez czlowieka. |
