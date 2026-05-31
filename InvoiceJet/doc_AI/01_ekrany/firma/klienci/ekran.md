# ClientsComponent — Lista klientów

| Pole | Wartość |
|---|---|
| ID dokumentu | EKRAN-Klienci |
| Typ dokumentu | ekran |
| Wersja | 0.1 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 max |
| Data ostatniej modyfikacji | 2026-05-31 |

## Streszczenie

Ekran zarządzania listą firm klientów użytkownika. Prezentuje tabelę z sortowaniem, paginacją i filtrowaniem. Operacje dodawania i edycji klienta realizowane przez dialog Angular Material (`AddEditClientDialogComponent`). Usunięcie zaznaczonych klientów wywołuje API batch. Chroniony przez AuthGuard (rola: User).

## Wizualizacja układu

```
┌────────────────────────────────────────────────────────────────┐
│ Klienci                                     [+ Dodaj klienta]  │
├────────────────────────────────────────────────────────────────┤
│ [Filtr wyszukiwania]                                           │
├──┬──────────┬──────┬────────┬──────────┬────────┬─────────────┤
│☐ │ Nazwa    │ CUI  │ RegCom │ Adres    │ Okręg  │ Miasto      │
├──┼──────────┼──────┼────────┼──────────┼────────┼─────────────┤
│☐ │ ...      │ ...  │ ...    │ ...      │ ...    │ ...         │
├──┴──────────┴──────┴────────┴──────────┴────────┴─────────────┤
│ [Usuń zaznaczone]                          [Paginacja]         │
└────────────────────────────────────────────────────────────────┘
```

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/clients` |
| Wymagana rola/uprawnienie | User (AuthGuard) |
| Punkty wejścia | Klik „Klienci" w Sidebar |
| Powiązany kod komponentu | `src/app/components/firm/clients/clients.component.ts` |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunki | Wymagane uprawnienie |
|---|---|---|---|
| Modal AddEditClientDialog | Klik „Dodaj klienta" | Zawsze | User |
| Modal AddEditClientDialog (edycja) | Klik „Edytuj" przy wierszu | Zawsze | User |

## Sekcje ekranu

### Filtry

| ID filtru | Nazwa w UI | Typ | Link do dokumentu |
|---|---|---|---|
| FILTR-Klienci-Szukaj | Filtr wyszukiwania | input (MatTableDataSource filter) | — |

### Tabele i listy

| ID tabeli | Nazwa | Link do dokumentu |
|---|---|---|
| TAB-Klienci-ListaKlientow | Lista klientów | — |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox (select) | `selection` | Zaznaczanie do operacji batch |
| `name` | `IFirm.name` | Nazwa firmy klienta |
| `cui` | `IFirm.cuiValue` | CUI/NIP rumuński |
| `regCom` | `IFirm.regCom` | Numer rejestracji handlowej |
| `address` | `IFirm.address` | Adres |
| `county` | `IFirm.county` | Okręg |
| `city` | `IFirm.city` | Miasto |

### Pola

Brak (ekran listowy — bez pól formularza bezpośrednio na ekranie).

### Operacje

| ID operacji | Etykieta przycisku | Link do dokumentu |
|---|---|---|
| OP-Klienci-DodajKlienta | Dodaj klienta | — |
| OP-Klienci-EdytujKlienta | Edytuj (przy wierszu) | — |
| OP-Klienci-UsunZaznaczone | Usuń zaznaczone | — |

### Modale

| ID modalu | Nazwa | Wywołane przez | Link do dokumentu |
|---|---|---|---|
| MODAL-Klienci-DodajKlienta | AddEditClientDialog (dodaj) | OP-Klienci-DodajKlienta | `dialog_dodaj_klienta/modal.md` |
| MODAL-Klienci-EdytujKlienta | AddEditClientDialog (edytuj) | OP-Klienci-EdytujKlienta | `dialog_dodaj_klienta/modal.md` |

### Powiadomienia

Brak (anomalia: brak komunikatów sukcesu/błędu dla użytkownika).

## Wywołania API

| Akcja | Endpoint |
|---|---|
| Załadowanie listy (ngOnInit) | [GET /api/Firm/GetUserClientFirms](../../../04_api_i_integracje/01_api_frontend/firm/GET_Firm_GetUserClientFirms.md) |
| Usunięcie zaznaczonych | [PUT /api/Firm/DeleteFirms](../../../04_api_i_integracje/01_api_frontend/firm/PUT_Firm_DeleteFirms.md) (query string) |

## Powiązania

- Powiązane procesy: `../../../02_procesy/firma/pobierz_firmy_klientow/proces.md`
- Powiązane API: `../../../04_api_i_integracje/01_api_frontend/firm/`
- Powiązane UC: Brak

## Powiązania z kodem

- Komponent: `src/app/components/firm/clients/clients.component.ts`
- Szablon HTML: `src/app/components/firm/clients/clients.component.html`

## Informacje dla testów

| Aspekt | Wartość |
|---|---|
| Stabilne selektory | Brak `data-cy` — do uzupełnienia |

## Wątpliwości i braki

- `console.log(firms)` aktywny w metodzie `getUserFirms()` w kodzie produkcyjnym.

## Rejestr zmian

| Wersja | Data | Autor | Opis zmiany |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — adaptacja z `clients/clients.md`. |
