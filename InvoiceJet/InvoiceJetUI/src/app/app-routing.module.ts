import { NgModule } from "@angular/core";
import { Router, RouterModule, Routes } from "@angular/router";
import { LoginComponent } from "./components/login/login.component";
import { DashboardComponent } from "./components/dashboard/dashboard.component";
import { AuthGuard } from "./guards/auth.guard";
import { RegisterComponent } from "./components/register/register.component";
import { FirmDetailsComponent } from "./components/firm/firm-details/firm-details.component";
import { AuthService } from "./services/auth.service";
import { ClientsComponent } from "./components/firm/clients/clients.component";
import { BankAccountsComponent } from "./components/firm/bank-accounts/bank-accounts.component";
import { ProductsComponent } from "./components/products/products.component";
import { DocumentSeriesComponent } from "./components/document-series/document-series.component";
import { AddOrEditInvoiceComponent } from "./components/invoices/add-or-edit-invoice/add-or-edit-invoice.component";
import { InvoicesComponent } from "./components/invoices/invoices.component";
import { InvoiceStornosComponent } from "./components/invoice-stornos/invoice-stornos.component";
import { InvoiceProformasComponent } from "./components/invoice-proformas/invoice-proformas.component";
import { AddOrEditInvoiceProformaComponent } from "./components/invoice-proformas/add-or-edit-invoice-proforma/add-or-edit-invoice-proforma.component";
import { AddOrEditInvoiceStornosComponent } from "./components/invoice-stornos/add-or-edit-invoice-stornos/add-or-edit-invoice-stornos.component";

const routes: Routes = [
  { path: "login", component: LoginComponent },
  { path: "register", component: RegisterComponent },
  {
    path: "dashboard",
    component: DashboardComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/firm-details",
    component: FirmDetailsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/clients",
    component: ClientsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/bank-accounts",
    component: BankAccountsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/products",
    component: ProductsComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/document-series",
    component: DocumentSeriesComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/invoices",
    component: InvoicesComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/add-invoice",
    component: AddOrEditInvoiceComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/invoice-proformas",
    component: InvoiceProformasComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/invoice-stornos",
    component: InvoiceStornosComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/add-invoice-proforma",
    component: AddOrEditInvoiceProformaComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/edit-invoice/:id",
    component: AddOrEditInvoiceComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/edit-invoice-proforma/:id",
    component: AddOrEditInvoiceProformaComponent,
    canActivate: [AuthGuard],
  },
  {
    path: "dashboard/edit-invoice-storno/:id",
    component: AddOrEditInvoiceStornosComponent,
    canActivate: [AuthGuard],
  },
  { path: "**", component: DashboardComponent, canActivate: [AuthGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
