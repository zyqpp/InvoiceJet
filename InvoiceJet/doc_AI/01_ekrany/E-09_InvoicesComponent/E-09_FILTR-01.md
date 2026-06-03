# FILTR-E09-01 — Wyszukiwanie (Search)

| Pole | Wartość |
|---|---|
| ID dokumentu | FILTR-E09-01 |
| Typ dokumentu | filtr |
| Ekran nadrzędny | [E-09 InvoicesComponent](E-09_ekran.md) |
| Wersja | 1.0 |
| Status | zweryfikowany |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Search" |
| Nazwa w kodzie | `dataSource.filter` (`MatTableDataSource`) |
| Typ kontrolki | `input[matInput]` z przyciskiem Clear (×) |
| Zawęża | [TAB-E09-01 Lista faktur](E-09_TAB-01.md) |
| Parametr API | **brak** — filtrowanie klienckie (MatTableDataSource) |
| Pole DTO | nie dotyczy — filtr działa na załadowanej kolekcji |
| Pola filtrowane | wszystkie kolumny tekstowe: `documentNumber`, `clientName`, `documentStatus` |
| Wartości dopuszczalne | dowolny string; `toLowerCase()` przed porównaniem |
| Domyślna wartość | puste (brak filtru) |
| Wymagany | nie |

## Zachowanie

| Aspekt | Opis |
|---|---|
| Moment zastosowania | na bieżąco przy każdym `(keyup)` — metoda `applyFilter($event)` |
| Efekt na paginację | reset do strony 1 (`paginator.firstPage()`) |
| Przycisk Clear (×) | widoczny gdy `searchInput.value != ""`; czyści filtr i resetuje paginację |
| Łączenie z innymi filtrami | jedyny filtr na ekranie |

## Dane testowe

| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| Filtr po numerze | `"FV0001"` | tylko faktury zawierające „FV0001" |
| Filtr po kliencie | `"ABC SRL"` | faktury klienta ABC SRL |
| Filtr brak wyników | `"NIEISTNIEJACY_XYZ"` | tabela pusta |
| Clear filtra | klik × po wpisaniu tekstu | pełna lista |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Handler | `applyFilter()` w [`invoices.component.ts`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.ts) |
| Binding HTML | `(keyup)="applyFilter($event)"` w [`invoices.component.html`](../../../../InvoiceJetUI/src/app/components/invoices/invoices.component.html) |

## Wątpliwości i braki

Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-09_ekran.md. |
