# Mapa Nawigacji i Makiet

## 1. Cel mapy

Mapa Nawigacji i Makiet pokazuje, jak użytkownik przechodzi przez aplikacje. Mapa łączy sekcję menu, pozycje menu, trasy, ekrany potomne, dialogi i makiety elementarne.

## 2. Poziomy mapy

| Poziom | Dokument | Zawartość |
|---|---|---|
| Globalny | `00_GLOBAL/01_MAPA_NAWIGACJI_I_MAKIET.md` | Wszystkie sekcję menu i ekrany publiczne. |
| Sekcja menu | `NN_Sekcja/01_DIAGRAM_SEKCJI.md` | Pozycje w danej sekcji i ich główne przejścia. |
| Pozycja menu | `NN_Sekcja/Pozycja/01_MAPA_MAKIET_POZYCJI.md` | Ekran startowy, trasy potomne, dialogi i operacje. |
| Elementy elementarne | `02_ELEMENTY_ELEMENTARNE.md` | Lista ekranów, dialogów, gridów, formularzy i podglądów. |

## 3. Diagramy

Diagramy tworzy się w Mermaid. Po diagramie zawsze występuje tabela linków Markdown. Tabela jest głównym mechanizmem przejścia do dokumentów.

## 4. Kryterium twórzenia folderu pozycji

Folder pozycji menu tworzy się, jeżeli pozycja posiada:

- trase aplikacji,
- ekran potomny dodawania albo edycji,
- dialog,
- podgląd PDF,
- operacje masowe,
- osobny przepływ aplikacyjny.

## 5. Nazewnictwo

Nazwy katalogow sekcji są numerowane zgodnie z kolejnoscia w menu bocznym. Nazwy pozycji menu są zapisywane bez spacji, na przyklad `BankAccounts`.
