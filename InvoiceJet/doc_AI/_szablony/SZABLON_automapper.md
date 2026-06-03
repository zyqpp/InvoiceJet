# {TYTUL_PROFILU} — profil AutoMapper

| Pole | Wartość |
|---|---|
| ID dokumentu | {KLASA-BIZ-NAZWA_PROFILU} |
| Typ dokumentu | automapper |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten profil AutoMapper. Między jakimi typami realizuje mapowanie i w jakim kontekście biznesowym jest stosowany. */}
{OPIS_BIZNESOWY_PROFILU}

## Charakterystyka profilu

| Atrybut | Wartość |
|---|---|
| Nazwa klasy profilu | `{NazwaKlasyProfilu}` |
| Przestrzeń nazw | `{Namespace.Pelna.NazwaKlasyProfilu}` |
| Plik źródłowy | {LINK_DO_PLIKU_CS} |
| Rejestracja w DI | {Nie dotyczy — AutoMapper skanuje automatycznie / LINK_DO_PROGRAM_CS} |

## Mapowania

{/* Instrukcja: Każdy wiersz to jedna para typów mapowanych w tym profilu (jedno wywołanie CreateMap). */}

| Źródło | Cel | Kierunek odwrotny | Opis celu mapowania |
|---|---|---|---|
| `{NazwaTypuZrodlowego}` | `{NazwaTypuDocelowego}` | {tak / nie} | {OPIS} |

## Konfiguracja mapowania pól

{/* Instrukcja: Opisz pola, dla których zastosowano niestandardową konfigurację (ForMember, Ignore, MapFrom itp.). Pola mapowane 1:1 o tej samej nazwie pomijamy — są domyślne. */}

### `{NazwaTypuZrodlowego}` → `{NazwaTypuDocelowego}`

| Pole docelowe | Konfiguracja | Opis |
|---|---|---|
| `{NazwaPolaDocelowego}` | `ForMember(d => d.{Pole}, opt => opt.MapFrom(s => s.{Pole}))` | {OPIS_DLACZEGO_NIESTANDARDOWE} |
| `{NazwaPolaDocelowego2}` | `ForMember(d => d.{Pole2}, opt => opt.Ignore())` | {OPIS_DLACZEGO_IGNOROWANE} |

## Fragment kodu

{/* Instrukcja: Wklej kluczowy fragment profilu (nie całą klasę — tylko CreateMap z konfiguracją). */}

```csharp
{FRAGMENT_KODU_PROFILU}
```

## Powiązania

- Typy źródłowe: {LINKI_DO_ENCJI_LUB_DTO}
- Typy docelowe: {LINKI_DO_DTO}
- Wywoływane w serwisach: {LINKI_DO_SERWISOW_UZYWAJACYCH_AUTOMAPPERA}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
