# konta_bankowe — Lista i zarządzanie kontami bankowymi

Ekran i modal zarządzania kontami bankowymi własnej firmy użytkownika. Konta bankowe przypisywane są do dokumentów (faktury, proformy, storna) jako dane do przelewu. CRUD odbywa się przez dialog Angular Material.

## Drzewo zawartości

```
konta_bankowe/
├── README.md                        ← Ten plik
├── ekran.md                         ← BankAccountsComponent — lista kont bankowych
└── dialog_dodaj_konto/
    └── modal.md                     ← AddOrEditBankAccountDialogComponent — dodaj/edytuj konto
```

## Kluczowe dokumenty

- `ekran.md` — lista kont bankowych: tabela, CRUD, wywołania API
- `dialog_dodaj_konto/modal.md` — modal formularza konta bankowego (tryb dodaj + tryb edytuj)

## Powiązane katalogi

- `../` — katalog grupy firma
- `../../faktury/dodaj_edytuj_fakture/` — konta bankowe wybierane w formularzu dokumentu

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
