# dane_firmy — Dane własnej firmy

Ekran zarządzania danymi własnej firmy użytkownika (wystawiającego faktury). Umożliwia dodanie nowej firmy (przy pierwszym wejściu) lub edycję istniejących danych. Obsługuje autouzupełnianie danych z rejestru ANAF (rumuński rejestr firm) na podstawie numeru CUI.

## Drzewo zawartości

```
dane_firmy/
├── README.md    ← Ten plik
└── ekran.md     ← FirmDetailsComponent — formularz danych firmy
```

## Kluczowe dokumenty

- `ekran.md` — pełna dokumentacja ekranu: pola, wywołania API, anomalie (w tym błąd `isFormChanged()`)

## Powiązane katalogi

- `../` — katalog grupy firma
- `../../dashboard/` — ekran startowy

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
