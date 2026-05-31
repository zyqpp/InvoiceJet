# AddInitialDocumentSeries — algorytm inicjalizacji serii dokumentów

| Pole | Wartość |
|---|---|
| ID | ALG-Dedykowane-InicjalizacjaSeriDokumentow |
| Kategoria | dedykowane |
| Metoda | `DocumentSeriesService.AddInitialDocumentSeries()` |
| Wywoływana z | `FirmService.ManageUserFirmRelation()` — tylko gdy user dodaje **pierwszą** firmę |
| Ostatnia walidacja | 2026-05-31 |

---

## Co robi

Przy dodawaniu pierwszej firmy przez użytkownika automatycznie tworzy domyślne serie numeracji dokumentów dla wszystkich trzech typów: Faktura, Proforma i Storno. Dzięki temu użytkownik może od razu wystawiać dokumenty bez ręcznej konfiguracji serii.

---

## Kiedy jest wywoływana

```
AddFirm()
  └── ManageUserFirmRelation(firmId, isClient)
        └── if (user.ActiveUserFirm == null)   ← tylko dla PIERWSZEJ firmy
              └── AddInitialDocumentSeries(newUserFirm)
```

Dla każdej kolejnej firmy (gdy `user.ActiveUserFirm != null`) — NIE jest wywoływana.

---

## Jakie serie są tworzone

Na podstawie seedowanych typów dokumentów ([dbo.DocumentType](../../05_model_danych/01_db/dbo/dbo.DocumentType.md)):

| DocumentTypeId | Nazwa | Tworzona seria |
|---|---|---|
| 1 | Factura (Faktura) | seria domyślna, `FirstNumber=1` |
| 2 | Factura Proforma (Proforma) | seria domyślna, `FirstNumber=1` |
| 3 | Factura Storno (Storno) | seria domyślna, `FirstNumber=1` |

→ Szczegóły seedowania typów: [seed_typow_dokumentow.md](seed_typow_dokumentow.md)

---

## Model danych — tabela DocumentSeries

| Kolumna | Wartość przy inicjalizacji | Opis |
|---|---|---|
| `SeriesName` | `""` lub domyślna nazwa | Prefiks numeru |
| `FirstNumber` | `1` | Numer startowy |
| `CurrentNumber` | `1` | Numer bieżący |
| `IsDefault` | `true` | Czy domyślna dla typu |
| `DocumentTypeId` | 1, 2 lub 3 | Typ dokumentu |
| `UserFirmId` | `newUserFirm.UserFirmId` | Właściciel |

→ [dbo.DocumentSeries](../../05_model_danych/01_db/dbo/dbo.DocumentSeries.md)

---

## Powiązane

| Typ | Dokument |
|---|---|
| Algorytm | [zarzadzanie_relacja_userfirm.md](zarzadzanie_relacja_userfirm.md) — wywołujący |
| Algorytm | [generowanie_numeru_dokumentu.md](generowanie_numeru_dokumentu.md) — używa serii do numerowania |
| Algorytm | [seed_typow_dokumentow.md](seed_typow_dokumentow.md) — dane wejściowe (typy dokumentów) |
| Model | [dbo.DocumentSeries](../../05_model_danych/01_db/dbo/dbo.DocumentSeries.md) |
| Ekran | [Serie dokumentów](../../01_ekrany/serie_dokumentow/ekran.md) |
