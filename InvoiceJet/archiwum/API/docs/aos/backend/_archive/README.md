# Archiwum dokumentacji backendowej AOS

**Status:** Materiał archiwalny — **nie jest źródłem prawdy**.
**Data archiwizacji:** 2026-05-29

---

## Co tu jest

- `processes/` — 19 procesów (`P-01` … `P-19`) wytworzonych na **poprzedniej wersji frameworka** (chude szablony, brak Definicji Ukończenia, brak katalogu walidacji, brak schodzenia do kolumn).
- `REJESTR_PROCESOW_BACKEND.md` — poprzedni rejestr odpowiadający powyższym procesom.

## Dlaczego zostały zarchiwizowane

Nowy framework (`docs/BackendAgentAI/` + `docs/aos/backend/templates/`) wprowadza:

- 9 wymiarów opisu z obowiązkową Definicją Ukończenia per plik,
- zasadę kotwiczenia `Plik.cs › Klasa.Metoda` + krótki cytat kodu,
- katalog walidacji `WAL-XX` w pliku `05`,
- schodzenie do poziomu kolumn w pliku `04`,
- realne dane testowe (`DT-XX`) zamiast formalnych scenariuszy,
- katalogi przekrojowe (`KATALOG_API`, `SLOWNIK_DANYCH`, `KATALOG_WYJATKOW`, …).

Żaden z archiwalnych procesów nie spełnia nowego kontraktu wyjścia (w szczególności `P-01`, mimo że był najbogatszy w starej wersji, **nie jest wzorcem nowego frameworka**).

## Czy korzystać przy re-dokumentacji?

- **Tak**, jako materiał pomocniczy: szybkie rozpoznanie procesu, identyfikacja endpointów, dotychczasowe diagramy mermaid.
- **Nie** jako wzorzec stylu i głębi — wzorzec ma powstać dopiero z pierwszych procesów dokumentowanych już wg nowych szablonów.
- Każde twierdzenie z archiwum musi być potwierdzone wobec aktualnego kodu (zasada `ZB.1`).

## Co dalej

Re-dokumentacja procesów powstanie pod `docs/aos/backend/processes/` (od zera) oraz uzupełni katalogi przekrojowe pod `docs/aos/backend/` na bazie nowych szablonów z `docs/aos/backend/templates/`.

Archiwum można usunąć dopiero po pełnym pokryciu wszystkich procesów w nowym formacie.
