# 09_procesy_biznesowe — Analityczny katalog procesów biznesowych

Dokumentacja procesów biznesowych InvoiceJet z perspektywy analitycznej (PM, tester, biznes).
Każdy dokument BP-NN opisuje: cel biznesowy, aktorów, przebieg główny, reguły biznesowe, wyjątki i diagram sekwencji.

> Oddzielna perspektywa techniczna: `doc_AI/02_procesy/` — szczegółowe kroki implementacyjne dla developerów.

## Katalog procesów BP-NN

### Autentykacja

| ID | Plik | Opis |
|---|---|---|
| BP-AUTH-01 | [autentykacja/BP-AUTH-01_rejestracja.md](autentykacja/BP-AUTH-01_rejestracja.md) | Rejestracja nowego konta użytkownika |
| BP-AUTH-02 | [autentykacja/BP-AUTH-02_logowanie.md](autentykacja/BP-AUTH-02_logowanie.md) | Logowanie i wylogowanie z systemu |

### Dokumenty

| ID | Plik | Opis |
|---|---|---|
| BP-DOC-01 | [dokumenty/BP-DOC-01_wystawienie_faktury.md](dokumenty/BP-DOC-01_wystawienie_faktury.md) | Wystawienie faktury VAT |
| BP-DOC-02 | [dokumenty/BP-DOC-02_wystawienie_proformy.md](dokumenty/BP-DOC-02_wystawienie_proformy.md) | Wystawienie faktury proforma |
| BP-DOC-03 | [dokumenty/BP-DOC-03_wystawienie_storno.md](dokumenty/BP-DOC-03_wystawienie_storno.md) | Konwersja dokumentów na fakturę storno |
| BP-DOC-04 | [dokumenty/BP-DOC-04_eksport_pdf.md](dokumenty/BP-DOC-04_eksport_pdf.md) | Generowanie i podgląd pliku PDF |
| BP-DOC-05 | [dokumenty/BP-DOC-05_usuwanie_dokumentow.md](dokumenty/BP-DOC-05_usuwanie_dokumentow.md) | Trwałe usuwanie dokumentów |

### Firma i klienci

| ID | Plik | Opis |
|---|---|---|
| BP-FIRM-01 | [firma/BP-FIRM-01_dane_firmy.md](firma/BP-FIRM-01_dane_firmy.md) | Zarządzanie danymi własnej firmy |
| BP-FIRM-02 | [firma/BP-FIRM-02_klienci.md](firma/BP-FIRM-02_klienci.md) | Zarządzanie bazą klientów (kontrahentów) |

### Konfiguracja

| ID | Plik | Opis |
|---|---|---|
| BP-CFG-01 | [konfiguracja/BP-CFG-01_onboarding.md](konfiguracja/BP-CFG-01_onboarding.md) | Pierwsze kroki — onboarding nowego użytkownika |
| BP-CFG-02 | [konfiguracja/BP-CFG-02_konta_bankowe.md](konfiguracja/BP-CFG-02_konta_bankowe.md) | Zarządzanie kontami bankowymi firmy |
| BP-CFG-03 | [konfiguracja/BP-CFG-03_serie_dokumentow.md](konfiguracja/BP-CFG-03_serie_dokumentow.md) | Konfiguracja serii numeracji dokumentów |

### Produkty i usługi

| ID | Plik | Opis |
|---|---|---|
| BP-PRD-01 | [produkty/BP-PRD-01_produkty_i_uslugi.md](produkty/BP-PRD-01_produkty_i_uslugi.md) | Zarządzanie katalogiem produktów i usług |

## Drzewo katalogów

```
09_procesy_biznesowe/
├── README.md                                    ← ten plik
├── mapa_procesow.md                             ← mapa relacji między procesami
├── autentykacja/
│   ├── BP-AUTH-01_rejestracja.md
│   └── BP-AUTH-02_logowanie.md
├── dokumenty/
│   ├── BP-DOC-01_wystawienie_faktury.md
│   ├── BP-DOC-02_wystawienie_proformy.md
│   ├── BP-DOC-03_wystawienie_storno.md
│   ├── BP-DOC-04_eksport_pdf.md
│   └── BP-DOC-05_usuwanie_dokumentow.md
├── firma/
│   ├── BP-FIRM-01_dane_firmy.md
│   └── BP-FIRM-02_klienci.md
├── konfiguracja/
│   ├── BP-CFG-01_onboarding.md
│   ├── BP-CFG-02_konta_bankowe.md
│   └── BP-CFG-03_serie_dokumentow.md
└── produkty/
    └── BP-PRD-01_produkty_i_uslugi.md
```

## Zasada dokumentów BP-NN

Każdy plik BP-NN zawiera wyłącznie perspektywę biznesową:
- Przebieg główny: działania AKTORÓW (nie metod systemowych)
- Reguły biznesowe: tabela ID | Reguła | Objaśnienie (bez kodu)
- Wyjątki: tabela ID | Scenariusz | Warunek | Reakcja systemu
- Diagram sekwencji: uczestnicy = role (Użytkownik, Aplikacja, Serwer, Baza danych)
- Powiązania analityczne + techniczne w osobnych sekcjach

## Stare pliki (do archiwizacji)

Przed migracją do formatu BP-NN istniały następujące pliki BPMN:
- `BPMN-01_WystawienieFaktury.md` → zastąpiony przez BP-DOC-01
- `BPMN-02_Rejestracja_i_OnBoarding.md` → zastąpiony przez BP-AUTH-01 + BP-CFG-01
- `autentykacja/rejestracja_i_logowanie.md` → zastąpiony przez BP-AUTH-01 + BP-AUTH-02
- `dokumenty/wystawienie_faktury.md` → zastąpiony przez BP-DOC-01
- `dokumenty/wystawienie_proformy.md` → zastąpiony przez BP-DOC-02
- `dokumenty/wystawienie_storno.md` → zastąpiony przez BP-DOC-03
- `dokumenty/eksport_pdf.md` → zastąpiony przez BP-DOC-04
- `firma/zarzadzanie_firma.md` → zastąpiony przez BP-FIRM-01 + BP-FIRM-02
- `konfiguracja/konfiguracja_firmy.md` → zastąpiony przez BP-CFG-01 + BP-CFG-02 + BP-CFG-03

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet folderów |
| 0.2 | 2026-06-01 | Agent Claudiusz Sonte 4.6 max | Pełny katalog BP-NN — 13 dokumentów; migracja diagramów sekwencji z 02_procesy |
