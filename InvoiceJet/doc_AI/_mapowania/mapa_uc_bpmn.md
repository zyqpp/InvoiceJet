# Mapa: UC ↔ procesy biznesowe BPMN (M-04)

| Pole | Wartość |
|---|---|
| ID dokumentu | M-04 |
| Typ dokumentu | mapa krzyżowa |
| Wersja | 0.1 |
| Status | szkic |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Data | 2026-05-31 |

## Streszczenie

Mapa łączy przypadki użycia (UC) ze zdefiniowanymi procesami biznesowymi (BPMN). Dla każdego UC wskazuje plik specyfikacji UC oraz powiązany plik opisu procesu BPMN. Pozwala nawigować między wymaganiami funkcjonalnymi a modelami procesów.

## Tabela mapowań

| ID UC | Nazwa UC | Plik UC | Powiązany proces BPMN | Plik BPMN |
|---|---|---|---|---|
| UC-AUTH-01 | Rejestracja użytkownika | [`../07_use_case/globalny/uc_autentykacja.md`](../07_use_case/globalny/uc_autentykacja.md) | Rejestracja i logowanie | [`../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md`](../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md) |
| UC-AUTH-02 | Logowanie użytkownika | [`../07_use_case/globalny/uc_autentykacja.md`](../07_use_case/globalny/uc_autentykacja.md) | Rejestracja i logowanie | [`../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md`](../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md) |
| UC-AUTH-03 | Wylogowanie użytkownika | [`../07_use_case/globalny/uc_autentykacja.md`](../07_use_case/globalny/uc_autentykacja.md) | Rejestracja i logowanie | [`../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md`](../09_procesy_biznesowe/autentykacja/rejestracja_i_logowanie.md) |
| UC-FIRM-01 | Zarządzanie danymi własnej firmy | [`../07_use_case/firma/uc_firma.md`](../07_use_case/firma/uc_firma.md) | Zarządzanie firmą | [`../09_procesy_biznesowe/firma/zarzadzanie_firma.md`](../09_procesy_biznesowe/firma/zarzadzanie_firma.md) |
| UC-FIRM-02 | Konfiguracja firmy (ANAF) | [`../07_use_case/firma/uc_firma.md`](../07_use_case/firma/uc_firma.md) | Konfiguracja firmy | [`../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md`](../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md) |
| UC-FIRM-03 | Zarządzanie klientami | [`../07_use_case/firma/uc_firma.md`](../07_use_case/firma/uc_firma.md) | Zarządzanie firmą | [`../09_procesy_biznesowe/firma/zarzadzanie_firma.md`](../09_procesy_biznesowe/firma/zarzadzanie_firma.md) |
| UC-PROD-01 | Zarządzanie produktami | [`../07_use_case/produkty/uc_produkty.md`](../07_use_case/produkty/uc_produkty.md) | [Do weryfikacji] | [Do weryfikacji] |
| UC-BANK-01 | Zarządzanie kontami bankowymi | [`../07_use_case/konta_bankowe/uc_konta_bankowe.md`](../07_use_case/konta_bankowe/uc_konta_bankowe.md) | Konfiguracja firmy | [`../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md`](../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md) |
| UC-SERIES-01 | Zarządzanie seriami dokumentów | [`../07_use_case/serie_dokumentow/uc_serie_dokumentow.md`](../07_use_case/serie_dokumentow/uc_serie_dokumentow.md) | Konfiguracja firmy | [`../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md`](../09_procesy_biznesowe/konfiguracja/konfiguracja_firmy.md) |
| UC-DOC-01 | Wystawienie faktury | [`../07_use_case/dokumenty/uc_faktury.md`](../07_use_case/dokumenty/uc_faktury.md) | Wystawienie faktury | [`../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md`](../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md) |
| UC-DOC-02 | Edycja faktury | [`../07_use_case/dokumenty/uc_faktury.md`](../07_use_case/dokumenty/uc_faktury.md) | Wystawienie faktury | [`../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md`](../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md) |
| UC-DOC-03 | Generowanie PDF faktury | [`../07_use_case/dokumenty/uc_faktury.md`](../07_use_case/dokumenty/uc_faktury.md) | Wystawienie faktury | [`../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md`](../09_procesy_biznesowe/dokumenty/wystawienie_faktury.md) |
| UC-DOC-04 | Wystawienie faktury proforma | [`../07_use_case/dokumenty/uc_faktury_proforma.md`](../07_use_case/dokumenty/uc_faktury_proforma.md) | Wystawienie faktury proforma | [Do weryfikacji] |
| UC-DOC-05 | Wystawienie faktury storno | [`../07_use_case/dokumenty/uc_faktury_storno.md`](../07_use_case/dokumenty/uc_faktury_storno.md) | Konwersja na storno | [Do weryfikacji] |
| UC-DASH-01 | Podgląd statystyk dashboardu | [`../07_use_case/dokumenty/uc_dashboard.md`](../07_use_case/dokumenty/uc_dashboard.md) | [Do weryfikacji] | [Do weryfikacji] |

## Legenda

| Kolumna | Opis |
|---|---|
| ID UC | Identyfikator przypadku użycia (konwencja lokalna — wymaga weryfikacji z plikami UC) |
| Plik UC | Ścieżka względna do pliku specyfikacji UC |
| Powiązany proces BPMN | Nazwa procesu biznesowego opisanego notacją BPMN |
| Plik BPMN | Ścieżka względna do pliku opisu procesu |

## Uwagi

- Identyfikatory UC (np. UC-AUTH-01) są roboczymi identyfikatorami nadanymi na potrzeby tej mapy — dokładne ID należy zweryfikować z zawartością plików UC.
- Pozycje oznaczone `[Do weryfikacji]` wskazują na brak pewności co do istnienia odpowiedniego pliku BPMN — należy sprawdzić zawartość katalogu `09_procesy_biznesowe/`.
- Jeden plik UC może obejmować wiele powiązanych przypadków użycia (np. `uc_autentykacja.md` zawiera UC rejestracji, logowania i wylogowania).
- Jeden proces BPMN może pokrywać wiele UC (np. `wystawienie_faktury.md` pokrywa UC-DOC-01, UC-DOC-02, UC-DOC-03).

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
