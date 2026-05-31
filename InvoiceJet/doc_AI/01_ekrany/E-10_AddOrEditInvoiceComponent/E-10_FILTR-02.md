# FILTR-E10-02 — Autocomplete produktu (Name per wiersz)

| Pole | Wartość |
|---|---|
| ID | FILTR-E10-02 |
| Ekran nadrzędny | [E-10 Formularz faktury](E-10_ekran.md) |
| Wersja | 1.0 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Charakterystyka

| Atrybut | Wartość |
|---|---|
| Etykieta UI | „Name" (kolumna w [TAB-E10-01](E-10_TAB-01.md), per wiersz) |
| Nazwa w kodzie | `productsFormArray.at(i).get('name')` |
| Typ kontrolki | `mat-autocomplete` per wiersz pozycji |
| Parametr API | brak — filtrowanie klienckie na `invoiceAutofillData.products` |
| Źródło danych autofill | [DTO-10](../../../05_model_danych/02_dto/DTO-10_DocumentAutofillInfoDto.md) → `Products[]` |
| Pole filtrowane | `Product.Name` (contains, case-insensitive) |
| Domyślna wartość | `null` (wymagane) |

## Zachowanie po wyborze produktu (onProductSelected)

Autouzupełnia pozostałe pola wiersza:
- `unitPrice` ← `product.price`
- `unitOfMeasurement` ← `product.unitOfMeasurement`
- `tvaValue` ← `product.tvaValue`
- `containsTva` ← `product.containsTva`
- Wywołuje `calculateTotalPrice(index)` → [ALG-Wyliczeniowe-ObliczanieCenyPozycji](../../../03_algorytmy/wyliczeniowe/obliczanie_ceny_pozycji.md)

## Dane testowe

| Scenariusz | Dane wejściowe | Oczekiwany efekt |
|---|---|---|
| Filtr po nazwie | `"Con"` | lista produktów zawierających „Con" |
| Wybór produktu | klik podpowiedź „Consulting" | autouzupełnianie pól wiersza |
| Wpisanie ręczne | dowolna nazwa bez wyboru z listy | produkt zapisywany jako nowy rekord `Product` (anomalia UPD-02) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wydzielony z E-10_ekran.md. |
