# Serwisy Angular — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Lista serwisów

| Serwis | Plik | Odpowiada za |
|---|---|---|
| `AuthService` | `src/app/services/auth.service.ts` | Logowanie, rejestracja |
| `FirmService` | `src/app/services/firm.service.ts` | Zarządzanie firmami |
| `BankAccountService` | `src/app/services/bank-account.service.ts` | Konta bankowe |
| `ProductService` | `src/app/services/product.service.ts` | Produkty |
| `DocumentSeriesService` | `src/app/services/document-series.service.ts` | Serie numeracji |
| `DocumentService` | `src/app/services/document.service.ts` | Dokumenty, PDF, statystyki |
| `ClientService` | `src/app/services/client.service.ts` | Klienci (firmy) |
| `NotificationService` | `src/app/services/notification.service.ts` | Toastr powiadomienia |

## Wzorzec serwisu Angular

```typescript
@Injectable({ providedIn: 'root' })
export class DocumentService {
    private apiUrl = `${environment.apiUrl}/Document`;

    constructor(private http: HttpClient) {}

    getTableRecords(documentTypeId: number): Observable<IDocumentTableRecord[]> {
        return this.http.get<IDocumentTableRecord[]>(
            `${this.apiUrl}/GetTableRecords/${documentTypeId}`
        );
    }

    add(document: IDocumentRequest): Observable<any> {
        return this.http.post(`${this.apiUrl}/Add`, document);
    }

    getPdfStream(documentId: number): Observable<Blob> {
        return this.http.post(
            `${this.apiUrl}/GetPdfStream`,
            { documentId },
            { responseType: 'blob' }
        );
    }
}
```

## Interfejsy TypeScript

| Interfejs | Odpowiada DTO | Plik |
|---|---|---|
| `IUser` | — | `models/user.model.ts` |
| `IFirm` | `FirmRequestDto` | `models/firm.model.ts` |
| `IBankAccount` | `BankAccountRequestDto` | `models/bank-account.model.ts` |
| `IProduct` | `ProductRequestDto` | `models/product.model.ts` |
| `IDocumentSeries` | `DocumentSeriesRequestDto` | `models/document-series.model.ts` |
| `IDocument` | `DocumentRequestDto` | `models/document.model.ts` |
| `IDocumentProduct` | `DocumentProductRequestDto` | `models/document.model.ts` |
| `IDocumentTableRecord` | `DocumentTableRecordDto` | `models/document.model.ts` |
| `IDocumentAutofillInfo` | `DocumentAutofillInfoDto` | `models/document.model.ts` |
| `IDashboardStats` | `DashboardStatsDto` | `models/dashboard.model.ts` |

## Obsługa błędów (wzorzec)

```typescript
// Komponent — obsługa błędu
this.documentService.add(document).subscribe({
    next: () => {
        this.router.navigate(['/dashboard/invoices']);
        this.notificationService.success('Document saved');
    },
    error: (err) => {
        this.notificationService.error(err.error?.message || 'Unknown error');
    }
});
```

## Helpers

| Plik | Opis |
|---|---|
| `src/app/helpers/jwt.interceptor.ts` | Dołącza `Authorization: Bearer {token}` do każdego HTTP request |
| `src/app/helpers/auth.guard.ts` | Blokuje dostęp jeśli JWT wygasł (sprawdza `isTokenExpired`) |

## Package.json (kluczowe zależności)

| Pakiet | Wersja | Rola |
|---|---|---|
| `@angular/core` | 16.2.12 | Framework Angular |
| `@angular/material` | 16.2.14 | UI komponenty |
| `@auth0/angular-jwt` | 5.2.0 | `JwtHelperService.isTokenExpired()` |
| `ng2-charts` | 5.0.3 | Wykres liniowy (Chart.js) |
| `ngx-toastr` | 16.2.0 | Powiadomienia toast |

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
