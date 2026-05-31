# Wytyczne dokumentacji projektu AOS

> **UWAGA: Wytyczne startowe — wersja 0.1**
> Pliki w tym katalogu są oryginalnymi wytycznymi przekazanymi przez właściciela projektu.
> Są źródłem prawdy dla całego procesu dokumentacyjnego.
> Nazwa modelu w wytycznych: „Agent Codex 5.5 (bardzo wysoki)" = „Agent Claudiusz Sonte 4.6 max" (wykonawca rzeczywisty).

Ten katalog zawiera **kompletny i obowiązujący** zestaw reguł dla wytwarzania dokumentacji projektu AOS. Wszelka praca agentów oraz autorów-ludzi musi się do nich stosować bez wyjątków.

## Status

Wytyczne są dokumentem żywym. Każda zmiana musi być odnotowana w rejestrze zmian danego pliku oraz w globalnym dzienniku zmian wytycznych (do założenia w momencie pierwszej modyfikacji).

## Spis treści

| Plik | Zakres |
|---|---|
| `01_zasady_zlote_i_ogolne.md` | Złote zasady, których nie wolno łamać. Reguły wspólne dla całej dokumentacji. |
| `02_struktura_dokumentacji.md` | Pełna struktura katalogów `doc_AI/`, podział na sekcje, hierarchia. |
| `03_szablony_dokumentow.md` | Szablony per typ dokumentu (ekran, API, encja, proces, UC, BPMN, test itd.). |
| `04_jezyk_styl_i_konwencje.md` | Język, ton, nazewnictwo plików, konwencje diagramów, formatowanie tabel. |
| `05_agenci_i_role.md` | Definicje typów agentów, ich celów, granic odpowiedzialności i osobowości. |
| `06_plan_i_kolejnosc_pracy.md` | Fazy projektu dokumentacyjnego od archiwizacji do walidacji. |
| `07_mapowania_i_slowniki.md` | Wymagane mapy powiązań między elementami i wymagane słowniki. |

## Sposób użycia

Każdy nowy agent (lub człowiek) podejmujący pracę nad dokumentacją zaczyna od przeczytania **wszystkich** plików w tym katalogu, w kolejności podanej w spisie treści. Praca bez znajomości wytycznych jest niedopuszczalna.

## Hierarchia źródeł prawdy

W razie konfliktu obowiązuje następująca hierarchia (od najwyższego do najniższego priorytetu):

1. Decyzja właściciela projektu wydana w trakcie pracy.
2. `01_zasady_zlote_i_ogolne.md` — złote zasady.
3. Pozostałe pliki wytycznych.
4. Kod źródłowy projektu.
5. Konwencje branżowe (BPMN 2.0, Mermaid, Markdown CommonMark itd.).

Stara dokumentacja w katalogu `archiwum/` **nie jest źródłem prawdy w żadnym przypadku** i nie wolno z niej korzystać.

## Rejestr zmian katalogu wytycznych

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | (data utworzenia) | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja kompletu wytycznych. |
