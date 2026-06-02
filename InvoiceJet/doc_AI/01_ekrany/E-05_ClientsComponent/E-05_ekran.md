# E-05 ClientsComponent — Lista klientów

| Pole | Wartość |
|---|---|
| ID dokumentu | E-05 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran zarządzania listą firm klientów użytkownika. Prezentuje tabelę z sortowaniem, paginacją i filtrowaniem po stronie klienta. Operacje dodawania i edycji klienta realizowane przez dialog Angular Material (`AddEditClientDialogComponent`). Usunięcie zaznaczonych klientów wywołuje API batch. Wszystkie dane izolowane per UserFirm. Chroniony przez `AuthGuard` (rola: User).

---

## Wizualizacja układu

```
┌────────────────────────────────────────────────────────────────┐
│ Klienci                                     [+ Dodaj klienta]  │
├────────────────────────────────────────────────────────────────┤
│ [Filtr wyszukiwania ________________________]                  │
├──┬──────────┬──────┬────────┬──────────┬────────┬─────────────┤
│☐ │ Nazwa    │ CUI  │ RegCom │ Adres    │ Okręg  │ Miasto      │
├──┼──────────┼──────┼────────┼──────────┼────────┼─────────────┤
│☐ │ ...      │ ...  │ ...    │ ...      │ ...    │ ...         │
├──┴──────────┴──────┴────────┴──────────┴────────┴─────────────┤
│ [Usuń zaznaczone]                          [Paginacja]         │
└────────────────────────────────────────────────────────────────┘
```

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/clients` |
| Wymagana rola | User (AuthGuard JWT) |
| Punkty wejścia | Klik „Klienci" w Sidebar |
| Komponent Angular | [`ClientsComponent`](../../../../InvoiceJetUI/src/app/components/firm/clients/clients.component.ts) |
| Szablon HTML | [`clients.component.html`](../../../../InvoiceJetUI/src/app/components/firm/clients/clients.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| Modal AddEditClientDialog (dodaj) | [OP-E05-01](E-05_OP-01.md) | zawsze | User |
| Modal AddEditClientDialog (edytuj) | [OP-E05-02](E-05_OP-02.md) | zawsze | User |

---

## Filtry

| ID | Nazwa w UI | Typ | Dokument |
|---|---|---|---|
| FILTR-E05-01 | Filtr wyszukiwania | input (MatTableDataSource filter, po stronie klienta) | [E-05_FILTR-01.md](E-05_FILTR-01.md) |

## Tabele i listy

| ID | Nazwa | Dokument |
|---|---|---|
| TAB-E05-01 | Lista klientów | [E-05_TAB-01.md](E-05_TAB-01.md) |

### Kolumny tabeli

| Kolumna | Źródło danych | Opis |
|---|---|---|
| Checkbox | `selection` | Zaznaczanie do operacji batch |
| `name` | `IFirm.name` | Nazwa firmy klienta |
| `cui` | `IFirm.cuiValue` | CUI/NIP rumuński |
| `regCom` | `IFirm.regCom` | Numer rejestracji handlowej |
| `address` | `IFirm.address` | Adres |
| `county` | `IFirm.county` | Okręg |
| `city` | `IFirm.city` | Miasto |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E05-01 | Dodaj klienta | [E-05_OP-01.md](E-05_OP-01.md) |
| OP-E05-02 | Edytuj (przy wierszu) | [E-05_OP-02.md](E-05_OP-02.md) |
| OP-E05-03 | Usuń zaznaczone | [E-05_OP-03.md](E-05_OP-03.md) |

## Modale

| ID | Nazwa | Wywołane przez |
|---|---|---|
| MODAL-E05-01 | AddEditClientDialog (dodaj) | OP-E05-01 |
| MODAL-E05-02 | AddEditClientDialog (edytuj) | OP-E05-02 |

## Scenariusze testowe

→ [E-05_TC.md](E-05_TC.md) — prereq JWT, prereq DB, selektory CSS, 5 scenariuszy e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie listy (ngOnInit) | GET | `/api/Firm/GetUserClientFirms` |
| Usunięcie zaznaczonych | PUT | `/api/Firm/DeleteFirms` (query string IDs) |

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| OP-E05-01 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Klient tworzony w kontekście UserFirm zalogowanego użytkownika — klienci tylko bieżącej firmy |
| OP-E05-03 | [ALG-10 Izolacja danych UserFirm](../../../03_algorytmy/dedykowane/izolacja_danych_userfirm.md) | Usunięcie batch działa tylko na klientach należących do UserFirm aktualnie zalogowanego użytkownika |
| FILTR-E05-01 | — (filtr kliencki MatTable) | Filtrowanie po stronie klienta — brak algorytmu backendowego |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`clients.component.ts`](../../../../InvoiceJetUI/src/app/components/firm/clients/clients.component.ts) |
| Szablon HTML | [`clients.component.html`](../../../../InvoiceJetUI/src/app/components/firm/clients/clients.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| KA-01 | `console.log(firms)` aktywny w metodzie `getUserFirms()` w kodzie produkcyjnym |
| KA-02 | Brak komunikatów sukcesu/błędu dla użytkownika po operacjach (dodaj/edytuj/usuń) |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
