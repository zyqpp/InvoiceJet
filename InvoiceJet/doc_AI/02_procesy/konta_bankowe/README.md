# konta_bankowe

Procesy techniczne związane z zarządzaniem kontami bankowymi firmy w systemie InvoiceJet.

## Drzewo zawartości

```
konta_bankowe/
├── README.md                    # ten plik
├── pobierz_konta/
│   └── proces.md                # PROC-GetAllBankAccounts — lista kont bankowych firmy
├── dodaj_konto/
│   └── proces.md                # PROC-AddBankAccount — dodanie nowego konta
├── edytuj_konto/
│   └── proces.md                # PROC-EditBankAccount — edycja danych konta
└── usun_konta/
    └── proces.md                # PROC-DeleteBankAccounts — usunięcie kont (UWAGA: CASCADE DELETE dokumentów!)
```

## Kluczowe dokumenty

- `usun_konta/proces.md` — **KRYTYCZNA ANOMALIA BA-01:** usunięcie konta kasuje kaskadowo wszystkie powiązane dokumenty!

## Powiązane katalogi

- `../../04_api_i_integracje/01_api_frontend/bank_account/` — dokumentacja endpointów API kont bankowych
- `../../01_ekrany/firma/konta_bankowe/` — ekran zarządzania kontami bankowymi
- `../../05_model_danych/01_db/dbo/dbo.BankAccount.md` — tabela BankAccount

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja — struktura podfolderów konta_bankowe (z P-05). |
