# Słownik pojęć procesowych i dokumentacyjnych
## Wytyczne językowe AOS — Część 4 z 7

**Obowiązuje:** Każda sesja generowania dokumentacji AOS  
**Zasada:** Pojęcia opisujące sam proces tworzenia dokumentacji i role w tym procesie muszą być stosowane jednolicie we wszystkich dokumentach.

---

## 1. Artefakty dokumentacyjne

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **dokument AOS** | Analityczny Opis Systemu — ustandaryzowany dokument opisujący jeden ekran aplikacji, wytworzony zgodnie z szablonem AOS. | dokumentacja ekranu, spec, specyfikacja (gdy mowa o AOS), opis funkcjonalny |
| **szablon AOS** | Plik `AOS_FRONTEND_TEMPLATE.md` definiujący strukturę i sekcje dokumentu AOS. | template (ang.), wzorzec dokumentu |
| **primer systemu** | Dokument opisujący stos technologiczny i architekturę aplikacji — wczytywany jako kontekst inicjalny przed sesją. | dokument architektury (gdy mowa o primerze), system overview |
| **rejestr ekranów** | Arkusz lub plik Markdown zawierający listę wszystkich ekranów aplikacji ze statusami dokumentacji i priorytetami. | backlog dokumentacji, lista ekranów, inventory |

---

## 2. Narzędzia i komponenty procesu

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **skill** | Plik `SKILL.md` zawierający instrukcje sterujące zachowaniem agenta podczas sesji dokumentowania. | prompt systemowy (gdy mowa o skilu), instrukcja agenta, system prompt |
| **agent** | Instancja modelu LLM (Claude) z załadowanym skillem, prowadząca sesję dokumentowania jednego ekranu. | model, Claude (gdy mowa o roli w procesie), AI, bot |
| **pakiet plików** | Zestaw plików kodu przekazywanych agentowi jako kontekst dla jednej sesji dokumentowania. | kontekst agenta, input agenta |
| **sesja dokumentowania** | Pojedyncza rozmowa z agentem poświęcona udokumentowaniu jednego ekranu aplikacji. | sesja AI, uruchomienie agenta |

---

## 3. Etapy procesu

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **weryfikacja analityczna** | Etap A procesu — porównanie wygenerowanego dokumentu AOS z działającą aplikacją przez analityka. | review, przegląd dokumentu, analiza |
| **weryfikacja techniczna** | Etap B procesu — uzupełnienie danych technicznych i pozycji `[WYMAGA WERYFIKACJI]` przez dewelopera. | tech review, przegląd kodu, code review |
| **zatwierdzenie dokumentu** | Formalne nadanie statusu `Zatwierdzony` po ukończeniu obu etapów weryfikacji. | akceptacja, sign-off, approve |

---

## 4. Role w procesie

| Termin obowiązujący | Definicja | Nazwy zakazane |
|---|---|---|
| **analityk** | Osoba zarządzająca procesem dokumentowania: przygotowuje pakiet plików, uruchamia agenta, przeprowadza weryfikację analityczną. | product owner (gdy nie chodzi o rolę PO), BA |
| **deweloper** | Programista przeprowadzający weryfikację techniczną i uzupełniający dane techniczne w dokumencie AOS. | developer (ang. w opisach procesowych po polsku), programista frontendowy |
| **tester** | Osoba korzystająca z dokumentu AOS jako źródła scenariuszy testowych i selektorów do automatyzacji. | QA (gdy mowa o roli testera) |

---

## 5. Statusy dokumentu AOS

Statusy są ściśle zdefiniowane i muszą być stosowane wyłącznie w podanej formie:

| Status | Znaczenie | Poprzedni status | Następny status |
|---|---|---|---|
| `Roboczy` | Dokument wygenerowany przez agenta, bez weryfikacji. | — | `Do weryfikacji technicznej` |
| `Do weryfikacji technicznej` | Weryfikacja analityczna ukończona, czeka na dewelopera. | `Roboczy` | `Do zatwierdzenia` |
| `Do zatwierdzenia` | Obie weryfikacje ukończone, czeka na formalny sign-off. | `Do weryfikacji technicznej` | `Zatwierdzony` |
| `Zatwierdzony` | Dokument produkcyjny — może być używany przez testerów i analityków. | `Do zatwierdzenia` | `Wymaga aktualizacji` |
| `Wymaga aktualizacji` | Aplikacja się zmieniła — dokument jest nieaktualny i wymaga re-runu agenta lub ręcznej korekty. | `Zatwierdzony` | `Roboczy` |

---

## 6. Klasyfikacja ekranów według rozmiaru

| Termin obowiązujący | Definicja | Przykłady (InvoiceJet) |
|---|---|---|
| **ekran Prosty** | Grid z CRUD do 8 kolumn lub formularz do 8 pól, brak złożonych zależności między polami. | Clients, Bank Accounts, Document Series, Login |
| **ekran Standardowy** | Formularz 9–20 pól lub grid z filtrami, 1–3 dialogi. | Products, Firm Details, Invoice Proformas |
| **ekran Duży** | Formularz 21+ pól, rozbudowane walidacje, wiele dialogów, integracje zewnętrzne. | Add/Edit Invoice, Invoice Stornos |
| **ekran Złożony** | Wiele zagnieżdżonych komponentów, dynamiczne sekcje, niestandardowa logika biznesowa. | Dashboard z chartami, wieloetapowe formularze |
