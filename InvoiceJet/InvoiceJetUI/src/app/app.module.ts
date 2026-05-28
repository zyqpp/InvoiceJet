import { NgModule, importProvidersFrom } from "@angular/core";
import { BrowserModule } from "@angular/platform-browser";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import {
  BrowserAnimationsModule,
  provideAnimations,
} from "@angular/platform-browser/animations";
import { HttpClientModule } from "@angular/common/http";
import { HTTP_INTERCEPTORS } from "@angular/common/http";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { LoginComponent } from "./components/login/login.component";
import { NavbarComponent } from "./components/navbar/navbar.component";
import { JwtHelperService, JWT_OPTIONS } from "@auth0/angular-jwt";
import { DashboardComponent } from "./components/dashboard/dashboard.component";
import { RegisterComponent } from "./components/register/register.component";
import { SidebarComponent } from "./components/sidebar/sidebar.component";
import { FirmDetailsComponent } from "./components/firm/firm-details/firm-details.component";
import { MaterialModule } from "./material/material.module";
import { AuthInterceptor } from "./services/interceptor/auth.interceptor";
import { ClientsComponent } from "./components/firm/clients/clients.component";
import { AddEditClientDialogComponent } from "./components/firm/add-edit-client-dialog/add-edit-client-dialog.component";
import { BankAccountsComponent } from "./components/firm/bank-accounts/bank-accounts.component";
import { AddOrEditBankAccountDialogComponent } from "./components/firm/bank-accounts/add-or-edit-bank-account-dialog/add-or-edit-bank-account-dialog.component";
import { ProductsComponent } from "./components/products/products.component";
import { AddOrEditProductDialogComponent } from "./components/products/add-or-edit-product-dialog/add-or-edit-product-dialog.component";
import { DocumentSeriesComponent } from "./components/document-series/document-series.component";
import { AddOrEditDocumentSeriesDialogComponent } from "./components/document-series/add-or-edit-document-series-dialog/add-or-edit-document-series-dialog.component";
import { InvoicesComponent } from "./components/invoices/invoices.component";
import { AddOrEditInvoiceComponent } from "./components/invoices/add-or-edit-invoice/add-or-edit-invoice.component";
import { MAT_FORM_FIELD_DEFAULT_OPTIONS } from "@angular/material/form-field";
import { TokenExpiredDialogComponent } from "./components/token-expired-dialog/token-expired-dialog.component";
import { PdfViewerComponent } from "./components/pdf-viewer/pdf-viewer.component";
import { NgChartsModule } from "ng2-charts";
import { InvoiceProformasComponent } from "./components/invoice-proformas/invoice-proformas.component";
import { AddOrEditInvoiceProformaComponent } from "./components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component";
import { InvoiceStornosComponent } from "./components/invoice-stornos/invoice-stornos.component";
import { ErrorInterceptor } from "./services/interceptor/error.interceptor";
import { ToastrModule } from "ngx-toastr";
import { AddOrEditInvoiceStornosComponent } from "./components/invoice-stornos/add-or-edit-invoice-stornos/add-or-edit-invoice-stornos.component";
import { MatPaginatorModule } from "@angular/material/paginator";

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    NavbarComponent,
    DashboardComponent,
    RegisterComponent,
    SidebarComponent,
    FirmDetailsComponent,
    ClientsComponent,
    AddEditClientDialogComponent,
    BankAccountsComponent,
    AddOrEditBankAccountDialogComponent,
    ProductsComponent,
    AddOrEditProductDialogComponent,
    DocumentSeriesComponent,
    AddOrEditDocumentSeriesDialogComponent,
    InvoicesComponent,
    AddOrEditInvoiceComponent,
    TokenExpiredDialogComponent,
    PdfViewerComponent,
    InvoiceProformasComponent,
    AddOrEditInvoiceProformaComponent,
    InvoiceStornosComponent,
    AddOrEditInvoiceStornosComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MaterialModule,
    HttpClientModule,
    NgChartsModule,
    MatPaginatorModule,
    ToastrModule.forRoot({
      timeOut: 4000,
      positionClass: "toast-bottom-right",
      preventDuplicates: true,
      progressBar: true,
    }),
  ],
  providers: [
    provideAnimations(),
    { provide: JWT_OPTIONS, useValue: JWT_OPTIONS },
    {
      provide: MAT_FORM_FIELD_DEFAULT_OPTIONS,
      useValue: { appearance: "outline" },
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: ErrorInterceptor,
      multi: true,
    },
    JwtHelperService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
