# EditFirm — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono pełną dokumentację procesu wg frameworku AOS Backend. Zidentyfikowano 6 uwag wymagających weryfikacji: (1) `throw new Exception("Firm not found.")` zamiast wyjątku domenowego → `500` zamiast `404`; (2) brak weryfikacji własności firmy — każdy użytkownik może edytować dowolną firmę po Id; (3) brak jawnej transakcji między `CompleteAsync()` #1 i #2; (4) `ManageUserFirmRelation` może tworzyć duplikaty `UserFirm` przy braku unikalnego indeksu `(UserId, FirmId)`; (5) `FirmDto.RegCom` nullable vs NOT NULL w DB; (6) odpowiedź to echo żądania, nie odczyt z DB po zapisie. |

---

*Katalogi do aktualizacji po tym procesie:*
- `KATALOG_API.md` — dodać `API-05` (plik nie istnieje jeszcze)
- `KATALOG_WYJATKOW.md` — odnotować brak klasy `FirmNotFoundException` i mapowanie `Exception("Firm not found.")` → `500` (plik nie istnieje jeszcze)
