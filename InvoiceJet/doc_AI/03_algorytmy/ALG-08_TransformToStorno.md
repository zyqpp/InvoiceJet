# Algorytm: Konwersja dokumentów na storno (TransformToStorno)

| Atrybut | Wartość |
|---|---|
| ID | ALG-08 |
| Nazwa | Transform To Storno |
| Kategoria | Logika biznesowa |
| Pliki | `DocumentService.cs › TransformToStorno()` |
| Ostatnia walidacja | 2026-05-31 (zweryfikowano kod źródłowy) |
| Autor | Agent Claudiusz Sonte 4.6 max |

## ⚠️ Czym jest storno w InvoiceJet — kluczowe ustalenie

> **Storno w InvoiceJet to MUTACJA istniejącego dokumentu, nie utworzenie nowego.**

Operacja `TransformToStorno` zmienia wyłącznie pole `DocumentTypeId` z `1` na `3` na tym samym rekordzie w bazie. **Nie tworzy żadnego nowego dokumentu korygującego.** Oznacza to:

- Oryginalny dokument (faktura) **przestaje istnieć jako faktura** — staje się stornem
- Nie ma referencji storno → oryginał (brak `OriginalDocumentId`)
- Wartości (`UnitPrice`, `TotalPrice`, `Quantity`) pozostają **dodatnie w bazie danych**
- Ujemne wartości na wydruku PDF to efekt wyłącznie szablonu (`-item.Quantity` w kodzie)
- Nie ma podwójnego zapisu księgowego (brak dokumentu rozliczeniowego)

### Jak "zerowanie" faktury działa w praktyce

```
PRZED Transform:
  dbo.Document { Id=5, DocumentTypeId=1, TotalPrice=1000 }
  → widoczny w liście FAKTUR (TypeId=1)
  → liczony w statystykach faktur

PO Transform:
  dbo.Document { Id=5, DocumentTypeId=3, TotalPrice=1000 }  ← te same wartości!
  → widoczny w liście STORN (TypeId=3)
  → NIE jest liczony w statystykach faktur
  → na PDF: wartości wyświetlane ze znakiem minus (tylko wizualnie)
```

**„Zerowanie" następuje przez wykluczenie z filtra TypeId=1** — storned dokument znika ze statystyk faktur, bo `GetDashboardStats` i `GetDocumentTableRecords` filtrują po `DocumentTypeId`. Nie ma żadnej operacji matematycznej na danych.

---

## Kod źródłowy (aktualny — zweryfikowany)

```csharp
// DocumentService.cs › TransformToStorno() — AKTUALNY KOD
public async Task TransformToStorno(int[] documentIds)
{
    var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
    if (activeUserFirmId == null)
        throw new Exception("User firm not found.");

    foreach (var documentId in documentIds)
    {
        var document = await _unitOfWork.Documents.Query()
            .Where(d => d.Id == documentId && d.UserFirmId == activeUserFirmId)  // filtr ownership
            .FirstOrDefaultAsync();

        if (document == null)
            throw new Exception("Document not found.");  // throw, nie continue

        document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;  // JEDYNA zmiana
        await _unitOfWork.Documents.UpdateAsync(document);
        await _unitOfWork.CompleteAsync();  // WEWNĄTRZ pętli — anomalia STORNO-01
    }
}
```

---

## Co NIE jest robione (w porównaniu z poprawnym stornem księgowym)

| Brakująca operacja | Skutek |
|---|---|
| Brak tworzenia nowego dokumentu korygującego | Oryginalny dokument jest nadpisywany, nie anulowany |
| Brak referencji `OriginalDocumentId` | Niemożliwe prześledzenie: które storno dotyczy której faktury |
| Brak negowania wartości w DB | `TotalPrice=1000` przed i po transform — wartości w DB zawsze dodatnie |
| Brak zmiany numeru dokumentu | `FV0001` pozostaje `FV0001` mimo zmiany na storno |
| Brak zmiany `DocumentStatusId` | Storno może mieć status „Paid" — niespójność semantyczna |
| Brak zapisu do tabeli historii/audytu | Zmiana nieodwracalna bez śladu w logach |

---

## Sekwencja dla N dokumentów

```
1. Pobierz activeUserFirmId z JWT (jeden raz, przed pętlą)
2. Dla każdego documentId w [id1, id2, id3]:
   a. Query: Document WHERE Id=documentId AND UserFirmId=activeUserFirmId
   b. Jeśli null → throw Exception("Document not found.")
   c. document.DocumentTypeId = 3
   d. UpdateAsync(document)
   e. CompleteAsync()  ← WEWNĄTRZ PĘTLI (anomalia STORNO-01)
```

## Wartości enum

```csharp
public enum DocumentTypeEnum {
    Invoice = 1,
    ProformaInvoice = 2,
    StornoInvoice = 3
}
```

---

## Anomalie (zaktualizowane po weryfikacji kodu)

| # | Anomalia | Status |
|---|---|---|
| STORNO-01 | **KRYTYCZNE:** `CompleteAsync()` wewnątrz pętli — brak atomowości; przy błędzie w N-tym ID, dokumenty 1..N-1 są już przekonwertowane, brak rollback | ✅ potwierdzona w kodzie |
| STORNO-02 | ~~Brak walidacji właściciela dokumentu~~ — **NAPRAWIONE** w aktualnym kodzie: `WHERE d.UserFirmId == activeUserFirmId` | ❌ nieaktualna (ALG-08 v1.0 miał błąd) |
| STORNO-03 | Zmiana `DocumentTypeId` bez zmiany numeru — `FV0001` pozostaje `FV0001` po przekształceniu na storno | ✅ potwierdzona |
| STORNO-04 | Brak zmiany `DocumentStatusId` — storno może pozostać ze statusem „Paid" | ✅ potwierdzona |
| STORNO-05 | ~~`int[]` bez `[FromBody]`~~ — **NAPRAWIONE**: kontroler MA atrybut `[FromBody] int[] documentIds` | ❌ nieaktualna (ALG-08 v1.0 miał błąd) |
| **STORNO-06** | **ARCHITEKTONICZNIE:** brak podwójnego zapisu — storno to mutacja oryginału, nie nowy dokument korygujący. Brak możliwości jednoczesnego wyświetlenia oryginału i korekty | ✅ nowa, fundamentalna |
| **STORNO-07** | Wartości w DB zawsze dodatnie — negacja wyłącznie wizualna w szablonie PDF. Przy bezpośredniej analizie DB saldo storn wygląda na sumę dodatnią, nie ujemną | ✅ nowa |

---

## Wpływ na statystyki dashboardu

`GetDashboardStats` i `GetMonthlyTotalsAsync` filtrują po `DocumentTypeId`:
```csharp
.Where(d => d.DocumentType!.Id == documentType)  // TypeId=1 lub 2 lub 3
```

Po Transform storned dokument:
- **Znika** z `InvoiceAmount` (TypeId=1 filtr)
- **Pojawia się** w statystykach storn (TypeId=3 filtr) — z wartościami **dodatnimi** w DB

---

## Poprawna implementacja (referencja — minimalna poprawa)

```csharp
// Poprawa 1: jeden CompleteAsync po pętli
public async Task TransformToStorno(int[] documentIds)
{
    var activeUserFirmId = await _unitOfWork.Users.GetUserFirmIdAsync(_userService.GetCurrentUserId());
    if (activeUserFirmId == null)
        throw new Exception("User firm not found.");

    var documents = await _unitOfWork.Documents.Query()
        .Where(d => documentIds.Contains(d.Id) && d.UserFirmId == activeUserFirmId)
        .ToListAsync();

    if (documents.Count != documentIds.Length)
        throw new Exception("One or more documents not found.");

    foreach (var doc in documents)
        doc.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;

    await _unitOfWork.CompleteAsync(); // JEDEN zapis na końcu
}
```

---

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
| 1.1 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Weryfikacja kodu źródłowego: zaktualizowano snippet (stary był nieaktualny), dodano STORNO-06/07, naprawiono STORNO-02/05, dodano sekcję mechanizmu zerowania. |
