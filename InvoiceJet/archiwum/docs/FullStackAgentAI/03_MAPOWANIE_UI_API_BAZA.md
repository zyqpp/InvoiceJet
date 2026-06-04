# Mapowańie UI, API i bazy danych

## 1. Reguła mapowańia pola

Każde pole danych opisuje się w jednym wierszu tabeli mapowańia.

| Element | Wymagana informacja |
|---|---|
| Element makiety | Nazwa sekcji, etykieta pola albo kolumna gridu. |
| Frontend | `formControlName`, model TS, komponent i handler. |
| HTTP | Metoda serwisu Angular i endpoint. |
| Backend | DTO, kontroler i metoda serwisu aplikacyjnego. |
| Baza | Encja oraz `Tabela.Kolumna`. |
| Uwagi | Marker, jeżeli pełny ślad nie istnieje. |

## 2. Reguła mapowańia operacji

Operacja UI musi pokazac pełny skutek. Opis zawiera:

- element wyzwalajacy,
- handler w komponencie,
- walidacje frontendu,
- metodę serwisu Angular,
- endpoint,
- metodę kontrolera,
- metodę serwisu backendowego,
- odczyty i zapisy w bazie,
- reakcje UI po sukcesie i błędzie.

## 3. Reguła mapowańia gridu

Grid opisuje się przez źródło kolekcji i przeksztalcenia:

| Obszar | Opis |
|---|---|
| Źródło UI | `MatTableDataSource`, kolekcja modelu TS, filtr, sortowanie, paginacja. |
| Wywołanie HTTP | Metoda serwisu Angular oraz endpoint. |
| Odpowiedź API | DTO listy albo rekord tabeli. |
| Backend | Repozytorium, `Query()`, `Include()` albo metoda dedykowana. |
| Baza | Tabele i kolumny użyte do zasilenia kolumn gridu. |

## 4. Reguła walidacji

Walidacje opisywac warstwowo:

| Warstwa | Co dokumentówac |
|---|---|
| Frontend | `Validators`, walidatory niestandardowe, stan `invalid`, komunikaty `mat-error`. |
| API | Atrybuty walidacyjne DTO, wymagalność parametrow trasy i body. |
| Backend | Warunki w serwisach, wyjatki domenowe, skutki braku danych. |
| Baza | Wymagalność kolumn, typy danych, relacje, indeksy. |

## 5. Reguła braku pełnego śladu

Jeżeli dana informacja kończy sie na jednej warstwie, dokument wskazuje ostatni potwierdzony punkt. Brak dalszego śladu oznacza sie markerem z `05_MARKERY_I_JAKOSC.md`.
