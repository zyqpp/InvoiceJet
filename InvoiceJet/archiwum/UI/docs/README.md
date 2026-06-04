# Dokumentacja AOS — Frontend InvoiceJet

**Status**: Wdrożony 2026-05-29

---

## 📚 Struktura dokumentacji

```
docs/
├── aos/
│   ├── frontend/                 ← Dokumenty ekranów
│   │   ├── E-01_Clients/        ← Katalog ekranu #1
│   │   │   ├── 00_METADANE.md
│   │   │   ├── 01_PRZEGLĄD.md
│   │   │   ├── 02_DANE_I_OPERACJE.md
│   │   │   ├── 03_LOGIKA_BIZNESOWA.md
│   │   │   ├── 04_SCENARIUSZE_TESTOWE.md
│   │   │   └── HISTORIA_ZMIAN.md
│   │   ├── E-02_Products/       ← Katalog ekranu #2
│   │   │   └── [struktura jak wyżej]
│   │   └── ...
│   └── templates/               ← Szablony Markdown
│       ├── TEMPLATE_00_METADANE.md
│       ├── TEMPLATE_01_PRZEGLĄD.md
│       ├── TEMPLATE_02_DANE_I_OPERACJE.md
│       ├── TEMPLATE_03_LOGIKA_BIZNESOWA.md
│       └── TEMPLATE_04_SCENARIUSZE_TESTOWE.md
├── scripts/                     ← Narzędzia automatyzacji
│   ├── create-aos-screen.ps1   ← Tworzenie struktury ekranu
│   └── scan-aos-screens.ps1    ← Generowanie rejestru
├── REJESTR_EKRANÓW.md          ← Generowany rejestr
├── README.md                    ← Ten plik
└── ...
```

---

## 🚀 Quick Start

### 1. Tworzenie dokumentacji dla nowego ekranu

Aby utworzyć strukturę katalogu dla nowego ekranu, użyj skryptu:

```powershell
cd .\docs\scripts
.\create-aos-screen.ps1 -ScreenNumber 1 -ScreenName "Clients"
```

**Rezultat**: Katalog `docs/aos/frontend/E-01_Clients/` z szablonami

### 2. Uzupełnianie dokumentacji

1. Otwórz plik `00_METADANE.md` i wypełnij dane ekranu
2. Otwórz `01_PRZEGLĄD.md` i opisz layout
3. Otwórz `02_DANE_I_OPERACJE.md` i opisz pola + operacje
4. Otwórz `03_LOGIKA_BIZNESOWA.md` i opisz przepływy
5. Otwórz `04_SCENARIUSZE_TESTOWE.md` i dodaj scenariusze testowe

### 3. Generowanie rejestru ekranów

Aby wygenerować aktualny rejestr wszystkich ekranów:

```powershell
cd .\docs\scripts
.\scan-aos-screens.ps1
```

**Rezultat**: `docs/REJESTR_EKRANÓW.md` (zaktualizowany)

---

## 📖 Struktura każdego dokumentu ekranu

Każdy ekran dokumentowany jest w **4 plikach + historia**:

### 00_METADANE.md
- **Szybki lookup**: nazwa, wersja, status, ścieżki do plików
- **Dla kogo**: wszystkich (szybka orientacja)
- **Czytanie**: < 2 min
- **Zawartość**: tabela metadanych + linki do pozostałych dokumentów

### 01_PRZEGLĄD.md
- **Overview ekranu**: layout, komponenty, scenariusz główny
- **Dla kogo**: wszystkich (zrozumienie struktury)
- **Czytanie**: 2-3 min
- **Zawartość**: diagram ASCII, lista komponentów, golden path, stany

### 02_DANE_I_OPERACJE.md
- **Szczegółowy opis pól i operacji**: pola formularza, przyciski, dialogi
- **Dla kogo**: developerów, analityków, testerów
- **Czytanie**: 5-10 min
- **Zawartość**: tabele pól, walidatory, szczegóły operacji, komunikaty

### 03_LOGIKA_BIZNESOWA.md
- **Przepływy danych i reguły biznesowe**: API, integracje, warunki
- **Dla kogo**: architektów, developerów, analityków
- **Czytanie**: 10-15 min
- **Zawartość**: diagramy przepływów, endpointy API, reguły biznesowe, obsługa błędów

### 04_SCENARIUSZE_TESTOWE.md
- **Kroki testowe dla QA**: przypadki testowe, selektory, dane
- **Dla kogo**: testerów, analityków QA
- **Czytanie**: 5-10 min (zależy od liczby scenariuszy)
- **Zawartość**: tabele z krokami, selektory CSS, dane testowe, assercje

### HISTORIA_ZMIAN.md
- **Wersjonowanie dokumentu**: co się zmieniło, kiedy, przez kogo
- **Dla kogo**: wszyscy (audyt)
- **Czytanie**: < 1 min
- **Zawartość**: tabela wersji z datami i opisami zmian

---

## 📋 Role i ich ścieżki czytania

### 👨‍💼 Analityk (BA)
1. **00_METADANE.md** — co to jest?
2. **01_PRZEGLĄD.md** — jak wygląda?
3. **02_DANE_I_OPERACJE.md** — jakie pola?
4. **03_LOGIKA_BIZNESOWA.md** — jakie reguły biznesowe?

### 👨‍💻 Developer
1. **00_METADANE.md** — gdzie są pliki?
2. **02_DANE_I_OPERACJE.md** — jakie pola i operacje?
3. **03_LOGIKA_BIZNESOWA.md** — jakie API i przepływy?
4. **HISTORIA_ZMIAN.md** — co zmieniło się od ostatniej wersji?

### 👨‍🔬 Tester QA
1. **01_PRZEGLĄD.md** — jak wygląda ekran? (golden path)
2. **04_SCENARIUSZE_TESTOWE.md** — jakie scenariusze testować?
3. **02_DANE_I_OPERACJE.md** — jakie selektory i dane testowe?

### 👔 Project Manager / Product Owner
1. **00_METADANE.md** — status dokumentacji
2. **01_PRZEGLĄD.md** — przegląd funkcjonalności
3. **HISTORIA_ZMIAN.md** — tracking zmian

---

## 🎯 Wytyczne pisania

### Zasady absolutne (Z.1–Z.5)

**Z.1 — Precyzja ponad elegancję**
- Zdanie brzmiące technicznie jest lepsze od eleganckiego i wieloznacznego
- ❌ "Pole przyjmuje wartości słownikowe"
- ✅ "Pole akceptuje wartości ze słownika Currency: RON, EUR, USD, GBP"

**Z.2 — Opisujemy to co jest, nie co powinno być**
- Agent opisuje kod, nie interpretuje intencji
- ❌ "Pole powinno mieć minimalną długość 5 znaków"
- ✅ "Pole nie posiada walidatora minLength [WYMAGA WERYFIKACJI]"

**Z.3 — Jedno pojęcie, jedna nazwa**
- "Dialog Edycja klienta" zawsze, nigdy "Dialog edycji", "Modal klienta", itp.

**Z.4 — Dane techniczne w oryginalnym języku**
- Nazwy klas, metody, selectory — zawsze w oryginalnym brzmieniu z kodu
- ✅ `` formControlName: `firmName` ``
- ❌ "kontroler nazwy firmy"

**Z.5 — Opis biznesowy po polsku**
- Co pole oznacza dla użytkownika — zawsze po polsku
- ✅ "Pole CUI — unikalny numer identyfikacji podatkowej firmy"

### Terminologia (słowniki)

Wszystkie dokumenty AOS używają znormalizowanej terminologii:

- **Warstwa techniczna**: `ekran`, `komponent`, `pole`, `grid`, `dialog`, `formularz`
- **Warstwa domenowa** (InvoiceJet): `faktura`, `klient`, `seria dokumentów`, `TVA`, `CUI`
- **Warstwa API**: `endpoint`, `GET`, `POST`, `PUT`, `DELETE`
- **Zakazane**: `strona` (zamiast: `ekran`), `input` (zamiast: `pole`), `modal` (zamiast: `dialog`)

### Markery dokumentu

Gdy brakuje informacji — używaj markerów:

- `[WYMAGA WERYFIKACJI]` — dane istnieją w kodzie ale agent nie może ich ustalić pewnie
- `[BRAK W DOSTARCZONYCH PLIKACH]` — element widoczny na UI ale nie w kodzie
- `[NA PODSTAWIE SCREENSHOTU]` — opisano ze screena, czeka na potwierdzenie kodem
- `[UWAGA: opis]` — agent znalazł potencjalny problem

---

## 🛠️ Narzędzia automatyzacji

### create-aos-screen.ps1
```powershell
.\create-aos-screen.ps1 -ScreenNumber 5 -ScreenName "InvoiceDetails"
```

**Co robi**:
- Tworzy katalog `E-05_InvoiceDetails/`
- Generuje szablony (00–04)
- Personalizuje template do nazwy ekranu
- Tworzy plik HISTORIA_ZMIAN.md

**Parametry**:
- `-ScreenNumber` — numer ekranu (1–999)
- `-ScreenName` — nazwa ekranu (bez spacji)
- `-TemplateDir` — katalog szablonów (domyślnie: docs/aos/templates)
- `-OutputDir` — katalog wyjściowy (domyślnie: docs/aos/frontend)

### scan-aos-screens.ps1
```powershell
.\scan-aos-screens.ps1 -ExportCsv $true
```

**Co robi**:
- Skanuje wszystkie katalogi `E-XX_*`
- Czyta metadane z `00_METADANE.md`
- Generuje rejestr w Markdown
- Opcjonalnie eksportuje CSV

**Parametry**:
- `-AosDir` — katalog do skanowania (domyślnie: docs/aos/frontend)
- `-OutputFile` — plik wyjściowy (domyślnie: docs/REJESTR_EKRANÓW.md)
- `-ExportCsv` — czy eksportować do CSV (domyślnie: $false)

---

## 📊 Workflow dokumentowania (pełny cykl)

### Faza 1: Przygotowanie
```
developer → przygotowuje pliki kodu (komponenty, serwisy, modele)
          → komunikuje zespołowi że ekran jest gotowy
```

### Faza 2: Generowanie struktury
```
analityk → uruchamia skrypt create-aos-screen.ps1
         → tworzy katalog ekranu z szablonami
```

### Faza 3: Analiza kodu przez agenta
```
agent → czyta kod z pakietu plików
      → wczytuje wytyczne jezykowe i skill
      → analizuje komponenty, serwisy, modele
      → generuje dokumenty w katalogu ekranu
      → oznacza [WYMAGA WERYFIKACJI] gdy brakuje informacji
```

### Faza 4: Weryfikacja analityczna
```
analityk → czyta dokumenty agenta
         → porównuje z działającą aplikacją
         → poprawia błędy, dodaje brakujące dane
         → zmienia status na "Do weryfikacji technicznej"
```

### Faza 5: Weryfikacja techniczna
```
developer → czyta dokumenty (szczególnie 02 i 03)
          → uzupełnia [WYMAGA WERYFIKACJI] markers
          → potwierdza dane techniczne
          → zmienia status na "Do zatwierdzenia"
```

### Faza 6: Zatwierdzenie
```
product-owner → przegląda status
              → zatwierdza dokument
              → zmienia status na "Zatwierdzony"
              → dokument gotowy do użytku
```

### Faza 7: Utrzymanie
```
każdy-kto-zmienia-kod → gdy aplikacja się zmienia
                     → aktualizuje odpowiednie dokumenty
                     → zmienia status na "Wymaga aktualizacji"
                     → generuje nową wersję w HISTORIA_ZMIAN.md
```

---

## 🔗 Powiązane dokumenty

- **Wytyczne jezykowe**: Pliki 01_ZASADY_NADRZEDNE_I_TON.md przez 07_REGULY_FORMATOWANIA_MARKDOWN.md (katalog `./wytyczne/`)
- **Skill agenta**: SKILL_aos-frontend-angular.md (katalog `./skills/`)
- **Proces dokumentowania**: PROCES_DOKUMENTOWANIA_FRONTU.md

---

## ⚡ Tips & Tricks

### Szybkie uruchamianie skryptów
```powershell
# Dodaj alias do profilu PowerShell
Function Create-AosScreen { & .\docs\scripts\create-aos-screen.ps1 @args }
Function Scan-AosScreens { & .\docs\scripts\scan-aos-screens.ps1 @args }

# Teraz możesz skracać:
Create-AosScreen -ScreenNumber 1 -ScreenName "Clients"
Scan-AosScreens -ExportCsv $true
```

### Automatyzacja w CI/CD
```powershell
# W pipeline (GitLab CI, GitHub Actions, Azure Pipelines)
- name: Regenerate AOS Registry
  run: |
    pwsh .\docs\scripts\scan-aos-screens.ps1
    git add docs/REJESTR_EKRANÓW.md
    git commit -m "docs: aktualizacja rejestru ekranów [skip ci]"
```

### Czytanie dokumentów z markdown viewer
```bash
# VS Code → zainstalować rozszerzenie "Markdown Preview Enhanced"
# Terminal → pandoc docs/aos/frontend/E-01_Clients/01_PRZEGLĄD.md | less
```

---

## 📞 Support

Jeśli masz problemy:

1. Sprawdź wytyczne w pliku `01_ZASADY_NADRZEDNE_I_TON.md`
2. Przeczytaj skill w `SKILL_aos-frontend-angular.md`
3. Spróbuj ponownie wygenerować dokument
4. Skontaktuj się z architektem systemu

---

**Ostatnia aktualizacja**: 2026-05-29  
**Status**: ✅ Aktywny  
**Wersja**: 1.0
