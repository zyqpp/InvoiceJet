# {NAZWA_DTO} — DTO

| Pole | Wartość |
|---|---|
| ID dokumentu | {DTO-NAZWA_DTO} |
| Typ dokumentu | DTO |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

{/* Instrukcja: 2–4 zdania. Czym jest ten DTO z perspektywy technicznej i biznesowej. Do czego służy, w jakim kontekście jest używany. */}
{OPIS_BIZNESOWY_DTO}

## Charakterystyka DTO

| Atrybut | Wartość |
|---|---|
| Nazwa | `{NazwaDto}` |
| Przestrzeń nazw | `{Namespace.Pelna.NazwaDto}` |
| Cel | {1–2 zdania opisujące cel DTO} |
| Kierunek użycia | {żądanie / odpowiedź / oba} |
| Plik źródłowy | {LINK_DO_PLIKU_CS} |

## Pola

{/* Instrukcja: Wymień wszystkie pola DTO. "Wymagane" dotyczy walidacji po stronie backendu (atrybuty [Required] itp.). "Powiązane pole bazy" to kolumna tabeli, z której pochodzi lub do której trafia wartość. */}

| Pole | Typ C# | Wymagane | Walidacje | Powiązane pole bazy | Powiązany słownik |
|---|---|---|---|---|---|
| `{NazwaPola}` | `{string / int / decimal / DateTime / bool / Guid}` | {tak / nie} | {[Required] / [MaxLength(255)] / [Range(0, 100)] / Brak} | {schema.tabela.kolumna — LINK} | {LINK_DO_SLOWNIKA_LUB_Nie dotyczy} |

## Walidacje zbiorcze

{/* Instrukcja: Opisz reguły walidacji dotyczące całego DTO (a nie pojedynczych pól). Np. "data od" < "data do". Jeśli brak — wpisz: "Brak". */}
Brak.

## Mapowania

{/* Instrukcja: Opisz, jak ten DTO jest mapowany. Podaj linki do profili AutoMapper oraz metod ręcznego mapowania. */}

| Kierunek | Źródło | Cel | Profil AutoMapper / metoda |
|---|---|---|---|
| encja → DTO | `{NazwaEncji}` | `{NazwaDto}` | {LINK_DO_PROFILU_AUTOMAPPER} |
| DTO → encja | `{NazwaDto}` | `{NazwaEncji}` | {LINK_DO_PROFILU_AUTOMAPPER} |

## Wykorzystanie

{/* Instrukcja: Wymień miejsca w kodzie, gdzie ten DTO jest używany (endpointy, serwisy). */}

| Kontekst | Rola DTO | Link |
|---|---|---|
| {NAZWA_ENDPOINTU_LUB_METODY} | {ciało żądania / ciało odpowiedzi / parametr serwisu} | {LINK_DO_DOKUMENTU_API_LUB_PLIKU} |

## Powiązania

- Powiązane endpointy API: {LINKI_DO_ENDPOINTOW}
- Powiązane tabele DB: {LINKI_DO_TABEL_DB}
- Profil AutoMapper: {LINK_DO_DOKUMENTU_AUTOMAPPER}

## Wątpliwości i braki

{/* Instrukcja: Lista rzeczy nieustalonych z kodu lub wymagających decyzji właściciela projektu. Jeśli brak — wpisz: "Brak". */}
Brak.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
