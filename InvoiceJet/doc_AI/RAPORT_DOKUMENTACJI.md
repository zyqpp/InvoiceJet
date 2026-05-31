# Raport stanu dokumentacji — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Data raportu | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Status | Wersja 1.0 — Dokumentacja wstępna kompletna |
| Łączna liczba plików | **177 pliki .md** |

---

## Podsumowanie wykonanej pracy

### ✅ Ukończone sekcje

| Sekcja | Pliki | Status |
|---|---|---|
| `_mapowania/` — Inwentaryzacje | 6 | ✅ KOMPLETNE |
| `00_meta/` — Metadokumenty | 9 | ✅ KOMPLETNE |
| `01_ekrany/` — Ekrany i komponenty | 24 | ✅ KOMPLETNE |
| `02_procesy/` — Procesy techniczne | 15 | ✅ KOMPLETNE |
| `03_algorytmy/` — Algorytmy | 10 | ✅ KOMPLETNE |
| `04_api_i_integracje/01_api_frontend/` — Endpointy | 31 | ✅ KOMPLETNE |
| `04_api_i_integracje/02_anaf/` — ANAF | 1 | ✅ KOMPLETNE |
| `04_api_i_integracje/03_db_seeder/` — DbSeeder | 1 | ✅ KOMPLETNE |
| `05_model_danych/01_db/` — Schemat DB | 12 | ✅ KOMPLETNE |
| `05_model_danych/02_linq/` — Zapytania LINQ | 5 | ✅ KOMPLETNE |
| `05_model_danych/03_dto/` — DTO | 14 | ✅ KOMPLETNE |
| `05_model_danych/04_automapper/` — AutoMapper | 7 | ✅ KOMPLETNE |
| `06_role_i_uprawnienia/` — Role | 4 | ✅ KOMPLETNE |
| `07_use_case/` — Use Cases | 4 | ✅ KOMPLETNE |
| `08_model_biznesowy/` — Model biznesowy | 1 | ✅ KOMPLETNE |
| `09_procesy_biznesowe/` — BPMN | 2 | ✅ KOMPLETNE |
| `10_testy/` — Testy | 1 | ✅ KOMPLETNE |
| `_slowniki/` — Słowniki | 2 | ✅ KOMPLETNE |
| `INDEX.md` | 1 | ✅ KOMPLETNE |

**Łącznie:** **177 pliki dokumentacji** (zweryfikowane: `Get-ChildItem -Recurse -Filter "*.md" | Count`)

---

## Kluczowe odkrycia

### 🔴 4 Anomalie krytyczne wymagające natychmiastowej uwagi

| ID | Anomalia | Ryzyko |
|---|---|---|
| A-KRIT-01 | CASCADE DELETE konta bankowego usuwa faktury | **Utrata danych** |
| A-KRIT-02 | TransformToStorno — CompleteAsync() w pętli | **Niespójna konwersja** |
| A-KRIT-03 | Race condition na numerach dokumentów | **Duplikaty numerów** |
| A-KRIT-04 | GenerateInvoicePdf hardkoduje InvoiceDocument | **Błędne PDF** |

### 💡 Najważniejsze mechanizmy techniczne

1. **JWT 10 minut + HmacSha512** — bardzo krótka sesja, brak refresh token
2. **Izolacja danych przez UserFirm** — każdy zasób powiązany z UserFirmId z JWT
3. **BCrypt haszowanie** — work factor 11, regex walidacja hasła (tylko 7 znaków specjalnych)
4. **Clean Architecture** — 4 warstwy: Presentation → Application → Domain ← Infrastructure
5. **Unit of Work** — `CompleteAsync()` = `SaveChangesAsync()`
6. **BaseInvoiceComponent** — abstrakcja dla 3 typów formularzy dokumentów
7. **ANAF integracja** — POST z `[{cui, data}]`, brak cache/timeout

### 📊 Statystyki systemu

| Komponent | Liczba |
|---|---|
| Tabele DB | 10 |
| Endpointy API | ~30 |
| Ekrany Angular | 14 |
| Dialogi | 6 |
| DTOs | 14 |
| AutoMapper profiles | 7 |
| Procesy backendowe | 15 |
| Algorytmy | 10 |
| Anomalie zidentyfikowane | 28 |
| Dług techniczny (LT) | 14 pozycji |

---

## Co zostało pominięte / wymaga uzupełnienia

| Obszar | Opis | Priorytet |
|---|---|---|
| Migracje EF Core | Szczegółowa historia migracji | NISKI |
| Testy jednostkowe | Brak (nie istnieją w projekcie) | WYSOKI (do stworzenia) |
| Dokumentacja Swagger | Brak notacji XML w kontrolerach | NISKI |
| Więcej Use Cases | UC-05 do UC-15 (CRUD scenariusze) | ŚREDNI |
| Pełne BPMN | Więcej procesów biznesowych | NISKI |
| Performance benchmarks | Brak testów wydajnościowych | NISKI |

---

## Jak korzystać z tej dokumentacji

1. **Nowy deweloper:** Zacznij od `00_meta/01_o_projekcie.md` → `08_quickstart_dev.md`
2. **Naprawianie buga:** Znajdź w `_slowniki/slownik_anomalii.md` → `02_procesy/P-XX.md`
3. **Dodawanie funkcji:** `03_algorytmy/` → `02_procesy/` → `01_ekrany/`
4. **Audyt bezpieczeństwa:** `06_role_i_uprawnienia/audyt_bezpieczenstwa.md`
5. **Planowanie refactoru:** `00_meta/07_dług_techniczny.md`
6. **Nawigacja ogólna:** `INDEX.md`

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza kompletna wersja dokumentacji systemu InvoiceJet. |
