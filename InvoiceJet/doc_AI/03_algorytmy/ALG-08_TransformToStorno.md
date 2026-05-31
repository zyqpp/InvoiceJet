# Algorytm: Konwersja dokumentów na storno (TransformToStorno)

| Atrybut | Wartość |
|---|---|
| ID | ALG-08 |
| Nazwa | Transform To Storno |
| Kategoria | Logika biznesowa |
| Pliki | `DocumentService.cs › TransformToStorno()` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Cel

Masowa zmiana typu istniejących dokumentów na fakturę storno (DocumentTypeId=3). Realizuje biznesową operację "anulowania" dokumentów.

## Kod źródłowy

```csharp
// DocumentService › TransformToStorno
public async Task TransformToStorno(int[] documentIds)
{
    foreach (var documentId in documentIds)
    {
        var document = await _unitOfWork.Documents.GetByIdAsync(documentId);
        if (document == null) continue; // lub throw?

        document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice; // = 3
        await _unitOfWork.Documents.UpdateAsync(document);
        await _unitOfWork.CompleteAsync(); // ← WEWNĄTRZ pętli!
    }
}
```

## Sekwencja dla N dokumentów

```
Dla każdego documentId w [id1, id2, id3]:
  1. GetByIdAsync(documentId)
  2. document.DocumentTypeId = 3
  3. UpdateAsync(document)
  4. CompleteAsync()  ← osobna transakcja dla każdego dokumentu
```

## Wartości enum

```csharp
public enum DocumentTypeEnum {
    Invoice = 1,
    ProformaInvoice = 2,
    StornoInvoice = 3
}
```

## Anomalie

| # | Anomalia |
|---|---|
| STORNO-01 | **KRYTYCZNE:** `CompleteAsync()` wewnątrz pętli — brak atomowości; przy błędzie w N-tym ID, dokumenty 1..N-1 są już przekonwertowane |
| STORNO-02 | Brak walidacji czy dokument należy do zalogowanego użytkownika |
| STORNO-03 | Tylko zmiana `DocumentTypeId` — numer dokumentu zostaje bez zmian (brak numeru storno) |
| STORNO-04 | Brak zmiany `DocumentStatusId` — storno może mieć status "Zapłacona" (niespójność semantyczna) |
| STORNO-05 | `int[]` bez `[FromBody]` na kontrolerze — potencjalny problem z deserializacją żądania |

## Poprawna implementacja (referencja)

```csharp
// Zalecany pattern — jedna transakcja
public async Task TransformToStorno(int[] documentIds)
{
    var documents = await _unitOfWork.Documents
        .GetByIdsAsync(documentIds); // batch fetch

    foreach (var doc in documents)
        doc.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice;

    await _unitOfWork.CompleteAsync(); // JEDEN zapis na końcu
}
```

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
