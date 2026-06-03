# Audyt bezpieczeństwa — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Zakres

Analiza bezpieczeństwa oparta na inspekcji kodu źródłowego — bez testów penetracyjnych.

---

## Uwierzytelnienie i autoryzacja

| # | Obszar | Ocena | Opis |
|---|---|---|---|
| B-01 | JWT Signing | ✅ | HmacSha512 — silny algorytm |
| B-02 | Hasło hashing | ✅ | BCrypt z work factor 11 |
| B-03 | Czas sesji | ⚠️ | 10 minut — zbyt krótki; brak refresh token |
| B-04 | Token storage | ❌ | localStorage — podatny na XSS |
| B-05 | Server-side invalidation | ❌ | Brak — wylogowanie tylko lokalne |
| B-06 | ValidateIssuer | ⚠️ | false — słabsza weryfikacja |
| B-07 | ValidateAudience | ⚠️ | false — słabsza weryfikacja |
| B-08 | ClockSkew | ✅ | TimeSpan.Zero — dokładne wygaśnięcie |

---

## Izolacja danych

| # | Obszar | Ocena | Opis |
|---|---|---|---|
| D-01 | Izolacja przez UserFirm | ✅ | Każdy zasób powiązany z UserFirmId |
| D-02 | Weryfikacja własności (Edit) | ❌ | Brak sprawdzenia czy zasób należy do użytkownika przy edycji/usunięciu |
| D-03 | Weryfikacja własności (Get) | ✅ | GetAll filtruje przez UserFirmId |
| D-04 | IDOR (Insecure Direct Object Reference) | ❌ | Możliwe — znając ID można edytować cudzy zasób |

---

## Bezpieczeństwo API

| # | Obszar | Ocena | Opis |
|---|---|---|---|
| A-01 | CORS | ❌ | Tylko localhost:4200; brak produkcyjnego origina |
| A-02 | HTTPS | ✅ | Wymagane na Azure |
| A-03 | Rate limiting | ❌ | Brak — możliwy brute-force login |
| A-04 | Input validation | ⚠️ | Walidacja hasła przez regex; brak innych walidacji w DTO |
| A-05 | SQL Injection | ✅ | EF Core parametryzuje zapytania |
| A-06 | Error disclosure | ❌ | catch-all 500 zwraca `ex.Message` w produkcji |
| A-07 | Swagger w produkcji | ⚠️ | Nieznany — zależy od konfiguracji |

---

## Integralność danych

| # | Obszar | Ocena | Opis |
|---|---|---|---|
| I-01 | CASCADE DELETE | ❌ | Usunięcie konta bankowego usuwa faktury |
| I-02 | Numeracja dokumentów | ❌ | Race condition — możliwe duplikaty |
| I-03 | Transakcje | ⚠️ | TransformToStorno bez transakcji; dwa CompleteAsync w AddDocument |
| I-04 | Soft delete | ❌ | Brak — dane bezpowrotnie usuwane |

---

## Podsumowanie ocen

| Kategoria | ✅ OK | ⚠️ Uwaga | ❌ Problem |
|---|---|---|---|
| Uwierzytelnienie | 3 | 3 | 2 |
| Izolacja danych | 2 | 0 | 2 |
| Bezpieczeństwo API | 2 | 2 | 3 |
| Integralność | 0 | 1 | 3 |
| **ŁĄCZNIE** | **7** | **6** | **10** |

## Rekomendacje priorytetowe

1. **Napraw CASCADE DELETE** (LT-01) — krytyczny risk utraty danych
2. **Wdróż refresh token** (LT-05) — poprawa UX i bezpieczeństwa
3. **Przenieś JWT do HttpOnly cookie** (LT-08) — eliminacja XSS wektora
4. **Dodaj weryfikację własności zasobów** (LT-XX) — eliminacja IDOR
5. **Dodaj rate limiting** — ochrona przed brute-force

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny — audyt na podstawie inspekcji kodu. |
