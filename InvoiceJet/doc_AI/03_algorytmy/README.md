# 03_algorytmy — Algorytmy

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
03_algorytmy/
├── README.md
├── walidacji/
│   ├── README.md
│   └── walidacja_hasla.md                   ← regex + BCrypt
├── autoryzacyjne/
│   ├── README.md
│   ├── tworzenie_tokenu_jwt.md
│   └── weryfikacja_tokenu_jwt.md
├── generowania_pdf/
│   ├── README.md
│   ├── generuj_pdf_na_dysk.md               ← API-28 (hardcoded InvoiceDocument — bug)
│   └── generuj_pdf_stream.md                ← API-29 (wzorzec fabryki)
├── wyliczeniowe/
│   ├── README.md
│   └── obliczanie_wartosci_dokumentu.md
└── dedykowane/
    ├── README.md
    └── seed_typow_dokumentow.md             ← DbSeeder przy starcie
```

## Kluczowe dokumenty

- [`walidacji/walidacja_hasla.md`](walidacji/walidacja_hasla.md) — regex + BCrypt, dozwolone znaki specjalne
- [`generowania_pdf/generuj_pdf_na_dysk.md`](generowania_pdf/generuj_pdf_na_dysk.md) — bug: hardcoded `InvoiceDocument`

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
