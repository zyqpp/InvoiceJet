# A-00: AppShell — Historia zmian

## Wersjonowanie dokumentu

| Wersja | Data | Autor | Model AI | Opis zmian | Status |
|---|---|---|---|---|---|
| 1.0 | 2026-05-29 | Agent AI: Golden Zebra | Claude Haiku 4.5 | Dokument inicjalny. Przygotowanie 9 dokumentów (00-07 + HISTORIA): Metadane, Przegląd end-to-end, Mapa pól UI, Operacje, Gridy (N/D), Walidacje/bezpieczeństwo, Scenariusze testowe, Śledzenie źródeł. Wszystkie elementy mapowane z dokumentacji frontendu E-00_AppShell. Brak dedykowanego backendu (operacje [TYLKO FRONTEND]). | ✓ Stworzony |

---

## Notatki do implementacji

### 2026-05-29 — Inicjalizacja
- Przepływ A-00 wybrany jako pierwszy do dokumentacji (AppShell to fundament aplikacji)
- Źródła: E-00_AppShell (kompletna dokumentacja frontendu), brak P-XX (AppShell to UI)
- Struktura: 9 plików zgodnie z szablonem TEMPLATE_*.md
- Markery: `[TYLKO FRONTEND]` dla wszystkich operacji (brak API), `[WYMAGA WERYFIKACJI]` dla niejasności

### Decyzje projektu
1. **AppShell bez backendu**: Wszystkie operacje (toggle menu, logout, nawigacja) są frontendowe. Nie ma dedykowanego procesu P-00.
2. **Token JWT z backendu**: Używany przez AuthService, ale pochodzący z P-03 (Register) lub P-04 (Login).
3. **Gridy nie dotyczą**: Dokument 04 jest pusty — AppShell nie ma list/gridów danych.
4. **Bezpieczeństwo oznaczone**: localStorage (XSS risk), brak refresh tokenu (WYMAGA WERYFIKACJI), rola-based access (WYMAGA WERYFIKACJI).

---

## Następne dokumenty do przygotowania

| Przepływ | Status | Kolejność |
|---|---|---|
| A-00: AppShell | ✓ **STWORZONY** | 1 ✓ |
| A-01: Dashboard | ⏳ Do przygotowania | 2 |
| A-02: Invoices (lista, przeglądanie) | ⏳ Do przygotowania | 3 |
| A-03: Invoice Proformas | ⏳ Do przygotowania | 4 |
| A-04: Invoice Stornos | ⏳ Do przygotowania | 5 |
| A-06: Clients | ⏳ Do przygotowania | 6 |
| A-07: Products | ⏳ Do przygotowania | 7 |
| A-08: Firm Details | ⏳ Do przygotowania | 8 |
| A-09: Bank Accounts | ⏳ Do przygotowania | 9 |
| A-10: Document Series | ⏳ Do przygotowania | 10 |
| A-11: Login | ⏳ Do przygotowania | 11 |
| A-12: Register | ⏳ Do przygotowania | 12 |

---

## Kontrola jakości

### Cele zrealizowane
- ✓ Wszystkie 9 dokumentów dla A-00 stworzonych
- ✓ Metadane linkują do 7 pozostałych dokumentów
- ✓ Każdy wiersz tabeli ma dowód (link do E-00_AppShell)
- ✓ Markery stosowane konsekwentnie (`[TYLKO FRONTEND]`, `[WYMAGA WERYFIKACJI]`, `N/D`)
- ✓ Scenariusze testowe mapują do selektorów CSS/Angular
- ✓ Bezpieczeństwo opisane warstwowo (Frontend, API, Backend)
- ✓ Luki i niejasności zaznaczone (XSS, refresh token, role-based access)

### Linki do weryfikacji
- [E-00_AppShell — Dokumentacja frontend](../../../InvoiceJet/InvoiceJetUI/docs/aos/frontend/E-00_AppShell/)
- [Szablony AOS](../../templates/)
- [Instrukcje agenta](../../FullStackAgentAI/)

---

## Zgłoszone problemy (niezależnie od A-00)

1. **localStorage + XSS** — Token przechowywany w localStorage (dostępny dla JS). Powinny być HttpOnly cookies.
2. **Brak refresh tokenu** — Przy 401 token usuwany bez możliwości odnawiania sesji.
3. **Dane z tokenu bez weryfikacji** — Imię/email dekodowane z JWT bez sprawdzenia na backendzie.
4. **Dark mode nieuprawdzony** — Stan nie utrwalany w localStorage (resetuje się po odświeżeniu).
5. **Brak role-based access** — AuthGuard sprawdza tylko isLoggedIn(), brak kontroli ról (admin, user).

Problemy wymagają weryfikacji z zespołem backendu/security.
