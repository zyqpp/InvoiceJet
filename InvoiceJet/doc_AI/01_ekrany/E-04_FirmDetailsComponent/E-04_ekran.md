# E-04 FirmDetailsComponent — Dane firmy

| Pole | Wartość |
|---|---|
| ID dokumentu | E-04 |
| Typ dokumentu | ekran |
| Wersja | 1.0 |
| Status | szkic |
| Autor (ostatnia modyfikacja) | Agent Claudiusz Sonte 4.6 |
| Data ostatniej modyfikacji | 2026-06-02 |

## Streszczenie

Ekran zarządzania danymi własnej firmy użytkownika (wystawiającego faktury). Przy pierwszym wejściu bez zarejestrowanej firmy wyświetlany jest formularz dodawania. Gdy firma już istnieje — formularz edycji z przyciskiem „Zapisz" aktywnym tylko przy wykrytych zmianach (uwaga: logika wykrywania zmian zawiera błąd — patrz anomalie). Obsługuje autouzupełnianie danych z rejestru ANAF na podstawie numeru CUI. Chroniony przez `AuthGuard` (rola: User).

---

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

---

## Wywołanie ekranu

| Atrybut | Wartość |
|---|---|
| Ścieżka URL | `/dashboard/firm-details` |
| Wymagana rola | User (AuthGuard JWT) |
| Punkty wejścia | Klik „Dane firmy" w Sidebar z [E-03 Dashboard](../E-03_DashboardComponent/E-03_ekran.md) |
| Komponent Angular | [`FirmDetailsComponent`](../../../../InvoiceJetUI/src/app/components/firm/firm-details/firm-details.component.ts) |
| Szablon HTML | [`firm-details.component.html`](../../../../InvoiceJetUI/src/app/components/firm/firm-details/firm-details.component.html) |

## Przejścia z ekranu

| Cel | Wywołane przez | Warunek | Uprawnienie |
|---|---|---|---|
| Ten sam ekran (odświeżenie danych) | [OP-E04-01](E-04_OP-01.md) sukces | Zapis zakończony powodzeniem | User |

---

## Filtry

Brak.

## Tabele i listy

Brak.

## Pola

| ID | Nazwa w UI | Wymagalność | Algorytm |
|---|---|---|---|
| POLE-E04-firmName | Nazwa firmy | wymagane | — |
| POLE-E04-cuiValue | CUI (NIP rumuński) | opcjonalne | [ALG-06 Integracja ANAF](../../../03_algorytmy/dedykowane/integracja_anaf.md) |
| POLE-E04-regCom | Numer rejestracji handlowej | opcjonalne | — |
| POLE-E04-address | Adres | opcjonalne | — |
| POLE-E04-county | Okręg | opcjonalne | — |
| POLE-E04-city | Miasto | opcjonalne | — |

## Operacje

| ID | Etykieta UI | Dokument |
|---|---|---|
| OP-E04-01 | Zapisz | [E-04_OP-01.md](E-04_OP-01.md) |
| OP-E04-02 | Ikona chmury ☁ (ANAF) | [E-04_OP-02.md](E-04_OP-02.md) |

## Modale

Brak.

## Scenariusze testowe

→ [E-04_TC.md](E-04_TC.md) — prereq JWT, prereq DB, selektory CSS, 4 scenariusze e2e

---

## Wywołania API — podsumowanie

| Akcja | Metoda | Endpoint |
|---|---|---|
| Załadowanie danych (ngOnInit) | GET | `/api/Firm/GetUserActiveFirm` |
| Zapis nowej firmy | POST | `/api/Firm/AddFirm` |
| Edycja istniejącej firmy | PUT | `/api/Firm/EditFirm` |
| Autouzupełnienie ANAF | GET | `/api/Firm/fromAnaf?cui={cuiValue}` |

---

## Powiązane algorytmy

| Pole / Operacja | Algorytm | Opis powiązania |
|---|---|---|
| POLE-E04-cuiValue | [ALG-06 Integracja ANAF](../../../03_algorytmy/dedykowane/integracja_anaf.md) | ANAF API: po CUI zwraca dane firmy do autouzupełnienia pól formularza |
| OP-E04-02 | [ALG-06 Integracja ANAF](../../../03_algorytmy/dedykowane/integracja_anaf.md) | Wywołanie GET ANAF API, autouzupełnienie pól: firmName, regCom, address, county, city |
| OP-E04-01 | [ALG-07 UserFirm](../../../03_algorytmy/dedykowane/zarzadzanie_relacja_userfirm.md) | UserFirm relation przy AddFirm — powiązanie firmy z zalogowanym użytkownikiem |

## Metody komponentu

| Metoda | Opis |
|---|---|
| `onSubmit()` | Sprawdza `currentUserFirm` → AddFirm (POST) lub EditFirm (PUT) |
| `onCloudIconClick()` | Wywołuje ANAF API i wypełnia pola formularza danymi firmy |
| `isFormChanged()` | Sprawdza czy formularz zmieniony — BŁĘDNA IMPLEMENTACJA (patrz anomalie) |
| `addNewClient()` | Niezaimplementowana — tylko `console.log("Add new client")` |

## Powiązania z kodem

| Artefakt | Ścieżka |
|---|---|
| Komponent TS | [`firm-details.component.ts`](../../../../InvoiceJetUI/src/app/components/firm/firm-details/firm-details.component.ts) |
| Szablon HTML | [`firm-details.component.html`](../../../../InvoiceJetUI/src/app/components/firm/firm-details/firm-details.component.html) |

## Wątpliwości i braki

| ID | Opis |
|---|---|
| FA-01 | `isFormChanged()` — błędna logika: `JSON.stringify(this.initialFormValues.value)` vs `JSON.stringify(this.initialFormValues)`. `initialFormValues` to plain object, więc `.value` to `undefined`. Przycisk „Zapisz" nigdy nie blokuje się przy braku zmian |
| FA-02 | `addNewClient()` niezaimplementowana — zawiera tylko `console.log("Add new client")` |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-06-02 | Agent Claudiusz Sonte 4.6 | Szkic — nowy format E-NN. |
