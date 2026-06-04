# AddFirm — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-29 | Agent AI | Utworzono pełną dokumentację procesu wg frameworku AOS Backend. Zidentyfikowano 5 uwag wymagających weryfikacji: brak transakcji obejmującej 3 CompleteAsync, isClient=true może stać się ActiveFirm, brak walidacji RegCom nullable vs NOT NULL, brak unikalnego indeksu CUI, null-forgiving na user po GetUserByIdAsync. |
