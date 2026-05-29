# Mapowanie UI, API i bazy danych

## 1. Regula mapowania pola

Kazde pole danych opisuje sie w jednym wierszu tabeli mapowania.

| Element | Wymagana informacja |
|---|---|
| Element makiety | Nazwa sekcji, etykieta pola albo kolumna gridu. |
| Frontend | `formControlName`, model TS, komponent i handler. |
| HTTP | Metoda serwisu Angular i endpoint. |
| Backend | DTO, kontroler i metoda serwisu aplikacyjnego. |
| Baza | Encja oraz `Tabela.Kolumna`. |
| Uwagi | Marker, jezeli pelny slad nie istnieje. |

## 2. Regula mapowania operacji

Operacja UI musi pokazac pelny skutek. Opis zawiera:

- element wyzwalajacy,
- handler w komponencie,
- walidacje frontendu,
- metode serwisu Angular,
- endpoint,
- metode kontrolera,
- metode serwisu backendowego,
- odczyty i zapisy w bazie,
- reakcje UI po sukcesie i bledzie.

## 3. Regula mapowania gridu

Grid opisuje sie przez zrodlo kolekcji i przeksztalcenia:

| Obszar | Opis |
|---|---|
| Zrodlo UI | `MatTableDataSource`, kolekcja modelu TS, filtr, sortowanie, paginacja. |
| Wywolanie HTTP | Metoda serwisu Angular oraz endpoint. |
| Odpowiedz API | DTO listy albo rekord tabeli. |
| Backend | Repozytorium, `Query()`, `Include()` albo metoda dedykowana. |
| Baza | Tabele i kolumny uzyte do zasilenia kolumn gridu. |

## 4. Regula walidacji

Walidacje opisywac warstwowo:

| Warstwa | Co dokumentowac |
|---|---|
| Frontend | `Validators`, walidatory niestandardowe, stan `invalid`, komunikaty `mat-error`. |
| API | Atrybuty walidacyjne DTO, wymagalnosc parametrow trasy i body. |
| Backend | Warunki w serwisach, wyjatki domenowe, skutki braku danych. |
| Baza | Wymagalnosc kolumn, typy danych, relacje, indeksy. |

## 5. Regula braku pelnego sladu

Jezeli dana informacja konczy sie na jednej warstwie, dokument wskazuje ostatni potwierdzony punkt. Brak dalszego sladu oznacza sie markerem z `05_MARKERY_I_JAKOSC.md`.
