# 01_ekrany — Ekrany aplikacji

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
01_ekrany/
├── README.md                    ← ten plik
├── mapa_przejsc.md              ← globalny diagram przejść między ekranami
├── 00_wspolne/                  ← navbar, sidebar, modale wspólne
│   ├── README.md
│   ├── navbar/
│   │   └── ekran.md
│   ├── sidebar/
│   │   └── ekran.md
│   ├── modale_wspolne/
│   │   ├── token_expired_dialog/
│   │   │   └── modal.md
│   │   └── pdf_viewer/
│   │       └── modal.md
│   └── base_invoice_component/
│       └── ekran.md
├── login/
│   ├── README.md
│   └── ekran.md
├── register/
│   ├── README.md
│   └── ekran.md
├── dashboard/
│   ├── README.md
│   └── ekran.md
├── firma/
│   ├── README.md
│   ├── dane_firmy/
│   │   ├── README.md
│   │   └── ekran.md
│   ├── klienci/
│   │   ├── README.md
│   │   ├── ekran.md
│   │   └── dialog_dodaj_klienta/
│   │       └── modal.md
│   └── konta_bankowe/
│       ├── README.md
│       ├── ekran.md
│       └── dialog_dodaj_konto/
│           └── modal.md
├── produkty/
│   ├── README.md
│   ├── ekran.md
│   └── dialog_dodaj_produkt/
│       └── modal.md
├── serie_dokumentow/
│   ├── README.md
│   ├── ekran.md
│   └── dialog_dodaj_serie/
│       └── modal.md
├── faktury/
│   ├── README.md
│   ├── lista_faktur/
│   │   └── ekran.md
│   └── dodaj_edytuj_fakture/
│       └── ekran.md
├── faktury_proforma/
│   ├── README.md
│   ├── lista_faktur_proforma/
│   │   └── ekran.md
│   └── dodaj_edytuj_fakture_proforma/
│       └── ekran.md
└── faktury_storno/
    ├── README.md
    ├── lista_faktur_storno/
    │   └── ekran.md
    └── dodaj_edytuj_fakture_storno/
        └── ekran.md
```

## Kluczowe dokumenty

- [`mapa_przejsc.md`](mapa_przejsc.md) — diagram przejść między ekranami z uprawnieniami i ścieżkami URL
- [`00_wspolne/base_invoice_component/ekran.md`](00_wspolne/base_invoice_component/ekran.md) — klasa bazowa formularzy dokumentów (faktury, proformy, storna)
- [`00_wspolne/modale_wspolne/token_expired_dialog/modal.md`](00_wspolne/modale_wspolne/token_expired_dialog/modal.md) — globalny dialog wygaśnięcia sesji JWT

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet. |
