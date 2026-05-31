# 05_model_danych — Model danych

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
05_model_danych/
├── README.md
├── 01_db/
│   ├── README.md
│   ├── spis_schem_i_tabel.md            ← lista wszystkich 10 tabel
│   ├── erd_globalny.md                  ← diagram ERD całej bazy (Mermaid erDiagram)
│   └── dbo/
│       ├── erd_dbo.md                   ← ERD dla schematu dbo
│       ├── dbo.User.md
│       ├── dbo.Firm.md
│       ├── dbo.BankAccount.md
│       ├── dbo.UserFirm.md
│       ├── dbo.Product.md
│       ├── dbo.DocumentType.md
│       ├── dbo.DocumentSeries.md
│       ├── dbo.Document.md
│       ├── dbo.DocumentProduct.md
│       └── dbo.DocumentStatus.md
├── 02_dto/
│   ├── README.md
│   ├── spis_dto.md
│   └── (per DTO — po ukończeniu eksploracji)
├── 03_linq/
│   ├── README.md
│   └── (zapytania per serwis)
├── 04_zapytania_bezposrednie/
│   └── README.md
├── 05_automapper/
│   ├── README.md
│   ├── BankAccountProfile.md
│   ├── DocumentProductProfile.md
│   ├── DocumentProfile.md
│   ├── DocumentSeriesProfile.md
│   ├── DocumentStatusProfile.md
│   ├── FirmProfile.md
│   └── ProductProfile.md
└── 06_skrypty/
    ├── README.md
    └── DbSeeder.md                       ← seed DocumentType + DocumentStatus przy starcie
```

## Kluczowe dokumenty

- [`01_db/erd_globalny.md`](01_db/erd_globalny.md) — diagram ERD całej bazy
- [`01_db/spis_schem_i_tabel.md`](01_db/spis_schem_i_tabel.md) — lista tabel z opisami
- [`02_dto/spis_dto.md`](02_dto/spis_dto.md) — lista wszystkich DTO

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
