# [NAZWA PROCESU] — Logika aplikacyjna

## Przepływ wykonania

1. `[Controller].[Method]` odbiera żądanie.
2. Kontroler wywołuje `[Service].[Method]`.
3. Serwis wykonuje logikę procesu.
4. Serwis zapisuje zmiany przez `IUnitOfWork.CompleteAsync()`.
5. Kontroler zwraca odpowiedź API.

## Operacje na danych

| Krok | Operacja | Klasa |
|---|---|---|
| 1 | [Opis] | `[Class]` |
