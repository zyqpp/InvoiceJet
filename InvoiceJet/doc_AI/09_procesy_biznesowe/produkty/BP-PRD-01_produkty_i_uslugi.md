# BP-PRD-01 Zarządzanie katalogiem produktów i usług

| Pole | Wartość |
|---|---|
| ID dokumentu | BP-PRD-01 |
| Obszar | Produkty |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-06-01 |

## Cel biznesowy

Umożliwić użytkownikowi budowanie i utrzymywanie katalogu produktów i usług, które będą dostępne do szybkiego wyboru przy wystawianiu dokumentów handlowych.

## Kontekst

Użytkownik zarządza katalogiem produktów na ekranie „Produkty" (`/dashboard/products`). Każdy produkt w katalogu zawiera domyślne wartości (nazwa, cena, jednostka miary, stawka VAT), które mogą być przyspieszeniem przy wypełnianiu pozycji faktur — użytkownik wybiera produkt z listy zamiast wpisywać dane ręcznie. Pozycje na fakturze mogą być też wpisywane ręcznie bez korzystania z katalogu.

## Aktorzy

| Aktor | Rola |
|---|---|
| Użytkownik | Zarządza katalogiem produktów i usług firmy |
| Aplikacja (Frontend) | Wyświetla katalog, obsługuje dialogi dodawania i edycji |
| Serwer (API) | Zapisuje, aktualizuje lub usuwa pozycje katalogu |
| Baza danych | Trwale przechowuje dane produktów i usług |

## Warunki wejścia

- Użytkownik zalogowany
- Ekran produktów otwarty

## Przebieg główny — Dodanie produktu/usługi

1. **Użytkownik** otwiera ekran „Produkty"
2. **Aplikacja** pobiera i wyświetla listę produktów i usług firmy
3. **Użytkownik** klika „Dodaj produkt"
4. **Aplikacja** wyświetla dialog z formularzem: nazwa, jednostka miary, cena jednostkowa, stawka VAT
5. **Użytkownik** wypełnia formularz i klika „Zapisz"
6. **Serwer** zapisuje produkt w katalogu firmy użytkownika
7. **System** zamyka dialog; produkt widoczny na liście i dostępny w selektorach formularzy dokumentów

## Przebieg główny — Edycja produktu/usługi

1. **Użytkownik** klika przycisk edycji przy wybranym produkcie
2. **Aplikacja** wyświetla dialog z wypełnionym formularzem
3. **Użytkownik** modyfikuje dane i klika „Zapisz"
4. **Serwer** aktualizuje dane produktu
5. **System** zamyka dialog; zaktualizowane dane widoczne na liście

## Przebieg główny — Usunięcie produktu/usługi

1. **Użytkownik** klika ikonę usunięcia przy wybranym produkcie
2. **Aplikacja** wyświetla pytanie o potwierdzenie
3. **Użytkownik** potwierdza
4. **Serwer** usuwa produkt z katalogu
5. **System** odświeża listę produktów

## Reguły biznesowe

| ID | Reguła | Objaśnienie |
|---|---|---|
| RB-01 | Produkt powiązany jest z firmą użytkownika | Katalog produktów widoczny tylko dla właściciela firmy |
| RB-02 | Produkt dostępny jest w selektorach formularza faktury | Po dodaniu produkt pojawia się na liście wyboru pozycji dokumentu |
| RB-03 | Nazwa produktu musi być unikalna w systemie | Ograniczenie techniczne — unikalność sprawdzana globalnie (nie per firma) |
| RB-04 | Katalog produktów jest opcjonalny | Pozycje faktur można wpisywać ręcznie bez korzystania z katalogu |
| RB-05 | Cena i stawka VAT z katalogu to wartości domyślne | Przy wystawianiu faktury można zmienić cenę i stawkę VAT dla konkretnej pozycji |

## Wyjątki i scenariusze alternatywne

| ID | Scenariusz | Warunek | Reakcja systemu |
|---|---|---|---|
| WYJ-01 | Zduplikowana nazwa produktu | Użytkownik chce dodać produkt o nazwie już istniejącej w systemie | Błąd zapisu z niezrozumiałym komunikatem technicznym (znana anomalia — system zwraca błąd 500 zamiast czytelnego komunikatu) |
| WYJ-02 | Pusty katalog przy wystawianiu faktury | Użytkownik nie dodał żadnych produktów | Selektor produktów pusty; użytkownik musi wpisać pozycje ręcznie |
| WYJ-03 | Usunięcie produktu używanego w dokumentach | Produkt przypisany do pozycji w wystawionych fakturach | Zachowanie nieokreślone — możliwy błąd klucza obcego |

## Wynik procesu

Po dodaniu produktu:
- Produkt zapisany w katalogu firmy
- Produkt dostępny do wyboru w formularzu faktury / proformy / storno
- Przy wyborze produktu z listy pola ceny, jednostki i VAT wypełniają się automatycznie

Po usunięciu:
- Produkt niewidoczny na liście i niewidoczny w selektorach formularzy

## Diagram sekwencji

```mermaid
sequenceDiagram
    autonumber
    participant U as Użytkownik
    participant FE as Aplikacja (Frontend)
    participant API as Serwer (API)
    participant DB as Baza danych

    U->>FE: Otwiera ekran Produkty
    FE->>API: Pobierz katalog produktów firmy
    API->>DB: Zapytanie o produkty powiązane z firmą użytkownika
    DB-->>API: Lista produktów i usług
    API-->>FE: Lista produktów
    FE-->>U: Lista produktów z przyciskami Dodaj / Edytuj / Usuń

    U->>FE: Klik Dodaj produkt
    FE-->>U: Dialog z formularzem produktu
    U->>FE: Wypełnia: nazwa, jednostka miary, cena jednostkowa, stawka VAT
    U->>FE: Klik Zapisz

    FE->>API: Wyślij dane nowego produktu
    API->>DB: Pobierz identyfikator firmy użytkownika
    DB-->>API: Identyfikator firmy
    API->>DB: Zapisz produkt powiązany z firmą

    alt Nazwa produktu unikalna
        DB-->>API: Produkt zapisany
        API-->>FE: Produkt dodany
        FE-->>U: Dialog zamknięty; produkt na liście i w selektorach dokumentów
    else Nazwa produktu zajęta
        DB-->>API: Błąd unikalności
        API-->>FE: Błąd (komunikat techniczny)
        FE-->>U: Ogólny komunikat błędu
    end
```

## Powiązania analityczne

| Typ | Dokument |
|---|---|
| Use Case | [uc_produkty](../../07_use_case/produkty/uc_produkty.md) |
| Proces powiązany | [BP-CFG-01 Onboarding](../konfiguracja/BP-CFG-01_onboarding.md) |
| Proces powiązany | [BP-DOC-01 Wystawienie faktury](../dokumenty/BP-DOC-01_wystawienie_faktury.md) |

## Powiązania techniczne

| Typ | Dokument |
|---|---|
| Proces techniczny | [dodaj_produkt/proces.md](../../02_procesy/produkty/dodaj_produkt/proces.md) |
| API | [POST /api/Product/Add](../../04_api_i_integracje/01_api_frontend/product/POST_Product_Add.md) |
| Model DB | [dbo.Product](../../05_model_danych/01_db/dbo/dbo.Product.md) |

## Wątpliwości i braki

- Unikalność nazwy produktu egzekwowana **globalnie** (nie per firma) — dwie firmy nie mogą mieć produktu o tej samej nazwie; to błąd projektowy
- Naruszenie unikalności powoduje błąd 500 zamiast czytelnego komunikatu „Produkt o tej nazwie już istnieje"
- Brak importu produktów z pliku CSV — każdy produkt dodawany ręcznie
- Edycja produktu nie aktualizuje retroaktywnie cen na już wystawionych fakturach (pozycje faktur mają niezależnie zapisane wartości)

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-06-01 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja BP — na podstawie PROC-AddProduct i BPMN-KONF-01; format analityczny BP-NN |
