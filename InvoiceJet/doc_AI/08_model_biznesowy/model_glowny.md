# Model klas biznesowych InvoiceJet — diagram główny

| Pole | Wartość |
|---|---|
| ID dokumentu | MOD-GLOWNY |
| Typ dokumentu | diagram klas |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Diagram przedstawia główne klasy biznesowe systemu InvoiceJet oraz ich powiązania. Centralnym elementem jest `Dokument`, który łączy firmę wystawiającą (`Firma`), odbiorcę (`Klient`), konto bankowe (`KontoBankowe`) i pozycje (`PozycjaDokumentu`). Właścicielem wszystkich bytów jest `Uzytkownik`, który zarządza zasobami w kontekście swojej aktywnej firmy.

## Diagram klas

```mermaid
classDiagram
    class Uzytkownik {
        +GUID id
        +String imie
        +String nazwisko
        +String email
        +String haslo
        +String rola
        +referencja aktywnaFirma
    }

    class Firma {
        +int id
        +String nazwa
        +String cui
        +String numerRejestruHandlowego
        +String adres
        +String okrag
        +String miasto
    }

    class Klient {
        +int id
        +String nazwa
        +String cui
        +String numerRejestruHandlowego
        +String adres
        +String okrag
        +String miasto
    }

    class KontoBankowe {
        +int id
        +String nazwaBanku
        +String iban
        +String waluta
        +Boolean aktywne
    }

    class ProduktKatalogowy {
        +int id
        +String nazwa
        +Decimal cenaBazowa
        +Boolean zawieraVat
        +int stawkaVat
        +String jednostkaMiary
    }

    class SeriaDokumentow {
        +int id
        +String prefiks
        +int numerStartowy
        +int numerBiezacy
        +Boolean domyslna
        +String typDokumentu
    }

    class Dokument {
        +int id
        +String numerDokumentu
        +Date dataWystawienia
        +Date terminPlatnosci
        +Decimal wartoscNetto
        +Decimal wartoscBrutto
        +String typDokumentu
        +String status
    }

    class PozycjaDokumentu {
        +int id
        +Decimal ilosc
        +Decimal cenaJednostkowa
        +Decimal wartoscCalkowita
    }

    %% Relacje użytkownik - firma
    Uzytkownik "1" --> "0..*" Firma : posiada firmy
    Uzytkownik "1" --> "0..*" Klient : prowadzi bazę klientów

    %% Zasoby firmy
    Firma "1" --> "0..*" KontoBankowe : posiada konta
    Firma "1" --> "0..*" ProduktKatalogowy : ma katalog
    Firma "1" --> "0..*" SeriaDokumentow : konfiguruje numerację
    Firma "1" --> "0..*" Dokument : wystawia dokumenty

    %% Dokument i jego składniki
    Dokument "1" --> "1..*" PozycjaDokumentu : zawiera pozycje
    Dokument "0..*" --> "0..1" Klient : wystawiony dla
    Dokument "0..*" --> "1" KontoBankowe : wskazuje konto do zapłaty
    Dokument "0..*" --> "0..1" SeriaDokumentow : numerowany wg serii

    %% Pozycja i produkt
    PozycjaDokumentu "0..*" --> "0..1" ProduktKatalogowy : oparta na produkcie
```

## Legenda typów powiązań

| Notacja | Znaczenie |
|---|---|
| `1 --> 0..*` | Jeden do wielu (opcjonalne po stronie wielu) |
| `1 --> 1..*` | Jeden do wielu (co najmniej jedna po stronie wielu) |
| `0..*  --> 0..1` | Wiele do opcjonalnego jednego |
| `0..*  --> 1` | Wiele do wymaganego jednego |

## Uwagi do diagramu

- `Klient` i `Firma` to ta sama struktura danych w bazie (tabela `dbo.Firm`) — rozróżniane przez kontekst powiązania z użytkownikiem (`UserFirm.IsClient`).
- `Uzytkownik` posiada wskaźnik aktywnej firmy — w danej chwili pracuje w kontekście jednej firmy.
- `PozycjaDokumentu` przechowuje migawkę cenową niezależną od aktualnej ceny w `ProduktKatalogowy`.
- Powiązanie `Dokument → SeriaDokumentow` jest pośrednie — dokument przechowuje wygenerowany numer tekstowy, nie referencję do serii.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
