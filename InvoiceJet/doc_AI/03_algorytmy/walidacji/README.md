# walidacji — Algorytmy walidacyjne

Algorytmy odpowiedzialne za weryfikację poprawności danych wejściowych przed ich przetworzeniem lub zapisem do bazy danych.

## Drzewo zawartości

```
walidacji/
├── README.md
└── walidacja_hasla.md           ← regex + BCrypt (AuthService)
```

## Kluczowe dokumenty

- [`walidacja_hasla.md`](walidacja_hasla.md) — walidacja siły hasła (regex) i haszowanie BCrypt przy rejestracji; lista dozwolonych znaków specjalnych.

## Powiązane katalogi

- [`../autoryzacyjne/`](../autoryzacyjne/) — algorytmy tworzenia i weryfikacji tokenu JWT
- [`../../02_procesy/autentykacja/`](../../02_procesy/autentykacja/) — procesy rejestracji i logowania

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
