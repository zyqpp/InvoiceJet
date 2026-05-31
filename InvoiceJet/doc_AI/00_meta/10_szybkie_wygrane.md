# Szybkie wygrane (Quick Wins) — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Opis

Lista napraw możliwych do wykonania w 1-2 godzinach, które znacząco poprawiają jakość systemu.

---

## 🟢 30 minut lub mniej

### QW-01: Napraw GenerateInvoicePdf (1 linia kodu!)

```csharp
// PRZED (błędne):
var document = new InvoiceDocument(data);

// PO (poprawne):
var invoiceDoc = InvoiceDocumentFactory.Create(dbDocument.DocumentTypeId, data);
```

**Plik:** `DocumentService.cs` → metoda `GenerateInvoicePdf`  
**Efekt:** Proformy i storna generują prawidłowy PDF

---

### QW-02: Napraw TransformToStorno atomowość (3 linie)

```csharp
// PRZED (błędne — CompleteAsync wewnątrz pętli):
foreach (var documentId in documentIds) {
    var document = await ...GetByIdAsync(documentId);
    document.DocumentTypeId = 3;
    await ...UpdateAsync(document);
    await _unitOfWork.CompleteAsync(); // ← przenieść poza pętlę!
}

// PO (poprawne):
foreach (var documentId in documentIds) {
    var document = await ...GetByIdAsync(documentId);
    document.DocumentTypeId = 3;
    await ...UpdateAsync(document);
}
await _unitOfWork.CompleteAsync(); // ← jeden zapis na końcu
```

**Plik:** `DocumentService.cs` → metoda `TransformToStorno`  
**Efekt:** Atomowa konwersja — albo wszystko albo nic

---

### QW-03: Usuń console.log z produkcji (2 linie)

```typescript
// Usuń lub zabezpiecz:
// console.log(invoiceAmounts);  ← USUŃ
// console.log(incomeAmounts);   ← USUŃ
```

**Plik:** `src/app/components/dashboard/dashboard.component.ts`  
**Efekt:** Brak wycieku danych biznesowych w narzędziach deweloperskich

---

### QW-04: CORS — dodaj produkcyjny origin (1 linia)

```csharp
// Program.cs — dodaj URL frontu produkcyjnego:
policy.WithOrigins(
    "http://localhost:4200",
    "https://twoja-aplikacja.azurestaticapps.net"  // ← DODAJ
)
```

**Plik:** `InvoiceJet.Presentation/Program.cs`  
**Efekt:** Aplikacja działa z produkcyjnej domeny frontendu

---

## 🟡 1-2 godziny

### QW-05: Napraw CASCADE DELETE konta bankowego (1 migracja)

Zmień relację `Document.BankAccountId` z `CASCADE` na `RESTRICT`:

```csharp
// EF Core configuration:
modelBuilder.Entity<Document>()
    .HasOne(d => d.BankAccount)
    .WithMany(ba => ba.Documents)
    .HasForeignKey(d => d.BankAccountId)
    .OnDelete(DeleteBehavior.Restrict); // ← zmień z Cascade na Restrict
```

Uruchom nową migrację: `dotnet ef migrations add FixBankAccountCascadeDelete`  
**Efekt:** Usunięcie konta nie usuwa faktur — użytkownik dostaje błąd i musi ręcznie przenieść faktury

---

### QW-06: Napraw UNIQUE INDEX produktu (1 migracja)

Zmień z globalnego UNIQUE na composite UNIQUE `(UserFirmId, Name)`:

```csharp
modelBuilder.Entity<Product>()
    .HasIndex(p => new { p.UserFirmId, p.Name })  // ← composite
    .IsUnique();
// Usuń stary: .HasIndex(p => p.Name).IsUnique();
```

**Efekt:** Dwóch użytkowników może mieć produkt o tej samej nazwie

---

### QW-07: Wydłuż czas JWT do 60 minut

```csharp
// AuthService.cs → CreateToken():
expires: DateTime.UtcNow.AddMinutes(60) // ← zmień z 10 na 60
```

**Efekt:** Użytkownicy nie muszą logować się co 10 minut  
**Uwaga:** Nie rozwiązuje problemu braku refresh token, ale znacząco poprawia UX

---

## 📊 ROI szybkich wygranych

| ID | Wysiłek | Efekt | ROI |
|---|---|---|---|
| QW-01 | 5 min | Krytyczny bug PDF naprawiony | 🔥🔥🔥 |
| QW-02 | 5 min | Krytyczny bug atomowości naprawiony | 🔥🔥🔥 |
| QW-03 | 2 min | Bezpieczeństwo danych | 🔥🔥 |
| QW-04 | 2 min | Produkcja działa | 🔥🔥🔥 |
| QW-05 | 60 min | Zapobieganie utracie danych | 🔥🔥🔥 |
| QW-06 | 60 min | Poprawna izolacja produktów | 🔥🔥 |
| QW-07 | 2 min | Znacząca poprawa UX | 🔥🔥🔥 |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
