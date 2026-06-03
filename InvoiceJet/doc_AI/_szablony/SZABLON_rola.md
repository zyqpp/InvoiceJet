# {NAZWA_ROLI} — rola użytkownika

| Pole | Wartość |
|---|---|
| ID dokumentu | {ROLA-NAZWA_ROLI} |
| Typ dokumentu | rola |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Kim jest użytkownik w tej roli z perspektywy biznesowej. Jaki zakres działań i dostępu mu przysługuje. */}
{OPIS_BIZNESOWY_ROLI}

## Charakterystyka roli

| Atrybut | Wartość |
|---|---|
| ID roli | {ROLA-NAZWA_ROLI} |
| Nazwa roli w systemie | `{NazwaRoliWKodzie}` |
| Nazwa w UI | {POLSKA_NAZWA_WYSWIETLANA_W_INTERFEJSIE} |
| Typ roli | {systemowa / biznesowa / techniczna} |
| Nadawana przez | {administrator / automatycznie przy rejestracji / Do ustalenia} |
| Zdefiniowana w | {Identity / appsettings / baza danych / kod} |

## Uprawnienia

{/* Instrukcja: Wymień, do jakich ekranów, operacji i zasobów API rola ma dostęp. Kolumna "Typ dostępu": odczyt / zapis / pełny / brak. */}

### Dostęp do ekranów

| Ekran | Typ dostępu | Warunki |
|---|---|---|
| {LINK_DO_EKRANU} | {odczyt / zapis / pełny} | {WARUNEK_LUB_Zawsze} |

### Dostęp do operacji

| Operacja | Typ dostępu | Warunki |
|---|---|---|
| {LINK_DO_OPERACJI} | {dozwolona / zabroniona / warunkowa} | {WARUNEK_LUB_Zawsze} |

### Dostęp do endpointów API

| Endpoint | Typ dostępu |
|---|---|
| {LINK_DO_DOKUMENTU_API} | {dozwolony / zabroniony} |

## Ograniczenia roli

{/* Instrukcja: Opisz, czego ta rola NIE może robić. Jeśli brak — wpisz: "Brak". */}

| Zasób / operacja | Powód ograniczenia |
|---|---|
| {OPIS_ZASOBU_LUB_OPERACJI} | {POWOD_OGRANICZENIA} |

## Powiązania z kodem

- Atrybut autoryzacji: `[Authorize(Roles = "{NazwaRoliWKodzie}")]`
- Konfiguracja polityk: {LINK_DO_PLIKU_KONFIGURACJI_AUTORYZACJI}
- Seeding roli w bazie: {LINK_DO_PLIKU_SEED_LUB_Nie dotyczy}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
