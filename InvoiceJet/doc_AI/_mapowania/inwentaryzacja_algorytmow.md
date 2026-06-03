# Inwentaryzacja algorytmów

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |
| Źródło | `InvoiceJetAPI/InvoiceJet.Application/Services/Impl/`, `InvoiceJet.Infrastructure/` |

## Lista algorytmów (10)

| ID | Nazwa algorytmu | Lokalizacja | Dokument | Status |
|---|---|---|---|---|
| ALG-01 | Generowanie JWT | `AuthService.cs › CreateToken` | [link](../03_algorytmy/ALG-01_GenerowanieJWT.md) | szkic |
| ALG-02 | Walidacja hasła | `AuthService.cs › RegisterUser` | [link](../03_algorytmy/ALG-02_WalidacjaHasla.md) | szkic |
| ALG-03 | Hashowanie hasła BCrypt | `AuthService.cs › RegisterUser` + `LoginUser` | [link](../03_algorytmy/ALG-03_HashowanieBCrypt.md) | szkic |
| ALG-04 | Generowanie numeru dokumentu | `DocumentService.cs › AddDocument` + `IncreaseDocumentSeriesNumber` | [link](../03_algorytmy/ALG-04_GenerowanieNumeruDok.md) | szkic |
| ALG-05 | Aktualizacja produktów dokumentu | `DocumentService.cs › UpdateDocumentProducts` | [link](../03_algorytmy/ALG-05_AktualizacjaProduktow.md) | szkic |
| ALG-06 | Kalkulacja statystyk miesięcznych | `DocumentService.cs › GetMonthlyTotalsAsync` | [link](../03_algorytmy/ALG-06_KalkulacjaMiesiecznych.md) | szkic |
| ALG-07 | TransformToStorno | `DocumentService.cs › TransformToStorno` | [link](../03_algorytmy/ALG-07_TransformToStorno.md) | szkic |
| ALG-08 | Pobieranie danych z ANAF | `FirmService.cs › GetFirmDataFromAnaf` | [link](../03_algorytmy/ALG-08_PobieranieANAF.md) | szkic |
| ALG-09 | Generowanie PDF (zapis na dysk) | `PdfGenerationService.cs › GenerateInvoicePdf` | [link](../03_algorytmy/ALG-09_GenerowaniePDF.md) | szkic |
| ALG-10 | Generowanie PDF (strumień) | `PdfGenerationService.cs › GetInvoicePdfStream` | [link](../03_algorytmy/ALG-10_StreamPDF.md) | szkic |

## Szczegóły algorytmów

---

### ALG-01 Generowanie JWT

**Plik:** `AuthService.cs › CreateToken(User user)`  
**Wywołanie:** po RegisterUser i LoginUser

**Kroki:**
1. Zbudowanie listy `Claims`:
   - `"userId"` = `user.Id.ToString()`
   - `"firstName"` = `user.FirstName`
   - `"lastName"` = `user.LastName`
   - `"email"` = `user.Email`
   - `ClaimTypes.Role` = `"User"`
2. Klucz symetryczny z `AppSettings:Token` (UTF-8 bytes)
3. Algorytm podpisywania: `HmacSha512Signature`
4. Tworzenie `JwtSecurityToken` z `expires = DateTime.UtcNow.AddMinutes(10)`
5. Serializacja przez `JwtSecurityTokenHandler().WriteToken(token)`
6. Zwrot tokenu jako `string`

**Uwaga:** Token wygasa po **10 minutach** — bardzo krótka sesja. Frontend sprawdza wygaśnięcie przez `JwtHelperService.isTokenExpired()`.

---

### ALG-02 Walidacja hasła

**Plik:** `AuthService.cs › RegisterUser`  
**Regex:**
```
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$
```

**Wymagania hasła:**
- Minimum 8 znaków
- Przynajmniej jedna mała litera (`[a-z]`)
- Przynajmniej jedna wielka litera (`[A-Z]`)
- Przynajmniej jedna cyfra (`\d`)
- Przynajmniej jeden znak specjalny z zestawu `@$!%*?&`
- Dozwolone tylko znaki: `[A-Za-z\d@$!%*?&]`

**Wyjątek przy naruszeniu:** `InvalidPasswordException`  
**Wyjątek przy niezgodności:** `PasswordMismatchException`

---

### ALG-03 Hashowanie hasła BCrypt

**Plik:** `AuthService.cs › RegisterUser` i `LoginUser`  
**Biblioteka:** `BCrypt.Net-Next` (alias `BC = BCrypt.Net.BCrypt`)

**Rejestracja:**
```csharp
PasswordHash = BC.HashPassword(userDto.Password)
```
Generuje hash z wbudowanym salt (domyślny work factor — prawdopodobnie 10).

**Logowanie:**
```csharp
BC.Verify(userDto.Password, user.PasswordHash)
```
Zwraca `bool` — jeśli `false` → `IncorrectPasswordException`.

---

### ALG-04 Generowanie numeru dokumentu

**Plik:** `DocumentService.cs › AddDocument` + `IncreaseDocumentSeriesNumber`

**Format numeru:**
```
{SeriesName}{CurrentNumber:D4}
// Przykład: SeriesName="FV", CurrentNumber=5 → "FV0005"
```

**Kod:**
```csharp
DocumentNumber = documentRequestDto.DocumentSeries?.SeriesName +
                 documentRequestDto.DocumentSeries?.CurrentNumber.ToString("D4")
```

**Inkrementacja po zapisie:**
```csharp
private async Task IncreaseDocumentSeriesNumber(int documentSeriesId)
{
    var docSeries = await _unitOfWork.DocumentSeries.GetByIdAsync(documentSeriesId);
    docSeries!.CurrentNumber++;
    await _unitOfWork.DocumentSeries.UpdateAsync(docSeries);
}
```

**Uwaga:** Numer generowany z `CurrentNumber` **przed** inkrementacją. `CurrentNumber` jest inkrementowany po zapisie dokumentu. Nie ma mechanizmu blokowania race condition przy jednoczesnym tworzeniu dokumentów.

---

### ALG-05 Aktualizacja produktów dokumentu

**Plik:** `DocumentService.cs › UpdateDocumentProducts(int documentId, List<DocumentProductRequestDto>, int userFirmId)`

**Kroki:**
1. Pobierz wszystkie istniejące `DocumentProduct` dla `documentId`
2. `RemoveRangeAsync` — fizyczne usunięcie poprzednich pozycji
3. Dla każdego produktu z DTO:
   - Jeśli `dto.Id > 0` → szukaj produktu po `Name` i `UserFirmId` (jeśli nie znaleziony: `Exception("Product not found.")`)
   - Jeśli `dto.Id == 0` → mapuj DTO → `Product` przez AutoMapper i dodaj nowy produkt do DB
   - Utwórz `DocumentProduct` z `Quantity`, `UnitPrice`, `TotalPrice`
   - Akumuluj `totalInvoicePrice += UnitPrice * Quantity` i `totalInvoicePriceWithTva += TotalPrice`
4. Pobierz dokument i zaktualizuj `UnitPrice = totalInvoicePrice`, `TotalPrice = totalInvoicePriceWithTva`

**Anomalie:**
- Lookup produktu po `Name` (nie po `Id`) — jeśli istnieją dwa produkty o tej samej nazwie, `FirstOrDefaultAsync` zwróci losowy
- `Exception("Product not found.")` — plain `Exception`, nie domenowy wyjątek

---

### ALG-06 Kalkulacja statystyk miesięcznych

**Plik:** `DocumentService.cs › GetMonthlyTotalsAsync(int userFirmId, int year, int documentType)`

**Zapytanie LINQ:**
```csharp
.Where(d => d.UserFirmId == userFirmId 
         && d.IssueDate.Year == year 
         && d.DocumentType!.Id == documentType)
.GroupBy(d => new { month = d.IssueDate.Month })
.Select(group => new MonthlyTotalDto
{
    Month = group.Key.month,
    InvoiceAmount = group.Sum(d => d.TotalPrice),
    IncomeAmount  = group.Sum(d => d.DocumentStatusId == (int)DocumentStatusEnum.Paid 
                                   ? d.TotalPrice 
                                   : 0)
})
.OrderBy(x => x.Month)
```

**Wynik:** Lista maks. 12 `MonthlyTotalDto`. Miesiące bez dokumentów są pomijane (brak wypełnienia zerami).

**Pola:**
- `InvoiceAmount` = suma wszystkich faktur w miesiącu (`TotalPrice`)
- `IncomeAmount` = suma tylko opłaconych faktur (`DocumentStatusId == Paid`)

---

### ALG-07 TransformToStorno

**Plik:** `DocumentService.cs › TransformToStorno(int[] documentIds)`

**Kroki:**
```csharp
foreach (var documentId in documentIds)
{
    var document = await ... .FirstOrDefaultAsync();
    if (document == null) throw new Exception("Document not found.");
    document.DocumentTypeId = (int)DocumentTypeEnum.StornoInvoice; // = 3
    await _unitOfWork.Documents.UpdateAsync(document);
    await _unitOfWork.CompleteAsync(); // ← SaveChanges wewnątrz pętli
}
```

**Anomalie:**
- `CompleteAsync()` wywoływany **wewnątrz pętli** — każdy dokument w oddzielnej transakcji; przy błędzie N-tego dokumentu, dokumenty 1..N-1 są już przetransformowane
- Brak domenowego wyjątku — plain `Exception`
- Brak sprawdzenia czy dokument należy do aktywnej firmy usera (sprawdzany przez `UserFirmId` w WHERE, ale brak eksplicytnego wyjątku)

---

### ALG-08 Pobieranie danych z ANAF

**Plik:** `FirmService.cs › GetFirmDataFromAnaf` (szczegóły do weryfikacji z kodem)

**Cel:** HTTP GET do rumuńskiego API ANAF (`https://webservicesp.anaf.ro/...`) na podstawie numeru CUI.

**Zwraca:** dane firmy (nazwa, adres, kod pocztowy) do wypełnienia formularza.

> [UWAGA: Szczegóły URL i struktury odpowiedzi ANAF do weryfikacji z kodem serwisu FirmService.cs]

---

### ALG-09 Generowanie PDF (zapis na dysk)

**Plik:** `PdfGenerationService.cs › GenerateInvoicePdf(DocumentRequestDto documentRequestDto)`  
**Biblioteka:** QuestPDF Community

**Kroki:**
1. Tworzy `new InvoiceDocument(documentRequestDto)` — **hardcoded** klasa faktury zwykłej
2. Wywołuje `document.GeneratePdf(filePath)` — zapisuje plik na dysk serwera
3. Zwraca — klient nie dostaje pliku (tylko potwierdzenie)

**Anomalia (ALG-09-A):** Zawsze `new InvoiceDocument()` — ignoruje `DocumentRequestDto.DocumentType.Id`. Dla proform i storn generuje błędnie fakturę zwykłą.

---

### ALG-10 Generowanie PDF (strumień bajtów)

**Plik:** `PdfGenerationService.cs › GetInvoicePdfStream(DocumentRequestDto documentRequestDto)`  
**Biblioteka:** QuestPDF Community

**Kroki:**
1. Na podstawie `DocumentType.Id` wybiera odpowiednią klasę dokumentu (factory pattern):
   - `DocumentTypeEnum.Invoice` → `InvoiceDocument`
   - `DocumentTypeEnum.ProformaInvoice` → (klasa proformy)
   - `DocumentTypeEnum.StornoInvoice` → (klasa storno)
2. Wywołuje `document.GeneratePdfStream()` — zwraca `byte[]`
3. Zwraca strumień do `DocumentService.GetInvoicePdfStream()`

> [UWAGA: Dokładny kod switch/factory do weryfikacji z `PdfGenerationService.cs`]

---

## Anomalie algorytmów

| # | Anomalia |
|---|---|
| ALG-A01 | JWT wygasa po 10 minutach — bardzo krótka sesja; brak mechanizmu refresh token |
| ALG-A02 | ALG-05: lookup produktu po `Name`, nie po `Id` — ryzyko błędu gdy dwa produkty o tej samej nazwie |
| ALG-A03 | ALG-07: `CompleteAsync()` w pętli — brak atomowości operacji TransformToStorno |
| ALG-A04 | ALG-04: brak mechanizmu blokowania concurrent access do `DocumentSeries.CurrentNumber` (race condition) |
| ALG-A05 | ALG-09: `GenerateInvoicePdf` hardcodes `new InvoiceDocument()` — zawsze generuje fakturę zwykłą, ignoruje typ dokumentu |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Inwentaryzacja 10 algorytmów z cytatami kodu i analizą anomalii. |
