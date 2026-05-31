# FAQ dla deweloperów — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

---

## Pytania ogólne

### Jak działa autoryzacja?

JWT token wystawiany przy logowaniu/rejestracji, ważny **10 minut** (uwaga: bardzo krótko!). Angular dołącza go do każdego żądania przez `JwtInterceptor`. Backend weryfikuje przez `[Authorize]` attribute. Klucz w `AppSettings:Token`. Szczegóły: `ALG-01_JwtAuthentication.md`, `ALG-04_JwtTokenCreation.md`.

---

### Jak uzyskać userId w backendzie?

```csharp
var userId = int.Parse(User.FindFirst("userId")!.Value);
```

`userId` to custom claim dodany do JWT w `AuthService.CreateToken()`.

---

### Co to jest UserFirm i dlaczego jest potrzebne?

`UserFirm` to tabela pośrednicząca łącząca `User` z `Firm`. Jeden użytkownik ma jeden `UserFirm`. Wszystkie zasoby (produkty, konta bankowe, faktury) są powiązane z `UserFirmId`, nie z `UserId`. Dzięki temu możliwe jest rozszerzenie do modelu wieloużytkownikowego (wiele osób w jednej firmie) bez zmian logiki zasobów. Szczegóły: `ALG-10_DataIsolationPattern.md`, `dbo.UserFirm_relations.md`.

---

### Dlaczego konto bankowe nie może być usunięte bez utraty faktur?

To jest **znany błąd (A-KRIT-01)**. FK `Document.BankAccountId` ma `ON DELETE CASCADE`. Naprawka w `00_meta/10_szybkie_wygrane.md → QW-05`.

---

### Dlaczego numery dokumentów mogą się duplikować?

**Race condition** — `DocumentSeries.CurrentNumber` inkrementowany bez blokady. Przy dwóch równoległych żądaniach oba mogą wygenerować ten sam numer. Szczegóły: `ALG-02_DocumentNumberGeneration.md`.

---

### Jak działa generowanie PDF?

**Dwa różne endpointy z różnym zachowaniem:**
- `POST /Document/GenerateInvoicePdf` — BŁĘDNY: hardkoduje `new InvoiceDocument()`, zawsze faktura zwykła
- `POST /Document/GetPdfStream` — POPRAWNY: używa `InvoiceDocumentFactory`, zwraca właściwy typ

Używaj `GetPdfStream`. Szczegóły: `ALG-07_PdfGeneration.md`, `P-12_GeneratePdf.md`.

---

### Dlaczego AutoMapper `DocumentProfile` ma kod LINQ inline?

Zamiast osobnego `CreateMap<DocumentProduct, DocumentProductRequestDto>()`, kod mapowania pozycji dokumentu jest wbudowany bezpośrednio w lambdę. To anomalia (AM-06). Wymaga uwagi przy zmianie pól `DocumentProductRequestDto`.

---

### Co to jest `CompleteAsync()`?

Alias dla `SaveChangesAsync()` z wzorca Unit of Work. `_unitOfWork.CompleteAsync()` = `dbContext.SaveChangesAsync()`. Każdy serwis zapisuje zmiany przez `CompleteAsync()`.

---

### Jak dodać nowy endpoint?

1. Dodaj metodę w `I{Nazwa}Service.cs` (interfejs)
2. Zaimplementuj w `Application/Services/Impl/{Nazwa}Service.cs`
3. Dodaj endpoint w `Presentation/Controllers/{Nazwa}Controller.cs`
4. Jeśli nowe wyjątki domenowe → dodaj do `Domain/Exceptions/` + mapuj w `ExceptionMiddleware.cs`
5. Jeśli nowe DTO → dodaj w `Application/DTOs/` + profil w `Application/MappingProfiles/`
6. Zarejestruj DI w `Program.cs` jeśli nowe serwisy

---

### Jak uruchomić migracje EF Core?

```bash
cd InvoiceJetAPI/InvoiceJet.Presentation
dotnet ef migrations add NazwaMigracji --project ../InvoiceJet.Infrastructure
dotnet ef database update
```

Lub z poziomu Package Manager Console w Visual Studio.

---

### Gdzie jest konfiguracja ANAF?

W `appsettings.json`:
```json
"AppSettings": {
  "AnafApiUrl": "https://webservicesp.anaf.ro/PlatitorTvaRest/api/v8/ws/tva"
}
```

Szczegóły integracji: `04_api_i_integracje/02_anaf/ANAF_integracja.md`.

---

### Jak działa walidacja hasła?

Regex: `^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$`  
Wymagane: wielka+mała litera, cyfra, znak specjalny z zestawu `@$!%*?&`, min. 8 znaków.  
Walidacja TYLKO na backendzie. Szczegóły: `ALG-03_PasswordHashingVerification.md`.

---

### Dlaczego produkty różnych użytkowników nie mogą mieć tej samej nazwy?

**Znany błąd (A-WYS-05)**: `Product.Name` ma globalny UNIQUE INDEX zamiast composite `(UserFirmId, Name)`. Naprawka: `00_meta/10_szybkie_wygrane.md → QW-06`.

---

### Jak sprawdzić wszystkie znane anomalie?

→ `_slowniki/slownik_anomalii.md` — 28 anomalii w 4 kategoriach  
→ `00_meta/07_dług_techniczny.md` — 14 pozycji długu technicznego z wysiłkiem naprawy  
→ `06_role_i_uprawnienia/audyt_bezpieczenstwa.md` — audyt bezpieczeństwa

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
