# Reguły formatowania Markdown
## Wytyczne językowe AOS — Część 7 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Zasada:** Formatowanie dokumentu AOS jest ustandaryzowane. Agent nie wprowadza własnych preferencji formatowania.

---

## 1. Hierarchia nagłówków

```
# Tytuł dokumentu              ← jeden na cały dokument
## Sekcja główna               ← numerowane: 1, 2, 3...
### Podsekcja                  ← numerowane: 1.1, 1.2...
#### Element szczegółowy       ← np. "#### Pole: firmName"
```

**Zakaz:** Przeskakiwania poziomów (`##` → `####` bez `###` pośredniego).  
**Zakaz:** Więcej niż czterech poziomów zagłębienia.

---

## 2. Tabele

Każda tabela musi posiadać nagłówek z nazwami kolumn oraz wartość `N/D` zamiast pustej komórki.

**Zakaz:** Tabel z więcej niż 8 kolumnami — podziel na dwie tabele tematyczne.

**Obowiązek:** Wyrównanie separatora tabel dla czytelności kodu MD:

```markdown
| Kolumna A | Kolumna B | Kolumna C |
|---|---|---|
| wartość 1 | wartość 2 | N/D |
```

---

## 3. Wartości techniczne — backticki

Wszystkie wartości techniczne muszą być wrapowane w backticki `` ` ``:

| Co wrapować | Przykład |
|---|---|
| Nazwy `formControlName` | `` `productName` `` |
| Endpointy API | `` `GET /api/products` `` |
| Walidatory | `` `Validators.required` `` |
| Nazwy klas Angular | `` `ClientsComponent` `` |
| Nazwy serwisów i metod | `` `firmService.getClients()` `` |
| Nazwy interfejsów TS | `` `IFirm` `` |
| Selektory CSS | `` `[formControlName="firmName"]` `` |
| Nazwy plików | `` `clients.component.ts` `` |
| Metody HTTP | `` `GET` ``, `` `POST` ``, `` `PUT` ``, `` `DELETE` `` |
| Wartości enumeracji | `` `Unpaid` ``, `` `RON` `` |

**Bloki kodu wieloliniowego** — fenced code blocks z oznaczeniem języka:

````markdown
```typescript
this.clientForm = this.fb.group({
  firmName: ['', Validators.required]
});
```
````

---

## 4. Pogrubienie i kursywa

**Pogrubienie** (`**tekst**`) — wyłącznie dla:
- Nazw sekcji przywołanych w tekście ciągłym: `Sekcja **Pola formularza**`
- Kluczowych wartości w opisach reguł: `Pole jest **wymagane**`
- Terminów definiowanych po raz pierwszy w dokumencie

*Kursywa* (`*tekst*`) — wyłącznie dla:
- Tytułów dokumentów zewnętrznych przywołanych w tekście

**Zakaz:** Pogrubienia dla efektu estetycznego lub podkreślenia ważności fragmentu.  
**Zakaz:** Kursywy dla wartości technicznych (do tego służą backticki).

---

## 5. Listy

**Listy punktowane** (`-`) — dla zestawień bez wymaganej kolejności.  
**Listy numerowane** (`1.`) — wyłącznie dla kroków procesu lub procedur wymagających kolejności.

**Zakaz:** List jednoelementowych — użyj zdania.  
**Zakaz:** Zagnieżdżania list głębiej niż dwa poziomy.

---

## 6. Cytaty blokowe (`>`)

Stosowane wyłącznie dla:

- Komunikatów wyświetlanych użytkownikowi (tekst UI): `> Komunikat błędu: "Pole jest wymagane."`
- Ważnych uwag i zastrzeżeń: `> Uwaga: wartość przekazywana przez parametr data wymaga weryfikacji.`
- Sekcji N/D: `> Sekcja nie dotyczy tego ekranu. Ekran nie zawiera formularza.`

---

## 7. Separatory sekcji

Poziomy separator `---` stosowany wyłącznie między sekcjami głównymi (`##`).  
**Zakaz:** Separatorów wewnątrz podsekcji.

---

## 8. Metadane dokumentu — format obowiązkowy

Każdy dokument AOS zaczyna się od tabeli metadanych w sekcji `## 1. Metadane dokumentu`:

```markdown
| Atrybut | Wartość |
|---|---|
| **Aplikacja** | InvoiceJet |
| **Moduł** | [nazwa modułu] |
| **Ekran** | [biznesowa nazwa ekranu] |
| **Wersja dokumentu** | 1.0 |
| **Data utworzenia** | YYYY-MM-DD |
| **Autor dokumentu** | Agent AI / [imię i nazwisko weryfikującego] |
| **Status** | Roboczy |
| **Plik komponentu** | `src/app/components/[ścieżka]/[nazwa].component.ts` |
| **Plik szablonu** | `src/app/components/[ścieżka]/[nazwa].component.html` |
| **Ścieżka URL** | `/[ścieżka]` |
```

---

## 9. Diagram layoutu ekranu — format obowiązkowy

Każdy dokument AOS zawiera diagram ASCII layoutu w sekcji `### 2.2 Struktura layoutu`:

```
┌─────────────────────────────────────────────────────────┐
│  [NAGŁÓWEK APLIKACJI]                                   │
├──────────────┬──────────────────────────────────────────┤
│              │  [TYTUŁ EKRANU]         [PRZYCISKI TOP]  │
│  [SIDEBAR]   ├──────────────────────────────────────────┤
│              │  [SEKCJA — np. filtry, formularz, grid]  │
└──────────────┴──────────────────────────────────────────┘
```

Używaj wyłącznie znaków: `┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ │ ─`  
**Zakaz:** Używania `+`, `-`, `|` jako zastępników znaków ramki.

---

## 10. Wersjonowanie dokumentu — format obowiązkowy

Ostatnia sekcja każdego dokumentu AOS:

```markdown
## [N]. Historia zmian dokumentu

| Wersja | Data | Autor | Opis zmian |
|---|---|---|---|
| 1.0 | YYYY-MM-DD | Agent AI | Dokument inicjalny — wygenerowany automatycznie. |
```

Numer sekcji `[N]` odpowiada ostatniemu numerowi sekcji w dokumencie.
