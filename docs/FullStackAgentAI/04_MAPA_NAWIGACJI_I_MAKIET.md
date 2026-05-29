# Mapa Nawigacji i Makiet

## 1. Cel mapy

Mapa Nawigacji i Makiet pokazuje, jak uzytkownik przechodzi przez aplikacje. Mapa laczy sekcje menu, pozycje menu, trasy, ekrany potomne, dialogi i makiety elementarne.

## 2. Poziomy mapy

| Poziom | Dokument | Zawartosc |
|---|---|---|
| Globalny | `00_GLOBAL/01_MAPA_NAWIGACJI_I_MAKIET.md` | Wszystkie sekcje menu i ekrany publiczne. |
| Sekcja menu | `NN_Sekcja/01_DIAGRAM_SEKCJI.md` | Pozycje w danej sekcji i ich glowne przejscia. |
| Pozycja menu | `NN_Sekcja/Pozycja/01_MAPA_MAKIET_POZYCJI.md` | Ekran startowy, trasy potomne, dialogi i operacje. |
| Elementy elementarne | `02_ELEMENTY_ELEMENTARNE.md` | Lista ekranow, dialogow, gridow, formularzy i podgladow. |

## 3. Diagramy

Diagramy tworzy sie w Mermaid. Po diagramie zawsze wystepuje tabela linkow Markdown. Tabela jest glownym mechanizmem przejscia do dokumentow.

## 4. Kryterium tworzenia folderu pozycji

Folder pozycji menu tworzy sie, jezeli pozycja posiada:

- trase aplikacji,
- ekran potomny dodawania albo edycji,
- dialog,
- podglad PDF,
- operacje masowe,
- osobny przeplyw aplikacyjny.

## 5. Nazewnictwo

Nazwy katalogow sekcji sa numerowane zgodnie z kolejnoscia w menu bocznym. Nazwy pozycji menu sa zapisywane bez spacji, na przyklad `BankAccounts`.
