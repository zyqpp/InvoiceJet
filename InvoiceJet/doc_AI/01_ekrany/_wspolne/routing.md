# Konfiguracja routingu Angular — InvoiceJet

| Atrybut | Wartość |
|---|---|
| Plik | `src/app/app-routing.module.ts` |
| Ostatnia walidacja | 2026-05-31 |
| Autor | Agent Claudiusz Sonte 4.6 max |

## Pełna mapa tras

```typescript
const routes: Routes = [
    // Trasy publiczne
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },

    // Trasy chronione (AuthGuard)
    {
        path: 'dashboard',
        component: DashboardLayoutComponent,
        canActivate: [AuthGuard],
        children: [
            { path: '', component: DashboardComponent },                                    // EKRAN-03
            { path: 'firm-details', component: FirmDetailsComponent },                      // EKRAN-04
            { path: 'clients', component: ClientsComponent },                               // EKRAN-05
            { path: 'bank-accounts', component: BankAccountsComponent },                    // EKRAN-06
            { path: 'products', component: ProductsComponent },                             // EKRAN-07
            { path: 'document-series', component: DocumentSeriesComponent },                // EKRAN-08
            { path: 'invoices', component: InvoicesComponent },                             // EKRAN-09
            { path: 'add-invoice', component: AddOrEditInvoiceComponent },                  // EKRAN-10
            { path: 'edit-invoice/:id', component: AddOrEditInvoiceComponent },             // EKRAN-10
            { path: 'invoice-proformas', component: InvoiceProformasComponent },            // EKRAN-11
            { path: 'add-invoice-proforma', component: AddOrEditInvoiceProformaComponent }, // EKRAN-12
            { path: 'edit-invoice-proforma/:id', component: AddOrEditInvoiceProformaComponent }, // EKRAN-12
            { path: 'invoice-stornos', component: InvoiceStornosComponent },               // EKRAN-13
            { path: 'add-invoice-storno', component: AddOrEditInvoiceStornosComponent },   // EKRAN-14
            { path: 'edit-invoice-storno/:id', component: AddOrEditInvoiceStornosComponent }, // EKRAN-14
        ]
    },

    // Domyślne przekierowanie
    { path: '', redirectTo: '/login', pathMatch: 'full' },
    { path: '**', redirectTo: '/login' }
];
```

## Mapowanie tras → ekranów

| Trasa | EKRAN | Komponent |
|---|---|---|
| `/login` | EKRAN-01 | `LoginComponent` |
| `/register` | EKRAN-02 | `RegisterComponent` |
| `/dashboard` | EKRAN-03 | `DashboardComponent` |
| `/dashboard/firm-details` | EKRAN-04 | `FirmDetailsComponent` |
| `/dashboard/clients` | EKRAN-05 | `ClientsComponent` |
| `/dashboard/bank-accounts` | EKRAN-06 | `BankAccountsComponent` |
| `/dashboard/products` | EKRAN-07 | `ProductsComponent` |
| `/dashboard/document-series` | EKRAN-08 | `DocumentSeriesComponent` |
| `/dashboard/invoices` | EKRAN-09 | `InvoicesComponent` |
| `/dashboard/add-invoice` | EKRAN-10 | `AddOrEditInvoiceComponent` |
| `/dashboard/edit-invoice/:id` | EKRAN-10 | `AddOrEditInvoiceComponent` |
| `/dashboard/invoice-proformas` | EKRAN-11 | `InvoiceProformasComponent` |
| `/dashboard/add-invoice-proforma` | EKRAN-12 | `AddOrEditInvoiceProformaComponent` |
| `/dashboard/edit-invoice-proforma/:id` | EKRAN-12 | `AddOrEditInvoiceProformaComponent` |
| `/dashboard/invoice-stornos` | EKRAN-13 | `InvoiceStornosComponent` |
| `/dashboard/add-invoice-storno` | EKRAN-14 | `AddOrEditInvoiceStornosComponent` |
| `/dashboard/edit-invoice-storno/:id` | EKRAN-14 | `AddOrEditInvoiceStornosComponent` |

## AuthGuard

```typescript
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
    constructor(private router: Router, private jwtHelper: JwtHelperService) {}

    canActivate(): boolean {
        const token = localStorage.getItem('authToken');
        if (!token || this.jwtHelper.isTokenExpired(token)) {
            this.router.navigate(['/login']);
            return false;
        }
        return true;
    }
}
```

Stosowany na wszystkich trasach `/dashboard/**`. Sprawdza ważność tokenu JWT przy każdej nawigacji.

## DashboardLayoutComponent

Komponent-wrapper dla tras `/dashboard/**`. Renderuje:
- `NavbarComponent` (górna belka)
- `SidebarComponent` (lewe menu)
- `<router-outlet>` (treść strony)

## Rejestr zmian

| Wersja | Data | Autor | Opis |
|---|---|---|---|
| 1.0 | 2026-05-31 | Agent Claudiusz Sonte 4.6 max | Dokument wstępny. |
