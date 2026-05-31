# FirmDetailsComponent — Dane firmy

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-DaneFirmy |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran zarządzania danymi własnej firmy użytkownika (wystawiającego faktury). Przy pierwszym wejściu bez zarejestrowanej firmy wyświetlany jest formularz dodawania. Gdy firma już istnieje — formularz edycji z przyciskiem „Zapisz" aktywnym tylko przy wykrytych zmianach (uwaga: logika wykrywania zmian zawiera błąd — patrz anomalie). Obsługuje autouzupełnianie danych z rejestru ANAF na podstawie numeru CUI.

## Wizualizacja układu

```
┌─────────────────────────────────────────────────┐
│ Dane firmy                                      │
├─────────────────────────────────────────────────┤
│ Nazwa firmy:   [_______________________________] │
│ CUI:           [_______________________] [☁ ANAF]│
│ Reg. handlowy: [_______________________________] │
│ Adres:         [_______________________________] │
│ Okręg:         [_______________________________] │
│ Miasto:        [_______________________________] │
├─────────────────────────────────────────────────┤
│                              [  Zapisz  ]        │
└─────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/firm-details` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Dane firmy" w Sidebar |
| Powiązany kod komponentu | `src/app/components/firm/firm-details/firm-details.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| Ten sam ekran (odświeżenie danych) | Submit → sukces | Zapis zakończony powodzeniem | User |

## Sekcje ekranu

### Filtry

Brak.

### Tabele i listy

Brak.

### Pola

| ID pola | Nazwa w UI | Wymagalność | Link do dokumentu |
|---|---|---|---|
| POLE-DaneFirmy-firmName | Nazwa firmy | wymagane | — |
| POLE-DaneFirmy-cuiValue | CUI (NIP rumuński) | opcjonalne | — |
| POLE-DaneFirmy-regCom | Numer rejestracji handlowej | opcjonalne | — |
| POLE-DaneFirmy-address | Adres | opcjonalne | — |
| POLE-DaneFirmy-county | Okręg | opcjonalne | — |
| POLE-DaneFirmy-city | Miasto | opcjonalne | — |

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-DaneFirmy-Zapisz | Zapisz | — |
| OP-DaneFirmy-ANAF | Ikona chmury (☁) — pobierz z ANAF | — |

### Modale

Brak.

### Powiadomienia

Brak (komunikaty błędów niejawne — anomalia).

## Pola formularza — szczegóły

| Pole | Kontrolka | Opis |
|---|---|---|
| `firmName` | `mat-form-field` | Nazwa firmy |
| `cuiValue` | `mat-form-field` | CUI (NIP rumuński) + przycisk ikona chmury (ANAF) |
| `regCom` | `mat-form-field` | Numer rejestracji handlowej |
| `address` | `mat-form-field` | Adres |
| `county` | `mat-form-field` | Okręg |
| `city` | `mat-form-field` | Miasto |

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie danych (ngOnInit) | `GET /api/Firm/GetUserActiveFirm` |
| Submit (edycja) | `PUT /api/Firm/EditFirm/false` (`isClient=false`) |
| Submit (dodanie) | `POST /api/Firm/AddFirm/false` (`isClient=false`) |
| Ikona chmury (ANAF) | `GET /api/Firm/fromAnaf/{cuiValue}` → autouzupełnienie pól |

## Metody

| Metoda | Opis |
|---|---|
| `onSubmit()` | Sprawdza `currentUserFirm` → AddFirm (POST) lub EditFirm (PUT) |
| `onCloudIconClick()` | Wywołuje ANAF API i wypełnia pola formularza danymi firmy |
| `isFormChanged()` | Sprawdza czy formularz zmieniony — BŁĘDNA IMPLEMENTACJA (patrz anomalie) |
| `addNewClient()` | Niezaimplementowana — tylko `console.log("Add new client")` |

## Powiązania

- Powiązane procesy: `../../../02_procesy/firma/edytuj_firme/proces.md`, `../../../02_procesy/firma/dodaj_firme/proces.md`, `../../../02_procesy/firma/pobierz_z_anaf/proces.md`
- Powiązane API: `../../../04_api_i_integracje/01_api_frontend/firm/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/firm/firm-details/firm-details.component.ts`
- Szablon HTML: `src/app/components/firm/firm-details/firm-details.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- FA-01: `isFormChanged()` — błędna logika: `JSON.stringify(this.initialFormValues.value)` vs `JSON.stringify(this.initialFormValues)`. `initialFormValues` to plain object, więc `.value` to `undefined`. Porównanie zawsze zwraca `false` — przycisk „Zapisz" nigdy nie blokuje się przy braku zmian.
- FA-02: `addNewClient()` niezaimplementowana — zawiera tylko `console.log("Add new client")`. Przycisk w UI może być widoczny, ale nie wywołuje żadnej akcji.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `firm_details/firm-details.md`. |
