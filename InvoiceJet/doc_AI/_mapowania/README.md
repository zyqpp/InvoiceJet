# _mapowania — Mapy krzyżowe i inwentaryzacje

Opis biznesowy: [do uzupełnienia w fazie 11]

## Drzewo zawartości

```
_mapowania/
├── README.md
│
│   ── INWENTARYZACJE (Faza 1) ──
├── inwentaryzacja_encji.md          ← 10 encji DB
├── inwentaryzacja_dto.md            ← 14 DTO
├── inwentaryzacja_api.md            ← 31 endpointów
├── inwentaryzacja_ekranow.md        ← 16 tras / 13 komponentów
├── inwentaryzacja_rol.md            ← 1 rola (User)
├── inwentaryzacja_linq.md           ← 5 zapytań LINQ
├── inwentaryzacja_automappera.md    ← 7 profili AutoMapper
├── inwentaryzacja_algorytmow.md     ← 10 algorytmów
├── inwentaryzacja_procesow.md       ← 15 procesów technicznych
│
│   ── MAPY KRZYŻOWE (Faza 11) ──
├── mapa_db_dto_ekrany.md            ← kolumna DB ↔ pole DTO ↔ pole UI (M-02)
├── mapa_api_dto_linq_db.md          ← endpoint ↔ DTO ↔ LINQ ↔ tabela (M-03)
├── mapa_uc_bpmn.md                  ← UC ↔ procesy biznesowe (M-04)
├── mapa_warstwowa.md                ← UC → ekran → API → DB (M-05)
├── pokrycie_testow.md               ← UC / ekran ↔ scenariusze testowe (M-06)
├── mapa_rol_ekranow_operacji.md     ← rola × ekran × operacja (M-07)
├── mapa_uprawnien_api.md            ← uprawnienie ↔ endpointy (M-08)
├── mapa_integracji_procesow.md      ← integracja (ANAF) ↔ procesy (M-09)
└── mapa_przejsc_ekranow.md          ← diagram przejść między ekranami (M-10)
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 0.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Szkielet + inwentaryzacje (Faza 1). |
| 0.2 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dodano inwentaryzacja_linq.md (brakujące M-01). |
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Wszystkie 9 map krzyzowych M-02..M-10 ukonczone. README zaktualizowane. |
