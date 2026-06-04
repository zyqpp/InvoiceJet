# Struktura katalogowa — frontend (InvoiceJetUI)

Katalog główny projektu: `InvoiceJet/InvoiceJetUI/`

Spis wygenerowany na podstawie struktury plików i folderów w repozytorium. Pominięto katalogi generowane lokalnie (`node_modules`, `dist`, `.angular`), jeśli występują po `npm install` / `ng build`.

---

## Drzewo katalogów i plików

```
InvoiceJetUI/
├── .editorconfig
├── .gitignore
├── angular.json
├── package.json
├── package-lock.json
├── README.md
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.spec.json
│
└── src/
    ├── favicon.ico
    ├── index.html
    ├── main.ts
    ├── styles.scss
    │
    ├── app/
    │   ├── app-routing.module.ts
    │   ├── app.component.html
    │   ├── app.component.scss
    │   ├── app.component.spec.ts
    │   ├── app.component.ts
    │   ├── app.module.ts
    │   │
    │   ├── components/
    │   │   ├── dashboard/
    │   │   │   ├── dashboard.component.html
    │   │   │   ├── dashboard.component.scss
    │   │   │   └── dashboard.component.ts
    │   │   │
    │   │   ├── document-series/
    │   │   │   ├── document-series.component.html
    │   │   │   ├── document-series.component.scss
    │   │   │   ├── document-series.component.spec.ts
    │   │   │   ├── document-series.component.ts
    │   │   │   └── add-or-edit-document-series-dialog/
    │   │   │       ├── add-or-edit-document-series-dialog.component.html
    │   │   │       ├── add-or-edit-document-series-dialog.component.scss
    │   │   │       ├── add-or-edit-document-series-dialog.component.spec.ts
    │   │   │       └── add-or-edit-document-series-dialog.component.ts
    │   │   │
    │   │   ├── firm/
    │   │   │   ├── add-edit-client-dialog/
    │   │   │   │   ├── add-edit-client-dialog.component.html
    │   │   │   │   ├── add-edit-client-dialog.component.scss
    │   │   │   │   └── add-edit-client-dialog.component.ts
    │   │   │   ├── bank-accounts/
    │   │   │   │   ├── bank-accounts.component.html
    │   │   │   │   ├── bank-accounts.component.scss
    │   │   │   │   ├── bank-accounts.component.spec.ts
    │   │   │   │   ├── bank-accounts.component.ts
    │   │   │   │   └── add-or-edit-bank-account-dialog/
    │   │   │   │       ├── add-or-edit-bank-account-dialog.component.html
    │   │   │   │       ├── add-or-edit-bank-account-dialog.component.scss
    │   │   │   │       ├── add-or-edit-bank-account-dialog.component.spec.ts
    │   │   │   │       └── add-or-edit-bank-account-dialog.component.ts
    │   │   │   ├── clients/
    │   │   │   │   ├── clients.component.html
    │   │   │   │   ├── clients.component.scss
    │   │   │   │   └── clients.component.ts
    │   │   │   └── firm-details/
    │   │   │       ├── firm-details.component.html
    │   │   │       ├── firm-details.component.scss
    │   │   │       └── firm-details.component.ts
    │   │   │
    │   │   ├── invoice-proformas/
    │   │   │   ├── invoice-proformas.component.html
    │   │   │   ├── invoice-proformas.component.scss
    │   │   │   ├── invoice-proformas.component.spec.ts
    │   │   │   ├── invoice-proformas.component.ts
    │   │   │   └── add-or-edit-invoice-proforma/
    │   │   │       ├── add-or-edit-invoice-proforma.component.html
    │   │   │       ├── add-or-edit-invoice-proforma.component.scss
    │   │   │       ├── add-or-edit-invoice-proforma.component.spec.ts
    │   │   │       └── add-or-edit-invoice-proforma.component.ts
    │   │   │
    │   │   ├── invoice-stornos/
    │   │   │   ├── invoice-stornos.component.html
    │   │   │   ├── invoice-stornos.component.scss
    │   │   │   ├── invoice-stornos.component.spec.ts
    │   │   │   ├── invoice-stornos.component.ts
    │   │   │   └── add-or-edit-invoice-stornos/
    │   │   │       ├── add-or-edit-invoice-stornos.component.html
    │   │   │       ├── add-or-edit-invoice-stornos.component.scss
    │   │   │       ├── add-or-edit-invoice-stornos.component.spec.ts
    │   │   │       └── add-or-edit-invoice-stornos.component.ts
    │   │   │
    │   │   ├── invoices/
    │   │   │   ├── invoices.component.html
    │   │   │   ├── invoices.component.scss
    │   │   │   ├── invoices.component.spec.ts
    │   │   │   ├── invoices.component.ts
    │   │   │   ├── add-or-edit-invoice/
    │   │   │   │   ├── add-or-edit-invoice.component.html
    │   │   │   │   ├── add-or-edit-invoice.component.scss
    │   │   │   │   ├── add-or-edit-invoice.component.spec.ts
    │   │   │   │   └── add-or-edit-invoice.component.ts
    │   │   │   └── base-invoice/
    │   │   │       ├── base-invoice.component.ts
    │   │   │       └── date-validator.ts
    │   │   │
    │   │   ├── login/
    │   │   │   ├── login.component.html
    │   │   │   ├── login.component.scss
    │   │   │   └── login.component.ts
    │   │   │
    │   │   ├── navbar/
    │   │   │   ├── navbar.component.html
    │   │   │   ├── navbar.component.scss
    │   │   │   └── navbar.component.ts
    │   │   │
    │   │   ├── pdf-viewer/
    │   │   │   ├── pdf-viewer.component.html
    │   │   │   ├── pdf-viewer.component.scss
    │   │   │   └── pdf-viewer.component.ts
    │   │   │
    │   │   ├── products/
    │   │   │   ├── products.component.html
    │   │   │   ├── products.component.scss
    │   │   │   ├── products.component.ts
    │   │   │   └── add-or-edit-product-dialog/
    │   │   │       ├── add-or-edit-product-dialog.component.html
    │   │   │       ├── add-or-edit-product-dialog.component.scss
    │   │   │       ├── add-or-edit-product-dialog.component.spec.ts
    │   │   │       └── add-or-edit-product-dialog.component.ts
    │   │   │
    │   │   ├── register/
    │   │   │   ├── register.component.html
    │   │   │   ├── register.component.scss
    │   │   │   ├── register.component.spec.ts
    │   │   │   └── register.component.ts
    │   │   │
    │   │   ├── sidebar/
    │   │   │   ├── sidebar.component.html
    │   │   │   ├── sidebar.component.scss
    │   │   │   └── sidebar.component.ts
    │   │   │
    │   │   └── token-expired-dialog/
    │   │       ├── token-expired-dialog.component.html
    │   │       ├── token-expired-dialog.component.scss
    │   │       ├── token-expired-dialog.component.spec.ts
    │   │       └── token-expired-dialog.component.ts
    │   │
    │   ├── enums/
    │   │   └── Currency.ts
    │   │
    │   ├── guards/
    │   │   └── auth.guard.ts
    │   │
    │   ├── material/
    │   │   └── material.module.ts
    │   │
    │   ├── models/
    │   │   ├── IBankAccount.ts
    │   │   ├── ICurrency.ts
    │   │   ├── IDashboardStats.ts
    │   │   ├── IDocument.ts
    │   │   ├── IDocumentAutofill.ts
    │   │   ├── IDocumentProduct.ts
    │   │   ├── IDocumentProductRequest.ts
    │   │   ├── IDocumentRequest.ts
    │   │   ├── IDocumentSeries.ts
    │   │   ├── IDocumentStatus.ts
    │   │   ├── IDocumentTableRecord.ts
    │   │   ├── IDocumentType.ts
    │   │   ├── IFirm.ts
    │   │   ├── ILoginUser.ts
    │   │   ├── IMonthlyTotal.ts
    │   │   ├── IProduct.ts
    │   │   └── IRegisterUser.ts
    │   │
    │   └── services/
    │       ├── auth.service.ts
    │       ├── bank-account.service.ts
    │       ├── document-series.service.ts
    │       ├── document.service.ts
    │       ├── firm.service.ts
    │       ├── product.service.ts
    │       ├── sidebar.service.ts
    │       ├── user.service.ts
    │       └── interceptor/
    │           ├── auth.interceptor.ts
    │           └── error.interceptor.ts
    │
    ├── assets/
    │   └── .gitkeep
    │
    └── environments/
        ├── environment.ts
        └── environment.prod.ts
```

---

## Podsumowanie — rozszerzenia plików

| Rozszerzenie | Liczba plików | Typ |
|--------------|---------------|-----|
| `.ts` | 74 | TypeScript (komponenty, serwisy, modele, konfiguracja; w tym pliki `.spec.ts`) |
| `.html` | 24 | Szablony komponentów Angular + `index.html` |
| `.scss` | 24 | Style komponentów + `styles.scss` |
| `.json` | 6 | Konfiguracja Angular / npm / TypeScript |
| `.ico` | 1 | Favicon |
| `.gitkeep` | 1 | Plik zachowujący pusty katalog `assets` |
| `.md` | 1 | README projektu UI |
| `.editorconfig` | 1 | Ustawienia edytora |
| `.gitignore` | 1 | Wykluczenia Git |

**Łącznie plików w repozytorium (bez `node_modules`, `dist`, `.angular`):** 133

---

## Katalogi pomijane (nie w repozytorium / generowane)

Poniższe katalogi mogą pojawić się lokalnie, ale nie są częścią źródeł w repozytorium:

- `node_modules/` — zależności npm
- `dist/` — wynik `ng build`
- `.angular/` — cache Angular CLI
