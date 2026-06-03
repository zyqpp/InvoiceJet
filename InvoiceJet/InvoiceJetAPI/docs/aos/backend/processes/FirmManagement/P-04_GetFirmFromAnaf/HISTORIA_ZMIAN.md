# GetFirmFromAnaf — Historia zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| `1.0` | 2026-05-30 | Agent AI | Utworzono pełną dokumentację procesu wg frameworku AOS Backend. Zidentyfikowano 7 uwag wymagających weryfikacji: (1) ANAF HTTP 200 z pustą tablicą `found` → klient dostaje 200 zamiast 404; (2) `catch (Exception)` maskuje błędy sieciowe; (3) `new HttpClient()` bez IHttpClientFactory → ryzyko socket exhaustion; (4) brak explicite timeout na HttpClient; (5) mieszane serializery JSON (System.Text.Json + Newtonsoft); (6) niezgodność Unicode `ŞOS.` (U+015E); (7) `regCom == null` blokuje ustawienie Name i Cui. |
