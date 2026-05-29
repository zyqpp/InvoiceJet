# A-00: AppShell — Śledzenie źródeł

## A. Źródła Frontend (E-00_AppShell)

Wszystkie elementy A-00 są potwierdzone w dokumentacji frontendu:

| Dokument Frontend | Zakres użytku | Status |
|---|---|---|
| **E-00 / 00_METADANE.md** | Komponenty: AppComponent, NavbarComponent, SidebarComponent; Serwisy: AuthService, SidebarService, Router; Guardy: AuthGuard; Interceptory: AuthInterceptor, ErrorInterceptor | ✓ Potwierdzone |
| **E-00 / 01_PRZEGLĄD.md** | Layout powłoki (navbar, sidebar, router-outlet); Menu główne (Dashboard, Documents, Inventory, Settings); Scenariusz główny (AuthGuard → render) | ✓ Potwierdzone |
| **E-00 / 02_DANE_I_OPERACJE.md** | Pola navbar (przycisk menu, logo, Login/Register, profil); Menu profilu (imię, email, Dark Mode, Logout); Pola sidebar (Search, Clear, Mat-Tree); Operacje (toggle menu, logout, nawigacja, toggle dark mode) | ✓ Potwierdzone |
| **E-00 / 03_LOGIKA_BIZNESOWA.md** | Logika inicjalizacji (Angular boot, Router events); Routing ekranów (chronionych/publicznych); Menu boczne (SidebarService); Filtrowanie drzewa; Profil użytkownika (dekodowanie tokenu); Wylogowanie; Tryb ciemny; Interceptory | ✓ Potwierdzone |
| **E-00 / 04_SCENARIUSZE_TESTOWE.md** | 8 scenariuszy: render powłoki, bez menu, toggle menu, filtrowanie, active-link, logout, dark mode, brak dostępu | ✓ Potwierdzone |
| **E-00 / HISTORIA_ZMIAN.md** | Wersjonowanie dokumentu E-00 | ✓ Potwierdzone |

**Podsumowanie:** Wszystkie elementy A-00 (metadane, przegląd, pola, operacje, walidacje, scenariusze) są w pełni opisane w E-00_AppShell.

---

## B. Źródła Backend (P-XX)

AppShell **nie ma dedykowanego procesu backend**, ponieważ jest to czysta warstwa UI i routing bez komunikacji API.

| Proces Backend | Powiązanie z A-00 | Status |
|---|---|---|
| P-01: IssueNewInvoice | — | Brak powiązania (to jest proces dla A-05) |
| P-02: AddFirm | — | Brak powiązania (A-08) |
| P-03: RegisterUser | Rejestracja (wchodzi z A-12: Register) | Pośrednie: A-12 → AuthToken → A-00 |
| P-04: LoginUser | Logowanie (otrzymanie tokenu) | Pośrednie: A-11 → AuthToken → A-00 |
| P-05: GetFirmFromAnaf | — | Brak powiązania |
| P-06: EditFirm | — | Brak powiązania |
| P-07: GetUserActiveFirm | — | Brak powiązania |
| P-08: ManageClientFirms | — | Brak powiązania |
| P-09: ManageProducts | — | Brak powiązania |
| P-10: ManageBankAccounts | — | Brak powiązania |
| P-11: ManageDocumentSeries | — | Brak powiązania |

**Wniosek:** AppShell nie konsumuje żadnych procesów backend bezpośrednio. Token JWT (pochodzący z P-03 lub P-04) jest jedynym "produktem" backendu używanym przez A-00.

---

## C. Powiązania między warstwami A-00 → E-00

| Element A-00 | Źródło E-00 | Typ mapowania |
|---|---|---|
| Komponenty (App, Navbar, Sidebar) | E-00 / 00_METADANE.md | 1:1 mapowanie |
| Serwisy (AuthService, SidebarService) | E-00 / 00_METADANE.md | 1:1 mapowanie |
| Guardy (AuthGuard) | E-00 / 00_METADANE.md | 1:1 mapowanie |
| Interceptory (Auth, Error) | E-00 / 00_METADANE.md | 1:1 mapowanie |
| Layout powłoki | E-00 / 01_PRZEGLĄD.md | 1:1 mapowanie |
| Menu główne (Dashboard, Documents itp.) | E-00 / 01_PRZEGLĄD.md | 1:1 mapowanie |
| Elementy navbar | E-00 / 02_DANE_I_OPERACJE.md | 1:1 mapowanie (5 elementów) |
| Menu profilu | E-00 / 02_DANE_I_OPERACJE.md | 1:1 mapowanie (4 elementy) |
| Elementy sidebar | E-00 / 02_DANE_I_OPERACJE.md | 1:1 mapowanie (3 elementy + mat-tree) |
| Operacje | E-00 / 02_DANE_I_OPERACJE.md + 03_LOGIKA_BIZNESOWA.md | 1:1 mapowanie (8 operacji) |
| Logika biznesowa | E-00 / 03_LOGIKA_BIZNESOWA.md | 1:1 mapowanie (6 przepływów logiki) |
| Scenariusze testowe | E-00 / 04_SCENARIUSZE_TESTOWE.md | 1:1 mapowanie (8 scenariuszy) |

---

## D. Luki i niejasności

| Problem | Status | Notatka |
|---|---|---|
| **Brak backendu dla AppShell** | [WYMAGA WERYFIKACJI] | AppShell nie ma procesu P-XX. Czy guardy/interceptory powinny być udokumentowane jako osobny proces? |
| **Tryb ciemny bez utrwalenia** | [WYMAGA WERYFIKACJI] | Dokumentacja E-00 mówi, że stan nie jest zapisywany w localStorage. Czy to zamierzone? |
| **Token JWT bez weryfikacji** | [WYMAGA WERYFIKACJI] | Dane użytkownika są dekodowane z tokenu bez weryfikacji na backendzie. Czy to bezpiecze? |
| **Refresh token** | [WYMAGA WERYFIKACJI] | Czy backend implementuje refresh token do odnawiania sesji? E-00 mówi, że przy 401 token jest usuwany. |
| **Role użytkownika** | [WYMAGA WERYFIKACJI] | AuthGuard sprawdza tylko isLoggedIn(). Czy istnieją rola-based access controls (admin, user)? |
| **Logout bez API** | [WYMAGA WERYFIKACJI] | Logout usuwa token lokalnie bez komunikacji z backendem. Czy sesja na backendzie jest invalidowana? |
| **CSRF protection** | [WYMAGA WERYFIKACJI] | Czy aplikacja ma mechanizmy ochrony przed CSRF? |
| **XSS protection** | [WYMAGA WERYFIKACJI] | Token przechowywany w localStorage (podatne na XSS). Czy są sanitizacja danych wejściowych? |

---

## E. Powiązania E-00 z pozostałymi przepływami

AppShell (A-00) jest **fundamentem** dla wszystkich ekranów chronionych (A-01 do A-10):

| Przepływ | Powiązanie z A-00 |
|---|---|
| **A-01: Dashboard** | Renderowany w `<router-outlet>` po AuthGuard |
| **A-02: Invoices** | Dostępny przez menu "Documents → Invoices", router: `/documents/invoices` |
| **A-03: Invoice Proformas** | Dostępny przez menu "Documents → Invoice Proformas" |
| **A-04: Invoice Stornos** | Dostępny przez menu "Documents → Invoice Stornos" |
| **A-05: IssueNewInvoice** | Operacja wewnątrz A-02 (dodawanie faktury) |
| **A-06: Clients** | Dostępny przez menu "Inventory → Clients" |
| **A-07: Products** | Dostępny przez menu "Inventory → Products" |
| **A-08: Firm Details** | Dostępny przez menu "Settings → Firm Details" |
| **A-09: Bank Accounts** | Dostępny przez menu "Settings → Bank Accounts" |
| **A-10: Document Series** | Dostępny przez menu "Settings → Document Series" |
| **A-11: Login** | Ekran publiczny, AccessGuard na `<app-navbar>` pokazuje Login link |
| **A-12: Register** | Ekran publiczny, AccessGuard na `<app-navbar>` pokazuje Register link |

---

## F. Mapa zależy od czego A-00 zależy

```
A-00: AppShell
│
├─→ E-00: AppShell (dokumentacja frontend) ✓ Potwierdzone
│   ├─ 00_METADANE.md (komponenty, serwisy, guardy)
│   ├─ 01_PRZEGLĄD.md (layout, routing)
│   ├─ 02_DANE_I_OPERACJE.md (elementy UI, operacje)
│   ├─ 03_LOGIKA_BIZNESOWA.md (przepływy, inicjalizacja)
│   └─ 04_SCENARIUSZE_TESTOWE.md (testy E2E)
│
├─→ P-XX: Backend (procesów) ✗ Brak dedykowanego
│   └─ Pośrednie: P-03/P-04 (token JWT) → AuthService
│
├─→ A-01 do A-12: Pozostałe przepływy (zależy od nich)
│   └─ A-00 jest fundamentem dla wszystkich (navbar, sidebar, routing)
│
└─→ Baza danych: ✗ Nie mapuje
    └─ Token JWT pochodzący z backendu, ale A-00 go nie odczytuje
```

---

## G. Kontrola jakości dokumentu A-00

### ✓ Potwierdzone
- [x] Wszystkie metadane pochodzą z E-00_AppShell
- [x] Wszystkie operacje są opisane w E-00_AppShell
- [x] Wszystkie scenariusze testowe pochodzą z E-00_AppShell
- [x] Walidacje i bezpieczeństwo opisane na podstawie kodu Angular

### ⚠️ Wymaga weryfikacji
- [ ] Czy guardy/interceptory powinny mieć własny proces backend (P-00)?
- [ ] Czy dane w tokenie JWT są bezpiecze (nie zawierają haseł)?
- [ ] Czy istnieją rola-based access controls?
- [ ] Czy aplikacja jest chroniona przed XSS/CSRF?
- [ ] Czy dark mode powinien być utrwalony w localStorage?

### [BRAK MAPOWANIA DO BAZY]
- AppShell nie mapuje do żadnych tabel bazy danych
- Wszystkie operacje są na poziomie UI (localStorage, komponenty, serwisy)

---

## H. Historia linków do źródeł

| Data | Zmiana | Status |
|---|---|---|
| 2026-05-29 | Początkowe mapowanie do E-00_AppShell | ✓ Potwierdzone |
| — | Powiązania do P-XX | ✗ Brak (AppShell bez backendu) |
