# 01. Zasady złote i ogólne

## Metryka dokumentu

| Pole | Wartość |
|---|---|
| Autor | Właściciel projektu + Agent Claudiusz Sonte 4.6 max |
| Wersja | 0.1 |
| Status | Obowiązujący |

## A. Złote zasady (nienegocjowalne)

Te reguły mają najwyższy priorytet. Złamanie którejkolwiek z nich jest błędem krytycznym i wymaga natychmiastowej korekty.

**ZZ-01. Język polski z polskimi znakami.** Cała dokumentacja powstaje w języku polskim, z pełnymi polskimi znakami diakrytycznymi (ą, ć, ę, ł, ń, ó, ś, ź, ż). Wyjątkiem są cytaty z kodu, nazwy własne technologii i terminy, które utraciłyby precyzję w tłumaczeniu (np. `DTO`, `LINQ`, `endpoint`).

**ZZ-02. Nazwy z kodu cytujemy 1:1.** Nazwy plików, klas, metod, kolumn, tabel, schem, endpointów, ról, uprawnień itd. zapisujemy dokładnie tak, jak występują w kodzie. Bez polonizacji, bez upiększania, bez zmiany wielkości liter, bez tłumaczenia. Nazwa w kodzie jest faktem, nie sugestią.

**ZZ-03. Stara dokumentacja jest nieistniejąca.** Cała wcześniejsza dokumentacja zostaje przeniesiona do `archiwum/` w roocie projektu w Fazie 0. Od tego momentu żaden agent ani człowiek pracujący nad nową dokumentacją do `archiwum/` nie zagląda. Nie jest źródłem prawdy. Nie jest inspiracją. Nie istnieje.

**ZZ-04. Brak nadinterpretacji.** Jeśli czegoś nie da się ustalić z kodu — odnotowujemy to wprost (sekcja „Wątpliwości i braki" w danym dokumencie). Nie zgadujemy, nie konfabulujemy, nie wypełniamy luk wyobraźnią. „Nie wiem" jest legalną i wymaganą odpowiedzią.

**ZZ-05. Wszystko musi być powiązane.** Każdy dokument linkuje do innych dokumentów, których dotyczy, oraz do plików z kodem, które dokumentuje (gdy to ma sens — np. dokument BPMN nie linkuje do kodu, dokument ekranu linkuje do kodu komponentu i kontrolera). Dokument-wyspa jest błędem.

**ZZ-06. Każdy katalog ma `README.md`.** README pełni rolę mapy folderu: krótki opis biznesowy zawartości, lista podkatalogów i plików z jednolinijkowymi opisami, linki do najważniejszych dokumentów wewnątrz. Opisy biznesowe finalizujemy na końcu projektu (kiedy zawartość folderu jest już znana), ale szkielet README z drzewem powstaje od razu po utworzeniu katalogu.

**ZZ-07. Dokumenty są małe.** Lepiej dziesięć dokumentów po dwie strony niż jeden na dwadzieścia. Granica decyzji: jeśli dokument musiałby mieć więcej niż jeden poziom nagłówków zagnieżdżonych głęboko, albo użytkownik musiałby scrollować, żeby zrozumieć, gdzie jest — podziel.

**ZZ-08. Każdy dokument ma metrykę i rejestr zmian.** Metryka na górze (autor, wersja, status, data), rejestr zmian na dole (tabela: wersja, data, autor, opis zmiany). Autor zapisuje się jako pełna nazwa modelu, np. **Agent Claudiusz Sonte 4.6 max**. Jeśli pracuje pod inną nazwą modelu — używa tej.

**ZZ-09. Szablony są uniwersalne.** Szablony dokumentów (`wytyczne/03_szablony_dokumentow.md`) są oderwane od konkretnego stosu technologicznego. Mają sens dla aplikacji webowej z dowolnym frontendem i dowolnym backendem. Jeżeli technologia projektu wymusza nową sekcję — proponujemy zmianę wytycznych, nie przemycamy jej do dokumentu.

**ZZ-10. Dokumentacja ma być czytelna dla człowieka i przyswajalna dla RAG.** Krótkie akapity, jednoznaczne pojęcia, jawne nagłówki, brak ukrytego kontekstu. Pojęcia spoza słownika są błędem — każdy termin używany w dokumentacji znajduje się w słowniku biznesowym lub technicznym.

## B. Reguły ogólne (obowiązujące domyślnie, można odstąpić tylko za wyraźną decyzją właściciela projektu)

**RO-01. Standardy diagramów.** Diagramy domyślnie w formacie Mermaid umieszczanym inline w Markdownie. Wyjątek: diagramy procesów biznesowych w sekcji `09_procesy_biznesowe/` — BPMN 2.0 (źródła i wyrenderowane obrazki). Diagramy ERD dla modelu danych — Mermaid `erDiagram`.

**RO-02. Tabele opisu elementów.** Element aplikacji (pole, operacja, filtr itd.) opisywany jest w formie tabeli dwukolumnowej: po lewej **nazwa atrybutu** (co to jest), po prawej **wartość/treść** (informacja). Atrybuty są wymienione w szablonie danego elementu i kolejność jest niezmienna.

**RO-03. Nazewnictwo plików dokumentacji.** `snake_case`, bez polskich znaków w nazwach plików (tylko w treści). Prefiks numeryczny dla katalogów porządkujących, np. `01_ekrany/`, `02_procesy/`. Pliki opisujące konkretny obiekt z kodu mają nazwę odpowiadającą obiektowi (np. `OrderController.md`, `dbo.Orders.md`) — wówczas zachowujemy oryginalną wielkość liter z kodu.

**RO-04. Linkowanie.** Linki względne (`../05_model_danych/dto/OrderDto.md`), nigdy bezwzględne. Linki do kodu jako linki do plików w repo (`../../InvoiceJetAPI/InvoiceJet.Presentation/Controllers/AuthController.cs`). Każdy link ma czytelny tekst — bez wklejania surowych URL-i w treść.

**RO-05. Format daty.** ISO 8601: `YYYY-MM-DD`. W rejestrach zmian, metrykach i wszędzie indziej.

**RO-06. Wersjonowanie dokumentów.** Semantyczne, w formacie `MAJOR.MINOR`. `MAJOR` zmienia się przy istotnej zmianie zakresu lub struktury dokumentu. `MINOR` przy uzupełnieniach i poprawkach. Pierwsza wersja to `0.1`. `1.0` osiąga się przy akceptacji właściciela projektu.

**RO-07. Brak wodolejstwa.** Każde zdanie ma nieść informację. Sformułowania w rodzaju „warto wspomnieć", „należy zauważyć", „jak wszyscy wiedzą" są zakazane. Piszemy treść, nie metakomentarze.

**RO-08. Spójność z kodem to obowiązek.** Jeżeli kod zmienia się, dokumentacja musi się zmienić. Brak synchronizacji wykrywa Agent-Walidator (patrz `05_agenci_i_role.md`). Dokument niespójny z kodem otrzymuje status `do_aktualizacji` i ma priorytet w kolejce prac.

**RO-09. Identyfikatory elementów.** Każdy istotny element dokumentacji (pole, operacja, krok procesu BPMN, przypadek użycia, scenariusz testowy itd.) ma stabilny identyfikator nadany w jego szablonie. ID nie zmieniają się przy edycji — można je wykorzystywać w mapowaniach krzyżowych i w testach.

**RO-10. Sekcja „Wątpliwości i braki".** Każdy dokument opisujący artefakt z kodu kończy się sekcją „Wątpliwości i braki", w której zapisujemy wszystko, czego nie udało się ustalić jednoznacznie. Pusta sekcja jest dozwolona (i preferowana).

## C. Zasada porządku informacji w dokumencie

Każdy dokument w `doc_AI/` ma następujący porządek:

1. **Tytuł** (`# Nazwa elementu`).
2. **Metryka** (autor, wersja, status, data, ID dokumentu).
3. **Streszczenie** — dwa do czterech zdań, dla człowieka, czym jest opisywany element.
4. **Treść główna** — zgodna z szablonem typu dokumentu z `03_szablony_dokumentow.md`.
5. **Powiązania** — linki do innych dokumentów (powiązane ekrany, API, encje, role, UC, BPMN, testy).
6. **Powiązania z kodem** — linki do plików w repo (gdy ma to zastosowanie).
7. **Wątpliwości i braki**.
8. **Rejestr zmian** — tabela.

Kolejność jest niezmienna. Sekcje, które nie mają zawartości, pozostają z adnotacją „Brak" — nie usuwamy ich.

## Rejestr zmian dokumentu

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Właściciel projektu + Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
