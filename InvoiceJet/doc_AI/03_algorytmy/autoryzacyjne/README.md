# autoryzacyjne — Algorytmy autoryzacyjne

Algorytmy odpowiedzialne za tworzenie i weryfikację tokenów JWT oraz zarządzanie sesją użytkownika po stronie frontendu i backendu.

## Drzewo zawartości

```
autoryzacyjne/
├── README.md
├── weryfikacja_tokenu_jwt.md    ← pipeline JWT (Program.cs + JwtInterceptor + AuthGuard)
└── tworzenie_tokenu_jwt.md      ← AuthService.CreateToken()
```

## Kluczowe dokumenty

- [`weryfikacja_tokenu_jwt.md`](weryfikacja_tokenu_jwt.md) — pełny cykl życia tokenu JWT; anomalie bezpieczeństwa (brak refresh token, localStorage, ValidateIssuer=false).
- [`tworzenie_tokenu_jwt.md`](tworzenie_tokenu_jwt.md) — metoda `CreateToken()`, claims tokenu, parametry podpisywania.

## Powiązane katalogi

- [`../walidacji/`](../walidacji/) — walidacja hasła przed wystawieniem tokenu
- [`../../02_procesy/autentykacja/`](../../02_procesy/autentykacja/) — procesy logowania i rejestracji

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
