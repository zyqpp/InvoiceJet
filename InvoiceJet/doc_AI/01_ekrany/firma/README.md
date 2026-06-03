# firma — Zarządzanie danymi firmy

Grupa ekranów odpowiadających za zarządzanie danymi związanymi z firmą użytkownika: dane własnej firmy (wystawiającego faktury), lista firm klientów oraz konta bankowe. Wszystkie ekrany chronione przez AuthGuard (rola: User).

## Drzewo zawartości

```
firma/
├── README.md                            ← Ten plik
├── dane_firmy/
│   ├── README.md                        ← Opis sekcji dane firmy
│   └── ekran.md                         ← FirmDetailsComponent
├── klienci/
│   ├── README.md                        ← Opis sekcji klienci
│   ├── ekran.md                         ← ClientsComponent
│   └── dialog_dodaj_klienta/
│       └── modal.md                     ← AddEditClientDialogComponent
└── konta_bankowe/
    ├── README.md                        ← Opis sekcji konta bankowe
    ├── ekran.md                         ← BankAccountsComponent
    └── dialog_dodaj_konto/
        └── modal.md                     ← AddOrEditBankAccountDialogComponent
```

## Kluczowe dokumenty

- `dane_firmy/ekran.md` — formularz danych własnej firmy (ANAF, edycja, dodawanie)
- `klienci/ekran.md` — lista klientów z CRUD przez dialog
- `klienci/dialog_dodaj_klienta/modal.md` — modal dodawania/edycji klienta
- `konta_bankowe/ekran.md` — lista kont bankowych z CRUD przez dialog
- `konta_bankowe/dialog_dodaj_konto/modal.md` — modal dodawania/edycji konta bankowego

## Powiązane katalogi

- `../dashboard/` — ekran startowy (sidebar: Dane firmy, Klienci, Konta bankowe)
- `../faktury/dodaj_edytuj_fakture/` — klienci i konta bankowe używane w formularzach dokumentów

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
