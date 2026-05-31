# klienci — Lista i zarządzanie klientami

Ekran i modal zarządzania listą firm klientów użytkownika. Klienci to firmy, na które wystawiane są dokumenty (faktury, proformy, storna). CRUD odbywa się przez dialog Angular Material.

## Drzewo zawartości

```
klienci/
├── README.md                        ← Ten plik
├── ekran.md                         ← ClientsComponent — lista klientów
└── dialog_dodaj_klienta/
    └── modal.md                     ← AddEditClientDialogComponent — dodaj/edytuj klienta
```

## Kluczowe dokumenty

- `ekran.md` — lista klientów: tabela, CRUD, wywołania API
- `dialog_dodaj_klienta/modal.md` — modal formularza klienta (tryb dodaj + tryb edytuj); obsługuje ANAF autouzupełnianie

## Powiązane katalogi

- `../` — katalog grupy firma
- `../../faktury/dodaj_edytuj_fakture/` — klienci wybierani w formularzu dokumentu (autocomplete)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Pierwsza wersja. |
