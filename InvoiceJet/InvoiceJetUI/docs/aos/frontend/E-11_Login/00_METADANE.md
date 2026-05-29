# Login — Metadane

**Dokument:** Metadane ekranu  
**Aplikacja:** InvoiceJet  
**Moduł:** Auth  
**Klasyfikacja:** Publiczny  
**Data utworzenia:** 2026-05-29  
**Status:** Do weryfikacji technicznej

---

## Metadane ekranu

| Atrybut | Wartość |
|---|---|
| **Nazwa biznesowa ekranu** | Login |
| **Ścieżka URL** | `/login` |
| **Guard dostępu** | Brak |
| **Lazy loading** | Nie |
| **Plik komponentu** | `src/app/components/login/login.component.ts` |
| **Plik szablonu** | `src/app/components/login/login.component.html` |
| **Plik stylów** | `src/app/components/login/login.component.scss` |
| **Model formularza** | `src/app/models/ILoginUser.ts` |
| **Wersja dokumentu** | 1.0 |
| **Autor dokumentu** | Agent AI |
| **Ostatnia aktualizacja** | 2026-05-29 |

---

## Krótki opis

Ekran Login wyświetla publiczny formularz logowania użytkownika. Po poprawnym wysłaniu formularza frontend zapisuje token z odpowiedzi API w `localStorage` i nawiguje do `dashboard`.

---

## Powiązane dokumenty

| Dokument | Link |
|---|---|
| Przegląd ekranu | [01_PRZEGLĄD.md](01_PRZEGLĄD.md) |
| Dane i operacje | [02_DANE_I_OPERACJE.md](02_DANE_I_OPERACJE.md) |
| Logika frontendowa | [03_LOGIKA_BIZNESOWA.md](03_LOGIKA_BIZNESOWA.md) |
| Scenariusze testowe | [04_SCENARIUSZE_TESTOWE.md](04_SCENARIUSZE_TESTOWE.md) |
| Historia zmian | [HISTORIA_ZMIAN.md](HISTORIA_ZMIAN.md) |

---

## Szybkie odniesienia

### Główne serwisy

- `AuthService` — wywołuje logowanie przez `login(user)`.
- `Router` — nawiguje do `dashboard` po sukcesie.

### Modele danych

- `ILoginUser` — model danych wysyłanych z formularza logowania.

---

## Notatki

- Ekran jest publiczny i nie używa `AuthGuard`.
- Menu boczne aplikacji nie jest renderowane na trasie `/login`.
- Endpoint jest podany wyłącznie jako adres wywoływany przez `AuthService`.
