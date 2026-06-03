# login — Ekran logowania

Ekran logowania do aplikacji InvoiceJet. Publicznie dostępny — nie wymaga autoryzacji. Jest punktem wejściowym dla użytkowników powracających oraz celem przekierowania po wylogowaniu lub wygaśnięciu sesji JWT.

## Drzewo zawartości

```
login/
├── README.md    ← Ten plik
└── ekran.md     ← LoginComponent — formularz logowania (email + hasło)
```

## Kluczowe dokumenty

- `ekran.md` — pełna dokumentacja ekranu logowania: pola, przepływ, wywołania API

## Powiązane katalogi

- `../register/` — ekran rejestracji (link „Zarejestruj się")
- `../dashboard/` — cel nawigacji po poprawnym zalogowaniu
- `../00_wspolne/modale_wspolne/token_expired_dialog/` — przekierowuje na `/login` po wygaśnięciu tokenu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
